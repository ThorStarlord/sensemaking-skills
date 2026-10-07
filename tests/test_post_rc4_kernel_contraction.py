"""Adversarial structural regression for the post-RC4 pragmatic kernel contraction.

These checks pin executable/product-surface facts rather than historical prose.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_active_workflows_carry_no_auto_execution_metadata() -> None:
    registry = _load_yaml(
        ROOT / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml"
    )
    liveness = _load_yaml(
        ROOT / "skills" / "workflow-planner" / "references" / "workflow-liveness.yaml"
    )
    overrides = liveness.get("overrides", {})
    default = liveness.get("default_liveness", "active")
    offenders = []
    for workflow in registry["workflows"]:
        if overrides.get(workflow["id"], default) != "active":
            continue
        if any(
            key in workflow
            for key in (
                "auto_invoke_next_workflow",
                "auto_invoke_source",
                "auto_invoke_next_workflow_id",
            )
        ):
            offenders.append(workflow["id"])
    assert offenders == []


def test_product_and_architecture_wrappers_are_compatibility_only() -> None:
    liveness = _load_yaml(
        ROOT / "skills" / "workflow-planner" / "references" / "workflow-liveness.yaml"
    )
    overrides = liveness["overrides"]
    assert overrides["product-discovery-sprint"] == "compatibility_only"
    assert overrides["architectural-review-planning-workflow"] == "compatibility_only"


def test_legacy_auto_routing_apis_are_absent_from_current_runtime() -> None:
    surfaces = {
        ROOT / "scripts" / "workflow-runtime.py": (
            "_should_auto_invoke_next",
            "_surface_candidate_next_workflow",
        ),
        ROOT / "src" / "sensemaking_skills" / "runner.py": (
            "_handle_auto_invocation",
        ),
        ROOT / "src" / "sensemaking_skills" / "registry.py": (
            "has_auto_invocation",
            "get_recommended_next_workflow",
        ),
    }
    for path, forbidden in surfaces.items():
        text = path.read_text(encoding="utf-8")
        for symbol in forbidden:
            assert symbol not in text, f"{symbol} survived in {path}"


def test_yolo_is_historical_not_current_execution_mode() -> None:
    runtime_path = ROOT / "scripts" / "workflow-runtime.py"
    spec = importlib.util.spec_from_file_location("workflow_runtime_kernel_regression", runtime_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert "yolo_execution" in module.RETIRED_EXECUTION_MODES
    assert "yolo_execution" not in module.CURRENT_EXECUTION_MODES


def test_campaign_root_discloses_kernel_and_advanced_holds_secondary_surface() -> None:
    runner = CliRunner()
    root_help = runner.invoke(cli, ["campaign", "--help"])
    assert root_help.exit_code == 0, root_help.output
    for command in (
        "init",
        "ingest",
        "status",
        "validate",
        "advance",
        "defer",
        "close",
        "inspect",
        "resume-profile",
        "working-context",
        "advanced",
    ):
        assert command in root_help.output
    assert "history" not in root_help.output

    advanced_help = runner.invoke(cli, ["campaign", "advanced", "--help"])
    assert advanced_help.exit_code == 0, advanced_help.output
    assert "history" in advanced_help.output


def test_stale_generic_strategic_instances_are_archived() -> None:
    assert not (ROOT / "artifacts" / "strategic_repository_analysis.md").exists()
    assert not (ROOT / "artifacts" / "strategic_reconciliation.md").exists()
    assert not (ROOT / "artifacts" / "owner_decision_capsule.md").exists()
    assert (
        ROOT / "artifacts" / "history" / "2026-09-20-strategic-repository-analysis.md"
    ).is_file()
    assert (
        ROOT / "artifacts" / "history" / "2026-09-22-strategic-reconciliation.md"
    ).is_file()
    assert (
        ROOT / "artifacts" / "history" / "2026-09-30-owner-decision-simplify-hard.md"
    ).is_file()
