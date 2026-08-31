"""Real-evidence -> MODEL_WARRANT probe adapter (S1, bounded slice).

The six-probe structure is internal to this bounded slice (NOT ratified as a
permanent product contract). What matters is the amendment's semantics:

    observable repository evidence
      -> explicit probe result (value + basis + epistemic)
      -> MODEL_WARRANT

Rules enforced here (owner directive #8):
  - NEVER infer FALSE merely because evidence is absent.
  - NEVER turn a free-form evidence summary into unsupported confident bools.
  - NEVER introduce repository-specific rules.
  - NEVER encode ViralFactory/interface-skills/delta outcomes.
  - NEVER silently convert UNKNOWN into NO/PARTIAL/FULL.
  - NEVER auto-escalate INCONCLUSIVE.
  - If the real evidence cannot support a probe, record UNKNOWN.
  - If unresolved UNKNOWN is load-bearing, MODEL_WARRANT may be INCONCLUSIVE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .vertical_slice import EpistemicStatus, UncertaintyKind, Warrant


class ProbeValue(str):
    pass


PROBE_TRUE = "TRUE"
PROBE_FALSE = "FALSE"
PROBE_UNKNOWN = "UNKNOWN"


@dataclass
class ProbeResult:
    """A single warrant probe's derivation."""

    probe: str
    value: str                  # TRUE | FALSE | UNKNOWN
    basis: str                  # the observable evidence that supports this value
    epistemic_status: EpistemicStatus
    reason: str = ""            # why UNKNOWN (when value == UNKNOWN)

    def resolved(self) -> bool:
        return self.value != PROBE_UNKNOWN


@dataclass
class EvidenceDerivation:
    """Per-probe derivations + the load-bearing-UNKNOWN summary for one episode."""

    probes: List[ProbeResult] = field(default_factory=list)
    load_bearing_unknown: List[str] = field(default_factory=list)
    # Ruled authority (directive #25): the task-relative representation-
    # sufficiency verdict that determines MODEL_WARRANT. Mechanical probes are
    # reported as diagnostic signals; they do NOT veto this verdict. One of:
    #   Warrant.NO / Warrant.PARTIAL / Warrant.INCONCLUSIVE
    representation_warrant: Optional[Warrant] = None

    def by_probe(self, name: str) -> Optional[ProbeResult]:
        for p in self.probes:
            if p.probe == name:
                return p
        return None


# ---------------------------------------------------------------------------
# Observable signal extractors (real production evidence only; genre-neutral)
# ---------------------------------------------------------------------------

@dataclass
class EvidenceInput:
    """The observable evidence available at the seam (real production path).

    Composed from whatever the production path genuinely has at warrant time:
    - probe_report (dict) if a probe-report.py artifact is present;
    - brief_machine (dict) if a brief section 13 block is available;
    - provided evidence_summary string list (from the brief's evidence field).
    All fields are optional: absent fields yield UNKNOWN, never FALSE.
    ``provenance`` records where the transported evidence came from (e.g. the
    same-episode validated brief / probe-report) so the warrant record can tie
    evidence to the target revision + reasoning episode.
    """

    probe_report: Optional[dict] = None
    brief_machine: Optional[dict] = None
    evidence_lines: List[str] = field(default_factory=list)
    provenance: str = ""
    # Ruling 2 (directive #23): the producer-authored, task-relative
    # representation-sufficiency assessment (an INTERNAL machine input to
    # MODEL_WARRANT). Optional dict:
    #   { "status": "sufficient"|"insufficient_bounded"|"inconclusive",
    #     "rationale": str,
    #     "needed_representation": str|null }
    # Sufficiency/bounded-insufficiency is a REASONING-EPISODE judgment that
    # cannot be reduced to evidence-count or citation-presence heuristics.
    representation_sufficiency: Optional[dict] = None


def _observed(probe: str, test: bool, basis: str, eps: EpistemicStatus) -> ProbeResult:
    return ProbeResult(
        probe=probe, value=PROBE_TRUE if test else PROBE_FALSE, basis=basis,
        epistemic_status=eps,
    )


