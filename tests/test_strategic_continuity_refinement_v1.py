"""Qualification for Issue #430 Strategic Continuity Refinement v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[1]
STRATEGIC_VALIDATOR = ROOT / "scripts" / "validate-strategic-repository-analysis.py"
COMPANION_VALIDATOR = ROOT / "scripts" / "validate-strategic-companion.py"


def _analysis(source_identity: str, *, roadmap_field: bool = False, candidate_ref: str = "PATH-1/T1") -> dict:
    transition = {
        "transition_ref": "PATH-1/T1",
        "transition": "isolated lineage -> typed currentness",
    }
    if roadmap_field:
        transition["deadline"] = "tomorrow"
    return {
        "artifact_id": "strategic_repository_analysis",
        "analysis_ref": "SRA-1",
        "continuity": {
            "prior_analysis_ref": "SRA-0",
            "disposition": "CONTINUE",
            "prior_selected_path_id": "PATH-1",
            "reason": "The same broad trajectory remains material.",
        },
        "target_repository": "owner/repo",
        "target_source_identity": f"sha:{source_identity}",
        "governing_intent": "Improve reconstructible strategic decisions.",
        "governing_authority_refs": ["docs/product-strategy.md"],
        "capability_states": [
            {
                "capability_id": "continuity",
                "state": "PARTIAL",
                "evidence_refs": ["docs/evidence.md"],
            }
        ],
        "strategic_frontier": [
            {"frontier_id": "FRONTIER-1", "statement": "Currentness precision is material."}
        ],
        "construction_paths": [
            {
                "path_id": "PATH-1",
                "name": "Deepen continuity",
                "future_state": "Strategic state is cheaper to reconstruct.",
                "builds_on": ["continuity"],
                "required_capabilities": ["typed currentness"],
                "construction_sequence": ["observe", "reconcile"],
                "path_transitions": [transition],
                "dependencies": ["repository evidence"],
                "unlocks": ["cheaper reconstruction"],
                "risks": ["roadmap drift"],
                "reversibility": "High",
                "evidence_gaps": ["normal-use friction"],
                "assumptions": ["Current authority remains stable."],
                "reassessment_triggers": ["Governing authority changes."],
            }
        ],
        "path_comparison": [
            {
                "path_id": "PATH-1",
                "lenses": {
                    "mission_relevance": "Direct",
                    "decision_value": "Material",
                    "blocking_power": "Relevant",
                    "evidence_sufficiency": "Bounded",
                    "consequence_of_error": "Reversible",
                    "deferral_cost": "Moderate",
                    "reversibility": "High",
                    "authority_availability": "Available",
                    "dependency": "Known",
                    "smallest_warranted_intervention": "Add bounded continuity depth.",
                },
            }
        ],
        "decision_changing_uncertainty": {
            "statement": "Whether currentness is too coarse.",
            "could_change": "The depth of continuity support.",
            "inquiry_warranted": False,
            "evidence_needed": "None for the authorized package.",
            "source": "repository_evidence",
        },
        "decision_assumptions": [
            {
                "assumption_id": "ASSUMPTION-1",
                "statement": "Product authority remains stable.",
                "evidence_refs": ["docs/product-strategy.md"],
                "reassessment_triggers": ["Product authority changes."],
            }
        ],
        "strategic_disposition": "BUILD",
        "selected_path_id": "PATH-1",
        "candidate_repository_responsibility": "Implement continuity refinement.",
        "candidate_path_transition_ref": candidate_ref,
        "smallest_warranted_intervention": "Typed currentness plus read-only history.",
        "implementation_authority_established_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T16:00:00Z",
        "immutable": True,
    }


def _reconciliation(*, roadmap_field: bool = False) -> dict:
    effect = {"transition_ref": "PATH-1/T1", "disposition": "ESTABLISHED"}
    if roadmap_field:
        effect["percent_complete"] = 100
    return {
        "artifact_id": "strategic_reconciliation",
        "target_repository": "owner/repo",
        "prior_analysis_ref": "SRA-1",
        "current_source_identity": "main@def",
        "returned_evidence": [{"evidence_ref": "PR#1", "claim": "Typed currentness exists."}],
        "claim_updates": [
            {"claim_ref": "CLAIM-1", "disposition": "CONFIRM", "reason": "Evidence supports it."}
        ],
        "assumption_updates": [
            {
                "assumption_id": "ASSUMPTION-1",
                "disposition": "CONFIRM",
                "reason": "Authority remains stable.",
            }
        ],
        "path_disposition": "CONTINUE",
        "prior_path_id": "PATH-1",
        "current_path_id": "PATH-1",
        "path_transition_effect": effect,
        "strategic_effect": "REAFFIRM",
        "candidate_next_responsibility": None,
        "implementation_authority_established_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T17:00:00Z",
        "immutable": True,
    }


def _artifact(path: Path, data: dict) -> None:
    path.write_text(
        "# Artifact\n\n## Machine-Readable Summary\n\n```yaml\n"
        + yaml.safe_dump(data, sort_keys=False)
        + "```\n",
        encoding="utf-8",
    )


def _run_validator(script: Path, artifact: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(script), str(artifact), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def test_typed_currentness_reports_mechanical_observation_kinds(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "docs").mkdir()
    (repo / "docs" / "product-strategy.md").write_text("authority v1\n", encoding="utf-8")
    (repo / "docs" / "evidence.md").write_text("evidence v1\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    initial = _git(repo, "rev-parse", "HEAD")

    artifact = tmp_path / "analysis.md"
    _artifact(artifact, _analysis(initial))
    runner = CliRunner()

    current = runner.invoke(
        cli, ["strategy", "drift", "--artifact", str(artifact), "--repo", str(repo), "--json"]
    )
    assert current.exit_code == 0, current.output
    current_payload = json.loads(current.output)
    assert current_payload["currentness_observations"] == []
    assert current_payload["mechanical_drift_detected"] is False

    (repo / "docs" / "product-strategy.md").write_text("authority v2\n", encoding="utf-8")
    (repo / "docs" / "evidence.md").write_text("evidence v2\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "change authority and evidence")

    drifted = runner.invoke(
        cli, ["strategy", "drift", "--artifact", str(artifact), "--repo", str(repo), "--json"]
    )
    assert drifted.exit_code == 0, drifted.output
    payload = json.loads(drifted.output)
    kinds = {item["kind"] for item in payload["currentness_observations"]}
    assert {
        "SOURCE_IDENTITY_CHANGED",
        "GOVERNING_AUTHORITY_REF_CHANGED",
        "EVIDENCE_REF_CHANGED",
    } <= kinds
    assert payload["semantic_consequence_inferred_by_command"] is False
    assert payload["strategy_invalidated_by_command"] is False
    assert payload["reanalysis_required_by_command"] is False

    (repo / "docs" / "evidence.md").unlink()
    missing = runner.invoke(
        cli, ["strategy", "drift", "--artifact", str(artifact), "--repo", str(repo), "--json"]
    )
    assert missing.exit_code == 0, missing.output
    missing_kinds = {item["kind"] for item in json.loads(missing.output)["currentness_observations"]}
    assert "EVIDENCE_REF_MISSING" in missing_kinds


def test_history_and_graph_project_only_declared_relationships(tmp_path: Path) -> None:
    analysis = tmp_path / "analysis.md"
    reconciliation = tmp_path / "reconciliation.md"
    _artifact(analysis, _analysis("abc1234"))
    _artifact(reconciliation, _reconciliation())
    runner = CliRunner()

    history = runner.invoke(
        cli,
        [
            "strategy",
            "history",
            "--artifact",
            str(analysis),
            "--artifact",
            str(reconciliation),
            "--json",
        ],
    )
    assert history.exit_code == 0, history.output
    payload = json.loads(history.output)
    assert [event["artifact_id"] for event in payload["events"]] == [
        "strategic_repository_analysis",
        "strategic_reconciliation",
    ]
    assert payload["caller_order_preserved"] is True
    assert payload["chronology_inferred_by_command"] is False
    assert payload["strategy_selected_by_command"] is False
    assert payload["semantic_consequence_inferred_by_command"] is False
    assert payload["events"][0]["path_transitions"][0]["transition_ref"] == "PATH-1/T1"
    assert payload["events"][1]["path_transition_effect"]["disposition"] == "ESTABLISHED"

    graph = runner.invoke(
        cli,
        [
            "strategy",
            "graph",
            "--artifact",
            str(analysis),
            "--artifact",
            str(reconciliation),
            "--json",
        ],
    )
    assert graph.exit_code == 0, graph.output
    graph_payload = json.loads(graph.output)
    mermaid = graph_payload["mermaid"]
    assert "graph TD" in mermaid
    assert "CONTINUE" in mermaid
    assert "selected" in mermaid
    assert "reconciled by" in mermaid
    assert "transition ESTABLISHED" in mermaid
    assert graph_payload["causality_inferred_by_command"] is False
    assert graph_payload["strategy_selected_by_command"] is False


def test_path_transition_identity_is_optional_but_roadmap_fields_are_rejected(
    tmp_path: Path,
) -> None:
    valid = tmp_path / "valid-analysis.md"
    _artifact(valid, _analysis("abc1234"))
    code, payload = _run_validator(STRATEGIC_VALIDATOR, valid)
    assert code == 0, payload

    roadmap = tmp_path / "roadmap-analysis.md"
    _artifact(roadmap, _analysis("abc1234", roadmap_field=True))
    code, payload = _run_validator(STRATEGIC_VALIDATOR, roadmap)
    assert code == 1
    assert "STRATEGIC_ANALYSIS_PATH_TRANSITION_ROADMAP_FIELD_FORBIDDEN" in {
        item["error_id"] for item in payload["errors"]
    }

    unknown = tmp_path / "unknown-analysis.md"
    _artifact(unknown, _analysis("abc1234", candidate_ref="PATH-1/T9"))
    code, payload = _run_validator(STRATEGIC_VALIDATOR, unknown)
    assert code == 1
    assert "STRATEGIC_ANALYSIS_CANDIDATE_TRANSITION_UNKNOWN" in {
        item["error_id"] for item in payload["errors"]
    }


def test_reconciliation_may_record_transition_effect_without_project_status(
    tmp_path: Path,
) -> None:
    valid = tmp_path / "valid-reconciliation.md"
    _artifact(valid, _reconciliation())
    code, payload = _run_validator(COMPANION_VALIDATOR, valid)
    assert code == 0, payload
    assert payload["strategy_mutated_by_validator"] is False

    roadmap = tmp_path / "roadmap-reconciliation.md"
    _artifact(roadmap, _reconciliation(roadmap_field=True))
    code, payload = _run_validator(COMPANION_VALIDATOR, roadmap)
    assert code == 1
    assert "STRATEGIC_RECONCILIATION_PATH_TRANSITION_ROADMAP_FIELD_FORBIDDEN" in {
        item["error_id"] for item in payload["errors"]
    }
