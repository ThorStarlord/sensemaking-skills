"""Regression tests for issue #56: update_mode_coverage() must merge/union new
run evidence with historical docs/mode-coverage.yaml state instead of
replacing it.

These tests exercise the real OrchestrationRunner.update_mode_coverage() and
OrchestrationRunner.write_run_log() methods against an isolated fixture
repo_root (never the real docs/mode-coverage.yaml), and also run the real
scripts/validate-mode-coverage.py against the resulting file to prove the
fix does not weaken validation.
"""

import os
import shutil
import subprocess
import sys
import importlib.util

import yaml

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Reuse the already-loaded module if another test file loaded it first, so all test
# files share one module object (clobbering sys.modules breaks @patch in sibling files).
if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime",
        os.path.join(scripts_dir, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Scripts that must exist under the fixture repo_root/scripts/ for
# validate-mode-coverage.py (and the validate-run-log.py / analyze-run-failures.py
# it shells out to) to run for real -- these are copied verbatim, never mocked.
_REQUIRED_SCRIPTS = [
    "_validator_utils.py",
    "validate-mode-coverage.py",
    "validate-run-log.py",
    "analyze-run-failures.py",
]


def _setup_fixture_repo(tmp_path):
    """Build a minimal but real repo_root: scripts/ (real validators), artifacts/, docs/."""
    scripts_out = tmp_path / "scripts"
    scripts_out.mkdir()
    for name in _REQUIRED_SCRIPTS:
        shutil.copy(os.path.join(REPO_ROOT, "scripts", name), scripts_out / name)
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "docs").mkdir()
    return tmp_path


def _step(status="COMPLETED", step_id="1", skill="repo-sensemaker"):
    return {
        "step_id": step_id,
        "skill": skill,
        "status": status,
        "gate": "none",
        "output_artifact": "repository_sensemaking_brief",
        "artifact_path": "artifacts/brief.md",
        "validator_stack": [],
    }


def _make_runner(tmp_path, workflow_id, mode="plan_only", session_id=None, step_results=None):
    runner = OrchestrationRunner.__new__(OrchestrationRunner)
    runner.workflow_id = workflow_id
    runner.mode = mode
    runner.session_id = session_id or f"session-{workflow_id}"
    runner.repo_root = str(tmp_path)
    runner.log_dir = str(tmp_path / "artifacts")
    runner.workflow = {
        "id": workflow_id,
        "display_name": workflow_id,
        "steps": [{"skill": "repo-sensemaker"}],
    }
    runner.step_results = step_results if step_results is not None else [_step("COMPLETED")]
    runner.gate_decisions = []
    runner.errors = []
    runner.final_state = "not_started"
    runner.final_note = ""
    runner.use_fixtures = True
    runner.executor = "dry-run"
    return runner


def _run_full_update(runner, monkeypatch):
    """Write a real run log and call the real update_mode_coverage(), bypassing
    the PYTEST_CURRENT_TEST guard (which exists to protect the *real* repo's
    docs/mode-coverage.yaml from ephemeral test writes -- irrelevant here since
    repo_root is an isolated tmp fixture)."""
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    run_log_path = runner.write_run_log()
    runner.update_mode_coverage(run_log_path)
    return run_log_path


def _load_coverage(tmp_path):
    with open(tmp_path / "docs" / "mode-coverage.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _save_coverage(tmp_path, data):
    with open(tmp_path / "docs" / "mode-coverage.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _seed_minimal_coverage(tmp_path):
    _save_coverage(tmp_path, {"mode_coverage": [], "orchestration_runner": {}})


def _inject_historical_families(tmp_path, families):
    """Simulate a coverage file whose top-level ledger already records `families`
    as historically proven (mirroring the real committed state before this fix,
    where mode_coverage: entries can be trimmed independently of the ledger --
    see commit 4ce4667 removing orphaned entries)."""
    coverage = _load_coverage(tmp_path)
    coverage.setdefault("orchestration_runner", {})
    coverage["orchestration_runner"]["workflow_families_proven"] = sorted(families)
    coverage["orchestration_runner"]["total_workflow_families"] = len(families)
    _save_coverage(tmp_path, coverage)


def _run_validate_mode_coverage(tmp_path):
    result = subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "validate-mode-coverage.py"),
         "--repo-root", str(tmp_path)],
        capture_output=True, text=True, timeout=60,
    )
    return result.returncode, (result.stdout + result.stderr)


# ---------------------------------------------------------------------------
# Test 1: 17 historical families survive an update touching only 2
# ---------------------------------------------------------------------------

def test_historical_families_preserved_across_narrow_update(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)

    historical = [f"historical-family-{i:02d}" for i in range(1, 18)]  # 17 families
    _inject_historical_families(tmp_path, historical)

    # Back 2 of those 17 families with real, valid mode_coverage entries + run logs.
    for wf in historical[:2]:
        runner = _make_runner(tmp_path, wf)
        _run_full_update(runner, monkeypatch)

    coverage = _load_coverage(tmp_path)
    proven = set(coverage["orchestration_runner"]["workflow_families_proven"])

    assert set(historical).issubset(proven), (
        f"Historical families lost: {set(historical) - proven}"
    )
    assert coverage["orchestration_runner"]["total_workflow_families"] == len(proven)


# ---------------------------------------------------------------------------
# Test 2: repeated identical update is idempotent (no duplication, no drift)
# ---------------------------------------------------------------------------

