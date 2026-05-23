"""Workflow orchestration runner for Sensemaking Skills.

Delegates to the legacy workflow-runtime.py for orchestration execution
while providing a modern, configurable interface. Also manages skill execution.
"""

import os
import sys
import subprocess
import shutil
import yaml
from typing import Optional, List, Dict, Any
from pathlib import Path
from .config import ConfigManager, SkillsConfig
from .paths import PathResolver
from .skills import BaseSkill, RepoSensemakerSkill, WorkflowPlannerSkill


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

    def run_skill(self, skill: BaseSkill, **kwargs) -> Dict[str, Any]:
        """Execute a skill and return results.

        Args:
            skill: BaseSkill instance to execute
            **kwargs: Arguments to pass to the skill's run method

        Returns:
            Dictionary containing skill execution results
        """
        try:
            result = skill.run(**kwargs)
            return result
        except Exception as e:
            return {
                "artifact_id": None,
                "success": False,
                "message": f"Skill execution failed: {e}",
            }

    def run_repo_sensemaker_skill(self) -> Dict[str, Any]:
        """Execute the RepoSensemakerSkill.

        Returns:
            Dictionary containing skill execution results
        """
        skill = RepoSensemakerSkill(self.config)
        return self.run_skill(skill)

    def run_workflow_planner_skill(
        self, brief_artifact_id: str = "repository_sensemaking_brief"
    ) -> Dict[str, Any]:
        """Execute the WorkflowPlannerSkill.

        Args:
            brief_artifact_id: ID of the repository sensemaking brief artifact

        Returns:
            Dictionary containing skill execution results
        """
        skill = WorkflowPlannerSkill(self.config)
        return self.run_skill(skill, brief_artifact_id=brief_artifact_id)

    def instantiate_skill(self, skill_name: str) -> Optional[BaseSkill]:
        """Instantiate a skill by name.

        Args:
            skill_name: Name of the skill class to instantiate

        Returns:
            Skill instance or None if not found
        """
        skill_map = {
            "RepoSensemakerSkill": RepoSensemakerSkill,
            "WorkflowPlannerSkill": WorkflowPlannerSkill,
        }

        skill_class = skill_map.get(skill_name)
        if not skill_class:
            return None

        return skill_class(self.config)

    def _handle_auto_invocation(self, current_workflow_id: str, parent_session: Optional[str] = None) -> int:
        """Handle automatic chaining to next workflow.

        Reads recommended_workflow_id from orchestration plan artifact and auto-invokes.
        Includes recursion guard and session passing.

        Args:
            current_workflow_id: The ID of the currently executing workflow
            parent_session: Path to the parent session directory (for chained invocation)

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Determine which artifact to read based on session
            if parent_session:
                artifact_dir = Path(parent_session)
            else:
                artifact_dir = self.path_resolver.artifacts_dir()

            # Find the orchestration plan artifact (plan_<workflow_id>.md pattern)
            plan_file = artifact_dir / f"plan_{current_workflow_id}.md"

            if not plan_file.exists():
                print(f"[ERROR] Orchestration plan not found: {plan_file}")
                return 1

            # Read and parse the orchestration plan YAML
            with open(plan_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML front matter
            if content.startswith("---"):
                _, yaml_str, _ = content.split("---", 2)
                try:
                    plan_data = yaml.safe_load(yaml_str)
                except yaml.YAMLError as e:
                    print(f"[ERROR] Failed to parse orchestration plan YAML: {e}")
                    return 1
            else:
                print(f"[ERROR] Orchestration plan missing YAML front matter: {plan_file}")
                return 1

            # Extract next workflow ID (check canonical field names per CONTEXT.md)
            next_workflow_id = (
                plan_data.get("recommended_workflow_id") or
                plan_data.get("chosen_workflow_id") or
                plan_data.get("selected_workflow")
            )

            if not next_workflow_id:
                print(f"[INFO] No next workflow recommended in plan")
                return 0

            # RECURSION GUARD: Prevent self-routing
            if next_workflow_id == current_workflow_id:
                print(f"[ERROR] RECURSION DETECTED: Workflow '{current_workflow_id}' would invoke itself.")
                print(f"[ERROR] recommended_workflow_id: {next_workflow_id}")
                return 1

            print(f"\n{'='*60}")
            print(f"AUTO-INVOCATION: Next Workflow")
            print(f"{'='*60}")
            print(f"  Current workflow: {current_workflow_id}")
            print(f"  Next workflow:    {next_workflow_id}")
            print()

            # Auto-invoke the next workflow with session passing
            session_dir = parent_session or str(artifact_dir)
            return self.run_workflow(
                next_workflow_id,
                execution_mode="yolo_execution",
                from_session=session_dir
            )

        except Exception as e:
            print(f"[ERROR] Auto-invocation failed: {e}")
            import traceback
            traceback.print_exc()
            return 1

    def _run_workflow_with_parent_session(
        self,
        workflow_id: str,
        parent_session: Path,
    ) -> int:
        """Run workflow with parent artifacts available.

        Used in manual path: diagnostic runs, user manually invokes implementation with
        --from-session. Copies parent artifacts to current session so implementation can
        access them.

        Args:
            workflow_id: The workflow to execute
            parent_session: Path to parent session directory with artifacts

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            parent_session = Path(parent_session).resolve()

            if not parent_session.exists():
                print(f"[ERROR] Parent session directory does not exist: {parent_session}")
                return 1

            # Find parent artifacts (particularly user_intent and orchestration plan)
            parent_intent = parent_session / "00-user-intent.md"
            if not parent_intent.exists():
                print(f"[ERROR] Parent user intent not found: {parent_intent}")
                return 1

            # Get or create session directory for this workflow
            session_id = parent_session.name
            current_session = self.path_resolver.session_dir(session_id)

            # Copy parent artifacts to current session
            print(f"[INFO] Copying parent artifacts from {parent_session.name}")
            for artifact_file in parent_session.glob("*.md"):
                dest = current_session / artifact_file.name
                if not dest.exists():
                    shutil.copy2(artifact_file, dest)
                    print(f"  ✓ Copied {artifact_file.name}")

            # Run workflow with parent session artifacts available
            return self.run_workflow(
                workflow_id,
                execution_mode="yolo_execution",
                from_session=str(current_session)
            )

        except Exception as e:
            print(f"[ERROR] Failed to run workflow with parent session: {e}")
            import traceback
            traceback.print_exc()
            return 1
