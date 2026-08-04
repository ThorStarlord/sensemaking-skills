"""Crash-safety proofs for Phase 4 (#120).

These tests kill a real child process with ``os._exit`` at defined
checkpoints -- after the durable reservation, and after the durable INVOKED
transition -- then inspect the surviving filesystem state from the parent.
They prove the DoD properties:

* A process crash cannot erase an attempt.
* Crash-visible state is either valid or explicitly incomplete -- never
  silently accepted as something it is not.
* Recovery can classify a crash-before-invocation attempt as
  ABORTED_BEFORE_INVOCATION; a crash after INVOKED leaves a spent,
  visible, incomplete attempt that is never retried and never rewritten.
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import _ANCHOR_NOW, build_valid_bundle

from sensemaking_skills.campaign_accounting import (
    AttemptRecovery,
    AttemptState,
    CampaignLedger,
    CampaignSummaryGenerator,
    DurableReservationManager,
)

_CRASH_CHILD = Path(__file__).resolve().parent / "_crash_child.py"


def _run_child(mode: str, tmp_path: Path) -> dict:
    out_json = tmp_path / "child-out.json"
    result = subprocess.run(
        [sys.executable, str(_CRASH_CHILD), mode, str(tmp_path), str(out_json)],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, (
        f"child failed: {result.returncode}\nstdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    assert out_json.exists(), "child died before reporting its identity"
    return json.loads(out_json.read_text(encoding="utf-8"))


def _states(tmp_path: Path, campaign_id: str, attempt_id: str) -> list:
    ledger = CampaignLedger(tmp_path / campaign_id, campaign_id)
    return [
        e.event_type
        for e in ledger.read_events()
        if e.attempt_id == attempt_id
    ]


def test_crash_after_reservation_leaves_visible_state(tmp_path: Path) -> None:
    """Crash right after RESERVED: the attempt survives and is recoverable."""
    info = _run_child("reserve", tmp_path)
    campaign_id, attempt_id = info["campaign_id"], info["attempt_id"]

    # The ledger (fsynced before the crash) still shows the reservation.
    assert _states(tmp_path, campaign_id, attempt_id) == [
        AttemptState.RESERVED.value
    ]

    # The attempt directory and reservation document survived.
    attempt_dir = tmp_path / campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "reservation.yaml").exists()
    assert (attempt_dir / "request-metadata.json").exists()

    # Recovery classifies it ABORTED_BEFORE_INVOCATION -- never deleted,
    # never refunded, never silently retried.
    recovery = AttemptRecovery(tmp_path)
    recovered = recovery.recover_uninvoked_reservations(
        campaign_id, now=_ANCHOR_NOW
    )
    assert attempt_id in recovered
    assert _states(tmp_path, campaign_id, attempt_id)[-1] == (
        AttemptState.ABORTED_BEFORE_INVOCATION.value
    )


def test_crash_after_reservation_blocks_attempt_id_reuse(tmp_path: Path) -> None:
    """After a crash the same attempt ID can never be reserved again."""
    info = _run_child("reserve", tmp_path)
    campaign_id, attempt_id = info["campaign_id"], info["attempt_id"]

    bundle = build_valid_bundle()
    manager = DurableReservationManager(tmp_path)
    from sensemaking_skills.campaign_accounting import (
        RESERVATION_EXISTS_FOR_ATTEMPT,
        CampaignAccountingError,
    )

    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id=attempt_id,
            configuration_id=bundle.configuration.configuration_id,
            request_metadata={"campaign_id": campaign_id},
            now=_ANCHOR_NOW,
        )
    assert exc_info.value.failure_code == RESERVATION_EXISTS_FOR_ATTEMPT


def test_crash_after_invoked_leaves_spent_incomplete_attempt(tmp_path: Path) -> None:
    """Crash after durable INVOKED: spent, visible, never retried, listed."""
    info = _run_child("invoke", tmp_path)
    campaign_id, attempt_id = info["campaign_id"], info["attempt_id"]

    assert _states(tmp_path, campaign_id, attempt_id) == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
    ]

    # Recovery must NOT rewrite INVOKED (the provider boundary may have been
    # entered; the attempt stays exactly as visible as it is).
    recovery = AttemptRecovery(tmp_path)
    assert recovery.recover_uninvoked_reservations(
        campaign_id, now=_ANCHOR_NOW
    ) == []

    # The summary includes the incomplete attempt with no terminal_at.
    bundle = build_valid_bundle()
    summary = CampaignSummaryGenerator(tmp_path).update_campaign_summary(
        bundle, now=_ANCHOR_NOW
    )
    entry = next(a for a in summary.attempts if a["attempt_id"] == attempt_id)
    assert entry["state"] == AttemptState.INVOKED.value
    assert entry["terminal_at"] is None

    # The INVOKED attempt is still active (nonterminal), so the concurrency
    # ceiling (v1: 1) blocks any new reservation: the slot stays consumed.
    from sensemaking_skills.campaign_accounting import CampaignAccountingError

    manager = DurableReservationManager(tmp_path)
    with pytest.raises(CampaignAccountingError) as exc_info:
        manager.reserve_attempt(
            bundle=bundle,
            attempt_id="00000000-0000-4000-8000-000000009999",
            configuration_id=bundle.configuration.configuration_id,
            request_metadata={"campaign_id": campaign_id},
            now=_ANCHOR_NOW,
        )
    assert exc_info.value.failure_code == "CONCURRENCY_CEILING_EXCEEDED"
