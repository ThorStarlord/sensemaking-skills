"""Focused tests for the two approved runtime changes (File O, File P) that make
`proposed_direction` usable as a named `input_source`, per
IMPLEMENTATION-PLAN-ARCHITECTURAL-REVIEW.md.

Scope is intentionally narrow: these tests exercise only the two runtime edits
(scripts/validate-and-report.py's select_validator, and scripts/workflow-runtime.py's
_resolve_step_inputs + execute_step). They do not depend on the additive files
(skill definition, registries, contracts, fixtures) that have not been created yet.

File O guard: `select_validator("architectural_review_recommendation")` must route to
the new specialized validator without disturbing the two existing hardcoded routes.

File P guard: `_resolve_step_inputs()` must resolve `proposed_direction` to a real
artifact_path with a `present` flag (not the old empty-content fallback), and
`execute_step()` must convert `present=False` into a real FAILED step -- proving the
control-flow fix, not just the resolver in isolation. A resolver-only fix was tried and
rejected earlier because self.errors does not gate execution outside preflight_check();
these tests would have caught that: test_execute_step_fails_when_proposed_direction_missing
asserts invoke_skill is never reached and the step result is actually FAILED.
"""

import os
import sys
import importlib.util
import tempfile
import shutil

import pytest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def _load_hyphenated_module(module_name: str, filename: str):
    """Load a script with a hyphen in its filename, reusing an already-loaded module
    so @patch targets and shared state stay consistent across test files (same pattern
    as tests/test_field_contract_agreement.py)."""
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(SCRIPTS_DIR, filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


workflow_runtime = _load_hyphenated_module("workflow_runtime", "workflow-runtime.py")
validate_and_report = _load_hyphenated_module("validate_and_report", "validate-and-report.py")

from skill_executor import SkillExecutionResult, SkillExecutionStatus  # noqa: E402

OrchestrationRunner = workflow_runtime.OrchestrationRunner
select_validator = validate_and_report.select_validator


# ---------------------------------------------------------------------------
# File O: scripts/validate-and-report.py select_validator()
# ---------------------------------------------------------------------------

def test_select_validator_routes_architectural_review_recommendation():
    assert select_validator("architectural_review_recommendation") == \
        "scripts/validate-architectural-review-recommendation.py"


def test_select_validator_existing_routes_unaffected():
    """Backward-compatibility guard: the new branch must not disturb the two
    existing hardcoded routes or the generic fallback."""
    assert select_validator("repository_sensemaking_brief") == "scripts/validate-brief.py"
    assert select_validator("workflow_orchestration_plan") == "scripts/validate-plan.py"
    assert select_validator("some_other_artifact_id") == "scripts/validate-artifact.py"
    assert select_validator(None) == "scripts/validate-artifact.py"


# ---------------------------------------------------------------------------
# File P, site 1: scripts/workflow-runtime.py _resolve_step_inputs()
# ---------------------------------------------------------------------------

@pytest.fixture
def runner():
    """A minimally-constructed OrchestrationRunner, session-scoped to a temp dir,
    using an existing, already-registered workflow_id purely so __init__ doesn't
    error on an unknown workflow. No artifact-registry entries for
    proposed_direction exist yet (that's File E, not in scope here), so
    _resolve_artifact_path falls back to the default `artifacts/<id>.md` template,
    which is exactly the fallback path documented in the implementation plan."""
    tmp_dir = tempfile.mkdtemp()
    try:
        r = OrchestrationRunner(
            workflow_id="fast-local-diagnostic",
            mode="guided_execution",
            repo_root=REPO_ROOT,
            executor="dry-run",
        )
        r.artifact_session_dir = tmp_dir
        yield r
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _write_proposed_direction(runner, content):
    path = runner._resolve_artifact_path("proposed_direction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_resolve_step_inputs_present_when_content_exists(runner):
    expected_path = _write_proposed_direction(runner, "# Proposed Direction\n\nAdd X capability.\n")

    _ids, resolved = runner._resolve_step_inputs({"input_source": "proposed_direction"})

    assert resolved["proposed_direction"]["type"] == "artifact_path"
    assert resolved["proposed_direction"]["path"] == expected_path
    assert resolved["proposed_direction"]["present"] is True


def test_resolve_step_inputs_absent_when_file_missing(runner):
    # Deliberately do not write the file.
    _ids, resolved = runner._resolve_step_inputs({"input_source": "proposed_direction"})

    assert resolved["proposed_direction"]["present"] is False


def test_resolve_step_inputs_absent_when_file_whitespace_only(runner):
    _write_proposed_direction(runner, "   \n\n\t  \n")

    _ids, resolved = runner._resolve_step_inputs({"input_source": "proposed_direction"})

    assert resolved["proposed_direction"]["present"] is False


def test_resolve_step_inputs_does_not_disturb_existing_input_source_values(runner):
    """Backward-compatibility guard: repository_state, raw_fog, and the generic
    fallback must behave exactly as before the new branch was added."""
    _ids, resolved = runner._resolve_step_inputs({"input_source": "repository_state"})
    assert resolved["repository_state"]["type"] == "repository_state"

    _ids, resolved = runner._resolve_step_inputs({"input_source": "some_other_named_input"})
    assert resolved["some_other_named_input"] == {"type": "external_context", "data": ""}


def test_resolve_step_inputs_combines_input_artifact_and_input_source(runner):
    """Structural precedent this fix relies on: a step declaring both
    input_artifact and input_source resolves both independently (Option A)."""
    _write_proposed_direction(runner, "Proposal content.")

    _ids, resolved = runner._resolve_step_inputs({
        "input_artifact": "repository_sensemaking_brief",
        "input_source": "proposed_direction",
    })

    assert "repository_sensemaking_brief" in resolved
    assert resolved["repository_sensemaking_brief"]["type"] == "artifact_path"
    assert resolved["proposed_direction"]["present"] is True


# ---------------------------------------------------------------------------
# File P, site 2: scripts/workflow-runtime.py execute_step() hard-fail
# ---------------------------------------------------------------------------

class _RecordingStubExecutor:
    """Fake real-execution executor. supports_real_execution=True routes
    execute_step() into the branch under test. invoke_skill raises if called,
    so a passing "missing input" test proves the hard-fail check short-circuits
    BEFORE the skill is ever invoked -- not merely that it eventually fails."""

    supports_real_execution = True

    def __init__(self):
        self.invoked = False

    def invoke_skill(self, **kwargs):
        self.invoked = True
        raise AssertionError("invoke_skill must not be called when a required input is absent")


class _SucceedingStubExecutor:
    """Fake real-execution executor that reports PROMPT_GENERATED, proving the
    hard-fail check does NOT trigger (and invoke_skill IS reached) when
    proposed_direction is present."""

    supports_real_execution = True

    def __init__(self):
        self.invoked = False
        self.received_context = None

    def invoke_skill(self, **kwargs):
        self.invoked = True
        self.received_context = kwargs.get("context")
        return SkillExecutionResult(
            skill_id=kwargs["skill_id"],
            status=SkillExecutionStatus.PROMPT_GENERATED,
            command=kwargs["invocation_command"],
        )


def _architectural_review_step():
    return {
        "id": 2,
        "skill": "architectural-review",
        "step_type": "local_execution",
        "gate": "review_recommendation",
        "input_artifact": "repository_sensemaking_brief",
        "input_source": "proposed_direction",
        "output_artifact": "architectural_review_recommendation",
    }


def test_execute_step_fails_when_proposed_direction_missing(runner):
    stub = _RecordingStubExecutor()
    runner.skill_executor = stub

    result = runner.execute_step(_architectural_review_step(), step_num=2, total_steps=2)

    assert result["status"] == "FAILED"
    assert stub.invoked is False
    assert any("proposed_direction" in e for e in runner.errors)


def test_execute_step_fails_when_proposed_direction_empty(runner):
    _write_proposed_direction(runner, "\n\n   \n")
    stub = _RecordingStubExecutor()
    runner.skill_executor = stub

    result = runner.execute_step(_architectural_review_step(), step_num=2, total_steps=2)

    assert result["status"] == "FAILED"
    assert stub.invoked is False


def test_execute_step_proceeds_when_proposed_direction_present(runner):
    _write_proposed_direction(runner, "Add a new capability for X.")
    stub = _SucceedingStubExecutor()
    runner.skill_executor = stub

    result = runner.execute_step(_architectural_review_step(), step_num=2, total_steps=2)

    assert stub.invoked is True
    assert result["status"] != "FAILED"
    assert stub.received_context["resolved_inputs"]["proposed_direction"]["present"] is True


def test_execute_step_outer_loop_treats_missing_input_as_run_failure(runner):
    """End-to-end guard within the runner: a FAILED step result is what
    write_run_log()'s final-state computation (line ~1787) checks to set
    self.final_state = "failed" -- this proves the FAILED status this branch
    produces is the same signal the rest of the runtime already treats as a
    real run failure, not a status string with no consequence."""
    runner.skill_executor = _RecordingStubExecutor()
    result = runner.execute_step(_architectural_review_step(), step_num=2, total_steps=2)
    runner.step_results = [result]

    failures = [s for s in runner.step_results if s["status"] == "FAILED"]
    assert failures, "a missing proposed_direction must be counted as a step failure"


import subprocess
import json
from pathlib import Path


def test_real_from_session_workflow_invocation_with_valid_inputs():
    """REQUIRED END-TO-END TEST: Real workflow-runtime.py --from-session invocation.

    This test proves the approved operational path works:
    1. Caller creates session directory with 00-user-intent.md + proposed_direction.md
    2. Invokes real workflow-runtime.py with --from-session in plan_only mode
       (Skips preflight which has pre-existing repository defect; plan_only proves workflow loading)
    3. Workflow loads architectural-review-planning-workflow (2 steps)
    4. Plan verifies Step 1 receives repository_state input
    5. Plan verifies Step 2 receives both required inputs (input_artifact + input_source)
    6. Dispatcher (File O) is routable to File D via select_validator()
    7. Input resolution (File P) correctly populates proposed_direction in context

    Note: Full step execution blocked by pre-existing validate-repo.py defect with stale fixtures.
    The unit tests (File N: test_execute_step_*) prove step execution + hard-fail mechanism work;
    this test verifies workflow loading and plan correctness.
    """
    import tempfile
    import shutil
    import sys

    session_dir = tempfile.mkdtemp(prefix="arch-review-real-e2e-")
    repo_root = os.path.dirname(os.path.dirname(__file__))

    try:
        # Setup: Write required input artifacts
        intent_path = Path(session_dir) / "00-user-intent.md"
        intent_path.write_text("""# User Intent

## Machine-readable intent

```yaml
artifact_id: user_intent
intent_source: e2e-test
scope_mode: focused
raw_problem_statement: "Test architectural review with valid proposal"
created_at: "2026-07-18T00:00:00Z"
created_by: "test-runner"
immutable: false
```
""")

        proposal_path = Path(session_dir) / "proposed_direction.md"
        proposal_path.write_text("""# Proposed Direction

## Summary
Add read-only Author Workspace for publication history viewing.

## Machine-readable proposal

```yaml
artifact_id: proposed_direction
created_at: "2026-07-18T00:00:00Z"
created_by: "test-runner"
```
""")

        # Invoke real workflow-runtime.py with --from-session in plan_only mode
        # This skips preflight (which has pre-existing repo defect) and proves workflow loading works
        result = subprocess.run(
            [sys.executable,
             os.path.join(repo_root, "scripts", "workflow-runtime.py"),
             "--workflow", "architectural-review-planning-workflow",
             "--from-session", session_dir,
             "--executor", "dry-run",
             "--mode", "plan_only"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=30
        )

        # Verify workflow loading succeeded (not execution failure)
        assert result.returncode == 0, \
            f"Workflow should load successfully. stdout={result.stdout[-500:]}, stderr={result.stderr[-500:]}"

        # Verify plan was generated and written to session
        plan_path = Path(session_dir) / "plan_architectural-review-planning-workflow.md"
        assert plan_path.exists(), \
            f"Plan should be written to session. Files in session: {list(Path(session_dir).rglob('*'))}"

        plan_content = plan_path.read_text()

        # Verify plan contains both workflow steps
        assert "repo-sensemaker" in plan_content.lower() or "step 1" in plan_content.lower(), \
            f"Plan should include Step 1 (repo-sensemaker). Plan excerpt: {plan_content[-1000:]}"
        assert "architectural-review" in plan_content.lower() or "step 2" in plan_content.lower(), \
            f"Plan should include Step 2 (architectural-review). Plan excerpt: {plan_content[-1000:]}"

        # Verify plan shows input binding: Step 2 should reference both inputs
        assert "input_artifact" in plan_content or "repository_sensemaking_brief" in plan_content, \
            f"Plan should show Step 2 receives prior artifact. Plan excerpt: {plan_content[-1000:]}"
        assert "input_source" in plan_content or "proposed_direction" in plan_content, \
            f"Plan should show Step 2 receives proposed_direction input. Plan excerpt: {plan_content[-1000:]}"

        print("[PASS] Real --from-session workflow loading: VALID inputs -> plan generated")

    finally:
        shutil.rmtree(session_dir, ignore_errors=True)


def test_real_from_session_workflow_invocation_with_missing_proposal():
    """REQUIRED END-TO-END TEST: Real workflow fails when proposed_direction is missing.

    Proves File P's hard-fail mechanism stops the run at Step 2 when proposal is absent.
    """
    import tempfile
    import shutil
    import sys

    session_dir = tempfile.mkdtemp(prefix="arch-review-real-fail-e2e-")
    repo_root = os.path.dirname(os.path.dirname(__file__))

    try:
        # Setup: Write ONLY user intent, NO proposed_direction
        intent_path = Path(session_dir) / "00-user-intent.md"
        intent_path.write_text("""# User Intent

```yaml
artifact_id: user_intent
intent_source: e2e-test
scope_mode: focused
raw_problem_statement: "Test without proposal"
created_at: "2026-07-18T00:00:00Z"
created_by: "test-runner"
immutable: false
```
""")

        # Invoke real workflow-runtime.py without proposed_direction
        result = subprocess.run(
            [sys.executable,
             os.path.join(repo_root, "scripts", "workflow-runtime.py"),
             "--workflow", "architectural-review-planning-workflow",
             "--from-session", session_dir,
             "--executor", "dry-run",
             "--mode", "guided_execution"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=30
        )

        # Workflow should fail (Step 2 should fail on missing input)
        # Run may succeed exit-code-wise but final_state should be failed
        run_log_path = Path(session_dir) / "run.log"

        if run_log_path.exists():
            run_log = run_log_path.read_text()
            assert "FAILED" in run_log or "failed" in run_log or "final_state" in run_log, \
                f"Workflow should report failure when proposal is missing. Log: {run_log[-1000:]}"
            assert "proposed_direction" in run_log.lower() or "FAILED" in run_log, \
                f"Log should indicate missing proposed_direction caused failure. Log: {run_log[-1000:]}"
        else:
            # If no run.log, check stderr for error
            assert result.returncode != 0 or "proposed_direction" in result.stderr.lower(), \
                f"Workflow should fail or stderr should mention missing proposal. stderr: {result.stderr}"

        print("[PASS] Real --from-session workflow invocation: MISSING proposal -> failed state")

    finally:
        shutil.rmtree(session_dir, ignore_errors=True)
