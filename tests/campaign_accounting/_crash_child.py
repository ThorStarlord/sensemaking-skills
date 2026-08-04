"""Crash-test child process (Phase 4, #120).

Performs durable campaign writes and then HARD-EXITS with ``os._exit(0)``,
bypassing all Python cleanup, atexit handlers, and buffered-stream flushes.
Only bytes already flushed and fsynced by the campaign accounting runtime
may survive. The parent test then inspects the ledger to prove a process
crash cannot erase an attempt.

Never reaches a provider: this child only reserves (or reserves + records
INVOKED), which is the boundary Phase 4 must make crash-visible.

Usage: python _crash_child.py <reserve|invoke> <campaign_root> <out_json>
"""

import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from exploratory_fixtures import build_valid_bundle, new_attempt_id  # noqa: E402

from sensemaking_skills.campaign_accounting import (  # noqa: E402
    AttemptOutcomeRecorder,
    DurableReservationManager,
)


def main() -> int:
    mode = sys.argv[1]
    campaign_root = Path(sys.argv[2])
    out_json = Path(sys.argv[3])

    bundle = build_valid_bundle()
    campaign_id = bundle.policy.campaign_id
    attempt_id = new_attempt_id()

    manager = DurableReservationManager(campaign_root)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": campaign_id},
    )

    if mode == "invoke":
        recorder = AttemptOutcomeRecorder(campaign_root, campaign_id, attempt_id)
        recorder.record_invoked(bundle)

    # Tell the parent what identity to inspect, then die WITHOUT any
    # Python-level cleanup. Nothing beyond the fsynced writes may survive.
    out_json.write_text(
        json.dumps({"campaign_id": campaign_id, "attempt_id": attempt_id}),
        encoding="utf-8",
    )
    os._exit(0)  # noqa: PLR1722 -- deliberate hard crash for the test


if __name__ == "__main__":
    raise SystemExit(main())
