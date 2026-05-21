"""Regression tests for the runtime<->executor artifact-path handoff.

Background (the bug these tests lock down):
  A real skill run (problem-framer via the claude-code executor) wrote its
  artifact to the flat path `artifacts/problem_frame.md`, but the runtime —
  which session-scopes every artifact — looked for it at
  `artifacts/<session>/problem_frame.md`. The executor returned EXECUTED, the
  runtime could not find the file, and the step failed with
  "Executor reported success but artifact not found".

  Root cause: producer (executor) and consumer (runtime) computed the output
  path independently and disagreed. The runtime owns path resolution
  (`_resolve_artifact_path` -> session scoping), so it must hand the resolved
  path to the executor instead of letting the executor guess.

These tests assert the fixed contract:
  1. `resolve_output_path` prefers the runtime-provided path and only falls
     back to the flat path when none is supplied.
  2. The real `OrchestrationRunner.execute_step` hands the session-scoped path
     to the executor, so an executor that writes where it is told produces an
     artifact the runtime can find.
"""

import os
import sys
import tempfile
import shutil
import importlib.util
import unittest
from unittest.mock import MagicMock

# Add scripts directory to sys.path so scripts can import _validator_utils
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from skill_executor import (
    resolve_output_path,
    SkillExecutionResult,
    SkillExecutionStatus,
)

# Load scripts/workflow-runtime.py dynamically due to hyphen in filename.
# Reuse the already-loaded module if another test file loaded it first, so we
# do not clobber sys.modules["workflow_runtime"] — clobbering it breaks other
# test files that bind OrchestrationRunner and @patch this module by name.
if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime",
        os.path.join(scripts_dir, "workflow-runtime.py"),
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


class TestResolveOutputPath(unittest.TestCase):
    """Unit tests for the shared output-path resolver used by real executors."""

    def test_prefers_runtime_provided_path(self):
        """When the runtime supplies expected_output_path, the executor must use it
        verbatim (this is the session-scoped path the runtime will check)."""
        session_path = os.path.join(
            "/repo", "artifacts", "100-orchestration-run", "problem_frame.md"
        )
        ctx = {"expected_output_path": session_path}
        result = resolve_output_path("/repo", "problem_frame", ctx)
        self.assertEqual(result, session_path)

    def test_falls_back_to_flat_path(self):
        """With no runtime-provided path (e.g. standalone executor use), fall back
        to the flat artifacts/<id>.md path."""
        result = resolve_output_path("/repo", "problem_frame", {})
        self.assertEqual(
            os.path.normpath(result),
            os.path.normpath(os.path.join("/repo", "artifacts", "problem_frame.md")),
        )

    def test_none_context_falls_back(self):
        """A missing context dict must not raise; it falls back to the flat path."""
        result = resolve_output_path("/repo", "problem_frame", None)
        self.assertEqual(
            os.path.normpath(result),
            os.path.normpath(os.path.join("/repo", "artifacts", "problem_frame.md")),
        )


class _PathHonoringExecutor:
    """A stand-in for a real executor (e.g. claude-code) that writes its artifact
    to whatever path the runtime resolves for it, using the production helper.

    This mimics the *fixed* executor faithfully: it does not invent its own path,
    it uses resolve_output_path(... context). If the runtime fails to pass
    expected_output_path, this executor falls back to the flat path — which is
    exactly the situation that produced the original bug.
    """

    supports_real_execution = True

    def __init__(self, repo_root):
        self.repo_root = repo_root

    def invoke_skill(self, skill_id, invocation_command, input_artifacts,
                     expected_output_artifact, context):
        out_path = resolve_output_path(self.repo_root, expected_output_artifact, context)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# Problem Frame\n\nfake but real-on-disk artifact\n")
        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.EXECUTED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
        )


class TestRuntimeExecutorHandoff(unittest.TestCase):
    """Exercise the real OrchestrationRunner.execute_step path resolution + executor
    handoff (not logic-in-isolation). Proves the producer writes where the consumer
    reads when a session directory is active."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo_root = self.tmp
        self.session_dir = os.path.join(self.repo_root, "artifacts", "100-orchestration-run")
        os.makedirs(self.session_dir, exist_ok=True)

        # Build a runner with real path methods bound, everything else stubbed.
        self.runner = MagicMock(spec=OrchestrationRunner)
        self.runner.workflow_id = "full-local-sensemaking"
        self.runner.session_id = "session-xyz"
        self.runner.repo_root = self.repo_root
        self.runner.artifact_session_dir = self.session_dir
        self.runner.use_fixtures = False
        self.runner.mode = "guided_execution"
        self.runner.errors = []
        self.runner.contracts = {
            "artifacts": [
                {"id": "problem_frame", "path": "artifacts/problem_frame.md"}
            ]
        }
        self.runner.skill_executor = _PathHonoringExecutor(self.repo_root)

        # Bind the real methods we want to exercise.
        self.runner.execute_step = OrchestrationRunner.execute_step.__get__(
            self.runner, OrchestrationRunner)
        self.runner._resolve_artifact_path = OrchestrationRunner._resolve_artifact_path.__get__(
            self.runner, OrchestrationRunner)
        self.runner._scope_to_session_dir = OrchestrationRunner._scope_to_session_dir.__get__(
            self.runner, OrchestrationRunner)

        # Stub the parts not under test.
        self.runner._resolve_step_inputs = MagicMock(return_value=([], {}))
        self.runner._run_validator_stack = MagicMock(return_value=[])
        self.runner._manage_gate = MagicMock(return_value="approved_by_user")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_step_succeeds_when_executor_honors_runtime_path(self):
        """The runtime must pass its session-scoped path to the executor so the
        artifact lands where the runtime then looks. Before the fix the runtime
        passed no path, the executor fell back to the flat artifacts/ path, and
        this step failed with ARTIFACT_NOT_FOUND."""
        step = {
            "skill": "problem-framer",
            "gate": "review_problem_frame",
            "output_artifact": "problem_frame",
            "step_type": "local_execution",
        }

        result = self.runner.execute_step(step, 1, 6)

        # No "artifact not found" error should have been recorded.
        self.assertEqual(
            self.runner.errors, [],
            f"Unexpected errors during step execution: {self.runner.errors}",
        )
        # guided_execution ends a clean step at VALIDATED.
        self.assertEqual(result["status"], "VALIDATED")
        # The artifact must exist at the session-scoped path the runtime owns.
        expected = os.path.join(self.session_dir, "problem_frame.md")
        self.assertTrue(
            os.path.exists(expected),
            f"Artifact not found at session-scoped path: {expected}",
        )
        # And NOT at the flat path (that would mean producer/consumer diverged).
        flat = os.path.join(self.repo_root, "artifacts", "problem_frame.md")
        self.assertFalse(
            os.path.exists(flat),
            "Artifact written to flat path; producer and consumer disagree.",
        )


if __name__ == "__main__":
    unittest.main()
