# CodeMender Scan Agent

An ADK agent on Agent Engine. You give it a GitHub repo; it scans the code for security vulnerabilities with **Google CodeMender**
and answers with a summary plus a **PDF report and a Markdown copy** (risk score, severity chart, OWASP/CWE mapping, every finding
with why it matters, and the fix or patch where there is one).

```
User (Gemini Enterprise) → CodeMender Scan Agent (Agent Engine)
                              │  run_codemender / check_codemender_run       HTTPS + ID token (IAM)
                              ▼
                        CodeMender runner (Cloud Run, sandbox, `cm` CLI) → clones the repo → cm find → cm report → findings JSON
                              │                                                   │
                              │                                                   └→ Google's CodeMender backend (aiplatform.googleapis.com)
                              ▼
              PDF + Markdown built in the agent from the real findings, attached to the reply (no bucket)
```

## Two engines (every report names the one it used)
| | Real CodeMender | Built-in quick scan |
|---|---|---|
| Tools | `run_codemender`, `check_codemender_run` | `analyze_repository` |
| What runs | Google's CodeMender CLI (`cm`) in the runner | The rule-based scanner in this repo (not CodeMender) |
| Used when | The runner is configured (`CODEMENDER_RUNNER_URL`); the default | No runner configured, the runner is down, or you ask for a "quick scan" |
| Speed | Minutes | Seconds |
| Results | LLM-based; can vary between runs | Deterministic |

**Scope today: find and report only.** CodeMender can also verify findings with a real exploit and generate validated fixes (`cm verify`, `cm fix`).
Those are built but switched off on the runner (`RUNNER_ALLOW_VERIFY_FIX` is not set), because `cm verify` runs exploit code on the machine it is on.
Turn them on later once you are comfortable with that sandbox.

## Why a separate runner
`cm` is a command-line tool. An Agent Engine agent cannot install and run one safely, and `cm` resets the folder it scans
(`git checkout HEAD -- . && git clean -fd`) and, when verifying, runs exploit scripts. So the agent calls a small **runner service** (`runner/`,
Cloud Run) where `cm` is installed. Each job gets a fresh clone and its own `CM_HOME`, runs `cm` non-interactively (`-y --bypass-warning`) with the
sandbox left on, and the runner has no GitHub tokens in `cm`'s environment. More detail in [`flow.md`](flow.md).
`cm find` uploads the scanned files to Google's CodeMender backend; confirm that is acceptable for each repo.

## Use
Ask: `Analyse https://github.com/<owner>/<repo>` (optionally `folder <path>` or `branch <name>`). The first answer says the scan is running; ask again
for the status. Follow-ups: findings under a folder or of a type, one finding's details, patches, SARIF/CSV/JSON/Markdown text.
The agent remembers the last scan in the conversation.

## Run locally
```bash
pip install -r requirements-dev.txt
pytest                                         # tests run offline; the runner tests use tests/fake_cm.py, a SIMULATOR of the cm CLI
export GOOGLE_GENAI_USE_VERTEXAI=true GOOGLE_CLOUD_PROJECT=<proj> GOOGLE_CLOUD_LOCATION=us-central1
adk web .                                      # chat UI; without CODEMENDER_RUNNER_URL it uses the built-in scan
```
Private repos: set `GITHUB_TOKEN` for the built-in scan. If the host has no `git` binary, github.com repos are downloaded as a tarball.

## Deploy
```bash
git clone https://github.com/DasBalvinderDas/code-mender.git
cd code-mender
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com cloudbuild.googleapis.com --project gebu-demo-sandbox
cp .env.example .env            # repository root; edit if needed (project, region, service account, model)
```
**1. The CodeMender runner (Cloud Run).** Needs your access to the CodeMender download; the service account in `.env` runs the runner, so it must be the one that can use CodeMender.
```bash
./deploy/deploy_runner.sh                      # downloads cm, builds the image, deploys, saves CODEMENDER_RUNNER_URL in .env
python deploy/check_runner.py                  # checks the runner on its own: runs cm find on demo/vulnerable-app and prints the findings
```
**2. The agent (Agent Engine, ADK's own deploy command, no bucket).**
```bash
python deploy/deploy_agent_engine.py --dry-run     # shows the settings and the command, deploys nothing
python deploy/deploy_agent_engine.py               # deploys, saves AGENT_ENGINE_RESOURCE in .env, runs a smoke test
```
Run step 2 again after any change; it updates the saved engine (`--new` makes a separate one). It passes `CODEMENDER_RUNNER_URL` to the agent.
Without a runner URL the agent still deploys and uses the built-in scan only.
**Do not create a `.env` inside `codemender_agent/`**: `adk deploy` would read it and override the settings (the script stops if it finds one).

Permissions: the service account needs `roles/aiplatform.user` (and CodeMender access for the runner); the agent's identity needs `roles/run.invoker` on the runner
(the runner script grants it); whoever deploys needs `roles/iam.serviceAccountUser` on the service account.

Test and debug the deployed agent from the shell:
```bash
python deploy/query_agent_engine.py                # chat: ask it to analyse a repo, then ask for the status; saves the PDF and .md to reports_out/
python deploy/agent_engine_logs.py                 # key lines of the engine's logs; add --full for everything
```

## What is verified and what is not
Verified locally: the agent, tools and reports; the runner pipeline and the whole agent → runner → PDF chain against the `cm` **simulator**; the deploy
requests (ADK's own deploy command with the cloud call intercepted). The built-in scan and the agent on Agent Engine ran for real in your project.
**Not verified:** the runner against the real `cm` CLI. Open points: how `cm` authenticates with the service account on Cloud Run (assumed Application Default
Credentials), whether `cm`'s sandbox works inside Cloud Run, flags beyond those in the codelab, the exact JSON of your build of `cm`, and whether a long run fits
Gemini Enterprise's response time. `deploy/check_runner.py` is the first test; send me its output.

## More
Demo with Juice Shop: [`demo.md`](demo.md). How it all works: [`flow.md`](flow.md). CodeMender CLI demo script: [`cli-demo.md`](cli-demo.md).
Short version, commands and why: [`basic-demo-commands.md`](basic-demo-commands.md). Test plan: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md).
Small demo repo prompts: [`docs/DEMO_PROMPTS.md`](docs/DEMO_PROMPTS.md). Deck: `ppt/CodeMender_Overview.pptx`. A2A packaging and the defect-fix hand-off are parked in [`future/`](future/README.md).
`demo/vulnerable-app/` is intentionally insecure; never deploy it.
