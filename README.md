# CodeMender Analysis Agent

An ADK agent that analyses a git repository for security vulnerabilities and returns CodeMender-style
results (Find → Verification plan → Fix) plus a full report pack. It is served over **A2A** so the existing
defect-fix agent can call it.

```
Gemini Enterprise → Defect-Fix agent (Agent Engine) ──A2A──▶ CodeMender Analysis agent (Agent Engine)
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
adk web .        # chat UI; ask: "analyse demo/vulnerable-app"
```
Private repos: set `GITHUB_TOKEN`. If the host has no `git` binary (Agent Engine), github.com repos are fetched as a tarball.

## Deploy to Agent Engine (A2A)
```bash
gcloud auth application-default login
python deploy/deploy_agent_engine.py --project <proj> --location us-central1 \
  --staging-bucket gs://<staging-bucket> --reports-bucket gs://<reports-bucket-name>   # bucket name only for reports
```
It prints the resource name, A2A endpoint and agent-card URL. Checks after deploy:
1. `curl -H "Authorization: Bearer $(gcloud auth print-access-token)" <card URL>` returns the agent card.
2. Reports: grant the engine's service account `roles/storage.objectAdmin` on the reports bucket and
   `roles/iam.serviceAccountTokenCreator` on itself (for 24h signed links to the HTML dashboard). Without signing,
   the agent returns `gs://` URIs, and the Markdown summary can always be returned in chat.
3. Sessions and tasks are in memory, so the deploy pins `min/max_instances=1`. Raise that only after moving state
   to a persistent session service.

## Connect the defect-fix agent
Add the CodeMender agent as a `RemoteA2aAgent` in the defect-fix agent
([`deploy/defect_fix_client_example.py`](deploy/defect_fix_client_example.py)), redeploy it, and give its runtime
service account `roles/aiplatform.user`.

## Gemini Enterprise
Register CodeMender via the Gemini Enterprise admin (Agents → add a custom A2A agent, pasting the agent card JSON) or
the registration API, as you did for the defect-fix agent. Check Google's current "register ADK and A2A agents in
Gemini Enterprise" doc, since the steps move. If registration requires an `url` in the card that Gemini Enterprise
can reach, use the A2A endpoint printed by the deploy script.
Status: deployment code is written against the installed SDK (`google-cloud-aiplatform` 2.6.0, `a2a-sdk` 1.2.3) and the
`A2aAgent` builds locally, but nothing has been deployed or called live.

## Demo repo
`demo/vulnerable-app/` is intentionally insecure (SQLi, command injection, XSS, secrets, deserialisation, buffer
overflow, privileged pod…). Never deploy it.

## Deck
`ppt/CodeMender_Overview.pptx` (rebuild with `python ppt/build_deck.py`; restyle via `THEME`/`TEMPLATE`).
