"""Campaign-facing B7 semantic-reference audit behavior."""

from __future__ import annotations

import json
import subprocess

from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import CampaignState, Uncertainty, target_snapshot_sha256
from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _campaign(tmp_path):
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-B7",
            mission="audit semantic references without semantic inference",
            status="active",
            current_state="initialized",
            active_uncertainty=Uncertainty(
                id="U-current",
                question="Which evidence remains mechanically addressable?",
                consequences={"if_unresolved": "reference audit remains bounded"},
            ),
        )
    )
    evidence = workspace / "evidence" / "observed.txt"
    evidence.write_text("mechanical evidence\n", encoding="utf-8")
    return workspace


def _bound_campaign(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    subprocess.run(["git", "-C", str(target), "init"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(target), "config", "user.email", "b7@example.invalid"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "config", "user.name", "B7 Fixture"],
        check=True,
        capture_output=True,
    )
    (target / "tracked.txt").write_text("target\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "tracked.txt"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(target), "commit", "-m", "initial"],
        check=True,
        capture_output=True,
    )
    workspace = tmp_path / "campaign"
    CampaignService(workspace, target_repo=target).initialize(
        CampaignState(
            campaign_id="CMP-B7-BOUND",
            mission="audit bound target references",
            status="active",
            current_state="initialized",
        )
    )
    return workspace


def _append(workspace, *extra_args, target_ref="external:test"):
    args = [
        "campaign",
        "semantic-state-append",
        "--workspace",
        str(workspace),
        "--entry-id",
        "S1",
        "--source-skill",
        "repo-sensemaker",
        "--artifact-ref",
        "brief.md",
    ]
    if target_ref is not None:
        args.extend(["--target-ref", target_ref])
    args.extend([*extra_args, "--json"])
    return CliRunner().invoke(cli, args)


def test_semantic_state_audit_resolves_evidence_but_keeps_opaque_refs_informational(tmp_path):
    workspace = _campaign(tmp_path)
    appended = _append(
        workspace,
        "--evidence-ref",
        "evidence/observed.txt",
        "--claim-ref",
        "C1",
        "--uncertainty-ref",
        "U-current",
    )
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        ["campaign", "semantic-state", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    audit = payload["reference_audit"]
    assert payload["code"] == "CAMPAIGN_SEMANTIC_STATE_VALID"
    assert audit["integrity_ok"] is True
    assert audit["resolved_count"] == 2
    assert audit["not_addressable_count"] == 3
    assert audit["integrity_failure_count"] == 0
    assert audit["semantic_truth_established"] is False

    by_field = {item["field"]: item for item in audit["items"]}
    assert by_field["evidence_refs[0]"]["resolution"] == "resolved"
    assert by_field["uncertainty_refs[0]"]["resolution"] == "resolved"
    assert by_field["artifact_ref"]["resolution"] == "not_addressable"
    assert by_field["claim_refs[0]"]["resolution"] == "not_addressable"


def test_semantic_state_audit_resolves_bound_target_ref(tmp_path):
    workspace = _bound_campaign(tmp_path)
    snapshot = CampaignService(workspace).resume()
    target_ref = f"target-snapshot-sha256:{target_snapshot_sha256(snapshot.state.target_snapshot)}"
    appended = _append(workspace, target_ref=target_ref)
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        ["campaign", "semantic-state", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    by_field = {item["field"]: item for item in payload["reference_audit"]["items"]}
    assert by_field["target_ref"]["resolution"] == "resolved"
    assert by_field["target_ref"]["resolver"] == "campaign.target_snapshot"
    assert by_field["target_ref"]["integrity_effect"] == "pass"

    explained = CliRunner().invoke(
        cli,
        [
            "campaign",
            "explain",
            "--workspace",
            str(workspace),
            "--ref",
            target_ref,
            "--json",
        ],
    )
    assert explained.exit_code == 0, explained.output
    explain_payload = json.loads(explained.output)
    assert explain_payload["code"] == "CAMPAIGN_REFERENCE_EXPLAINED"
    assert any(item["kind"] == "semantic_target_ref" for item in explain_payload["matches"])
    assert explain_payload["reference_audit"][0]["resolution"] == "resolved"


def test_semantic_state_audit_reports_campaign_local_dangling_reference(tmp_path):
    workspace = _campaign(tmp_path)
    appended = _append(workspace, "--evidence-ref", "evidence/missing.txt")
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        ["campaign", "semantic-state", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    audit = payload["reference_audit"]
    assert payload["code"] == "CAMPAIGN_SEMANTIC_STATE_REFERENCE_INTEGRITY_FAILED"
    assert payload["diagnostics"] == []
    assert audit["integrity_ok"] is False
    assert audit["dangling_count"] == 1
    assert audit["integrity_failure_count"] == 1


def test_campaign_explain_renders_reference_audit_without_turning_it_into_truth(tmp_path):
    workspace = _campaign(tmp_path)
    appended = _append(workspace, "--evidence-ref", "evidence/missing.txt")
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        [
            "campaign",
            "explain",
            "--workspace",
            str(workspace),
            "--ref",
            "evidence/missing.txt",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_REFERENCE_EXPLAINED"
    assert payload["reference_integrity_ok"] is False
    assert payload["reference_audit"][0]["resolution"] == "dangling"
    assert payload["reference_audit"][0]["integrity_effect"] == "fail"
    assert payload["semantic_truth_established"] is False


def test_campaign_explain_marks_opaque_claim_not_addressable_without_failure(tmp_path):
    workspace = _campaign(tmp_path)
    appended = _append(workspace, "--claim-ref", "C1")
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        ["campaign", "explain", "--workspace", str(workspace), "--ref", "C1", "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["reference_integrity_ok"] is True
    assert payload["reference_audit"][0]["resolution"] == "not_addressable"
    assert payload["reference_audit"][0]["integrity_effect"] == "informational"


def test_resume_context_remains_outside_b7_reference_audit_surface(tmp_path):
    workspace = _campaign(tmp_path)
    appended = _append(workspace, "--evidence-ref", "evidence/missing.txt")
    assert appended.exit_code == 0, appended.output

    result = CliRunner().invoke(
        cli,
        ["campaign", "resume-context", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert "reference_audit" not in payload
    assert "reference_integrity_ok" not in payload
    assert payload["semantic_recommendation_included"] is False
