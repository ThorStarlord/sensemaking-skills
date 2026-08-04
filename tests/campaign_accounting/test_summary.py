"""Tests for CampaignSummaryGenerator (Phase 4, #120)."""

import sys
from pathlib import Path
import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import build_valid_bundle, _ANCHOR_NOW

from sensemaking_skills.campaign_accounting import (
    AttemptState,
    DurableReservationManager,
    AttemptOutcomeRecorder,
    CampaignSummaryGenerator,
)
from sensemaking_skills.campaign_accounting.models import TERMINAL_STATES


def _setup_campaign(tmp_path: Path, bundle=None):
    """Return (bundle, manager)."""
    if bundle is None:
        bundle = build_valid_bundle(
            policy_kwargs={"max_attempt_slots": 5, "max_attempts_per_configuration": 5}
        )
    manager = DurableReservationManager(tmp_path)
    return bundle, manager


def _reserve(manager, bundle, attempt_id: str) -> AttemptOutcomeRecorder:
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    return AttemptOutcomeRecorder(
        manager.campaign_root,
        bundle.policy.campaign_id,
        attempt_id,
    )


def aid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _count_by_state(summary, state: str) -> int:
    return sum(1 for a in summary.attempts if a["state"] == state)


# ---------------------------------------------------------------------------
# No-attempt baseline
# ---------------------------------------------------------------------------


def test_summary_no_attempts(tmp_path: Path) -> None:
    bundle, _ = _setup_campaign(tmp_path)

    gen = CampaignSummaryGenerator(tmp_path)
    summary = gen.update_campaign_summary(bundle, now=_ANCHOR_NOW)

    assert summary.campaign_id == bundle.policy.campaign_id
    assert summary.reservations_issued["count"] == 0
    assert summary.attempts == []
    assert summary.provider_invocations_made == 0
    assert summary.campaign_state == "APPROVED_NOT_STARTED"


# ---------------------------------------------------------------------------
# Single passed attempt
# ---------------------------------------------------------------------------


def test_summary_one_passed_attempt(tmp_path: Path) -> None:
    bundle, manager = _setup_campaign(tmp_path)

    r = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000001")
    r.record_invoked(bundle, now=_ANCHOR_NOW)
    r.record_raw_output(b"ok output", now=_ANCHOR_NOW)
    r.record_validation_outcome(passed=True, details={"ok": True}, now=_ANCHOR_NOW)

    gen = CampaignSummaryGenerator(tmp_path)
    summary = gen.update_campaign_summary(bundle, now=_ANCHOR_NOW)

    assert summary.reservations_issued["count"] == 1
    assert _count_by_state(summary, AttemptState.VALIDATION_PASSED.value) == 1
    assert summary.provider_invocations_made == 1


# ---------------------------------------------------------------------------
# Mixed outcomes — all attempts enumerated
# ---------------------------------------------------------------------------


def test_summary_mixed_outcomes(tmp_path: Path) -> None:
    bundle, manager = _setup_campaign(tmp_path)

    # Attempt 1: VALIDATION_PASSED
    r1 = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000001")
    r1.record_invoked(bundle, now=_ANCHOR_NOW)
    r1.record_raw_output(b"ok", now=_ANCHOR_NOW)
    r1.record_validation_outcome(passed=True, details={}, now=_ANCHOR_NOW)

    # Attempt 2: VALIDATION_FAILED
    r2 = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000002")
    r2.record_invoked(bundle, now=_ANCHOR_NOW)
    r2.record_raw_output(b"bad", now=_ANCHOR_NOW)
    r2.record_validation_outcome(passed=False, details={"err": "schema"}, now=_ANCHOR_NOW)

    # Attempt 3: PROVIDER_FAILED
    r3 = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000003")
    r3.record_invoked(bundle, now=_ANCHOR_NOW)
    r3.record_provider_failure("timeout", now=_ANCHOR_NOW)

    # Attempt 4: ABORTED_BEFORE_INVOCATION
    r4 = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000004")
    r4.record_pre_invocation_abort("policy change", now=_ANCHOR_NOW)

    gen = CampaignSummaryGenerator(tmp_path)
    summary = gen.update_campaign_summary(bundle, now=_ANCHOR_NOW)

    assert summary.reservations_issued["count"] == 4
    assert len(summary.attempts) == 4
    assert _count_by_state(summary, AttemptState.VALIDATION_PASSED.value) == 1
    assert _count_by_state(summary, AttemptState.VALIDATION_FAILED.value) == 1
    assert _count_by_state(summary, AttemptState.PROVIDER_FAILED.value) == 1
    assert _count_by_state(summary, AttemptState.ABORTED_BEFORE_INVOCATION.value) == 1
    assert summary.provider_invocations_made == 3


# ---------------------------------------------------------------------------
# Written to disk
# ---------------------------------------------------------------------------


def test_summary_written_to_disk(tmp_path: Path) -> None:
    bundle, manager = _setup_campaign(tmp_path)

    r = _reserve(manager, bundle, "00000000-0000-4000-8000-000000000001")
    r.record_pre_invocation_abort("test abort", now=_ANCHOR_NOW)

    gen = CampaignSummaryGenerator(tmp_path)
    gen.update_campaign_summary(bundle, now=_ANCHOR_NOW)

    campaign_id = bundle.policy.campaign_id
    summary_file = tmp_path / campaign_id / "campaign-summary.yaml"
    assert summary_file.exists()

    raw = yaml.safe_load(summary_file.read_text(encoding="utf-8"))
    assert raw["campaign_id"] == campaign_id
    assert raw["reservations_issued"]["count"] == 1


# ---------------------------------------------------------------------------
# Completeness invariant
# ---------------------------------------------------------------------------


def test_summary_all_attempts_included(tmp_path: Path) -> None:
    """Summary must enumerate every reserved attempt, without selective omission."""
    bundle, manager = _setup_campaign(tmp_path)

    for i in range(1, 5):
        r = _reserve(manager, bundle, f"{aid(i)}")
        r.record_pre_invocation_abort(f"abort {i}", now=_ANCHOR_NOW)

    gen = CampaignSummaryGenerator(tmp_path)
    summary = gen.update_campaign_summary(bundle, now=_ANCHOR_NOW)

    assert summary.reservations_issued["count"] == 4
    assert len(summary.attempts) == 4
    ids = {a["attempt_id"] for a in summary.attempts}
    assert ids == {"00000000-0000-4000-8000-000000000001", "00000000-0000-4000-8000-000000000002", "00000000-0000-4000-8000-000000000003", "00000000-0000-4000-8000-000000000004"}
