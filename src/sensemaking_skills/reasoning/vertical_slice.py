"""Vertical slice: MODEL_WARRANT-driven Sensemaking reasoning loop (experimental).

BOUNDED VERTICAL SLICE only. This module proves the ratified product-direction
semantic loop end-to-end and in isolation:

    user goal
      -> evidence baseline
      -> MODEL_WARRANT  (NO / PARTIAL / FULL / INCONCLUSIVE)
      -> NO  direct-reasoning path (NO representation artifact)
         |  PARTIAL minimum-representation path (bounded representation)
      -> decision synthesis
      -> consequential boundary
      -> warranted responsibility / NO_REPOSITORY_CHANGE_WARRANTED
      -> Repository Sensemaking Brief (brief-compatible shape)

It is self-contained and does NOT modify or depend on the production
orchestrator (scripts/workflow-runtime.py), the repo-sensemaker skill, or any
experimental repository_model.json schema. It uses only this module's own
minimal semantic dataclasses. Production-runtime integration is explicitly
deferred (see experiments/product-hypothesis-b/implementation/SEAM-AND-CONTRACT-DECISION.md).

Epistemic discipline (owner directive #5, D3-1):
  - assertion epistemic status: DEMONSTRATED_FACT / DERIVED_CONCLUSION /
    INTERPRETATION / HYPOTHESIS
  - uncertainty kinds (separate field): UNKNOWN / MISSING_EVIDENCE /
    CONFLICTING_EVIDENCE / OWNER_INTENT / EXTERNAL_ENVIRONMENT_UNKNOWN
  - uncertainty, confidence, and epistemic status are NEVER collapsed into one.

One recorded intentional contract change (NO_CHANGE path only): the brief may
omit ``recommended_workflow_id`` and instead carry
``warranted_responsibility = NO_REPOSITORY_CHANGE_WARRANTED``. All other brief
output mimics the existing brief's required machine fields.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ---------------------------------------------------------------------------
# Epistemic vocabulary (ratified D3-1)
# ---------------------------------------------------------------------------

class EpistemicStatus(str, Enum):
    DEMONSTRATED_FACT = "DEMONSTRATED_FACT"
    DERIVED_CONCLUSION = "DERIVED_CONCLUSION"
    INTERPRETATION = "INTERPRETATION"
    HYPOTHESIS = "HYPOTHESIS"


class UncertaintyKind(str, Enum):
    UNKNOWN = "UNKNOWN"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"
    OWNER_INTENT = "OWNER_INTENT"
    EXTERNAL_ENVIRONMENT_UNKNOWN = "EXTERNAL_ENVIRONMENT_UNKNOWN"


@dataclass
class Uncertainty:
    kind: UncertaintyKind
    question: str
    affects: List[str] = field(default_factory=list)
    resolution: str = ""
    load_bearing: bool = False


@dataclass
class Assertion:
    claim: str
    epistemic_status: EpistemicStatus
    evidence: List[str] = field(default_factory=list)
    provenance: str = ""  # repository revision scope
    uncertainty: Optional[Uncertainty] = None


# ---------------------------------------------------------------------------
# MODEL_WARRANT
# ---------------------------------------------------------------------------

class Warrant(str, Enum):
    NO = "NO"
    PARTIAL = "PARTIAL"
    FULL = "FULL"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass
class WarrantDecision:
    warrant: Warrant
    rationale: str
    probes: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Reasoning episode
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReasoningEpisode:
    target_repository: str
    target_revision: str
    user_goal: str
    evidence_baseline_note: str = ""


# ---------------------------------------------------------------------------
# Representation (PARTIAL) — minimal, bounded. NO path creates none.
# ---------------------------------------------------------------------------

@dataclass
class PartialRepresentation:
    orientation: str = ""
    entries: List[Assertion] = field(default_factory=list)
    relationships: List[Assertion] = field(default_factory=list)
    behavioral_flow: List[str] = field(default_factory=list)
    uncertainties: List[Uncertainty] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Decision synthesis
# ---------------------------------------------------------------------------

@dataclass
class DecisionSynthesis:
    consequential_boundary: str
    warranted_responsibility: str  # description, or NO_REPOSITORY_CHANGE_WARRANTED
    is_no_change: bool
    rationale: str
    assertions: List[Assertion] = field(default_factory=list)


class BriefProduced(Exception):
    """Guard: produced brief should only ever be read back, never mutated."""


@dataclass(frozen=True)
class SensemakingBrief:
    artifact_id: str
    created_at: str
    immutable: bool
    primary_fog_type: Optional[str]
    evidence: List[str]
    consequential_boundary: str
    warranted_responsibility: str
    is_no_change: bool
    recommended_workflow_id: Optional[str]  # omitted on NO_CHANGE path
    source_path: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize the brief for artifact-style persistence (minimal dict).

        Mirrors the existing brief's required machine fields, EXCEPT that the
        NO_CHANGE path omits ``recommended_workflow_id`` (recorded intentional
        contract decision).
        """
        d = {
            "artifact_id": self.artifact_id,
            "created_at": self.created_at,
            "immutable": self.immutable,
        }
        if self.primary_fog_type is not None:
            d["primary_fog_type"] = self.primary_fog_type
        d["evidence"] = list(self.evidence)
        d["consequential_boundary"] = self.consequential_boundary
        d["warranted_responsibility"] = self.warranted_responsibility
        d["is_no_change"] = self.is_no_change
        if self.recommended_workflow_id is not None:
            d["recommended_workflow_id"] = self.recommended_workflow_id
        if self.source_path is not None:
            d["source_path"] = self.source_path
        return d


