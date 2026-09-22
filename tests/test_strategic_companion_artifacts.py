"""Repository qualification for strategic reconciliation and reserved-decision artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
GENERIC = ROOT / "scripts" / "validate-artifact.py"
SPECIAL = ROOT / "scripts" / "validate-strategic-companion.py"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
OWNER_DECISION_SKILL = ROOT / "skills" / "owner-decision-capsule" / "SKILL.md"
OWNER_DECISION_SKILL = ROOT / "skills" / "owner-decision-capsule" / "SKILL.md"
OWNER_DECISION_SKILL = ROOT / "skills" / "owner-decision-capsule" / "SKILL.md"


def _artifact(title: str, sections: list[str], data: dict) -> str:
    chunks = [f"# {title}\n"]
    for index, section in enumerate(sections, start=1):
        heading = section.replace("_", " ").title()
        chunks.append(f"\n## {index}. {heading}\n\nDeclared.\n")
    chunks.append(
        f"\n## {len(sections) + 1}. Machine-Readable Summary\n\n```yaml\n"
        + yaml.safe_dump(data, sort_keys=False)
        + "```\n"
    )
    return "".join(chunks)


def _validate(tmp_path: Path, artifact_id: str, content: str) -> dict:
    path = tmp_path / f"{artifact_id}.md"
    path.write_text(content, encoding="utf-8")
    special = subprocess.run(
        [sys.executable, str(SPECIAL), str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert special.returncode == 0, special.stdout + special.stderr
    payload = json.loads(special.stdout)
    assert payload["valid"] is True
    assert payload["semantic_truth_established"] is False
    assert payload["implementation_authorized_by_validator"] is False

    generic = subprocess.run(
        [
            sys.executable,
            str(GENERIC),
            artifact_id,
            str(path),
            "--repo-root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert generic.returncode == 0, generic.stdout + generic.stderr
    return payload


def test_strategic_reconciliation_validates_without_mutating_strategy(tmp_path: Path) -> None:
    data = {
        "artifact_id": "strategic_reconciliation",
        "target_repository": "owner/repo",
        "prior_analysis_ref": "SRA-1",
        "current_source_identity": "main@abc",
        "returned_evidence": [{"evidence_ref": "PR#1", "claim": "Capability shipped."}],
        "claim_updates": [
            {"claim_ref": "CLAIM-1", "disposition": "CONFIRM", "reason": "Evidence supports it."}
        ],
        "assumption_updates": [
            {
                "assumption_id": "ASSUMPTION-1",
                "disposition": "RESOLVE",
                "reason": "Dependency is now evidenced.",
            }
        ],
        "path_disposition": "CONTINUE",
        "prior_path_id": "PATH-1",
        "current_path_id": "PATH-1",
        "strategic_effect": "REAFFIRM",
        "candidate_next_responsibility": None,
        "implementation_authority_established_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T05:00:00Z",
        "immutable": True,
    }
    sections = [
        "prior_decision_and_scope",
        "returned_evidence",
        "claim_updates",
        "assumption_updates",
        "path_continuation",
        "strategic_implication",
        "authority_and_claim_boundaries",
        "evidence",
    ]
    payload = _validate(tmp_path, "strategic_reconciliation", _artifact("Strategic Reconciliation", sections, data))
    assert payload["strategy_mutated_by_validator"] is False


def test_owner_decision_capsule_cannot_make_owner_decision(tmp_path: Path) -> None:
    data = {
        "artifact_id": "owner_decision_capsule",
        "decision_id": "OWNER-1",
        "target_repository": "owner/repo",
        "decision_statement": "Choose the external authority boundary.",
        "repository_can_resolve": False,
        "options": [
            {
                "option_id": "OPTION-A",
                "statement": "Keep current boundary.",
                "unlocks": [],
                "tradeoffs": ["Less automation."],
                "reversibility": "High",
                "deferral_effect": "No immediate repository change.",
                "authority_if_selected": [],
            },
            {
                "option_id": "OPTION-B",
                "statement": "Delegate the boundary explicitly.",
                "unlocks": ["Bounded automation."],
                "tradeoffs": ["Broader authority surface."],
                "reversibility": "Moderate",
                "deferral_effect": "Automation remains blocked.",
                "authority_if_selected": ["Explicit bounded external mutation."],
            },
        ],
        "owner_decision_made_by_artifact": False,
        "implementation_authority_established_by_artifact": False,
        "created_at": "2026-09-20T05:00:00Z",
        "immutable": True,
    }
    sections = [
        "decision_needed",
        "why_repository_evidence_cannot_resolve_it",
        "credible_options",
        "tradeoffs_reversibility_and_deferral",
        "authority_effects",
        "evidence",
    ]
    payload = _validate(tmp_path, "owner_decision_capsule", _artifact("Owner Decision Capsule", sections, data))
    assert payload["owner_decision_made_by_validator"] is False


def test_thesis_review_packet_cannot_ratify_level4_change(tmp_path: Path) -> None:
    data = {
        "artifact_id": "thesis_review_packet",
        "target_repository": "owner/repo",
        "level4_commitment_ref": "docs/product-strategy.md#product-purpose",
        "challenge_statement": "A concrete consumer conflicts with the current product boundary.",
        "evidence_refs": ["docs/product-strategy.md"],
        "affected_responsibilities": ["PATH-1"],
        "candidate_dispositions": ["REAFFIRM", "REINTERPRET"],
        "downstream_reconciliation": ["Reassess the Strategic Frontier."],
        "owner_ratification_required": True,
        "thesis_revision_ratified_by_artifact": False,
        "implementation_authority_established_by_artifact": False,
        "created_at": "2026-09-20T05:00:00Z",
        "immutable": True,
    }
    sections = [
        "challenged_commitment",
        "thesis_tension",
        "evidence",
        "affected_level3_work",
        "candidate_level4_dispositions",
        "downstream_reconciliation",
        "authority_boundary",
    ]
    payload = _validate(tmp_path, "thesis_review_packet", _artifact("Thesis Review Packet", sections, data))
    assert payload["thesis_revision_ratified_by_validator"] is False


def test_external_evidence_packet_binds_claims_to_sources(tmp_path: Path) -> None:
    data = {
        "artifact_id": "external_evidence_packet",
        "target_decision_ref": "SRA-1",
        "retrieved_at": "2026-09-20T05:00:00Z",
        "sources": [
            {
                "source_id": "SOURCE-1",
                "uri": "https://example.com",
                "title": "Example",
                "publisher": "Example",
                "publication_date": None,
                "retrieved_at": "2026-09-20T05:00:00Z",
            }
        ],
        "claims": [
            {
                "claim_id": "EXT-1",
                "statement": "A bounded external fact.",
                "source_ids": ["SOURCE-1"],
                "currentness_limit": "Recheck when the external contract changes.",
            }
        ],
        "repository_fact_established_by_artifact": False,
        "semantic_truth_established": False,
        "implementation_authority_established_by_artifact": False,
        "created_at": "2026-09-20T05:00:00Z",
        "immutable": True,
    }
    sections = [
        "question_and_scope",
        "sources",
        "claims_supported",
        "currentness_limits",
        "provenance",
        "authority_and_claim_boundaries",
    ]
    _validate(tmp_path, "external_evidence_packet", _artifact("External Evidence Packet", sections, data))


def test_strategic_companion_skills_are_registered_in_product_surfaces() -> None:
    contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))["artifacts"]
    contract_ids = {item["id"] for item in contracts}
    expected_artifacts = {
        "strategic_reconciliation",
        "owner_decision_capsule",
        "thesis_review_packet",
        "external_evidence_packet",
    }
    assert expected_artifacts <= contract_ids

    registry = yaml.safe_load(
        (ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    core_ids = {item["id"] for item in registry["ecosystems"]["core"]["skills"]}
    expected_skills = {
        "strategic-repository-reconciliation",
        "owner-decision-capsule",
        "thesis-review-packet",
        "external-evidence-packet",
    }
    assert expected_skills <= core_ids

    domain = yaml.safe_load((ROOT / "domain-packs" / "engineering.yaml").read_text(encoding="utf-8"))
    assert expected_artifacts <= set(domain["artifact_contracts"])

    release = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    assert expected_skills <= set(release["skill_inventory"]["supported"])


def test_owner_decision_capsule_fails_closed_when_option_set_is_materially_incomplete() -> None:
    skill = OWNER_DECISION_SKILL.read_text(encoding="utf-8")

    assert "option-set adequacy" in skill
    assert "OPTION_SET_INCOMPLETE" in skill
    assert "do not emit a misleading binary capsule" in skill
    assert "construction-path/frontier synthesis must be reopened" in skill
    assert "two represented options != option set necessarily complete" in skill
    assert "OPTION_SET_INCOMPLETE != owner decision" in skill


def test_owner_decision_capsule_fails_closed_when_option_set_is_materially_incomplete() -> None:
    skill = OWNER_DECISION_SKILL.read_text(encoding="utf-8")

    assert "option-set adequacy" in skill
    assert "OPTION_SET_INCOMPLETE" in skill
    assert "do not emit a misleading binary capsule" in skill
    assert "construction-path/frontier synthesis must be reopened" in skill
    assert "two represented options != option set necessarily complete" in skill
    assert "OPTION_SET_INCOMPLETE != owner decision" in skill


def test_owner_decision_capsule_fails_closed_when_option_set_is_materially_incomplete() -> None:
    skill = OWNER_DECISION_SKILL.read_text(encoding="utf-8")

    assert "option-set adequacy" in skill
    assert "OPTION_SET_INCOMPLETE" in skill
    assert "do not emit a misleading binary capsule" in skill
    assert "construction-path/frontier synthesis must be reopened" in skill
    assert "two represented options != option set necessarily complete" in skill
    assert "OPTION_SET_INCOMPLETE != owner decision" in skill
