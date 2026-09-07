from pathlib import Path

import pytest

from sensemaking_skills.campaign_semantics.io import (
    ContractError,
    canonicalize,
    dump_campaign_state,
    dump_campaign_trace,
    load_campaign_state,
    load_campaign_trace,
    load_campaign_handoff,
    load_transition_record,
)


ROOT = Path(__file__).parents[1]
# Minimal frozen representative M7R campaign corpus, vendored as a test fixture
# (3 states + 3 transitions + 1 trace). These are the real M7R replication
# artifacts the contract's historical-shape compatibility was qualified against;
# they carry no private or machine-specific content.
M7R = Path(__file__).parent / "fixtures" / "campaign-semantics" / "m7r"


def test_real_m7r_states_round_trip_semantically():
    for path in sorted(M7R.glob("*CAMPAIGN-STATE.yaml")):
        model = load_campaign_state(path)
        reloaded = load_campaign_state(dump_campaign_state(model))
        assert canonicalize(model) == canonicalize(reloaded)


def test_real_m7r_trace_round_trips():
    model = load_campaign_trace(M7R / "M7R-E04-CAMPAIGN-TRACE.yaml")
    assert canonicalize(model) == canonicalize(load_campaign_trace(dump_campaign_trace(model)))


def test_real_m7r_transitions_load():
    for path in sorted(M7R.glob("*TRANSITION.yaml")):
        load_transition_record(path)


def test_unknown_authority_is_rejected():
    with pytest.raises(ContractError, match="authority"):
        load_campaign_state({"campaign_id": "c", "mission": "m", "status": "active",
                             "current_state": "s", "authority": "made_up"})


def test_terminal_state_cannot_keep_active_responsibility():
    with pytest.raises(ContractError, match="terminal"):
        load_campaign_state({"campaign_id": "c", "mission": "m", "status": "terminal",
                             "current_state": "done", "terminal_state": "owner_decision_required",
                             "authority": "authorized_autonomously",
                             "active_responsibility": {"id": "r", "statement": "s",
                               "trigger_evidence": [], "decision_blocked": "d", "scope": "x",
                               "authority": "authorized_autonomously", "success_conditions": []}})


def test_template_state_is_loadable():
    model = load_campaign_state(ROOT / "templates" / "campaign-state.yaml")
    assert model.campaign_id == "example-campaign"


@pytest.mark.parametrize("payload", [
    {"campaign_id": "c", "mission": "m", "status": "active", "current_state": "s", "unknown_semantic": 1},
    {"campaign_id": "c", "mission": "m", "status": "active", "current_state": "s", "schema_version": "9"},
])
def test_unknown_or_unsupported_contract_fields_fail(payload):
    with pytest.raises(ContractError):
        load_campaign_state(payload)


def test_empirical_owner_routing_extension_is_preserved():
    model = load_campaign_state({"campaign_id": "c", "mission": "m", "status": "active", "current_state": "s", "owner_routing": {"route_to": "owner"}})
    assert model.extensions["owner_routing"]["route_to"] == "owner"


def test_handoff_reference_is_consumed_against_loaded_state():
    state = load_campaign_state(ROOT / "templates" / "campaign-state.yaml")
    handoff = load_campaign_handoff({
        "campaign_id": state.campaign_id,
        "current_state_reference": state.current_state, "allowed_next_actions": ["review"],
        "stop_conditions": ["owner_decision_required"],
    }, current_state=state)
    assert handoff.current_state.current_state == "qualification"
