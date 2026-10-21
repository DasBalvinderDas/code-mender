from pathlib import Path

import pytest

from codemender_agent import reports
from codemender_agent.scanner import scan_path

DEMO = Path(__file__).resolve().parent.parent / "demo" / "vulnerable-app"


@pytest.fixture(scope="module")
def res():
    return scan_path(DEMO)


def test_detects_core_classes(res):
    cwes = {f.cwe for f in res.findings}
    assert {"CWE-89", "CWE-78", "CWE-79", "CWE-798", "CWE-502", "CWE-120", "CWE-327", "CWE-250"} <= cwes


def test_sorted_by_severity_and_scored(res):
    assert res.findings[0].severity == "CRITICAL"
    assert 0 < res.risk_score <= 100


def test_patches_are_unified_diffs(res):
    patched = [f for f in res.findings if f.patch]
    assert patched and all(f.patch.startswith("--- a/") for f in patched)


def test_clean_code_has_no_findings(tmp_path):
    (tmp_path / "ok.py").write_text('import hashlib\nx = hashlib.sha256(b"a")\ncur.execute("SELECT 1 WHERE a=?", (a,))\n')
    assert scan_path(tmp_path).findings == []


def test_all_report_formats(res, tmp_path):
    import json
    paths = reports.write_all(res, tmp_path)
    assert set(paths) == set(reports.FORMATS)
    assert json.loads(Path(paths["sarif"]).read_text())["version"] == "2.1.0"
    assert "CodeMender Security Report" in Path(paths["html"]).read_text()
    assert json.loads(Path(paths["json"]).read_text())["summary"]["total_findings"] == len(res.findings)


def test_rejects_bad_repo_url():
    from codemender_agent.scanner import clone_repo
    with pytest.raises(ValueError):
        clone_repo("file:///etc/passwd")
