"""Unit tests for dynamic artifact path resolution in workflow-runtime.py."""

import os
import sys
import importlib.util
import unittest
from unittest.mock import patch, MagicMock

# Add scripts directory to sys.path so scripts can import _validator_utils
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Load scripts/workflow-runtime.py dynamically due to hyphen in filename.
# Reuse the already-loaded module if another test file loaded it first. Clobbering
# sys.modules["workflow_runtime"] gives different test files different module objects,
# so @patch("workflow_runtime.<x>") here can target a module instance other than the
# one our bound OrchestrationRunner came from (mock then never fires).
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


class TestDynamicPathResolution(unittest.TestCase):
    """Test cases for dynamic path resolution of artifacts."""

    def setUp(self):
        # Create a mock OrchestrationRunner without calling __init__
        self.runner = MagicMock(spec=OrchestrationRunner)
        self.runner.workflow_id = "test-wf"
        self.runner.session_id = "session-123"
        self.runner.repo_root = "h:\\GithubRepositories\\sensemaking-skills"
        self.runner.artifact_session_dir = None

        # Explicitly bind methods to the mock instance
        # so we can test the actual method logic
        self.runner._resolve_artifact_path = OrchestrationRunner._resolve_artifact_path.__get__(self.runner, OrchestrationRunner)
        self.runner._scope_to_session_dir = OrchestrationRunner._scope_to_session_dir.__get__(self.runner, OrchestrationRunner)

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_from_contracts_with_path(self, mock_load):
        """Test resolving an artifact path from contracts using the path field."""
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "custom_dir/{workflow_id}/{session_id}_report.md"
                }
            ]
        }

        # Resolve path
        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        # Expected path
        expected_rel = os.path.join("custom_dir", "test-wf", "session-123_report.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))
        mock_load.assert_not_called()

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_from_contracts_fallback(self, mock_load):
        """Test fallback to known_paths when contract doesn't specify a path."""
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "prd",  # Exists in known_paths as os.path.join("artifacts", "prd.md")
                }
            ]
        }

        # Resolve path
        resolved = self.runner._resolve_artifact_path("prd")

        # Expected path from known_paths fallback
        expected_rel = os.path.join("artifacts", "prd.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))
        mock_load.assert_not_called()

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_fallback_when_artifact_not_in_contracts(self, mock_load):
        """Test fallback when artifact is not in contracts."""
        self.runner.contracts = {
            "artifacts": []
        }

        resolved = self.runner._resolve_artifact_path("prd")

        expected_rel = os.path.join("artifacts", "prd.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_dynamic_load_when_contracts_none(self, mock_load):
        """Test that contracts are loaded dynamically if self.contracts is None."""
        self.runner.contracts = None
        mock_load.return_value = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "custom_dir/{workflow_id}_doc.md"
                }
            ]
        }

        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        expected_rel = os.path.join("custom_dir", "test-wf_doc.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))
        mock_load.assert_called_once_with(self.runner.repo_root)

    @patch("workflow_runtime.load_artifact_contracts")
    def test_dynamic_load_fails_graceful_fallback(self, mock_load):
        """Test graceful fallback if dynamic load raises an exception."""
        self.runner.contracts = None
        mock_load.side_effect = Exception("File not found")

        resolved = self.runner._resolve_artifact_path("prd")

        expected_rel = os.path.join("artifacts", "prd.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))
        mock_load.assert_called_once_with(self.runner.repo_root)

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_fallback_for_workflow_orchestration_plan(self, mock_load):
        """Test fallback for workflow_orchestration_plan when contract resolution is unavailable."""
        self.runner.contracts = None
        mock_load.side_effect = Exception("Load error")

        resolved = self.runner._resolve_artifact_path("workflow_orchestration_plan")

        expected_rel = os.path.join("artifacts", "plan_test-wf.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_with_session_dir(self, mock_load):
        """Test that artifact path is scoped under session directory when set."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = None
        mock_load.return_value = {"artifacts": []}

        resolved = self.runner._resolve_artifact_path("prd")

        expected = os.path.join(session_dir, "prd.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_with_session_dir_workflow_plan(self, mock_load):
        """Test workflow_orchestration_plan path is scoped under session dir."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = None
        mock_load.return_value = {"artifacts": []}

        resolved = self.runner._resolve_artifact_path("workflow_orchestration_plan")

        expected = os.path.join(session_dir, "plan_test-wf.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_without_session_dir(self, mock_load):
        """Test that path falls back to artifacts/ when no session dir is set."""
        self.runner.contracts = None
        mock_load.return_value = {"artifacts": []}

        resolved = self.runner._resolve_artifact_path("prd")

        expected = os.path.join(self.runner.repo_root, "artifacts", "prd.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_contract_path_with_session_dir(self, mock_load):
        """Test contract-based path is also scoped under session dir."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "artifacts/custom_report.md"
                }
            ]
        }

        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        expected = os.path.join(session_dir, "custom_report.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_contract_with_template_not_scoped(self, mock_load):
        """Test contract paths with {session_id} template are NOT double-scoped."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "custom_dir/{workflow_id}/{session_id}_report.md"
                }
            ]
        }

        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        # Template paths under custom_dir (not artifacts/) should NOT be scoped
        expected_rel = os.path.join("custom_dir", "test-wf", "session-123_report.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))


if __name__ == "__main__":
    unittest.main()
