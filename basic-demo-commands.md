# Basic demo commands

Each step: the command, and why we run it. Details and expected output are in [`cli-demo.md`](cli-demo.md).
Run this on a throwaway machine (a fresh Cloud Shell is fine), not inside the `code-mender` folder.

## Part 1: CodeMender CLI

**1. Download and install the CLI**
```bash
gcloud artifacts generic download --project=cmoc-prod --location=us --repository=codemender-cli-production \
  --package=cm --version=stable --name=cm-linux-amd64.zip --destination=./
unzip cm-*.zip && chmod +x cm && sudo mv cm /usr/local/bin/cm
```
Why: gets the `cm` tool onto the machine.

**2. Check it works**
```bash
cm --version
```
Why: confirms the install.

**3. Create the sample app** (copy the file contents from `cli-demo.md`, section 3)
```bash
mkdir -p ~/codemender-lab/sample_app && cd ~/codemender-lab
# create sample_app/data_service.py (deliberately vulnerable code)
```
Why: gives us code with known security problems to scan.

**4. Install the app's dependency**
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install flask
```
Why: the verify step runs the app, so Flask must be installed.

**5. Commit a starting point with git**
```bash
printf '.venv/\n__pycache__/\n' > .gitignore
git init && git add -A && git commit -m "baseline"
```
Why: CodeMender uses git to reset the folder between runs. Always commit first, or uncommitted files can be deleted.

**6. Set up CodeMender**
```bash
cm init
sed -i 's/^  type: ""/  type: "git"/' ~/.codemender/config.yaml
sed -i 's/^  command: ""/  command: "python3 -m compileall -q ."/' ~/.codemender/config.yaml
```
Why: creates its workspace, and tells it we use git and how to check the code still builds after a fix.

**7. Check the setup**
```bash
cm init --verify
```
Why: shows everything is configured correctly.

**8. Scan for vulnerabilities**
```bash
cm find ./sample_app
```
Why: CodeMender reads the code and lists the problems it finds (takes about a minute).

**9. See the results**
```bash
cm report
cm report --format html
```
Why: shows the findings as a table, and writes an HTML report to `~/.codemender/reports/report.html` to open or download.

**10. Pick a finding**
```bash
export FINDING_ID=<an ID from the table>
```
Why: the next commands need to know which finding to work on.

**11. (Optional) Add a finding from another scanner**
```bash
cm report import --file ./external-findings.json
```
Why: shows CodeMender can verify and fix findings that other tools reported (file contents in `cli-demo.md`, section 7).

**12. Prove the problem is real**
```bash
cm verify "$FINDING_ID" -y --bypass-warning
cat sample_app/.exploit/REPORT.md
```
Why: CodeMender writes and runs a test exploit to confirm the finding is exploitable (about 3 minutes). The `.exploit/` folder holds the documents it generated. This runs on this machine, so use a throwaway one.

**13. Fix it**
```bash
cm fix "$FINDING_ID" -y --bypass-warning
git diff
```
Why: CodeMender writes a patch, re-runs the exploit to confirm it is blocked, runs the build, and applies the change (about 5 minutes). `git diff` shows exactly what changed.

**14. Save the fix and clear CodeMender's snapshot**
```bash
git add -A && git commit -m "Fix applied"
rm -f sample_app/.git
```
Why: keeps the fix, and stops the next run from undoing it.

**15. (Optional) Fix with our own rules**
```bash
cm fix -c "$(cat CONTEXT.md)" "$FINDING_ID" -y --bypass-warning
```
Why: tells CodeMender our team's coding rules so the patch follows them (file contents in `cli-demo.md`, section 9).

**16. Clean up**
```bash
cm clean
cd ~ && rm -rf ~/codemender-lab
```
Why: removes CodeMender's saved findings and the demo folder.

## Part 2: Our deployed agent (the quick scanner)

**1. Start a chat with the agent**
```bash
python deploy/query_agent_engine.py
```
Why: opens a chat with the deployed agent. It remembers the last scan only within one chat, so do both questions below in the same chat.

**2. Ask it to scan a repo** (type this in the chat)
```
Analyse https://github.com/juice-shop/juice-shop for security vulnerabilities.
```
Why: the agent scans the repo and gives a summary. The PDF and Markdown report are saved in `reports_out/`.

**3. Ask a follow-up** (same chat)
```
Show only the findings under routes/ and lib/.
```
Why: shows the agent answering from the scan results. Type `exit` to leave the chat.
