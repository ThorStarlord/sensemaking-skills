"""Mechanical campaign-contract consumption and round-trip gate."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sensemaking_skills.campaign_semantics.io import (  # noqa: E402
    canonicalize, dump_campaign_state, dump_campaign_trace,
    load_campaign_state, load_campaign_trace, load_transition_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m7r-root", type=Path, required=True)
    args = parser.parse_args()
    states = sorted(args.m7r_root.glob("*CAMPAIGN-STATE.yaml"))
    transitions = sorted(args.m7r_root.glob("*TRANSITION.yaml"))
    trace_path = args.m7r_root / "M7R-E04-CAMPAIGN-TRACE.yaml"
    if not states or not transitions or not trace_path.exists():
        raise SystemExit("M7R fixture set is incomplete")
    for path in states:
        model = load_campaign_state(path)
        assert canonicalize(model) == canonicalize(load_campaign_state(dump_campaign_state(model)))
    for path in transitions:
        load_transition_record(path)
    trace = load_campaign_trace(trace_path)
    assert canonicalize(trace) == canonicalize(load_campaign_trace(dump_campaign_trace(trace)))
    template = load_campaign_state(ROOT / "templates" / "campaign-state.yaml")
    assert template.campaign_id == "example-campaign"
    print(f"CAMPAIGN_CONTRACT_ROUNDTRIP: PASS states={len(states)} transitions={len(transitions)} trace=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
