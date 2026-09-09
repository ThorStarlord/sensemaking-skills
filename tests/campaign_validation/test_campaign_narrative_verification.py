"""Package 2 qualification for mechanical Campaign narrative verification."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from sensemaking_skills.campaign_semantics import (
    CampaignState,
    ClaimEvidence,
    TransitionRecord,
)
from sensemaking_skills.campaigns import (
    CampaignIntegrityError,
    CampaignNarrativeContractError,
    CampaignNarrativeVerificationService,
    CampaignService,
    CampaignTransactionError,
    load_narrative_claims,
)


CAMPAIGN_ID = "CMP-NARRATIVE"
FACT = "Repository has a durable Campaign workspace"
QUESTION = "Which repository state was inspected?"


def _initialize(workspace: Path) -> CampaignService:
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id=CAMPAIGN_ID,
            mission="bind Campaign narrative to durable evidence without semantic routing",
            status="active",
            current_state="diagnosed",
            established_facts=(FACT,),
            resolved_questions=(QUESTION,),
        )
    )
    (workspace / "evidence" / "review.txt").write_text(
        "review evidence\n",
        encoding="utf-8",
    )
    return service


def _claim(
    text: str = FACT,
    *,
    scope: str = "established_fact",
    evidence: tuple[str, ...] = ("evidence/review.txt",),
) -> ClaimEvidence:
    return ClaimEvidence(
        claim=text,
        scope=scope,
        method="agent_cross_check",
        coverage=("bounded narrative claim",),
        claim_strength="supported",
        evidence=evidence,
    )


def test_verify_binds_current_narrative_to_exact_durable_evidence(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    service = CampaignNarrativeVerificationService(workspace)

    result = service.verify(
        receipt_id="NV-001",
        claims=(
            _claim("diagnosed", scope="current_state"),
            _claim(),
            _claim(QUESTION, scope="resolved_question"),
        ),
    )

    assert result.receipt.campaign_id == CAMPAIGN_ID
    assert result.receipt.receipt_id == "NV-001"
    assert result.receipt.state_sha256
    assert result.receipt.evidence_sha256.keys() == {"evidence/review.txt"}
    assert result.receipt_ref.startswith("narrative-verifications/NV-001--")
    assert result.receipt_ref.endswith(f"{result.receipt_sha256}.yaml")
    assert (workspace / result.receipt_ref).is_file()

    history = service.history()
    assert len(history) == 1
    assert history[0].receipt_id == "NV-001"
    assert history[0].current_state_match is True
    assert history[0].claim_count == 3
    assert history[0].evidence_refs == ("evidence/review.txt",)


def test_yaml_claim_document_loads_strict_claim_evidence(tmp_path: Path) -> None:
    path = tmp_path / "claims.yaml"
    path.write_text(
        (
            "claims:\n"
            "  - claim: Repository has a durable Campaign workspace\n"
            "    scope: established_fact\n"
            "    method: agent_cross_check\n"
            "    coverage: [bounded narrative claim]\n"
            "    claim_strength: supported\n"
            "    evidence: [evidence/review.txt]\n"
        ),
        encoding="utf-8",
    )

    claims = load_narrative_claims(path)

    assert claims == (_claim(),)


def test_claim_document_rejects_unknown_fields(tmp_path: Path) -> None:
    path = tmp_path / "claims.yaml"
    path.write_text(
        (
            "claims:\n"
            "  - claim: x\n"
            "    scope: established_fact\n"
            "    method: m\n"
            "    coverage: [c]\n"
            "    claim_strength: supported\n"
            "    evidence: [evidence/review.txt]\n"
            "    semantic_truth: true\n"
        ),
        encoding="utf-8",
    )

    with pytest.raises(CampaignNarrativeContractError, match="unknown"):
        load_narrative_claims(path)


def test_unknown_narrative_scope_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(CampaignNarrativeContractError, match="scope"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="NV-UNKNOWN-SCOPE",
            claims=(_claim(scope="semantic_truth"),),
        )


def test_claim_without_evidence_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(CampaignNarrativeContractError, match="at least one"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="NV-NO-EVIDENCE",
            claims=(_claim(evidence=()),),
        )


def test_claim_must_be_exact_member_of_current_campaign_narrative(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(CampaignTransactionError, match="not an exact member"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="NV-INVENTED",
            claims=(_claim("This claim was inferred but never recorded"),),
        )


def test_orphan_artifact_cannot_be_used_as_narrative_evidence(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    orphan = workspace / "artifacts" / "orphan.md"
    orphan.write_text("not admitted\n", encoding="utf-8")

    with pytest.raises(CampaignTransactionError, match="non-durable evidence"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="NV-ORPHAN",
            claims=(_claim(evidence=("artifacts/orphan.md",)),),
        )


def test_missing_evidence_ref_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(CampaignTransactionError, match="non-durable evidence"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="NV-MISSING",
            claims=(_claim(evidence=("evidence/missing.txt",)),),
        )


def test_unsafe_receipt_id_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(CampaignTransactionError, match="receipt id"):
        CampaignNarrativeVerificationService(workspace).verify(
            receipt_id="../escape",
            claims=(_claim(),),
        )


def test_receipt_ids_are_append_only(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    service = CampaignNarrativeVerificationService(workspace)
    service.verify(receipt_id="NV-APPEND", claims=(_claim(),))

    with pytest.raises(CampaignTransactionError, match="already exists"):
        service.verify(receipt_id="NV-APPEND", claims=(_claim(),))


def test_evidence_byte_mutation_fails_closed(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    service = CampaignNarrativeVerificationService(workspace)
    service.verify(receipt_id="NV-BYTES", claims=(_claim(),))
    (workspace / "evidence" / "review.txt").write_text(
        "mutated after verification\n",
        encoding="utf-8",
    )

    with pytest.raises(CampaignIntegrityError) as exc_info:
        service.history()

    assert "NARRATIVE_VERIFICATION_EVIDENCE_DIGEST_MISMATCH" in exc_info.value.diagnostic_codes


def test_evidence_deletion_fails_closed(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    service = CampaignNarrativeVerificationService(workspace)
    service.verify(receipt_id="NV-DELETE", claims=(_claim(),))
    (workspace / "evidence" / "review.txt").unlink()

    with pytest.raises(CampaignIntegrityError) as exc_info:
        service.history()

    assert "NARRATIVE_VERIFICATION_EVIDENCE_MISSING" in exc_info.value.diagnostic_codes


def test_receipt_tampering_fails_closed(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    service = CampaignNarrativeVerificationService(workspace)
    result = service.verify(receipt_id="NV-TAMPER", claims=(_claim(),))
    path = workspace / result.receipt_ref
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload["claims"][0]["method"] = "rewritten_after_verification"
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    with pytest.raises(CampaignIntegrityError) as exc_info:
        service.history()

    assert "NARRATIVE_VERIFICATION_DIGEST_MISMATCH" in exc_info.value.diagnostic_codes


def test_receipt_becomes_historical_after_legitimate_state_transition(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    campaign = _initialize(workspace)
    narrative = CampaignNarrativeVerificationService(workspace)
    narrative.verify(receipt_id="NV-HISTORY", claims=(_claim(),))

    current = campaign.resume().state
    campaign.record_transition(
        new_state=replace(current, current_state="bounded_work"),
        transition=TransitionRecord(
            id="TR-001",
            from_state="diagnosed",
            to_state="bounded_work",
            evidence=(),
            decision="Agent explicitly advanced after reviewing the verified bindings",
            authority=current.authority,
        ),
    )

    history = narrative.history()
    assert len(history) == 1
    assert history[0].current_state_match is False
    assert history[0].state_sha256


def test_verification_does_not_mutate_campaign_state_or_history(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    campaign = _initialize(workspace)
    before = campaign.resume()

    CampaignNarrativeVerificationService(workspace).verify(
        receipt_id="NV-NONSEMANTIC",
        claims=(_claim(),),
    )

    after = campaign.resume()
    assert after.state == before.state
    assert after.transitions == before.transitions
    assert after.trace == before.trace
