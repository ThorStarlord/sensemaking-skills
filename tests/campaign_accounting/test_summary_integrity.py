"""Summary projection integrity tests (Phase 4, #120).

The campaign summary is a DERIVED projection of the ledger -- never a
separate source of truth. These tests pin the fail-closed behaviors: orphan
results are rejected, missing attempt directories are rejected, malformed
ledgers fail closed, expired/exhausted campaigns are labeled, and
incomplete (crash-visible) attempts are included rather than hidden.
"""

from datetime import timedelta
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import _ANCHOR_NOW, build_valid_bundle, new_attempt_id

from sensemaking_skills.campaign_accounting import (
    CAMPAIGN_LEDGER_CORRUPT,
    CAMPAIGN_LEDGER_TRUNCATED,
    CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR,
    CAMPAIGN_SUMMARY_ORPHAN_RESULT,
    AttemptState,
    CampaignAccountingError,
    DurableReservationManager,
    AttemptOutcomeRecorder,
    CampaignSummaryGenerator,
)


def aid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _reserve(tmp_path: Path, bundle, attempt_id=None):
    attempt_id = attempt_id or new_attempt_id()
    manager = DurableReservationManager(tmp_path)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    return AttemptOutcomeRecorder(
        tmp_path, bundle.policy.campaign_id, attempt_id
    )


def _generate(tmp_path: Path, bundle):
    return CampaignSummaryGenerator(tmp_path).update_campaign_summary(
        bundle, now=_ANCHOR_NOW
    )


# ---------------------------------------------------------------------------
# Fail-closed reconciliation
# ---------------------------------------------------------------------------


def test_summary_rejects_orphan_result(tmp_path: Path) -> None:
    """An attempt-result.yaml with no RESERVED ledger event is rejected."""
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    # Fabricate an orphan: a result file whose attempt never reserved.
    orphan_id = aid(777)
    orphan_dir = Path(tmp_path) / bundle.policy.campaign_id / "attempts" / orphan_id
    orphan_dir.mkdir(parents=True)
    (orphan_dir / "attempt-result.yaml").write_text(
        "state: 'VALIDATION_PASSED'\n", encoding="utf-8"
    )

    with pytest.raises(CampaignAccountingError) as exc_info:
        _generate(tmp_path, bundle)
    assert exc_info.value.failure_code == CAMPAIGN_SUMMARY_ORPHAN_RESULT


def test_summary_rejects_missing_attempt_dir(tmp_path: Path) -> None:
    """A RESERVED event whose attempt directory vanished is rejected."""
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    attempt_id = recorder.attempt_id
    attempt_dir = (
        Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
    )
    # Tampering: delete the whole attempt directory after a terminal result.
    import shutil
    shutil.rmtree(attempt_dir)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _generate(tmp_path, bundle)
    assert exc_info.value.failure_code == CAMPAIGN_SUMMARY_MISSING_ATTEMPT_DIR


def test_summary_malformed_ledger_fails_closed(tmp_path: Path) -> None:
    """A truncated ledger must fail closed, never produce a partial summary."""
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    ledger_file = (
        Path(tmp_path) / bundle.policy.campaign_id / "ledger.jsonl"
    )
    content = ledger_file.read_text(encoding="utf-8")
    # Truncate the final event mid-line (drop the trailing newline plus a
    # few characters of the last event).
    ledger_file.write_text(content[:-3], encoding="utf-8")

    with pytest.raises(CampaignAccountingError) as exc_info:
        _generate(tmp_path, bundle)
    # Any corrupt-family code is fail-closed: the summary is never produced
    # from a truncated ledger.
    assert exc_info.value.failure_code in (
        CAMPAIGN_LEDGER_CORRUPT,
        CAMPAIGN_LEDGER_TRUNCATED,
    )


# ---------------------------------------------------------------------------
# Campaign states
# ---------------------------------------------------------------------------


