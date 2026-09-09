from pathlib import Path

import pytest

from sensemaking_skills.campaign_semantics.io import (
    ContractError,
    canonicalize,
    dump_campaign_handoff,
    dump_campaign_policy,
    dump_campaign_state,
    dump_campaign_trace,
    dump_transition_record,
    load_campaign_handoff,
    load_campaign_policy,
    load_campaign_state,
    load_campaign_trace,
    load_responsibility,
    load_transition_record,
)
from sensemaking_skills.campaign_semantics.models import (
    Authority,
    CampaignState,
    Dependency,
    DependencyType,
    DeferredResponsibility,
    Responsibility,
    validate_reconstruction,
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


# --- uniform strictness across every public loader and nested record ---------

TEMPLATES = ROOT / "templates"


def test_every_shipped_template_loads_through_its_production_loader():
    load_campaign_state(TEMPLATES / "campaign-state.yaml")
    load_transition_record(TEMPLATES / "transition-record.yaml")
    load_campaign_policy(TEMPLATES / "campaign-policy.yaml")
    load_campaign_handoff(TEMPLATES / "campaign-handoff.yaml")


def test_every_shipped_template_round_trips_semantically():
    pairs = [
        (TEMPLATES / "campaign-state.yaml", load_campaign_state, dump_campaign_state),
        (TEMPLATES / "transition-record.yaml", load_transition_record, dump_transition_record),
        (TEMPLATES / "campaign-policy.yaml", load_campaign_policy, dump_campaign_policy),
        (TEMPLATES / "campaign-handoff.yaml", load_campaign_handoff, dump_campaign_handoff),
    ]
    for path, load, dump in pairs:
        model = load(path)
        assert canonicalize(model) == canonicalize(load(dump(model))), path.name


def test_nested_responsibility_snapshot_rejects_unknown_fields():
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_state({
            "campaign_id": "c", "mission": "m", "status": "active", "current_state": "s",
            "authority": "authorized_autonomously",
            "active_responsibility": {
                "id": "r", "statement": "s", "scope": "x",
                "authority": "authorized_autonomously", "surprise": True,
            },
        })


def test_standalone_responsibility_loader_rejects_unknown_fields():
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_responsibility({
            "id": "r", "statement": "s", "scope": "x", "authority": "authorized_autonomously",
            "decision_blocked": "d", "success_conditions": [], "bogus": 1,
        })


def test_deferred_and_boundary_records_reject_unknown_fields():
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_state({
            "campaign_id": "c", "mission": "m", "status": "active", "current_state": "s",
            "deferred_responsibilities": [{"responsibility_id": "R", "reason": "later", "huh": 1}],
        })
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_state({
            "campaign_id": "c", "mission": "m", "status": "active", "current_state": "s",
            "external_boundaries": [{
                "id": "b", "capability": "x", "owner": "o", "repository_owned": False,
                "accessible": False, "implication": "i", "extra": 1,
            }],
        })


@pytest.mark.parametrize("bad", [
    {"id": "t", "from_state": "a", "to_state": "b", "evidence": [], "decision": "d", "mystery": 1},
])
def test_transition_record_rejects_unknown_fields(bad):
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_transition_record(bad)


def test_transition_record_accepts_current_schema_version():
    model = load_transition_record({"id": "t", "from_state": "a", "to_state": "b",
                                    "evidence": [], "decision": "d", "schema_version": "2"})
    assert model.schema_version == "2"


def test_campaign_policy_is_strict_and_raises_contracterror_not_keyerror():
    with pytest.raises(ContractError, match="missing required fields"):
        load_campaign_policy({"campaign_id": "c"})  # no mission -> ContractError, not KeyError
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_policy({"campaign_id": "c", "mission": "m", "surprise": 1})
    with pytest.raises(ContractError, match="schema_version"):
        load_campaign_policy({"campaign_id": "c", "mission": "m", "schema_version": "x"})


def test_campaign_trace_is_strict_about_unknown_fields_and_schema_version():
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_trace({"campaign_id": "c", "events": [], "weird": 1})
    with pytest.raises(ContractError, match="schema_version"):
        load_campaign_trace({"campaign_id": "c", "events": [], "schema_version": "7"})


def test_campaign_handoff_is_strict_and_enforces_campaign_id_consistency():
    state = load_campaign_state(TEMPLATES / "campaign-state.yaml")
    with pytest.raises(ContractError, match="unknown decision-relevant field"):
        load_campaign_handoff({"campaign_id": state.campaign_id, "stop_conditions": [],
                               "allowed_next_actions": [], "nope": 1}, current_state=state)
    with pytest.raises(ContractError, match="schema_version"):
        load_campaign_handoff({"campaign_id": state.campaign_id, "stop_conditions": [],
                               "allowed_next_actions": [], "schema_version": "3"}, current_state=state)
    with pytest.raises(ContractError, match="campaign_id"):
        load_campaign_handoff({"campaign_id": "a-different-campaign", "stop_conditions": [],
                               "allowed_next_actions": []}, current_state=state)


def test_handoff_template_campaign_id_matches_its_embedded_state():
    handoff = load_campaign_handoff(TEMPLATES / "campaign-handoff.yaml")
    assert handoff.campaign_id == handoff.current_state.campaign_id


def test_task_dependency_on_deferred_responsibility_is_valid_but_missing_is_flagged():
    def _resp(requires):
        return Responsibility(
            id="R-active", statement="s", trigger_evidence=(), decision_blocked="d",
            scope="x", authority=Authority.AUTHORIZED_AUTONOMOUSLY, success_conditions=(),
            dependencies=(Dependency(DependencyType.TASK, requires),),
        )

    ok = CampaignState(
        campaign_id="c", mission="m", status="active", current_state="s",
        active_responsibility=_resp("R-deferred"), authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        deferred_responsibilities=(DeferredResponsibility("R-deferred", "later", ()),),
    )
    result = validate_reconstruction(ok, (), existing_evidence=set())
    assert result.valid, [d.code for d in result.diagnostics]

    missing = CampaignState(
        campaign_id="c", mission="m", status="active", current_state="s",
        active_responsibility=_resp("R-nonexistent"), authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    )
    codes = {d.code for d in validate_reconstruction(missing, (), set()).diagnostics}
    assert "MISSING_TASK_DEPENDENCY" in codes
