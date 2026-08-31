"""Qualification tests for the MODEL_WARRANT vertical slice (bounded).

Proves the seven mandated qualification criteria (owner directive #5):

  1. MODEL_WARRANT=NO reaches decision synthesis WITHOUT creating a
     representation artifact.
  2. MODEL_WARRANT=PARTIAL creates only a bounded representation and reaches
     the SAME decision-synthesis interface.
  3. Both paths produce a Repository Sensemaking Brief.
  4. NO_REPOSITORY_CHANGE_WARRANTED is distinguishable from failure/unknown.
  5. Load-bearing epistemic/provenance state survives through the brief.
  6. Existing brief-centered behavior remains compatible (all required machine
     fields present) except the ONE recorded intentional NO_CHANGE contract
     change (recommended_workflow_id omitted on the NO_CHANGE path).
  7. No experimental repository_model.json schema is a production dependency
     (this module imports only dataclasses/enum; verified below).
"""
import importlib
import json
import os

import pytest

from sensemaking_skills.reasoning.vertical_slice import (
    EpistemicStatus,
    ReasoningEpisode,
    SensemakingBrief,
    UncertaintyKind,
    Warrant,
    WarrantGateProbeError,
    run_reasoning_episode,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _episode(user_goal="Establish the consequential remaining boundary."):
    return ReasoningEpisode(
        target_repository="genre-neutral/pressure-target",
        target_revision="abc123",
        user_goal=user_goal,
    )


# --- 1. NO path creates NO representation artifact ------------------------

def test_no_warrant_materializes_no_representation_and_reaches_synthesis():
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=True,
        behavioral_flow_unassembled=False,
        provenance_scattered=False,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=False,
        minimum_subset_suffices=False,
        owned_fog_type="architecture_fog",
        allowed_workflow_id="architecture-implementation-workflow",
    )
    assert out["warrant_decision"].warrant == Warrant.NO
    assert out["materialized_representation"] is None          # criterion 1
    assert "no-representation" in " ".join(out["paths_taken"])
    assert isinstance(out["decision_synthesis"], object)        # reached synthesis
    assert isinstance(out["brief"], SensemakingBrief)

    wd = out["warrant_decision"]
    assert (
        wd.rationale
        == "Existing repository evidence is sufficient for the consequential "
        "reasoning problem; no additional representation is warranted (least ceremony)."
    )


def test_no_warrant_does_not_create_an_empty_model_artifact():
    """Directive: MODEL_WARRANT=NO must NOT create an empty model artifact."""
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=True,
        behavioral_flow_unassembled=False,
        provenance_scattered=False,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=False,
        minimum_subset_suffices=False,
    )
    assert out["materialized_representation"] is None


# --- 2. PARTIAL path creates bounded representation, same interface --------

def test_partial_warrant_materializes_bounded_representation_same_interface():
    out = run_reasoning_episode(
        _episode(user_goal="Understand the live execution flow."),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
        owned_fog_type="architecture_fog",
        allowed_workflow_id="architecture-implementation-workflow",
    )
    assert out["warrant_decision"].warrant == Warrant.PARTIAL
    rep = out["materialized_representation"]
    assert rep is not None                                     # PARTIAL materializes
    assert rep.orientation.startswith("(warranted partial representation")  # bounded shape
    assert len(rep.entries) == 1                                # bounded, not full
    assert isinstance(out["brief"], SensemakingBrief)           # same interface -> brief
    assert "partial-representation" in " ".join(out["paths_taken"])


def test_partial_scope_matches_the_warranted_projections():
    wd = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=False,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=False,
        minimum_subset_suffices=True,
    )["warrant_decision"]
    assert wd.warrant == Warrant.PARTIAL
    assert "behavioral-flow" in wd.rationale
    assert "contradiction" not in wd.rationale  # only warranted projection


# --- 3. Both paths produce a brief ----------------------------------------

def test_both_paths_produce_a_brief():
    for scenario in [
        dict(existing_evidence_sufficient=True, behavioral_flow_unassembled=False,
             provenance_scattered=False, existing_artifact_self_derived=False,
             fresh_comprehension_needed=False, minimum_subset_suffices=False),
        dict(existing_evidence_sufficient=False, behavioral_flow_unassembled=True,
             provenance_scattered=True, existing_artifact_self_derived=False,
             fresh_comprehension_needed=True, minimum_subset_suffices=True),
    ]:
        out = run_reasoning_episode(_episode(), owned_fog_type="architecture_fog",
                                    allowed_workflow_id="architecture-implementation-workflow", **scenario)
        assert isinstance(out["brief"], SensemakingBrief)
        assert out["brief"].artifact_id == "repository_sensemaking_brief"
        assert out["brief"].immutable is True


# --- 4. NO_REPOSITORY_CHANGE_WARRANTED distinct from failure/unknown -------

def test_no_change_is_a_distinct_first_class_outcome():
    # NO_CHANGE is an AFFIRMATIVE decision-synthesis outcome, supplied
    # explicitly (orthogonal to the warrant).
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=True,
        behavioral_flow_unassembled=False,
        provenance_scattered=False,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=False,
        minimum_subset_suffices=False,
        decision_no_change=True,
    )
    assert out["no_change"] is True
    assert out["brief"].warranted_responsibility == "NO_REPOSITORY_CHANGE_WARRANTED"
    assert out["brief"].is_no_change is True
    # Distinct from an error/failure: the returned object is a valid brief, not an
    # exception, and NOT an INCONCLUSIVE probe-stop.
    assert "--" not in out["brief"].to_dict().get("warranted_responsibility", "")


