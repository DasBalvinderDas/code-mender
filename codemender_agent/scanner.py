"""Repository acquisition and static analysis (find -> verify plan -> fix)."""
from __future__ import annotations

import difflib
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .rules import RULES, Rule

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", "target", "vendor", ".tox",
             # test code: fake credentials and deliberate payloads would drown real findings
             "test", "tests", "__tests__", "spec", "specs", "e2e", "cypress", "fixtures", "__mocks__"}
MAX_FILE_BYTES = 1_000_000
SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SEV_WEIGHT = {"CRITICAL": 10, "HIGH": 6, "MEDIUM": 3, "LOW": 1}
# Language-specific auto-fixes: rule id -> extensions the substitution is valid for (default: any).
_PY = {".py"}
FIX_EXTS = {"CM-INJ-002": _PY, "CM-INJ-003": _PY, "CM-SEC-001": _PY, "CM-CRY-001": _PY, "CM-CRY-002": _PY,
            "CM-CRY-003": _PY, "CM-DES-001": _PY, "CM-NET-001": _PY, "CM-NET-003": _PY, "CM-AUTH-001": _PY,
            "CM-XSS-001": {".js", ".jsx", ".ts", ".tsx", ".mjs"}}
_GITHUB = re.compile(r"^https://([\w.-]+)/[\w.-]+/[\w.-]+(\.git)?/?$")


@dataclass
class Finding:
    id: str
    rule_id: str
    title: str
    severity: str
    cwe: str
    owasp: str
    file: str
    line: int
    snippet: str
    description: str
    remediation: str
    verification_plan: str
    confidence: str
    patch: str = ""  # unified diff, empty when no mechanical fix exists
    status: str = "detected"

    def to_dict(self):
        return asdict(self)


@dataclass
class ScanResult:
    repo: str
    ref: str
    commit: str
    files_scanned: int
    lines_scanned: int
    languages: dict
    findings: list = field(default_factory=list)
    engine: str = "Built-in rule engine (CodeMender-style)"

    @property
    def risk_score(self) -> int:
        return min(100, sum(SEV_WEIGHT[f.severity] for f in self.findings))

    @property
    def by_severity(self) -> dict:
        out = {s: 0 for s in SEV_ORDER}
        for f in self.findings:
            out[f.severity] += 1
        return out


def clone_repo(url: str, ref: str = "", token: str = "") -> tuple[Path, str]:
    """Shallow-clone a repo into a temp dir. Local paths are used as-is."""
    if os.path.isdir(url):
        return Path(url).resolve(), _head(Path(url))
    if not _GITHUB.match(url):
        raise ValueError("repo must be an https git URL (github.com / gitlab.com style) or a local path")
    dest = Path(tempfile.mkdtemp(prefix="cm_repo_"))
    if shutil.which("git") is None:  # e.g. Agent Engine runtime has no git binary
        return _download_tarball(url, ref, token or os.environ.get("GITHUB_TOKEN", ""), dest)
    auth_url = url
    token = token or os.environ.get("GITHUB_TOKEN", "")
    if token:
        auth_url = url.replace("https://", f"https://x-access-token:{token}@", 1)
    cmd = ["git", "clone", "--depth", "1", "--quiet"] + (["--branch", ref] if ref else []) + [auth_url, str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode:
        shutil.rmtree(dest, ignore_errors=True)
        err = r.stderr.replace(token, "***") if token else r.stderr
        raise RuntimeError("git clone failed: " + err)
    return dest, _head(dest)


def _download_tarball(url: str, ref: str, token: str, dest: Path) -> tuple[Path, str]:
    import io
    import tarfile
    import urllib.request
    m = re.match(r"^https://github\.com/([\w.-]+)/([\w.-]+?)(\.git)?/?$", url)
    if not m:
        shutil.rmtree(dest, ignore_errors=True)
        raise RuntimeError("git is not installed on this host; only github.com repositories can be fetched without it")
    req = urllib.request.Request(f"https://api.github.com/repos/{m[1]}/{m[2]}/tarball/{ref}".rstrip("/"),
                                 headers={"User-Agent": "codemender-agent", **({"Authorization": f"Bearer {token}"} if token else {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read(200_000_000)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(dest, filter="data")  # rejects absolute paths, traversal and unsafe links
    except Exception as exc:
        shutil.rmtree(dest, ignore_errors=True)
        raise RuntimeError(f"could not download repository: {exc}") from exc
    top = next(dest.iterdir())
    return top, top.name.rsplit("-", 1)[-1][:7]


def _head(path: Path) -> str:
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() or "n/a"


_TEST_FILE = re.compile(r"(\.(spec|test)\.[a-z]+$|_test\.(go|py|rb|c|cc|cpp)$|(^|/)test_[^/]*\.py$|Test\.java$|Tests\.java$)")


def _iter_files(root: Path):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            p = Path(dp) / f
            if _TEST_FILE.search(f):
                continue
            try:
                if p.stat().st_size <= MAX_FILE_BYTES:
                    yield p
            except OSError:
                continue


def _make_patch(rel: str, lines: list[str], idx: int, rule: Rule) -> str:
    if not rule.fix or Path(rel).suffix.lower() not in FIX_EXTS.get(rule.id, {Path(rel).suffix.lower()}):
        return ""
    pat, repl = rule.fix
    new = pat.sub(repl, lines[idx], count=1)
    if new == lines[idx]:
        return ""
    a, b = lines[:], lines[:]
    b[idx] = new
    return "".join(difflib.unified_diff([x + "\n" for x in a], [x + "\n" for x in b],
                                        f"a/{rel}", f"b/{rel}", n=2))


def scan_path(root: Path, repo: str = "", ref: str = "", commit: str = "") -> ScanResult:
    findings, langs, nfiles, nlines = [], {}, 0, 0
    for p in _iter_files(root):
        ext = p.suffix.lower() if p.suffix else ("." + p.name.lstrip(".")).lower()
        rules = [r for r in RULES if ext in r.exts]
        if not rules:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        lines = text.splitlines()
        nfiles += 1
        nlines += len(lines)
        langs[ext] = langs.get(ext, 0) + 1
        rel = str(p.relative_to(root))
        is_test = bool(re.search(r"(^|/)(tests?|__tests__|spec)(/|$)|\.test\.|_test\.", rel))
        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith(("#", "//", "*", "/*")) and "BEGIN" not in s:
                continue
            for rule in rules:
                if rule.pattern.search(line):
                    fid = hashlib.sha1(f"{rule.id}{rel}{i}".encode()).hexdigest()[:8]
                    conf = "LOW" if is_test else rule.confidence
                    findings.append(Finding(
                        id=f"CM-{fid}", rule_id=rule.id, title=rule.title, severity=rule.severity,
                        cwe=rule.cwe, owasp=rule.owasp, file=rel, line=i + 1, snippet=s[:200],
                        description=rule.description, remediation=rule.remediation,
                        verification_plan=rule.verification, confidence=conf,
                        patch=_make_patch(rel, lines, i, rule)))
    findings.sort(key=lambda f: (SEV_ORDER[f.severity], f.file, f.line))
    return ScanResult(repo or str(root), ref or "default", commit or _head(root), nfiles, nlines, langs, findings)
