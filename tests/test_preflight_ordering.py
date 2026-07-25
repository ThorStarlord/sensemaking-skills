"""Regression tests for preflight ordering defect fix (ADR 0011).

Tests verify that runner.run() calls preflight_check() BEFORE
_create_user_intent_artifact(), that failed preflight prevents artifact 
creation, and that repo-inferred None problems are preserved.

Tests use mocking to verify call ordering - NO DESTRUCTIVE OPERATIONS.
"""

import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def same_drive_tmp_path():
    """A tempdir on the same drive as the repo.

    pytest's built-in tmp_path lives under the OS temp dir, which on
    Windows CI/dev machines can be on a different drive than the repo
    checkout (e.g. C: vs H:) -- os.path.relpath() raises ValueError across
    drives. These tests run the real OrchestrationRunner.run(), which calls
    os.path.relpath(path, self.repo_root) while writing Phase 2/4 reports,
    so the confinement dir must be same-drive.
    """
    repo_root = Path(__file__).parent.parent
    d = tempfile.mkdtemp(prefix="preflight-ordering-", dir=str(repo_root.parent))
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def runner_module():
    """Load the OrchestrationRunner module."""
    scripts_dir = Path(__file__).parent.parent / "scripts"
    sys.path.insert(0, str(scripts_dir))
    
    import importlib.util
    importlib.invalidate_caches()
    spec = importlib.util.spec_from_file_location("wfrt", str(scripts_dir / "workflow-runtime.py"))
    wfrt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wfrt)
    
    return wfrt


def test_run_calls_preflight_before_artifact(runner_module, same_drive_tmp_path):
    """run() must call preflight_check() BEFORE _create_user_intent_artifact()."""
    call_order = []
    repo_root = Path(__file__).parent.parent
    
    def track_preflight():
        call_order.append("preflight")
        return True
    
    def track_artifact(*args):
        call_order.append("artifact")
        return "path/to/artifact"
    
    with patch.object(runner_module.OrchestrationRunner, 'preflight_check', side_effect=track_preflight), \
         patch.object(runner_module.OrchestrationRunner, '_create_user_intent_artifact', side_effect=track_artifact), \
         patch.object(runner_module.OrchestrationRunner, '_load_registries'):
        
        runner = runner_module.OrchestrationRunner(
            workflow_id='test',
            mode='guided_execution',  # Mutating mode, not plan_only
            repo_root=str(repo_root),
            executor='dry-run',
            log_dir=str(same_drive_tmp_path),
            plan_out=str(same_drive_tmp_path / "plan_test.md"),
        )
        runner.create_intent_artifact = True
        runner.problem_for_intent = "test"
        runner.scope_for_intent = "soft"

        # Invoke run()
        result = runner.run()

        # ASSERTIONS: preflight must come FIRST, then artifact, in exact order
        assert len(call_order) >= 2, \
            f"Expected at least preflight and artifact calls. Order: {call_order}"
        assert call_order[0] == "preflight", \
            f"First call must be preflight. Order: {call_order}"
        assert call_order[1] == "artifact", \
            f"Second call must be artifact. Order: {call_order}"


def test_failed_preflight_prevents_artifact_creation(runner_module, same_drive_tmp_path):
    """Failed preflight must prevent artifact creation - artifact never called."""
    artifact_called = []
    repo_root = Path(__file__).parent.parent
    
    def track_artifact(*args):
        artifact_called.append(True)
        return "path"
    
    with patch.object(runner_module.OrchestrationRunner, 'preflight_check', return_value=False), \
         patch.object(runner_module.OrchestrationRunner, '_create_user_intent_artifact', side_effect=track_artifact), \
         patch.object(runner_module.OrchestrationRunner, '_load_registries'):
        
        runner = runner_module.OrchestrationRunner(
            workflow_id='test',
            mode='guided_execution',
            repo_root=str(repo_root),
            executor='dry-run',
            log_dir=str(same_drive_tmp_path),
            plan_out=str(same_drive_tmp_path / "plan_test.md"),
        )
        runner.create_intent_artifact = True
        runner.problem_for_intent = "test"
        runner.scope_for_intent = "soft"

        # Invoke run()
        result = runner.run()

        # ASSERTIONS: artifact must NOT be called when preflight fails
        assert not artifact_called, \
            f"artifact should not be created when preflight_check() returns False"
        assert result == 1, \
            f"run() should return 1 when preflight fails"


