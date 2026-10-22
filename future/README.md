# Parked for later (not part of the simple agent)

Built earlier, tested only against a simulator, and set aside so the simple scan agent can be proven first.

| What | Where |
|---|---|
| Real Google CodeMender CLI (`cm find/verify/fix/report`) run in a sandboxed Cloud Run service | `runner/`, `codemender_agent/cm_tools.py`, `codemender_agent/runner_client.py`, `deploy/deploy_runner.sh`, `deploy/cloudbuild-runner.yaml` |
| A2A server / Agent Engine A2A packaging and the defect-fix `RemoteA2aAgent` example | `codemender_agent/a2a_app.py`, `codemender_agent/agent_engine_app.py`, `deploy/defect_fix_client_example.py` |
| Tests using `tests/fake_cm.py`, a simulator of the `cm` CLI | `tests/` |
| Earlier demo prompts and test plan covering those parts | `DEMO_PROMPTS_old.md`, `TEST_PLAN_old.md` |

To bring them back: move the files to the paths in the table (drop the `future/` prefix), add `run_codemender` and `check_codemender_run` to the agent's tools in `codemender_agent/agent.py`, and re-add `a2a-sdk[http-server]==1.2.3`, `sse-starlette==3.5.0` and `uvicorn==0.54.0` to `requirements.txt` for A2A. Commit `68384dc` has the last working layout.
