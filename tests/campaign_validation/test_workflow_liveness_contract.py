"""ADR 0027 workflow catalog/liveness regression contract (issue #263)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from _validator_utils import load_workflow_catalog, load_workflow_registry  # noqa: E402
from sensemaking_skills.registry import WorkflowRegistry  # noqa: E402


COMPATIBILITY_ONLY = {
    "product-to-issues",
    "product-autonomous-sprint",
    "experimental-autonomous-sprint",
    "implementation-workflow",
    "product-implementation-workflow",
    "ui-diagnostic-workflow",
    "ui-implementation-workflow",
    "architecture-implementation-workflow",
}


def _by_id(registry: dict) -> dict[str, dict]:
    return {w["id"]: w for w in registry.get("workflows", [])}


def _load_script_planner():
    path = SCRIPTS / "workflow-planner.py"
    spec = importlib.util.spec_from_file_location("workflow_planner_script", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_catalog_preserves_compatibility_workflow_definitions() -> None:
    catalog = load_workflow_catalog(str(ROOT))
    assert catalog is not None
    workflows = _by_id(catalog)

    assert COMPATIBILITY_ONLY <= set(workflows)
    for workflow_id in COMPATIBILITY_ONLY:
        workflow = workflows[workflow_id]
        assert workflow["liveness"] == "compatibility_only"
        assert workflow.get("steps"), f"catalog history lost for {workflow_id}"
        assert workflow.get("allowed_execution_modes"), (
            f"catalog execution metadata lost for {workflow_id}"
        )


def test_operational_view_fail_closes_compatibility_workflows() -> None:
    operational = load_workflow_registry(str(ROOT))
    assert operational is not None
    workflows = _by_id(operational)

    # Stable IDs remain recognizable, but current execution surfaces are empty.
    assert COMPATIBILITY_ONLY <= set(workflows)
    for workflow_id in COMPATIBILITY_ONLY:
        workflow = workflows[workflow_id]
        assert workflow["liveness"] == "compatibility_only"
        assert workflow["allowed_execution_modes"] == []
        assert workflow["steps"] == []

    active = workflows["docs-contract-reconciliation"]
    assert active["liveness"] == "active"
    assert active["allowed_execution_modes"]
    assert active["steps"]


def test_package_registry_separates_catalog_from_selectable_workflows(tmp_path: Path) -> None:
    registry = WorkflowRegistry(tmp_path)

    catalog_ids = set(registry.list_workflows())
    selectable_ids = set(registry.list_selectable_workflows())

    shipped_compat = COMPATIBILITY_ONLY & catalog_ids
    assert shipped_compat, "expected packaged catalog to include affected workflow IDs"
    assert shipped_compat.isdisjoint(selectable_ids)

    for workflow_id in shipped_compat:
        assert registry.get_workflow(workflow_id) is not None
        assert registry.get_workflow_liveness(workflow_id) == "compatibility_only"
        assert registry.get_selectable_workflow(workflow_id) is None

    assert registry.get_workflow_liveness("docs-contract-reconciliation") == "active"
    assert registry.get_selectable_workflow("docs-contract-reconciliation") is not None


def test_external_custom_workflow_defaults_active_without_liveness_migration(tmp_path: Path) -> None:
    registry = WorkflowRegistry(
        tmp_path,
        user_registry={
            "workflows": [
                {
                    "id": "custom-current-workflow",
                    "allowed_execution_modes": ["plan_only"],
                    "steps": [{"id": 1, "skill": "handoff"}],
                }
            ]
        },
    )

    assert registry.get_workflow_liveness("custom-current-workflow") == "active"
    assert "custom-current-workflow" in registry.list_selectable_workflows()


def test_user_can_explicitly_reactivate_an_overridden_compatibility_id(tmp_path: Path) -> None:
    registry = WorkflowRegistry(
        tmp_path,
        user_registry={
            "workflows": [
                {
                    "id": "implementation-workflow",
                    "allowed_execution_modes": ["plan_only"],
                    "steps": [{"id": 1, "skill": "handoff"}],
                }
            ],
            "workflow_liveness": {
                "default_liveness": "active",
                "overrides": {"implementation-workflow": "active"},
            },
        },
    )

    assert registry.get_workflow_liveness("implementation-workflow") == "active"
    assert registry.get_selectable_workflow("implementation-workflow") is not None


def test_deterministic_planner_refuses_inactive_former_default_without_substitution(
    tmp_path: Path,
) -> None:
    planner = _load_script_planner()
    brief = tmp_path / "brief.md"
    brief.write_text(
        "# Brief\n\n"
        "## 13. Machine-readable handoff\n"
        "```yaml\n"
        "primary_fog_type: product_fog\n"
        "recommended_workflow_id: product-implementation-workflow\n"
        "escalation_recommended: false\n"
        "```\n",
        encoding="utf-8",
    )

    result = planner.plan_workflow(str(brief), str(ROOT))
    assert result.startswith("ERROR:")
    assert "not currently active under ADR 0027" in result
    assert "No replacement route is ratified" in result


def test_deterministic_planner_still_plans_active_default(tmp_path: Path) -> None:
    planner = _load_script_planner()
    brief = tmp_path / "brief.md"
    brief.write_text(
        "# Brief\n\n"
        "## 13. Machine-readable handoff\n"
        "```yaml\n"
        "primary_fog_type: docs_fog\n"
        "recommended_workflow_id: docs-implementation-workflow\n"
        "escalation_recommended: false\n"
        "```\n",
        encoding="utf-8",
    )

    result = planner.plan_workflow(str(brief), str(ROOT))
    assert not result.startswith("ERROR:")
    assert "chosen_workflow_id: docs-implementation-workflow" in result
