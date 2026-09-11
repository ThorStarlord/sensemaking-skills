"""Repository/hermetic qualification for Campaign usability/composition v1."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility, Uncertainty
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.campaigns.bundle import CampaignBundleService
from sensemaking_skills.campaigns.uncertainty_history import UncertaintyHistoryService
from sensemaking_skills.cli import cli


def _workspace(tmp_path: Path, name: str = "campaign", *, responsibility: bool = False, uncertainty: bool = False) -> Path:
    workspace = tmp_path / name
    active_responsibility = None
    authority = None
    if responsibility:
        active_responsibility = Responsibility(
            id="R-1",
            statement="diagnose repository before implementation",
            trigger_evidence=(),
            decision_blocked="which bounded responsibility is warranted",
            scope="repository",
            authority=Authority.AUTHORIZED_AUTONOMOUSLY,
            success_conditions=("diagnosis returned",),
        )
        authority = Authority.AUTHORIZED_AUTONOMOUSLY
    active_uncertainty = None
    if uncertainty:
        active_uncertainty = Uncertainty(
            id="U-1",
            question="Which fact changes the decision?",
            consequences={"decision": "responsibility may change"},
        )
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id=f"CMP-{name.upper()}",
            mission="qualify usability composition",
            status="active",
            current_state="inspect",
            active_responsibility=active_responsibility,
            active_uncertainty=active_uncertainty,
            authority=authority,
            established_facts=("f1", "f2", "f3"),
            resolved_questions=("q1", "q2"),
        )
    )
    return workspace


def test_resume_profile_v2_progressive_disclosure_and_bounding(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    runner = CliRunner()
    minimal = runner.invoke(cli, ["campaign", "resume-profile", "--workspace", str(workspace), "--profile", "minimal", "--json"])
    assert minimal.exit_code == 0, minimal.output
    minimal_payload = json.loads(minimal.output)
    assert minimal_payload["capsule_version"] == "2"
    assert minimal_payload["projection"] == "minimal"
    assert "established_facts" not in minimal_payload
    assert minimal_payload["semantic_recommendation_included"] is False

    working = runner.invoke(cli, ["campaign", "resume-profile", "--workspace", str(workspace), "--profile", "working", "--max-items", "1", "--json"])
    assert working.exit_code == 0, working.output
    working_payload = json.loads(working.output)
    assert working_payload["established_facts"] == ["f3"]
    assert working_payload["resolved_questions"] == ["q2"]
    assert working_payload["omissions"]["omitted_counts"]["established_facts"] == 2
    assert working_payload["omissions"]["semantic_selection_performed"] is False

    audit = runner.invoke(cli, ["campaign", "resume-profile", "--workspace", str(workspace), "--profile", "audit", "--json"])
    assert audit.exit_code == 0, audit.output
    audit_payload = json.loads(audit.output)
    assert "preflight" in audit_payload
    assert "semantic_companion" in audit_payload
    assert audit_payload["preflight"]["semantic_recommendation_included"] is False


def test_capability_context_enumerates_without_selection(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path, responsibility=True)
    result = CliRunner().invoke(
        cli,
        ["campaign", "capability-context", "--workspace", str(workspace), "--responsibility-type", "repository_diagnosis", "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["responsibility_id"] == "R-1"
    assert payload["candidate_count"] >= 1
    assert {item["id"] for item in payload["candidates"]} >= {"repo-sensemaker"}
    assert payload["selection_performed"] is False
    assert payload["recommendation_performed"] is False
    assert payload["authority_granted"] is False


def test_uncertainty_relationships_are_explicit_and_unranked(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path, uncertainty=True)
    history = UncertaintyHistoryService(workspace)
    history.append(event_id="UE-1", uncertainty_id="U-1", status="active")
    history.append(event_id="UE-2", uncertainty_id="U-2", status="deferred")
    runner = CliRunner()
    related = runner.invoke(
        cli,
        ["campaign", "uncertainty-relate", "--workspace", str(workspace), "--relation-id", "UR-1", "--uncertainty-id", "U-1", "--relation", "depends_on", "--target", "U-2", "--json"],
    )
    assert related.exit_code == 0, related.output
    shown = runner.invoke(cli, ["campaign", "uncertainty-show", "--workspace", str(workspace), "U-1", "--json"])
    assert shown.exit_code == 0, shown.output
    shown_payload = json.loads(shown.output)
    assert shown_payload["found"] is True
    assert shown_payload["outbound_relations"][0]["relation"]["target_ref"] == "U-2"
    graph = runner.invoke(cli, ["campaign", "uncertainty-graph", "--workspace", str(workspace), "--format", "json"])
    assert graph.exit_code == 0, graph.output
    graph_payload = json.loads(graph.output)
    assert graph_payload["semantic_ranking_performed"] is False
    assert any(edge["relation"] == "depends_on" for edge in graph_payload["edges"])

    rejected = runner.invoke(
        cli,
        ["campaign", "uncertainty-relate", "--workspace", str(workspace), "--relation-id", "UR-2", "--uncertainty-id", "U-1", "--relation", "depends_on", "--target", "U-1"],
    )
    assert rejected.exit_code != 0
    assert "may not target itself" in rejected.output


def test_bundle_can_be_inspected_and_projected_before_durable_import(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    bundle = tmp_path / "campaign.sensemaking"
    CampaignBundleService(workspace).export(bundle)
    runner = CliRunner()
    inspected = runner.invoke(cli, ["campaign", "bundle-inspect", "--bundle", str(bundle), "--json"])
    assert inspected.exit_code == 0, inspected.output
    inspect_payload = json.loads(inspected.output)
    assert inspect_payload["valid"] is True
    assert inspect_payload["file_count"] > 0

    resumed = runner.invoke(cli, ["campaign", "bundle-resume-context", "--bundle", str(bundle), "--profile", "minimal", "--json"])
    assert resumed.exit_code == 0, resumed.output
    resume_payload = json.loads(resumed.output)
    assert resume_payload["capsule_version"] == "2"
    assert resume_payload["durable_import_performed"] is False

    graph = runner.invoke(cli, ["campaign", "bundle-graph", "--bundle", str(bundle), "--json"])
    assert graph.exit_code == 0, graph.output
    assert json.loads(graph.output)["durable_import_performed"] is False


def test_campaign_inventory_is_sorted_and_does_not_prioritize(tmp_path: Path) -> None:
    root = tmp_path / "campaigns"
    root.mkdir()
    _workspace(root, "b")
    _workspace(root, "a")
    result = CliRunner().invoke(cli, ["campaign", "inventory", "--root", str(root), "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["campaign_count"] == 2
    assert [Path(item["workspace"]).name for item in payload["entries"]] == ["a", "b"]
    assert payload["prioritization_performed"] is False
    assert payload["semantic_recommendation_included"] is False
