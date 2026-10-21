"""Report generators: HTML dashboard, Markdown, JSON, SARIF 2.1.0, CSV, unified-diff patch set."""
from __future__ import annotations

import csv
import html
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .scanner import SEV_ORDER, ScanResult

SEV_COLOR = {"CRITICAL": "#b3261e", "HIGH": "#e8710a", "MEDIUM": "#f9ab00", "LOW": "#1a73e8"}
SARIF_LEVEL = {"CRITICAL": "error", "HIGH": "error", "MEDIUM": "warning", "LOW": "note"}


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def summary(res: ScanResult) -> dict:
    f = res.findings
    return {
        "repo": res.repo, "ref": res.ref, "commit": res.commit, "files_scanned": res.files_scanned,
        "lines_scanned": res.lines_scanned, "total_findings": len(f), "by_severity": res.by_severity,
        "risk_score": res.risk_score, "auto_fixable": sum(1 for x in f if x.patch),
        "top_cwes": Counter(x.cwe for x in f).most_common(5),
        "owasp": dict(Counter(x.owasp for x in f)), "languages": res.languages,
    }


def to_json(res: ScanResult) -> str:
    return json.dumps({"generated": _now(), "summary": summary(res), "findings": [x.to_dict() for x in res.findings]}, indent=2)


def to_sarif(res: ScanResult) -> str:
    rules, seen = [], set()
    for x in res.findings:
        if x.rule_id in seen:
            continue
        seen.add(x.rule_id)
        rules.append({"id": x.rule_id, "name": x.title, "shortDescription": {"text": x.title},
                      "fullDescription": {"text": x.description}, "help": {"text": x.remediation},
                      "properties": {"tags": ["security", x.cwe, x.owasp], "security-severity": {"CRITICAL": "9.5", "HIGH": "8.0", "MEDIUM": "5.5", "LOW": "3.0"}[x.severity]}})
    results = [{"ruleId": x.rule_id, "level": SARIF_LEVEL[x.severity], "message": {"text": f"{x.title}: {x.description}"},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": x.file}, "region": {"startLine": x.line, "snippet": {"text": x.snippet}}}}],
                "partialFingerprints": {"codemenderId": x.id}} for x in res.findings]
    return json.dumps({"$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0",
                       "runs": [{"tool": {"driver": {"name": "CodeMender Analysis Agent", "rules": rules}}, "results": results}]}, indent=2)


def to_csv(res: ScanResult) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "severity", "cwe", "owasp", "title", "file", "line", "confidence", "auto_fix"])
    for x in res.findings:
        w.writerow([x.id, x.severity, x.cwe, x.owasp, x.title, x.file, x.line, x.confidence, "yes" if x.patch else "no"])
    return buf.getvalue()


def to_patches(res: ScanResult) -> str:
    return "\n".join(f"# {x.id} {x.title} ({x.cwe})\n{x.patch}" for x in res.findings if x.patch)


def to_markdown(res: ScanResult, limit: int = 25) -> str:
    s = summary(res)
    sev = s["by_severity"]
    L = [f"# CodeMender Security Analysis", f"**Repo:** {res.repo} @ `{res.commit}`  |  **Generated:** {_now()}", "",
         f"**Risk score:** {s['risk_score']}/100 | **Findings:** {s['total_findings']} | **Auto-fixable:** {s['auto_fixable']} | "
         f"**Files/Lines scanned:** {s['files_scanned']}/{s['lines_scanned']}", "",
         "| Critical | High | Medium | Low |", "|---|---|---|---|",
         f"| {sev['CRITICAL']} | {sev['HIGH']} | {sev['MEDIUM']} | {sev['LOW']} |", "", "## OWASP Top 10 coverage"]
    L += [f"- {k}: {v}" for k, v in sorted(s["owasp"].items())] or ["- none"]
    L += ["", "## Top findings"]
    for x in res.findings[:limit]:
        L += [f"### [{x.severity}] {x.title} — `{x.file}:{x.line}` ({x.cwe})", f"```\n{x.snippet}\n```",
              f"- **Why it matters:** {x.description}", f"- **Fix:** {x.remediation}",
              f"- **Verification plan:** {x.verification_plan}", ""]
        if x.patch:
            L += ["```diff", x.patch.strip(), "```", ""]
    if len(res.findings) > limit:
        L.append(f"_…and {len(res.findings) - limit} more in the full report._")
    return "\n".join(L)


def _donut(sev: dict) -> str:
    total = sum(sev.values()) or 1
    r, c, off, parts = 54, 2 * 3.14159 * 54, 0.0, []
    for k in SEV_ORDER:
        d = sev[k] / total * c
        parts.append(f'<circle r="{r}" cx="70" cy="70" fill="none" stroke="{SEV_COLOR[k]}" stroke-width="22" '
                     f'stroke-dasharray="{d:.1f} {c - d:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 70 70)"/>')
        off += d
    return (f'<svg viewBox="0 0 140 140" width="150" height="150">{"".join(parts)}'
            f'<text x="70" y="76" text-anchor="middle" font-size="26" font-weight="700" fill="currentColor">{sum(sev.values())}</text></svg>')


