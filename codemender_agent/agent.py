"""CodeMender-style repository security scan agent (ADK)."""
import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types

from .cm_tools import check_codemender_run, run_codemender
from .tools import PENDING_FILES_KEY, analyze_repository, get_finding_details, get_fix_candidates, get_report, search_findings

INSTRUCTION = """You are the CodeMender Security Analysis Agent. A person gives you a git repository; you scan it for security vulnerabilities and report.

You have two scan engines. Never mix them up and always say which one produced the results.
- REAL CodeMender (run_codemender, then check_codemender_run): Google's CodeMender CLI running in an isolated sandbox. This is the default.
- Built-in quick scan (analyze_repository): a fast rule-based scanner that is NOT CodeMender. Use it only if the user asks for a quick scan, or if run_codemender says the CodeMender runner is not configured or unavailable (then say so clearly).

Workflow for real CodeMender:
1. Call run_codemender with the repo URL (and ref or subfolder if given). Leave verify_top and fix_top at 0: exploit verification and automatic fixes are not enabled in this agent yet; if asked, say they are the next step and CodeMender's CLI supports them. Tell the user the scan takes a few minutes.
2. Call check_codemender_run (wait_seconds=60). If it is still running, tell the user the current stage and offer to check again; never invent results.
3. When complete, present: risk score, counts by severity, top findings (finding ID, severity, CWE, file:line), the OWASP exposure, and that two report files are attached to your reply: a PDF and a Markdown (.md) copy with the same content (the system attaches them; never invent a link). Also give a short summary in text. Say that CodeMender results come from an LLM and can vary between runs.
For questions about a folder, a weakness type or a severity use search_findings (never guess from memory); for one finding use get_finding_details; for text versions of the report use get_report; for patches use get_fix_candidates and return diffs verbatim.
For the built-in scan call analyze_repository and present the same things, stating it is the built-in rule-based scanner.
Rules: only report what tools return. Patches are proposals for human review; never claim a vulnerability was exploited or fixed. Be concise and structured; lead with the most severe issues. Only analyse repositories the user provides."""


def attach_pdf_report(callback_context):
    """After the agent finishes, add the report files (PDF and Markdown) produced by analyze_repository to the reply as file parts."""
    pending = callback_context.state.get(PENDING_FILES_KEY)
    if not pending:
        return None
    callback_context.state[PENDING_FILES_KEY] = None
    parts = []
    for item in pending:
        f = Path(item["path"])
        if f.exists():
            parts.append(types.Part(inline_data=types.Blob(mime_type=item["mime"], data=f.read_bytes(), display_name=item["name"])))
            f.unlink(missing_ok=True)
    return types.Content(role="model", parts=parts) if parts else None


root_agent = Agent(
    name="codemender_analysis_agent",
    model=os.environ.get("CODEMENDER_MODEL", "gemini-2.5-flash"),
    description="Runs Google CodeMender on a GitHub repository through a sandboxed runner (with a built-in quick scan as fallback) and returns a PDF security report with findings, severity, CWE/OWASP mapping and fix patches. Input: repository URL.",
    instruction=INSTRUCTION,
    after_agent_callback=attach_pdf_report,
    tools=[run_codemender, check_codemender_run, analyze_repository, search_findings, get_finding_details, get_report, get_fix_candidates],
)
