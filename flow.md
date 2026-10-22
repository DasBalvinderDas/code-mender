# How CodeMender and this agent work (flow)

**Short version:** CodeMender is a command-line tool (`cm`) that runs on a machine you control. An agent on Agent Engine cannot run a
CLI itself, and `cm` runs exploit code, so it must not run inside the agent anyway. **The agent therefore calls a sandboxed runner that
runs `cm` (section 3).** The runner and the agent's tools for it are built and tested against a **simulator** of `cm`, not yet against the real CLI. If no runner is
configured, the agent falls back to its own built-in scanner and says so. This file explains both engines, what is verified and what is not.

---

## 1. What CodeMender (`cm`) is and how it works
Facts below come from Google's CodeMender CLI codelab and launch material, not from running `cm` here.

* **A local CLI plus a Google-hosted agent.** `cm` runs on your machine or VM. It reads files, runs builds and tests, and runs exploit
  scripts locally. It sends only targeted code snippets and tool results to Google's backend (`aiplatform.googleapis.com`), where
  Gemini models do the reasoning. During `cm find`, the files in the scan folder are uploaded for analysis.
* **Three stages, each a command:**

| Stage | Command | What happens | Time (codelab) |
|---|---|---|---|
| Find | `cm find <dir> [--deep]` | The model reads the code with tools (`list_dir`, `read_file`, ...) and reports vulnerabilities, each with an 8-character ID (a prefix of a full UUID), severity and a CWE type | about 1 min for one file |
| Verify | `cm verify <id>` | Writes a reproduction plan and an exploit script into `<dir>/.exploit/` and **runs it on the same machine**; the finding becomes VERIFIED if the exploit works | about 3 min |
| Fix | `cm fix <id> [-c "<project rules>"]` | Resets the folder, writes a patch, re-runs the exploit to confirm it is blocked, runs your `build.command`, prints the diff and applies it to the working tree; the finding becomes FIXED | about 5-7 min |

* **State and reports.** Everything lives in `~/.codemender` (or `$CM_HOME`): `config.yaml` and `state.db`. `cm report` lists **every** finding in that
  database; `cm report --format json` prints a JSON array (`finding_id`, `session_id`, `title`, `file_path`, `severity`, `confidence`,
  `analysis`, `snippet`, `vuln_type`, `vuln_id`, `status`, `start_line`, `end_line`); `--format html` writes `~/.codemender/reports/report.html`.
  `cm report import --file x.json` accepts findings from other scanners (simple JSON or SARIF 2.1.0).
* **Configuration (`config.yaml`).** `vcs.type: git` (used to reset and diff the workspace), `build.command` (run after a fix to prove the code still builds),
  `tools.confirm_commands` and `tools.confirm_writes` (default `true`: it asks `[Y/n]` before every command and file write, 10 or more prompts per verify),
  `scan.extensions.include`. Automation passes `-y --bypass-warning` to skip the prompts. A filesystem sandbox is on by default.
