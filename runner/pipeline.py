"""Runs the real CodeMender `cm` CLI against a fresh clone: init -> find -> report -> verify -> fix -> report.

Every job gets its own clone and its own CM_HOME, because `cm report` lists every finding in state.db, `cm verify`
and `cm fix` reset the scan directory with `git checkout HEAD -- . && git clean -fd`, and `cm verify` runs exploit
scripts on this machine. Command shapes follow the CodeMender CLI codelab; flags that could not be confirmed are noted.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

CM_BIN = os.environ.get("CM_BIN", "cm")
ALLOW_LOCAL = os.environ.get("RUNNER_ALLOW_LOCAL") == "1"  # tests only
GITHUB_RE = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+?(\.git)?/?$")
HEX_ID = re.compile(r"^[0-9a-fA-F][0-9a-fA-F-]{6,35}$")
SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SOURCE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".rs", ".c", ".cc", ".cpp", ".h", ".hpp"}
TIMEOUTS = {"init": 300, "find": int(os.environ.get("CM_FIND_TIMEOUT", 1500)),
            "verify": int(os.environ.get("CM_VERIFY_TIMEOUT", 900)), "fix": int(os.environ.get("CM_FIX_TIMEOUT", 1500)),
            "report": 120}
SECRET_ENV = ("GITHUB_TOKEN", "GH_TOKEN", "GITHUB_PAT", "GITHUB_APP_TOKEN", "GCP_SA_KEY")


class JobError(Exception):
    pass


def verify_fix_enabled() -> bool:
    """`cm verify` runs exploit code and `cm fix` rewrites code, so they stay off unless the operator turns them on."""
    return os.environ.get("RUNNER_ALLOW_VERIFY_FIX") == "1"


def _run(cmd, cwd, env, timeout):
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return 124, (out.decode() if isinstance(out, bytes) else out) + "\n[timed out]"


def validate_request(p: dict) -> dict:
    repo = p.get("repo_url", "")
    if not (GITHUB_RE.match(repo) or (ALLOW_LOCAL and os.path.isdir(repo))):
        raise ValueError("repo_url must be an https://github.com/<owner>/<repo> URL")
    subdir = p.get("subdir", "") or ""
    if subdir.startswith("/") or ".." in Path(subdir).parts:
        raise ValueError("subdir must be a relative path inside the repo")
    ref = p.get("ref", "") or ""
    if ref and not re.match(r"^[\w./-]{1,100}$", ref):
        raise ValueError("invalid ref")
    return {
        "repo_url": repo, "ref": ref, "subdir": subdir, "deep": bool(p.get("deep", False)),
        "verify_top": max(0, min(int(p.get("verify_top", 0)), 10)) if verify_fix_enabled() else 0,
        "fix_top": max(0, min(int(p.get("fix_top", 0)), 5)) if verify_fix_enabled() else 0,
        "verify_fix_requested": bool(int(p.get("verify_top", 0) or 0) or int(p.get("fix_top", 0) or 0)),
        "install_deps": bool(p.get("install_deps", False)), "context": str(p.get("context", ""))[:8000],
        "build_command": str(p.get("build_command", ""))[:300],
    }


def _env(cm_home: Path, workdir: Path, extra_path: str = "") -> dict:
    env = {k: v for k, v in os.environ.items() if k not in SECRET_ENV}
    env.update(CM_HOME=str(cm_home), XDG_CACHE_HOME=str(workdir / ".cache"), PIP_CACHE_DIR=str(workdir / ".cache" / "pip"),
               TMPDIR=str(workdir / "tmp"))
    if extra_path:
        env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    (workdir / "tmp").mkdir(exist_ok=True)
    return env


def _clone(p: dict, workdir: Path) -> tuple[Path, str]:
    dest = workdir / "repo"
    url = p["repo_url"]
    token = os.environ.get("GITHUB_TOKEN", "")
    if token and url.startswith("https://"):
        url = url.replace("https://", f"https://x-access-token:{token}@", 1)
    cmd = ["git", "clone", "--quiet"] + ([] if ALLOW_LOCAL and os.path.isdir(p["repo_url"]) else ["--depth", "1"]) \
        + (["--branch", p["ref"]] if p["ref"] else []) + [url, str(dest)]
    rc, out = _run(cmd, workdir, {**os.environ, "GIT_TERMINAL_PROMPT": "0"}, 300)
    if rc:
        raise JobError("git clone failed: " + out.replace(token, "***")[-500:] if token else "git clone failed: " + out[-500:])
    _, sha = _run(["git", "rev-parse", "--short", "HEAD"], dest, os.environ, 30)
    return dest, sha.strip()


def _detect_build(scan_dir: Path) -> str:
    if any(scan_dir.rglob("*.py")):
        return "python3 -m compileall -q ."
    return "true"  # no toolchain for other languages in the runner image: build validation is effectively off


def _configure(cm_home: Path, env: dict, build_cmd: str, scan_dir: Path):
    rc, out = _run([CM_BIN, "init"], scan_dir, env, TIMEOUTS["init"])
    cfg_path = cm_home / "config.yaml"
    if not cfg_path.exists():
        raise JobError(f"cm init did not create config.yaml (exit {rc}): {out[-400:]}")
    cfg = yaml.safe_load(cfg_path.read_text()) or {}
    cfg.setdefault("vcs", {})["type"] = "git"
    cfg.setdefault("build", {})["command"] = build_cmd
    cfg.setdefault("tools", {}).update(confirm_commands=False, confirm_writes=False)
    cfg_path.write_text(yaml.safe_dump(cfg))


def _cm(args, scan_dir, env, stage, flags=True, log=None):
    """Run a cm command non-interactively (-y --bypass-warning). If the CLI rejects the flags, retry without them."""
    cmd = [CM_BIN, *args] + (["-y", "--bypass-warning"] if flags else [])
    rc, out = _run(cmd, scan_dir, env, TIMEOUTS[stage])
    if rc and flags and re.search(r"unknown (flag|shorthand)|unrecognized|invalid flag", out, re.I):
        rc, out = _run([CM_BIN, *args], scan_dir, env, TIMEOUTS[stage])
    if log:
        log(f"cm {' '.join(args[:1])} exit={rc}")
    return rc, out


def _report(scan_dir: Path, env: dict) -> list[dict]:
    rc, out = _run([CM_BIN, "report", "--format", "json"], scan_dir, env, TIMEOUTS["report"])
    items, dec = None, json.JSONDecoder()
    for m in re.finditer(r"\[", out):  # skip banner/log lines such as "[INFO] ..." until a JSON array decodes
        try:
            val, _ = dec.raw_decode(out[m.start():])
        except ValueError:
            continue
        if isinstance(val, list) and all(isinstance(x, dict) for x in val):
            items = val
            break
    if items is None:
        raise JobError(f"could not read `cm report --format json` output (exit {rc}): {out[-300:]}")
    root = str(scan_dir.resolve())
    return [f for f in items if os.path.realpath(f.get("file_path", "")).startswith(root)]


def _read(path: Path, limit=6000) -> str:
    try:
        return path.read_text(errors="replace")[:limit]
    except OSError:
        return ""


def _count_source(scan_dir: Path) -> tuple[int, int]:
    files = lines = 0
    for p in scan_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in SOURCE_EXT and ".git" not in p.parts:
            files += 1
            try:
                lines += sum(1 for _ in p.open(errors="replace"))
            except OSError:
                pass
    return files, lines


def _pick(findings, statuses, n):
    rows = [f for f in findings if f.get("status", "").upper() in statuses]
    rows.sort(key=lambda f: (SEV_ORDER.get(f.get("severity", "").upper(), 9), -(f.get("confidence") or 0)))
    return rows[:n]


def execute(params: dict, log=lambda m: None) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix="cmjob_"))
    cm_home = workdir / "cm_home"
    result = {"engine": "CodeMender CLI (cm)", "errors": [], "findings": []}
    try:
        log("cloning repository")
        repo_dir, sha = _clone(params, workdir)
        scan_dir = (repo_dir / params["subdir"]).resolve() if params["subdir"] else repo_dir.resolve()
        if repo_dir.resolve() not in [scan_dir, *scan_dir.parents] or not scan_dir.is_dir():
            raise JobError(f"subdir '{params['subdir']}' not found in repository")
        result.update(repo=params["repo_url"], ref=params["ref"] or "default", commit=sha, subdir=params["subdir"])
        if params["verify_fix_requested"] and not verify_fix_enabled():
            result["errors"].append("verify and fix are disabled on this runner (RUNNER_ALLOW_VERIFY_FIX is not set to 1); only find and report ran")
        result["files_scanned"], result["lines_scanned"] = _count_source(scan_dir)

        extra_path = ""
        if params["install_deps"] and (scan_dir / "requirements.txt").exists():
            log("installing python dependencies (opt-in)")
            venv = workdir / "venv"
            _run(["python3", "-m", "venv", str(venv)], workdir, os.environ, 120)
            rc, out = _run([str(venv / "bin" / "pip"), "install", "-q", "-r", "requirements.txt"], scan_dir, os.environ, 600)
            if rc:
                result["errors"].append("dependency install failed; verification may be slower: " + out[-200:])
            extra_path = str(venv / "bin")
        env = _env(cm_home, workdir, extra_path)
        build_cmd = params["build_command"] or _detect_build(scan_dir)
        result["build_command"] = build_cmd
        log("initialising CodeMender workspace")
        _configure(cm_home, env, build_cmd, scan_dir)

        log("cm find (this can take several minutes)")
        extra = shlex.split(os.environ.get("CM_FIND_EXTRA_ARGS", ""))  # optional, for example a sandbox flag if the host needs it
        rc, out = _cm(["find", str(scan_dir)] + (["--deep"] if params["deep"] else []) + extra, scan_dir, env, "find", log=log)
        if rc:
            result["errors"].append(f"cm find exited {rc}: {out[-300:]}")
        findings = _report(scan_dir, env)
        log(f"cm found {len(findings)} findings")

        evidence, diffs = {}, {}
        for f in _pick(findings, {"OPEN"}, params["verify_top"]):
            fid = f["finding_id"]
            if not HEX_ID.match(fid):
                continue
            log(f"cm verify {fid[:8]} (about 3 minutes)")
            rc, out = _cm(["verify", fid], scan_dir, env, "verify", log=log)
            ex = scan_dir / ".exploit"
            evidence[fid] = {"report": _read(ex / "REPORT.md"), "plan": _read(ex / "PLAN.md"), "output_tail": out[-800:]}
            shutil.rmtree(ex, ignore_errors=True)
        findings = _report(scan_dir, env)

        for f in _pick(findings, {"VERIFIED"}, params["fix_top"]):
            fid = f["finding_id"]
            if not HEX_ID.match(fid):
                continue
            log(f"cm fix {fid[:8]} (about 5-7 minutes)")
            args = ["fix"] + (["-c", params["context"]] if params["context"] else []) + [fid]
            rc, out = _cm(args, scan_dir, env, "fix", log=log)
            _, diff = _run(["git", "diff", "--", "."], scan_dir, os.environ, 60)
            diffs[fid] = {"diff": diff[:30000], "output_tail": out[-800:],
                          "build_validated": bool(re.search(r"build and test validation succeeded", out, re.I))}
            _run(["git", "checkout", "HEAD", "--", "."], scan_dir, os.environ, 60)
            _run(["git", "clean", "-fdq"], scan_dir, os.environ, 60)
            snap = scan_dir / ".git"
            if snap.is_symlink():  # cm's snapshot repo; removing it makes the next run snapshot current code
                snap.unlink()
        findings = _report(scan_dir, env)

        root = str(scan_dir)
        for f in findings:
            fid = f["finding_id"]
            rel = os.path.relpath(os.path.realpath(f["file_path"]), root)
            result["findings"].append({
                "finding_id": fid, "short_id": fid[:8], "title": f.get("title", ""), "severity": str(f.get("severity", "")).upper(),
                "confidence": f.get("confidence"), "vuln_type": f.get("vuln_type") or f.get("vuln_id") or "",
                "file": rel, "start_line": f.get("start_line"), "end_line": f.get("end_line"),
                "snippet": (f.get("snippet") or "")[:600], "analysis": (f.get("analysis") or "")[:3000],
                "status": str(f.get("status", "")).upper(), "verification": evidence.get(fid), "fix": diffs.get(fid)})
        result["findings"].sort(key=lambda x: (SEV_ORDER.get(x["severity"], 9), x["file"]))
        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
