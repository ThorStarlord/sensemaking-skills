"""Tests for AttemptOutcomeRecorder (Phase 4, #120)."""

from datetime import datetime, timezone
import json
import sys
from pathlib import Path
import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import build_valid_bundle, _ANCHOR_NOW

from sensemaking_skills.campaign_accounting import (
    ATTEMPT_NOT_RESERVED,
    BUDGET_EXCEEDED_PROVIDER_INVOCATIONS,
    AttemptState,
    CampaignAccountingError,
    DurableReservationManager,
    AttemptOutcomeRecorder,
)


def _make_reservation(tmp_path: Path, *, bundle=None, attempt_id: str = "00000000-0000-4000-8000-000000000001"):
    """Helper: create a durable reservation and return (bundle, attempt_id)."""
    if bundle is None:
        bundle = build_valid_bundle()
    manager = DurableReservationManager(tmp_path)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    return bundle, attempt_id


# ---------------------------------------------------------------------------
# record_pre_invocation_abort
# ---------------------------------------------------------------------------


def test_pre_invocation_abort_writes_result(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    result = recorder.record_pre_invocation_abort("test abort reason", now=_ANCHOR_NOW)

    assert result.state == AttemptState.ABORTED_BEFORE_INVOCATION.value
    assert result.attempt_id == attempt_id
    assert result.provider_invoked_at is None
    assert result.terminal_at == _ANCHOR_NOW.isoformat()

    # Attempt directory must contain attempt-result.yaml
    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "attempt-result.yaml").exists()

    raw_result = yaml.safe_load(
        (attempt_dir / "attempt-result.yaml").read_text(encoding="utf-8")
    )
    assert raw_result["state"] == "ABORTED_BEFORE_INVOCATION"


def test_pre_invocation_abort_ledger_event(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_pre_invocation_abort("abort for ledger test", now=_ANCHOR_NOW)

    from sensemaking_skills.campaign_accounting.ledger import CampaignLedger
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    events = ledger.read_events()

    states = [e.event_type for e in events if e.attempt_id == attempt_id]
    assert states == [
        AttemptState.RESERVED.value,
        AttemptState.ABORTED_BEFORE_INVOCATION.value,
    ]


def test_pre_invocation_abort_no_reservation_raises(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, "nonexistent-attempt")
    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_pre_invocation_abort("no reservation")
    assert exc_info.value.failure_code == ATTEMPT_NOT_RESERVED


# ---------------------------------------------------------------------------
# record_invoked
# ---------------------------------------------------------------------------


def test_record_invoked_transitions_state(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)

    from sensemaking_skills.campaign_accounting.ledger import CampaignLedger
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    events = ledger.read_events()
    states = [e.event_type for e in events if e.attempt_id == attempt_id]
    assert AttemptState.INVOKED.value in states


def test_record_invoked_budget_exceeded(tmp_path: Path) -> None:
    """max_provider_invocations=1 → second INVOKED must fail."""
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 2, "max_provider_invocations": 1})
    manager = DurableReservationManager(tmp_path)
    campaign_id = bundle.policy.campaign_id

    # First attempt: reserve → invoke → abort (to free concurrency slot)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id="00000000-0000-4000-8000-000000000001",
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": campaign_id},
        now=_ANCHOR_NOW,
    )
    recorder1 = AttemptOutcomeRecorder(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000001")
    recorder1.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder1.record_provider_failure("simulated failure", now=_ANCHOR_NOW)

    # Second attempt: reserve → try to invoke → budget exceeded
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id="00000000-0000-4000-8000-000000000002",
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": campaign_id},
        now=_ANCHOR_NOW,
    )
    recorder2 = AttemptOutcomeRecorder(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000002")
    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder2.record_invoked(bundle, now=_ANCHOR_NOW)
    assert exc_info.value.failure_code == BUDGET_EXCEEDED_PROVIDER_INVOCATIONS


# ---------------------------------------------------------------------------
# record_raw_output / record_validation_outcome
# ---------------------------------------------------------------------------


def test_record_raw_output_preserves_bytes(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)

    raw_bytes = b"raw provider response payload\n"
    rel_ref = recorder.record_raw_output(raw_bytes, extension="bin", now=_ANCHOR_NOW)

    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "raw-output.bin").exists()
    assert (attempt_dir / "raw-output.bin").read_bytes() == raw_bytes
    assert "raw-output.bin" in rel_ref


def test_record_validation_outcome_passed(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"output", now=_ANCHOR_NOW)
    result = recorder.record_validation_outcome(
        passed=True,
        details={"validator": "ok"},
        now=_ANCHOR_NOW,
    )

    assert result.state == AttemptState.VALIDATION_PASSED.value
    assert result.validation_outcome is not None
    assert result.validation_outcome["passed"] is True

    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "validation-result.json").exists()
    assert (attempt_dir / "attempt-result.yaml").exists()


def test_record_validation_outcome_failed(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"output", now=_ANCHOR_NOW)
    result = recorder.record_validation_outcome(
        passed=False,
        details={"validator": "schema mismatch"},
        now=_ANCHOR_NOW,
    )

    assert result.state == AttemptState.VALIDATION_FAILED.value
    assert result.validation_outcome["passed"] is False


def test_record_validation_outcome_requires_raw_output(tmp_path: Path) -> None:
    """Reaching validation without first capturing raw output must fail.

    The state machine itself rejects the jump INVOKED -> VALIDATION_*: a
    validation state with no OUTPUT_CAPTURED stage is an illegal transition,
    so no validation result can ever be written without preserved raw
    output.
    """
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    # Deliberately skip record_raw_output
    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_validation_outcome(passed=True, details={}, now=_ANCHOR_NOW)
    assert exc_info.value.failure_code == "ATTEMPT_STATE_INVALID_TRANSITION"
    # Nothing may have been written without a raw output first.
    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert not (attempt_dir / "validation-result.json").exists()
    assert not (attempt_dir / "attempt-result.yaml").exists()


# ---------------------------------------------------------------------------
# record_provider_failure
# ---------------------------------------------------------------------------


def test_record_provider_failure_terminal(tmp_path: Path) -> None:
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    result = recorder.record_provider_failure("provider timeout", now=_ANCHOR_NOW)

    assert result.state == AttemptState.PROVIDER_FAILED.value
    assert result.provider_invoked_at is not None

    from sensemaking_skills.campaign_accounting.ledger import CampaignLedger
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    events = ledger.read_events()
    states = [e.event_type for e in events if e.attempt_id == attempt_id]
    assert AttemptState.PROVIDER_FAILED.value in states


def test_full_happy_path_ledger_chain(tmp_path: Path) -> None:
    """End-to-end: RESERVED → INVOKED → OUTPUT_CAPTURED → VALIDATION_PASSED."""
    bundle, attempt_id = _make_reservation(tmp_path)
    campaign_id = bundle.policy.campaign_id

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"hello", now=_ANCHOR_NOW)
    recorder.record_validation_outcome(passed=True, details={"ok": True}, now=_ANCHOR_NOW)

    from sensemaking_skills.campaign_accounting.ledger import CampaignLedger
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    events = ledger.read_events()
    states = [e.event_type for e in events if e.attempt_id == attempt_id]
    assert states == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
        AttemptState.OUTPUT_CAPTURED.value,
        AttemptState.VALIDATION_PASSED.value,
    ]
