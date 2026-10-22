# CodeMender CLI demo: find, verify, fix, and the documents it generates

A presenter's script for showing Google CodeMender (`cm`) on the command line. It follows the nine sections of Google's
"CodeMender CLI Basics" codelab, with commands and expected output taken from it, plus a "show this" note so you can open the
documents CodeMender writes at each step.

> **Read before presenting**
> * `cm verify` **runs an exploit script on the machine you are on** (the codelab's example reads `/etc/passwd`). Use a disposable
>   VM or a fresh Cloud Shell, never a laptop or shared host with credentials.
> * With `vcs.type: git`, `cm verify` and `cm fix` run `git checkout HEAD -- . && git clean -fd` in the scanned folder: **uncommitted or
>   untracked files there are deleted.** Always commit first, and only run it on the lab folder.
> * `cm find` uploads the files in the scanned folder to Google's CodeMender backend (`aiplatform.googleapis.com`) for analysis.
> * Results are LLM-generated and **vary between runs**. Do not promise exact counts; rehearse once and keep screenshots as a fallback.
> * Marked **(assumed)** below means it is not shown in the codelab screenshots and you should confirm it on your machine.

## At a glance
| # | Section | Commands | Time | What you can show |
|---|---|---|---|---|
| 1 | Introduction | none | 2 min | Slide: find, verify, fix, human approval |
| 2 | Installation and setup | `gcloud artifacts ...`, `cm --version` | 3 min | The version output |
| 3 | Sample application | create `sample_app/`, venv, git baseline | 3 min | The deliberately vulnerable code |
| 4 | Initializing the workspace | `cm init`, edit `config.yaml`, `cm init --verify` | 3 min | `~/.codemender/config.yaml` |
| 5 | Scanning | `cm find ./sample_app` | 2 min | The findings table |
| 6 | Querying reports | `cm report` (table, html, json, filters) | 4 min | `report.html`, the JSON fields |
| 7 | Importing external findings | `cm report import --file` | 2 min | Findings from another scanner in the same list |
| 8 | Triage and verify | `cm verify` | 4 min | `.exploit/` documents and the exploit output |
| 9 | Remediate | `cm fix`, `CONTEXT.md` | 7 min | The diff, "Build and test validation succeeded" |
| | Clean up | `cm clean` | 1 min | |

About 30 minutes live (verify takes about 3 minutes and each fix 5 to 7). Start `cm verify` and `cm fix` early and talk while they run.

---

## 1. Introduction (slide, no commands)
Say:
* CodeMender is Google's AI code-security agent. It **finds** vulnerabilities, **verifies** them by building and running a proof-of-concept exploit in a sandbox, and **fixes** them with a patch that must pass your build.
* The CLI runs on your machine: it reads files, runs builds and tests, and executes the exploit locally. Only targeted code and tool results go to Google's backend, where the Gemini models reason. Source code is not retained and is not used to train models.
* Languages: C/C++, Go, Java, Python, Ruby, Rust, TypeScript. Weakness classes: memory corruption, injection, web security issues, crypto flaws, insecure data handling.
* A person approves every change before it is committed.
* Today's flow: `cm init`, then `cm find`, then `cm report`, then `cm verify`, then `cm fix`.

## 2. Installation and setup
Use a disposable Linux VM or Cloud Shell. You need access to the CodeMender preview (a service account or user that can read the download repository).
```bash
# For Linux (x86_64)
gcloud artifacts generic download \
    --project=cmoc-prod \
    --location=us \
    --repository=codemender-cli-production \
    --package=cm \
    --version=stable \
    --name=cm-linux-amd64.zip \
    --destination=./

unzip cm-*.zip
chmod +x cm
sudo mv cm /usr/local/bin/cm

cm --version
cm --help
```
Show: `cm --version` and the command list from `cm --help`.
How `cm` authenticates to the backend is not shown in the screenshots **(assumed)**: Application Default Credentials (for example `gcloud auth application-default login`) or the VM's service account. Confirm before the session; the first `cm find` is the real connectivity test.

## 3. Sample application setup
```bash
mkdir -p ~/codemender-lab && cd ~/codemender-lab
mkdir -p sample_app
cat << 'EOF' > sample_app/data_service.py
import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey123!@#'

@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

@app.route('/read_file')
def read_file():
    filename = request.args.get('file')
    with open(os.path.join('/var/www/uploads', filename), 'r') as f:
        content = f.read()
    return content

@app.route('/ping')
def ping_host():
    ip = request.args.get('ip')
    cmd = f"ping -c 1 {ip}"
    os.system(cmd)
    return "Ping initiated"

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
EOF

# verification runs the app, so Flask must be installed (otherwise the verifier wastes many steps looking for it)
python3 -m venv .venv && source .venv/bin/activate && pip install flask

# CodeMender uses git to reset the workspace between runs: commit a baseline
printf '.venv/\n__pycache__/\n' > .gitignore
git init && git add -A && git commit -m "baseline"
```
Say: the file contains SQL injection, path traversal, OS command injection, a hard-coded secret, MD5 password hashing and debug mode.
Warn the audience about the reset behaviour: **commit your work before `cm verify` or `cm fix`.**

## 4. Initializing the workspace
```bash
cm init
```
Creates `~/.codemender` (or `$CM_HOME`) with a default `config.yaml`. It can take a minute or two with no output, then prints `Initialized CodeMender workspace at ~/.codemender`.
If you ran `cm init` before, it asks `Overwrite? [y/N]` with no trailing newline, so it looks hung; back up the config first (`cp ~/.codemender/config.yaml ~/.codemender/config.yaml.bak`) or just run `cm init --verify`.

Set git and the build command:
```bash
sed -i 's/^  type: ""/  type: "git"/' ~/.codemender/config.yaml
sed -i 's/^  command: ""/  command: "python3 -m compileall -q ."/' ~/.codemender/config.yaml
```
Resulting config:
```yaml
vcs:
  type: "git"
build:
  command: "python3 -m compileall -q ."
```
Verify the environment:
```bash
cm init --verify
```
Expected: workspace directory, config file, config parsing, server `https://aiplatform.googleapis.com`, a warning that server connectivity is skipped by this client, build command, VCS type `git (reset: git checkout HEAD -- . && git clean -fd)`, state database `~/.codemender/state.db`. Result: 7 passed, 1 warning.

Show **`~/.codemender/config.yaml`** and explain the core settings:

| Setting | Meaning |
|---|---|
| `tools.confirm_commands` (default `true`) | asks `[Y/n]` before the agent runs each terminal command |
| `tools.confirm_writes` (default `true`) | asks `[Y/n]` before the agent writes or edits a file |
| `scan.extensions.include` | file extensions to scan, for example `[".py", ".java", ".go"]` |
| `vcs.type` | `git`, `mercurial` or `custom`; used to reset and diff the workspace |
| `build.command` | run after a fix to confirm the code still builds |

The agent's filesystem sandbox is on by default and limits it to the scan target. It is controlled with `--sandbox`; `--unrestricted` turns it off and is not recommended. Expect 10 or more prompts per `cm verify` unless you pass `-y --bypass-warning` (used below for automation and demos).

## 5. Scanning for vulnerabilities
```bash
cm find ./sample_app
```
Takes about a minute. Output: files discovered, `Starting FIND session (mode: SCAN)`, the server, the scan target, the sandbox roots, tool steps (`list_dir`, `read_file`), then a table with an 8-character ID, severity, CWE type, file and title. In the codelab it found 3 findings:

| ID (yours will differ) | Severity | Type | Title |
|---|---|---|---|
| `49fe487d` | CRITICAL | CWE-89 | SQL Injection in get_user endpoint |
| `80bdddd6` | CRITICAL | CWE-78 | OS Command Injection in ping_host |
| `87ab8566` | HIGH | CWE-22 | Path Traversal / Arbitrary File Read |

Say: results come from an LLM and vary between runs; the quick scan focuses on exploitable injection-style flaws, so the hard-coded `SECRET_KEY` and MD5 hashing may not appear. For an exhaustive file-by-file scan use `cm find --deep` (slower).
Show: the table and the tool-step lines.

## 6. Querying reports and extracting finding IDs
Everything is stored in `~/.codemender/state.db`.
```bash
cm report                                         # terminal table of all findings
cm report --format html                           # writes ~/.codemender/reports/report.html (add --open on a desktop)
cm report --status OPEN --severity HIGH           # filter
cm report --status OPEN --format json             # structured JSON
```
**Show the generated document:** `~/.codemender/reports/report.html`. On Cloud Shell `--open` does nothing, so copy the file out and download or preview it:
```bash
cp ~/.codemender/reports/report.html ~/codemender-lab/ && cloudshell download ~/codemender-lab/report.html
```
`cm report` shows **every** finding in the state database, including old ones. Run `cm clean` first for a fresh start.

JSON structure (one object per finding):
```json
{
  "finding_id": "49fe487d-9911-5030-9c86-99f0aa981eb1",
  "session_id": "ChA4NTUyMDRiNTc1ZmRjY2I3EAgaATAqBG1haW4",
  "title": "SQL Injection in get_user endpoint",
  "file_path": "/home/you/codemender-lab/sample_app/data_service.py",
  "severity": "CRITICAL",
  "confidence": 100,
  "analysis": "- Source: Untrusted user input enters the application via `request.args.get(...`",
  "snippet": "query = f\"SELECT * FROM users WHERE username = '{username}'\"",
  "vuln_type": "CWE-89",
  "vuln_id": "CWE-89",
  "status": "OPEN",
  "start_line": 14,
  "end_line": 15
}
```
The `finding_id` is a full UUID; the 8-character ID in tables is its prefix, and any command that takes a finding ID accepts either. Pick one for the next steps:
```bash
cm report
export FINDING_ID=49fe487d          # replace with an ID from your own report

# or script it (prints null if nothing matched):
export FINDING_ID=$(cm report --format json | jq -r '[.[] | select(.vuln_type=="CWE-89")][0].finding_id')
```

## 7. Importing external findings
CodeMender can verify and fix findings from other scanners. `cm report import` accepts **simple JSON** (`file_path`, `line`, `title`, `message`, `severity`, `vuln_type`) or **SARIF 2.1.0**.
```bash
cat << 'EOF' > external-findings.json
[
  {
    "file_path": "sample_app/data_service.py",
    "line": 23,
    "title": "Path Traversal via Uncanonicalized Upload Path",
    "message": "User-supplied filename is passed to os.path.join without path canonicalization",
    "severity": "CRITICAL",
    "vuln_type": "CWE-22"
  }
]
EOF
cm report import --file ./external-findings.json      # Successfully imported 1 findings.
cm report
export FINDING_ID=e9ab3732          # the ID of the imported finding in your report
```
If the file is in an unsupported format the import fails with `failed to parse file as simple JSON or SARIF` and prints examples of both formats.
Say: this is how an existing SAST tool feeds CodeMender; the imported finding goes through the same verify and fix steps.

## 8. Triaging and verifying findings
```bash
cm verify "$FINDING_ID" -y --bypass-warning
```
`-y` skips the per-command and per-file `[Y/n]` prompts and `--bypass-warning` skips the one-time "agent may modify files or execute commands" warning. Leave them off if you want to approve each step (10 or more prompts).
What happens (about 3 minutes): CodeMender resets the folder to the last commit, writes a reproduction plan and a standalone exploit script to `sample_app/.exploit/`, and runs it. Expected end of output (path traversal example):
```
Programmatically running exploit script to confirm: ~/codemender-lab/sample_app/.exploit/...
Successfully read /etc/passwd via path traversal:
root:x:0:0:root:/root:/bin/bash
...
EXPLOIT SUCCESSFUL

Exploit execution succeeded. Finding VERIFIED (confidence: 100%)
```
Then:
```bash
cm report              # the finding's status is now VERIFIED
ls -la sample_app/.exploit/
```
**Show these generated documents** (all in `sample_app/.exploit/`):

| File | What it is |
|---|---|
| `PLAN.md` | the reproduction plan the agent wrote |
| `LOG.md` | the steps it took |
| `REPORT.md` | the verification result and evidence |
| `exploit.sh` | the standalone exploit script it ran |
| `info.yaml` | metadata about the verification |

```bash
cat sample_app/.exploit/PLAN.md sample_app/.exploit/REPORT.md
```
Warn: the exploit ran on this machine and read its real `/etc/passwd`, which is why this must be a sandbox or VM.

## 9. Remediating vulnerabilities (with project context)
**Step 1: standard auto-remediation** (about 5 minutes)
```bash
cm fix "$FINDING_ID" -y --bypass-warning
```
CodeMender will: reset the folder to your last commit; analyse the vulnerable file and the earlier `.exploit/` artifacts; write a patch; **re-run the exploit to confirm it is now blocked**; run your `build.command`; print the diff and apply it to the working tree. Afterwards `cm report` shows the finding as `FIXED` with `applied`.
```bash
git diff                                              # show the patch
git add -A && git commit -m "Fix path traversal in read_file"
rm -f sample_app/.git                                 # see the warning below
```
**Warning:** `cm fix` creates a snapshot repository for the scan folder (`sample_app/.git`, a symlink into `/tmp`). Every later `cm verify` or `cm fix` resets the folder to that snapshot, which was taken **before** the first fix, so it **silently reverts the earlier fix, even if you committed it**. Removing `sample_app/.git` after each fix makes CodeMender take a fresh snapshot next time.

**Step 2: guide fixes with `CONTEXT.md`** (about 5 to 7 minutes)
By default the fixer does not know your team's helpers or rules. Put them in a file kept outside `sample_app/` and pass its contents with `-c`. The codelab's file lists boundaries, approved helpers and a vulnerability-class table; this version follows the same idea **(assumed wording; the codelab's exact text was only partly visible)**:
```bash
cat << 'EOF' > CONTEXT.md
# Project Context & Architectural Rules (CONTEXT.md)

## 1. Architectural Boundaries & Trust Zones
1. All incoming input must be validated before reaching a file system or database sink.
2. Dynamic shell execution (`os.system`, `subprocess(shell=True)`) is prohibited; use `subprocess.run` with an argument list.

## 2. Approved Helpers & Standard Security Patterns
| Vulnerability Class | Prohibited Pattern | Required Helper / Safe Pattern |
| :--- | :--- | :--- |
| **SQL Injection** | `f"SELECT * FROM users WHERE username = '{username}'"` | Parameterized queries: `cursor.execute("... WHERE username = ?", (username,))` |
| **Path Traversal** | `open(os.path.join(base_dir, filename))` | Canonicalize with `os.path.realpath` and verify the result stays inside `base_dir` |
| **Secrets & Tokens** | Hard-coded `SECRET_KEY` literals | Load from `os.environ["SECRET_KEY"]` |
EOF

cm report --status OPEN
export FINDING_ID=49fe487d          # an SQL injection finding from your report

cm fix -c "$(cat CONTEXT.md)" "$FINDING_ID" -y --bypass-warning
```
Expected: the patch follows the rules, for example
```diff
-    query = f"SELECT * FROM users WHERE username = '{username}'"
-    cursor.execute(query)
+    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```
ending with **Build and test validation succeeded.** once your `build.command` passes.
```bash
git diff
git add -A && git commit -m "Fix SQL injection in get_user"
rm -f sample_app/.git
```
Because scans can report the same issue more than once, other findings for a bug you just fixed may still show as OPEN. Re-run `cm find ./sample_app` to rescan the patched code.
Show: the diff, the build-validation line, and `cm report` with FIXED findings.

## Clean up
```bash
cm clean            # lists what it will remove and asks "Are you sure you want to continue? [y/N]"; -y does not skip this prompt
cd ~ && rm -rf ~/codemender-lab
```
`cm clean` deletes `~/.codemender/state.db` (all findings and patch history), `~/.codemender/reports/`, `~/.codemender/logs/` and the `.cm_project` marker files in scanned folders. It does **not** touch `config.yaml` or your code.

---

## Optional: run it on a repo of your own (Juice Shop)
To show CodeMender on a real project, scan a small folder of a larger repo, for example OWASP Juice Shop's route handlers:
```bash
cd ~/codemender-lab
git clone https://github.com/juice-shop/juice-shop.git --depth 1
cd juice-shop
cm find ./routes --deep            # a folder, not the whole repo: the scan uploads the folder and takes minutes
cm report --severity CRITICAL
cm report --format html
```
Expect SQL injection findings in `routes/login.ts` and `routes/search.ts`, `eval` in `routes/captcha.ts` and `routes/userProfile.ts`, and others; the exact list varies per run.
Do **not** run `cm verify` or `cm fix` live on Juice Shop: verification must run the app, which needs its Node dependencies and a running server, and the build command needs a Node toolchain. Do verify and fix on the sample app above.

**Combining with the scanning agent (optional, untested):** the project's agent can produce SARIF, which `cm report import` accepts.
```bash
cd ~/code-mender
python -c "from pathlib import Path; from codemender_agent.scanner import scan_path; from codemender_agent import reports; Path('juice.sarif').write_text(reports.to_sarif(scan_path(Path('../codemender-lab/juice-shop/routes'))))"
cd ~/codemender-lab/juice-shop && cm report import --file ~/code-mender/juice.sarif
```
Not verified: whether the file paths in this SARIF line up with where `cm` expects them. If the import fails, the error shows the accepted formats. This is a good "better together" story if it works: a fast scanner finds candidates in seconds, CodeMender confirms and fixes them.

## Pre-demo checklist
- [ ] A disposable VM or fresh Cloud Shell, with access to the CodeMender preview confirmed
- [ ] `cm --version` works and `cm init --verify` passes
- [ ] One full rehearsal of steps 3 to 9 on the same machine (note the real IDs and timings)
- [ ] Screenshots or a recording of `cm verify` and `cm fix` as a fallback, since each takes minutes and results vary
- [ ] `report.html`, `.exploit/REPORT.md` and the final `git diff` ready to open
- [ ] A backup: the deployed scan agent (see `demo.md`) answers in seconds if the CLI is slow

## How this relates to the agent
The scanning agent in this repo is a separate, fast, rule-based scanner in the CodeMender style; it does not call `cm` yet. How a future version would run `cm` safely on the agent's behalf is in `flow.md`.
