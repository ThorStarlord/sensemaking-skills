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
    AdvanceDecision,
    ArtifactAdmission,
    CampaignDecisionService,
    CampaignIntegrityError,
    CampaignReconciliationService,
    CampaignService,
)
from sensemaking_skills.campaigns.admission import (
    canonical_json_digest,
    dump_artifact_admission,
)
from sensemaking_skills.cli import cli


def _initialize(tmp_path):
    workspace = tmp_path / "CMP-P9"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-P9",
            mission="prove reconciliation lifecycle without semantic routing",
            status="active",
            current_state="initialized",
        )
    )
    return workspace


def _install_admitted_artifact(
    workspace,
    *,
    artifact_id: str,
    content: bytes,
    timestamp: str,
    marker: str,
) -> tuple[str, str, str]:
    digest = hashlib.sha256(content).hexdigest()
    artifact_ref = f"artifacts/{artifact_id}/{digest}.{marker}.md"
    artifact_path = workspace / artifact_ref
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_bytes(content)

    validator = "generic-test-validator"
    validation_result = {
        "valid": True,
        "artifact_id": artifact_id,
        "validator": validator,
        "validation_timestamp": timestamp,
        "errors": [],
    }
    admission = ArtifactAdmission(
        campaign_id="CMP-P9",
        artifact_id=artifact_id,
        artifact_ref=artifact_ref,
        artifact_sha256=digest,
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
    return artifact_ref, receipt_ref, digest


def _responsibility(*, evidence: tuple[str, ...]) -> Responsibility:
    return Responsibility(
        id="R-P9",
        statement="make the next semantic decision from admitted reconciliation evidence",
        trigger_evidence=evidence,
        decision_blocked="whether the Campaign should advance, defer, or close",
        scope="P9 qualification",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("explicit disposition is durably reconstructible",),
    )


def _advance_with_report(workspace, artifact_ref: str, transition_id: str = "TR-P9"):
    return CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id=transition_id,
            to_state="post_reconciliation_decision",
            decision="the agent explicitly consumed reconciliation evidence",
            evidence=(artifact_ref,),
            next_responsibility=_responsibility(evidence=(artifact_ref,)),
        )
    )


def test_no_admitted_reconciliation_evidence_is_empty(tmp_path):
    workspace = _initialize(tmp_path)

    result = CampaignReconciliationService(workspace).inspect()

    assert result.campaign_id == "CMP-P9"
    assert result.reports == ()
    assert result.disposition_required_count == 0
    assert result.disposition_recorded_count == 0
    assert result.legacy_unbound_count == 0


def test_admitted_reconciliation_report_requires_explicit_disposition(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, receipt_ref, digest = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"claims: all verified\nrecommendations: none\n",
        timestamp="2026-09-08T14:00:00Z",
        marker="one",
    )

    result = CampaignReconciliationService(workspace).inspect()

    assert len(result.reports) == 1
    report = result.reports[0]
    assert report.artifact_id == "reconciliation_report"
    assert report.artifact_ref == artifact_ref
    assert report.artifact_sha256 == digest
    assert [item.ref for item in report.admissions] == [receipt_ref]
    assert report.disposition_status == "disposition_required"
    assert report.disposition_required is True
    assert report.bound_transition_ids == ()
    assert report.legacy_unbound_transition_ids == ()
    assert result.disposition_required_count == 1


def test_repair_verification_report_is_independent_admitted_evidence(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="repair_verification_report",
        content=b"findings_closed: all\nfindings_remaining: []\n",
        timestamp="2026-09-08T14:01:00Z",
        marker="verify",
    )

    result = CampaignReconciliationService(workspace).inspect()

    assert [item.artifact_id for item in result.reports] == [
        "repair_verification_report"
    ]
    assert result.reports[0].artifact_ref == artifact_ref
    assert result.reports[0].disposition_status == "disposition_required"


def test_unadmitted_artifact_like_file_is_ignored(tmp_path):
    workspace = _initialize(tmp_path)
    orphan = workspace / "artifacts" / "reconciliation_report" / "orphan.md"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text("artifact_id: reconciliation_report", encoding="utf-8")

    result = CampaignReconciliationService(workspace).inspect()

    assert result.reports == ()


def test_explicit_p5_transition_consuming_report_records_disposition(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"one admitted reconciliation report\n",
        timestamp="2026-09-08T14:02:00Z",
        marker="consume",
    )

    _advance_with_report(workspace, artifact_ref, transition_id="TR-P9-BOUND")
    result = CampaignReconciliationService(workspace).inspect()

    report = result.reports[0]
    assert report.disposition_status == "disposition_recorded"
    assert report.disposition_required is False
    assert report.bound_transition_ids == ("TR-P9-BOUND",)
    assert report.legacy_unbound_transition_ids == ()
    assert result.disposition_required_count == 0
    assert result.disposition_recorded_count == 1


