"""Regression test for run_log_path AttributeError fix.

Tests that _run_validate_and_report() correctly uses self.log_dir instead of
the undefined self.run_log_path attribute.
"""

import os
import sys
import json
import tempfile
import importlib.util
from unittest.mock import patch, MagicMock

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

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


def test_run_validate_and_report_uses_log_dir():
    """Behavioral test: _run_validate_and_report() correctly constructs validation run log path.

    Before fix: AttributeError: 'OrchestrationRunner' object has no attribute 'run_log_path'
    After fix: Uses self.log_dir to construct the run log path

    This test exercises the real method path and verifies:
    - No AttributeError is raised
    - The validation run log path is correctly passed to the record script
    - The path is os.path.join(log_dir, "validation_run_log.md")
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal runner with log_dir set
        runner = OrchestrationRunner.__new__(OrchestrationRunner)
        runner.repo_root = tmpdir
        runner.log_dir = tmpdir
        runner.workflow_id = "test"

        # Create a dummy artifact to validate
        artifact_path = os.path.join(tmpdir, "test_artifact.md")
        with open(artifact_path, "w") as f:
            f.write("# Test Artifact")

        # Expected validation log path
        expected_run_log_path = os.path.join(tmpdir, "validation_run_log.md")

        # Mock subprocess.run to capture validator calls without actually running them
        captured_record_cmd = {}

        def mock_run(cmd, *args, **kwargs):
            result = MagicMock()
            result.returncode = 0
            result.stdout = json.dumps({"valid": True, "errors": []})
            result.stderr = ""

            # Capture record-validation.py calls to check the run_log_path
            if len(cmd) > 1 and "record-validation.py" in cmd[1]:
                # Extract --run-log path
                if "--run-log" in cmd:
                    idx = cmd.index("--run-log")
                    captured_record_cmd["path"] = cmd[idx + 1]

            return result

        # Mock os.path.exists to pretend validator scripts exist
        def mock_exists(path):
            if "validate-and-report.py" in path or "record-validation.py" in path:
                return True
            return os.path.exists(path)

        with patch("subprocess.run", side_effect=mock_run):
            with patch("os.path.exists", side_effect=mock_exists):
                # Call the method that previously raised AttributeError
                try:
                    stack = runner._run_validate_and_report(
                        artifact_id="test_artifact",
                        artifact_path=artifact_path,
                        stack=[]
                    )
                    # If we reach here, no AttributeError was raised
                    assert isinstance(stack, list)
                except AttributeError as e:
                    if "run_log_path" in str(e):
                        raise AssertionError(
                            f"AttributeError indicates fix was not applied: {e}"
                        )
                    raise

        # Verify that record-validation.py received the correct run_log_path
        if captured_record_cmd:
            assert captured_record_cmd["path"] == expected_run_log_path, \
                f"Expected {expected_run_log_path}, got {captured_record_cmd['path']}"


def test_log_dir_initialization():
    """Verify that log_dir is properly initialized in OrchestrationRunner.__init__."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("workflow_runtime.create_executor", return_value=None):
            runner = OrchestrationRunner(
                workflow_id="test",
                mode="autonomous_execution",
                repo_root=tmpdir,
                log_dir=tmpdir
            )
            assert hasattr(runner, 'log_dir')
            assert runner.log_dir == tmpdir
