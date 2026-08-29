"""Production-seam warrant gate (bounded integration).

Thin, production-safe wrapper around the qualified vertical slice. It is the
only surface `workflow-runtime.py` (and any future caller) touches, so the
warrant logic stays in the tested module while production gets a minimal,
non-invasive hook.

Boundary guarantees:
  - Never raises on normal operation: any warrant computation error is caught
    and returned as an INCONCLUSIVE-with-reason record so a production call can
    log-and-continue rather than abort brief production.
  - Does NOT mutate repository native evidence, does NOT create an empty
    representation (`NO` -> none), and for `PARTIAL` only records a minimal
    representation record.
  - Existing behavior is preserved: this module does not change how the existing
    repo-sensemaker skill produces the brief; it only computes + records a
    warrant decision at the seam.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .vertical_slice import (
    ReasoningEpisode,
    SensemakingBrief,
    Uncertainty,
    UncertaintyKind,
    Warrant,
)
from .evidence_probes import (
    EvidenceInput,
    derive_probes,
    probes_to_warrant,
)


@dataclass
class WarrantRecord:
    """The seam-facing record of a MODEL_WARRANT decision + any minimal
    representation projection. Serializable; provenance-bearing."""

    warrant: str                       # NO | PARTIAL | FULL | INCONCLUSIVE
    target_repository: str
    target_revision: str
    user_goal: str
    representation_materialized: bool
    representation: Optional[dict] = None   # minimal bounded dict (PARTIAL)
    brief: Optional[dict] = None            # brief projection when produced
    no_change: bool = False
    uncertainty_log: List[Dict[str, Any]] = field(default_factory=list)
    derivation: List[Dict[str, Any]] = field(default_factory=list)  # per-probe
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warrant": self.warrant,
            "target_repository": self.target_repository,
            "target_revision": self.target_revision,
            "user_goal": self.user_goal,
            "representation_materialized": self.representation_materialized,
            "representation": self.representation,
            "brief": self.brief,
            "no_change": self.no_change,
            "uncertainty_log": self.uncertainty_log,
            "derivation": self.derivation,
            "error": self.error,
        }

    def as_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def run_seam_warrant(
    *,
    target_repository: str,
    target_revision: str,
    user_goal: str,
    evidence: Optional[EvidenceInput] = None,
) -> WarrantRecord:
    """Compute a MODEL_WARRANT decision at the production seam from REAL evidence.

    Args:
        target_repository/target_revision/user_goal: episode identity.
        evidence: observable production evidence (probe-report + brief machine +
            evidence lines). If None, a no-evidence input is used (all probes
            UNKNOWN -> INCONCLUSIVE, per the amendment — no fabricated booleans).
    """
    ev = evidence if evidence is not None else EvidenceInput()
    episode = ReasoningEpisode(
        target_repository=target_repository,
        target_revision=target_revision,
        user_goal=user_goal,
    )
    record = WarrantRecord(
        warrant=Warrant.INCONCLUSIVE.value,
        target_repository=target_repository,
        target_revision=target_revision,
        user_goal=user_goal,
        representation_materialized=False,
    )

    try:
        deriv = derive_probes(ev)
        warrant = probes_to_warrant(deriv)
        record.warrant = warrant.value
        # ORTHOGONALITY (ratified directive #10): MODEL_WARRANT and repository-action
        # outcome are distinct. `no_change` is NEVER inferred from the warrant
        # (MODEL_WARRANT=NO does NOT imply no repository change is warranted; it
        # only says no additional representation is needed). NO_CHANGE is an
        # affirmative decision-synthesis outcome carried by the brief's `outcome`
        # field. Leave record.no_change False here; the synthesis/brief sets it.
        # Record the per-probe derivations for traceability.
        record.derivation = [p.__dict__ for p in deriv.probes]

        if warrant == Warrant.PARTIAL:
            record.representation_materialized = True
            record.representation = {
                "scope": {
                    p.probe or k: {"value": p.value, "basis": p.basis}
                    for k, p in enumerate(deriv.probes)
                },
                "note": "Minimal PARTIAL representation projection (orientation/"
                        "behavioral/context). Brief production remains delegated "
                        "to the repo-sensemaker skill.",
            }
        elif warrant == Warrant.FULL:
            # Not implemented in this bounded slice (deferred). Record intent;
            # do not fabricate a full representation.
            record.representation_materialized = False
        elif warrant == Warrant.INCONCLUSIVE:
            record.uncertainty_log.append(
                {
                    "kind": UncertaintyKind.UNKNOWN.value,
                    "question": "Model warrant is INCONCLUSIVE because one or "
                                "more load-bearing probes are UNKNOWN / "
                                "unresolved. Preserve uncertainty or request "
                                "human input; do NOT auto-escalate and do NOT "
                                "materialize an unjustified representation.",
                    "load_bearing": True,
                    "unresolved_probes": deriv.load_bearing_unknown,
                }
            )
        # NO: no representation materialized.
        record.error = None
    except Exception as exc:  # defensive: never break the seam
        record.warrant = Warrant.INCONCLUSIVE.value
        record.error = f"warrant computation failed at seam: {exc}"

    return record


# Optional export for ergonomics.
__all__ = ["WarrantRecord", "run_seam_warrant"]
