from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import pytest
import yaml
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignState,
    Responsibility,
    TransitionRecord,
)
from sensemaking_skills.campaigns import (
    CampaignIntegrityError,
    CampaignService,
    CampaignTransactionError,
)
from sensemaking_skills.campaigns.admission import (
    ArtifactAdmission,
    canonical_json_digest,
    dump_artifact_admission,
)
from sensemaking_skills.campaigns.decisions import (
    AdvanceDecision,
    CampaignDecisionService,
)
from sensemaking_skills.campaigns.lineage import CampaignLineageService
from sensemaking_skills.cli import cli


def _state(*, current_state: str = "initialized") -> CampaignState:
    return CampaignState(
        campaign_id="CMP-P8",
        mission="prove artifact and evidence lineage",
        status="active",
        current_state=current_state,
    )


def _responsibility(*, evidence: tuple[str, ...] = ()) -> Responsibility:
    return Responsibility(
        id="R-P8",
        statement="perform the explicitly authored next responsibility",
        trigger_evidence=evidence,
        decision_blocked="whether the bounded P8 responsibility is complete",
        scope="P8 qualification",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("lineage is durable and reconstructible",),
    )


def _initialize(tmp_path):
    workspace = tmp_path / "CMP-P8"
    CampaignService(workspace).initialize(_state())
    return workspace


def _write_raw_evidence(workspace, name: str, data: bytes) -> str:
    path = workspace / "evidence" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path.relative_to(workspace).as_posix()


def _advance(workspace, *, transition_id: str, evidence: tuple[str, ...]):
    return CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id=transition_id,
            to_state=f"state-{transition_id}",
            decision="the agent explicitly cites these evidence refs",
            evidence=evidence,
            next_responsibility=_responsibility(evidence=evidence),
        )
    )


def _install_admitted_artifact(workspace) -> tuple[str, str, str]:
    artifact_id = "brief"
    artifact_bytes = b"validated artifact bytes\n"
    artifact_sha = hashlib.sha256(artifact_bytes).hexdigest()
    artifact_ref = f"artifacts/{artifact_id}/{artifact_sha}.md"
    artifact_path = workspace / artifact_ref
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_bytes(artifact_bytes)

    timestamp = "2026-09-08T12:00:00Z"
    validator = "manual-test-validator"
    validation_result = {
        "valid": True,
        "artifact_id": artifact_id,
        "validator": validator,
        "validation_timestamp": timestamp,
        "errors": [],
    }
    admission = ArtifactAdmission(
        campaign_id="CMP-P8",
        artifact_id=artifact_id,
        artifact_ref=artifact_ref,
        artifact_sha256=artifact_sha,
        validator=validator,
        validation_timestamp=timestamp,
        router_sha256="1" * 64,
        validator_sha256="2" * 64,
        validation_result_sha256=canonical_json_digest(validation_result),
        validation_result=validation_result,
    )
    payload = dump_artifact_admission(admission)
    receipt_digest = canonical_json_digest(payload)
    receipt_ref = f"admissions/{artifact_id}/{receipt_digest}.yaml"
    receipt_path = workspace / receipt_ref
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return artifact_ref, receipt_ref, artifact_sha


def test_raw_evidence_consumption_preserves_exact_bytes_and_reports_source_drift(tmp_path):
    workspace = _initialize(tmp_path)
    original = b"evidence used by the authored decision\n"
    evidence_ref = _write_raw_evidence(workspace, "brief.md", original)

    _advance(workspace, transition_id="TR-P8-RAW", evidence=(evidence_ref,))
    lineage = CampaignLineageService(workspace).inspect()

    assert lineage.transitions[0].binding_status == "bound"
    assert lineage.transitions[0].receipt_ref is not None
    edge = lineage.consumption_edges[0]
    expected_sha = hashlib.sha256(original).hexdigest()
    assert edge.evidence_ref == evidence_ref
    assert edge.kind == "raw_evidence"
    assert edge.consumed_sha256 == expected_sha
    assert edge.immutable_ref == f"lineage/evidence/{expected_sha}"
    assert edge.source_matches_consumed_bytes is True
    assert (workspace / edge.immutable_ref).read_bytes() == original

    # Raw source evidence may later drift, but P8 retains the exact consumed
    # bytes instead of silently rewriting history to the new file contents.
    (workspace / evidence_ref).write_bytes(b"later edited source evidence\n")
    drifted = CampaignLineageService(workspace).inspect()
    drifted_edge = drifted.consumption_edges[0]
    assert drifted_edge.consumed_sha256 == expected_sha
    assert drifted_edge.source_matches_consumed_bytes is False
    assert (workspace / drifted_edge.immutable_ref).read_bytes() == original