def test_repeated_identical_update_is_idempotent(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)

    runner = _make_runner(tmp_path, "idempotent-family", session_id="fixed-session")
    _run_full_update(runner, monkeypatch)
    first_bytes = (tmp_path / "docs" / "mode-coverage.yaml").read_bytes()

    # Apply the exact same update again with a fresh runner carrying identical data.
    runner2 = _make_runner(tmp_path, "idempotent-family", session_id="fixed-session")
    _run_full_update(runner2, monkeypatch)
    second_bytes = (tmp_path / "docs" / "mode-coverage.yaml").read_bytes()

    assert first_bytes == second_bytes, "Second identical update produced drift"

    coverage = _load_coverage(tmp_path)
    matching = [e for e in coverage["mode_coverage"]
                if e.get("workflow_id") == "idempotent-family" and e.get("mode") == "plan_only"]
    assert len(matching) == 1, f"Expected exactly one entry, found {len(matching)}"
    assert coverage["orchestration_runner"]["workflow_families_proven"].count("idempotent-family") == 1


# ---------------------------------------------------------------------------
# Test 3: a genuinely new workflow family is appended exactly once
# ---------------------------------------------------------------------------

def test_new_family_appended_once(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)
    _inject_historical_families(tmp_path, ["existing-family-a", "existing-family-b"])

    runner = _make_runner(tmp_path, "brand-new-family")
    _run_full_update(runner, monkeypatch)

    coverage = _load_coverage(tmp_path)
    proven = coverage["orchestration_runner"]["workflow_families_proven"]
    assert proven.count("brand-new-family") == 1
    assert "existing-family-a" in proven and "existing-family-b" in proven
    assert coverage["orchestration_runner"]["total_workflow_families"] == 3

    entries = [e for e in coverage["mode_coverage"] if e.get("workflow_id") == "brand-new-family"]
    assert len(entries) == 1


# ---------------------------------------------------------------------------
# Test 4: updating one entry's metadata does not corrupt unrelated entries
# ---------------------------------------------------------------------------

def test_unrelated_entries_untouched(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)

    runner_a = _make_runner(tmp_path, "family-a")
    _run_full_update(runner_a, monkeypatch)
    runner_b = _make_runner(tmp_path, "family-b")
    _run_full_update(runner_b, monkeypatch)

    before = _load_coverage(tmp_path)
    entry_b_before = next(e for e in before["mode_coverage"] if e["workflow_id"] == "family-b")

    # Re-run family-a only, with different step content (changed notes/run_log_path).
    runner_a2 = _make_runner(tmp_path, "family-a", session_id="second-session-a")
    _run_full_update(runner_a2, monkeypatch)

    after = _load_coverage(tmp_path)
    entry_b_after = next(e for e in after["mode_coverage"] if e["workflow_id"] == "family-b")
    entry_a_after = next(e for e in after["mode_coverage"] if e["workflow_id"] == "family-a")

    assert entry_b_after == entry_b_before, "Unrelated entry 'family-b' was mutated"
    assert "second-session-a" in entry_a_after["notes"]
    assert len([e for e in after["mode_coverage"] if e["workflow_id"] == "family-a"]) == 1


# ---------------------------------------------------------------------------
# Test 5: a partial/failed run (steps_completed=0) must not wipe history
# ---------------------------------------------------------------------------

def test_partial_failed_run_preserves_history(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)

    historical = [f"historical-family-{i:02d}" for i in range(1, 18)]
    _inject_historical_families(tmp_path, historical)

    # A failed run: steps_completed will be 0 because no step reached COMPLETED.
    failing_runner = _make_runner(
        tmp_path, "failing-family",
        step_results=[_step("FAILED", step_id="1")],
    )
    _run_full_update(failing_runner, monkeypatch)

    coverage = _load_coverage(tmp_path)
    proven = set(coverage["orchestration_runner"]["workflow_families_proven"])

    assert set(historical).issubset(proven), "Failed run wiped historical families"
    assert "failing-family" in proven

    entry = next(e for e in coverage["mode_coverage"] if e["workflow_id"] == "failing-family")
    assert entry["steps_completed"] == 0
    assert entry["steps_total"] == 1


# ---------------------------------------------------------------------------
# Test 6: validate-mode-coverage.py (the real script) stays green
# ---------------------------------------------------------------------------

def test_validator_passes_after_legitimate_update(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)
    _inject_historical_families(tmp_path, ["historical-only-family"])

    runner = _make_runner(tmp_path, "validated-family")
    _run_full_update(runner, monkeypatch)

    code, output = _run_validate_mode_coverage(tmp_path)
    assert code == 0, f"validate-mode-coverage.py failed:\n{output}"


# ---------------------------------------------------------------------------
# Test 7: a missing run-log path must still fail clearly (fix must not
# silently tolerate bad paths introduced by the merge logic)
# ---------------------------------------------------------------------------

def test_missing_run_log_path_still_flagged(tmp_path, monkeypatch):
    _setup_fixture_repo(tmp_path)
    _seed_minimal_coverage(tmp_path)

    runner = _make_runner(tmp_path, "bad-path-family")
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    # Do NOT call write_run_log() -- point at a run log path that will never exist.
    fake_log_path = os.path.join(str(tmp_path), "artifacts", "does_not_exist.md")
    runner.update_mode_coverage(fake_log_path)

    code, output = _run_validate_mode_coverage(tmp_path)
    assert code != 0
    assert "RUN_LOG_NOT_FOUND" in output
