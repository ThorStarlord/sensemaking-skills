"""Campaign observability/portability contracts."""

from __future__ import annotations

import json
import zipfile
from dataclasses import replace

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState, TransitionRecord
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.campaigns.bundle import CampaignBundleService
from sensemaking_skills.cli import cli


def _campaign(tmp_path):
    workspace = tmp_path / "campaign"
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id="CMP-OBS",
            mission="preserve reconstructible campaign state",
            status="active",
            current_state="initialized",
            established_facts=("Fact supplied by the agent",),
        )
    )
    current = service.resume().state
    service.record_transition(
        new_state=replace(current, current_state="review"),
        transition=TransitionRecord(
            id="T1",
            from_state="initialized",
            to_state="review",
            evidence=(),
            decision="agent-authored move to review",
            authority=None,
        ),
    )
    current = service.resume().state
    service.record_transition(
        new_state=replace(current, current_state="verify"),
        transition=TransitionRecord(
            id="T2",
            from_state="review",
            to_state="verify",
            evidence=(),
            decision="agent-authored move to verify",
            authority=None,
        ),
    )
    return workspace


def test_resume_context_is_deterministic_projection_not_recommendation(tmp_path):
    workspace = _campaign(tmp_path)
    result = CliRunner().invoke(
        cli,
        ["campaign", "resume-context", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_RESUME_CONTEXT"
    assert payload["current_state"] == "verify"
    assert payload["recent_transitions"][-1]["id"] == "T2"
    assert payload["semantic_recommendation_included"] is False
    assert "next warranted" not in result.output.lower()


def test_inspect_explain_diff_replay_and_graph_are_provenance_only(tmp_path):
    workspace = _campaign(tmp_path)
    runner = CliRunner()

    inspect = runner.invoke(cli, ["campaign", "inspect", "--workspace", str(workspace), "--json"])
    assert inspect.exit_code == 0, inspect.output
    inspected = json.loads(inspect.output)
    assert inspected["semantic_truth_established"] is False
    assert [item["id"] for item in inspected["transitions"]] == ["T1", "T2"]

    explain = runner.invoke(
        cli,
        ["campaign", "explain", "--workspace", str(workspace), "--ref", "T1", "--json"],
    )
    assert explain.exit_code == 0, explain.output
    assert json.loads(explain.output)["matches"][0]["kind"] == "transition"

    diff = runner.invoke(
        cli,
        [
            "campaign",
            "diff",
            "--workspace",
            str(workspace),
            "--from-transition",
            "T1",
            "--to-transition",
            "T2",
            "--json",
        ],
    )
    assert diff.exit_code == 0, diff.output
    assert "from_state" in json.loads(diff.output)["changed_fields"]

    replay = runner.invoke(
        cli,
        ["campaign", "replay", "--workspace", str(workspace), "--at-transition", "T1", "--json"],
    )
    assert replay.exit_code == 0, replay.output
    replay_payload = json.loads(replay.output)
    assert replay_payload["state_label_at_cursor"] == "review"
    assert replay_payload["historic_full_state_reconstructed"] is False

    graph = runner.invoke(
        cli,
        ["campaign", "graph", "--workspace", str(workspace), "--format", "json"],
    )
    assert graph.exit_code == 0, graph.output
    graph_payload = json.loads(graph.output)
    assert graph_payload["semantic_truth_established"] is False
    assert any(edge["relation"] == "followed_by" for edge in graph_payload["edges"])


def test_campaign_bundle_roundtrip_preserves_exact_workspace_bytes(tmp_path):
    workspace = _campaign(tmp_path)
    bundle = tmp_path / "campaign.sensemaking.zip"
    exported = CampaignBundleService(workspace).export(bundle)
    verification = CampaignBundleService.verify(exported)
    assert verification.valid, verification.diagnostics
    assert verification.semantic_truth_established is False

    imported = tmp_path / "imported"
    CampaignBundleService.import_bundle(bundle, imported)
    source_files = {
        path.relative_to(workspace).as_posix(): path.read_bytes()
        for path in workspace.rglob("*")
        if path.is_file()
    }
    imported_files = {
        path.relative_to(imported).as_posix(): path.read_bytes()
        for path in imported.rglob("*")
        if path.is_file()
    }
    assert imported_files == source_files
    assert CampaignService(imported).validate().valid


def test_campaign_bundle_rejects_path_traversal(tmp_path):
    bundle = tmp_path / "malicious.zip"
    manifest = {
        "format": "sensemaking_campaign_bundle",
        "format_version": 1,
        "files": [],
        "semantic_truth_established": False,
    }
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("bundle-manifest.json", json.dumps(manifest))
        archive.writestr("../escape.txt", "bad")

    result = CampaignBundleService.verify(bundle)
    assert not result.valid
    assert "BUNDLE_UNSAFE_MEMBER" in {item.code for item in result.diagnostics}


def test_bundle_cli_verify_reports_integrity_not_semantic_truth(tmp_path):
    workspace = _campaign(tmp_path)
    bundle = tmp_path / "campaign.zip"
    export = CliRunner().invoke(
        cli,
        [
            "campaign",
            "bundle-export",
            "--workspace",
            str(workspace),
            "--output",
            str(bundle),
            "--json",
        ],
    )
    assert export.exit_code == 0, export.output
    verify = CliRunner().invoke(
        cli,
        ["campaign", "bundle-verify", "--bundle", str(bundle), "--json"],
    )
    assert verify.exit_code == 0, verify.output
    payload = json.loads(verify.output)
    assert payload["code"] == "CAMPAIGN_BUNDLE_VALID"
    assert payload["semantic_truth_established"] is False
