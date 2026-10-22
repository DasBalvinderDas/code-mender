# Parked for later

The real CodeMender integration (the runner and the agent's tools for it) is now part of the main code: see `runner/`, `codemender_agent/cm_tools.py`,
`codemender_agent/runner_client.py` and `deploy/deploy_runner.sh`.

What is still parked here:

| What | Where |
|---|---|
| A2A server / Agent Engine A2A packaging | `codemender_agent/a2a_app.py`, `codemender_agent/agent_engine_app.py` |
| The defect-fix agent's `RemoteA2aAgent` example | `deploy/defect_fix_client_example.py` |
| Earlier demo prompts and test plan (older wording) | `DEMO_PROMPTS_old.md`, `TEST_PLAN_old.md` |

To bring A2A back: move the files to the paths in the table (drop the `future/` prefix) and add `a2a-sdk[http-server]==1.2.3`, `sse-starlette==3.5.0` and `uvicorn==0.54.0` to the requirements.
Note that ADK's own deployment already starts the agent with `--a2a`, so you may not need the separate server.
