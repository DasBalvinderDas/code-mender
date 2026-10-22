"""ADK tools exposed to the CodeMender analysis agent."""
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from pathlib import Path

from google.adk.tools import ToolContext
from . import reports
from .scanner import Finding, ScanResult, clone_repo, scan_path

_STATE_KEY = "codemender_last_scan"
PENDING_FILES_KEY = "codemender_pending_files"  # report files (PDF + Markdown) the agent callback attaches to the reply, then deletes
REPORT_NAME = "CodeMender_Security_Report"


async def analyze_repository(repo_url: str, tool_context: ToolContext, ref: str = "", subdir: str = "") -> dict:
    """FAST built-in scan (seconds). Use run_codemender for the real CodeMender (find, exploit verification, validated fixes).

    Builds a PDF report and a Markdown report, both attached to the reply automatically (do not try to link or upload them).

    Args:
        repo_url: https git URL (e.g. https://github.com/org/repo) or a local path.
        ref: Optional branch or tag. Defaults to the default branch.
        subdir: Optional folder inside the repo to scan (e.g. demo/vulnerable-app). Defaults to the whole repo.

    Returns:
        Summary with severity counts, risk score, top findings and the report attachment status.
    """
    try:
        root, commit = await asyncio.to_thread(clone_repo, repo_url, ref)
    except Exception as exc:  # surfaced to the calling agent
        return {"status": "error", "message": str(exc)}
    is_tmp = not os.path.isdir(repo_url)
    try:
        scan_root = (root / subdir).resolve() if subdir else root
        if not scan_root.is_dir() or (root.resolve() not in scan_root.parents and scan_root != root.resolve()):
            return {"status": "error", "message": f"subdir '{subdir}' not found inside the repository"}
        res: ScanResult = await asyncio.to_thread(scan_path, scan_root, repo_url + (f"/{subdir}" if subdir else ""), ref, commit)
    finally:
        if is_tmp:
            shutil.rmtree(root, ignore_errors=True)

    files = []
    for ext, mime, data in (("pdf", "application/pdf", await asyncio.to_thread(reports.to_pdf_bytes, res)),
                            ("md", "text/markdown", reports.to_markdown(res, limit=100).encode("utf-8"))):
        fd, path = tempfile.mkstemp(prefix="cm_report_", suffix="." + ext)
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        files.append({"path": path, "name": f"{REPORT_NAME}.{ext}", "mime": mime})
    tool_context.state[PENDING_FILES_KEY] = files
    tool_context.state[_STATE_KEY] = {"findings": [f.to_dict() for f in res.findings], "summary": reports.summary(res)}

    top = [{k: f.to_dict()[k] for k in ("id", "severity", "title", "cwe", "file", "line", "owasp")} for f in res.findings[:10]]
    return {"status": "ok", "summary": reports.summary(res), "top_findings": top,
            "report": "Two files are attached to this reply: CodeMender_Security_Report.pdf and CodeMender_Security_Report.md (same content)",
            "engine": res.engine}


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
    s = data["summary"]
    res = ScanResult(s["repo"], s["ref"], s["commit"], s["files_scanned"], s["lines_scanned"], s["languages"],
                     [Finding(**f) for f in data["findings"]], s.get("engine", ScanResult.engine))
    return {"status": "ok", "format": format, "content": (reports.to_markdown(res, limit=100) if format == "md" else reports.FORMATS[format](res))}


def search_findings(tool_context: ToolContext, path_prefix: str = "", cwe: str = "", severity: str = "", limit: int = 30) -> dict:
    """Filter the findings of the last analysis. Use this to answer questions about a folder, a weakness type or a severity.

    Args:
        path_prefix: Only findings whose file path starts with this (e.g. "routes/" or "lib/insecurity").
        cwe: Only this CWE, e.g. "CWE-89" (SQL injection), "CWE-95" (eval), "CWE-798" (hard-coded secret).
        severity: CRITICAL, HIGH, MEDIUM or LOW.
        limit: Maximum rows to return (default 30).
    """
    data = tool_context.state.get(_STATE_KEY)
    if not data:
        return {"status": "error", "message": "no analysis yet; run analyze_repository first"}
    rows = [f for f in data["findings"]
            if f["file"].startswith(path_prefix) and (not cwe or f["cwe"].upper() == cwe.upper())
            and (not severity or f["severity"].upper() == severity.upper())]
    keep = ("id", "severity", "cwe", "title", "file", "line", "snippet")
    return {"status": "ok", "matches": len(rows), "returned": min(len(rows), max(1, limit)),
            "findings": [{**{k: f[k] for k in keep}, "has_patch": bool(f["patch"])} for f in rows[:max(1, limit)]]}


def get_fix_candidates(tool_context: ToolContext) -> dict:
    """List findings that have an auto-generated patch ready for human review, for hand-off to a defect-fix agent."""
    fs = [f for f in tool_context.state.get(_STATE_KEY, {}).get("findings", []) if f["patch"]]
    return {"count": len(fs), "fixes": [{"id": f["id"], "severity": f["severity"], "file": f["file"], "line": f["line"],
                                          "title": f["title"], "cwe": f["cwe"], "patch": f["patch"]} for f in fs]}
