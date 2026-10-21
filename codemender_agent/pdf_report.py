"""Single-file PDF security report (reportlab). Returned inline over A2A; nothing is written to cloud storage."""
from __future__ import annotations

import io
from datetime import datetime, timezone
from xml.sax.saxutils import escape

from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle)

from .scanner import SEV_ORDER, ScanResult

NAVY, BLUE = colors.HexColor("#0B1F3A"), colors.HexColor("#1A73E8")
SEV = {"CRITICAL": colors.HexColor("#B3261E"), "HIGH": colors.HexColor("#E8710A"),
       "MEDIUM": colors.HexColor("#F9AB00"), "LOW": colors.HexColor("#1A73E8")}
MAX_DETAILED = 60


def _styles():
    ss = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], textColor=NAVY, fontSize=20, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], textColor=NAVY, fontSize=14, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=13),
        "small": ParagraphStyle("small", parent=ss["BodyText"], fontSize=8, leading=10, textColor=colors.HexColor("#5F6368")),
        "cell": ParagraphStyle("cell", parent=ss["BodyText"], fontSize=8, leading=10),
        "band": ParagraphStyle("band", parent=ss["BodyText"], fontSize=22, leading=28),
        "kpi": ParagraphStyle("kpi", parent=ss["BodyText"], fontSize=9, leading=26),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=7.5, leading=9.5, backColor=colors.HexColor("#F1F3F4"),
                               borderPadding=3, leftIndent=3),
    }


def _chart(sev: dict) -> Drawing:
    d = Drawing(170 * mm, 48 * mm)
    order = list(SEV_ORDER)
    bc = HorizontalBarChart()
    bc.x, bc.y, bc.width, bc.height = 28 * mm, 4 * mm, 125 * mm, 40 * mm
    bc.data = [[sev[k] for k in reversed(order)]]
    bc.categoryAxis.categoryNames = [k.title() for k in reversed(order)]
    bc.categoryAxis.labels.fontSize = 9
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(max(sev.values()), 1) * 1.15
    bc.valueAxis.labels.fontSize = 8
    bc.bars.strokeColor = None
    for i, k in enumerate(reversed(order)):
        bc.bars[(0, i)].fillColor = SEV[k]
    bc.barLabelFormat = "%d"
    bc.barLabels.nudge = 8
    bc.barLabels.fontSize = 9
    d.add(bc)
    return d


def _p(t, st):
    return Paragraph(escape(str(t)), st)