def test_direct_p2_reference_remains_legacy_unbound_and_requires_disposition(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"legacy direct P2 reference\n",
        timestamp="2026-09-08T14:03:00Z",
        marker="legacy",
    )

    service = CampaignService(workspace)
    current = service.resume().state
    service.record_transition(
        new_state=replace(current, current_state="legacy_reconciliation_reference"),
        transition=TransitionRecord(
            id="TR-P9-LEGACY",
            from_state="initialized",
            to_state="legacy_reconciliation_reference",
            evidence=(artifact_ref,),
            decision="historical lower-level transition",
            authority=None,
        ),
    )

    result = CampaignReconciliationService(workspace).inspect()
    report = result.reports[0]

    assert report.disposition_status == "legacy_unbound"
    assert report.disposition_required is True
    assert report.bound_transition_ids == ()
    assert report.legacy_unbound_transition_ids == ("TR-P9-LEGACY",)
    assert result.legacy_unbound_count == 1
    assert result.disposition_required_count == 1


def test_verdict_like_content_never_changes_campaign_state_automatically(tmp_path):
    workspace = _initialize(tmp_path)
    _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=(
            b"classification: verified\nclassification: disputed\n"
            b"recommendation: close campaign\n"
        ),
        timestamp="2026-09-08T14:04:00Z",
        marker="verdict",
    )
    _install_admitted_artifact(
        workspace,
        artifact_id="repair_verification_report",
        content=(
            b"findings_closed: all\nfindings_remaining: none\n"
            b"verdict: complete\n"
        ),
        timestamp="2026-09-08T14:05:00Z",
        marker="closed",
    )

    before = CampaignService(workspace).resume().state
    result = CampaignReconciliationService(workspace).inspect()
    after = CampaignService(workspace).resume().state

    assert before == after
    assert after.current_state == "initialized"
    assert after.status == "active"
    assert len(result.reports) == 2
    assert all(item.disposition_required for item in result.reports)


def test_multiple_reports_are_deterministic_without_latest_or_superseded_semantics(tmp_path):
    workspace = _initialize(tmp_path)
    first_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"first report\n",
        timestamp="2026-09-08T14:09:00Z",
        marker="first",
    )
    second_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"second report\n",
        timestamp="2026-09-08T14:06:00Z",
        marker="second",
    )

    result = CampaignReconciliationService(workspace).inspect()

    assert [item.artifact_ref for item in result.reports] == sorted(
        [first_ref, second_ref]
    )
    assert result.disposition_required_count == 2


def test_tampered_admitted_artifact_fails_closed_through_p4_p8_integrity(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"original reconciliation bytes\n",
        timestamp="2026-09-08T14:07:00Z",
        marker="tamper",
    )
    (workspace / artifact_ref).write_bytes(b"tampered bytes\n")

    with pytest.raises(CampaignIntegrityError):
        CampaignReconciliationService(workspace).inspect()


def test_cli_json_is_read_only_and_contains_no_semantic_routing_fields(tmp_path):
    workspace = _initialize(tmp_path)
    artifact_ref, _, _ = _install_admitted_artifact(
        workspace,
        artifact_id="reconciliation_report",
        content=b"CLI reconciliation evidence\n",
        timestamp="2026-09-08T14:08:00Z",
        marker="cli",
    )

    before = {
        path.relative_to(workspace).as_posix(): path.read_bytes()
        for path in workspace.rglob("*")
        if path.is_file()
    }
    result = CliRunner().invoke(
        cli,
        ["campaign", "reconciliation", "--workspace", str(workspace), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)

    assert payload["code"] == "CAMPAIGN_RECONCILIATION"
    assert payload["report_count"] == 1
    assert payload["disposition_required_count"] == 1
    assert payload["reports"][0]["artifact_ref"] == artifact_ref
    assert payload["reports"][0]["disposition_status"] == "disposition_required"

    encoded = json.dumps(payload, sort_keys=True).lower()
    for forbidden in (
        "recommended_action",
        "recommended_capability",
        "selected_capability",
        "semantic_score",
        "evidence_sufficient",
        "repair_authorized",
        "auto_advance",
        "auto_close",
        "superseded",
        "latest_report",
    ):
        assert forbidden not in encoded

    after = {
        path.relative_to(workspace).as_posix(): path.read_bytes()
        for path in workspace.rglob("*")
        if path.is_file()
    }
    assert after == before
