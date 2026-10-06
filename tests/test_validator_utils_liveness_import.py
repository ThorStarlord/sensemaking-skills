"""Regression tests for lazy ``workflow_liveness`` resolution in
``scripts/_validator_utils.py`` (campaign R7 / defect D12).

``_validator_utils`` used to execute ``import workflow_liveness`` at module
import time. That only works when ``scripts/`` is on ``sys.path`` (direct
script execution). Loading the module any other way -- as the
``scripts._validator_utils`` package path from the repository root, or from a
copied file, as ``tests/test_mode_coverage_aggregation.py`` does -- failed
with ``ModuleNotFoundError: No module named 'workflow_liveness'``.

Every test here runs a fresh interpreter: ``sys.modules`` / ``sys.path`` state
left behind by sibling test modules (several insert ``scripts/`` into
``sys.path``) would otherwise mask the behavior under test. Child output is
ASCII JSON so the tests behave identically under cp1252 and UTF-8 consoles.
"""

import json
import os
import shutil
import subprocess
import sys

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
REFERENCES_DIR = os.path.join(REPO_ROOT, "skills", "workflow-planner", "references")
OVERLAY_PATH = os.path.join(REFERENCES_DIR, "workflow-liveness.yaml")
REGISTRY_PATH = os.path.join(REFERENCES_DIR, "workflow-registry.yaml")

# Child prologue. argv[1] is always the real scripts/ directory: remove it (and
# a cwd entry that resolves to it) from sys.path so the only way to reach
# workflow_liveness is the resolution path under test.
_CHILD_PROLOGUE = """
import importlib.util, json, os, sys
_scripts = os.path.normcase(os.path.abspath(sys.argv[1]))
sys.path[:] = [
    p for p in sys.path
    if os.path.normcase(os.path.abspath(p or os.getcwd())) != _scripts
]
assert importlib.util.find_spec("workflow_liveness") is None, sys.path
"""

# (a) package-path import with only the repository root on sys.path.
_CHILD_PACKAGE_IMPORT = _CHILD_PROLOGUE + """
repo_root = sys.argv[2]
sys.path.insert(0, repo_root)
import scripts._validator_utils as vu
print(json.dumps({
    "overlay": vu.load_workflow_liveness(repo_root),
    "format_error": vu.format_error("CODE", "message"),
}, sort_keys=True))
"""

# (b) a copy of _validator_utils.py with no workflow_liveness.py beside it.
_CHILD_COPY_WITHOUT_SIBLING = _CHILD_PROLOGUE + """
copy_path, repo_root = sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("_validator_utils_copy", copy_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
try:
    mod.load_workflow_liveness(repo_root)
except ImportError as exc:
    error = str(exc)
else:
    error = None
print(json.dumps({
    "format_error": mod.format_error("CODE", "message"),
    "error": error,
}, sort_keys=True))
"""

# (c) a copy of _validator_utils.py with workflow_liveness.py beside it.
_CHILD_COPY_WITH_SIBLING = _CHILD_PROLOGUE + """
copy_path, repo_root = sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("_validator_utils_copy", copy_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
overlay = mod.load_workflow_liveness(repo_root)
catalog = mod.load_workflow_catalog(repo_root)
operational = mod.load_workflow_registry(repo_root)
print(json.dumps({
    "overlay": overlay,
    "resolved_file": os.path.normcase(os.path.abspath(mod._workflow_liveness().__file__)),
    "catalog_ids": sorted(w["id"] for w in catalog["workflows"]),
    "operational_ids": sorted(w["id"] for w in operational["workflows"]),
    "top_level_imported": "workflow_liveness" in sys.modules,
}, sort_keys=True))
"""


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _run_child(code, *args, cwd):
    result = subprocess.run(
        [sys.executable, "-c", code, SCRIPTS_DIR, *args],
        capture_output=True, text=True, encoding="utf-8", cwd=str(cwd), timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


def _copy_validator_utils(tmp_path, with_sibling):
    copy_dir = tmp_path / "scripts_copy"
    copy_dir.mkdir()
    shutil.copy(os.path.join(SCRIPTS_DIR, "_validator_utils.py"), copy_dir / "_validator_utils.py")
    if with_sibling:
        shutil.copy(os.path.join(SCRIPTS_DIR, "workflow_liveness.py"), copy_dir / "workflow_liveness.py")
    return copy_dir


def test_package_import_from_repo_root_resolves_liveness(tmp_path):
    out = _run_child(_CHILD_PACKAGE_IMPORT, REPO_ROOT, cwd=tmp_path)
    assert out["format_error"] == "CODE: message"
    assert out["overlay"] == _load_yaml(OVERLAY_PATH)


def test_copy_without_sibling_imports_and_fails_only_on_liveness_call(tmp_path):
    copy_dir = _copy_validator_utils(tmp_path, with_sibling=False)
    out = _run_child(
        _CHILD_COPY_WITHOUT_SIBLING, str(copy_dir / "_validator_utils.py"), REPO_ROOT, cwd=tmp_path,
    )
    assert out["format_error"] == "CODE: message"
    assert out["error"] is not None, "load_workflow_liveness must raise ImportError"
    assert "workflow_liveness" in out["error"]


def test_copy_with_sibling_resolves_liveness_from_sibling_file(tmp_path):
    copy_dir = _copy_validator_utils(tmp_path, with_sibling=True)
    out = _run_child(
        _CHILD_COPY_WITH_SIBLING, str(copy_dir / "_validator_utils.py"), REPO_ROOT, cwd=tmp_path,
    )
    expected_sibling = os.path.normcase(os.path.abspath(str(copy_dir / "workflow_liveness.py")))
    assert out["resolved_file"] == expected_sibling
    assert out["top_level_imported"] is False

    overlay = _load_yaml(OVERLAY_PATH)
    assert out["overlay"] == overlay

    # ADR 0027 fail-closed behavior is preserved through the sibling path: the
    # operational view contains exactly the active workflows of the catalog.
    registry_ids = sorted(w["id"] for w in _load_yaml(REGISTRY_PATH)["workflows"])
    assert out["catalog_ids"] == registry_ids
    compat_only = {wid for wid, v in overlay["overrides"].items() if v == "compatibility_only"}
    assert compat_only, "overlay fixture must declare at least one compatibility_only workflow"
    assert out["operational_ids"] == [wid for wid in registry_ids if wid not in compat_only]