def to_pdf(res: ScanResult, summary: dict) -> bytes:
    S = _styles()
    buf = io.BytesIO()

    def footer(c, doc):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#5F6368"))
        c.drawString(18 * mm, 10 * mm, "CodeMender Security Analysis · confidential · patches are suggestions for human review")
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        c.restoreState()

    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                            title="CodeMender Security Report", author="CodeMender Analysis Agent")
    W = A4[0] - 36 * mm
    f = []

    # Title band
    band = Table([[Paragraph('<font color="white" size="22"><b>CodeMender Security Report</b></font>', S["band"])],
                  [Paragraph(f'<font color="#BBD3F7" size="9">{escape(res.repo)} @ {escape(res.commit)} · '
                             f'{datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}</font>', S["cell"])]], colWidths=[W])
    band.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                              ("TOPPADDING", (0, 0), (0, 0), 12), ("BOTTOMPADDING", (0, -1), (-1, -1), 10)]))
    f += [band, Spacer(1, 8)]

    risk = summary["risk_score"]
    rc = SEV["CRITICAL"] if risk >= 70 else SEV["HIGH"] if risk >= 40 else SEV["MEDIUM"] if risk >= 15 else colors.HexColor("#188038")
    kpi = Table([[Paragraph(f'<font size="30" color="{rc.hexval()}"><b>{risk}</b></font><br/><font size="8">Risk score / 100</font>', S["kpi"]),
                  Paragraph(f'<font size="20"><b>{summary["total_findings"]}</b></font><br/><font size="8">Findings</font>', S["kpi"]),
                  Paragraph(f'<font size="20"><b>{summary["auto_fixable"]}</b></font><br/><font size="8">With ready patch</font>', S["kpi"]),
                  Paragraph(f'<font size="20"><b>{summary["files_scanned"]}</b></font><br/><font size="8">Files · {summary["lines_scanned"]:,} lines</font>', S["kpi"])]],
                colWidths=[W / 4] * 4)
    kpi.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, colors.lightgrey), ("INNERGRID", (0, 0), (-1, -1), .5, colors.lightgrey),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    f += [kpi, Paragraph("Findings by severity", S["h2"]), _chart(summary["by_severity"])]

    f.append(Paragraph("OWASP Top 10 (2021) exposure", S["h2"]))
    rows = [[_p("Category", S["cell"]), _p("Findings", S["cell"])]] + [[_p(k, S["cell"]), _p(v, S["cell"])] for k, v in
                                                                      sorted(summary["owasp"].items(), key=lambda t: -t[1])]
    t = Table(rows, colWidths=[W - 25 * mm, 25 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FE")), ("GRID", (0, 0), (-1, -1), .25, colors.lightgrey)]))
    f.append(t)

    # Findings overview
    f += [Paragraph("Findings overview", S["h2"])]
    rows = [[_p(h, S["cell"]) for h in ("Sev", "ID", "Issue", "CWE", "Location", "Patch")]]
    for x in res.findings:
        rows.append([_p(x.severity.title(), S["cell"]), _p(x.id, S["cell"]), _p(x.title, S["cell"]), _p(x.cwe, S["cell"]),
                     _p(f"{x.file}:{x.line}", S["cell"]), _p("yes" if x.patch else "-", S["cell"])])
    t = Table(rows, colWidths=[15 * mm, 25 * mm, W - 125 * mm, 17 * mm, 48 * mm, 14 * mm], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FE")), ("GRID", (0, 0), (-1, -1), .25, colors.lightgrey),
          ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i, x in enumerate(res.findings, 1):
        st.append(("TEXTCOLOR", (0, i), (0, i), SEV[x.severity]))
    t.setStyle(TableStyle(st))
    f += [t, PageBreak(), Paragraph("Detailed findings", S["h1"])]

    for x in res.findings[:MAX_DETAILED]:
        blk = [Paragraph(f'<font color="{SEV[x.severity].hexval()}"><b>[{x.severity}]</b></font> {escape(x.title)} '
                         f'<font size="8" color="#5F6368">· {x.cwe} · {escape(x.owasp)}</font>', S["h2"]),
               Paragraph(f"<b>{escape(x.file)}:{x.line}</b> · {x.id} · confidence {x.confidence}", S["small"]),
               Preformatted(x.snippet[:160], S["code"]),
               Paragraph(f"<b>Why it matters:</b> {escape(x.description)}", S["body"]),
               Paragraph(f"<b>Recommended fix:</b> {escape(x.remediation)}", S["body"]),
               Paragraph(f"<b>Verification plan:</b> {escape(x.verification_plan)}", S["body"])]
        if x.patch:
            diff = "\n".join(l[:110] for l in x.patch.strip().splitlines()[:24])
            blk += [Paragraph("<b>Proposed patch (for human review):</b>", S["body"]), Preformatted(diff, S["code"])]
        f += [KeepTogether(blk[:4]), *blk[4:], Spacer(1, 4)]
    if len(res.findings) > MAX_DETAILED:
        f.append(Paragraph(f"{len(res.findings) - MAX_DETAILED} lower-severity findings are listed in the overview only.", S["small"]))

    f += [Paragraph("Method and limits", S["h2"]),
          Paragraph("Findings come from rule-based static analysis mapped to CWE and OWASP. Verification plans describe how a finding "
                    "would be confirmed in a sandbox; no exploit was executed. Patches are suggestions that must be reviewed and tested "
                    "before merge.", S["body"])]
    doc.build(f, onFirstPage=footer, onLaterPages=footer)
    return buf.getvalue()
