"""The agent runs inside AdkApp (what Agent Engine hosts) and returns the PDF in its reply. Scripted model, no cloud access."""
import asyncio
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from vertexai.agent_engines import AdkApp

from codemender_agent.agent import INSTRUCTION, attach_pdf_report
from codemender_agent.tools import analyze_repository, get_finding_details, get_fix_candidates, get_report

DEMO = str(Path(__file__).resolve().parent.parent / "demo" / "vulnerable-app")


class Script(BaseLlm):
    model: str = "scripted"

    async def generate_content_async(self, llm_request, stream=False):
        if any(p.function_response for c in llm_request.contents for p in c.parts):
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="Scan complete.")]))
        else:
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(
                function_call=types.FunctionCall(name="analyze_repository", args={"repo_url": DEMO}))]))


def test_adkapp_returns_pdf(monkeypatch):
    import vertexai
    vertexai.init(project="test-project", location="us-central1")
    from google.adk.sessions import InMemorySessionService
    agent = Agent(name="codemender_analysis_agent", model=Script(), instruction=INSTRUCTION, after_agent_callback=attach_pdf_report,
                  tools=[analyze_repository, get_finding_details, get_report, get_fix_candidates])
    app = AdkApp(agent=agent, enable_tracing=False, session_service_builder=lambda: InMemorySessionService())
    app.set_up()

    async def go():
        return [e async for e in app.async_stream_query(user_id="u", message="scan it")]

    events = asyncio.run(go())
    blob = str(events)
    assert "Scan complete." in blob
    assert "CodeMender_Security_Report.pdf" in blob and "application/pdf" in blob