def test_admitted_artifact_reuses_p4_content_address_and_exposes_admission_provenance(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, receipt_ref, artifact_sha = _install_admitted_artifact(workspace)

    _advance(
        workspace,
        transition_id="TR-P8-ADMITTED",
        evidence=(artifact_ref, receipt_ref),
    )
    lineage = CampaignLineageService(workspace).inspect()
    by_ref = {edge.evidence_ref: edge for edge in lineage.consumption_edges}

    artifact_edge = by_ref[artifact_ref]
    assert artifact_edge.kind == "admitted_artifact"
    assert artifact_edge.consumed_sha256 == artifact_sha
    assert artifact_edge.immutable_ref == artifact_ref
    assert artifact_edge.source_matches_consumed_bytes is True
    assert receipt_ref in artifact_edge.provenance["admission_refs"]

    receipt_edge = by_ref[receipt_ref]
    assert receipt_edge.kind == "admission_receipt"
    assert receipt_edge.immutable_ref.startswith("lineage/evidence/")
    assert receipt_edge.provenance["artifact_ref"] == artifact_ref
    assert receipt_edge.provenance["artifact_sha256"] == artifact_sha

    evidence_records = {item.ref: item for item in lineage.evidence}
    assert evidence_records[artifact_ref].immutable_by_source_contract is True
    assert evidence_records[receipt_ref].immutable_by_source_contract is False


def test_unadmitted_artifact_is_not_evidence_lineage_and_cannot_be_consumed(tmp_path):
    workspace = _initialize(tmp_path)
    orphan = workspace / "artifacts" / "orphan" / "not-admitted.md"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text("not admitted", encoding="utf-8")
    orphan_ref = orphan.relative_to(workspace).as_posix()

    lineage = CampaignLineageService(workspace).inspect()
    assert orphan_ref not in {item.ref for item in lineage.evidence}

    with pytest.raises(CampaignTransactionError, match="missing evidence"):
        CampaignLineageService(workspace).prepare_consumption(
            transition_id="TR-ORPHAN",
            evidence_refs=(orphan_ref,),
        )


def test_direct_p2_transition_remains_honestly_legacy_unbound(tmp_path):
    workspace = _initialize(tmp_path)
    evidence_ref = _write_raw_evidence(workspace, "legacy.md", b"legacy bytes\n")
    service = CampaignService(workspace)
    current = service.resume().state
    new_state = replace(current, current_state="legacy-transition")
    service.record_transition(
        new_state=new_state,
        transition=TransitionRecord(
            id="TR-LEGACY",
            from_state="initialized",
            to_state="legacy-transition",
            evidence=(evidence_ref,),
            decision="legacy lower-level P2 transition",
            authority=None,
        ),
    )

    lineage = CampaignLineageService(workspace).inspect()
    assert lineage.transitions[0].binding_status == "legacy_unbound"
    assert lineage.transitions[0].receipt_ref is None
    edge = lineage.consumption_edges[0]
    assert edge.binding_status == "legacy_unbound"
    assert edge.consumed_sha256 is None
    assert edge.immutable_ref is None


def test_tampered_immutable_snapshot_fails_closed(tmp_path):
    workspace = _initialize(tmp_path)
    evidence_ref = _write_raw_evidence(workspace, "tamper.md", b"original\n")
    _advance(workspace, transition_id="TR-TAMPER", evidence=(evidence_ref,))

    first = CampaignLineageService(workspace).inspect()
    immutable_ref = first.consumption_edges[0].immutable_ref
    assert immutable_ref is not None
    (workspace / immutable_ref).write_bytes(b"tampered snapshot\n")

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignLineageService(workspace).inspect()
    assert "LINEAGE_IMMUTABLE_EVIDENCE_DIGEST_MISMATCH" in exc_info.value.diagnostic_codes


def test_failed_semantic_commit_leaves_orphan_intent_not_false_consumption_edge(tmp_path):
    workspace = _initialize(tmp_path)
    evidence_ref = _write_raw_evidence(workspace, "orphan-intent.md", b"intent bytes\n")
    lineage_service = CampaignLineageService(workspace)

    receipt_ref = lineage_service.prepare_consumption(
        transition_id="TR-NEVER-COMMITTED",
        evidence_refs=(evidence_ref,),
    )
    assert receipt_ref is not None

    lineage = lineage_service.inspect()
    assert lineage.transitions == ()
    assert lineage.consumption_edges == ()
    assert receipt_ref in lineage.orphan_intent_refs


def test_conflicting_precommit_intent_for_same_transition_id_fails_closed(tmp_path):
    workspace = _initialize(tmp_path)
    first = _write_raw_evidence(workspace, "first.md", b"first\n")
    second = _write_raw_evidence(workspace, "second.md", b"second\n")
    lineage_service = CampaignLineageService(workspace)

    lineage_service.prepare_consumption(
        transition_id="TR-CONFLICT",
        evidence_refs=(first,),
    )
    with pytest.raises(CampaignTransactionError, match="different lineage"):
        lineage_service.prepare_consumption(
            transition_id="TR-CONFLICT",
            evidence_refs=(second,),
        )


def test_lineage_cli_json_is_read_only_and_contains_no_recommendation_semantics(tmp_path):
    workspace = _initialize(tmp_path)
    evidence_ref = _write_raw_evidence(workspace, "cli.md", b"cli lineage\n")
    _advance(workspace, transition_id="TR-CLI", evidence=(evidence_ref,))

    before = {
        path.relative_to(workspace).as_posix(): path.read_bytes()
        for path in workspace.rglob("*")
        if path.is_file()
    }
    result = CliRunner().invoke(
        cli,
        ["campaign", "lineage", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_LINEAGE"
    assert payload["transition_count"] == 1
    assert payload["consumption_edge_count"] == 1
    assert payload["transitions"][0]["binding_status"] == "bound"

    encoded = json.dumps(payload, sort_keys=True).lower()
    for forbidden in (
        "recommended_capability",
        "recommended_action",
        "selected_capability",
        "evidence_sufficient",
        "semantic_score",
        "rank",
    ):
        assert forbidden not in encoded

    after = {
        path.relative_to(workspace).as_posix(): path.read_bytes()
        for path in workspace.rglob("*")
        if path.is_file()
    }
    assert after == before
