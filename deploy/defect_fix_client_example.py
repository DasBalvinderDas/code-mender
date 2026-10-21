"""How the existing defect-fix ADK agent calls the CodeMender analysis agent over A2A.

Add `codemender` as a sub-agent (or wrap with AgentTool) on the defect-fix agent.
For a Cloud Run deployment with IAM auth, give the HTTP client an ID token for the service URL.
"""
import os

import google.auth.transport.requests
import google.oauth2.id_token
import httpx
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

CODEMENDER_URL = os.environ["CODEMENDER_URL"]  # e.g. https://codemender-agent-xxxx.run.app


def _id_token_client() -> httpx.AsyncClient:
    token = google.oauth2.id_token.fetch_id_token(google.auth.transport.requests.Request(), CODEMENDER_URL)
    return httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"}, timeout=900)


codemender = RemoteA2aAgent(
    name="codemender_analysis",
    description="Security analysis of a git repo: vulnerabilities, severity, patches, reports.",
    agent_card=f"{CODEMENDER_URL}/.well-known/agent-card.json",
    httpx_client=_id_token_client(),
)

defect_fix_agent = Agent(
    name="defect_fix_agent",
    model="gemini-2.5-flash",
    instruction="Fix defects. For security questions or before fixing, delegate repo analysis to codemender_analysis "
                "and use the returned patches/findings as input.",
    sub_agents=[codemender],
)
