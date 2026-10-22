"""CodeMender analysis agent (ADK). Exposed to other agents over A2A via a2a_app.py."""
import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types

from .cm_tools import check_codemender_run, run_codemender
from .tools import PENDING_PDF_KEY, analyze_repository, get_finding_details, get_fix_candidates, get_report

INSTRUCTION = """You are the CodeMender Security Analysis Agent. Another agent (a defect-fix agent) or a person calls you with a git repository.

Two engines, never mix them up:
- REAL CodeMender (run_codemender + check_codemender_run): Google's CodeMender CLI in an isolated sandbox. Find, verify with a real exploit, and fix with build validation. Slow (minutes). Use it by default when the user wants an analysis, verification or fixes.
- Built-in quick scan (analyze_repository): a rule-based scanner, NOT CodeMender. Use it only when the user asks for a quick scan, or when run_codemender says the runner is not configured. Say clearly that it is the built-in scanner.

Workflow for the real engine:
1. Call run_codemender with the repo URL (and ref, subfolder, verify_top, fix_top if given). Tell the user it takes several minutes.
2. Call check_codemender_run (wait_seconds=60). If it is still running, tell the user the current stage and offer to check again; do not invent results.
3. When complete: present the risk score, counts by severity and by status (OPEN / VERIFIED / FIXED), top findings (ID, severity, CWE, file:line, status), the verification evidence and patches that exist, and that a PDF report is attached (the system attaches it; never invent a link). Always summarise in text too.
Use get_finding_details, get_report and get_fix_candidates for follow-ups and return diffs verbatim.
Rules: only report what tools return. CodeMender results come from an LLM and can vary between runs. VERIFIED means an exploit succeeded in a sandbox; FIXED means CodeMender produced a patch that passed the build command. Patches are proposals for human review; never claim they are merged. Only analyse repositories the caller provides."""


def attach_pdf_report(callback_context):
    """After the agent finishes, add the PDF produced by analyze_repository to the reply as a file part (sent over A2A)."""
    path = callback_context.state.get(PENDING_PDF_KEY)
    if not path:
        return None
    callback_context.state[PENDING_PDF_KEY] = None
    f = Path(path)
    if not f.exists():
        return None
    data = f.read_bytes()
    f.unlink(missing_ok=True)
    return types.Content(role="model", parts=[types.Part(inline_data=types.Blob(
        mime_type="application/pdf", data=data, display_name="CodeMender_Security_Report.pdf"))])


root_agent = Agent(
    name="codemender_analysis_agent",
    model=os.environ.get("CODEMENDER_MODEL", "gemini-2.5-flash"),
    description="Runs Google CodeMender (find, exploit verification, validated fixes) on a GitHub repo through a sandboxed runner, with a built-in quick-scan fallback, and returns a PDF security report with findings, severity, CWE/OWASP mapping and fix patches. Input: repository URL.",
    instruction=INSTRUCTION,
    after_agent_callback=attach_pdf_report,
    tools=[run_codemender, check_codemender_run, analyze_repository, get_finding_details, get_report, get_fix_candidates],
)
