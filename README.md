# CodeMender Analysis Agent

An ADK agent that runs **Google CodeMender** (`cm` CLI: find, exploit verification, validated fixes) on a GitHub repo and
returns a **PDF report**. It is served over **A2A on Agent Engine** so the existing defect-fix agent can call it, and it
is registered in Gemini Enterprise.

```
Gemini Enterprise ─▶ Defect-Fix agent (Agent Engine) ──A2A──▶ CodeMender agent (Agent Engine)
                                                                  │ HTTPS + ID token
                                                                  ▼
                                             CodeMender runner (Cloud Run, sandbox, `cm` CLI) ──▶ Vertex AI
                                                 clone → cm find → cm verify → cm fix → findings JSON
                                                                  │
                          PDF built in the agent and attached to the reply (nothing stored in a bucket)
```

## Two engines (always labelled in the report)
| | Real CodeMender | Built-in quick scan |
|---|---|---|
| Tools | `run_codemender`, `check_codemender_run` | `analyze_repository` |
| Engine | Google CodeMender CLI via the runner | Rule-based scanner in this repo (not CodeMender) |
| Speed | Minutes (find 1-10, verify ~3 each, fix ~5-7 each) | Seconds |
| Verification | A real exploit is built and run in the sandbox (VERIFIED) | Describes a test plan only |
| Fixes | Patch validated by your build command (FIXED) | Mechanical suggestions for some rules |
| Results | LLM-based, can vary between runs | Deterministic |

The agent uses real CodeMender by default when `CODEMENDER_RUNNER_URL` is set, and the built-in scan otherwise or on request.

## Why a separate runner
`cm verify` builds and **runs exploit scripts on the machine where `cm` runs** (the lab's example reads `/etc/passwd`), and
`cm verify`/`cm fix` reset the scan directory with `git checkout HEAD -- . && git clean -fd`. That must not happen in the
agent's own runtime. The runner (`runner/`) is a Cloud Run service where each job gets:
a fresh clone, its own `CM_HOME` (so `cm report` never shows other jobs' findings), the `cm` sandbox left **on**, no
GitHub tokens in the `cm` environment, and a dedicated service account with only `roles/aiplatform.user`.
Source code is sent to Google's CodeMender backend (`aiplatform.googleapis.com`) as part of `cm find`; confirm that is
acceptable for each repo you scan.

## What the runner does per request (`POST /v1/analyses`)
1. Clone the GitHub repo (shallow), choose the scan folder (`subdir`).
2. `cm init`, then set `vcs.type: git`, `build.command` (Python repos default to `python3 -m compileall -q .`; other
   languages default to a no-op because the image has no toolchains, so set `build_command` for them), and turn the
   interactive confirmations off.
3. `cm find <dir> [--deep] -y --bypass-warning`, then read `cm report --format json`.
4. `cm verify <id>` for the top `verify_top` open findings (default 2); collect `.exploit/REPORT.md` and `PLAN.md`.
5. `cm fix <id> [-c context]` for the top `fix_top` verified findings (default 1); capture `git diff`, reset the tree.
6. Return findings with status OPEN / VERIFIED / FIXED, evidence and diffs. Poll with `GET /v1/analyses/{id}`.

## PDF report
One PDF (`CodeMender_Security_Report.pdf`): engine used, risk score, severity chart, OWASP exposure, findings overview with
status, and per-finding detail (CWE, analysis, verification evidence, proposed diff). It is built in memory in the agent
and attached to the reply as an A2A file part. Sample: [`docs/sample-report/report.pdf`](docs/sample-report/report.pdf)
(built-in engine). Whether Gemini Enterprise renders the file part is not verified; the text summary always carries the key findings.

## Deploy
```bash
# 1. Get the cm binary (needs your CodeMender access)
gcloud artifacts generic download --project=cmoc-prod --location=us --repository=codemender-cli-production \
  --package=cm --version=stable --name=cm-linux-amd64.zip --destination=runner/
# 2. Runner on Cloud Run (IAM-protected; AGENT_SA = the CodeMender agent's runtime service account)
PROJECT=<proj> REGION=us-central1 AGENT_SA=<agent-sa-email> ./deploy/deploy_runner.sh
# 3. Agent on Agent Engine (A2A)
python deploy/deploy_agent_engine.py --project <proj> --location us-central1 \
  --staging-bucket gs://<staging-bucket> --runner-url <runner URL> [--service-account <agent-sa-email>]
```
Then connect the defect-fix agent with [`deploy/defect_fix_client_example.py`](deploy/defect_fix_client_example.py)
(`RemoteA2aAgent`; its service account needs `roles/aiplatform.user`) and register the agent in Gemini Enterprise as you did the defect-fix agent.

**Needs your confirmation (could not be verified from here):**
* The service account that `cm` uses on Cloud Run (the runner SA) must be allowed to use CodeMender/Vertex AI in your project; the lab does not show the auth step, so I assumed Application Default Credentials.
* The `cm` binary's exact flags beyond those in the lab (`-y --bypass-warning`, `-c`, `--deep`, `--format json`). The runner retries `cm` without `-y --bypass-warning` if the CLI rejects them.
* The agent-card URL on Agent Engine and Gemini Enterprise's rendering of the PDF (see below in the test plan).
* Timeouts: a real run takes many minutes, so the agent starts a run and the user (or the defect-fix agent) checks back with `check_codemender_run`. The runner keeps results in memory for 1 hour and runs as one instance.

## Local development
```bash
pip install -r requirements-dev.txt
pytest          # 17+ tests; the runner tests use tests/fake_cm.py, a SIMULATOR of the cm CLI, not CodeMender itself
adk web .       # agent chat UI (needs Vertex credentials)
```
`tests/fake_cm.py` reproduces the codelab's documented command shapes so the orchestration can be tested offline.
It cannot tell you whether the real `cm` behaves identically; run Stage 6 of the test plan against the real CLI.

## Demo repo
`demo/vulnerable-app/` is intentionally insecure. Never deploy it.
Prompts: [`docs/DEMO_PROMPTS.md`](docs/DEMO_PROMPTS.md). Test plan: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md). Deck: `ppt/CodeMender_Overview.pptx`.
