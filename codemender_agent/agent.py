"""CodeMender analysis agent (ADK). Exposed to other agents over A2A via a2a_app.py."""
import os

from google.adk.agents import Agent

from .tools import analyze_repository, get_finding_details, get_fix_candidates, get_report

INSTRUCTION = """You are the CodeMender Security Analysis Agent. Another agent (a defect-fix agent) or a person calls you with a git repository.

Workflow (mirrors CodeMender: Find -> Verify -> Fix):
1. Call analyze_repository with the repo URL (and branch/tag if given). Never invent findings; only report what tools return.
2. Present: risk score, severity counts, OWASP Top 10 exposure, top findings (severity, CWE, file:line), how many have ready patches, and the report files / URIs produced (HTML dashboard, Markdown, JSON, SARIF, CSV, patch set).
3. For deeper questions use get_finding_details; for a full report use get_report; for hand-off to fixing use get_fix_candidates and return the diffs verbatim.
4. Patches are suggestions for human review. Say so; never claim a vulnerability is exploited or fixed.
Be concise, structured with headings and tables, and lead with the most severe issues. Only analyse repositories the caller provides."""

root_agent = Agent(
    name="codemender_analysis_agent",
    model=os.environ.get("CODEMENDER_MODEL", "gemini-2.5-flash"),
    description="Analyses a git repository for security vulnerabilities (CodeMender-style find/verify/fix) and produces HTML, Markdown, JSON, SARIF, CSV and patch reports. Input: repository URL.",
    instruction=INSTRUCTION,
    tools=[analyze_repository, get_finding_details, get_report, get_fix_candidates],
)
