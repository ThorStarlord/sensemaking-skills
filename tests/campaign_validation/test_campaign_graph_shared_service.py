"""Regression coverage for shared graph rendering/integrity construction."""

from __future__ import annotations

import json

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _workspace(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-GRAPH-SHARED",
            mission="share one graph construction authority",
            status="active",
            current_state="initialized",
        )
    )
    return workspace


def test_graph_renderer_reports_same_clean_integrity_as_graph_integrity(tmp_path):
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    rendered = runner.invoke(
        cli,
        ["campaign", "graph", "--workspace", str(workspace), "--format", "json"],
    )
    checked = runner.invoke(
        cli,
        ["campaign", "graph-integrity", "--workspace", str(workspace), "--json"],
    )
    assert rendered.exit_code == 0, rendered.output
    assert checked.exit_code == 0, checked.output
    graph = json.loads(rendered.output)
    integrity = json.loads(checked.output)
    assert graph["integrity_valid"] is True
    assert len(graph["nodes"]) == integrity["node_count"]
    assert len(graph["edges"]) == integrity["edge_count"]
    assert graph["semantic_truth_established"] is False


def test_graph_renderer_and_integrity_reject_same_node_collision(tmp_path):
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    appended = runner.invoke(
        cli,
        [
            "campaign",
            "semantic-state-append",
            "--workspace",
            str(workspace),
            "--entry-id",
            "CMP-GRAPH-SHARED",
            "--source-skill",
            "example-skill",
            "--artifact-ref",
            "opaque.md",
            "--target-ref",
            "target:declared",
            "--json",
        ],
    )
    assert appended.exit_code == 0, appended.output

    rendered = runner.invoke(
        cli,
        ["campaign", "graph", "--workspace", str(workspace), "--format", "json"],
    )
    checked = runner.invoke(
        cli,
        ["campaign", "graph-integrity", "--workspace", str(workspace), "--json"],
    )
    assert rendered.exit_code == 3, rendered.output
    assert checked.exit_code == 3, checked.output
    graph_codes = {item["code"] for item in json.loads(rendered.output)["diagnostics"]}
    integrity_codes = {item["code"] for item in json.loads(checked.output)["diagnostics"]}
    assert "GRAPH_NODE_ID_COLLISION" in graph_codes
    assert graph_codes == integrity_codes
