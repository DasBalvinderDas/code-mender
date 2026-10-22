#!/usr/bin/env python3
"""Check the CodeMender runner on its own (no agent involved): start a find-only run on a repo and follow it to the end.

  python deploy/check_runner.py                                   # scans demo/vulnerable-app of this project's repo
  python deploy/check_runner.py --repo https://github.com/juice-shop/juice-shop --subdir routes --deep

Uses CODEMENDER_RUNNER_URL from .env and your gcloud identity (the script adds you as an invoker when it deploys the runner).
"""
import argparse
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import read_env  # noqa: E402


def identity_token() -> str:
    r = subprocess.run(["gcloud", "auth", "print-identity-token"], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit("Could not get an identity token. Run: gcloud auth login   (error: " + r.stderr.strip()[:200] + ")")
    return r.stdout.strip()


def summarize(result: dict) -> str:
    findings = result.get("findings", [])
    lines = [f"Engine: {result.get('engine')}   repo: {result.get('repo')} {result.get('subdir') or ''}   "
             f"files: {result.get('files_scanned')}   lines: {result.get('lines_scanned')}",
             f"Findings: {len(findings)}   by severity: {dict(Counter(f['severity'] for f in findings))}   "
             f"by status: {dict(Counter(f['status'] for f in findings))}"]
    for f in findings[:15]:
        lines.append(f"  {f['short_id']}  {f['severity']:<8} {f['vuln_type']:<8} {f['file']}:{f.get('start_line')}  {f['title'][:70]}")
    for e in result.get("errors", []):
        lines.append(f"  NOTE: {e}")
    return "\n".join(lines)


def run(client: httpx.Client, base: str, headers: dict, params: dict, wait: int, poll: float = 10.0, out=print) -> int:
    r = client.get(f"{base}/healthz", headers=headers)
    out(f"healthz: {r.status_code}")
    if r.status_code != 200:
        out("The runner did not answer. 401/403 means your identity may not invoke it; 404/5xx means it is not running.")
        return 1
    r = client.post(f"{base}/v1/analyses", json=params, headers=headers)
    if r.status_code >= 400:
        out(f"The runner rejected the request ({r.status_code}): {r.text[:300]}")
        return 1
    job = r.json()["id"]
    out(f"started run {job}")
    deadline, last = time.time() + wait, None
    while time.time() < deadline:
        run_ = client.get(f"{base}/v1/analyses/{job}", headers=headers).json()
        if run_["stage"] != last:
            out(f"  [{run_['status']}] {run_['stage']}")
            last = run_["stage"]
        if run_["status"] == "completed":
            out("\n" + summarize(run_["result"]))
            return 0
        if run_["status"] == "failed":
            out(f"\nFAILED: {run_.get('error')}")
            return 1
        time.sleep(poll)
    out(f"\nStill running after {wait}s; check later with GET {base}/v1/analyses/{job}")
    return 2


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default="https://github.com/DasBalvinderDas/code-mender")
    ap.add_argument("--subdir", default="demo/vulnerable-app")
    ap.add_argument("--ref", default="")
    ap.add_argument("--deep", action="store_true")
    ap.add_argument("--wait", type=int, default=1500, help="seconds to wait for the run")
    ap.add_argument("--url", default=None)
    a = ap.parse_args()
    base = (a.url or read_env().get("CODEMENDER_RUNNER_URL", "")).rstrip("/")
    if not base:
        sys.exit("No runner URL. Deploy it (./deploy/deploy_runner.sh) or pass --url.")
    headers = {"Authorization": f"Bearer {identity_token()}"}
    params = {"repo_url": a.repo, "subdir": a.subdir, "ref": a.ref, "deep": a.deep}
    with httpx.Client(timeout=60) as client:
        sys.exit(run(client, base, headers, params, a.wait))


if __name__ == "__main__":
    main()
