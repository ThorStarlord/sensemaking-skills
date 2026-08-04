"""Append-only, tamper-evident Campaign Ledger for Phase 4 (#120).

Maintains `ledger.jsonl` under cross-process locking (`ledger.lock`) in the
campaign directory (`experiments/campaigns/<campaign_id>/`). Every event
contains a sequence number, timestamp, campaign_id, attempt_id, event_type,
payload, previous_event_hash, and event_hash computed via JCS SHA-256.

The ledger is authoritative. A malformed, reordered, modified, or truncated
ledger fails closed with `CAMPAIGN_LEDGER_CORRUPT` (or specific sub-codes).
"""

from contextlib import contextmanager
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .digests import GENESIS_HASH, compute_event_hash
from .failure_codes import (
    CAMPAIGN_LEDGER_CORRUPT,
    CAMPAIGN_LEDGER_HASH_MISMATCH,
    CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY,
    CAMPAIGN_LEDGER_TRUNCATED,
    CampaignAccountingError,
)
from .models import (
    AttemptState,
    LedgerEvent,
    validate_state_transition,
)


@contextmanager
def campaign_lock(campaign_dir: Path) -> Iterator[None]:
    """Cross-process lock for campaign operations."""
    campaign_dir.mkdir(parents=True, exist_ok=True)
    lock_file = campaign_dir / "ledger.lock"
    # Simple cross-platform file locking
    lock_fd = None
    try:
        lock_fd = open(lock_file, "a+b")
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(lock_fd.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
        yield
    finally:
        if lock_fd:
            try:
                if os.name == "nt":
                    import msvcrt
                    lock_fd.seek(0)
                    msvcrt.locking(lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except Exception:
                pass
            try:
                lock_fd.close()
            except Exception:
                pass


class CampaignLedger:
    """Manages the append-only, tamper-evident event ledger for a single campaign."""

    def __init__(self, campaign_dir: Path, campaign_id: str) -> None:
        self.campaign_dir = Path(campaign_dir)
        self.campaign_id = campaign_id
        self.ledger_file = self.campaign_dir / "ledger.jsonl"

    def read_events(self) -> List[LedgerEvent]:
        """Read and validate the full event history. Fail-closed on any corruption."""
        if not self.ledger_file.exists():
            return []

        events: List[LedgerEvent] = []
        expected_seq = 1
        expected_prev_hash = GENESIS_HASH
        attempt_states: Dict[str, str] = {}

        with open(self.ledger_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            line_str = line.strip()
            if not line_str:
                # Truncated or trailing empty line
                if idx == len(lines) - 1:
                    continue  # trailing whitespace line
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_TRUNCATED,
                    f"Empty line encountered in ledger at line {idx + 1}",
                )

            try:
                data = json.loads(line_str)
            except json.JSONDecodeError as exc:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_TRUNCATED,
                    f"Malformed JSON in ledger at line {idx + 1}: {exc}",
                ) from exc

            # Verify required fields
            req_fields = [
                "sequence",
                "timestamp",
                "campaign_id",
                "attempt_id",
                "event_type",
                "payload",
                "previous_event_hash",
                "event_hash",
            ]
            for rf in req_fields:
                if rf not in data:
                    raise CampaignAccountingError(
                        CAMPAIGN_LEDGER_CORRUPT,
                        f"Missing field '{rf}' in ledger event at sequence {data.get('sequence')}",
                    )

            seq = data["sequence"]
            if seq != expected_seq:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY,
                    f"Ledger sequence discontinuity: expected {expected_seq}, got {seq}",
                )

            if data["campaign_id"] != self.campaign_id:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_CORRUPT,
                    f"Campaign ID mismatch in ledger: expected '{self.campaign_id}', got '{data['campaign_id']}'",
                )

            if data["previous_event_hash"] != expected_prev_hash:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_HASH_MISMATCH,
                    f"Previous event hash mismatch at sequence {seq}: expected {expected_prev_hash}, got {data['previous_event_hash']}",
                )

            # Recompute event hash
            actual_hash = compute_event_hash(data)
            if actual_hash != data["event_hash"]:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_HASH_MISMATCH,
                    f"Event hash mismatch at sequence {seq}: recorded {data['event_hash']}, computed {actual_hash}",
                )

            # Check attempt state transitions if event represents a state
            event_type = data["event_type"]
            attempt_id = data["attempt_id"]
            if event_type in [s.value for s in AttemptState]:
                curr_state = attempt_states.get(attempt_id)
                if curr_state is not None:
                    validate_state_transition(curr_state, event_type)
                elif event_type != AttemptState.RESERVED.value:
                    raise CampaignAccountingError(
                        CAMPAIGN_LEDGER_CORRUPT,
                        f"Attempt '{attempt_id}' started with state '{event_type}' instead of RESERVED",
                    )
                attempt_states[attempt_id] = event_type

            event = LedgerEvent(
                sequence=data["sequence"],
                timestamp=data["timestamp"],
                campaign_id=data["campaign_id"],
                attempt_id=data["attempt_id"],
                event_type=data["event_type"],
                payload=data["payload"],
                previous_event_hash=data["previous_event_hash"],
                event_hash=data["event_hash"],
            )
            events.append(event)
            expected_seq += 1
            expected_prev_hash = event.event_hash

        return events

    def _append_event_unlocked(
        self,
        events: List[LedgerEvent],
        timestamp: str,
        attempt_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> LedgerEvent:
        """Append a new event WITHOUT acquiring the campaign lock.

        Must only be called from within a ``campaign_lock`` context that the
        caller already holds. ``events`` must be the current ledger contents
        (already read under the same lock).
        """
        seq = len(events) + 1
        prev_hash = events[-1].event_hash if events else GENESIS_HASH

        # Check attempt state transition if applicable
        if event_type in [s.value for s in AttemptState]:
            attempt_events = [e for e in events if e.attempt_id == attempt_id]
            if attempt_events:
                last_attempt_event = [
                    e for e in attempt_events
                    if e.event_type in [s.value for s in AttemptState]
                ][-1]
                validate_state_transition(last_attempt_event.event_type, event_type)
            elif event_type != AttemptState.RESERVED.value:
                raise CampaignAccountingError(
                    CAMPAIGN_LEDGER_CORRUPT,
                    f"First event for attempt '{attempt_id}' must be RESERVED, got '{event_type}'",
                )

        event_dict_no_hash = {
            "sequence": seq,
            "timestamp": timestamp,
            "campaign_id": self.campaign_id,
            "attempt_id": attempt_id,
            "event_type": event_type,
            "payload": payload,
            "previous_event_hash": prev_hash,
        }
        event_hash = compute_event_hash(event_dict_no_hash)

        event = LedgerEvent(
            sequence=seq,
            timestamp=timestamp,
            campaign_id=self.campaign_id,
            attempt_id=attempt_id,
            event_type=event_type,
            payload=payload,
            previous_event_hash=prev_hash,
            event_hash=event_hash,
        )

        # Append to file with flush and fsync
        self.campaign_dir.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")
            f.flush()
            os.fsync(f.fileno())

        return event

    def append_event(
        self,
        timestamp: str,
        attempt_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> LedgerEvent:
        """Atomically append a new event under lock."""
        with campaign_lock(self.campaign_dir):
            events = self.read_events()
            return self._append_event_unlocked(
                events, timestamp, attempt_id, event_type, payload
            )
