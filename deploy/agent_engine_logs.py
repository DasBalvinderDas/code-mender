#!/usr/bin/env python3
"""Show recent logs of the deployed agent, to see why it failed to start or answer.

  python deploy/agent_engine_logs.py                 # engine saved in .env
  python deploy/agent_engine_logs.py --resource projects/.../reasoningEngines/123 --errors-only --full
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import resolve_project, resource_from_env  # noqa: E402


def build_filter(resource: str, errors_only: bool = False) -> str:
    f = ('resource.type="aiplatform.googleapis.com/ReasoningEngine" '
         f'AND resource.labels.reasoning_engine_id="{resource.rstrip("/").split("/")[-1]}"')
    return f + (" AND severity>=ERROR" if errors_only else "")


KEY_WORDS = ("error", "exception", "denied", "permission", "not found", "no module", "cannot", "failed", "traceback")


def key_lines(lines):
    seen, out = set(), []
    for ln in lines:
        if any(k in ln.lower() for k in KEY_WORDS) and ln.strip() not in seen:
            seen.add(ln.strip())
            out.append(ln.strip())
    return "\n".join(out) if out else "\n".join(lines[-15:])


def recent_logs(project, resource, limit=60, errors_only=False, full=False) -> str:
    cmd = ["gcloud", "logging", "read", build_filter(resource, errors_only), f"--project={project}", f"--limit={limit}",
           "--freshness=1d", "--order=desc", "--format=value(timestamp,severity,textPayload,jsonPayload.message,jsonPayload.error)"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return f"(could not read the logs: {r.stderr.strip()[:300]})"
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not lines:
        return "(no log entries found for this engine yet)"
    lines.reverse()
    return "\n".join(lines) if full else key_lines(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--resource")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--errors-only", action="store_true")
    ap.add_argument("--full", action="store_true", help="every line instead of the key lines")
    a = ap.parse_args()
    resource = resource_from_env(a.resource)
    if not resource:
        sys.exit("No engine known. Deploy first, or pass --resource projects/<p>/locations/<region>/reasoningEngines/<id>")
    print(recent_logs(resolve_project(a.project), resource, a.limit, a.errors_only, a.full))


if __name__ == "__main__":
    main()
