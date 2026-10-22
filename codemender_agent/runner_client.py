"""Client for the CodeMender runner service (Cloud Run, IAM-protected). Auth: an ID token for the runner URL."""
from __future__ import annotations

import asyncio
import os

import httpx


_TRANSPORT = None  # tests inject an ASGI transport


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=60, transport=_TRANSPORT)


def runner_url() -> str:
    return os.environ.get("CODEMENDER_RUNNER_URL", "").rstrip("/")


def _token(url: str) -> str:
    if os.environ.get("CODEMENDER_RUNNER_TOKEN"):  # local testing only
        return os.environ["CODEMENDER_RUNNER_TOKEN"]
    import google.auth.transport.requests
    import google.oauth2.id_token
    return google.oauth2.id_token.fetch_id_token(google.auth.transport.requests.Request(), url)


async def _headers(url: str) -> dict:
    if url.startswith("http://localhost") or url.startswith("http://127."):
        return {}
    return {"Authorization": f"Bearer {await asyncio.to_thread(_token, url)}"}


async def start(params: dict) -> dict:
    url = runner_url()
    if not url:
        raise RuntimeError("CODEMENDER_RUNNER_URL is not configured")
    async with _client() as c:
        r = await c.post(f"{url}/v1/analyses", json=params, headers=await _headers(url))
    if r.status_code >= 400:
        raise RuntimeError(f"runner rejected the request ({r.status_code}): {r.text[:300]}")
    return r.json()


async def get(run_id: str) -> dict:
    url = runner_url()
    async with _client() as c:
        r = await c.get(f"{url}/v1/analyses/{run_id}", headers=await _headers(url))
    if r.status_code >= 400:
        raise RuntimeError(f"runner error ({r.status_code}): {r.text[:300]}")
    return r.json()