# ---------------------------------------------------------------------------
# MODEL_WARRANT judgment (pure; deterministic given probes)
# ---------------------------------------------------------------------------

def judge_warrant(
    *,
    existing_evidence_sufficient: bool,
    behavioral_flow_unassembled: bool,
    provenance_scattered: bool,
    existing_artifact_self_derived: bool,
    fresh_comprehension_needed: bool,
    minimum_subset_suffices: bool,
) -> WarrantDecision:
    """Determine MODEL_WARRANT from genre-neutral sufficiency probes.

    Mirrors the ratified MODEL_WARRANT semantics (owner directive #5 / D1-2):
      - NO       : existing evidence sufficient  (least ceremony default)
      - PARTIAL  : some missing context/relationships/behavior only
      - FULL     : broad representation warranted for the current scope
      - INCONCLUSIVE: cannot decide; bounded probe then preserve-uncertainty/human
    """
    if existing_evidence_sufficient and not behavioral_flow_unassembled:
        return WarrantDecision(
            warrant=Warrant.NO,
            rationale="Existing repository evidence is sufficient for the "
                      "consequential reasoning problem; no additional "
                      "representation is warranted (least ceremony).",
            probes={"existing_evidence_sufficient": True},
        )
    if existing_artifact_self_derived and existing_evidence_sufficient:
        # Self-derived concise artifacts (e.g. validator output) make a separate
        # model redundant for decision support (Iteration-4 counterevidence).
        return WarrantDecision(
            warrant=Warrant.NO,
            rationale="Existing artifact is already self-derived concise "
                      "output; a separately materialized representation would "
                      "be redundant.",
            probes={"existing_artifact_self_derived": True},
        )
    if existing_evidence_sufficient and (
        behavioral_flow_unassembled or provenance_scattered
    ):
        # Contradictory sufficiency signal: evidence is nominally sufficient but
        # a flow/provenance gap is also reported. We cannot cleanly choose NO,
        # nor justify PARTIAL/FULL on the current signal -- bounded probe.
        return WarrantDecision(
            warrant=Warrant.INCONCLUSIVE,
            rationale="Existing evidence is reported sufficient yet a behavioral "
                      "flow or provenance gap is also present; the warrant is "
                      "indeterminate. A bounded evidence probe is permitted, after "
                      "which load-bearing uncertainty must be preserved or a human "
                      "consulted (no auto-escalation to FULL).",
            probes={
                "existing_evidence_sufficient": True,
                "behavioral_flow_unassembled": behavioral_flow_unassembled,
                "provenance_scattered": provenance_scattered,
            },
        )
    if minimum_subset_suffices or behavioral_flow_unassembled:
        scope = []
        if behavioral_flow_unassembled:
            scope.append("behavioral-flow")
        if provenance_scattered:
            scope.append("contradiction-uncertainty-context")
        if fresh_comprehension_needed:
            scope.append("orientation")
        return WarrantDecision(
            warrant=Warrant.PARTIAL,
            rationale="Existing evidence is insufficient for the reasoning "
                      "problem; materialize ONLY the missing "
                      "projections: " + (", ".join(scope) if scope else "behaviour"),
            probes={
                "behavioral_flow_unassembled": behavioral_flow_unassembled,
                "provenance_scattered": provenance_scattered,
                "fresh_comprehension_needed": fresh_comprehension_needed,
                "minimum_subset_suffices": minimum_subset_suffices,
            },
        )
    if not existing_evidence_sufficient and not minimum_subset_suffices:
        return WarrantDecision(
            warrant=Warrant.FULL,
            rationale="Broad representation is warranted for the current "
                      "reasoning scope (NOT exhaustive permanent modeling).",
            probes={"existing_evidence_sufficient": False},
        )
    return WarrantDecision(
        warrant=Warrant.INCONCLUSIVE,
        rationale="Cannot determine warrant from current evidence; a bounded "
                  "probe is permitted, after which load-bearing uncertainty "
                  "must be preserved or a human consulted (no auto-escalation).",
        probes={},
    )


