#!/usr/bin/env python3
"""Talk to the deployed agent from the shell and save the report files it attaches.

  python deploy/query_agent_engine.py "Analyse https://github.com/juice-shop/juice-shop"
  python deploy/query_agent_engine.py                # interactive chat (type exit to quit)

Attachments (the PDF and Markdown report) are written to ./reports_out/. Needs AGENT_ENGINE_RESOURCE in .env or --resource.
"""
import argparse
import asyncio
import base64
import sys
import uuid
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, resolve_project, resource_from_env  # noqa: E402


def _get(d, *names, default=None):
    """Read a key that may be snake_case or camelCase."""
    for n in names:
        if isinstance(d, dict) and d.get(n) is not None:
            return d[n]
    return default


def parse_event(event: dict):
    """Returns (texts, attachments) from one streamed event; attachments are (filename, bytes)."""
    texts, files = [], []
    content = _get(event, "content", default={}) or {}
    for part in _get(content, "parts", default=[]) or []:
        if _get(part, "text") and _get(content, "role", default="model") != "user":
            texts.append(part["text"])
        blob = _get(part, "inline_data", "inlineData")
        if blob and _get(blob, "data"):
            data = blob["data"]
            raw = base64.b64decode(data) if isinstance(data, str) else bytes(data)
            name = _get(blob, "display_name", "displayName") or f"attachment-{uuid.uuid4().hex[:6]}"
            files.append((Path(name).name, raw))
    return texts, files


def save_files(files, out_dir: Path) -> list:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for name, raw in files:
        path = out_dir / name
        path.write_bytes(raw)
        saved.append(path)
    return saved


async def converse(remote, user_id, session_id, message, out_dir: Path):
    async for event in remote.async_stream_query(user_id=user_id, session_id=session_id, message=message):
        texts, files = parse_event(event)
        for t in texts:
            print(t)
        for path in save_files(files, out_dir):
            print(f"\n[saved attachment: {path} ({path.stat().st_size:,} bytes)]")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("message", nargs="?")
    ap.add_argument("--resource")
    ap.add_argument("--project")
    ap.add_argument("--out", default=str(ROOT / "reports_out"))
    a = ap.parse_args()
    resource = resource_from_env(a.resource)
    if not resource:
        sys.exit("No engine known. Deploy first, or pass --resource projects/<p>/locations/<region>/reasoningEngines/<id>")
    warnings.filterwarnings("ignore", category=FutureWarning)
    try:
        import agentplatform as sdk
        sdk.Client
    except (ImportError, AttributeError):
        import vertexai as sdk
    remote = sdk.Client(project=resolve_project(a.project), location=resource.split("/")[3]).agent_engines.get(name=resource)

    async def go():
        user_id = f"demo-{uuid.uuid4().hex[:6]}"
        session = await remote.async_create_session(user_id=user_id)
        sid = _get(session, "id")
        print(f"Session {sid} on {resource}\n")
        if a.message:
            return await converse(remote, user_id, sid, a.message, Path(a.out))
        while True:
            try:
                text = input("\nyou> ").strip()
            except EOFError:
                return
            if text.lower() in ("", "exit", "quit"):
                return
            await converse(remote, user_id, sid, text, Path(a.out))

    asyncio.run(go())


if __name__ == "__main__":
    main()
