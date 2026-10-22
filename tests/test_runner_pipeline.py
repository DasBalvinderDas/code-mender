"""Runner pipeline against the cm SIMULATOR (tests/fake_cm.py). Proves the orchestration, not the real CLI."""
import subprocess
from pathlib import Path

import pytest

from runner import pipeline

FAKE = str(Path(__file__).parent / "fake_cm.py")


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "src"; (r / "app").mkdir(parents=True)
    (r / "app" / "svc.py").write_text(
        "import os, sqlite3\n\ndef get(name, cur):\n    cur.execute(f\"SELECT * FROM users WHERE name = '{name}'\")\n\n"
        "def ping(ip):\n    os.system('ping ' + ip)\n")
    (r / "README.md").write_text("x")
    for c in (["init", "-q"], ["add", "-A"], ["-c", "user.email=a@b", "-c", "user.name=t", "commit", "-qm", "base"]):
        subprocess.run(["git", *c], cwd=r, check=True)
    return r


@pytest.fixture(autouse=True)
def fake(monkeypatch):
    monkeypatch.setattr(pipeline, "CM_BIN", FAKE)
    monkeypatch.setattr(pipeline, "ALLOW_LOCAL", True)
    monkeypatch.setenv("RUNNER_ALLOW_VERIFY_FIX", "1")  # most tests exercise the full flow; the gate has its own test


def params(repo, **kw):
    return pipeline.validate_request({"repo_url": str(repo), "subdir": "app", **kw})


def test_full_pipeline_find_verify_fix(repo):
    logs = []
    res = pipeline.execute(params(repo, verify_top=2, fix_top=1), logs.append)
    assert res["engine"].startswith("CodeMender CLI") and res["errors"] == []
    st = {f["vuln_type"]: f for f in res["findings"]}
    assert set(st) == {"CWE-89", "CWE-78"}
    assert sorted(f["status"] for f in res["findings"]) == ["FIXED", "VERIFIED"]
    fixed = next(f for f in res["findings"] if f["status"] == "FIXED")
    assert "WHERE name = ?" in fixed["fix"]["diff"] or "# fixed os.system" in fixed["fix"]["diff"]
    assert fixed["fix"]["build_validated"] is True
    assert "EXPLOIT SUCCESSFUL" in fixed["verification"]["report"]
    assert all(f["file"] == "svc.py" for f in res["findings"]) and res["files_scanned"] == 1
    assert any("cm verify" in m for m in logs)


def test_find_only_when_no_verify(repo):
    res = pipeline.execute(params(repo, verify_top=0, fix_top=0))
    assert {f["status"] for f in res["findings"]} == {"OPEN"}


def test_flag_fallback_when_cli_rejects_y(repo, monkeypatch):
    monkeypatch.setenv("FAKE_CM_REJECT_FLAGS", "1")
    assert len(pipeline.execute(params(repo, verify_top=0, fix_top=0))["findings"]) == 2


@pytest.mark.parametrize("bad", [{"repo_url": "file:///etc"}, {"repo_url": "https://evil.com/a/b"},
                                 {"repo_url": "https://github.com/a/b", "subdir": "../x"},
                                 {"repo_url": "https://github.com/a/b", "ref": "x; rm -rf /"}])
def test_rejects_bad_requests(bad):
    with pytest.raises(ValueError):
        pipeline.validate_request(bad)


def test_missing_subdir_fails_cleanly(repo):
    with pytest.raises(pipeline.JobError):
        pipeline.execute(params(repo, subdir="nope"))


def test_verify_and_fix_are_off_unless_the_operator_enables_them(repo, monkeypatch):
    monkeypatch.delenv("RUNNER_ALLOW_VERIFY_FIX")
    p = params(repo, verify_top=2, fix_top=1)
    assert p["verify_top"] == 0 and p["fix_top"] == 0 and p["verify_fix_requested"]
    res = pipeline.execute(p)
    assert {f["status"] for f in res["findings"]} == {"OPEN"} and res["findings"]
    assert any("disabled on this runner" in e for e in res["errors"])


def test_find_only_is_the_default(repo, monkeypatch):
    p = params(repo)
    assert p["verify_top"] == 0 and p["fix_top"] == 0 and not p["verify_fix_requested"]