def to_html(res: ScanResult) -> str:
    s = summary(res)
    e = html.escape
    cards = "".join(f'<div class="card"><div class="n" style="color:{SEV_COLOR[k]}">{v}</div><div>{k.title()}</div></div>' for k, v in s["by_severity"].items())
    mx = max(s["owasp"].values(), default=1)
    bars = "".join(f'<div class="bar"><span>{e(k)}</span><i style="width:{v / mx * 100:.0f}%"></i><b>{v}</b></div>' for k, v in sorted(s["owasp"].items(), key=lambda t: -t[1]))
    rows = []
    for x in res.findings:
        patch = f'<pre class="diff">{e(x.patch)}</pre>' if x.patch else ""
        rows.append(f'<details data-sev="{x.severity}"><summary><span class="pill" style="background:{SEV_COLOR[x.severity]}">{x.severity}</span> '
                    f'{e(x.title)} <code>{e(x.file)}:{x.line}</code> <em>{x.cwe}</em></summary>'
                    f'<pre>{e(x.snippet)}</pre><p><b>Why:</b> {e(x.description)}</p><p><b>Fix:</b> {e(x.remediation)}</p>'
                    f'<p><b>Verification plan:</b> {e(x.verification_plan)}</p><p><b>Confidence:</b> {x.confidence}</p>{patch}</details>')
    buttons = ''.join('<button data-s="%s">%s</button> ' % (k, k.title()) for k in SEV_ORDER) + '<button data-s="">All</button>'
    risk = s["risk_score"]
    rc = SEV_COLOR["CRITICAL"] if risk >= 70 else SEV_COLOR["HIGH"] if risk >= 40 else SEV_COLOR["MEDIUM"] if risk >= 15 else "#188038"
    return f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CodeMender Security Report</title><style>
:root{{--bg:#f8f9fa;--fg:#202124;--card:#fff;--mut:#5f6368;--line:#dadce0}}
@media(prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8eaed;--card:#202327;--mut:#9aa0a6;--line:#3c4043}}}}
body{{margin:0;font:15px/1.5 system-ui,sans-serif;background:var(--bg);color:var(--fg)}}
main{{max-width:1000px;margin:auto;padding:24px 16px}} h1{{margin:0}} .mut{{color:var(--mut)}}
.grid{{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}} .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 20px;min-width:110px;text-align:center}}
.n{{font-size:32px;font-weight:700}} .panel{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}}
.row{{display:flex;gap:24px;align-items:center;flex-wrap:wrap}} .bar{{display:grid;grid-template-columns:260px 1fr 30px;gap:8px;align-items:center;margin:4px 0;font-size:13px}}
.bar i{{display:block;height:10px;background:#1a73e8;border-radius:5px}} details{{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:8px 0;padding:10px 14px}}
summary{{cursor:pointer}} .pill{{color:#fff;border-radius:10px;padding:1px 9px;font-size:12px;font-weight:600}} em{{color:var(--mut);font-size:12px}}
pre{{overflow:auto;background:rgba(127,127,127,.12);padding:8px;border-radius:6px;font-size:12px}} .diff{{border-left:3px solid #188038}}
.score{{font-size:56px;font-weight:800;color:{rc}}} button{{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:16px;padding:4px 12px;cursor:pointer}}
</style><main>
<h1>CodeMender Security Report</h1>
<p class="mut">{e(res.repo)} @ {e(res.commit)} · {_now()} · {s['files_scanned']} files / {s['lines_scanned']:,} lines</p>
<div class="panel row"><div><div class="score">{risk}</div><div class="mut">Risk score / 100</div></div>{_donut(s['by_severity'])}
<div><b>{s['auto_fixable']}</b> of {s['total_findings']} findings have a ready-to-review patch.<br>Stages: Find → Verify plan → Fix (diff for human approval)</div></div>
<div class="grid">{cards}</div>
<div class="panel"><h3>OWASP Top 10 (2021) exposure</h3>{bars or '<p class="mut">No findings.</p>'}</div>
<h3>Findings</h3><p>{buttons}</p>
{''.join(rows)}
</main><script>document.querySelectorAll('button[data-s]').forEach(b=>b.onclick=()=>{{const s=b.dataset.s;document.querySelectorAll('details').forEach(d=>d.style.display=!s||d.dataset.sev===s?'':'none')}})</script></html>"""


FORMATS = {"html": to_html, "md": to_markdown, "json": to_json, "sarif": to_sarif, "csv": to_csv, "patch": to_patches}


def write_all(res: ScanResult, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for ext, fn in FORMATS.items():
        name = {"patch": "patches.diff", "sarif": "report.sarif"}.get(ext, f"report.{ext}")
        p = out_dir / name
        p.write_text(fn(res), encoding="utf-8")
        paths[ext] = str(p)
    return paths