# ---------------------------------------------------------------------------
# Default probes -> model-warrant gate driver (single operating loop)
# ---------------------------------------------------------------------------

class WarrantGateProbeError(ValueError):
    """Raised when a reasoning episode cannot be bounded if INCONCLUSIVE."""


def run_reasoning_episode(
    episode: ReasoningEpisode,
    *,
    existing_evidence_sufficient: bool,
    behavioral_flow_unassembled: bool,
    provenance_scattered: bool,
    existing_artifact_self_derived: bool,
    fresh_comprehension_needed: bool,
    minimum_subset_suffices: bool,
    owned_fog_type: Optional[str] = None,
    allowed_workflow_id: Optional[str] = None,
    decision_no_change: bool = False,
) -> dict:
    """Run one Sensemaking reasoning episode end-to-end.

    Deterministic. Returns a dict with keys:
      episode, warrant_decision, materialized_representation (None when NO),
      decision_synthesis, brief (SensemakingBrief), no_change, paths_taken.

    For MODEL_WARRANT=NO, ``materialized_representation`` is None and the loop
    reasons directly over native evidence (no empty representation artifact).
    For PARTIAL, a bounded representation is materialized and passed to the
    same decision-synthesis interface.

    ORTHOGONALITY (directive #10): ``warrant`` (representation sufficiency) and
    ``decision_no_change`` (repository-action outcome) are independent. NO_CHANGE
    is an AFFIRMATIVE decision-synthesis result supplied via ``decision_no_change``,
    never inferred from the warrant.
    """
    wd = judge_warrant(
        existing_evidence_sufficient=existing_evidence_sufficient,
        behavioral_flow_unassembled=behavioral_flow_unassembled,
        provenance_scattered=provenance_scattered,
        existing_artifact_self_derived=existing_artifact_self_derived,
        fresh_comprehension_needed=fresh_comprehension_needed,
        minimum_subset_suffices=minimum_subset_suffices,
    )

    if wd.warrant == Warrant.INCONCLUSIVE:
        # Bounded evidence probe is a no-op here; we never auto-escalate.
        raise WarrantGateProbeError(
            "MODEL_WARRANT = INCONCLUSIVE: a bounded evidence probe is permitted; "
            "if unresolved, load-bearing uncertainty must be preserved or a human "
            "must be consulted, rather than automatically escalating to FULL."
        )

    representation: Optional[PartialRepresentation] = None
    paths_taken: List[str] = []

    if wd.warrant == Warrant.NO:
        paths_taken.append("no-representation: reason-directly-from-native-evidence")
        # NO path materializes NO representation artifact (directive: NO must not
        # create an empty representation artifact).
        representation = None
    else:  # PARTIAL (or, in this slice, we only materialize the bounded case)
        paths_taken.append("partial-representation: materialize-minimum-projection")
        representation = _materialize_partial(episode, wd.probes)

    synthesis = _synthesize_decision(
        episode=episode,
        wd=wd,
        representation=representation,
        decision_no_change=decision_no_change,
        reduction_note=(
            "Reasoned from native evidence (NO path): no representation "
            "artifact materialized." if representation is None else None
        ),
    )

    brief = _emit_brief(
        episode=episode,
        synthesis=synthesis,
        owned_fog_type=owned_fog_type,
        allowed_workflow_id=allowed_workflow_id,
    )

    return {
        "episode": episode,
        "warrant_decision": wd,
        "materialized_representation": representation,
        "decision_synthesis": synthesis,
        "no_change": synthesis.is_no_change,
        "brief": brief,
        "paths_taken": paths_taken,
    }


