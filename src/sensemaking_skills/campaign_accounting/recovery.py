"""Crash recovery utilities for Phase 4 (#120).

Inspects incomplete attempt reservations or interrupted invocations post-crash,
ensuring every attempt is accounted for without silently disappearing or allowing
unauthorized retries.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .ledger import CampaignLedger, campaign_lock
from .models import AttemptState, TERMINAL_STATES
from .recorder import AttemptOutcomeRecorder


class AttemptRecovery:
    """Inspects and reconciles incomplete attempts following a process crash."""

    def __init__(self, campaign_root: Path) -> None:
        self.campaign_root = Path(campaign_root)

    def recover_uninvoked_reservations(
        self,
        campaign_id: str,
        now: Optional[datetime] = None,
    ) -> List[str]:
        """Classify any attempts lingering in RESERVED as ABORTED_BEFORE_INVOCATION.

        If a process crashed after creating a reservation but before entering the
        provider (or before logging INVOKED), the reservation remains spent and is
        terminally closed as ABORTED_BEFORE_INVOCATION.
        """
        if now is None:
            now = datetime.now(timezone.utc)

        campaign_dir = self.campaign_root / campaign_id
        ledger = CampaignLedger(campaign_dir, campaign_id)

        recovered_attempts: List[str] = []

        with campaign_lock(campaign_dir):
            events = ledger.read_events()

            # Find latest state of each attempt
            attempt_states = {}
            for e in events:
                if e.event_type in [s.value for s in AttemptState]:
                    attempt_states[e.attempt_id] = e.event_type

        # Collect attempts to recover OUTSIDE the lock; record_pre_invocation_abort
        # acquires its own campaign_lock internally, so we must not hold it here.
        for attempt_id, state in attempt_states.items():
            if state == AttemptState.RESERVED.value:
                recorder = AttemptOutcomeRecorder(self.campaign_root, campaign_id, attempt_id)
                recorder.record_pre_invocation_abort(
                    reason="Process terminated while attempt was RESERVED before provider entry",
                    now=now,
                )
                recovered_attempts.append(attempt_id)

        return recovered_attempts
