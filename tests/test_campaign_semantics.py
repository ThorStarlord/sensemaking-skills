from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignState,
    CampaignConstitution,
    Capability,
    CapabilityAvailability,
    Dependency,
    DependencyType,
    Responsibility,
    TerminalState,
    TransitionRecord,
    Uncertainty,
    AvailabilityStatus,
    CapabilityRegistry,
    RegisteredCapability,
    validate_reconstruction,
)


def _responsibility(status="active"):
    return Responsibility(
        id="R-1",
        statement="qualify candidate",
        trigger_evidence=("E-1",),
        decision_blocked="whether candidate can proceed",
        scope="integration qualification",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("qualified", "owner_decision_required"),
        status=status,
    )


def test_valid_campaign_history_reconstructs_current_state():
    initial = CampaignState(
        campaign_id="campaign-1",
        mission="qualify integration",
        status="active",
        current_state="qualification",
        active_uncertainty=Uncertainty(
            id="U-1", question="can candidate integrate?", consequences={"yes": "qualify", "no": "owner_decision_required"}
        ),
        active_responsibility=_responsibility(),
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
    )
    transition = TransitionRecord(
        id="T-1", from_state="qualification", to_state="owner_decision_required",
        evidence=("E-2",), decision="candidate conflicts with current main",
        next_responsibility=None, terminal_state=TerminalState.OWNER_DECISION_REQUIRED,
    )
    result = validate_reconstruction(initial, (transition,), existing_evidence={"E-1", "E-2"})
    assert result.valid


def test_validator_rejects_two_active_responsibilities_and_broken_chain():
    state = CampaignState(
        campaign_id="campaign-1", mission="m", status="active", current_state="s",
        active_responsibility=_responsibility(), authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        additional_active_responsibilities=(_responsibility(),),
    )
    transition = TransitionRecord(
        id="T-1", from_state="wrong", to_state="s2", evidence=("missing",), decision="d",
        next_responsibility="R-1",
    )
    result = validate_reconstruction(state, (transition,), existing_evidence=set())
    assert not result.valid
    assert {d.code for d in result.diagnostics} >= {
        "MULTIPLE_ACTIVE_RESPONSIBILITIES", "BROKEN_TRANSITION_CHAIN", "MISSING_EVIDENCE"
    }


def test_terminal_state_cannot_keep_executable_responsibility():
    state = CampaignState(
        campaign_id="campaign-1", mission="m", status="terminal", current_state="done",
        active_responsibility=_responsibility(), authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        terminal_state=TerminalState.NO_FURTHER_WORK_WARRANTED,
    )
    result = validate_reconstruction(state, (), existing_evidence={"E-1"})
    assert any(d.code == "TERMINAL_STATE_HAS_ACTIVE_RESPONSIBILITY" for d in result.diagnostics)


def test_dependency_types_are_explicit_and_serializable():
    dependency = Dependency(DependencyType.AUTHORITY, "public_pr_creation")
    assert dependency.to_dict() == {"type": "authority", "requires": "public_pr_creation"}


def test_constitution_and_capability_records_keep_policy_separate_from_execution():
    constitution = CampaignConstitution(
        mission="m", principles=("preserve semantic control",), non_goals=("generic planner",),
        terminal_states=(TerminalState.GOAL_ACHIEVED,),
    )
    capability = Capability("repository-analysis", ("repository_diagnosis",), "brief")
    availability = CapabilityAvailability(capability.id, True, "local skill installed")
    assert constitution.non_goals == ("generic planner",)
    assert availability.available and capability.output_artifact == "brief"


def test_registry_reports_unavailable_capability_without_routing():
    registry = CapabilityRegistry([RegisteredCapability(
        Capability("controller-patch", ("controller_analysis",), "analysis"),
        "workflow", True, Authority.AUTHORIZED_AUTONOMOUSLY,
        AvailabilityStatus.UNAVAILABLE, availability_reason="runtime managed",
    )])
    assert registry.candidates("controller_analysis")[0].capability.id == "controller-patch"
    assert registry.validate_reference("controller-patch", executable=True)[0].code == "CAPABILITY_NOT_AVAILABLE"
    assert registry.validate_reference("missing")[0].code == "UNKNOWN_CAPABILITY"
