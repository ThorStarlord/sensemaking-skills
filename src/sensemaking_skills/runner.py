"""Workflow orchestration runner for Sensemaking Skills.

Delegates to the legacy workflow-runtime.py for orchestration execution
while providing a modern, configurable interface.
"""

import os
import sys
import subprocess
from typing import Optional, List
from pathlib import Path
from .config import ConfigManager, SkillsConfig
from .paths import PathResolver


class SkillsOrchestrator:
    """Main orchestration engine for running skill workflows.

    Accepts configuration and delegates workflow execution to the
    production-grade orchestration runner (scripts/workflow-runtime.py).
    """

    def __init__(self, config: Optional[SkillsConfig] = None, config_path: Optional[str] = None):
        """Initialize the orchestrator.

        Args:
            config: SkillsConfig instance (if provided, config_path is ignored)
            config_path: Path to configuration file
        """
        if config:
            self.config = config
        else:
            manager = ConfigManager(config_path)
            self.config = manager.config

        self.path_resolver = PathResolver(self.config)
        self._runtime_script = self._locate_runtime_script()

    def __repr__(self) -> str:
        """Return string representation."""
        return f"SkillsOrchestrator(project_root={self.config.project_root})"

    def _locate_runtime_script(self) -> Path:
        """Locate the workflow-runtime.py script.

        Returns:
            Path to workflow-runtime.py script

        Raises:
            FileNotFoundError: If workflow-runtime.py cannot be found
        """
        project_root = Path(self.config.project_root)
        candidates = [
            project_root / "scripts" / "workflow-runtime.py",
            Path(__file__).parent.parent.parent / "scripts" / "workflow-runtime.py",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()

        raise FileNotFoundError(
            "Could not locate workflow-runtime.py. Searched: " + ", ".join(str(c) for c in candidates)
        )

    def run_workflow(
        self,
        workflow_id: str,
        execution_mode: str = "yolo_execution",
        from_session: Optional[str] = None,
        **kwargs
    ) -> int:
        """Execute a workflow using the production orchestration runner.

        Args:
            workflow_id: ID of the workflow to execute
            execution_mode: Execution mode (plan_only, guided_execution, autonomous_execution, yolo_execution)
            from_session: Path to artifact session directory from a prior workflow run
            **kwargs: Additional arguments to pass to the runner (plan_out, log_dir, etc.)

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        project_root = str(self.config.project_root)
        cmd = [
            sys.executable,
            str(self._runtime_script),
            "--workflow", workflow_id,
            "--mode", execution_mode,
            "--repo-root", project_root,
        ]

        if from_session:
            cmd.extend(["--from-session", from_session])

        # Add optional arguments
        if kwargs.get("plan_out"):
            cmd.extend(["--plan-out", kwargs["plan_out"]])
        if kwargs.get("log_dir"):
            cmd.extend(["--log-dir", kwargs["log_dir"]])
        if kwargs.get("gate_decision"):
            cmd.extend(["--gate-decision", kwargs["gate_decision"]])
        if kwargs.get("executor"):
            cmd.extend(["--executor", kwargs["executor"]])
        if kwargs.get("use_fixtures"):
            cmd.append("--use-fixtures")
        if kwargs.get("resume"):
            cmd.append("--resume")

        # Run the workflow
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode

    def get_artifact_path(self, artifact_id: str) -> Path:
        """Get the path to a specific artifact.

        Args:
            artifact_id: The artifact identifier

        Returns:
            Path to the artifact file
        """
        return self.path_resolver.artifact_path(artifact_id)

    def list_workflows(self) -> int:
        """List all registered workflows.

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        project_root = str(self.config.project_root)
        cmd = [
            sys.executable,
            str(self._runtime_script),
            "--list-workflows",
            "--repo-root", project_root,
        ]

        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode

    def _handle_auto_invocation(self, parent_session: Optional[str] = None) -> int:
        """Handle auto-invocation and chaining logic.

        This is a stub for Task 7 (Implement Auto-Invocation with Recursion Guard).

        Args:
            parent_session: Path to the parent session directory for recursive invocation

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        raise NotImplementedError(
            "Auto-invocation will be implemented in Task 7 (Implement Auto-Invocation with Recursion Guard)"
        )
