"""Builds ppt/CodeMender_Overview.pptx. Restyle by editing THEME (or point TEMPLATE at a .pptx/.potx)."""
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent
TEMPLATE = None  # e.g. ROOT / "campaign_manager_template.pptx" to inherit its masters/theme
THEME = dict(bg="FFFFFF", dark="0B1F3A", primary="1A73E8", accent="34A853", warn="E8710A", crit="B3261E",
             text="202124", mut="5F6368", card="F1F3F4", font="Calibri")
SHOT = ROOT / "report_screenshot.png"
DATA = json.loads((ROOT / "demo_summary.json").read_text())


def rgb(h):
    return RGBColor.from_string(h)


prs = Presentation(str(TEMPLATE)) if TEMPLATE else Presentation()
if not TEMPLATE:
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def box(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, x, y, w, h)
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def text(s, x, y, w, h, t, size=16, bold=False, color=None, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, shape=None):
    tb = shape or s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1)
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold; r.font.name = THEME["font"]
        r.font.color.rgb = rgb(color or THEME["text"])
        p.space_after = Pt(6)
    return tb


def slide(title, sub=None, n=[0]):
    s = prs.slides.add_slide(BLANK); n[0] += 1
    box(s, 0, 0, W, Inches(1.15), THEME["dark"])
    box(s, 0, Inches(1.15), W, Inches(0.06), THEME["primary"])
    text(s, Inches(0.5), Inches(0.12), Inches(12), Inches(0.7), title, 30, True, "FFFFFF", anchor=MSO_ANCHOR.MIDDLE)
    if sub:
        text(s, Inches(0.5), Inches(0.68), Inches(12), Inches(0.4), sub, 14, False, "BBD3F7")
    text(s, Inches(0.5), H - Inches(0.45), Inches(8), Inches(0.3), "CodeMender · Code security agent", 10, False, THEME["mut"])
    text(s, W - Inches(1.2), H - Inches(0.45), Inches(0.8), Inches(0.3), str(n[0] + 1), 10, False, THEME["mut"], PP_ALIGN.RIGHT)
    return s


def card(s, x, y, w, h, head, body, color=None, size=13):
    box(s, x, y, w, h, THEME["card"])
    box(s, x, y, Inches(0.09), h, color or THEME["primary"])
    text(s, x + Inches(0.2), y + Inches(0.1), w - Inches(0.3), Inches(0.4), head, 17, True, color or THEME["primary"])
    text(s, x + Inches(0.2), y + Inches(0.55), w - Inches(0.3), h - Inches(0.6), body, size)


def notes(s, t):
    s.notes_slide.notes_text_frame.text = t


# 1 Title
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, W, H, THEME["dark"])
box(s, Inches(0.8), Inches(3.55), Inches(2.2), Inches(0.08), THEME["primary"])
text(s, Inches(0.8), Inches(1.7), Inches(11.5), Inches(1.0), "CodeMender", 60, True, "FFFFFF")
text(s, Inches(0.8), Inches(2.7), Inches(11.5), Inches(0.8), "AI that finds, verifies and fixes vulnerabilities in your code", 26, False, "BBD3F7")
text(s, Inches(0.8), Inches(3.9), Inches(11), Inches(1.2),
     ["Gemini Enterprise Agent Platform  ·  A2A-connected security analysis agent", "Live demo: Defect-Fix Agent → CodeMender Analysis Agent"], 16, False, "FFFFFF")
notes(s, "Open with the one-line story: we already have a defect-fix agent; CodeMender adds security analysis through A2A.")

# 2 Problem
s = slide("Finding bugs is no longer the bottleneck", "Fixing them safely is")
for i, (h, b, c) in enumerate([
    ("Scanner noise", ["SAST tools flood teams with findings, many false positives.", "Triage consumes the time meant for fixing."], THEME["warn"]),
    ("Slow remediation", ["Patches need context, tests and review.", "Critical flaws sit in backlogs for weeks."], THEME["crit"]),
    ("Risky fixes", ["A bad patch breaks functionality or adds new bugs.", "Teams hesitate to change working code."], THEME["primary"])]):
    card(s, Inches(0.5 + i * 4.15), Inches(1.7), Inches(3.95), Inches(2.6), h, b, c, 15)
text(s, Inches(0.5), Inches(4.7), Inches(12.3), Inches(1.5),
     "CodeMender closes the loop: it reasons about the codebase, proves a flaw is real, and proposes a tested patch for human approval.", 22, True, THEME["dark"])

# 3 What it is
s = slide("What is CodeMender?", "An autonomous AI code-security agent from Google (preview on Gemini Enterprise Agent Platform)")
steps = [("1  FIND", "Scans for vulnerabilities static and model-only scanners miss, using repo context.", THEME["primary"]),
         ("2  VERIFY", "Builds and runs proof-of-concept exploits in an isolated sandbox to confirm the flaw is real.", THEME["warn"]),
         ("3  FIX", "Generates a secure patch, validates build/tests, an LLM judge checks behaviour is preserved.", THEME["accent"])]
