# 10 — PHASE 1 STOP CHECK (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Qualitative inventory of V0 before evaluation. **Counts are descriptive, not a
quality score** (authorization Section 15).

## Coverage counts

| Dimension | Count | Notes |
|---|---|---|
| Components represented | **34** | 17 skills, 6 runtime/execution-infra, 3 probe-infra, 6 validators, 6 registries, 3 research-infra, 7 canonical/research docs (some components span kinds) |
| Relationship edges (total) | **105** | see family breakdown |
| — STRUCTURAL | 12 | CONTAINS / DEPENDS_ON / CALLS / INVOKES |
| — ARTIFACT | 21 | PRODUCES / CONSUMES / TRANSFORMS / SERIALIZES / READS_FROM / WRITES_TO |
| — VALIDATION | 14 | VALIDATES / VERIFIES / QUALIFIES / REJECTS |
| — AUTHORITY | 23 | GOVERNS / DEFINES_CONTRACT_FOR / ENFORCES_CONTRACT_FOR / AUTHORIZES / OWNS / DERIVES_FROM |
| — PRODUCT | 9 | IMPLEMENTS / SUPPORTS_CAPABILITY / ROUTES_TO |
| — LIFECYCLE | 12 | SUPERSEDES / REPLACES / DEPRECATES / HISTORICAL_ONLY |
| — RESEARCH | 14 | TESTS_HYPOTHESIS / PROVIDES_EVIDENCE_FOR / LIMITS_CLAIM / DOES_NOT_ESTABLISH / MOTIVATES_FOLLOWUP |
| Artifact flows fully traced (P/C/V/X/G) | **12** core + ~14 PM/UI (spine-only) | user_intent, probe_report, brief, plan, work_claim, reconciliation_report, docs_contract_reconciliation_report, repair_verification_report, prompt_handoff, session_summary, + amendment, + PM/UI sub-pipeline |
| Authority relationships (rows in `05`) | **11 named seams** + concentration ranking (5) + multiply-governed list (5) |
| Validation relationships (rows in `06`) | 23 contract→enforcer rows, 7 no/weak-enforcement rows, 4 multiple-authority rows, 2 registry-duplication rows |
| Research claims represented | **9** (RC-1..RC-9) each with question / evidence class / result / exact claim / ceiling / relevance / continuation / supersession |
| Unresolved / hypothetical relationships | edges graded HYPOTHESIS: 0; graded INTERPRETIVE: 6; open-work items (`08`): 8 |
| Epistemic grades assigned | every edge in `03` + every row in `05`/`06`/`07` carries DEMONSTRATED / DERIVED / INTERPRETIVE |
| — DEMONSTRATED | ~86 of 105 edges (~82%) |
| — DERIVED | ~13 |
| — INTERPRETIVE | 6 |
| — HYPOTHESIS | 0 |

## Construction friction (from `OBSERVATIONS.md` C-1..C-9)

| Area | Friction | Cause |
|---|---|---|
| Top-level flow / components / artifact flow | **low** | already in `CONTEXT.md` + `AGW` as prose; work was assembly not discovery |
| Authority map POLICY-vs-IMPL column | **medium** | required a judgment per seam; no single source |
| Validation map | **medium** | required diffing registry copies + reading the deprecated-file header |
| Component granularity | **high** | no repository-given unit; used "semantic responsibility" (INTERPRETIVE) |
| Path-resolution + warrant-seam semantics | **high** | only legible by reading runtime code across multiple call sites |
| Epistemic grading | **negligible** | cheap, disciplining |
| Infrastructure | **none** | plain MD/YAML sufficed |

Approx cost: ~18 targeted reads/greps, ~11 authored artifacts, no rework.

## Obvious redundancy

- `01-SYSTEM-OVERVIEW.md` flow diagram partially duplicates `AGW` section 1 (kept
  because it carries the *corrections* table).
- `04-ARTIFACT-FLOWS.md` P/C rows restate `artifact-contracts.yaml`
  `produced_by` / `consumed_by` verbatim for ~14 PM/UI artifacts that add no
  architectural insight — flagged as compressible.
- Enumerating all 21 validators individually would be pure size; `02` collapses
  them. Correct call, kept.
- `02` `does_not_own` fields for low-salience skills (problem-framer,
  unknowns-mapper, to-prd, to-issues) are near-trivial ("not X, which is
  another skill's job") — low value, retained only for uniformity.

## Representation areas that were unexpectedly difficult

1. **The opt-in nature of the MODEL_WARRANT seam.** Naive rich representation
   would draw it as a pipeline stage and mislead (code I risk). Establishing
   `warrant_enabled` / after-validator-PASS / routing-block-on-INCONCLUSIVE
   needed code reading, not doc reading.
2. **"Who is canonical" for duplicated registries.** `CONTEXT.md:299` names one
   copy; the other's status is inferred from a `defaults/` path and a deprecated
   header. Grade DERIVED, not DEMONSTRATED.
3. **Distinguishing "deferred by design" from "open defect."** OW-6 (routing)
   and OW-3 (`unevaluable`) are both "unresolved" but one is a deliberate
   deferral and one is a contract gap. The representation needs the lifecycle
   vocabulary to keep them apart; a dependency graph would flatten them.

## Stop-check conclusion

V0 has **semantic breadth** (34 components, 105 typed edges across 7 families,
9 research claims, 11 authority seams) without file-level enumeration bloat.
Richness is concentrated where the authorization predicted value (authority,
validation, research provenance, lifecycle) and thin where it predicted
low value (per-file structural detail). Ready to freeze.