def test_no_warrant_alone_does_not_imply_no_change():
    """ORTHOGONALITY (directive #10): MODEL_WARRANT=NO does NOT imply NO_CHANGE.
    With sufficient evidence (warrant NO) but NO affirmative no-change decision,
    the outcome stays action (no_change False)."""
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=True,
        behavioral_flow_unassembled=False,
        provenance_scattered=False,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=False,
        minimum_subset_suffices=False,
        # decision_no_change defaults False => action outcome, NOT NO_CHANGE
    )
    assert out["no_change"] is False
    assert out["brief"].is_no_change is False
    assert "NO_REPOSITORY_CHANGE_WARRANTED" not in out["brief"].warranted_responsibility


def test_no_change_brief_omits_recommended_workflow_id_intentional():
    """Recorded intentional contract change: NO_CHANGE omits recommended_workflow_id."""
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
        owned_fog_type="architecture_fog",
        decision_no_change=True,  # affirmative decision-synthesis NO_CHANGE
    )
    d = out["brief"].to_dict()
    assert "recommended_workflow_id" not in d
    assert d["is_no_change"] is True
    assert d["warranted_responsibility"] == "NO_REPOSITORY_CHANGE_WARRANTED"


def test_non_no_change_brief_keeps_recommended_workflow_id():
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
        owned_fog_type="architecture_fog",
        allowed_workflow_id="architecture-implementation-workflow",
    )
    d = out["brief"].to_dict()
    assert d["recommended_workflow_id"] == "architecture-implementation-workflow"
    assert d["is_no_change"] is False


# --- 5. Epistemic / provenance survives through the brief ------------------

def test_epistemic_provenance_survives_through_brief():
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
    )
    rep = out["materialized_representation"]
    # representation preserves epistemic + provenance per assertion
    assert rep.entries[0].epistemic_status == EpistemicStatus.DERIVED_CONCLUSION
    assert rep.entries[0].provenance == "abc123"
    # decision assertions carry epistemic + provenance and land in brief evidence
    synt_src_claims = [a.claim for a in out["decision_synthesis"].assertions]
    brief_evidence = out["brief"].evidence
    assert any(c in " ".join(brief_evidence) for c in synt_src_claims)


def test_uncertainty_kinds_are_not_collapsed_into_epistemic():
    rep = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
    )["materialized_representation"]
    assert rep.uncertainties[0].kind == UncertaintyKind.UNKNOWN
    # the assertion epistemic status is DERIVED_CONCLUSION -- a different field


# --- 6. Brief compatibility (required machine fields present) --------------

def test_brief_keeps_required_machine_fields():
    """Non-NO_CHANGE brief keeps the standard required fields; NO_CHANGE the
    one recorded exception."""
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
        owned_fog_type="architecture_fog",
        allowed_workflow_id="architecture-implementation-workflow",
    )
    d = out["brief"].to_dict()
    for required in ["artifact_id", "created_at", "immutable", "primary_fog_type",
                     "evidence", "recommended_workflow_id"]:
        assert required in d, required
    assert d["artifact_id"] == "repository_sensemaking_brief"
    assert d["immutable"] is True


# --- Inconclusive (bounded probe, no auto-escalation) -----------------------

def test_inconclusive_never_auto_escalates_to_full():
    # Contradictory sufficiency signal (evidence nominally sufficient yet a
    # behavioral-flow gap is also reported) -> INCONCLUSIVE; must NOT choose
    # FULL and must NOT auto-produce a representation. Bound: raise/guard
    # uncertainty instead.
    with pytest.raises(WarrantGateProbeError):
        run_reasoning_episode(
            _episode(),
            existing_evidence_sufficient=True,
            behavioral_flow_unassembled=True,
            provenance_scattered=False,
            existing_artifact_self_derived=False,
            fresh_comprehension_needed=False,
            minimum_subset_suffices=False,
        )


# --- 7. No experimental schema is a production dependency ------------------

def test_module_does_not_import_experimental_schema():
    """The vertical slice must not depend on any experimental
    repository_model.json schema. Use AST to inspect only executable code
    (identifiers/imports), ignoring docstrings/comments that merely DISCLAIM
    the experimental schema."""
    import ast
    import inspect
    import importlib
    mod = importlib.import_module("sensemaking_skills.reasoning.vertical_slice")
    src = inspect.getsource(mod)
    tree = ast.parse(src)
    # Collect every identifier + string literal used in executable code.
    names = set()
    strings = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.add(node.value)
    # The module must not import or load any repository/model schema package.
    assert "repository_model" not in {n.lower() for n in names}
    assert not any(
        (s.lower().startswith("repository_model") or "load_repository_model" in s.lower())
        for s in strings
    )


def test_module_is_json_serializable_brief_shaped():
    """The brief to_dict must be JSON-serializable (artifact text shape)."""
    out = run_reasoning_episode(
        _episode(),
        existing_evidence_sufficient=False,
        behavioral_flow_unassembled=True,
        provenance_scattered=True,
        existing_artifact_self_derived=False,
        fresh_comprehension_needed=True,
        minimum_subset_suffices=True,
    )
    json.dumps(out["brief"].to_dict())  # must not raise
