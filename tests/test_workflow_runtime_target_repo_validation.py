"""Confirms workflow-runtime.py's real validate-and-report.py invocation
passes --target-repo through, not just the standalone validate-brief.py CLI.

This traces the fix through the actual execution path used by a live run:
OrchestrationRunner._run_validate_and_report -> validate-and-report.py ->
invoke_validator() -> validate-brief.py --target-repo.
"""
import importlib.util
import os
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

spec = importlib.util.spec_from_file_location(
    "workflow_runtime", os.path.join(SCRIPTS_DIR, "workflow-runtime.py")
)
workflow_runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow_runtime)


class TestWorkflowRuntimePassesTargetRepo(unittest.TestCase):
    def test_run_validate_and_report_includes_target_repo_flag(self):
        """When self.target_repo differs from self.repo_root, the subprocess
        command list built by _run_validate_and_report must include
        --target-repo <target_repo>."""
        runner = workflow_runtime.OrchestrationRunner.__new__(workflow_runtime.OrchestrationRunner)
        runner.repo_root = os.path.abspath(".")
        runner.target_repo = os.path.abspath("..")  # deliberately different from repo_root
        runner.log_dir = None

        # Reconstruct just the command-building logic by calling the real
        # method up to subprocess dispatch; we intercept subprocess.run to
        # capture the built command instead of actually invoking a validator.
        captured = []

        class _FakeCompletedProcess:
            stdout = '{"valid": true, "errors": []}'
            stderr = ""

        def _fake_run(cmd, **kwargs):
            captured.append(cmd)
            return _FakeCompletedProcess()

        orig_run = workflow_runtime.subprocess.run
        workflow_runtime.subprocess.run = _fake_run
        try:
            runner._run_validate_and_report("repository_sensemaking_brief", "brief.md", [])
        finally:
            workflow_runtime.subprocess.run = orig_run

        # First subprocess.run call is validate-and-report.py; the second
        # (if any) is record-validation.py, which doesn't take --target-repo.
        validate_cmd = next(c for c in captured if any("validate-and-report.py" in str(part) for part in c))
        self.assertIn(
            "--target-repo", validate_cmd,
            f"target_repo was not threaded into the real command: {validate_cmd}",
        )
        idx = validate_cmd.index("--target-repo")
        self.assertEqual(validate_cmd[idx + 1], runner.target_repo)

    def test_no_target_repo_flag_when_target_equals_repo_root(self):
        """When target_repo == repo_root (the internal-proof/default case),
        --target-repo must NOT be passed, preserving existing behavior."""
        runner = workflow_runtime.OrchestrationRunner.__new__(workflow_runtime.OrchestrationRunner)
        runner.repo_root = os.path.abspath(".")
        runner.target_repo = runner.repo_root
        runner.log_dir = None

        captured = {}

        class _FakeCompletedProcess:
            stdout = '{"valid": true, "errors": []}'
            stderr = ""

        def _fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            return _FakeCompletedProcess()

        orig_run = workflow_runtime.subprocess.run
        workflow_runtime.subprocess.run = _fake_run
        try:
            runner._run_validate_and_report("repository_sensemaking_brief", "brief.md", [])
        finally:
            workflow_runtime.subprocess.run = orig_run

        cmd = captured.get("cmd", [])
        self.assertNotIn("--target-repo", cmd)


if __name__ == "__main__":
    unittest.main()
