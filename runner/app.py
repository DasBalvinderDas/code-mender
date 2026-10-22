"""HTTP API around runner.pipeline. Deploy on Cloud Run with IAM auth (no public access)."""
from __future__ import annotations

import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException

from . import pipeline

MAX_JOBS = int(__import__("os").environ.get("RUNNER_MAX_JOBS", 2))
KEEP_SECONDS = 3600
app = FastAPI(title="CodeMender runner")
_pool = ThreadPoolExecutor(max_workers=MAX_JOBS)
_jobs: dict[str, dict] = {}
_lock = threading.Lock()


def _gc():
    cutoff = time.time() - KEEP_SECONDS
    for k in [k for k, j in _jobs.items() if j["finished"] and j["finished"] < cutoff]:
        _jobs.pop(k, None)


def _work(job_id: str, params: dict):
    job = _jobs[job_id]

    def log(msg):
        job["progress"].append({"t": round(time.time() - job["started"]), "msg": msg})
        job["stage"] = msg

    try:
        job["status"] = "running"
        job["result"] = pipeline.execute(params, log)
        job["status"] = "completed"
    except Exception as exc:  # reported to the caller, never raised into the pool
        job["status"], job["error"] = "failed", str(exc)[:600]
    finally:
        job["finished"] = time.time()


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/v1/analyses", status_code=202)
def start(body: dict):
    try:
        params = pipeline.validate_request(body)
    except (ValueError, TypeError) as exc:
        raise HTTPException(400, str(exc))
    with _lock:
        _gc()
        if sum(1 for j in _jobs.values() if j["status"] in ("queued", "running")) >= MAX_JOBS * 2:
            raise HTTPException(429, "runner is busy; try again later")
        job_id = uuid.uuid4().hex[:12]
        _jobs[job_id] = {"id": job_id, "status": "queued", "stage": "queued", "progress": [], "started": time.time(),
                         "finished": None, "result": None, "error": None, "params": {k: params[k] for k in ("repo_url", "ref", "subdir")}}
    _pool.submit(_work, job_id, params)
    return {"id": job_id, "status": "queued"}


@app.get("/v1/analyses/{job_id}")
def status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(404, "unknown analysis id (the runner keeps results for 1 hour and in memory)")
    return {k: job[k] for k in ("id", "status", "stage", "progress", "error", "params", "result")}
