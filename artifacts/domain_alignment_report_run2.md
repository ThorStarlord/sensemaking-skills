# Domain Alignment Report — Run 2

## 1. Repository Analyzed
- **Repository**: `ThorStarlord/sensemaking-skills`
- **Pinned revision**: `060fc363f0e4778f543e2f52cc671af7129db7b9`
- **Purpose**: Controlled post-hardening rerun of `docs-aligner` after Run 1 reconciliation. Preserve `artifacts/domain_alignment_report.md` as Run 1 evidence and test whether authority/currentness triage, negative-evidence discipline, and gate discipline change the classification of the same repository state.
- **Run 1 reference**: `artifacts/domain_alignment_report.md` (produced at `5a77885`)
- **Run 1 reconciliation**: `artifacts/reconciliation_report.md`
- **Hardened Skill**: `skills/docs-aligner/SKILL.md:20-43`
- **Mutation policy for this comparison**: no `CONTEXT.md` or ADR mutation is applied before synthesis; the target revision is held fixed so Run 1 -> Run 2 classification changes remain attributable to the hardened analysis rules rather than a moving target.

## 2. Contradictions

### C1 — `ui-diagnostic-workflow` violates docs-aligner gate discipline
- **Term**: `docs-aligner` gate discipline / `review_alignment_report`
- **Claim**: `skills/docs-aligner/SKILL.md:20-43` requires authority/currentness triage and states that `gate: none` is permitted only when a downstream `review_alignment_report` gate mechanically exists; otherwise autonomous `CONTEXT.md` mutation must be reported as a boundary gap.
- **Reality**: `skills/workflow-planner/references/workflow-registry.yaml:793-826` defines `ui-diagnostic-workflow` Step 1 as `skill: docs-aligner`, `gate: none`; Step 2 uses generic `gate: review`, and the workflow contains no downstream `review_alignment_report`. The packaged registry mirror contains the same `gate: none` entry.
- **Evidence**: `skills/docs-aligner/SKILL.md:20-43`; `skills/workflow-planner/references/workflow-registry.yaml:793-826`; `src/sensemaking_skills/defaults/workflow-registry.yaml` matching `ui-diagnostic-workflow` entry.
- **Authority/currentness classification**: `confirmed_contradiction`
- **Resolution**: Update the canonical workflow definition so the docs-aligner step uses `review_alignment_report` (or otherwise introduces that exact mechanically enforced downstream gate), then synchronize the packaged workflow-registry mirror and add/extend a registry-agreement regression test. Do not weaken the Skill's gate discipline merely to preserve the stale workflow entry.

### Authority/currentness triage exclusions — not counted as contradictions

#### T1 — Run 1 C1 phantom skill-registry path
- **Classification**: `previously_adjudicated` / fixed.
- **Evidence**: `CONTEXT.md:315-323` now points to `skills/workflow-planner/references/skill-registry.yaml`.
- **Disposition**: Excluded from contradiction count.

#### T2 — Run 1 C2 canonical vocabulary dual-copy drift
- **Classification**: resolved on the pinned revision.
- **Evidence**: `docs/canonical-vocabulary.yaml` and `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` both resolve to Git blob `b94cd3d09b433c41903554b12f983e3d77880618`; `tests/test_path_drift.py:323-342` enforces byte-for-byte mirror agreement.
- **Disposition**: Excluded from contradiction count.

#### T3 — Run 1 C3 proposed/deprecated Skill consumers
- **Classification**: `needs_adjudication`.
- **Evidence**: `skills/workflow-planner/references/skill-registry.yaml:80-93` explicitly marks `triage` as `proposed` and `tdd` as `deprecated`; `skills/workflow-planner/references/workflow-registry.yaml:665-940` still presents multiple implementation workflows as executable `local_execution` chains containing those Skills.
- **Reason not counted**: the original contradiction framing against `CONTEXT.md` was wrong because the CONTEXT Skill list is explicitly representative, while the remaining executability/compatibility-liveness question has not yet been ratified as either intentional historical representation or an active workflow defect.
- **Disposition**: Preserve for bounded executability/consumer analysis; do not invent retirement or restoration policy in docs-aligner.

#### T4 — Run 1 C4 `yolo_execution` compatibility/default tension
- **Classification**: `needs_adjudication`.
- **Evidence**: `docs/canonical-vocabulary.yaml:390-421` marks `guided_execution` as default and `yolo_execution` as `compatibility_only`; `src/sensemaking_skills/runner.py:69-82` still defaults `run_workflow(... execution_mode="yolo_execution")`, and `runner.py:326-342` explicitly uses `yolo_execution` for parent-session execution.
- **Reason not counted**: the mismatch is real, but repository authority explicitly preserves it as `UNRESOLVED_COMPATIBILITY_DEFAULT_TENSION` pending bounded consumer analysis. `compatibility_only` is evidence against silently interpreting the legacy default as ratified policy, but it does not itself decide whether changing the API default is safe.
- **Disposition**: Preserve for consumer analysis; no runtime change in this run.

