"""Deploy the CodeMender scan agent to Agent Engine as an ADK agent. No GCS bucket needed.

    python deploy/deploy_agent_engine.py --project P --location us-central1 --model <gemini model>
    python deploy/deploy_agent_engine.py ... --update projects/P/locations/L/reasoningEngines/ID    # redeploy in place

Default mode ("source"): the agent's source files are sent inline in the create request (an in-memory tarball) and Agent
Engine imports `codemender_agent.agent:root_agent`. Fallback ("--staging-bucket gs://B"): the classic pickle upload via a
bucket, in case source mode is rejected in your project. Run from the repository root.
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)  # source_packages must be relative paths inside the project directory

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--location", default="us-central1")
ap.add_argument("--model", default="gemini-2.5-flash", help="Gemini model the agent uses (pick one available in your project)")
ap.add_argument("--python-version", default="3.12", help="Python runtime for the engine (3.10-3.14)")
ap.add_argument("--service-account", default="", help="optional runtime service account (needs roles/aiplatform.user)")
ap.add_argument("--update", default="", help="existing resource name to update instead of creating")
ap.add_argument("--staging-bucket", default="", help="FALLBACK ONLY: gs://bucket; uses the classic pickle upload instead of source mode")
a = ap.parse_args()

os.environ["CODEMENDER_MODEL"] = a.model  # read when the agent module is imported, so set it first

import vertexai  # noqa: E402
from vertexai.agent_engines import AdkApp  # noqa: E402

from codemender_agent.agent import root_agent  # noqa: E402

vertexai.init(project=a.project, location=a.location, **({"staging_bucket": a.staging_bucket} if a.staging_bucket else {}))
client = vertexai.Client(project=a.project, location=a.location)

common = {
    "display_name": "CodeMender Scan Agent",
    "description": "Scans a git repository for security vulnerabilities and returns a PDF and Markdown report with findings and suggested fixes.",
    "env_vars": {"CODEMENDER_MODEL": a.model},  # the engine imports the agent at startup, so it reads this
    **({"service_account": a.service_account} if a.service_account else {}),
}

if a.staging_bucket:
    config = {**common, "requirements_file": "requirements.txt", "extra_packages": ["codemender_agent"], "staging_bucket": a.staging_bucket}
    kwargs = {"agent": AdkApp(agent=root_agent, enable_tracing=False)}
else:
    from vertexai._genai import _agent_engines_utils as u

    app = AdkApp(agent=root_agent, enable_tracing=False)  # only used to read the standard ADK operations
    class_methods = [u._to_dict(s) for s in u._generate_class_methods_spec_or_raise(
        agent=app, operations=u._get_registered_operations(agent=app))]
    config = {**common, "source_packages": ["codemender_agent", "requirements.txt"], "entrypoint_module": "codemender_agent.agent",
              "entrypoint_object": "root_agent", "requirements_file": "requirements.txt", "class_methods": class_methods,
              "agent_framework": "google-adk", "python_version": a.python_version}
    kwargs = {}

remote = (client.agent_engines.update(name=a.update, config=config, **kwargs) if a.update
          else client.agent_engines.create(config=config, **kwargs))
print("Deployed:", remote.api_resource.name)
