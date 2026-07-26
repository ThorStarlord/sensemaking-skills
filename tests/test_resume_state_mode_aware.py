"""Regression tests for mode-aware resume-state parsing.

Root cause: `_find_resume_state()` in scripts/workflow-runtime.py only ever
treated a logged step as resumable when its status was literally
"COMPLETED". But a genuine `guided_execution` run records a successfully
approved step's status as "APPROVED" (MODE_CEILINGS["guided_execution"] ==
"APPROVED"), because that is the mode's real terminal success status.
"COMPLETED" only ever appears in already-resumed synthetic step
reconstructions, never in a genuine first-time guided_execution run log.

This meant a real, unmodified guided_execution run log (e.g. the one
produced by PR #59's live evidence run) could never be resumed without
hand-editing its status -- which is exactly the blocker these tests pin.

These tests exercise the REAL `_find_resume_state()` method (and, for the
step-selection test, the REAL `run()` step loop) rather than a
reimplemented/duplicated helper.
"""

import importlib.util
import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
REAL_PR59_RUN_LOG = (
    REPO_ROOT
    / "experiments"
    / "evidence"
    / "0006-semantic-authorities-live-step1"
    / "final-run-e787fc41"
    / "run_log_architectural-review-planning-workflow_guided_execution.md"
)


@pytest.fixture(scope="module")
def wfrt():
    """Load scripts/workflow-runtime.py as a module (real production code)."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    importlib.invalidate_caches()
    spec = importlib.util.spec_from_file_location(
        "wfrt_resume_mode_aware", str(SCRIPTS_DIR / "workflow-runtime.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def tmp_log_dir():
    """A tempdir on the same drive as the repo (see test_preflight_ordering.py)."""
    d = tempfile.mkdtemp(prefix="resume-mode-aware-", dir=str(REPO_ROOT.parent))
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _make_bare_runner(wfrt, mode, log_dir, workflow_id="test-workflow"):
    """Construct an OrchestrationRunner without running __init__'s heavy
    machinery (registry loading, executor creation, etc.) -- only the
    attributes _find_resume_state() actually reads are needed:
    self.log_dir, self.workflow_id, self.mode.
    """
    runner = object.__new__(wfrt.OrchestrationRunner)
    runner.log_dir = str(log_dir)
    runner.workflow_id = workflow_id
    runner.mode = mode
    return runner


def _write_run_log(log_dir, workflow_id, mode, body):
    path = os.path.join(str(log_dir), f"run_log_{workflow_id}_{mode}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


GUIDED_APPROVED_LOG = """# Workflow Run Log: Test

## Sequence Log

### Step 1
- **step_id**: 1
- **skill**: repo-sensemaker
- **status**: APPROVED

### Step 2
- **step_id**: 2
- **skill**: architectural-review
- **status**: FAILED
"""

AUTONOMOUS_COMPLETED_LOG = """# Workflow Run Log: Test

## Sequence Log

### Step 1
- **step_id**: 1
- **skill**: repo-sensemaker
- **status**: COMPLETED

### Step 2
- **step_id**: 2
- **skill**: architectural-review
- **status**: FAILED
"""

DENIED_LOG = """# Workflow Run Log: Test

## Sequence Log

### Step 1
- **step_id**: 1
- **skill**: repo-sensemaker
- **status**: DENIED
"""

MALFORMED_LOG = """# Workflow Run Log: Test

## Sequence Log

### Step 1
- **step_id**: 1
- **skill**: repo-sensemaker

