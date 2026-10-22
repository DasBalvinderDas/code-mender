#!/usr/bin/env python3
"""TEST SIMULATOR of the CodeMender CLI, modelled on the codelab (init / find / report --format json / verify / fix).
It is not CodeMender: it only reproduces the documented command shapes, output fields and side effects
(CM_HOME/state.db-like store, .exploit/ files, workspace reset, working-tree patch) so the runner can be tested offline."""
import json, os, re, subprocess, sys, uuid
from pathlib import Path

HOME = Path(os.environ.get("CM_HOME", Path.home() / ".codemender"))
STATE = HOME / "state.json"


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else []


def save(x):
    STATE.write_text(json.dumps(x))


def main(a):
    cmd, rest = a[0], a[1:]
    if cmd == "init":
        if (HOME / "config.yaml").exists():
            sys.stdout.write("Overwrite? [y/N] "); return 0
        HOME.mkdir(parents=True, exist_ok=True)
        (HOME / "config.yaml").write_text('vcs:\n  type: ""\nbuild:\n  command: ""\ntools:\n  confirm_commands: true\n  confirm_writes: true\n')
        STATE.write_text("[]"); print("Initialized CodeMender workspace at", HOME); return 0
    if cmd == "find":
        target = Path([x for x in rest if not x.startswith("-")][0]).resolve()
        if os.environ.get("FAKE_CM_REJECT_FLAGS") and "-y" in rest:
            print("unknown shorthand flag: 'y' in -y", file=sys.stderr); return 2
        st = load()
        for p in target.rglob("*.py"):
            for i, line in enumerate(p.read_text().splitlines(), 1):
                if re.search(r"execute\(.*(f[\"']|\+)", line) or "os.system(" in line:
                    sql = "execute" in line
                    st.append({"finding_id": str(uuid.uuid4()), "session_id": "s1", "title": "SQL Injection" if sql else "OS Command Injection",
                               "file_path": str(p), "severity": "CRITICAL", "confidence": 100, "analysis": "- Source: untrusted input reaches a sink.",
                               "snippet": line.strip(), "vuln_type": "CWE-89" if sql else "CWE-78", "vuln_id": "CWE-89" if sql else "CWE-78",
                               "status": "OPEN", "start_line": i, "end_line": i})
        save(st); print(f"Found {len(st)} vulnerabilities"); return 0
    if cmd == "report":
        print("some banner line [not json]")
        print(json.dumps(load(), indent=2)); return 0
    ids = [x for x in rest if not x.startswith("-")]
    fid = ids[-1]
    st = load()
    f = next((x for x in st if x["finding_id"].startswith(fid)), None)
    if not f:
        print("finding not found", file=sys.stderr); return 1
    scan = Path(f["file_path"]).parent
    subprocess.run("git checkout HEAD -- . && git clean -fd -q -e .exploit", shell=True, cwd=scan)
    if cmd == "verify":
        ex = scan / ".exploit"; ex.mkdir(exist_ok=True)
        (ex / "PLAN.md").write_text("# Plan\nSend a quote-breaking value to the endpoint.\n")
        (ex / "REPORT.md").write_text("# Report\nEXPLOIT SUCCESSFUL: query structure changed.\n")
        f["status"] = "VERIFIED"; save(st); print("EXPLOIT SUCCESSFUL\nFinding VERIFIED (confidence: 100%)"); return 0
    if cmd == "fix":
        p = Path(f["file_path"]); src = p.read_text()
        p.write_text(src.replace("f\"SELECT * FROM users WHERE name = '{name}'\"", "\"SELECT * FROM users WHERE name = ?\"").replace("os.system(", "# fixed os.system("))
        f["status"] = "FIXED"; save(st)
        print("Build and test validation succeeded."); return 0
    return 1


sys.exit(main(sys.argv[1:]))
