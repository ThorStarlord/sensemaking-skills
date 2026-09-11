"""Qualification for static, non-routing Campaign golden paths."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[2]


def test_workflow_list_is_static_discovery_not_selection() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["campaign", "workflow", "list", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert [item["id"] for item in payload["flows"]] == [
        "single-repository",
        "fresh-context",
        "transferred-campaign",
        "multi-repository",
    ]
    assert payload["flow_selected_by_tool"] is False
    assert payload["semantic_recommendation_included"] is False


def test_every_golden_path_preserves_agent_decision_gates() -> None:
    runner = CliRunner()
    for flow in (
        "single-repository",
        "fresh-context",
        "transferred-campaign",
        "multi-repository",
    ):
        result = runner.invoke(cli, ["campaign", "workflow", "show", flow, "--json"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["flow"] == flow
        assert payload["flow_selected_by_tool"] is False
        assert payload["steps_executed"] is False
        assert payload["responsibility_selected"] is False
        assert payload["capability_selected"] is False
        assert payload["authority_granted"] is False
        assert payload["semantic_truth_established"] is False
        assert any(step["decision_gate"] for step in payload["steps"])


def test_transferred_and_multi_repo_paths_expose_new_portable_surfaces() -> None:
    runner = CliRunner()
    transfer = json.loads(
        runner.invoke(cli, ["campaign", "workflow", "show", "transferred-campaign", "--json"]).output
    )
    transfer_surfaces = [item["surface"] for item in transfer["steps"]]
    assert any("bundle-inspect" in item for item in transfer_surfaces)
    assert any("target rebind" in item for item in transfer_surfaces)
    assert any("multi-target rebind" in item for item in transfer_surfaces)

    multi = json.loads(
        runner.invoke(cli, ["campaign", "workflow", "show", "multi-repository", "--json"]).output
    )
    multi_surfaces = [item["surface"] for item in multi["steps"]]
    assert "campaign multi-target relate" in multi_surfaces
    assert "campaign multi-target dependency-check" in multi_surfaces
    assert any("campaign closeout" in item for item in multi_surfaces)


def test_using_sensemaking_distribution_contains_golden_path_reference() -> None:
    text = (ROOT / "skills/using-sensemaking/references/golden-paths-v1.md").read_text(encoding="utf-8")
    assert "composition examples, not a router" in text
    assert "golden path != workflow engine" in text
    assert "campaign workflow show transferred-campaign" in text
