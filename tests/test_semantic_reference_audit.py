"""B7 semantic-reference resolution/audit contracts."""

from __future__ import annotations

from sensemaking_skills.semantic_architecture.reference_audit import (
    IntegrityEffect,
    ReferenceClass,
    ReferenceResolution,
    audit_semantic_references,
)


def _entry(**overrides):
    entry = {
        "entry_id": "S1",
        "source_skill": "repo-sensemaker",
        "artifact_ref": "brief.md",
        "target_ref": "external:test",
        "evidence_refs": [],
        "claim_refs": [],
        "uncertainty_refs": [],
        "parent_entry_ids": [],
        "semantic_profile_ref": None,
    }
    entry.update(overrides)
    return {"entry": entry}


def _by_field(result):
    return {item.field: item for item in result.items}


def test_audit_resolves_campaign_evidence_and_admitted_artifact_refs():
    artifact = "artifacts/repository_sensemaking_brief/abc123.md"
    evidence = "evidence/probe-report.yaml"
    result = audit_semantic_references(
        [
            _entry(
                artifact_ref=artifact,
                evidence_refs=[evidence],
            )
        ],
        campaign_evidence_refs=(artifact, evidence),
        active_uncertainty_ids=(),
    )

    fields = _by_field(result)
    assert fields["artifact_ref"].resolution is ReferenceResolution.RESOLVED
    assert fields["artifact_ref"].reference_class is ReferenceClass.CAMPAIGN_INTERNAL
    assert fields["evidence_refs[0]"].resolution is ReferenceResolution.RESOLVED
    assert fields["evidence_refs[0]"].resolver == "campaign.evidence_refs"
    assert result.integrity_ok
    assert result.resolved_count == 2
    assert result.semantic_truth_established is False


def test_audit_resolves_matching_campaign_target_ref():
    result = audit_semantic_references(
        [_entry(target_ref="target-snapshot-sha256:abc123")],
        campaign_evidence_refs=(),
        active_uncertainty_ids=(),
        campaign_target_ref="target-snapshot-sha256:abc123",
    )
    fields = _by_field(result)
    assert fields["target_ref"].resolution is ReferenceResolution.RESOLVED
    assert fields["target_ref"].reference_class is ReferenceClass.CAMPAIGN_INTERNAL
    assert fields["target_ref"].integrity_effect is IntegrityEffect.PASS


def test_audit_marks_mismatching_campaign_target_ref_dangling_and_failed():
    result = audit_semantic_references(
        [_entry(target_ref="target-snapshot-sha256:old")],
        campaign_evidence_refs=(),
        active_uncertainty_ids=(),
        campaign_target_ref="target-snapshot-sha256:current",
    )
    fields = _by_field(result)
    assert fields["target_ref"].resolution is ReferenceResolution.DANGLING
    assert fields["target_ref"].integrity_effect is IntegrityEffect.FAIL
    assert not result.integrity_ok


def test_audit_leaves_target_ref_not_addressable_without_campaign_authority():
    result = audit_semantic_references(
        [_entry(target_ref="external:target")],
        campaign_evidence_refs=(),
        active_uncertainty_ids=(),
    )
    fields = _by_field(result)
    assert fields["target_ref"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["target_ref"].integrity_effect is IntegrityEffect.INFORMATIONAL
    assert result.integrity_ok


def test_audit_marks_missing_campaign_local_refs_dangling_but_opaque_refs_informational():
    result = audit_semantic_references(
        [
            _entry(
                artifact_ref="brief.md",
                evidence_refs=["evidence/missing.txt"],
                claim_refs=["C1"],
                uncertainty_refs=["U-missing"],
                semantic_profile_ref="profile.json",
            )
        ],
        campaign_evidence_refs=(),
        active_uncertainty_ids=("U-current",),
    )

    fields = _by_field(result)
    assert fields["evidence_refs[0]"].resolution is ReferenceResolution.DANGLING
    assert fields["evidence_refs[0]"].integrity_effect is IntegrityEffect.FAIL
    assert fields["artifact_ref"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["artifact_ref"].reference_class is ReferenceClass.LEGACY_OPAQUE
    assert fields["artifact_ref"].integrity_effect is IntegrityEffect.INFORMATIONAL
    assert fields["claim_refs[0]"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["uncertainty_refs[0]"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["semantic_profile_ref"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert not result.integrity_ok
    assert result.dangling_count == 1
    assert result.not_addressable_count == 5


def test_audit_resolves_only_currently_represented_uncertainty_without_inventing_namespace():
    result = audit_semantic_references(
        [_entry(uncertainty_refs=["U-current", "U-other"])],
        campaign_evidence_refs=(),
        active_uncertainty_ids=("U-current",),
    )

    fields = _by_field(result)
    assert fields["uncertainty_refs[0]"].resolution is ReferenceResolution.RESOLVED
    assert fields["uncertainty_refs[0]"].resolver == "campaign.active_uncertainty"
    assert fields["uncertainty_refs[1]"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert result.integrity_ok


def test_audit_without_campaign_authority_does_not_guess_filesystem_resolution():
    result = audit_semantic_references(
        [_entry(artifact_ref="artifacts/x/abc.md", evidence_refs=["evidence/existing.txt"])],
        campaign_evidence_refs=None,
        active_uncertainty_ids=None,
    )

    fields = _by_field(result)
    assert fields["artifact_ref"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["evidence_refs[0]"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert result.integrity_ok
    assert result.dangling_count == 0


def test_audit_parent_resolution_is_ordered_and_mechanical():
    result = audit_semantic_references(
        [
            _entry(entry_id="S1"),
            _entry(entry_id="S2", parent_entry_ids=["S1"]),
            _entry(entry_id="S3", parent_entry_ids=["S4"]),
        ],
        campaign_evidence_refs=(),
        active_uncertainty_ids=(),
    )

    parents = [item for item in result.items if item.field.startswith("parent_entry_ids")]
    assert parents[0].resolution is ReferenceResolution.RESOLVED
    assert parents[0].resolver == "semantic_state.entry_id"
    assert parents[1].resolution is ReferenceResolution.DANGLING
    assert not result.integrity_ok


def test_claim_and_profile_refs_remain_unaddressable_not_invalid():
    result = audit_semantic_references(
        [_entry(claim_refs=["C1"], semantic_profile_ref="semantic-profile.json")],
        campaign_evidence_refs=(),
        active_uncertainty_ids=(),
    )

    fields = _by_field(result)
    assert fields["claim_refs[0]"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert fields["semantic_profile_ref"].resolution is ReferenceResolution.NOT_ADDRESSABLE
    assert result.integrity_ok
    assert result.integrity_failure_count == 0