def test_summary_expired_campaign(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    # Generate a summary at a time after the validity window.
    summary = CampaignSummaryGenerator(tmp_path).update_campaign_summary(
        bundle, now=_ANCHOR_NOW + timedelta(days=400)
    )
    assert summary.campaign_state == "EXPIRED"
    assert summary.terminal_reason is not None
    assert len(summary.attempts) == 1  # the attempt is still listed


def test_summary_exhausted_by_cost_ceiling(tmp_path: Path) -> None:
    """Observed cost crossing the (soft) ceiling makes the campaign EXHAUSTED."""
    bundle = build_valid_bundle(
        policy_kwargs={"max_attempt_slots": 5, "max_attempts_per_configuration": 5,
                       "cost_ceiling": {"amount": 4.0, "currency": "USD"}}
    )
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"raw", now=_ANCHOR_NOW)
    recorder.record_validation_outcome(
        passed=True,
        details={},
        cost_observed={"amount": 5.0, "currency": "USD"},
        now=_ANCHOR_NOW,
    )

    summary = _generate(tmp_path, bundle)
    assert summary.campaign_state == "EXHAUSTED"
    assert summary.terminal_reason is not None
    assert summary.remaining_budget["cost_observed"] == 5.0
    assert summary.remaining_budget["cost"] == 0.0
    # The exhausting attempt itself is still enumerated.
    assert len(summary.attempts) == 1


def test_summary_exhausted_by_token_ceiling_blocks_reservation(tmp_path: Path) -> None:
    """Once tokens cross the ceiling, no further attempt may be reserved."""
    bundle = build_valid_bundle(
        policy_kwargs={"max_attempt_slots": 5, "max_attempts_per_configuration": 5,
                       "token_ceiling": 100}
    )
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"raw", now=_ANCHOR_NOW)
    recorder.record_validation_outcome(
        passed=True, details={}, tokens_observed=150, now=_ANCHOR_NOW
    )

    summary = _generate(tmp_path, bundle)
    assert summary.campaign_state == "EXHAUSTED"
    assert summary.remaining_budget["tokens_observed"] == 150.0

    # A second reservation is refused: campaign is not active.
    from sensemaking_skills.campaign_accounting import CAMPAIGN_NOT_ACTIVE
    manager = DurableReservationManager(tmp_path)
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id=new_attempt_id(),
            configuration_id=bundle.configuration.configuration_id,
            request_metadata={"campaign_id": bundle.policy.campaign_id},
            now=_ANCHOR_NOW,
        )
    assert exc_info.value.failure_code == CAMPAIGN_NOT_ACTIVE


def test_summary_exhausted_when_attempt_slots_consumed(tmp_path: Path) -> None:
    """All attempt slots consumed => EXHAUSTED even with a crash-visible attempt."""
    bundle = build_valid_bundle(policy_kwargs={"max_attempt_slots": 1})
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    # Crash here: the attempt is left INVOKED-incomplete (no terminal event).

    summary = _generate(tmp_path, bundle)
    assert summary.campaign_state == "EXHAUSTED"
    # The incomplete attempt is included, not omitted.
    assert len(summary.attempts) == 1
    assert summary.attempts[0]["state"] == AttemptState.INVOKED.value
    assert summary.attempts[0]["terminal_at"] is None


def test_summary_no_cost_ceiling_reports_observed_only(tmp_path: Path) -> None:
    """Without declared ceilings, remaining budget reports observed totals only."""
    bundle = build_valid_bundle()  # token_ceiling=None, cost_ceiling=None
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    summary = _generate(tmp_path, bundle)
    assert "tokens" not in summary.remaining_budget
    assert "cost" not in summary.remaining_budget
    assert summary.remaining_budget["tokens_observed"] == 0.0
    assert summary.remaining_budget["cost_observed"] == 0.0
    assert summary.campaign_state == "ACTIVE"


def test_summary_written_atomically_no_temp_left(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_pre_invocation_abort("abort", now=_ANCHOR_NOW)

    _generate(tmp_path, bundle)
    campaign_dir = Path(tmp_path) / bundle.policy.campaign_id
    assert (campaign_dir / "campaign-summary.yaml").exists()
    assert not list(campaign_dir.glob(".tmp-campaign-summary.yaml"))