for i, (h, b, c) in enumerate(steps):
    x = Inches(0.5 + i * 4.2)
    box(s, x, Inches(1.8), Inches(3.8), Inches(0.7), c)
    text(s, x, Inches(1.8), Inches(3.8), Inches(0.7), h, 22, True, "FFFFFF", PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    box(s, x, Inches(2.5), Inches(3.8), Inches(1.9), THEME["card"])
    text(s, x + Inches(0.1), Inches(2.6), Inches(3.6), Inches(1.8), b, 15)
    if i < 2:
        text(s, x + Inches(3.75), Inches(1.85), Inches(0.5), Inches(0.6), "›", 32, True, THEME["mut"])
text(s, Inches(0.5), Inches(4.8), Inches(12.3), Inches(1.9),
     ["• Reactive: patches newly found flaws.  • Proactive: hardens code to remove whole vulnerability classes.",
      "• Developers approve every patch before commit.  • Fits CI/CD, CLI, VS Code and Antigravity."], 17)

# 4 Architecture
s = slide("How it works", "Local CLI keeps your code on your machine; the cloud agent reasons over targeted snippets")
parts = [("Your environment", "`cm` CLI: reads files, builds, runs PoCs and tests in your sandbox", THEME["accent"]),
         ("Gemini Enterprise Agent Platform", "CodeMender agent: plans scans, writes PoCs and patches, LLM-as-judge review", THEME["primary"]),
         ("Outputs", "Findings by severity/type, verification plan + tested exploits, code diffs for approval", THEME["warn"])]
for i, (h, b, c) in enumerate(parts):
    x = Inches(0.5 + i * 4.2)
    card(s, x, Inches(1.8), Inches(3.8), Inches(2.4), h, b, c, 14)
    if i < 2:
        text(s, x + Inches(3.75), Inches(2.7), Inches(0.5), Inches(0.6), "⇄" if i == 0 else "→", 28, True, THEME["mut"])
text(s, Inches(0.5), Inches(4.6), Inches(12.3), Inches(2.2),
     ["Tooling behind the agent: static + dynamic analysis, fuzzing, symbolic reasoning, differential testing.",
      "Governance: VPC routing, data isolation and encryption, zero retention of source code, model choice for cost vs depth."], 16)
notes(s, "Source: Google Cloud blog (Jul 2026) and CodeMender docs. Capabilities may change during preview.")

# 5 Coverage
s = slide("Coverage", "Languages and vulnerability classes")
card(s, Inches(0.5), Inches(1.7), Inches(5.9), Inches(2.2), "Languages", ["C/C++  ·  Go  ·  Java  ·  Python", "Ruby  ·  Rust  ·  TypeScript"], THEME["primary"], 18)
card(s, Inches(6.9), Inches(1.7), Inches(5.9), Inches(2.2), "Vulnerability classes",
     ["Memory corruption  ·  Injection", "Web security issues  ·  Cryptographic flaws", "Insecure data handling"], THEME["warn"], 18)
card(s, Inches(0.5), Inches(4.2), Inches(12.3), Inches(2.3), "Proven direction (Google DeepMind research)",
     ["72 security fixes upstreamed to open source (reported Oct 2025), incl. libwebp hardening with -fbounds-safety.",
      "All upstream patches were human-reviewed before submission."], THEME["accent"], 16)

# 6 Reports (screenshot)
s = slide("Reports and outputs", "Everything the analysis agent produces for a repository")
if SHOT.exists():
    s.shapes.add_picture(str(SHOT), Inches(7.3), Inches(1.5), width=Inches(5.6))
for i, (h, b) in enumerate([("Interactive HTML dashboard", "risk score, severity donut, OWASP exposure, filterable findings"),
                            ("Markdown executive summary", "paste into tickets / chat"),
                            ("SARIF 2.1.0", "GitHub code scanning, IDEs, DevSecOps pipelines"),
                            ("JSON + CSV", "dashboards, audit evidence, import to other tools"),
                            ("Patch set (unified diff)", "reviewable fixes, hand-off to the Defect-Fix agent"),
                            ("Per-finding detail", "CWE, OWASP, why it matters, fix, verification plan")]):
    y = Inches(1.5 + i * 0.9)
    box(s, Inches(0.5), y, Inches(0.12), Inches(0.75), THEME["primary"])
    text(s, Inches(0.7), y - Inches(0.05), Inches(6.4), Inches(0.4), h, 16, True, THEME["dark"])
    text(s, Inches(0.7), y + Inches(0.3), Inches(6.4), Inches(0.4), b, 13, False, THEME["mut"])

# 7 Architecture of the demo
s = slide("Demo architecture: agents working together via A2A")
nodes = [("Gemini Enterprise", "User asks:\n“Analyse and fix this repo”", THEME["dark"]),
         ("Defect-Fix Agent", "ADK · Agent Engine\nOrchestrates the fix", THEME["primary"]),
         ("CodeMender Analysis Agent", "ADK · A2A server\nFind · Verify plan · Fix", THEME["accent"]),
         ("Git repository", "Cloned read-only,\nscanned, discarded", THEME["warn"])]
for i, (h, b, c) in enumerate(nodes):
    x = Inches(0.4 + i * 3.2)
    box(s, x, Inches(2.0), Inches(2.8), Inches(1.9), c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, Inches(2.1), Inches(2.8), Inches(0.5), h, 16, True, "FFFFFF", PP_ALIGN.CENTER)
    text(s, x, Inches(2.8), Inches(2.8), Inches(1.0), b.split("\n"), 13, False, "FFFFFF", PP_ALIGN.CENTER)
    if i < 3:
        text(s, x + Inches(2.75), Inches(2.6), Inches(0.5), Inches(0.6), "→", 28, True, THEME["mut"])
text(s, Inches(0.4), Inches(4.3), Inches(12.5), Inches(0.5), "A2A: agent card at /.well-known/agent-card.json · JSON-RPC · IAM-authenticated on Cloud Run", 15, True, THEME["dark"])
text(s, Inches(0.4), Inches(4.9), Inches(12.5), Inches(2), [
    "1. Defect-Fix agent delegates repo analysis to CodeMender over A2A.",
    "2. CodeMender returns severity, CWE/OWASP, patches and report links.",
    "3. Defect-Fix agent applies approved fixes and re-runs analysis to confirm."], 16)

# 8 Demo results
d = DATA
s = slide("Live demo: results on the sample repository", f"{d['files_scanned']} files · {d['lines_scanned']:,} lines · Python, JavaScript, Java, C, Kubernetes YAML")
for i, (k, c) in enumerate([("CRITICAL", THEME["crit"]), ("HIGH", THEME["warn"]), ("MEDIUM", "F9AB00"), ("LOW", THEME["primary"])]):
    x = Inches(0.5 + i * 2.35)
    box(s, x, Inches(1.6), Inches(2.15), Inches(1.5), c)
    text(s, x, Inches(1.65), Inches(2.15), Inches(0.9), str(d["by_severity"][k]), 48, True, "FFFFFF", PP_ALIGN.CENTER)
    text(s, x, Inches(2.5), Inches(2.15), Inches(0.5), k.title(), 15, False, "FFFFFF", PP_ALIGN.CENTER)
box(s, Inches(10.0), Inches(1.6), Inches(2.85), Inches(1.5), THEME["dark"])
text(s, Inches(10.0), Inches(1.65), Inches(2.85), Inches(0.9), f"{d['risk_score']}/100", 40, True, "FFFFFF", PP_ALIGN.CENTER)
text(s, Inches(10.0), Inches(2.5), Inches(2.85), Inches(0.5), "Risk score", 15, False, "FFFFFF", PP_ALIGN.CENTER)
card(s, Inches(0.5), Inches(3.4), Inches(6.0), Inches(3.3), "Top weakness classes",
     [f"{c}  ×{n}" for c, n in d["top_cwes"]], THEME["crit"], 16)
card(s, Inches(6.9), Inches(3.4), Inches(5.95), Inches(3.3), "Remediation readiness",
     [f"{d['total_findings']} findings, {d['auto_fixable']} with a ready-to-review diff", "Every finding: CWE, OWASP category, fix guidance, verification plan",
      "Patches are suggestions; humans approve"], THEME["accent"], 16)

# 9 Value
s = slide("Business value")
for i, (h, b, c) in enumerate([("Faster remediation", "From finding to reviewed patch in one flow", THEME["primary"]),
                               ("Less noise", "Exploit verification reduces false positives", THEME["warn"]),
                               ("Safer changes", "Build/test validation and LLM-judge before approval", THEME["accent"]),
                               ("Audit-ready", "SARIF/JSON/CSV evidence, OWASP & CWE mapping", THEME["dark"])]):
    card(s, Inches(0.5 + (i % 2) * 6.25), Inches(1.6 + (i // 2) * 2.6), Inches(6.0), Inches(2.3), h, b, c, 18)

# 10 Next steps
s = slide("Next steps")
text(s, Inches(0.6), Inches(1.6), Inches(12), Inches(4.8), [
    "1.  Enable CodeMender preview on the Gemini Enterprise Agent Platform project",
    "2.  Install the `cm` CLI on build/dev hosts; connect to the analysis agent",
    "3.  Wire the analysis agent into CI and the Defect-Fix agent via A2A",
    "4.  Pilot on 2–3 priority repositories; track time-to-fix and false-positive rate",
    "5.  Expand: scheduled scans, SARIF into code scanning, Wiz / AI Threat Defense integration"], 22)
text(s, Inches(0.6), Inches(6.2), Inches(12), Inches(0.6),
     "Sources: Google Cloud blog “Now in preview: Find and fix software vulnerabilities with CodeMender” (Jul 2026); Google DeepMind announcement (Oct 2025).", 11, False, THEME["mut"])

out = ROOT / "CodeMender_Overview.pptx"
prs.save(out)
print("saved", out)
