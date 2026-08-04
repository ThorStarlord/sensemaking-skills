"""Tests for append-only, tamper-evident CampaignLedger (Phase 4, #120)."""

import json
from pathlib import Path
import pytest

from sensemaking_skills.campaign_accounting import (
    CAMPAIGN_LEDGER_CORRUPT,
    CAMPAIGN_LEDGER_HASH_MISMATCH,
    CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY,
    CAMPAIGN_LEDGER_TRUNCATED,
    AttemptState,
    CampaignAccountingError,
    CampaignLedger,
    GENESIS_HASH,
)


def test_empty_ledger(tmp_path: Path) -> None:
    ledger = CampaignLedger(tmp_path, "EXP-0001")
    events = ledger.read_events()
    assert events == []


def test_append_and_read_events(tmp_path: Path) -> None:
    ledger = CampaignLedger(tmp_path, "EXP-0001")

    e1 = ledger.append_event(
        timestamp="2026-01-01T00:00:00+00:00",
        attempt_id="00000000-0000-0000-0000-000000000001",
        event_type=AttemptState.RESERVED.value,
        payload={"configuration_id": "config1"},
    )
    assert e1.sequence == 1
    assert e1.previous_event_hash == GENESIS_HASH

    e2 = ledger.append_event(
        timestamp="2026-01-01T00:00:05+00:00",
        attempt_id="00000000-0000-0000-0000-000000000001",
        event_type=AttemptState.INVOKED.value,
        payload={"provider_invoked_at": "2026-01-01T00:00:05+00:00"},
    )
    assert e2.sequence == 2
    assert e2.previous_event_hash == e1.event_hash

    events = ledger.read_events()
    assert len(events) == 2
    assert events[0] == e1
    assert events[1] == e2


def test_ledger_tampered_payload_hash_mismatch(tmp_path: Path) -> None:
    ledger = CampaignLedger(tmp_path, "EXP-0001")
    ledger.append_event(
        timestamp="2026-01-01T00:00:00+00:00",
        attempt_id="00000000-0000-0000-0000-000000000001",
        event_type=AttemptState.RESERVED.value,
        payload={"configuration_id": "config1"},
    )

    ledger_file = tmp_path / "ledger.jsonl"
    content = ledger_file.read_text(encoding="utf-8")
    tampered_content = content.replace("config1", "tampered_config")
    ledger_file.write_text(tampered_content, encoding="utf-8")

    with pytest.raises(CampaignAccountingError) as exc_info:
        ledger.read_events()
    assert exc_info.value.failure_code == CAMPAIGN_LEDGER_HASH_MISMATCH


def test_ledger_sequence_discontinuity(tmp_path: Path) -> None:
    ledger_file = tmp_path / "ledger.jsonl"
    event1 = {
        "sequence": 1,
        "timestamp": "2026-01-01T00:00:00+00:00",
        "campaign_id": "EXP-0001",
        "attempt_id": "00000000-0000-0000-0000-000000000001",
        "event_type": AttemptState.RESERVED.value,
        "payload": {},
        "previous_event_hash": GENESIS_HASH,
        "event_hash": "dummy",
    }
    # Compute real hash
    from sensemaking_skills.campaign_accounting import compute_event_hash
    event1["event_hash"] = compute_event_hash(event1)

    event3 = {
        "sequence": 3,  # Skipping 2!
        "timestamp": "2026-01-01T00:00:05+00:00",
        "campaign_id": "EXP-0001",
        "attempt_id": "00000000-0000-0000-0000-000000000001",
        "event_type": AttemptState.INVOKED.value,
        "payload": {},
        "previous_event_hash": event1["event_hash"],
        "event_hash": "dummy",
    }
    event3["event_hash"] = compute_event_hash(event3)

    ledger_file.write_text(
        json.dumps(event1) + "\n" + json.dumps(event3) + "\n",
        encoding="utf-8",
    )

    ledger = CampaignLedger(tmp_path, "EXP-0001")
    with pytest.raises(CampaignAccountingError) as exc_info:
        ledger.read_events()
    assert exc_info.value.failure_code == CAMPAIGN_LEDGER_SEQUENCE_DISCONTINUITY


def test_ledger_truncated_line(tmp_path: Path) -> None:
    ledger_file = tmp_path / "ledger.jsonl"
    ledger_file.write_text('{"sequence": 1, "timestamp": "2026-01-01T00:00', encoding="utf-8")

    ledger = CampaignLedger(tmp_path, "EXP-0001")
    with pytest.raises(CampaignAccountingError) as exc_info:
        ledger.read_events()
    assert exc_info.value.failure_code == CAMPAIGN_LEDGER_TRUNCATED


def test_ledger_illegal_state_transition(tmp_path: Path) -> None:
    ledger = CampaignLedger(tmp_path, "EXP-0001")

    ledger.append_event(
        timestamp="2026-01-01T00:00:00+00:00",
        attempt_id="00000000-0000-0000-0000-000000000001",
        event_type=AttemptState.RESERVED.value,
        payload={"configuration_id": "config1"},
    )

    # Trying to jump directly from RESERVED to VALIDATION_PASSED (illegal transition)
    with pytest.raises(CampaignAccountingError) as exc_info:
        ledger.append_event(
            timestamp="2026-01-01T00:00:05+00:00",
            attempt_id="00000000-0000-0000-0000-000000000001",
            event_type=AttemptState.VALIDATION_PASSED.value,
            payload={},
        )
    assert exc_info.value.failure_code == "ATTEMPT_STATE_INVALID_TRANSITION"
