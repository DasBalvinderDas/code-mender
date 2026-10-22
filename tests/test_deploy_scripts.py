"""Deploy helpers, plus a dry run of `adk deploy agent_engine` with the API call intercepted (no cloud access)."""
import base64
import json
import os
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "deploy"))

import _common  # noqa: E402
import deploy_agent_engine as dep  # noqa: E402
import query_agent_engine as q  # noqa: E402
import agent_engine_logs as logs  # noqa: E402

ENV = {"CODEMENDER_MODEL": "gemini-2.5-flash", "AGENT_SERVICE_ACCOUNT": "sa@p.iam.gserviceaccount.com"}


def test_build_config():
    c = dep.build_config(ENV)
    assert c["service_account"] == ENV["AGENT_SERVICE_ACCOUNT"] and c["env_vars"] == {"CODEMENDER_MODEL": "gemini-2.5-flash"}
    assert "service_account" not in dep.build_config({})


def test_update_vs_new():
    saved = {"AGENT_ENGINE_RESOURCE": "projects/1/locations/us-central1/reasoningEngines/99"}
    assert dep.pick_update_id(types.SimpleNamespace(new=False), saved) == "99"
    assert dep.pick_update_id(types.SimpleNamespace(new=True), saved) is None
    assert dep.pick_update_id(types.SimpleNamespace(new=False), {"AGENT_ENGINE_RESOURCE": "junk"}) is None


def test_deploy_command():
    cmd = dep.deploy_command("p", "us-central1", "/tmp/c.json", "99")
    assert cmd[:3] == ["adk", "deploy", "agent_engine"] and "--agent_engine_id=99" in cmd and cmd[-1].endswith("codemender_agent")
    assert "--staging_bucket" not in " ".join(cmd)


def test_write_env_keeps_other_lines(tmp_path):
    p = tmp_path / ".env"; p.write_text("A=1\n# c\nB=2\n")
    _common.write_env({"B": "3", "C": "4"}, p)
    assert _common.read_env(p) == {"A": "1", "B": "3", "C": "4"} and "# c" in p.read_text()


def test_parse_event_and_save_attachments(tmp_path):
    pdf = b"%PDF-1.4 test"
    event = {"content": {"role": "model", "parts": [{"text": "hello"},
             {"inlineData": {"mimeType": "application/pdf", "data": base64.b64encode(pdf).decode(), "displayName": "../x/Report.pdf"}}]}}
    texts, files = q.parse_event(event)
    assert texts == ["hello"] and files == [("Report.pdf", pdf)]  # path parts stripped
    assert q.save_files(files, tmp_path)[0].read_bytes() == pdf
    assert q.parse_event({"content": {"role": "user", "parts": [{"text": "x"}]}}) == ([], [])


def test_log_filter_and_key_lines():
    f = logs.build_filter("projects/1/locations/us-central1/reasoningEngines/99", errors_only=True)
    assert 'reasoning_engine_id="99"' in f and "severity>=ERROR" in f
    assert "ModuleNotFoundError" in logs.key_lines(["starting", "ModuleNotFoundError: No module named 'x'", "ok"])


def test_explain_failed_start():
    assert "agent_engine_logs.py" in _common.explain("The Reasoning Engine failed to deploy and cannot serve traffic.", "p")


def test_adk_deploy_dry_run_uses_config_file_and_ships_no_env(tmp_path, monkeypatch):
    agentplatform = pytest.importorskip("google.adk.dependencies._agentplatform").agentplatform
    from click.testing import CliRunner
    from google.adk.cli.cli_tools_click import main
    captured = {}

    class Runtimes:
        def create(self):
            return types.SimpleNamespace(api_resource=types.SimpleNamespace(name="projects/p/locations/us-central1/reasoningEngines/1"))

        def update(self, name, config):
            captured["config"] = config
            captured["dockerfile"] = Path("Dockerfile").read_text()
            captured["files"] = sorted(os.listdir("agents/codemender_agent"))

        def delete(self, name):
            pass

    class FakeClient:
        def __init__(self, **kw):
            self.runtimes = Runtimes()

    monkeypatch.setattr(agentplatform, "Client", FakeClient)
    cfg = tmp_path / "c.json"; cfg.write_text(json.dumps(dep.build_config(ENV)))
    monkeypatch.chdir(ROOT)
    res = CliRunner().invoke(main, ["deploy", "agent_engine", "--project=p", "--region=us-central1",
                                    f"--agent_engine_config_file={cfg}", str(ROOT / "codemender_agent")])
    assert res.exit_code == 0, res.output
    c = captured["config"]
    assert c["service_account"] == ENV["AGENT_SERVICE_ACCOUNT"] and c["env_vars"]["CODEMENDER_MODEL"] == "gemini-2.5-flash"
    assert "agents/codemender_agent" in c["source_packages"] and "image_spec" in c   # inline source + Dockerfile, no bucket
    assert ".env" not in captured["files"] and "requirements.txt" in captured["files"]
    assert "adk\", \"api_server" in captured["dockerfile"].replace("'", '"') or "api_server" in captured["dockerfile"]
