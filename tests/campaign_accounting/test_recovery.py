"""Tests for AttemptRecovery (Phase 4, #120)."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import build_valid_bundle, _ANCHOR_NOW

from sensemaking_skills.campaign_accounting import (
    AttemptState,
    AttemptRecovery,
    DurableReservationManager,
    AttemptOutcomeRecorder,
)
from sensemaking_skills.campaign_accounting.ledger import CampaignLedger


def _make_reservation(manager, bundle, attempt_id: str) -> None:
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )


def _get_attempt_state(tmp_path: Path, campaign_id: str, attempt_id: str) -> str:
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    events = ledger.read_events()
    for e in reversed(events):
        if e.attempt_id == attempt_id:
            return e.event_type
    raise ValueError(f"No events found for attempt '{attempt_id}'")


# ---------------------------------------------------------------------------
# No lingering RESERVED attempts — nothing to recover
# ---------------------------------------------------------------------------


def test_recovery_no_reserved_attempts(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 3})
    campaign_id = bundle.policy.campaign_id
    manager = DurableReservationManager(tmp_path)

    # Reserve and immediately abort → no lingering RESERVED
    _make_reservation(manager, bundle, "00000000-0000-4000-8000-000000000001")
    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000001")
    recorder.record_pre_invocation_abort("test abort", now=_ANCHOR_NOW)

    recovery = AttemptRecovery(tmp_path)
    recovered = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)

    assert recovered == []


# ---------------------------------------------------------------------------
# Single lingering RESERVED attempt — crash-recovery scenario
# ---------------------------------------------------------------------------


def test_recovery_classifies_reserved_as_aborted(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 3})
    campaign_id = bundle.policy.campaign_id
    manager = DurableReservationManager(tmp_path)

    # Simulate crash: reserve, then do NOT transition
    _make_reservation(manager, bundle, "00000000-0000-4000-8000-000000000001")

    recovery = AttemptRecovery(tmp_path)
    recovered = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)

    assert recovered == ["00000000-0000-4000-8000-000000000001"]
    # Ledger must show ABORTED_BEFORE_INVOCATION as the terminal state
    final_state = _get_attempt_state(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000001")
    assert final_state == AttemptState.ABORTED_BEFORE_INVOCATION.value


# ---------------------------------------------------------------------------
# Multiple lingering RESERVED attempts
# ---------------------------------------------------------------------------


def test_recovery_classifies_multiple_reserved(tmp_path: Path) -> None:
    """Two sequential crash-recovery cycles both close their RESERVED attempt."""
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 5, "max_attempts_per_configuration": 5})
    campaign_id = bundle.policy.campaign_id
    manager = DurableReservationManager(tmp_path)

    # Crash 1: aaa-001 is reserved but process dies before entering provider
    _make_reservation(manager, bundle, "00000000-0000-4000-8000-000000000001")
    recovery = AttemptRecovery(tmp_path)
    recovered_1 = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)
    assert "00000000-0000-4000-8000-000000000001" in recovered_1
    assert _get_attempt_state(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000001") == AttemptState.ABORTED_BEFORE_INVOCATION.value

    # Crash 2: aaa-002 is reserved, process dies before provider
    _make_reservation(manager, bundle, "00000000-0000-4000-8000-000000000002")
    recovered_2 = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)
    assert "00000000-0000-4000-8000-000000000002" in recovered_2
    assert _get_attempt_state(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000002") == AttemptState.ABORTED_BEFORE_INVOCATION.value

    # Attempt 1's state was not disturbed by the second recovery
    assert _get_attempt_state(tmp_path, campaign_id, "00000000-0000-4000-8000-000000000001") == AttemptState.ABORTED_BEFORE_INVOCATION.value


# ---------------------------------------------------------------------------
# Recovery is idempotent: calling again on already-recovered attempts
# ---------------------------------------------------------------------------


def test_recovery_idempotent(tmp_path: Path) -> None:
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 3})
    campaign_id = bundle.policy.campaign_id
    manager = DurableReservationManager(tmp_path)

    _make_reservation(manager, bundle, "00000000-0000-4000-8000-000000000001")

    recovery = AttemptRecovery(tmp_path)
    recovered_first = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)
    assert "00000000-0000-4000-8000-000000000001" in recovered_first

    # Second call: aaa-001 is now terminal — must not be double-recovered
    recovered_second = recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW)
    assert recovered_second == []


# ---------------------------------------------------------------------------
# Empty campaign (no ledger yet)
# ---------------------------------------------------------------------------


def test_recovery_empty_campaign(tmp_path: Path) -> None:
    """Recovering against a campaign that has no ledger yet must be a no-op."""
    recovery = AttemptRecovery(tmp_path)
    # No campaign dir, no ledger.jsonl yet
    recovered = recovery.recover_uninvoked_reservations("EXP-9001-alpha", now=_ANCHOR_NOW)
    assert recovered == []


def test_crash_after_output_captured_resumes_validation(tmp_path: Path) -> None:
    """Crash after OUTPUT_CAPTURED: resume validation, never repeat the call.

    The raw output is preserved; recovery leaves the attempt as-is; the
    validation stage can be resumed from the preserved raw output without
    any provider call.
    """
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 3})
    campaign_id = bundle.policy.campaign_id
    attempt_id = "00000000-0000-4000-8000-000000000010"
    manager = DurableReservationManager(tmp_path)
    _make_reservation(manager, bundle, attempt_id)

    recorder = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"preserved raw bytes", now=_ANCHOR_NOW)
    # Crash: process dies before validation.

    # Recovery must not touch OUTPUT_CAPTURED attempts.
    recovery = AttemptRecovery(tmp_path)
    assert recovery.recover_uninvoked_reservations(campaign_id, now=_ANCHOR_NOW) == []
    assert _get_attempt_state(tmp_path, campaign_id, attempt_id) == (
        AttemptState.OUTPUT_CAPTURED.value
    )

    # The raw output survived and validation can resume from it.
    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "raw-output.bin").read_bytes() == b"preserved raw bytes"

    resumed = AttemptOutcomeRecorder(tmp_path, campaign_id, attempt_id)
    result = resumed.record_validation_outcome(
        passed=True, details={"resumed": True}, now=_ANCHOR_NOW
    )
    assert result.state == AttemptState.VALIDATION_PASSED.value
    assert _get_attempt_state(tmp_path, campaign_id, attempt_id) == (
        AttemptState.VALIDATION_PASSED.value
    )
