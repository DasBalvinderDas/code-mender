"""CodeMender analysis agent (ADK). Exposed to other agents over A2A via a2a_app.py."""
import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types

from .tools import PENDING_PDF_KEY, analyze_repository, get_finding_details, get_fix_candidates, get_report

INSTRUCTION = """You are the CodeMender Security Analysis Agent. Another agent (a defect-fix agent) or a person calls you with a git repository.

Workflow (mirrors CodeMender: Find -> Verify -> Fix):
1. Call analyze_repository with the repo URL (and branch/tag if given). Never invent findings; only report what tools return.
2. Present: risk score, severity counts, OWASP Top 10 exposure, top findings (severity, CWE, file:line), how many have ready patches, and and that a PDF report is attached to your reply (the system attaches it; never invent a link). Always also summarise the findings in text, since the PDF may not render everywhere.
3. For deeper questions use get_finding_details; for a full report use get_report; for hand-off to fixing use get_fix_candidates and return the diffs verbatim.
4. Patches are suggestions for human review. Say so; never claim a vulnerability is exploited or fixed.
Be concise, structured with headings and tables, and lead with the most severe issues. Only analyse repositories the caller provides."""

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
    description="Analyses a git repository for security vulnerabilities (CodeMender-style find/verify/fix) and returns a PDF security report with findings, severity, CWE/OWASP mapping and fix patches. Input: repository URL.",
    instruction=INSTRUCTION,
    after_agent_callback=attach_pdf_report,
    tools=[analyze_repository, get_finding_details, get_report, get_fix_candidates],
)
