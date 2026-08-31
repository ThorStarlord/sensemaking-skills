# COMPRESSION EVALUATION — SEMANTIC CONTROL CORE V1

Frozen V1 (`V1-FREEZE-MANIFEST.md`, 3 files / 299 lines) replayed against the
frozen V0 value cases (`f7b0d34`, 16 files / 2804 lines). **V1 not altered after
freeze to improve any result** (authorization §19).

Result vocabulary: `PRESERVED_DIRECT` · `PRESERVED_VIA_ON_DEMAND_PROJECTION` ·
`DEGRADED_BUT_ACCEPTABLE` · `LOST` · `MISLEADING`.

---

## 1. Size comparison (authorization §22)

| Measure | V0 | V1 (frozen core) |
|---|---|---|
| Artifact count | 16 | 3 |
| Approx lines | 2804 | 299 |
| Total prototype lines (incl. evaluation) | 2804 | ~299 core + `COMPRESSION-EVALUATION.md` + `SYNTHESIS.md` (~ +400) |
| V0 relationship families in the persistent core | 7 (STRUCTURAL, ARTIFACT, VALIDATION, AUTHORITY, PRODUCT, LIFECYCLE, RESEARCH) | 3 (**AUTHORITY**, **LIFECYCLE**, **VALIDATION/enforcement-gap**) + 1 narrow **RESEARCH→product edge** |
| Families moved to on-demand projection | — | ARTIFACT (producer/consumer/fan-in), cross-cutting impact (was V0's hardest capability) |
| Families discarded outright | — | STRUCTURAL (CALLS/DEPENDS_ON/CONTAINS), PRODUCT capability enumeration, full RESEARCH-claim map |
| Core rows retained | n/a | **22** load-bearing rows: 7 authority-seam + 6 lifecycle-ledger + 8 enforcement-gap + 1 research→product |

Descriptive compression: **the persistent core is ~11% of V0's line count and
~19% of its files.** No percentage target was set; this is what preserving the
value required.

## 2. Staleness classification of retained core rows (authorization §25)

| Change-rate | Count | Rows |
|---|---|---|
| SLOW (`S`) | 13 | A1, A3, A4, A5; ledger: ADR 0018, ADRs 0017/19/20/21, ADRs 0006/07/08/22, deprecated contracts file, `orchestration-runner` name, ADR-status enforcement; G1, G2, G3, G6, G7 |
| MEDIUM (`M`) | 7 | A2, A6, A7; ledger: `reasoning/` research-only; G4, G5, G8; research→product row |
| FAST (`F`) | 0 | — (deliberate: no current SHAs / counts / file inventory; only the V1-snapshot SHA as provenance) |

**Compression preferentially preserved slow-changing semantic facts.** Every
`F`-rate fact V0 carried (ADR counts, current file inventory, evidence-class
rung tallies, embedded SHAs) was dropped. The 7 `M`-rate rows are the
policy/impl-lag items (A5, G5, G6) and the warrant seam (A2, A6, A7, research
row) — these move on *decision* cadence, not commit cadence, so they are
plausibly maintainable.

## 3. V0 regression replay — the 10 mandated cases (authorization §20)

### Case 1 — PR #243 runtime/validator ownership distinction
- `V0_RESULT` = DERIVABLE_WITH_SMALL_REASONING
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = A2 (RUNTIME-OWNS *path* vs ENFORCES *validators*, split), A3 (runtime owns resolution), G4 (brief multiply-enforced)
- `PROJECTION_REQUIRED` = false (for the boundary); the general rule "a runtime gating a validator-bound forward on `os.path.exists` crosses the RUNTIME-OWNS/ENFORCES line" composes from A2 alone
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = yes, for the symbol `_episode_probe_report_path`, the guard, and the `PROBE_REPORT_NOT_FOUND` taxonomy — identical to V0's residual
- `WHAT_V1_REMOVED` = the `04-ARTIFACT-FLOWS.md` probe_report P/C/V row and the prose walk-through; the split is now one table cell

### Case 2 — Artifact-path ownership (ADR 0010 class)
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = A3 (sole resolver named; "executors must not recompute `artifacts/<id>.md`"; ENFORCES = path-containment tests + PreToolUse gate)
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = only which executor / which historical PR
- `WHAT_V1_REMOVED` = the component `does_not_own` list for all 17 skills; A3 keeps the one that matters

### Case 3 — Automatic routing policy-vs-implementation divergence
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = A4 (Status = SUPERSEDED/capability present; Policy-vs-impl = "impl ahead of policy — largest divergence"), G1
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = none for the boundary
- `WHAT_V1_REMOVED` = the concentration-ranking table and the `09` Q5 prose; the ranking claim ("largest divergence") is retained inline in A4

### Case 4 — `auto_invoke_next_workflow` authority semantics
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = A5 (ADR 0026 ruling; fail-closed guard; 2 mirrors + 2 consumers; Issue #230 open), G6
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = PR #235 merge SHA, exact consumer call sites
- `WHAT_V1_REMOVED` = `03` lifecycle `DEPRECATES` edge + `08` OW-1 as separate items; folded into A5 + G6

### Case 5 — superseded ADR / still-present implementation distinction
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = §2 lifecycle ledger (ADR 0018 row: "SUPERSEDED, never Accepted / still present as working `auto_invoke` chains / do not read as 'routing ratified'"); ADRs 0017/19/20/21 row
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = full ADR 0018 disposition text only if the reasoning is needed
- `WHAT_V1_REMOVED` = per-ADR status enumeration for all 27 ADRs; ledger keeps only the ones where presence ≠ authority

### Case 6 — deprecated artifact-contract file remaining load-bearing
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = §2 ledger (`workflow-orchestrator/references/artifact-contracts.yaml`: DEPRECATED, "No code should read this" + sole home of 4 contracts, xfail tests) + G3
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = the exact stranded field list per artifact
- `WHAT_V1_REMOVED` = `06` §2/§4 tables + `05` multiply-governed list; two cells now carry it

### Case 7 — registry duplication / drift
- `V0_RESULT` = DIRECTLY_VISIBLE
- `V1_RESULT` = **PRESERVED_DIRECT** (existence of drift) / **PRESERVED_VIA_ON_DEMAND_PROJECTION** (its blast radius — see §5 drill)
- `CORE_ELEMENTS_USED` = G5 (`MIRROR_DRIFT` + `DUPLICATED_AUTHORITY`; canonical copy named; `src/` copy's specific missing content; "no parity check"), A5
- `PROJECTION_REQUIRED` = false to know drift exists; true to know it only bites the external-target fallback path
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = registry-consumer resolution (done in §5)
- `WHAT_V1_REMOVED` = the `diff` output was quoted in V0 `06`; V1 references it by description

### Case 8 — research → product crossing identification
- `V0_RESULT` = DIRECTLY_VISIBLE (V0 `09` Q4)
- `V1_RESULT` = **PRESERVED_DIRECT**
- `CORE_ELEMENTS_USED` = §4 (the single crossing: C6R → `warrant_gate.run_seam_warrant`; guard = `warrant_enabled` default False; ceiling stated) + the explicit "no other thread wires in" line
- `PROJECTION_REQUIRED` = false
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = `warrant_enabled` default confirmed during construction (constructor kwarg `= False`)
- `WHAT_V1_REMOVED` = the entire 9-row research-claim map (`07`); only the one load-bearing edge kept

### Case 9 — `representation_sufficiency` cross-cutting blast-radius analysis
- `V0_RESULT` = DERIVED / assembled-on-the-page (V0 `09` Q6 — V0's single hardest-to-recover capability)
- `V1_RESULT` = **PRESERVED_VIA_ON_DEMAND_PROJECTION**
- `CORE_ELEMENTS_USED` = A2, A6, §4 row as **seeds**
- `PROJECTION_REQUIRED` = **true** — recipe steps A→E: seeds → inspect `artifact-contracts.yaml` brief entry + `validate-brief.py` + `reasoning/warrant_gate.py` + `vertical_slice.py` + `workflow-runtime.py` INCONCLUSIVE gate + `_WORKFLOW_ID_FIELDS` → affected set ≈ {ADR 0015 addendum, contract declaration, `validate-brief.py`, runtime warrant seam + INCONCLUSIVE gate, `reasoning/` mapping module}
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = yes — 3 files (`validate-brief.py`, `warrant_gate.py`, `vertical_slice.py`); the recipe *scopes* the search to those
- `WHAT_V1_REMOVED` = V0 never stored this as a graph either; V1 makes the on-demand nature explicit and gives the seed set + source list. Net: **equivalent capability, smaller standing cost.**

### Case 10 — V0's known floor: rule/symbol-level questions require raw inspection
- `V0_RESULT` = NOT_REPRESENTED (at rule level — V0 RC#3, the `Lx`-validator-rule-with-no-consumer episode)
- `V1_RESULT` = **PRESERVED_DIRECT** — and arguably *improved*: V1 `SEMANTIC-CONTROL-CORE.md` §5 and recipe step F **state the floor explicitly** ("rule/symbol/test-level detail is intentionally not here"; "core has no row → raw-inspection question")
- `CORE_ELEMENTS_USED` = the governing principle is implied by G2/G4 (validators must trace to consumers); the *specific* rule is still absent, as intended
- `PROJECTION_REQUIRED` = n/a — this class is defined as raw-inspection
- `RAW_REPOSITORY_INSPECTION_REQUIRED` = yes, by design
- `WHAT_V1_REMOVED` = nothing V0 had; V1 documents the boundary V0 left implicit

## 4. Regression summary

| Result | Count | Cases |
|---|---|---|
| PRESERVED_DIRECT | 8 | 1, 2, 3, 4, 5, 6, 8, 10 |
| PRESERVED_VIA_ON_DEMAND_PROJECTION | 1 | 9 (partial on 7) |
| DEGRADED_BUT_ACCEPTABLE | 0 | — |
| LOST | 0 | — |
| MISLEADING | 0 | — |

`V0_VALUE_PRESERVED_DIRECTLY` = the authority-seam distinctions (DEFINES /
ENFORCES / RUNTIME-OWNS / WINS-ON-CONFLICT / POLICY-vs-IMPL), lifecycle /
"present ≠ authoritative", enforcement-gap categories, the single research→product
edge, and the explicit statement of the raw-inspection floor.

`V0_VALUE_PRESERVED_BY_PROJECTION` = cross-cutting blast-radius analysis (case 9);
consumer-level impact of mirror drift (case 7 / §5 drill). Both were
question-specific in V0 too.

`V0_VALUE_LOST` = **none of the 10 mandated value cases.** Genuinely dropped
content — full component register, STRUCTURAL graph, PM/UI artifact-flow rows,
the research-claim encyclopedia, per-experiment ceilings, restated operating-flow
prose — was not used in any V0 retrospective or prospective reasoning case, so
its removal is compression, not loss.

`COMPRESSION_CREATED_MISLEADING_CASES` = none among the 10. **One residual
risk** (not a case failure): a reader who consults only the core and does **not**
invoke the recipe could over-read a *silent omission* (e.g. no plan-lifecycle
row) as "nothing to know here." Mitigation is in `SEMANTIC-CONTROL-CORE.md` §5
and recipe step A ("core has no row → raw-inspection question"), but it depends
on the reader reaching that instruction. Carried to `SYNTHESIS.md` Q5.

---

## 5. Current-state projection drill (authorization §24)

**Question (not encoded as a V1 row to answer it):** "G5 says the two
`workflow-registry.yaml` copies drifted. Which consumers read which copy, and
does the drift change runtime behavior on this repo today?"

- **Starting core rows:** G5, A5.
- **Missing relationships:** registry-file → consumer resolution.
- **Evidence inspected:** `scripts/_validator_utils.py::_registry_path`
  (hardcodes `skills/workflow-planner/references/`), `scripts/workflow-runtime.py`
  (3 call sites, all `load_workflow_registry`), `src/sensemaking_skills/registry.py::WorkflowRegistry._load_package_defaults` /
  `_load_user_registry`.
- **Temporary relationships materialized:**
  - `workflow-runtime.py` → **canonical copy only** (`skills/workflow-planner/references/`), never the `src/defaults/` copy. Grade DEMONSTRATED.
  - `WorkflowRegistry` (library API) → loads `src/sensemaking_skills/defaults/` as **package defaults**, then merges the target repo's `skills/workflow-planner/references/` copy on top (user overrides defaults by workflow id). Grade DEMONSTRATED.
- **Stopping point:** the responsibility is now stable — the drift's blast
  radius is bounded.
- **Answer:** On `sensemaking-skills` itself the drift is **inert**:
  `workflow-runtime.py` ignores the stale copy, and `WorkflowRegistry` merges
  the fresh canonical copy over the stale defaults. The stale `src/defaults/`
  copy (missing a `prior_evidence` input + a `repair-verifier` step) can only
  affect an **external target repo with no `skills/workflow-planner/references/workflow-registry.yaml`**,
  where `WorkflowRegistry` falls back to defaults only. That is a real but
  narrow exposure — not a current runtime defect here.
- **Deserved promotion into the core?** **NO.** Single question;
  consumer-resolution detail is code-level and MEDIUM/FAST-changing; G5 already
  flags the drift, which is the slow-changing part worth holding.

`CURRENT_PROJECTION_RESULT` = the recipe materially out-performed unstructured
rediscovery: G5 named the exact seed, and 3 targeted file reads bounded the
blast radius. Without the core row, "is this drift a problem?" is an open-ended
grep across `scripts/` + `src/`.

---

## 6. Holdout generalization check (authorization §23)

Two real episodes **not** in V0's challenge set (V0 challenged: PR #243, ADR
0010 path mismatch, `Lx` validator rule, `auto_invoke` #230, ADR 0018
supersession, INFRA-004, Auteur handoff 0020) and **not** used while authoring
V1. Not selected to flatter V1 — both deliberately probe *core omissions*.

### HOLDOUT_CASE_1 — ADR 0025 provisional vs finalized `workflow_orchestration_plan`
- **Episode:** the runtime's `generate_plan()` emits a PROVISIONAL skeleton
  (`plan_stage: provisional`) before the brief exists; only the FINALIZED plan
  (after `finalize_plan(brief_path)`) must satisfy `validate-plan.py` /
  `validate-artifact.py`. An agent seeing a provisional skeleton "fail"
  validation could wrongly call it a bug.
- **Question to V1:** does the thin core identify the right semantic region /
  authority question?
- **Core check:** A2 covers the brief contract + the 2-validator split but has
  **no plan-lifecycle row**; §2 ledger has none. The core does **not** answer
  directly.
- **Recipe:** seed = A2 (validator authority) → recipe source #3
  (`artifact-contracts.yaml` `workflow_orchestration_plan` entry, notes section)
  → ADR 0025. One hop.
- `HOLDOUT_CASE_1_RESULT` = **PROJECTION_SUFFICIENT**. The core's authority
  framing ("which validator, applied when") is the correct seed; the
  two-stage lifecycle fact is one documented hop away. Not misleading — the
  core is silent, and the recipe reaches it.

### HOLDOUT_CASE_2 — canonical-vocabulary drift (ADR 0011)
- **Episode:** a validator rejects a controlled-vocabulary value (e.g. a
  fog-type or status enum) a brief/plan author believes is valid; the authority
  for the enum set is `docs/canonical-vocabulary.yaml` (ADR 0011), enforced by
  controlled-vocab checks embedded across `validate-*.py`.
- **Question to V1:** does the core point at the right authority?
- **Core check:** deliberately **no vocabulary row** (excluded by the §11
  inclusion test — single obvious source, low authority ambiguity). Core does
  not answer directly.
- **Recipe:** seed = "core has no row → raw-inspection / single-source
  question" → recipe source #1 (`CONTEXT.md` source-of-truth map names
  `docs/canonical-vocabulary.yaml`) + source #4 (ADR 0011). One hop.
- `HOLDOUT_CASE_2_RESULT` = **PROJECTION_SUFFICIENT** (borderline
  `CORE_SUFFICIENT` — the recipe's "single obvious source" path resolves it
  almost trivially). This is the *intended* behavior for a fact the inclusion
  test excludes: cheap to recover, so not core-worthy.

**Holdout verdict:** both generalized — the thin core + recipe located the
correct authority region for two episodes outside the V0 set, with no
misleading result. Neither needed `RAW_REPOSITORY_REQUIRED` beyond a single
documented hop. Small sample (n=2), sanity-check only.
