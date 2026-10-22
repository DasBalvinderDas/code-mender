"""Agent -> runner API -> pipeline -> cm SIMULATOR -> PDF in the reply. Proves the wiring; the real CLI is not exercised."""
import asyncio
import subprocess
from pathlib import Path

import httpx
import pytest
from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

from codemender_agent import cm_tools, runner_client
from codemender_agent.agent import attach_pdf_report
from codemender_agent.tools import get_fix_candidates
from runner import app as runner_app, pipeline

FAKE = str(Path(__file__).parent / "fake_cm.py")


@pytest.fixture
def wired(tmp_path, monkeypatch):
    r = tmp_path / "src"; (r / "app").mkdir(parents=True)
    (r / "app" / "svc.py").write_text("def get(name, cur):\n    cur.execute(f\"SELECT * FROM users WHERE name = '{name}'\")\n")
    for c in (["init", "-q"], ["add", "-A"], ["-c", "user.email=a@b", "-c", "user.name=t", "commit", "-qm", "b"]):
        subprocess.run(["git", *c], cwd=r, check=True)
    monkeypatch.setattr(pipeline, "CM_BIN", FAKE)
    monkeypatch.setattr(pipeline, "ALLOW_LOCAL", True)
    monkeypatch.setenv("RUNNER_ALLOW_VERIFY_FIX", "1")
    monkeypatch.setenv("CODEMENDER_RUNNER_URL", "http://localhost:8080")
    monkeypatch.setattr(runner_client, "_TRANSPORT", httpx.ASGITransport(app=runner_app.app))
    return str(r)


class Script(BaseLlm):
    model: str = "scripted"
    repo: str = ""

    async def generate_content_async(self, llm_request, stream=False):
        n = sum(1 for c in llm_request.contents for p in c.parts if p.function_response)
        calls = [("run_codemender", {"repo_url": self.repo, "subdir": "app", "verify_top": 1, "fix_top": 1}),
                 ("check_codemender_run", {"wait_seconds": 30})]
        if n < len(calls):
            name, args = calls[n]
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=name, args=args))]))
        else:
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="done")]))


def test_agent_runs_real_flow_and_attaches_pdf(wired):
    agent = Agent(name="t", model=Script(repo=wired), tools=[cm_tools.run_codemender, cm_tools.check_codemender_run, get_fix_candidates],
                  after_agent_callback=attach_pdf_report)
    runner = InMemoryRunner(agent=agent, app_name="t")

    async def go():
        await runner.session_service.create_session(app_name="t", user_id="u", session_id="s")
        evs = [e async for e in runner.run_async(user_id="u", session_id="s", new_message=types.Content(role="user", parts=[types.Part(text="go")]))]
        sess = await runner.session_service.get_session(app_name="t", user_id="u", session_id="s")
        return evs, sess

    evs, sess = asyncio.run(go())
    resp = [p.function_response.response for e in evs if e.content for p in e.content.parts if p.function_response]
    assert resp[0]["status"] == "started"
    done = resp[1]
    assert done["status"] == "completed" and done["engine"] == "CodeMender CLI (cm)", done
    assert done["by_status"] == {"FIXED": 1}
    pdfs = [p.inline_data for e in evs if e.content for p in e.content.parts if p.inline_data]
    assert {b.mime_type for b in pdfs} == {"application/pdf", "text/markdown"}
    pdf = next(b for b in pdfs if b.mime_type == "application/pdf")
    md = next(b for b in pdfs if b.mime_type == "text/markdown")
    assert pdf.data.startswith(b"%PDF") and len(pdf.data) > 3000 and b"**Engine:** CodeMender CLI (cm)" in md.data
    fixes = sess.state["codemender_last_scan"]["findings"]
    assert fixes[0]["status"] == "fixed" and "WHERE name = ?" in fixes[0]["patch"]


def test_unconfigured_runner_falls_back_message(monkeypatch):
    monkeypatch.delenv("CODEMENDER_RUNNER_URL", raising=False)
    from unittest.mock import MagicMock
    out = asyncio.run(cm_tools.run_codemender("https://github.com/a/b", MagicMock(state={})))
    assert out["status"] == "error" and "analyze_repository" in out["message"]


def test_default_run_is_find_and_report_only(wired, monkeypatch):
    monkeypatch.delenv("RUNNER_ALLOW_VERIFY_FIX")
    calls = [("run_codemender", {"repo_url": wired, "subdir": "app"}), ("check_codemender_run", {"wait_seconds": 30})]

    class FindOnly(Script):
        async def generate_content_async(self, llm_request, stream=False):
            n = sum(1 for c in llm_request.contents for p in c.parts if p.function_response)
            if n < len(calls):
                name, args = calls[n]
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=name, args=args))]))
            else:
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="done")]))

    agent = Agent(name="t", model=FindOnly(repo=wired), tools=[cm_tools.run_codemender, cm_tools.check_codemender_run],
                  after_agent_callback=attach_pdf_report)
    runner = InMemoryRunner(agent=agent, app_name="t")

    async def go():
        await runner.session_service.create_session(app_name="t", user_id="u", session_id="s")
        return [e async for e in runner.run_async(user_id="u", session_id="s", new_message=types.Content(role="user", parts=[types.Part(text="go")]))]

    resp = [p.function_response.response for e in asyncio.run(go()) if e.content for p in e.content.parts if p.function_response]
    assert resp[1]["status"] == "completed" and resp[1]["by_status"] == {"OPEN": 1}
