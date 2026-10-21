"""Deploy the CodeMender analysis agent to Agent Engine as an A2A agent.

    python deploy/deploy_agent_engine.py --project P --location us-central1 --staging-bucket gs://B
    python deploy/deploy_agent_engine.py ... --update <reasoningEngine resource name>   # redeploy in place

Run from the repository root.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import vertexai  # noqa: E402

from codemender_agent.agent_engine_app import build_a2a_agent  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--location", default="us-central1")
ap.add_argument("--staging-bucket", required=True, help="gs://bucket used to stage the package")
ap.add_argument("--model", default="gemini-2.5-flash")
ap.add_argument("--service-account", default="", help="runtime service account (needs aiplatform.user)")
ap.add_argument("--update", default="", help="existing resource name to update instead of creating")
a = ap.parse_args()

vertexai.init(project=a.project, location=a.location, staging_bucket=a.staging_bucket)
client = vertexai.Client(project=a.project, location=a.location)

config = {
    "display_name": "CodeMender Analysis Agent",
    "description": "Security code analysis for a git repo (find / verify plan / fix) with a PDF report. A2A.",
    "requirements_file": "requirements.txt",
    "extra_packages": ["codemender_agent"],
    "staging_bucket": a.staging_bucket,
    "env_vars": {"CODEMENDER_MODEL": a.model},
    # Sessions/tasks are in memory, so keep one instance so follow-up questions hit the same state.
    "min_instances": 1, "max_instances": 1,
    **({"service_account": a.service_account} if a.service_account else {}),
}
agent = build_a2a_agent()
remote = (client.agent_engines.update(name=a.update, agent=agent, config=config) if a.update
          else client.agent_engines.create(agent=agent, config=config))
name = remote.api_resource.name
print("Deployed:", name)
print("A2A endpoint:", f"https://{a.location}-aiplatform.googleapis.com/v1beta1/{name}/a2a")
print("Agent card  :", f"https://{a.location}-aiplatform.googleapis.com/v1beta1/{name}/a2a/v1/card")