def test_from_session_skips_artifact_creation(runner_module, same_drive_tmp_path):
    """Existing artifact_session_dir must prevent artifact creation."""
    artifact_called = []
    repo_root = Path(__file__).parent.parent
    
    def track_artifact(*args):
        artifact_called.append(True)
        return "path"
    
    with patch.object(runner_module.OrchestrationRunner, 'preflight_check', return_value=True), \
         patch.object(runner_module.OrchestrationRunner, '_create_user_intent_artifact', side_effect=track_artifact), \
         patch.object(runner_module.OrchestrationRunner, '_load_registries'):
        
        runner = runner_module.OrchestrationRunner(
            workflow_id='test',
            mode='guided_execution',
            repo_root=str(repo_root),
            executor='dry-run',
            log_dir=str(same_drive_tmp_path),
            plan_out=str(same_drive_tmp_path / "plan_test.md"),
        )

        # Simulate --from-session: set artifact_session_dir
        runner.artifact_session_dir = str(repo_root / "artifacts" / "session")
        runner.create_intent_artifact = True  # Flag is set, but session dir exists
        runner.problem_for_intent = "test"
        
        # Invoke run()
        result = runner.run()
        
        # ASSERTIONS: artifact must NOT be created when session dir exists
        assert not artifact_called, \
            "artifact should not be created when artifact_session_dir is set"
        # Verify intent_path is set to existing session's artifact
        expected_path = str(repo_root / "artifacts" / "session" / "00-user-intent.md")
        assert runner.intent_path == expected_path, \
            f"intent_path should point to existing session artifact"


def test_repo_inferred_none_problem_creates_artifact(runner_module, same_drive_tmp_path):
    """Repo-inferred flows with problem=None should still create artifact."""
    artifact_calls = []
    repo_root = Path(__file__).parent.parent
    
    def track_artifact(problem, scope):
        artifact_calls.append((problem, scope))
        return "path"
    
    with patch.object(runner_module.OrchestrationRunner, 'preflight_check', return_value=True), \
         patch.object(runner_module.OrchestrationRunner, '_create_user_intent_artifact', side_effect=track_artifact), \
         patch.object(runner_module.OrchestrationRunner, '_load_registries'):
        
        runner = runner_module.OrchestrationRunner(
            workflow_id='test',
            mode='guided_execution',
            repo_root=str(repo_root),
            executor='dry-run',
            log_dir=str(same_drive_tmp_path),
            plan_out=str(same_drive_tmp_path / "plan_test.md"),
        )

        # Repo-inferred flow: problem can be None
        runner.create_intent_artifact = True
        runner.problem_for_intent = None  # Explicitly None
        runner.scope_for_intent = "soft"
        
        # Invoke run()
        result = runner.run()
        
        # ASSERTION: artifact should still be created even when problem is None
        assert len(artifact_calls) == 1, \
            f"artifact should be created for repo-inferred flow (problem=None). Calls: {artifact_calls}"
        assert artifact_calls[0] == (None, "soft"), \
            f"artifact should be called with None problem and soft scope. Calls: {artifact_calls}"


def test_plan_only_skips_user_intent_artifact(runner_module, same_drive_tmp_path):
    """Plan-only mode skips user-intent artifact creation.

    Note: Plan-only still generates plans and diagnostic reports;
    this test only verifies that 00-user-intent.md is not created.
    """
    artifact_called = []
    repo_root = Path(__file__).parent.parent

    def track_artifact(*args):
        artifact_called.append(True)
        return "path"

    with patch.object(runner_module.OrchestrationRunner, '_create_user_intent_artifact', side_effect=track_artifact), \
         patch.object(runner_module.OrchestrationRunner, '_load_registries'):

        runner = runner_module.OrchestrationRunner(
            workflow_id='test',
            mode='plan_only',
            repo_root=str(repo_root),
            executor='dry-run',
            log_dir=str(same_drive_tmp_path),
            plan_out=str(same_drive_tmp_path / "plan_test.md"),
        )

        runner.create_intent_artifact = True  # Flag set, but plan_only overrides
        runner.problem_for_intent = "test"
        runner.scope_for_intent = "soft"

        # Invoke run()
        result = runner.run()

        # ASSERTION: user-intent artifact must NOT be created in plan_only
        assert not artifact_called, \
            "plan_only mode should not create 00-user-intent.md artifact"