def _materialize_partial(episode: ReasoningEpisode, probes: dict) -> PartialRepresentation:
    """Materialize a bounded, evidence-tagged partial representation.

    This is intentionally composable: in production a real evidence pass would
    populate this. The slice provides the shape + epistemic tagging and does
    not fabricate repository-specific evidence values.
    """
    return PartialRepresentation(
        orientation="(warranted partial representation for episode: "
                    f"{episode.target_repository} @ {episode.target_revision}; "
                    f"goal: {episode.user_goal})",
        entries=[
            Assertion(
                claim="A warranted PARTIAL representation materializes only the "
                      "structure needed for the consequential problem.",
                epistemic_status=EpistemicStatus.DERIVED_CONCLUSION,
                provenance=episode.target_revision,
            )
        ],
        uncertainties=[
            Uncertainty(
                kind=UncertaintyKind.UNKNOWN,
                question="Unknowns not resolved in this bounded slice are "
                         "preserved, not converted to certainty.",
                load_bearing=False,
            )
        ],
    )


def _synthesize_decision(
    episode: ReasoningEpisode,
    wd: WarrantDecision,
    representation: Optional[PartialRepresentation],
    decision_no_change: bool,
    reduction_note: Optional[str],
) -> DecisionSynthesis:
    """Decision synthesis: consequential boundary + warranted responsibility.

    Sensemaking judgment; the representation (when present) only surfaces
    candidates. In this bounded slice the decision inputs are supplied as
    deterministic episode/goal facts; a real evidence pass would derive them.
    ``decision_no_change`` is the AFFIRMATIVE repository-action outcome decision
    (orthogonal to the warrant).
    """
    no_change = decision_no_change
    if no_change:
        return DecisionSynthesis(
            consequential_boundary="No repository change is warranted on the "
                                   "current evidence for this reasoning episode.",
            warranted_responsibility="NO_REPOSITORY_CHANGE_WARRANTED",
            is_no_change=True,
            rationale="The evidence/resolution for the episode's goal does not "
                      "demand a repository change; NO_REPOSITORY_CHANGE_WARRANTED "
                      "is a first-class successful outcome, distinct from "
                      "insufficient evidence or failure.",
            assertions=[
                Assertion(
                    claim="No change warranted for the given episode goal and evidence.",
                    epistemic_status=EpistemicStatus.DERIVED_CONCLUSION,
                    provenance=episode.target_revision,
                )
            ],
        )

    boundary = (
        "Consequential boundary derived for episode goal: " + episode.user_goal
    )
    responsibility = (
        "Warranted next responsibility: address the derived consequential boundary "
        "within the allowed workflow (see brief)."
    )
    return DecisionSynthesis(
        consequential_boundary=boundary,
        warranted_responsibility=responsibility,
        is_no_change=False,
        rationale="Decision synthesis over episode goal + representation/evidence. "
                  + (reduction_note or ""),
        assertions=[
            Assertion(
                claim="Boundary is consequential for this episode goal.",
                epistemic_status=EpistemicStatus.INTERPRETATION,
                provenance=episode.target_revision,
            )
        ],
    )


def _emit_brief(
    episode: ReasoningEpisode,
    synthesis: DecisionSynthesis,
    owned_fog_type: Optional[str],
    allowed_workflow_id: Optional[str],
) -> SensemakingBrief:
    """Project the decision synthesis into a brief-compatible artifact.

    For NO_CHANGE (synthesis.is_no_change) the brief OMITS recommended_workflow_id
    (recorded intentional contract decision). All other required machine fields
    are present; immutable=True.
    """
    evidence = [
        a.claim + (" | " + a.provenance if a.provenance else "")
        for a in synthesis.assertions
    ]
    if synthesis.is_no_change:
        return SensemakingBrief(
            artifact_id="repository_sensemaking_brief",
            created_at=str(int(time.time())),
            immutable=True,
            primary_fog_type=owned_fog_type,
            evidence=evidence,
            consequential_boundary=synthesis.consequential_boundary,
            warranted_responsibility=synthesis.warranted_responsibility,
            is_no_change=True,
            recommended_workflow_id=None,  # intentional NO_CHANGE contract decision
        )
    return SensemakingBrief(
        artifact_id="repository_sensemaking_brief",
        created_at=str(int(time.time())),
        immutable=True,
        primary_fog_type=owned_fog_type,
        evidence=evidence,
        consequential_boundary=synthesis.consequential_boundary,
        warranted_responsibility=synthesis.warranted_responsibility,
        is_no_change=False,
        recommended_workflow_id=allowed_workflow_id,
    )
