"""Tests for DurableReservationManager (Phase 4, #120)."""

from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path
import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import build_valid_bundle, _ANCHOR_NOW

from sensemaking_skills.campaign_accounting import (
    BUDGET_EXCEEDED_ATTEMPT_SLOTS,
    BUDGET_EXCEEDED_CONFIGURATION_SLOTS,
    CAMPAIGN_EXPIRED,
    CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH,
    RESERVATION_EXISTS_FOR_ATTEMPT,
    AttemptState,
    CampaignAccountingError,
    DurableReservationManager,
    verify_cross_document_campaign_id,
)


def test_verify_cross_document_campaign_id_success() -> None:
    verify_cross_document_campaign_id("EXP-0001", "EXP-0001", "EXP-0001", "EXP-0001")


def test_verify_cross_document_campaign_id_mismatch() -> None:
    with pytest.raises(CampaignAccountingError) as exc_info:
        verify_cross_document_campaign_id("EXP-0001", "EXP-0002", "EXP-0001", "EXP-0001")
    assert exc_info.value.failure_code == CROSS_DOCUMENT_CAMPAIGN_ID_MISMATCH


def test_successful_reservation(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    manager = DurableReservationManager(tmp_path)

    request_meta = {
        "campaign_id": bundle.policy.campaign_id,
        "intended_model": "claude-sonnet-5",
    }
    attempt_id = "00000000-0000-0000-0000-000000000001"
    config_id = bundle.configuration.configuration_id

    now = _ANCHOR_NOW
    res = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=config_id,
        request_metadata=request_meta,
        now=now,
    )

    assert res.attempt_id == attempt_id
    assert res.campaign_id == bundle.policy.campaign_id
    assert res.configuration_id == config_id
    assert res.state == AttemptState.RESERVED.value

    # Check filesystem
    attempt_dir = tmp_path / bundle.policy.campaign_id / "attempts" / attempt_id
    assert attempt_dir.exists()
    assert (attempt_dir / "reservation.yaml").exists()
    assert (attempt_dir / "request-metadata.json").exists()

    res_content = yaml.safe_load((attempt_dir / "reservation.yaml").read_text(encoding="utf-8"))
    assert res_content["attempt_id"] == attempt_id
    assert res_content["state"] == "RESERVED"


def test_reservation_duplicate_attempt_id(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    manager = DurableReservationManager(tmp_path)

    request_meta = {"campaign_id": bundle.policy.campaign_id}
    attempt_id = "00000000-0000-0000-0000-000000000001"
    config_id = bundle.configuration.configuration_id
    now = _ANCHOR_NOW

    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=config_id,
        request_metadata=request_meta,
        now=now,
    )

    # Attempting to reserve same attempt_id again must fail
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id=attempt_id,
            configuration_id=config_id,
            request_metadata=request_meta,
            now=now,
        )
    assert exc_info.value.failure_code == RESERVATION_EXISTS_FOR_ATTEMPT


def test_reservation_budget_exceeded_attempt_slots(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 1})
    manager = DurableReservationManager(tmp_path)

    request_meta = {"campaign_id": bundle.policy.campaign_id}
    config_id = bundle.configuration.configuration_id
    now = _ANCHOR_NOW

    # First reservation consumes the 1 available slot
    res1 = manager.reserve_attempt(
        bundle=bundle,
        attempt_id="00000000-0000-0000-0000-000000000001",
        configuration_id=config_id,
        request_metadata=request_meta,
        now=now,
    )
    # Complete attempt 1 so concurrency doesn't block it
    from sensemaking_skills.campaign_accounting import AttemptOutcomeRecorder
    recorder = AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, res1.attempt_id)
    recorder.record_pre_invocation_abort("aborted for test", now=now)

    # Second reservation must fail attempt_slots budget
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id="00000000-0000-0000-0000-000000000002",
            configuration_id=config_id,
            request_metadata=request_meta,
            now=now,
        )
    assert exc_info.value.failure_code == BUDGET_EXCEEDED_ATTEMPT_SLOTS


def test_reservation_budget_exceeded_configuration_slots(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 5, "max_attempts_per_configuration": 1})
    manager = DurableReservationManager(tmp_path)

    request_meta = {"campaign_id": bundle.policy.campaign_id}
    config_id = bundle.configuration.configuration_id
    now = _ANCHOR_NOW

    res1 = manager.reserve_attempt(
        bundle=bundle,
        attempt_id="00000000-0000-0000-0000-000000000001",
        configuration_id=config_id,
        request_metadata=request_meta,
        now=now,
    )
    from sensemaking_skills.campaign_accounting import AttemptOutcomeRecorder
    recorder = AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, res1.attempt_id)
    recorder.record_pre_invocation_abort("aborted for test", now=now)

    # Second attempt under same configuration must fail configuration slots budget
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id="00000000-0000-0000-0000-000000000002",
            configuration_id=config_id,
            request_metadata=request_meta,
            now=now,
        )
    assert exc_info.value.failure_code == BUDGET_EXCEEDED_CONFIGURATION_SLOTS


def test_reservation_concurrency_ceiling(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 5})
    manager = DurableReservationManager(tmp_path)

    request_meta = {"campaign_id": bundle.policy.campaign_id}
    config_id = bundle.configuration.configuration_id
    now = _ANCHOR_NOW

    # First attempt reserved and still active (non-terminal)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id="00000000-0000-0000-0000-000000000001",
        configuration_id=config_id,
        request_metadata=request_meta,
        now=now,
    )

    # Second attempt reserved while attempt 1 is active must fail concurrency
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id="00000000-0000-0000-0000-000000000002",
            configuration_id=config_id,
            request_metadata=request_meta,
            now=now,
        )
    assert exc_info.value.failure_code == "CONCURRENCY_CEILING_EXCEEDED"


def test_reservation_expired_policy(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    manager = DurableReservationManager(tmp_path)

    request_meta = {"campaign_id": bundle.policy.campaign_id}
    config_id = bundle.configuration.configuration_id
    # Time after validity_window
    expired_time = _ANCHOR_NOW + timedelta(days=400)

    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id="00000000-0000-0000-0000-000000000001",
            configuration_id=config_id,
            request_metadata=request_meta,
            now=expired_time,
        )
    assert exc_info.value.failure_code == CAMPAIGN_EXPIRED
