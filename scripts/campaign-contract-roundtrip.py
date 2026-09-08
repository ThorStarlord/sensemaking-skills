"""Mechanical campaign-contract consumption and round-trip gate.

Loads the historical campaign fixture corpus and every shipped template through
its production loader, and asserts semantic round-trip equality
(``canonicalize(model) == canonicalize(load(dump(model)))``) for each.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sensemaking_skills.campaign_semantics.io import (  # noqa: E402
    canonicalize,
    dump_campaign_handoff, dump_campaign_policy, dump_campaign_state,
    dump_campaign_trace, dump_transition_record,
    load_campaign_handoff, load_campaign_policy, load_campaign_state,
    load_campaign_trace, load_transition_record,
)

TEMPLATES = ROOT / "templates"


def _roundtrip(load, dump, source) -> None:
    model = load(source)
    assert canonicalize(model) == canonicalize(load(dump(model))), f"round-trip mismatch: {source}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m7r-root", type=Path, required=True)
    args = parser.parse_args()
    states = sorted(args.m7r_root.glob("*CAMPAIGN-STATE.yaml"))
    transitions = sorted(args.m7r_root.glob("*TRANSITION.yaml"))
    trace_path = args.m7r_root / "M7R-E04-CAMPAIGN-TRACE.yaml"
    if not states or not transitions or not trace_path.exists():
        raise SystemExit("historical campaign fixture set is incomplete")

    for path in states:
        _roundtrip(load_campaign_state, dump_campaign_state, path)
    for path in transitions:
        _roundtrip(load_transition_record, dump_transition_record, path)
    _roundtrip(load_campaign_trace, dump_campaign_trace, trace_path)

    templates = {
        "campaign-state.yaml": (load_campaign_state, dump_campaign_state),
        "transition-record.yaml": (load_transition_record, dump_transition_record),
        "campaign-policy.yaml": (load_campaign_policy, dump_campaign_policy),
        "campaign-handoff.yaml": (load_campaign_handoff, dump_campaign_handoff),
    }
    for name, (load, dump) in templates.items():
        _roundtrip(load, dump, TEMPLATES / name)
    assert load_campaign_state(TEMPLATES / "campaign-state.yaml").campaign_id == "example-campaign"

    print(
        f"CAMPAIGN_CONTRACT_ROUNDTRIP: PASS states={len(states)} "
        f"transitions={len(transitions)} trace=1 templates={len(templates)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
