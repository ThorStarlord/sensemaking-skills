"""Orthogonality qualification (directive #10): MODEL_WARRANT vs action outcome.

Proves the ratified orthogonality matrix all co-exist:
  - MODEL_WARRANT=NO + action warranted
  - MODEL_WARRANT=NO + NO_CHANGE
  - MODEL_WARRANT=PARTIAL + action warranted
  - MODEL_WARRANT=PARTIAL + NO_CHANGE
  - INCONCLUSIVE MUST NOT imply NO_CHANGE (G)
  - NO-warrant can still lead to an action-bearing recommendation (E)
  - PARTIAL can lead to either action or NO_CHANGE (F)
  - a brief emits NO_CHANGE only via an explicit affirmative decision (C/D);
    never inferred from warrant, missing workflow, or insufficient evidence.
"""
from sensemaking_skills.reasoning.vertical_slice import (
    ReasoningEpisode,
    run_reasoning_episode,
)


def _episode(user_goal="establish the consequential boundary"):
    return ReasoningEpisode(
        target_repository="genre-neutral/target",
        target_revision="abc",
        user_goal=user_goal,
    )


# MODEL_WARRANT = NO (evidence sufficient; no flow/provenance gap)
_NO_PROBES = dict(
    existing_evidence_sufficient=True,
    behavioral_flow_unassembled=False,
    provenance_scattered=False,
    existing_artifact_self_derived=False,
    fresh_comprehension_needed=False,
    minimum_subset_suffices=False,
)

# MODEL_WARRANT = PARTIAL (flow/provenance gap; minimum subset suffices)
_PARTIAL_PROBES = dict(
    existing_evidence_sufficient=False,
    behavioral_flow_unassembled=True,
    provenance_scattered=True,
    existing_artifact_self_derived=False,
    fresh_comprehension_needed=True,
    minimum_subset_suffices=True,
)


def test_warrant_no_plus_action_warranted():
    """MODEL_WARRANT=NO, no affirmative NO_CHANGE -> action-bearing result."""
    out = run_reasoning_episode(_episode(), **_NO_PROBES)
    assert out["warrant_decision"].warrant.value == "NO"
    assert out["no_change"] is False
    assert out["brief"].is_no_change is False
    assert "NO_REPOSITORY_CHANGE_WARRANTED" not in out["brief"].warranted_responsibility


def test_warrant_no_plus_no_change():
    """MODEL_WARRANT=NO + explicit affirmative NO_CHANGE decision."""
    out = run_reasoning_episode(_episode(), decision_no_change=True, **_NO_PROBES)
    assert out["warrant_decision"].warrant.value == "NO"
    assert out["no_change"] is True
    assert out["brief"].is_no_change is True


def test_warrant_partial_plus_action_warranted():
    """MODEL_WARRANT=PARTIAL, no NO_CHANGE -> action outcome, representation materialized."""
    out = run_reasoning_episode(_episode(), **_PARTIAL_PROBES)
    assert out["warrant_decision"].warrant.value == "PARTIAL"
    assert out["materialized_representation"] is not None
    assert out["no_change"] is False
    assert out["brief"].is_no_change is False


def test_warrant_partial_plus_no_change():
    """MODEL_WARRANT=PARTIAL + explicit affirmative NO_CHANGE decision."""
    out = run_reasoning_episode(_episode(), decision_no_change=True, **_PARTIAL_PROBES)
    assert out["warrant_decision"].warrant.value == "PARTIAL"
    assert out["no_change"] is True
    assert out["brief"].is_no_change is True


def test_no_warrant_never_implies_no_change():
    """C/D: a brief never emits NO_CHANGE from MODEL_WARRANT=NO alone."""
    out = run_reasoning_episode(_episode(), **_NO_PROBES)  # decision_no_change defaults False
    assert out["no_change"] is False
    assert out["brief"].is_no_change is False


def test_inconclusive_never_implies_no_change():
    """G: INCONCLUSIVE must NEVER become NO_CHANGE (a load-bearing UNKNOWN stops
    with uncertainty, not a no-change conclusion)."""
    from sensemaking_skills.reasoning.warrant_gate import (
        run_seam_warrant, EvidenceInput,
    )
    # No evidence -> all probes UNKNOWN -> warrant INCONCLUSIVE.
    rec = run_seam_warrant(
        target_repository="t", target_revision="r",
        user_goal="g", evidence=EvidenceInput(),
    )
    assert rec.warrant == "INCONCLUSIVE"
    # INCONCLUSIVE sets no_change False (never turns into NO_CHANGE).
    assert rec.no_change is False
    rec_nc = run_seam_warrant(
        target_repository="t", target_revision="r",
        user_goal="g", evidence=EvidenceInput(),
    )
    assert rec_nc.warrant == "INCONCLUSIVE"
    assert rec_nc.no_change is False
    # And no representation is materialized on INCONCLUSIVE.
    assert not rec.representation_materialized