def derive_probes(evidence: EvidenceInput) -> EvidenceDerivation:
    """Derive the six warrant probes from observable production evidence.

    Each probe returns (value, basis, epistemic). Absence of evidence for a
    probe => value UNKNOWN with reason; NEVER FALSE.
    """
    deriv = EvidenceDerivation()
    probes = {"existing_evidence_sufficient", "behavioral_flow_unassembled",
              "provenance_scattered", "existing_artifact_self_derived",
              "fresh_comprehension_needed", "minimum_subset_suffices"}

    pr = evidence.probe_report or {}
    brief = evidence.brief_machine or {}

    # --- P1: existing_evidence_sufficient -------------------------------
    # Ruling 2 (directive #23): "sufficient" is an AFFIRMATIVE task-relative
    # judgment supplied by the producer (representation_sufficiency.status). It
    # is NEVER inferred from evidence-line presence (presence != decision
    # sufficiency). Mapping:
    #   status == insufficient_bounded (with valid rationale+needed_representation)
    #       -> existing_evidence_sufficient = FALSE (affirmative insufficiency)
    #   status == sufficient                -> existing_evidence_sufficient = TRUE
    #   inconclusive / missing / malformed  -> UNKNOWN (fail closed; no FALSE)
    rs = evidence.representation_sufficiency
    rs_status = rs.get("status") if isinstance(rs, dict) else None
    ib_valid = bool(
        rs_status == "insufficient_bounded"
        and isinstance(rs, dict)
        and isinstance(rs.get("rationale"), str) and rs["rationale"].strip()
        and isinstance(rs.get("needed_representation"), str)
        and rs["needed_representation"].strip()
    )
    # evidence lines may still support grounding/provenance, but not sufficiency
    ev_lines = evidence.evidence_lines or brief.get("evidence") or []
    if rs_status == "insufficient_bounded":
        if ib_valid:
            deriv.probes.append(_observed(
                "existing_evidence_sufficient", False,
                "producer-asserted insufficient_bounded with a specific "
                "consequential gap and a bounded remedy (representation "
                "sufficiency assessment).",
                EpistemicStatus.DERIVED_CONCLUSION,
            ))
        else:
            deriv.probes.append(ProbeResult(
                probe="existing_evidence_sufficient", value=PROBE_UNKNOWN,
                basis="insufficient_bounded asserted but missing required "
                      "rationale / needed_representation; fails closed.",
                epistemic_status=EpistemicStatus.INTERPRETATION,
                reason="cannot affirm insufficiency without the consequential "
                       "gap + bounded remedy (no missing->FALSE).",
            ))
    elif rs_status == "sufficient":
        deriv.probes.append(_observed(
            "existing_evidence_sufficient", True,
            "producer-asserted sufficient for this consequential reasoning "
            "problem (representation sufficiency assessment).",
            EpistemicStatus.DERIVED_CONCLUSION,
        ))
    elif (evidence.probe_report is not None or brief or ev_lines):
        # Some evidence device exists but no affirmative sufficiency verdict.
        deriv.probes.append(
            ProbeResult(
                probe="existing_evidence_sufficient",
                value=PROBE_UNKNOWN,
                basis="evidence device present but no affirmative "
                      "representation-sufficiency verdict; evidence presence "
                      "cannot establish decision sufficiency.",
                epistemic_status=EpistemicStatus.INTERPRETATION,
                reason="cannot assert sufficiency under the amendment (no "
                       "absent->FALSE inference).",
            )
        )
    else:
        deriv.probes.append(
            ProbeResult(
                probe="existing_evidence_sufficient", value=PROBE_UNKNOWN,
                basis="no production evidence artifact available at the seam.",
                epistemic_status=EpistemicStatus.INTERPRETATION,
                reason="no evidence to support a TRUE/FALSE claim.",
            )
        )

    # ------ AUTHORITATIVE MODEL_WARRANT verdict (directive #25) ------
    # representation_sufficiency is the PRIMARY task-relative MODEL_WARRANT
    # authority. Mechanical/diagnostic probes (below) provide evidence TO this
    # assessment but do NOT independently gate the warrant. Mapping:
    #   sufficient                  -> NO
    #   insufficient_bounded valid  -> PARTIAL
    #   inconclusive/missing/malformed -> INCONCLUSIVE (fail closed)
    # FULL is deferred / never inferred.
    if rs_status == "sufficient":
        deriv.representation_warrant = Warrant.NO
    elif rs_status == "insufficient_bounded" and ib_valid:
        deriv.representation_warrant = Warrant.PARTIAL
    else:
        deriv.representation_warrant = Warrant.INCONCLUSIVE

    # --- P2: behavioral_flow_unassembled --------------------------------
    # Observable: probe-report explicit signal OR relationships findings / a
    # brief that names a runtime surface but no assembled flow. We only mark
    # TRUE/FALSE when there is an observable signal; otherwise UNKNOWN.
    rel = (pr or {}).get("relationships") or {}
    rel_findings = 0
    if isinstance(rel, dict):
        for _k, v in rel.items():
            if isinstance(v, dict):
                rel_findings += len(v.get("findings") or [])
    explicit_flow = (
        pr.get("behavioral_flow_unassembled")
        if isinstance(pr, dict)
        else None
    )
    if explicit_flow in (True, False):
        deriv.probes.append(_observed(
            "behavioral_flow_unassembled",
            bool(explicit_flow),
            "explicit production signal present for flow-unassembled.",
            EpistemicStatus.DEMONSTRATED_FACT,
        ))
    elif rel_findings > 0 or (ev_lines and any(
            "flow" in str(l).lower() or "pipeline" in str(l).lower()
            for l in ev_lines)):
        deriv.probes.append(_observed(
            "behavioral_flow_unassembled",
            True,
            f"{rel_findings} relationship finding(s) present or flow/pipeline "
            "evidence line present; flow is unassembled.",
            EpistemicStatus.DERIVED_CONCLUSION,
        ))
    else:
        deriv.probes.append(ProbeResult(
            probe="behavioral_flow_unassembled", value=PROBE_UNKNOWN,
            basis="no observable flow/pipeline/relationship-finding signal.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="cannot assert flow assembled/unassembled without evidence.",
        ))

    # --- P3: provenance_scattered ---------------------------------------
    # Observable: probe-report explicit signal OR relationship findings
    # (doc-vs-tree) or brief evidence lines that cross files.
    cross_file = sum(1 for l in ev_lines if ":" in l)
    explicit_prov = (
        pr.get("provenance_scattered")
        if isinstance(pr, dict)
        else None
    )
    if explicit_prov in (True, False):
        deriv.probes.append(_observed(
            "provenance_scattered",
            bool(explicit_prov),
            "explicit production signal present for provenance-scattered.",
            EpistemicStatus.DEMONSTRATED_FACT,
        ))
    elif rel_findings > 0 or (cross_file >= 2):
        deriv.probes.append(_observed(
            "provenance_scattered",
            True,
            f"{rel_findings} findings and/or {cross_file} cross-location "
            "evidence lines suggest scattered provenance.",
            EpistemicStatus.DERIVED_CONCLUSION,
        ))
    else:
        deriv.probes.append(ProbeResult(
            probe="provenance_scattered", value=PROBE_UNKNOWN,
            basis="no cross-file/finding evidence observed.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="cannot claim provenance scattered/unscattered without evidence.",
        ))

    # --- P4: existing_artifact_self_derived -----------------------------
    # Observable: explicit production signal OR a verification_gap with declared/
    # enforced checks suggesting deterministic auto-derived output. Absent =>
    # UNKNOWN (never FALSE).
    ph = (pr or {}).get("verification_gap") or {}
    enforced = (
        ph.get("enforced_checks") if isinstance(ph, dict) else None
    )
    explicit_self_derived = (
        pr.get("existing_artifact_self_derived")
        if isinstance(pr, dict)
        else None
    )
    if explicit_self_derived in (True, False):
        deriv.probes.append(_observed(
            "existing_artifact_self_derived",
            bool(explicit_self_derived),
            "explicit production signal present for self-derived output.",
            EpistemicStatus.DEMONSTRATED_FACT,
        ))
    elif isinstance(enforced, list) and len(enforced) > 0:
        # Real observing of enforced deterministic checks is a weak positive
        # signal the artifact is auto-verified, but NOT sufficient to claim the
        # artifact itself is auto-derived; be conservative -> UNKNOWN.
        deriv.probes.append(ProbeResult(
            probe="existing_artifact_self_derived", value=PROBE_UNKNOWN,
            basis=f"verification_gap.enforced_checks observed ({len(enforced)} "
                  "checks) but cannot assert the brief is auto-derived.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="enforced checks do not prove the artifact is self-derived.",
        ))
    else:
        deriv.probes.append(ProbeResult(
            probe="existing_artifact_self_derived", value=PROBE_UNKNOWN,
            basis="no explicit auto-derived signal observed.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="cannot assert self-derived vs human-produced without an "
                   "explicit production signal.",
        ))

    # --- P5: fresh_comprehension_needed ----------------------------------
    # Observable: explicit production signal the reasoning audience is a fresh/
    # non-expert human requiring orientation. Absent => UNKNOWN (never FALSE).
    fresh_hint = None
    if pr is not None and isinstance(pr, dict):
        fresh_hint = pr.get("fresh_comprehension_needed")
    if fresh_hint in (True, False):
        deriv.probes.append(_observed(
            "fresh_comprehension_needed",
            bool(fresh_hint),
            "explicit production signal present for comprehension need.",
            EpistemicStatus.DEMONSTRATED_FACT,
        ))
    else:
        deriv.probes.append(ProbeResult(
            probe="fresh_comprehension_needed", value=PROBE_UNKNOWN,
            basis="no explicit comprehension-signal in production evidence.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="cannot assert fresh-comprehension need without a signal.",
        ))

    # --- P6: minimum_subset_suffices ------------------------------------
    # Ruling 2 (directive #23): a producer-asserted insufficient_bounded that is
    # contract-valid (rationale + bounded needed_representation) affirms that a
    # BOUNDED additional representation resolves the gap -> minimum_subset_suffices
    # = TRUE. Otherwise UNKNOWN (never inferred from absence or convenience).
    subset_hint = None
    if pr is not None and isinstance(pr, dict):
        subset_hint = pr.get("minimum_subset_suffices")
    if subset_hint in (True, False):
        deriv.probes.append(_observed(
            "minimum_subset_suffices",
            bool(subset_hint),
            "explicit minimum-subset signal present.",
            EpistemicStatus.DEMONSTRATED_FACT,
        ))
    elif rs_status == "insufficient_bounded" and ib_valid:
        deriv.probes.append(_observed(
            "minimum_subset_suffices",
            True,
            "producer-asserted insufficient_bounded with a non-empty bounded "
            "needed_representation (a bounded subset resolves the reasoning gap).",
            EpistemicStatus.DERIVED_CONCLUSION,
        ))
    else:
        deriv.probes.append(ProbeResult(
            probe="minimum_subset_suffices", value=PROBE_UNKNOWN,
            basis="no explicit minimum-subset signal and no valid bounded "
                  "insufficient_bounded assessment.",
            epistemic_status=EpistemicStatus.INTERPRETATION,
            reason="cannot assert a strict subset suffices without evidence.",
        ))

    # --- Load-bearing UNKNOWN collection ---------------------------------
    # Any probe that is UNKNOWN and would change the warrant is load-bearing.
    # In this slice we conservatively treat every UNKNOWN as load-bearing unless
    # a later probe rules it out; the caller decides warrant from unresolved ones.
    for p in deriv.probes:
        if p.value == PROBE_UNKNOWN and p.probe in probes:
            deriv.load_bearing_unknown.append(p.probe)

    return deriv


def probes_to_warrant(deriv: EvidenceDerivation) -> Warrant:
    """Resolve a MODEL_WARRANT under the ruled authority (directive #25).

    representation_sufficiency is the PRIMARY task-relative MODEL_WARRANT
    authority; the deterministic judge validates/maps it directly:
      sufficient                  -> NO
      insufficient_bounded valid  -> PARTIAL
      inconclusive/missing/malformed -> INCONCLUSIVE (fail closed)
    Mechanical/diagnostic probes are reported (telemetry) but do NOT veto this
    verdict -- an UNKNOWN or TRUE diagnostic signal cannot force INCONCLUSIVE or
    PARTIAL on its own. Absence never becomes FALSE. FULL is deferred/never
    inferred. One canonical judge.
    """
    assert deriv.representation_warrant is not None, \
        "derive_probes must set the authoritative representation_warrant."
    return deriv.representation_warrant


__all__ = [
    "EvidenceInput", "EvidenceDerivation", "ProbeResult",
    "PROBE_TRUE", "PROBE_FALSE", "PROBE_UNKNOWN",
    "derive_probes", "probes_to_warrant",
]
