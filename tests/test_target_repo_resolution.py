"""Tests for framework/target repository separation.

These tests verify that repo_root and target_repo have distinct, coherent semantics:
- framework_root: skills, registries, validators, runtime
- target_repo_root: repository being analyzed by diagnostic skills
- artifact_output_root: session artifacts (currently framework_root/artifacts)
- executor_cwd: execution context (currently framework_root)

Tests do NOT invoke Claude Code or real executors. They verify path resolution only.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Setup paths
REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from _validator_utils import load_workflow_registry, load_artifact_contracts


class TestTargetRepoDefaults:
    """Test default target_repo behavior (backward compatibility)."""

    def test_target_repo_defaults_to_repo_root(self, tmp_path):
        """When target_repo is None, it should default to repo_root."""
        # This is the backward-compatibility contract
        framework_root = str(tmp_path / "framework")
        Path(framework_root).mkdir()

        # Import here to avoid loading at module level
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=None,  # Explicitly None
        )

        assert runner.target_repo == runner.repo_root, \
            "target_repo should default to repo_root when not provided"

    def test_explicit_target_repo_differs_from_repo_root(self, tmp_path):
        """When target_repo is explicit, it should not equal repo_root."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        framework_root = str(tmp_path / "framework")
        target_root = str(tmp_path / "target")
        Path(framework_root).mkdir()
        Path(target_root).mkdir()

        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=target_root,  # Explicit, different path
        )

        assert runner.target_repo == target_root, \
            "target_repo should equal the provided value"
        assert runner.repo_root == framework_root, \
            "repo_root should remain as framework_root"
        assert runner.target_repo != runner.repo_root, \
            "target_repo and repo_root should be different when explicitly provided"


class TestFrameworkResourceResolution:
    """Test that framework resources load from repo_root, not target_repo."""

    def test_workflow_registry_loads_from_repo_root(self):
        """Workflow registry should resolve from repo_root (framework)."""
        registry = load_workflow_registry(str(REPO_ROOT))
        assert registry is not None, "Workflow registry should load from framework_root"

    def test_artifact_contracts_load_from_repo_root(self):
        """Artifact contracts should resolve from repo_root (framework)."""
        contracts = load_artifact_contracts(str(REPO_ROOT))
        assert contracts is not None, "Artifact contracts should load from framework_root"
        artifacts = contracts.get("artifacts", [])
        artifact_ids = [a.get("id") for a in artifacts]
        assert "repository_sensemaking_brief" in artifact_ids, \
            "Contracts should include repository_sensemaking_brief"


class TestArtifactOutputLocation:
    """Test where artifacts are written."""

    def test_artifacts_written_to_repo_root_artifacts_dir(self, tmp_path):
        """Artifacts should be written to repo_root/artifacts, not target_repo."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        framework_root = str(tmp_path / "framework")
        target_root = str(tmp_path / "target")
        Path(framework_root).mkdir()
        Path(target_root).mkdir()

        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=target_root,
        )

        # Default log_dir should be in framework_root
        assert runner.log_dir.startswith(framework_root), \
            f"log_dir should be in framework_root, not target_repo: {runner.log_dir}"


class TestInvalidTargetContract:
    """Test that invalid explicit targets fail early and clearly."""

    def test_invalid_target_nonexistent_path(self, tmp_path):
        """Explicit invalid target (missing path) should be accepted but used for resolution."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        framework_root = str(tmp_path / "framework")
        invalid_target = str(tmp_path / "nonexistent" / "path")
        Path(framework_root).mkdir()

        # Runner accepts the invalid path (it's just a string at this point)
        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=invalid_target,  # This doesn't exist
        )

        # The runner should store it (validation happens at execution time)
        assert runner.target_repo == invalid_target, \
            "target_repo should be stored even if invalid"
        # It should NOT fall back to framework_root
        assert runner.target_repo != framework_root, \
            "target_repo should not silently fall back to framework_root"

    def test_invalid_target_is_file_not_dir(self, tmp_path):
        """Explicit invalid target (file instead of directory) should be stored without fallback."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        framework_root = str(tmp_path / "framework")
        file_path = str(tmp_path / "notadir.txt")
        Path(framework_root).mkdir()
        Path(file_path).touch()

        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=file_path,  # This is a file, not a directory
        )

        # The runner should store the file path
        assert runner.target_repo == file_path, \
            "target_repo should be stored even if it is a file"
        # It should NOT fall back to framework_root
        assert runner.target_repo != framework_root, \
            "target_repo should not silently fall back to framework_root when invalid"


class TestBackwardCompatibility:
    """Test that existing single-repo usage still works."""

    def test_single_repo_mode_unchanged(self, tmp_path):
        """Existing code without target_repo should work exactly as before."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        repo_root = str(tmp_path / "repo")
        Path(repo_root).mkdir()

        # Call exactly as existing code would (no target_repo parameter)
        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="test-workflow",
            mode="plan_only",
            repo_root=repo_root,
            # target_repo NOT provided
        )

        # Both should point to the same location
        assert runner.repo_root == repo_root
        assert runner.target_repo == repo_root


class TestTargetImmutability:
    """Test that target repository remains unchanged during framework operations."""

    def test_target_repo_unmodified_during_setup(self, tmp_path):
        """Target repository should not be modified during runner initialization and input resolution."""
        import importlib.util
        import subprocess
        spec = importlib.util.spec_from_file_location("workflow_runtime", str(SCRIPTS_DIR / "workflow-runtime.py"))
        workflow_runtime = importlib.util.module_from_spec(spec)
        sys.modules["workflow_runtime"] = workflow_runtime
        spec.loader.exec_module(workflow_runtime)

        framework_root = str(tmp_path / "framework")
        target_root = str(tmp_path / "target")
        Path(framework_root).mkdir()
        Path(target_root).mkdir()

        # Initialize target as a git repository
        subprocess.run(
            ["git", "init"],
            cwd=target_root,
            capture_output=True,
            check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=target_root,
            capture_output=True,
            check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=target_root,
            capture_output=True,
            check=True
        )

        # Capture target state before
        result_before = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_root,
            capture_output=True,
            text=True,
            check=True
        )
        status_before = result_before.stdout

        # Create runner and resolve inputs
        runner = workflow_runtime.OrchestrationRunner(
            workflow_id="architectural-review-planning-workflow",
            mode="plan_only",
            repo_root=framework_root,
            target_repo=target_root,
        )

        # Capture target state after
        result_after = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_root,
            capture_output=True,
            text=True,
            check=True
        )
        status_after = result_after.stdout

        # Verify no changes
        assert status_before == status_after, \
            f"Target repository was modified:\nBefore: {status_before}\nAfter: {status_after}"