### Step 2
- **step_id**: 2
- **skill**: architectural-review
- **status**: FAILED
"""


def test_genuine_guided_execution_approved_is_resumable(wfrt, tmp_log_dir):
    """A real guided_execution log with Step 1 status APPROVED (the mode's
    real MODE_CEILINGS terminal status) must be recognized as resumable."""
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", GUIDED_APPROVED_LOG)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is not None
    assert state["completed_steps"] == [1]


def test_genuine_completed_ceiling_mode_still_resumable_no_regression(wfrt, tmp_log_dir):
    """A log with status COMPLETED (legacy / a mode where COMPLETED is
    genuinely the ceiling, or an already-resumed synthetic reconstruction)
    must remain resumable -- no regression from the mode-aware change."""
    _write_run_log(tmp_log_dir, "test-workflow", "autonomous_execution", AUTONOMOUS_COMPLETED_LOG)
    runner = _make_bare_runner(wfrt, "autonomous_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is not None
    assert state["completed_steps"] == [1]


def test_failed_status_not_resumable(wfrt, tmp_log_dir):
    """FAILED must never be treated as resumable."""
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", GUIDED_APPROVED_LOG)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is not None
    assert 2 not in state["completed_steps"]


def test_denied_status_not_resumable(wfrt, tmp_log_dir):
    """DENIED must never be treated as resumable."""
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", DENIED_LOG)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    # No step is resumable and none is paused -> no resume state at all.
    assert state is None


def test_blocked_status_not_resumable(wfrt, tmp_log_dir):
    """BLOCKED must never be treated as resumable."""
    body = GUIDED_APPROVED_LOG.replace("APPROVED", "BLOCKED")
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", body)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is None or 1 not in state["completed_steps"]


def test_not_started_status_not_resumable(wfrt, tmp_log_dir):
    """NOT_STARTED must never be treated as resumable."""
    body = GUIDED_APPROVED_LOG.replace("APPROVED", "NOT_STARTED")
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", body)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is None or 1 not in state["completed_steps"]


def test_in_progress_status_not_resumable(wfrt, tmp_log_dir):
    """IN_PROGRESS must never be treated as resumable."""
    body = GUIDED_APPROVED_LOG.replace("APPROVED", "IN_PROGRESS")
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", body)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is None or 1 not in state["completed_steps"]


def test_malformed_or_missing_status_not_resumable(wfrt, tmp_log_dir):
    """A step block with no **status** line at all must not be resumable
    (the regex simply won't match it, so it can't appear in completed_steps)."""
    _write_run_log(tmp_log_dir, "test-workflow", "guided_execution", MALFORMED_LOG)
    runner = _make_bare_runner(wfrt, "guided_execution", tmp_log_dir)

    state = runner._find_resume_state()

    assert state is None or 1 not in state["completed_steps"]


def test_real_pr59_run_log_is_resumable_without_editing(wfrt, tmp_log_dir):
    """The concrete regression test: PR #59's real, unmodified live-evidence
    run log (Step 1 = APPROVED, Step 2 = FAILED) must be recognized as
    resumable at Step 1 without any hand-editing of its status field."""
    assert REAL_PR59_RUN_LOG.exists(), f"Fixture run log missing: {REAL_PR59_RUN_LOG}"

    workflow_id = "architectural-review-planning-workflow"
    mode = "guided_execution"
    dest = os.path.join(str(tmp_log_dir), f"run_log_{workflow_id}_{mode}.md")
    shutil.copy(str(REAL_PR59_RUN_LOG), dest)

    runner = _make_bare_runner(wfrt, mode, tmp_log_dir, workflow_id=workflow_id)

    state = runner._find_resume_state()

    assert state is not None, "Real PR #59 run log was not recognized as resumable"
    assert state["completed_steps"] == [1]
    assert 2 not in state["completed_steps"]


def test_resume_state_mapping_matches_mode_ceilings(wfrt):
    """The resumable-status source must be the same MODE_CEILINGS mapping
    execute_step() uses to write step statuses -- not a second, independently
    maintained vocabulary."""
    for mode, ceiling in wfrt.MODE_CEILINGS.items():
        runner = object.__new__(wfrt.OrchestrationRunner)
        runner.mode = mode
        accepted = runner._resumable_terminal_statuses()
        assert ceiling in accepted
        for rejected in ("FAILED", "BLOCKED", "DENIED", "NOT_STARTED", "IN_PROGRESS"):
            assert rejected not in accepted


def test_step_loop_actually_selects_step_2_after_resume(wfrt, tmp_log_dir):
    """End-to-end trace: after Step 1 is recognized as resumable via a real
    guided_execution/APPROVED run log, the run() step-execution loop must
    actually skip Step 1 and select/execute Step 2 next -- not merely that
    _find_resume_state() alone returns the right dict."""
    workflow_id = "test-workflow"
    mode = "guided_execution"
    _write_run_log(tmp_log_dir, workflow_id, mode, GUIDED_APPROVED_LOG)

    executed_steps = []

    def fake_execute_step(step, step_num, total_steps):
        executed_steps.append(step_num)
        return {
            "step_id": str(step_num),
            "skill": step.get("skill", "?"),
            "gate": step.get("gate", "review"),
            "output_artifact": step.get("output_artifact", "N/A"),
            "artifact_path": "",
            "validator_stack": [],
            "gate_result": "approved_by_user",
            "status": "APPROVED",
            "step_type": "local_execution",
        }

    with patch.object(wfrt.OrchestrationRunner, "_load_registries"), \
         patch.object(wfrt.OrchestrationRunner, "preflight_check", return_value=True), \
         patch.object(wfrt.OrchestrationRunner, "generate_plan"), \
         patch.object(wfrt.OrchestrationRunner, "generate_diagnostic_report"), \
         patch.object(wfrt.OrchestrationRunner, "execute_step", side_effect=fake_execute_step), \
         patch.object(wfrt.OrchestrationRunner, "write_run_log", return_value=os.path.join(str(tmp_log_dir), "x.md")), \
         patch.object(wfrt.OrchestrationRunner, "generate_implementation_report"), \
         patch.object(wfrt.OrchestrationRunner, "generate_workflow_summary_json", return_value=""), \
         patch.object(wfrt.OrchestrationRunner, "invoke_presentation_skill"), \
         patch.object(wfrt.OrchestrationRunner, "update_mode_coverage"), \
         patch.object(wfrt.OrchestrationRunner, "_should_auto_invoke_next", return_value=(False, None)):

        runner = wfrt.OrchestrationRunner(
            workflow_id=workflow_id,
            mode=mode,
            repo_root=str(REPO_ROOT),
            executor="dry-run",
            log_dir=str(tmp_log_dir),
            plan_out=str(tmp_log_dir / "plan_test.md"),
            resume=True,
        )
        runner.workflow = {
            "steps": [
                {"skill": "repo-sensemaker", "gate": "review_diagnosis", "output_artifact": "repository_sensemaking_brief"},
                {"skill": "architectural-review", "gate": "review_recommendation", "output_artifact": "architectural_review_recommendation"},
            ]
        }

        runner.run()

    # Step 1 was resumed/skipped (synthetic reconstruction), never re-executed.
    assert 1 not in executed_steps
    # Step 2 was actually selected and executed by the real step loop.
    assert 2 in executed_steps


def test_no_resume_flag_no_steps_skipped(wfrt, tmp_log_dir):
    """Baseline sanity check: without --resume, resume-state logic must not
    activate at all, and both steps must execute even though a resumable
    run log exists on disk."""
    workflow_id = "test-workflow"
    mode = "guided_execution"
    _write_run_log(tmp_log_dir, workflow_id, mode, GUIDED_APPROVED_LOG)

    executed_steps = []

    def fake_execute_step(step, step_num, total_steps):
        executed_steps.append(step_num)
        return {
            "step_id": str(step_num),
            "skill": step.get("skill", "?"),
            "gate": step.get("gate", "review"),
            "output_artifact": step.get("output_artifact", "N/A"),
            "artifact_path": "",
            "validator_stack": [],
            "gate_result": "approved_by_user",
            "status": "APPROVED",
            "step_type": "local_execution",
        }

    with patch.object(wfrt.OrchestrationRunner, "_load_registries"), \
         patch.object(wfrt.OrchestrationRunner, "preflight_check", return_value=True), \
         patch.object(wfrt.OrchestrationRunner, "generate_plan"), \
         patch.object(wfrt.OrchestrationRunner, "generate_diagnostic_report"), \
         patch.object(wfrt.OrchestrationRunner, "execute_step", side_effect=fake_execute_step), \
         patch.object(wfrt.OrchestrationRunner, "write_run_log", return_value=os.path.join(str(tmp_log_dir), "x.md")), \
         patch.object(wfrt.OrchestrationRunner, "generate_implementation_report"), \
         patch.object(wfrt.OrchestrationRunner, "generate_workflow_summary_json", return_value=""), \
         patch.object(wfrt.OrchestrationRunner, "invoke_presentation_skill"), \
         patch.object(wfrt.OrchestrationRunner, "update_mode_coverage"), \
         patch.object(wfrt.OrchestrationRunner, "_should_auto_invoke_next", return_value=(False, None)):

        runner = wfrt.OrchestrationRunner(
            workflow_id=workflow_id,
            mode=mode,
            repo_root=str(REPO_ROOT),
            executor="dry-run",
            log_dir=str(tmp_log_dir),
            plan_out=str(tmp_log_dir / "plan_test.md"),
            resume=False,
        )
        runner.workflow = {
            "steps": [
                {"skill": "repo-sensemaker", "gate": "review_diagnosis", "output_artifact": "repository_sensemaking_brief"},
                {"skill": "architectural-review", "gate": "review_recommendation", "output_artifact": "architectural_review_recommendation"},
            ]
        }

        runner.run()

    assert executed_steps == [1, 2]


def test_unrecognized_mode_fails_closed_not_silently(wfrt, tmp_log_dir):
    """An unrecognized mode must never silently fall back to a guessed
    resumable status (e.g. "VALIDATED"). CLI invocation already constrains
    --mode via argparse choices=list(KNOWN_MODES.keys()), so this can only
    happen via direct construction -- but _resumable_terminal_statuses()
    must still fail loudly rather than make an unproven resume decision."""
    _write_run_log(tmp_log_dir, "test-workflow", "not_a_real_mode", GUIDED_APPROVED_LOG)
    runner = _make_bare_runner(wfrt, "not_a_real_mode", tmp_log_dir)

    with pytest.raises(ValueError, match="not_a_real_mode"):
        runner._find_resume_state()