#### T5 — Run 1 C5 `MODEL_WARRANT` alleged non-wiring
- **Classification**: false positive removed by negative-evidence discipline.
- **Evidence**: `scripts/workflow-runtime.py` contains `_run_seam_warrant`; tests exercise the seam; `warrant_enabled: bool = False` makes it opt-in rather than absent.
- **Disposition**: Excluded from contradiction count. Correct statement: the warrant seam exists and is guarded/opt-in.

#### T6 — Run 1 C6 provisional orchestration-plan contract
- **Classification**: `previously_adjudicated`.
- **Evidence**: ADR 0025 (`docs/adr/0025-workflow-orchestration-plan-lifecycle.md:86-113`) explicitly ratifies a provisional skeleton distinct from the finalized canonical plan; `skills/workflow-planner/references/artifact-contracts.yaml:484-514` explicitly states that the provisional state may omit diagnosis-dependent fields and only the finalized plan must satisfy validators.
- **Disposition**: Excluded from contradiction count.

## 3. Fuzzy Language

No new decision-changing fuzzy-language cluster was confirmed in the Run 2 comparison.

The Run 1 language clusters are now materially sharpened in `CONTEXT.md:325-350`: qualified `Workflow`, `Warrant`, `MODEL_WARRANT`, `Representation Sufficiency`, `Probe`, `Gate`, `Execution Mode`, `Validation`, `Reconciliation`, and `Repair verification` are explicitly separated.

A generic `capability` vocabulary remains used in several technical contexts (for example Skill capability metadata such as `write_files`), but this run does not have enough evidence that the remaining usage changes a consequential domain interpretation. It is therefore not promoted to a fuzzy-language finding.

## 4. Undocumented Concepts

No globally undocumented domain-significant concept was confirmed.

Run 1's U1-U6 set no longer qualifies as globally undocumented: the concepts are documented in `CONTEXT.md:325-350`, repository Skill/reference documentation, or accepted ADRs. Under the hardened rule, a concept documented elsewhere but absent from a particular glossary would be a `glossary gap`, not an undocumented concept.

## 5. ADR Candidates

None.

- The confirmed gate mismatch is a reversible registry/Skill contract repair governed by an existing Skill boundary rule; it does not establish a new hard-to-reverse architectural decision.
- C3 and C4 remain `needs_adjudication`; creating an ADR before the required consumer/executability analysis would convert uncertainty into premature policy.

## 6. Glossary Mutations

None.

This is a controlled Run 1 -> Run 2 regression comparison on pinned revision `060fc363...`. No `CONTEXT.md` mutation is warranted by the confirmed gate mismatch, and no new glossary definition crossed the evidence threshold.

## 7. ADRs Created

None.

## 8. Summary
- Contradictions found: **1**
- Fuzzy terms sharpened: **0**
- Undocumented concepts discovered: **0**
- ADRs created: **0**
- Glossary entries added: **0**
- Glossary entries updated: **0**

### Run 1 -> Run 2 comparison

| Run 1 candidate | Run 1 treatment | Run 2 authority-aware disposition |
| --- | --- | --- |
| C1 phantom skill-registry path | contradiction | fixed / excluded |
| C2 canonical vocabulary mirror drift | contradiction | fixed / excluded |
| C3 proposed/deprecated Skill consumers | contradiction | `needs_adjudication` as executability/compatibility-liveness |
| C4 `yolo_execution` compatibility/default | contradiction | `needs_adjudication`; unresolved consumer-policy tension |
| C5 `MODEL_WARRANT` non-wiring | contradiction | false positive; seam exists, opt-in |
| C6 provisional orchestration-plan fields | contradiction | `previously_adjudicated` by ADR 0025 |
| New: `ui-diagnostic-workflow` docs-aligner `gate: none` | omitted | **confirmed contradiction** |

### Regression disposition

`DOCS_ALIGNER_AUTHORITY_HARDENING = BEHAVIORALLY_USEFUL_WITH_ONE_NEW_VALID_FINDING`

The hardened rules materially improved classification quality: they removed the C5 incomplete-search false positive, respected the C6 accepted lifecycle decision, stopped treating C3/C4 uncertainty as already-resolved contradictions, and surfaced a concrete gate-discipline violation that Run 1 missed.

The next warranted responsibility is a **bounded mechanical repair of the `ui-diagnostic-workflow` docs-aligner gate contract**, followed by finding-specific verification. C3/C4 should remain separate and must not be bundled into that repair.
