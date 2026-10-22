"""A2A server: `uvicorn codemender_agent.a2a_app:a2a_app --host 0.0.0.0 --port 8080`.

The agent card is served at /.well-known/agent-card.json. Set PUBLIC_URL to the
deployed https URL so the card advertises the right endpoint.
"""
import os
from urllib.parse import urlparse

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from .agent import root_agent

_u = urlparse(os.environ.get("PUBLIC_URL", "http://localhost:8080"))
a2a_app = to_a2a(root_agent, host=_u.hostname or "localhost",
                 port=_u.port or (443 if _u.scheme == "https" else 80), protocol=_u.scheme or "http")
