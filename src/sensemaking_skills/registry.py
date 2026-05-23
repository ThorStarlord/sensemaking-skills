"""Workflow registry management for Sensemaking Skills.

Provides injectable workflow registry system that loads package defaults
and allows external repo overrides.
"""

import yaml
from typing import Optional, Dict, Any, List
from pathlib import Path


class WorkflowRegistry:
    """Manages workflow definitions with support for package defaults and user overrides.

    The registry loads default workflows from package defaults and merges in
    user-provided overrides from the target repository.
    """

    def __init__(self, target_repo: Path, user_registry: Optional[Dict[str, Any]] = None):
        """Initialize the workflow registry.

        Args:
            target_repo: Path to the target repository
            user_registry: Optional dictionary of workflow definitions to merge with defaults.
                          If provided, takes precedence over file-based registry.
        """
        self.target_repo = Path(target_repo)
        self._workflows: Dict[str, Any] = {}

        # Load package defaults first
        self._load_package_defaults()

        # Load user-provided registry if specified
        if user_registry:
            self._merge_workflows(user_registry.get("workflows", []))
        else:
            # Try to load user registry from target repo
            self._load_user_registry()

    def _load_package_defaults(self) -> None:
        """Load default workflow registry from package.

        The defaults are packaged with the library at:
        src/sensemaking_skills/defaults/workflow-registry.yaml
        """
        # Locate the package defaults
        package_root = Path(__file__).parent
        defaults_file = package_root / "defaults" / "workflow-registry.yaml"

        if defaults_file.exists():
            try:
                with open(defaults_file, "r") as f:
                    data = yaml.safe_load(f) or {}
                    self._merge_workflows(data.get("workflows", []))
            except (yaml.YAMLError, IOError) as e:
                raise RuntimeError(
                    f"Failed to load default workflow registry from {defaults_file}: {e}"
                )
        else:
            raise FileNotFoundError(
                f"Package default workflow registry not found at {defaults_file}"
            )

    def _load_user_registry(self) -> None:
        """Load user-provided workflow registry from target repository.

        Looks for workflow-registry.yaml in standard locations within the target repo.
        """
        candidates = [
            self.target_repo / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml",
            self.target_repo / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml",
            self.target_repo / ".sensemaking" / "workflow-registry.yaml",
        ]

        for candidate in candidates:
            if candidate.exists():
                try:
                    with open(candidate, "r") as f:
                        data = yaml.safe_load(f) or {}
                        self._merge_workflows(data.get("workflows", []))
                    return
                except (yaml.YAMLError, IOError) as e:
                    raise RuntimeError(
                        f"Failed to load user workflow registry from {candidate}: {e}"
                    )

        # User registry is optional; if not found, we use defaults only

    def _merge_workflows(self, workflows: List[Dict[str, Any]]) -> None:
        """Merge workflow definitions into the registry.

        User workflows override package defaults with the same ID.

        Args:
            workflows: List of workflow definitions
        """
        for workflow in workflows:
            workflow_id = workflow.get("id")
            if workflow_id:
                self._workflows[workflow_id] = workflow

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get a workflow definition by ID.

        Args:
            workflow_id: The workflow ID

        Returns:
            Workflow definition dictionary or None if not found
        """
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[str]:
        """List all registered workflow IDs.

        Returns:
            List of workflow IDs sorted alphabetically
        """
        return sorted(self._workflows.keys())

    def list_workflow_details(self) -> List[Dict[str, Any]]:
        """List all workflows with their details.

        Returns:
            List of workflow definitions
        """
        return [
            self._workflows[wid] for wid in sorted(self._workflows.keys())
        ]

    def has_auto_invocation(self, workflow_id: str) -> bool:
        """Check if a workflow has auto-invocation enabled.

        Args:
            workflow_id: The workflow ID

        Returns:
            True if workflow has auto_invoke_next_workflow set to True
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return False
        return workflow.get("auto_invoke_next_workflow", False)

    def get_recommended_next_workflow(self, workflow_id: str) -> Optional[str]:
        """Get the recommended next workflow for auto-invocation.

        Args:
            workflow_id: The workflow ID

        Returns:
            The recommended next workflow ID, or None if not specified
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return None

        # Check for explicit next workflow ID first
        if "auto_invoke_next_workflow_id" in workflow:
            return workflow["auto_invoke_next_workflow_id"]

        # Check for source field (like workflow_orchestration_plan.recommended_workflow_id)
        auto_invoke_source = workflow.get("auto_invoke_source")
        if auto_invoke_source:
            # For now, just return the source path as documentation
            # The actual resolution will happen at runtime when the artifact is available
            return None

        return None

    def get_all_workflows(self) -> Dict[str, Any]:
        """Get all workflow definitions.

        Returns:
            Dictionary mapping workflow IDs to their definitions
        """
        return self._workflows.copy()

    def workflow_count(self) -> int:
        """Get the total number of registered workflows.

        Returns:
            Number of workflows
        """
        return len(self._workflows)
