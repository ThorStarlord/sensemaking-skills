"""Reasoning package: MODEL_WARRANT-driven vertical slice (experimental).

This package is intentionally minimal and self-contained. It is NOT the
production orchestrator path; production-runtime integration is deferred.
See experiments/product-hypothesis-b/implementation/SEAM-AND-CONTRACT-DECISION.md.
"""

from .vertical_slice import (
    EpistemicStatus,
    UncertaintyKind,
    Warrant,
    WarrantDecision,
    ReasoningEpisode,
    PartialRepresentation,
    DecisionSynthesis,
    SensemakingBrief,
    judge_warrant,
    run_reasoning_episode,
    WarrantGateProbeError,
)
from .warrant_gate import WarrantRecord, run_seam_warrant
from .evidence_probes import (
    EvidenceInput,
    EvidenceDerivation,
    ProbeResult,
    PROBE_TRUE,
    PROBE_FALSE,
    PROBE_UNKNOWN,
    derive_probes,
    probes_to_warrant,
)

__all__ = [
    "EpistemicStatus",
    "UncertaintyKind",
    "Warrant",
    "WarrantDecision",
    "ReasoningEpisode",
    "PartialRepresentation",
    "DecisionSynthesis",
    "SensemakingBrief",
    "judge_warrant",
    "run_reasoning_episode",
    "WarrantGateProbeError",
    "WarrantRecord",
    "run_seam_warrant",
    "EvidenceInput",
    "EvidenceDerivation",
    "ProbeResult",
    "PROBE_TRUE",
    "PROBE_FALSE",
    "PROBE_UNKNOWN",
    "derive_probes",
    "probes_to_warrant",
]
