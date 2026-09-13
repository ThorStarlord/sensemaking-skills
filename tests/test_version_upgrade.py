from __future__ import annotations

from pathlib import Path

from sensemaking_skills.campaign_semantics import CURRENT_SCHEMA_VERSION, migrate_payload


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_v1_artifact_migrates_to_v2_without_reinterpreting_extensions() -> None:
    evidence = {"source": "fixture", "items": ["unchanged"]}
    legacy = {
        "campaign_id": "CMP-UPGRADE",
        "mission": "prove migration",
        "status": "active",
        "current_state": "initialized",
        "schema_version": "1",
        "evidence": evidence,
    }

    result = migrate_payload(legacy, artifact_kind="campaign_state")

    assert result.target_version == CURRENT_SCHEMA_VERSION == "2"
    assert result.payload["evidence"] == evidence
    assert legacy["evidence"] == evidence
    assert legacy["schema_version"] == "1"


def test_release_checklist_requires_each_candidate_gate() -> None:
    checklist = (REPO_ROOT / "docs" / "release-v1.0-checklist.md").read_text(
        encoding="utf-8"
    )
    required_gates = (
        "exact release head",
        "product/lab boundary",
        "contract authority graph",
        "Skill inventory",
        "isolated collection",
        "wheel and sdist build",
        "Campaign golden path",
        "schema migration",
        "qualification claims",
        "documentation currentness",
    )

    missing = [gate for gate in required_gates if gate.lower() not in checklist.lower()]
    assert not missing, f"release checklist omits gates: {missing}"
