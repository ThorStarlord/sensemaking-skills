"""Campaign Operability v1 repository/hermetic qualification."""

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
            campaign_id="CMP-OPERABILITY",
            mission="inspect mechanical operability",
            status="active",
            current_state="initialized",
        )
    )
    return workspace


def test_campaign_doctor_reports_clean_without_repair_or_semantic_advice(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "doctor", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_DOCTOR_CLEAN"
    assert payload["findings"] == []
    assert payload["semantic_recommendation_included"] is False
    assert payload["automatic_repair_performed"] is False


def test_campaign_doctor_maps_preflight_failure_to_inspection_path(tmp_path):
    workspace = _workspace(tmp_path)
    (workspace / "semantic-state.jsonl").write_text("{broken-json}\n", encoding="utf-8")
    result = CliRunner().invoke(
        cli,
        ["campaign", "doctor", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_DOCTOR_FINDINGS"
    assert payload["automatic_repair_performed"] is False
    finding = payload["findings"][0]
    assert finding["diagnostic_class"] == "SEMANTIC_REFERENCE_INTEGRITY_INVALID"
    assert "campaign semantic-state" in finding["suggested_inspection"]
    assert "SEMANTIC_STATE_INVALID_JSON" in finding["diagnostics"]


def test_local_provenance_markdown_is_explicitly_not_published(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "provenance", "--workspace", str(workspace), "--format", "markdown"],
    )
    assert result.exit_code == 0, result.output
    assert "### Sensemaking Campaign Provenance" in result.output
    assert "`CMP-OPERABILITY`" in result.output
    assert "has not been published to GitHub" in result.output
    assert "semantic correctness" in result.output


def test_local_provenance_json_preserves_publication_boundary(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "provenance", "--workspace", str(workspace), "--format", "json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_PROVENANCE"
    assert payload["published"] is False
    assert payload["semantic_truth_established"] is False
    assert payload["preflight_ready"] is True


def test_graph_integrity_passes_for_clean_campaign(tmp_path):
    workspace = _workspace(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "graph-integrity", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_GRAPH_INTEGRITY_VALID"
    assert payload["node_count"] == 1
    assert payload["semantic_truth_established"] is False


def test_graph_integrity_rejects_cross_namespace_node_collision(tmp_path):
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
            "CMP-OPERABILITY",
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

    result = runner.invoke(
        cli,
        ["campaign", "graph-integrity", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    codes = {item["code"] for item in payload["diagnostics"]}
    assert "GRAPH_NODE_ID_COLLISION" in codes
    assert payload["semantic_truth_established"] is False
