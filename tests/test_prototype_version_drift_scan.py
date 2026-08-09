"""
Tests for scripts/prototype_version_drift_scan.py.

PROTOTYPE (prototype/repo-sensemaker-vnext). Operationalizes S1's own
"README 0.2.1 vs pyproject 0.2.2" finding as a reusable check.
"""

import importlib.util
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "prototype_version_drift_scan",
    os.path.join(SCRIPTS_DIR, "prototype_version_drift_scan.py"),
)
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def test_detects_drift_between_readme_and_pyproject(tmp_path):
    _write(str(tmp_path / "pyproject.toml"), '[project]\nname = "x"\nversion = "0.2.2"\n')
    _write(str(tmp_path / "README.md"), "Expected version: `0.2.1`\n")

    result = scan.detect_readme_pyproject_version_drift(str(tmp_path))

    assert result["pyproject_version"] == "0.2.2"
    assert (1, "0.2.1") in result["readme_mentions"]
    assert (1, "0.2.1") in result["drifted_mentions"]


def test_no_drift_when_versions_match(tmp_path):
    _write(str(tmp_path / "pyproject.toml"), '[project]\nversion = "1.0.0"\n')
    _write(str(tmp_path / "README.md"), "Current release: 1.0.0\n")

    result = scan.detect_readme_pyproject_version_drift(str(tmp_path))

    assert result["drifted_mentions"] == []


def test_missing_pyproject_produces_no_drift_claim(tmp_path):
    """No canonical version to compare against -- must not fabricate drift."""
    _write(str(tmp_path / "README.md"), "See version 2.3.4 for details.\n")

    result = scan.detect_readme_pyproject_version_drift(str(tmp_path))

    assert result["pyproject_version"] is None
    assert result["drifted_mentions"] == []


def test_missing_readme_produces_no_mentions(tmp_path):
    _write(str(tmp_path / "pyproject.toml"), 'version = "1.0.0"\n')

    result = scan.detect_readme_pyproject_version_drift(str(tmp_path))

    assert result["readme_mentions"] == []
    assert result["drifted_mentions"] == []


def test_against_real_repo_finds_the_known_s1_drift():
    """Sanity check against the actual repository: reproduces S1's own
    finding (owner-synthesis-v1.md section 6: 'README 0.2.1 vs pyproject
    0.2.2 version drift') -- confirmed still present via direct grep before
    building this tool."""
    result = scan.detect_readme_pyproject_version_drift(REPO_ROOT)

    assert result["pyproject_version"] == "0.2.2"
    assert any(v == "0.2.1" for _ln, v in result["drifted_mentions"])


def test_main_returns_nonzero_on_drift(tmp_path, capsys):
    _write(str(tmp_path / "pyproject.toml"), 'version = "2.0.0"\n')
    _write(str(tmp_path / "README.md"), "version 1.9.9\n")

    code = scan.main(["--repo-root", str(tmp_path)])
    out = capsys.readouterr().out

    assert code == 1
    assert "DRIFT" in out
