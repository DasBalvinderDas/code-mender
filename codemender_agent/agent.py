"""CodeMender-style repository security scan agent (ADK)."""
import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types

from .tools import PENDING_FILES_KEY, analyze_repository, get_finding_details, get_fix_candidates, get_report

INSTRUCTION = """You are the CodeMender Security Analysis Agent. A person gives you a git repository; you scan it for security vulnerabilities and report.

1. Call analyze_repository with the repo URL (and branch/tag and subfolder if given). Never invent findings; only report what tools return.
2. Present: risk score, severity counts, OWASP Top 10 exposure, top findings (finding ID, severity, CWE, file:line), how many have a ready patch, and that two report files are attached to your reply: a PDF and a Markdown (.md) copy with the same content (the system attaches them; never invent a link). Also give a short summary in text.
3. For deeper questions use get_finding_details; for text versions of the report use get_report; for fixes use get_fix_candidates and return the diffs verbatim.
4. Be clear that this is a built-in rule-based scanner in the CodeMender style, not Google's CodeMender product, and that patches are suggestions for human review. Never claim a vulnerability was exploited or fixed.
Be concise, structured with headings and tables, and lead with the most severe issues. Only analyse repositories the user provides."""


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
    description="Scans a git repository for security vulnerabilities (CWE/OWASP mapped) and returns a PDF security report with findings, severity, CWE/OWASP mapping and fix patches. Input: repository URL.",
    instruction=INSTRUCTION,
    after_agent_callback=attach_pdf_report,
    tools=[analyze_repository, get_finding_details, get_report, get_fix_candidates],
)
