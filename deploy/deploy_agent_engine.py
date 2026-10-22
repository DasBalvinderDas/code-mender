#!/usr/bin/env python3
"""Deploy the CodeMender scan agent to Vertex AI Agent Engine with ADK's own deploy command. No GCS bucket.

  python deploy/deploy_agent_engine.py             # first time: creates; afterwards: updates the engine saved in .env
  python deploy/deploy_agent_engine.py --new       # create a separate new engine
  python deploy/deploy_agent_engine.py --dry-run   # show the command and settings, deploy nothing

Settings come from the repository-root .env (copy .env.example): GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION,
AGENT_SERVICE_ACCOUNT, CODEMENDER_MODEL, CODEMENDER_RUNNER_URL (optional). After deploying it saves AGENT_ENGINE_RESOURCE in .env and asks the agent a
test question; if the engine does not start, it prints the engine's logs.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import RESOURCE_RE, ROOT, explain, read_env, resolve_project, write_env  # noqa: E402

AGENT_DIR = ROOT / "codemender_agent"
RUNTIME_KEYS = ["CODEMENDER_MODEL", "CODEMENDER_RUNNER_URL"]


def pick_update_id(args, env: dict):
    """Which existing engine to update: the one saved in .env, unless --new."""
    if args.new:
        return None
    saved = env.get("AGENT_ENGINE_RESOURCE")
    return saved.split("/")[-1] if saved and RESOURCE_RE.fullmatch(saved) else None


def build_config(env: dict) -> dict:
    config = {"display_name": "codemender-scan-agent",
              "description": "Scans a git repository for security vulnerabilities and returns a PDF and Markdown report "
                             "with findings and suggested fixes.",
              "env_vars": {k: env[k] for k in RUNTIME_KEYS if env.get(k)}}
    if env.get("AGENT_SERVICE_ACCOUNT"):
        config["service_account"] = env["AGENT_SERVICE_ACCOUNT"]
    return config


def deploy_command(project, region, config_path, update_id):
    cmd = ["adk", "deploy", "agent_engine", f"--project={project}", f"--region={region}",
           f"--agent_engine_config_file={config_path}"]
    if update_id:
        cmd.append(f"--agent_engine_id={update_id}")
    return cmd + [str(AGENT_DIR)]


def run_deploy(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=str(ROOT))
    out = []
    for line in proc.stdout:
        print(line, end="")
        out.append(line)
    proc.wait()
    return proc.returncode, "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--region")
    ap.add_argument("--new", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-smoke-test", action="store_true")
    args = ap.parse_args()

    env = read_env()
    project = resolve_project(args.project)
    region = args.region or env.get("GOOGLE_CLOUD_LOCATION") or "us-central1"
    if (AGENT_DIR / ".env").exists():
        sys.exit(f"\n{AGENT_DIR / '.env'} exists. `adk deploy` reads a .env next to the agent and it would override the "
                 "settings. Delete it (the repository-root .env is the one to use) and run this again.")
    update_id = pick_update_id(args, env)
    config = build_config(env)
    print(f"Project: {project}   Region: {region}")
    print(f"Runs as: {config.get('service_account', 'the Agent Engine service agent (default)')}")
    print(f"Model:   {config['env_vars'].get('CODEMENDER_MODEL', '(agent default)')}")
    print(f"Engine:  {'real CodeMender via the runner ' + config['env_vars']['CODEMENDER_RUNNER_URL'] if config['env_vars'].get('CODEMENDER_RUNNER_URL') else 'built-in quick scan only (no CODEMENDER_RUNNER_URL set)'}")
    print(f"{'Updating engine ' + update_id if update_id else 'Creating a new engine'}")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(config, f, indent=2)
    cmd = deploy_command(project, region, f.name, update_id)
    print("\nCommand:\n  " + " ".join(cmd))
    if args.dry_run:
        print("\n(dry run: nothing deployed)")
        return

    print("\nDeploying (several minutes: it builds a container image) ...\n")
    code, text = run_deploy(cmd)
    if code != 0 and update_id and ("NOT_FOUND" in text or "is not found" in text):
        print(f"\nSaved engine {update_id} no longer exists. Creating a new one ...\n")
        code, text = run_deploy(deploy_command(project, region, f.name, None))
    found = RESOURCE_RE.findall(text)
    resource = found[-1] if found else None
    if resource:
        write_env({"AGENT_ENGINE_RESOURCE": resource})
        print(f"\nSaved AGENT_ENGINE_RESOURCE={resource} to .env")
    if code != 0:
        hint = explain(text, project)
        print(f"\n{hint}" if hint else "\nDeployment failed (see the output above).")
        if resource:
            import agent_engine_logs
            print("\nRecent engine logs:\n" + agent_engine_logs.recent_logs(project, resource, errors_only=False))
        sys.exit(1)
    if resource and not args.no_smoke_test:
        print("\nSmoke test: asking the deployed agent to scan a small public repo ...\n")
        r = subprocess.run([sys.executable, str(ROOT / "deploy" / "query_agent_engine.py"),
                            "Analyse https://github.com/DasBalvinderDas/code-mender, folder demo/vulnerable-app. Reply in two lines.",
                            "--resource", resource, "--project", project])
        if r.returncode != 0:
            sys.exit("\nThe engine deployed, but the smoke test failed (details above). Try the query script yourself, and if the agent errors: python deploy/agent_engine_logs.py")
    print('\nTalk to it:  python deploy/query_agent_engine.py "Analyse https://github.com/juice-shop/juice-shop"')


if __name__ == "__main__":
    main()
