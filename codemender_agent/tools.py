"""ADK tools exposed to the CodeMender analysis agent."""
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from pathlib import Path

from google.adk.tools import ToolContext
from . import reports
from .scanner import clone_repo, cm_cli_available, run_cm_cli, scan_path, ScanResult

_STATE_KEY = "codemender_last_scan"
PENDING_PDF_KEY = "codemender_pending_pdf"  # temp-file path of a PDF the agent callback attaches to the reply, then deletes


async def analyze_repository(repo_url: str, tool_context: ToolContext, ref: str = "", use_codemender_cli: bool = False) -> dict:
    """Clone a git repository and run a full security analysis (find -> verification plan -> fix suggestions).

    Builds one PDF report, which is attached to the reply automatically (do not try to link or upload it).

    Args:
        repo_url: https git URL (e.g. https://github.com/org/repo) or a local path.
        ref: Optional branch or tag. Defaults to the default branch.
        use_codemender_cli: Also run the licensed `cm` CLI (find/verify/fix) if installed on this host.

    Returns:
        Summary with severity counts, risk score, top findings and the report attachment status.
    """
    try:
        root, commit = await asyncio.to_thread(clone_repo, repo_url, ref)
    except Exception as exc:  # surfaced to the calling agent
        return {"status": "error", "message": str(exc)}
    is_tmp = not os.path.isdir(repo_url)
    try:
        res: ScanResult = await asyncio.to_thread(scan_path, root, repo_url, ref, commit)
        cli = None
        if use_codemender_cli:
            cli = await asyncio.to_thread(run_cm_cli, root) if cm_cli_available() else {"error": "`cm` CLI not installed on this host; built-in engine used"}
    finally:
        if is_tmp:
            shutil.rmtree(root, ignore_errors=True)

    fd, pdf_path = tempfile.mkstemp(prefix="cm_report_", suffix=".pdf")
    with os.fdopen(fd, "wb") as fh:
        fh.write(await asyncio.to_thread(reports.to_pdf_bytes, res))
    tool_context.state[PENDING_PDF_KEY] = pdf_path
    tool_context.state[_STATE_KEY] = {"findings": [f.to_dict() for f in res.findings], "summary": reports.summary(res)}

    top = [{k: f.to_dict()[k] for k in ("id", "severity", "title", "cwe", "file", "line", "owasp")} for f in res.findings[:10]]
    return {"status": "ok", "summary": reports.summary(res), "top_findings": top,
            "report": "PDF security report is attached to this reply (CodeMender_Security_Report.pdf)",
            "codemender_cli": cli, "engine": "codemender-cli+builtin" if cli and "error" not in cli else "builtin"}


def get_finding_details(finding_id: str, tool_context: ToolContext) -> dict:
    """Return full details (description, fix, verification plan, patch diff) for a finding ID from the last analysis."""
    for f in tool_context.state.get(_STATE_KEY, {}).get("findings", []):
        if f["id"] == finding_id:
            return f
    return {"status": "error", "message": f"finding {finding_id} not found; run analyze_repository first"}


def get_report(format: str, tool_context: ToolContext) -> dict:
    """Return the last analysis as text in chat. format: md | json | sarif | csv | patch (use md for a readable summary)."""
    data = tool_context.state.get(_STATE_KEY)
    if not data:
        return {"status": "error", "message": "no analysis yet; run analyze_repository first"}
    if format not in reports.FORMATS or format == "html":
        return {"status": "error", "message": f"format must be one of {sorted(set(reports.FORMATS) - {'html'})}"}
    from .scanner import Finding
    s = data["summary"]
    res = ScanResult(s["repo"], s["ref"], s["commit"], s["files_scanned"], s["lines_scanned"], s["languages"],
                     [Finding(**f) for f in data["findings"]])
    return {"status": "ok", "format": format, "content": reports.FORMATS[format](res)}


def get_fix_candidates(tool_context: ToolContext) -> dict:
    """List findings that have an auto-generated patch ready for human review, for hand-off to a defect-fix agent."""
    fs = [f for f in tool_context.state.get(_STATE_KEY, {}).get("findings", []) if f["patch"]]
    return {"count": len(fs), "fixes": [{"id": f["id"], "severity": f["severity"], "file": f["file"], "line": f["line"],
                                          "title": f["title"], "cwe": f["cwe"], "patch": f["patch"]} for f in fs]}
