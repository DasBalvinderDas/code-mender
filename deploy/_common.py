"""Shared helpers for the deploy scripts."""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCE_RE = re.compile(r"projects/[^/\s]+/locations/[^/\s]+/reasoningEngines/\d+")


def read_env(path: Path = ROOT / ".env") -> dict:
    values = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip()
    return values


def write_env(updates: dict, path: Path = ROOT / ".env") -> None:
    """Set KEY=value lines in .env, keeping everything else."""
    lines = path.read_text().splitlines() if path.exists() else []
    for key, value in updates.items():
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                break
        else:
            lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n")


def resolve_project(explicit=None) -> str:
    project = explicit or os.getenv("GOOGLE_CLOUD_PROJECT") or read_env().get("GOOGLE_CLOUD_PROJECT")
    if not project:
        r = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True)
        project = r.stdout.strip()
    if not project:
        sys.exit("No project. Set GOOGLE_CLOUD_PROJECT in .env, pass --project, or run: gcloud config set project <id>")
    return project


def resource_from_env(explicit=None):
    return explicit or os.getenv("AGENT_ENGINE_RESOURCE") or read_env().get("AGENT_ENGINE_RESOURCE")


def explain(message: str, project: str):
    """Turn a Google API error into an actionable hint, or None if it is not a known case."""
    m = message.lower()
    if "service_disabled" in m or "has not been used in project" in m or "is disabled" in m or "api has not been enabled" in m:
        apis = [a for a in dict.fromkeys(re.findall(r"([a-z0-9-]+\.googleapis\.com)", message))
                if a not in ("console.developers.google.com", "console.cloud.google.com")] or ["<the API named in the error>"]
        return "A required API is not enabled. Enable it, wait a minute, run again:\n" + "\n".join(
            f"  gcloud services enable {a} --project {project}" for a in apis)
    if "actas" in m or "iam.serviceaccounts.actas" in m:
        return ("Your account may not run things as that service account. Ask an admin for "
                "Service Account User (roles/iam.serviceAccountUser) on it.")
    if "default credentials" in m or "reauthentication" in m or "invalid_grant" in m:
        return "No usable credentials. Run:  gcloud auth application-default login"
    if "quota project" in m:
        return f"Run:  gcloud auth application-default set-quota-project {project}"
    if "failed to deploy and cannot serve traffic" in m:
        return ("The engine was created but would not start. Read its logs with:\n  python deploy/agent_engine_logs.py\n"
                "(it finds the engine from the error text if you pass --resource <name>) and look at the first error.")
    return None
