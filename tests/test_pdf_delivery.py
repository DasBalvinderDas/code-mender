"""The PDF must come back inside the agent reply (no bucket). Uses a scripted model, so no cloud access is needed."""
import asyncio
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

from codemender_agent.agent import attach_pdf_report
from codemender_agent.tools import analyze_repository, get_report

DEMO = str(Path(__file__).resolve().parent.parent / "demo" / "vulnerable-app")


class ScriptedLlm(BaseLlm):
    model: str = "scripted"

    async def generate_content_async(self, llm_request, stream=False):
        last = llm_request.contents[-1].parts[0]
        if last.function_response:
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="Analysis done.")]))
        else:
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(
                function_call=types.FunctionCall(name="analyze_repository", args={"repo_url": DEMO}))]))


def test_pdf_is_attached_to_reply():
    agent = Agent(name="t", model=ScriptedLlm(), tools=[analyze_repository, get_report], after_agent_callback=attach_pdf_report)
    runner = InMemoryRunner(agent=agent, app_name="t")

    async def go():
        await runner.session_service.create_session(app_name="t", user_id="u", session_id="s")
        return [e async for e in runner.run_async(user_id="u", session_id="s",
                                                  new_message=types.Content(role="user", parts=[types.Part(text="scan")]))]

    pdfs = [p.inline_data for e in asyncio.run(go()) if e.content for p in e.content.parts if p.inline_data]
    assert len(pdfs) == 2
    md = next(b for b in pdfs if b.mime_type == "text/markdown")
    assert b"# CodeMender Security Analysis" in md.data and md.display_name.endswith(".md")
    pdfs = [b for b in pdfs if b.mime_type == "application/pdf"]
    assert pdfs[0].mime_type == "application/pdf" and pdfs[0].data.startswith(b"%PDF")
    assert pdfs[0].display_name == "CodeMender_Security_Report.pdf"


def test_no_pdf_when_nothing_pending():
    class Ctx:
        state = {}
    assert attach_pdf_report(Ctx()) is None


def test_subdir_scan_and_traversal_blocked():
    from unittest.mock import AsyncMock, MagicMock
    root = str(Path(DEMO).parent.parent)
    tc = MagicMock(); tc.state = {}; tc.save_artifact = AsyncMock()
    ok = asyncio.run(analyze_repository(root, tc, subdir="demo/vulnerable-app"))
    assert ok["status"] == "ok" and ok["summary"]["total_findings"] == 33
    bad = asyncio.run(analyze_repository(root, tc, subdir="../../etc"))
    assert bad["status"] == "error"


def test_search_findings_filters():
    from unittest.mock import AsyncMock, MagicMock
    from codemender_agent.tools import search_findings
    tc = MagicMock(); tc.state = {}; tc.save_artifact = AsyncMock()
    asyncio.run(analyze_repository(DEMO, tc))
    sqli = search_findings(tc, cwe="CWE-89")
    assert sqli["matches"] == 2 and all(f["cwe"] == "CWE-89" for f in sqli["findings"])
    assert {f["file"] for f in search_findings(tc, path_prefix="parser")["findings"]} == {"parser.c"}
    assert search_findings(tc, severity="critical", limit=3)["returned"] == 3
    assert search_findings(MagicMock(state={}))["status"] == "error"
