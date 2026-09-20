"""Qualification for Decision Journey Productization v1."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli


def _artifact(path: Path, data: dict) -> Path:
    path.write_text(
        "# Artifact\n\n## Machine-Readable Summary\n\n"
        "```yaml\n"
        + yaml.safe_dump(data, sort_keys=False)
        + "```\n",
        encoding="utf-8",
    )
    return path


def _analysis(
    path: Path,
    ref: str,
    disposition: str,
    path_id: str | None,
) -> Path:
    return _artifact(
        path,
        {
            "artifact_id": "strategic_repository_analysis",
            "analysis_ref": ref,
            "target_repository": "owner/repo",
            "target_source_identity": "main@abc1234",
            "strategic_disposition": disposition,
            "selected_path_id": path_id,
            "candidate_repository_responsibility": (
                "Bounded responsibility"
            ),
        },
    )


def test_guide_is_explicit_static_guidance() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "journey",
            "guide",
            "--intent",
            "repository-future",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["capability"] == "strategic-repository-analysis"
    assert payload["intent_selected_by_caller"] is True
    assert payload["automatic_routing_performed"] is False
    assert payload["capability_invoked_by_command"] is False


def test_strategic_context_pack_requires_explicit_profile_and_source(
    tmp_path: Path,
) -> None:
    analysis = _analysis(
        tmp_path / "sra.md",
        "SRA-1",
        "BUILD",
        "PATH-1",
    )
    result = CliRunner().invoke(
        cli,
        [
            "journey",
            "context",
            "--profile",
            "strategic",
            "--strategy-artifact",
            str(analysis),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["profile"] == "strategic"
    assert payload["context"]["strategic_analysis"]["ref"] == "SRA-1"
    assert payload["profile_selected_by_caller"] is True
    assert payload["automatic_routing_performed"] is False
    assert payload["next_action_selected"] is False


def test_authored_decision_delta_is_bound_to_analysis_refs(
    tmp_path: Path,
) -> None:
    before = _analysis(
        tmp_path / "before.md",
        "SRA-1",
        "BUILD",
        "PATH-1",
    )
    after = _analysis(
        tmp_path / "after.md",
        "SRA-2",
        "INVESTIGATE",
        None,
    )
    delta = _artifact(
        tmp_path / "delta.md",
        {
            "artifact_id": "strategic_decision_delta",
            "delta_ref": "DELTA-1",
            "prior_analysis_ref": "SRA-1",
            "current_analysis_ref": "SRA-2",
            "continuity_disposition": "REVISE",
            "unchanged_commitments": [
                "Product purpose remains unchanged."
            ],
            "new_evidence_refs": ["evidence:E-1"],
            "assumption_changes": [
                {
                    "assumption_id": "A-1",
                    "effect": "INVALIDATED",
                    "reason": (
                        "Returned evidence contradicted the premise."
                    ),
                }
            ],
            "decision_change": "BUILD -> INVESTIGATE",
            "semantic_reason": "A dependency must be resolved first.",
            "semantic_truth_established": False,
            "strategy_selected_by_delta": False,
            "implementation_authorized_by_delta": False,
        },
    )
    result = CliRunner().invoke(
        cli,
        [
            "journey",
            "delta",
            "--artifact",
            str(delta),
            "--before",
            str(before),
            "--after",
            str(after),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["delta_ref"] == "DELTA-1"
    assert payload["disposition_before"] == "BUILD"
    assert payload["disposition_after"] == "INVESTIGATE"
    assert payload["semantic_interpretation_authored"] is True
    assert payload["strategy_selected_by_command"] is False


def test_impact_closure_reports_unaccounted_surface_without_inference(
    tmp_path: Path,
) -> None:
    impact = _artifact(
        tmp_path / "impact.md",
        {
            "artifact_id": "change_impact_analysis",
            "analysis_ref": "CIA-1",
            "change": {
                "change_id": "CHANGE-1",
                "state": "IMPLEMENTED",
                "statement": "Bounded change",
            },
            "impact_items": [
                {"surface_id": "IMPACT-1"},
                {"surface_id": "IMPACT-2"},
            ],
            "closure_effect": "ADDITIONAL_VERIFICATION_REQUIRED",
        },
    )
    closure = _artifact(
        tmp_path / "closure.md",
        {
            "artifact_id": "change_evidence_closure",
            "closure_ref": "CEC-1",
            "change_impact_ref": "CIA-1",
            "observed_evidence_refs": ["test:1"],
            "verified_surface_ids": ["IMPACT-1"],
            "unresolved_surface_ids": [],
            "reconciliation_refs": [],
            "closure_disposition": "READY_TO_REASSESS",
            "semantic_reason": (
                "One anticipated surface still lacks evidence."
            ),
            "closure_inferred_by_artifact": False,
            "followup_execution_authorized_by_artifact": False,
            "semantic_truth_established": False,
        },
    )
    result = CliRunner().invoke(
        cli,
        [
            "journey",
            "impact-closure",
            "--impact-artifact",
            str(impact),
            "--closure-artifact",
            str(closure),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["verified_surface_ids"] == ["IMPACT-1"]
    assert payload["unaccounted_surface_ids"] == ["IMPACT-2"]
    assert payload["closure_inferred_by_command"] is False
    assert payload["difference_is_reassessment_evidence_only"] is True


def test_manifest_reports_missing_explicit_campaign_link(
    tmp_path: Path,
) -> None:
    analysis = _analysis(
        tmp_path / "sra.md",
        "SRA-1",
        "BUILD",
        "PATH-1",
    )
    manifest = _artifact(
        tmp_path / "journey.md",
        {
            "artifact_id": "decision_journey",
            "journey_id": "JOURNEY-1",
            "strategic_origin_ref": "SRA-1",
            "campaign_id": "CMP-1",
            "execution_handoff_ids": [],
            "execution_result_ids": [],
            "strategic_reconciliation_refs": [],
            "change_impact_refs": [],
        },
    )
    result = CliRunner().invoke(
        cli,
        [
            "journey",
            "inspect",
            "--manifest",
            str(manifest),
            "--strategy-artifact",
            str(analysis),
            "--json",
        ],
    )
    assert result.exit_code == 3
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["mechanical_reconstruction_only"] is True
    assert "JOURNEY_CAMPAIGN_MISSING" in {
        item["code"] for item in payload["diagnostics"]
    }
    assert payload["causal_truth_inferred"] is False


def test_journey_help_is_registered() -> None:
    result = CliRunner().invoke(cli, ["journey", "--help"])
    assert result.exit_code == 0, result.output
    assert "inspect" in result.output
    assert "context" in result.output
    assert "delta" in result.output
    assert "impact-closure" in result.output
    assert "guide" in result.output
