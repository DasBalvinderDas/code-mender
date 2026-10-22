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

## Deploy to Agent Engine
```bash
git clone -b claude/charming-gauss-uyqs3b https://github.com/DasBalvinderDas/code-mender.git
cd code-mender
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project <PROJECT_ID>
# one bucket is needed only to upload the deployment package (the reports do not use it); reuse any existing bucket
gcloud storage buckets create gs://<STAGING_BUCKET> --project <PROJECT_ID> --location us-central1   # skip if you have one

python deploy/deploy_agent_engine.py --project <PROJECT_ID> --location us-central1 \
  --staging-bucket gs://<STAGING_BUCKET> --model gemini-2.5-flash    # use a Gemini model available in your project
```
The last line prints the engine's resource name. To redeploy after changes, add `--update <that resource name>`.
Then register it in Gemini Enterprise the way you did the defect-fix agent (ADK agent on Agent Engine).

**Not verified yet (first deploy will tell):** the deploy call itself, the model name for your project, GitHub downloads from the
Agent Engine runtime, and whether Gemini Enterprise displays the file attachments. Every reply carries both a PDF and a
Markdown copy of the report (the `.md` is the fallback if the PDF does not render), plus a short text summary.

## Demo
`demo/vulnerable-app/` is intentionally insecure (never deploy it); the scan finds 33 issues (9 Critical, 16 High, 8 Medium).
Sample report: [`docs/sample-report/report.pdf`](docs/sample-report/report.pdf). Demo with Juice Shop: [`demo.md`](demo.md). Small demo repo prompts: [`docs/DEMO_PROMPTS.md`](docs/DEMO_PROMPTS.md).
Test plan: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md). Deck: `ppt/CodeMender_Overview.pptx`.
