"""How the defect-fix ADK agent (on Agent Engine) calls the CodeMender analysis agent (also on Agent Engine) over A2A.

Set CODEMENDER_RESOURCE to the CodeMender reasoning engine, e.g.
  projects/123/locations/us-central1/reasoningEngines/456
The defect-fix agent's runtime service account needs roles/aiplatform.user on that project.
"""
import os

import google.auth
import google.auth.transport.requests
import httpx
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

LOCATION = os.environ.get("CODEMENDER_LOCATION", "us-central1")
RESOURCE = os.environ["CODEMENDER_RESOURCE"]
BASE = f"https://{LOCATION}-aiplatform.googleapis.com/v1beta1/{RESOURCE}/a2a"


class GoogleAuth(httpx.Auth):
    """Adds a fresh Google access token (ADC / runtime service account) to each request."""

    def __init__(self):
        self._creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    def auth_flow(self, request):
        if not self._creds.valid:
            self._creds.refresh(google.auth.transport.requests.Request())
        request.headers["Authorization"] = f"Bearer {self._creds.token}"
        yield request


codemender = RemoteA2aAgent(
    name="codemender_analysis",
    description="Security analysis of a git repo: vulnerabilities (CWE/OWASP), severity, patches, report links.",
    agent_card=f"{BASE}/v1/card",  # verify this path against your deployed engine (see README)
    httpx_client=httpx.AsyncClient(auth=GoogleAuth(), timeout=900),
)

# Add to your existing defect-fix agent, e.g.:
defect_fix_agent = Agent(
    name="defect_fix_agent",
    model="gemini-2.5-flash",
    instruction="Fix defects. When asked about security, or before fixing a repository, delegate analysis to "
                "codemender_analysis and use its returned findings/patches as input to your fix.",
    sub_agents=[codemender],
)
