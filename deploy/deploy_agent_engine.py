"""Deploy the CodeMender scan agent to Agent Engine as a standard ADK agent (AdkApp).

    python deploy/deploy_agent_engine.py --project P --location us-central1 --staging-bucket gs://B --model <gemini model>
    python deploy/deploy_agent_engine.py ... --update projects/P/locations/L/reasoningEngines/ID   # redeploy in place

Run from the repository root.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--location", default="us-central1")
ap.add_argument("--staging-bucket", required=True, help="gs://bucket used only to upload the deployment package")
ap.add_argument("--model", default="gemini-2.5-flash", help="Gemini model the agent uses (pick one available in your project)")
ap.add_argument("--service-account", default="", help="optional runtime service account (needs roles/aiplatform.user)")
ap.add_argument("--update", default="", help="existing resource name to update instead of creating")
a = ap.parse_args()

os.environ["CODEMENDER_MODEL"] = a.model  # read when the agent module is imported, so set it first

import vertexai  # noqa: E402
from vertexai.agent_engines import AdkApp  # noqa: E402

from codemender_agent.agent import root_agent  # noqa: E402

vertexai.init(project=a.project, location=a.location, staging_bucket=a.staging_bucket)
client = vertexai.Client(project=a.project, location=a.location)

config = {
    "display_name": "CodeMender Scan Agent",
    "description": "Scans a git repository for security vulnerabilities and returns a PDF report with findings and suggested fixes.",
    "requirements_file": "requirements.txt",
    "extra_packages": ["codemender_agent"],
    "staging_bucket": a.staging_bucket,
    **({"service_account": a.service_account} if a.service_account else {}),
}
app = AdkApp(agent=root_agent, enable_tracing=False)
remote = (client.agent_engines.update(name=a.update, agent=app, config=config) if a.update
          else client.agent_engines.create(agent=app, config=config))
print("Deployed:", remote.api_resource.name)
