"""Workflow registry management for Sensemaking Skills.

Provides injectable workflow registry system that loads package defaults
and allows external repo overrides.
"""

import yaml
from typing import Optional, Dict, Any, List
from pathlib import Path


ACTIVE = "active"
COMPATIBILITY_ONLY = "compatibility_only"
ALLOWED_LIVENESS = {ACTIVE, COMPATIBILITY_ONLY}


class WorkflowRegistry:
    """Manage workflow catalog identity separately from current liveness.

    The registry loads default workflows from package defaults and merges in
    user-provided overrides from the target repository. Registry membership is
    the durable catalog view; ADR 0027 liveness decides whether a workflow is
    currently selectable.
    """

    def __init__(self, target_repo: Path, user_registry: Optional[Dict[str, Any]] = None):
        """Initialize the workflow registry.

        Args:
            target_repo: Path to the target repository
            user_registry: Optional dictionary of workflow definitions to merge with defaults.
                          If provided, takes precedence over file-based registry. An optional
                          ``workflow_liveness`` mapping may use the same overlay shape as
                          workflow-liveness.yaml.
        """
        self.target_repo = Path(target_repo)
        self._workflows: Dict[str, Any] = {}
        self._default_liveness: str = ACTIVE
        self._liveness_overrides: Dict[str, str] = {}

        # Package liveness is loaded before definitions so an external override
        # of a compatibility ID remains compatibility-only unless the target
        # explicitly reclassifies it.
        self._load_package_liveness()
        self._load_package_defaults()

        # Load user-provided registry if specified
        if user_registry:
            self._merge_workflows(user_registry.get("workflows", []))
            self._merge_liveness(user_registry.get("workflow_liveness", {}))
        else:
            # Try to load user registry from target repo
            self._load_user_registry()

    def _load_liveness_file(self, path: Path) -> Dict[str, Any]:
        """Load one liveness overlay. Missing files are an empty override."""
        if not path.exists():
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except (yaml.YAMLError, IOError) as e:
            raise RuntimeError(f"Failed to load workflow liveness from {path}: {e}")
        if not isinstance(data, dict):
            raise RuntimeError(f"Workflow liveness overlay must be a mapping: {path}")
        return data

    def _merge_liveness(self, overlay: Dict[str, Any]) -> None:
        """Merge liveness declarations, preserving fail-closed unknown values."""
        if not overlay:
            return
        if "default_liveness" in overlay:
            self._default_liveness = overlay["default_liveness"]
        overrides = overlay.get("overrides", {})
        if overrides is None:
            return
        if not isinstance(overrides, dict):
            raise RuntimeError("workflow liveness 'overrides' must be a mapping")
        for workflow_id, liveness in overrides.items():
            self._liveness_overrides[str(workflow_id)] = liveness

    def _load_package_liveness(self) -> None:
        """Load packaged ADR-0027 liveness defaults."""
        package_root = Path(__file__).parent
        liveness_file = package_root / "defaults" / "workflow-liveness.yaml"
        self._merge_liveness(self._load_liveness_file(liveness_file))

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
                with open(defaults_file, "r", encoding="utf-8") as f:
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
        If the selected registry has a sibling ``workflow-liveness.yaml``, that
        overlay is applied after the package defaults.
        """
        candidates = [
            self.target_repo / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml",
            self.target_repo / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml",
            self.target_repo / ".sensemaking" / "workflow-registry.yaml",
        ]

        for candidate in candidates:
            if candidate.exists():
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                        self._merge_workflows(data.get("workflows", []))
                    self._merge_liveness(
                        self._load_liveness_file(candidate.parent / "workflow-liveness.yaml")
                    )
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
        """Get a catalog workflow definition by ID, regardless of liveness."""
        return self._workflows.get(workflow_id)

    def get_workflow_liveness(self, workflow_id: str) -> Optional[str]:
        """Return effective liveness for a registered workflow, else None."""
        if workflow_id not in self._workflows:
            return None
        return self._liveness_overrides.get(workflow_id, self._default_liveness)

    def is_workflow_selectable(self, workflow_id: str) -> bool:
        """True only when a registered workflow is currently active."""
        return self.get_workflow_liveness(workflow_id) == ACTIVE

    def get_selectable_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Return a workflow only when it is currently active/selectable."""
        if not self.is_workflow_selectable(workflow_id):
            return None
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[str]:
        """List all registered catalog workflow IDs."""
        return sorted(self._workflows.keys())

    def list_selectable_workflows(self) -> List[str]:
        """List current active workflow IDs only."""
        return sorted(
            workflow_id
            for workflow_id in self._workflows
            if self.is_workflow_selectable(workflow_id)
        )

    def list_workflow_details(self) -> List[Dict[str, Any]]:
        """List all catalog workflows with effective liveness annotations."""
        details: List[Dict[str, Any]] = []
        for workflow_id in sorted(self._workflows.keys()):
            item = dict(self._workflows[workflow_id])
            item["liveness"] = self.get_workflow_liveness(workflow_id)
            details.append(item)
        return details

    def list_selectable_workflow_details(self) -> List[Dict[str, Any]]:
        """List active workflows with liveness annotations."""
        return [
            item for item in self.list_workflow_details()
            if item.get("liveness") == ACTIVE
        ]

    def has_auto_invocation(self, workflow_id: str) -> bool:
        """Check current auto-invocation metadata for an active workflow.

        Compatibility-only workflows never participate in current chaining.
        """
        workflow = self.get_selectable_workflow(workflow_id)
        if not workflow:
            return False
        return workflow.get("auto_invoke_next_workflow", False)

    def get_recommended_next_workflow(self, workflow_id: str) -> Optional[str]:
        """Get a current selectable next-workflow candidate.

        ADR 0026 still governs execution authority. ADR 0027 additionally
        prevents compatibility-only source or target workflows from appearing
        as current chaining candidates.
        """
        workflow = self.get_selectable_workflow(workflow_id)
        if not workflow:
            return None

        # Check for explicit next workflow ID first
        if "auto_invoke_next_workflow_id" in workflow:
            next_id = workflow["auto_invoke_next_workflow_id"]
            return next_id if self.is_workflow_selectable(next_id) else None

        # Check for source field (like workflow_orchestration_plan.recommended_workflow_id)
        auto_invoke_source = workflow.get("auto_invoke_source")
        if auto_invoke_source:
            # The actual resolution happens at runtime when the artifact is
            # available; this method does not infer a current target.
            return None

        return None

    def get_all_workflows(self) -> Dict[str, Any]:
        """Get all catalog workflow definitions."""
        return self._workflows.copy()

    def get_all_selectable_workflows(self) -> Dict[str, Any]:
        """Get current active workflow definitions only."""
        return {
            workflow_id: workflow
            for workflow_id, workflow in self._workflows.items()
            if self.is_workflow_selectable(workflow_id)
        }

    def workflow_count(self) -> int:
        """Get the total number of registered catalog workflows."""
        return len(self._workflows)

    def selectable_workflow_count(self) -> int:
        """Get the number of currently active workflows."""
        return len(self.list_selectable_workflows())
