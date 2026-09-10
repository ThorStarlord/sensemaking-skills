"""Mechanical conformance tests for manifest-driven semantic architecture."""

from __future__ import annotations

from sensemaking_skills.semantic_architecture import validate_conformance


def test_conformance_accepts_bounded_skill_and_domain_manifests(tmp_path):
    manifests = tmp_path / "skill-manifests"
    packs = tmp_path / "domain-packs"
    manifests.mkdir()
    packs.mkdir()
    (tmp_path / "ledger.md").write_text("ledger\n", encoding="utf-8")
    (tmp_path / "policy.md").write_text("policy\n", encoding="utf-8")
    (manifests / "repo-sensemaker.yaml").write_text(
        """schema_version: 1
skill_id: repo-sensemaker
domain: engineering
responsibilities: [repository_sensemaking]
consumes: [user_intent]
produces: [repository_sensemaking_brief]
semantic_concepts: [Intent, TargetSnapshot, Observation, Evidence, Claim, Uncertainty, Responsibility, Artifact]
repository_mutation: false
""",
        encoding="utf-8",
    )
    (packs / "engineering.yaml").write_text(
        """schema_version: 1
domain_id: engineering
capability_ledger: ledger.md
skill_manifests: [skill-manifests/repo-sensemaker.yaml]
responsibility_vocabulary: [repository_sensemaking]
artifact_contracts: [repository_sensemaking_brief]
qualification_policy: policy.md
""",
        encoding="utf-8",
    )

    result = validate_conformance(manifests, domain_packs_dir=packs, repo_root=tmp_path)
    assert result.valid, result.diagnostics
    assert result.semantic_truth_established is False


def test_conformance_rejects_unknown_semantic_concept(tmp_path):
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    (manifests / "bad.yaml").write_text(
        """schema_version: 1
skill_id: bad
domain: engineering
responsibilities: []
consumes: []
produces: []
semantic_concepts: [MagicTruth]
repository_mutation: false
""",
        encoding="utf-8",
    )

    result = validate_conformance(manifests)
    assert not result.valid
    assert "SKILL_MANIFEST_UNKNOWN_SEMANTIC_CONCEPT" in {item.code for item in result.diagnostics}


def test_conformance_rejects_semantic_authority_fields(tmp_path):
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    (manifests / "bad.yaml").write_text(
        """schema_version: 1
skill_id: bad
domain: engineering
responsibilities: []
consumes: []
produces: []
semantic_concepts: [Claim]
repository_mutation: false
auto_route: true
""",
        encoding="utf-8",
    )

    result = validate_conformance(manifests)
    assert not result.valid
    assert "SKILL_MANIFEST_PROHIBITED_AUTHORITY_FIELD" in {item.code for item in result.diagnostics}
