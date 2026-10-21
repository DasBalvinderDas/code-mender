# CodeMender Analysis Agent

An ADK agent that analyses a git repository for security vulnerabilities and returns CodeMender-style
results (Find → Verification plan → Fix) plus a full report pack. It is served over **A2A** so the existing
defect-fix agent can call it.

```
Gemini Enterprise → Defect-Fix agent (Agent Engine) ──A2A──▶ CodeMender Analysis agent (Cloud Run)
                                                                   │ clone → scan → reports (HTML/MD/JSON/SARIF/CSV/diff)
```

## Important: what runs where
Google's CodeMender (`cm find | verify | fix | report`) is a **preview product**; its hosted agent and `cm` CLI
need preview access, so they cannot be exercised from this repo. This agent therefore ships:

* a **built-in analysis engine** (`codemender_agent/rules.py`, 24 rules across Python, JS/TS, Java, Go, C/C++,
  Ruby, Rust, IaC; mapped to CWE and OWASP Top 10 2021) that works today and produces the demo reports, and
* a **`cm` CLI hook** (`analyze_repository(..., use_codemender_cli=True)`): if `cm` is installed on the host
  it runs `cm find`, `cm verify`, `cm fix` and returns their output alongside the built-in results.

The built-in engine is pattern-based; it does not build or run exploits. The "verification plan" per finding is a
described, non-weaponised test, not an executed PoC. Patches are suggestions for human review.

## Reports produced per scan
| File | Use |
|---|---|
| `report.html` | Interactive dashboard: risk score, severity donut, OWASP exposure, filterable findings with diffs |
| `report.md` | Executive summary for tickets/chat |
| `report.json` | Machine-readable (summary + findings) |
| `report.sarif` | SARIF 2.1.0 for GitHub code scanning / IDEs |
| `report.csv` | Audit / spreadsheet evidence |
| `patches.diff` | Unified-diff fixes for the defect-fix agent |

Example output for the demo app: [`docs/sample-report/`](docs/sample-report/).

## Run locally
```bash
pip install -r requirements-dev.txt
pytest
export GOOGLE_GENAI_USE_VERTEXAI=true GOOGLE_CLOUD_PROJECT=<proj> GOOGLE_CLOUD_LOCATION=us-central1
adk web .                                     # chat UI; ask: "analyse demo/vulnerable-app"
uvicorn codemender_agent.a2a_app:a2a_app --port 8080   # A2A server
curl localhost:8080/.well-known/agent-card.json
```
Private repos: set `GITHUB_TOKEN`. Optional `CODEMENDER_REPORT_BUCKET` uploads reports to GCS and returns `gs://` URIs
(A2A text responses cannot carry the HTML file inline).

## Deploy and connect
```bash
PROJECT=<proj> REGION=us-central1 BUCKET=<reports-bucket> ./deploy/deploy_cloud_run.sh
```
Grant the defect-fix agent's service account `roles/run.invoker`, then follow
[`deploy/defect_fix_client_example.py`](deploy/defect_fix_client_example.py) to add it as a `RemoteA2aAgent`.
Not yet verified end-to-end against a live Gemini model or Cloud Run; the A2A card and tools are covered by local checks.

## Demo repo
`demo/vulnerable-app/` is intentionally insecure (SQLi, command injection, XSS, secrets, deserialisation, buffer
overflow, privileged pod…). Never deploy it.

## Deck
`ppt/CodeMender_Overview.pptx` (rebuild with `python ppt/build_deck.py`; restyle via `THEME`/`TEMPLATE`).