* **Sharp edges the codelab warns about**
  * With `vcs.type: git`, `cm verify` and `cm fix` run `git checkout HEAD -- . && git clean -fd`: uncommitted and untracked files in the scan folder are **deleted**.
  * `cm fix` creates a snapshot repo (`<dir>/.git`, a symlink into `/tmp`) and later runs reset to it, silently reverting earlier fixes unless it is removed.
  * `cm verify` runs the exploit on your machine (the lab's example reads `/etc/passwd`). Use a disposable sandbox or VM.
  * Results are LLM-generated and vary between runs; the quick scan focuses on injection-style flaws, `--deep` is exhaustive.

```
developer / CI machine                                         Google
┌──────────────────────────────────────────┐                  ┌───────────────────────┐
│ cm find ./app      → reads files ────────┼─ snippets ─────▶ │ CodeMender agent      │
│ cm verify <id>     → runs exploit locally│ ◀─ plan/steps ── │ (Gemini models,       │
│ cm fix <id>        → applies patch, build│ ─ tool results ▶ │  aiplatform.googleapis│
│ ~/.codemender/state.db, .exploit/, git   │                  └───────────────────────┘
└──────────────────────────────────────────┘
```

---

## 2. The built-in quick scan (no `cm` involved; the fallback)
The deployed agent is a plain ADK agent. Its job: take a repo, scan it, report.

```
User in Gemini Enterprise
   │  "Analyse https://github.com/juice-shop/juice-shop"
   ▼
CodeMender Scan Agent (ADK, on Agent Engine; Gemini decides which tool to call)
   │  tool: analyze_repository(repo_url, ref, subdir)
   ▼
1. Fetch      git clone --depth 1  (or a GitHub tarball if the runtime has no git); only https GitHub URLs or local paths
2. Scan       codemender_agent/scanner.py applies 24 rules (rules.py) line by line over source/config files
              skips: .git, node_modules, vendor, build folders, test folders and test files, minified files
3. Findings   each: id, severity, CWE, OWASP category, file:line, snippet, why it matters, fix, verification plan, optional patch
4. Reports    PDF (pdf_report.py, reportlab) and Markdown (reports.py), built in memory
5. Reply      the agent writes a short text summary; after_agent_callback attaches both files to the reply
              (the findings are also saved in the conversation's session state)
   ▼
Follow-up questions use tools over the saved findings:
   search_findings (filter by folder / CWE / severity), get_finding_details, get_fix_candidates (patch diffs), get_report (md/json/sarif/csv/patch text)
```

* **No bucket.** Reports are generated in memory and attached to the reply; the agent's code is deployed inline (see the README).
* **Honest labelling.** Every report names its engine: "Built-in rule engine (CodeMender-style)". The scanner is pattern-based: it does not build
  or run exploits, and "verification plan" means a described test, not an executed one. Patches are suggestions.
* **Verified vs not.** Verified locally: scanning, reports, tool flow with a scripted model, running inside `AdkApp`, the bucket-free deploy request.
  Not yet verified: a real deploy, a real Gemini call, GitHub download from the Agent Engine runtime, Gemini Enterprise showing the file attachments.

---

## 3. How the agent calls the real CodeMender (`cm`)
**The problem.** `cm` is a native binary with a writable disk, git, the repo's dependencies and a place to run exploits. Agent Engine runs your Python code;
it is not a place to install an arbitrary CLI, and `cm verify` must not execute exploit scripts next to the agent's credentials.
So the agent never runs `cm`. It calls a **runner**: a small HTTP service in a sandbox where `cm` is installed.

```
Gemini Enterprise ─▶ CodeMender agent (Agent Engine)
                          │  run_codemender(repo, subdir, verify_top, fix_top, ...)   → returns a run id
                          │  check_codemender_run(run id)                              → progress, then final result
                          │  HTTPS + ID token (IAM-protected)
                          ▼
                 Runner (Cloud Run, dedicated service account with only roles/aiplatform.user)
                   per job, in a throwaway directory:
                   1. git clone --depth 1 <repo>                     fresh clone, committed baseline
                   2. CM_HOME=<job dir>; cm init                      so cm report only ever shows this job's findings
                      set config.yaml: vcs.type=git, build.command, confirm_commands=false, confirm_writes=false
                   3. cm find <dir> [--deep] -y --bypass-warning      → talks to aiplatform.googleapis.com
                   4. cm report --format json                          → parse findings (tolerates log lines before the JSON)
                   5. cm verify <id> -y --bypass-warning               for the top N open findings; copy .exploit/REPORT.md and PLAN.md
                   6. cm fix <id> [-c rules] -y --bypass-warning       for the top M verified findings; capture `git diff`,
                                                                       reset the tree, remove the snapshot symlink
                   7. cm report --format json                          → final statuses OPEN / VERIFIED / FIXED; delete the job directory
                          │  JSON: findings + exploit evidence + diffs
                          ▼
                 Agent builds the PDF + Markdown from the real results ("Engine: CodeMender CLI (cm)"),
                 attaches them to the reply, and keeps the findings for follow-up questions.
```

* **Why asynchronous.** One find, verify and fix takes roughly 10 minutes, longer than a chat turn should block. The agent starts a run, the user (or the defect-fix agent)
  asks again, and the agent returns the current stage until it completes.
* **Scope today: find and report only.** The runner ignores verify and fix requests unless `RUNNER_ALLOW_VERIFY_FIX=1` is set on it, and the agent never asks for them by default. That is deliberate: `cm verify` runs exploit code on the runner.
* **Safety measures built in.** One clone and one `CM_HOME` per job; the `cm` sandbox left on; no GitHub tokens passed into the `cm` environment; request validation (https GitHub URLs only, no `..` in paths, safe ref names); IAM-only access to the runner; one instance, results kept in memory for an hour. **Be aware:** the runner runs as the service account in `.env` (the one with CodeMender access), which in your project has broad access. With find-only that is acceptable; before enabling verify and fix, give the runner a dedicated service account with only the roles `cm` needs (`RUNNER_SA` in `deploy/deploy_runner.sh`).
* **Both engines.** The agent keeps the built-in scan for quick results and as a fallback when the runner is not configured; the report always says which engine produced it.
* **What is tested.** The orchestration passes tests against `tests/fake_cm.py`, a **simulator** written from the codelab. Nothing here has run against the real `cm`.
  Unconfirmed: how `cm` authenticates with a service account (assumed Application Default Credentials), flags beyond those in the codelab,
  the exact output of your build of `cm`, exit codes, and whether Gemini Enterprise and A2A tolerate runs of many minutes.

## 4. Where this connects to the defect-fix agent (later)
The planned chain: user → Gemini Enterprise → defect-fix agent → (A2A) → CodeMender agent → runner → `cm`. The scan agent returns findings with IDs, file and line, CWE,
status and diffs (`get_fix_candidates`); the defect-fix agent applies approved fixes. The A2A packaging is parked in `future/`.

## 5. Quick reference
| Question | Answer |
|---|---|
| Does the agent call the real CodeMender? | Yes, through the runner, when `CODEMENDER_RUNNER_URL` is set: `cm find` and `cm report` today (verify and fix are built but switched off). Otherwise it uses its built-in scanner and every report says which engine ran. |
| Can an Agent Engine agent run `cm` directly? | Not safely. It needs a sandboxed runner, as in section 3. |
| Does the PDF/Markdown use a bucket? | No. Both are generated in memory and attached to the reply. |
| Where does source code go? | Built-in scan: stays in the agent's runtime and is discarded. Real `cm`: uploaded to Google's CodeMender backend during `cm find`. |
| Which code is where? | Agent: `codemender_agent/` (agent, `cm_tools.py`, `runner_client.py`, built-in scanner, rules, reports, PDF). Runner: `runner/` (Cloud Run service wrapping `cm`). Deploy: `deploy/`. Parked: `future/` (A2A). |
