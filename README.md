# CodeMender Scan Agent

A simple ADK agent. You give it a GitHub repo; it scans the code for security vulnerabilities and answers with a summary
and a **PDF report plus a Markdown copy** (risk score, severity chart, OWASP/CWE mapping, every finding with why it matters, the fix, and a
suggested patch where one is mechanical).

```
User (Gemini Enterprise) → CodeMender Scan Agent (Agent Engine) → clones repo → scans → PDF + Markdown + summary in the reply
```

**What it is:** a built-in, rule-based scanner (24 rules; Python, JS/TS, Java, Go, C/C++, Ruby, Rust, Kubernetes/Terraform
config) in the CodeMender style. **It is not Google's CodeMender product**: it does not run exploits or validate fixes, and
the report says so. The work to call the real CodeMender CLI and to expose the agent over A2A is parked in
[`future/`](future/README.md) until this simple version works.

## Use
Ask: `Analyse https://github.com/<owner>/<repo>` (optionally `folder <path>` or `branch <name>`). Follow-ups: finding details,
the fixes with diffs, SARIF/CSV/JSON/Markdown text. The agent remembers the last scan in the conversation.

## Run locally
```bash
pip install -r requirements-dev.txt
pytest                                         # 10 tests, no cloud needed
export GOOGLE_GENAI_USE_VERTEXAI=true GOOGLE_CLOUD_PROJECT=<proj> GOOGLE_CLOUD_LOCATION=us-central1
adk web .                                      # chat UI, ask: "analyse demo/vulnerable-app"
```
Private repos: set `GITHUB_TOKEN`. If the host has no `git` binary, github.com repos are downloaded as a tarball.

## Deploy to Agent Engine (ADK's own command, no bucket)
```bash
git clone https://github.com/DasBalvinderDas/code-mender.git
cd code-mender
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com cloudbuild.googleapis.com --project gebu-demo-sandbox

cp .env.example .env            # repository root; edit if needed (project, region, service account, model)
python deploy/deploy_agent_engine.py --dry-run     # shows the settings and the command, deploys nothing
python deploy/deploy_agent_engine.py               # deploys, saves AGENT_ENGINE_RESOURCE in .env, runs a smoke test
```
This follows the same pattern as the market-campaign-agent deploy: it runs `adk deploy agent_engine --project --region
--agent_engine_config_file=<json>` where the JSON carries the runtime settings (`CODEMENDER_MODEL`) and the service account. ADK builds a
Dockerfile (Python 3.11, installs ADK and `codemender_agent/requirements.txt`) and sends the agent source inline, so there is no bucket.
Run it again later to update the same engine (the ID is saved in `.env`); `--new` creates a separate one.
**Do not create a `.env` inside `codemender_agent/`**: `adk deploy` would read it and override the settings (the script stops if it finds one).

The service account is the identity the agent runs as. It needs `roles/aiplatform.user`; whoever deploys needs
`roles/iam.serviceAccountUser` on it. The agent needs nothing else: it clones public repos over HTTPS and writes nothing to GCP.

Test and debug the deployed agent from the shell:
```bash
python deploy/query_agent_engine.py "Analyse https://github.com/juice-shop/juice-shop"   # prints the answer, saves the PDF and .md to reports_out/
python deploy/agent_engine_logs.py                 # key lines of the engine's logs; add --full for everything
```
The container started by `adk api_server` also serves A2A (`--a2a` is on by default in ADK's deployment), which may help later.

**Not verified yet (first deploy will tell):** the deploy call itself, the model name for your project, GitHub downloads from the
Agent Engine runtime, the first successful start of the engine (a first attempt with a hand-built request failed to start; this version uses ADK's own deploy command), and whether Gemini Enterprise displays the file attachments. Every reply carries both a PDF and a
Markdown copy of the report (the `.md` is the fallback if the PDF does not render), plus a short text summary.

## Demo
`demo/vulnerable-app/` is intentionally insecure (never deploy it); the scan finds 33 issues (9 Critical, 16 High, 8 Medium).
Sample report: [`docs/sample-report/report.pdf`](docs/sample-report/report.pdf). How it all works (including how the real `cm` CLI would be called): [`flow.md`](flow.md). Demo with Juice Shop: [`demo.md`](demo.md). Small demo repo prompts: [`docs/DEMO_PROMPTS.md`](docs/DEMO_PROMPTS.md).
Test plan: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md). Deck: `ppt/CodeMender_Overview.pptx`.
