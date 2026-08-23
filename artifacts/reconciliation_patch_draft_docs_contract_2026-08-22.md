# Reconciliation Patch Draft — rev 3 (APPLIED)

**Status:** APPLIED (owner approved rev 3, 2026-08-22). Mutations P1–P12 were
applied and the post-approval verification sequence ran. Repair verdict:
PARTIAL CLOSURE (see `artifacts/repair_verification_report.md`). This document
retains the approved diff as the record of what was applied.

---

## 0. Owner revision decision rev 3 (incorporated verbatim)

1. Pin the moved `integration_fog` negative fixture to
   `expected_error_contains: repository_sensemaking_brief.primary_fog_type.unknown_value`.
2. Remove the proposed mutation to `skills/workflow-planner/SKILL.md` from this reconciliation patch. Those lines contain actual routing/Skill semantics, and `sensemaking-docs-reconciler` explicitly forbids modifying skill logic or workflow execution behavior.
3. Record that contradiction as a separate follow-up finding requiring an independently authorized Skill-maintenance/semantic-repair responsibility.
4. Keep all other rev-2 decisions unchanged.
5. Update the parent plan to reflect the reduced mutation scope and re-run `validate-plan.py`.
6. Stop again at `review_reconciliation_patch`. Do not apply the patch or run `repair-verifier` yet.

**Post-application closure rule (owner):** if `repair-verifier` finds that the stale `workflow-planner` SKILL semantics prevent full closure, report **partial closure + the F4 follow-up** instead of weakening the closure criterion. A partial repair reported truthfully is stronger than a full closure manufactured by scope creep.

**Principles (owner):**
- It is not enough to identify the right repair; it is necessary to have **authority** to perform that repair.
- Documentation cleanup and Skill maintenance are **two bounded responsibilities that remain separate**.

---

## 1. Verified producer/consumer map (probe results, 2026-08-22)

| Consumer | Source it reads | Current behavior |
|---|---|---|
| `src/sensemaking_skills/validation.py:18-55` `CanonicalVocabulary` | packaged default `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` | loads defaults; `primary_fog_type`/`secondary_fog_types` enums include `integration_fog` |
| `scripts/validate-brief.py:193,196-201` | repo `docs/canonical-vocabulary.yaml` (`_load_allowed_fog_types`) | allowed fog types = vocab ids (5 today); `_DEFAULT_FOG_TYPES` fallback is already 4 |
| `scripts/validate-brief.py:543` | error emission | emits `repository_sensemaking_brief.primary_fog_type.unknown_value` for out-of-set values (verified) |
| `scripts/_validator_utils.py:119-129` | repo `docs/canonical-vocabulary.yaml` | shared vocab loader for validators |
| `scripts/validate-fog-type-normalization.py:70` | repo `docs/canonical-vocabulary.yaml` | normalization against vocab |
| `tests/test_validation.py:33-40` | packaged default via `CanonicalVocabulary` | asserts `"integration_fog" in fog_values` (line 40) |
| `tests/test_path_drift.py:143` | docstring only | lists `integration_fog` among "canonical forms" (comment, not assertion) |
| `scripts/test-validators.py` (positive/negative fixture harness) | `tests/fixtures/validate-brief/valid/integration-fog-brief.md` | expects positive PASS for a brief with `primary_fog_type: integration_fog` (fixture line 57); negative convention: front matter `validator_case: negative` + quoted `expected_error_contains` (e.g. `tests/fixtures/validate-brief/invalid/evidence-quote-not-found.md`) |
| `scripts/workflow-runtime.py` + validators + executor | `yolo_execution` mode string (10+ script refs incl. `workflow-runtime.py:87,102,553,592,1049,1085,1925,2195,2686`) | consumes `yolo_execution` as a mode |
| `scripts/validate-repo.py` | `skills/workflow-planner/references/skill-registry.yaml` ids vs contracts/workflows | cross-references registered ids |
| `skills/workflow-planner/SKILL.md:88-99` | its own routing-logic section | teaches `integration_fog` as a canonical fog type and auto-invoke routing semantics — **NOT edited by this patch** (see F4) |
| `skills/sensemaking-docs-reconciler/SKILL.md:22` | its own boundary | "must not modify skill logic, implementation code, or workflow execution behavior" |

**Verified:** `src/` and `scripts/` contain **zero** `integration_fog` references outside the packaged defaults file. The behavioral consumers are `tests/test_validation.py:40` (packaged default) and the positive fixture consumed by `scripts/test-validators.py` (docs copy via `validate-brief.py`). `tests/test_path_drift.py:143` is comment-only.

---

## 2. Part A — Remove `integration_fog` from the active canonical enum (owner decision, unchanged from rev 2)

### P1. `docs/canonical-vocabulary.yaml`
Remove the `integration_fog` entry from:
- `fog_types` (lines 46–53)
- `fog_type_decision_tree` step 5 (lines 72–74)
- `routing_fields.primary_fog_type.values` (line 79)
- `routing_fields.secondary_fog_types.values` (line 86)

### P2. `src/sensemaking_skills/defaults/canonical-vocabulary.yaml`
Same four removals (lines 46, 74, 79, 86). This is the file `CanonicalVocabulary` actually loads (`validation.py:42-55`).

### P3. `tests/test_validation.py:40`
Delete `assert "integration_fog" in fog_values`. The test's expectation changes from five to four canonical fog types. The test expresses the authoritative contract; it does not define it.

### P4. `tests/test_path_drift.py:143`
Update the docstring's canonical-forms list to the four ratified types. Comment-only correction.

### P5. `tests/fixtures/validate-brief/valid/integration-fog-brief.md`
**Move** to `tests/fixtures/validate-brief/invalid/integration-fog-brief.md` with pinned front matter:

```yaml
---
validator_case: negative
expected_error_contains: repository_sensemaking_brief.primary_fog_type.unknown_value
---
```

The error ID is stable and verified in `scripts/validate-brief.py:543`. The fixture becomes proof that the fifth type is **rejected** — a negative contract test. Consumer: `scripts/test-validators.py` (defaults `positive` for `/valid/`, `negative` for `/invalid/`).

### Backward-compatibility analysis (owner decision rev-2 #4)
`rg integration_fog` across the tree (excluding `.git`, worktrees, `build/`, `dist/`) returns: the two target vocabulary files, the two tests, the fixture, `skills/workflow-planner/SKILL.md` (now F4, not edited), the plan/draft artifacts in this work, and four historical/research records (`docs/HARDENING_STATUS.md`, `docs/research/warrant-prospective-dogfood.md`, `docs/research/uncertainty-selection-pr164-falsification.md`, `docs/candidate/architecture-decision.md`). None is a validated durable artifact whose `primary_fog_type` is `integration_fog`. **No legacy normalization/migration mechanism is required now**; if ever needed, add it outside the active canonical enum (follow-up F2).

### Part A consumer consequences (exact)
| Edit | Breaks if skipped | Breaks under this patch | Action |
|---|---|---|---|
| P1 (docs vocab) | validate-brief keeps accepting 5th type | none — `_DEFAULT_FOG_TYPES` is already 4 | apply |
| P2 (packaged default) | `CanonicalVocabulary` keeps 5th type; contract mismatch persists | `test_validation.py:40` fails | P3 in same change |
| P3 (test assert) | test contradicts ratified enum | none | apply with P2 |
| P4 (docstring) | stale comment | none | apply |
| P5 (fixture move) | `test-validators.py` reports positive-PASS regression | none (negative case, pinned error) | apply with P1 |
| ~~P6 (workflow-planner SKILL.md)~~ | — | — | **REMOVED — out of reconciler authority; see F4** |

---

## 3. Part B — `yolo_execution`: retain, mark compatibility (owner decision rev-2 #5, unchanged)

**Do NOT delete.** Runtime/executor/validator code still consumes `yolo_execution` as a mode. Deleting it during a docs reconciliation would change executable compatibility behavior.

- **P6.** `docs/canonical-vocabulary.yaml` `execution_modes` (`yolo_execution`, lines 422–426): add annotation `compatibility_only: true` / "legacy — not ratified product behavior; retained for mechanical compatibility" (per `CONTEXT.md:241` and the decision/orchestration boundary guardrail: supported mechanically ≠ ratified product behavior).
- **P7.** `skills/workflow-planner/references/execution-modes.md`: change the `yolo_execution` row status from `Stable` (line 11) to `Compatibility/legacy` and add the same "not ratified product behavior" note (lines 31–41).

No executable change; annotation only. (`execution-modes.md` is a reference/registry document, within the reconciler's registry/contract/documentation boundary; it is not Skill logic.)

---

## 4. Part C — Skill-registry classification (owner decision rev-2 #6, unchanged)

**P8.** `skills/workflow-planner/references/skill-registry.yaml` — the registry is a catalog/contract file, within the reconciler's authority (unlike `SKILL.md` bodies). Currently 44 registered ids; 30 have no implementation under `skills/`. Do **not** hard-delete (validate-repo cross-references and registered workflows reference these ids). Annotate status per id:

- **IMPLEMENTED + CURRENT (registered):** problem-framer, unknowns-mapper, repo-sensemaker, workflow-planner, architectural-review, sensemaking-docs-reconciler, output-reconciler, repair-verifier, handoff, skill-maintainer, usage-researcher, docs-aligner, to-prd, to-issues. No change.
- **IMPLEMENTED + CURRENT (NOT registered — registry gap, follow-up F3):** coding-agent-native-campaign, setup-sensemaking-skills, using-sensemaking, vnext-review-consumer. Recorded; not added in this patch.
- **UNIMPLEMENTED + STILL-PROPOSED** (referenced as consumers/producers in current docs): `prompt-handoff` (`docs/agent-native-operating-workflow.md:332-334,340`) and `triage` (`:331,339`). Annotate `status: proposed` / `implemented: false`.
- **UNIMPLEMENTED + HISTORICAL/DEPRECATED** (no current-doc reference; wayfinder-era pipeline/PM/GTM/UI): tdd, ui-brief, ui-flow, ui-screen-spec, persona, discovery, interview-synthesis, competitive-analysis, opportunity-tree, hypothesis, customer-journey, prd, user-stories, acceptance-criteria, prioritize, roadmap, okr, lean-canvas, pricing, north-star, experiment-design, measure-pmf, ab-test-analysis, pre-mortem, launch-checklist, release-notes, stakeholder-update, gtm, battlecard (28 ids). Annotate `status: deprecated` / `implemented: false`, do not remove.

---

## 5. Part D — Current-facing claim fixes (onboarding/source-of-truth paths, unchanged)

- **P9.** `docs/CUSTOMER_ONBOARDING.md` — add a HISTORICAL banner at the top: describes the retired runner-based orchestration product; automatic routing/autonomous/yolo execution is not current ratified product behavior; point to `README.md` / `GETTING_STARTED.md` and ADR 0013/0014. Banner, not rewrite.
- **P10.** `docs/FAQ.md:108-109` — replace "Is this production-ready? Yes!" with the owner-ratified readiness statement (current level "externally exercised"; target "externally validated" per D8; `docs/OWNER-DECISION-PACKAGE-2026-07-26.md:195`).
- **P11.** `GETTING_STARTED.md:176-177,295,335` — remove the `triage`/`tdd` ghost-skill references; re-scope to implemented skills.
- **P12.** `README.md` — line 10 readiness language; lines 337-354 stale "Roadmap to User-Ready" checkboxes → remove or replace with pointer to `roadmap.md`/`STATUS.md`.

---

## 6. Part E — Deferred historical-document sweep (unchanged, recorded as follow-up candidates)

`docs/ROUTING_GUIDE.md`, `docs/PORTFOLIO_OPERATIONS.md`, `docs/run-ledger-guide.md`, `docs/UI-ROUTING-IMPROVEMENTS.md`, `docs/ui-routing-test-plan.md`, `docs/UI-ROUTING-TESTING-RESULTS.md`, `docs/HARDENING_STATUS.md`, `docs/candidate/architecture-decision.md`, `docs/research/warrant-prospective-dogfood.md`, `docs/research/uncertainty-selection-pr164-falsification.md`, and the `docs/PHASE-*` / `docs/phase-*` records. Historical evidence; no deletion or rewriting. Optional `HISTORICAL IMPLEMENTATION RECORD` banner only where a file is discoverable enough to be mistaken for current guidance (candidate: `docs/ROUTING_GUIDE.md`, linked from `CUSTOMER_ONBOARDING.md`); decide after P9 lands.

---

## 7. Follow-up findings (recorded, not solved in this patch)

- **F1 — Packaged-default mirror drift.** Canonical vocabulary exists in two places: `docs/canonical-vocabulary.yaml` (validators) and `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` (package API). `docs/enforcement-stabilization.md:58` already flags this mirror. Future invariant: `canonical docs vocabulary → package-default mirror → validator behavior must not silently diverge` (generation, checksum/drift test, or single-source elimination are later design options). Do not solve in this patch.
- **F2 — Legacy normalization.** If durable artifacts containing `integration_fog` ever need backward compatibility, add a legacy alias/migration path outside the active canonical enum. Not needed today.
- **F3 — Registry completeness.** 4 implemented skills are not registered. Separable repair; not in this patch.
- **F4 — workflow-planner skill semantic drift** (NEW, owner decision rev-3 #2/#3):
  - Canonical product/contract: 4 fog types; routing recommendation ≠ execution authority.
  - Current `skills/workflow-planner/SKILL.md`: 5 fog types (line 93, 97), explicit fog → implementation routing (lines 88-94), auto-invoke language.
  - Disposition: **do not modify under `sensemaking-docs-reconciler`** (its No-Side-Effects rule, `SKILL.md:22`, forbids modifying skill logic / implementation code / workflow execution behavior). Route separately to `skill-maintainer` / an independently owner-authorized skill-repair responsibility.

---

## 8. R/T/H/A matrix (rev 3)

| Target | Tag | Disposition (rev 3) |
|---|---|---|
| `CONTEXT.md` architecture/ownership sections | R | No edits. |
| `docs/decision-orchestration-boundary.md` | R | No edits (read-only). |
| `docs/agent-native-operating-workflow.md` | R | No edits (its `triage`/`prompt-handoff` consumer refs justify STILL-PROPOSED in Part C). |
| `docs/research/control-model-research-agenda.md` | T | No edits — thesis/research preserved. |
| `docs/adr/0013`, `0014`, `0023` | R | No edits. |
| `docs/adr/0017`–`0021` | H | Already SUPERSEDED (2026-08-18); audit for stale citations — deferred follow-up. |
| `docs/canonical-vocabulary.yaml` | A | P1 (remove `integration_fog`), P6 (yolo annotation). |
| `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` | A | P2 (same removals). |
| `tests/test_validation.py` | A | P3. |
| `tests/test_path_drift.py` | A | P4 (docstring). |
| `tests/fixtures/validate-brief/valid/integration-fog-brief.md` | A | P5 (move to `invalid/`, pinned error). |
| `skills/workflow-planner/references/skill-registry.yaml` | A | P8 (classification, deprecate-before-delete; registry/contract boundary). |
| `skills/workflow-planner/references/execution-modes.md` | A | P7 (yolo → compatibility; reference doc). |
| **`skills/workflow-planner/SKILL.md`** | **—** | **NO MUTATION in this workflow — Skill semantics, outside reconciler authority (F4). Route to skill-maintenance / owner-authorized skill repair.** |
| `docs/CUSTOMER_ONBOARDING.md` | A | P9 (HISTORICAL banner; onboarding path → in-patch). |
| `docs/FAQ.md` | A | P10 (readiness language). |
| `GETTING_STARTED.md` | A | P11 (ghost-skill refs). |
| `README.md` | A | P12 (readiness + stale roadmap section). |
| `docs/ROUTING_GUIDE.md`, `PORTFOLIO_OPERATIONS.md`, `run-ledger-guide.md`, `UI-ROUTING-*`, `HARDENING_STATUS.md`, candidate/research records | H (deferred) | Part E — record-only; optional banner where discoverable. |

## 9. Non-goals / no-erase

- No mutation of `CONTEXT.md`, `docs/decision-orchestration-boundary.md`, `docs/agent-native-operating-workflow.md`, ADR 0013/0014/0023, or the research agenda.
- **No mutation of `skills/workflow-planner/SKILL.md`** — Skill semantics are outside `sensemaking-docs-reconciler`'s authority; recorded as F4.
- No re-opening of ADR 0014 scope.
- No deletion of `yolo_execution` machinery; no hard-delete of registered skill ids.
- No solving of the duplicated-vocabulary architecture (F1) in this patch.

## 10. Post-approval verification sequence (NOT run yet)

1. Apply P1–P5, P6–P7, P8, P9–P12 as the exact approved diff.
2. `python scripts/test-validators.py` (fixture harness incl. moved negative fixture with pinned error).
3. `python -m pytest tests/test_validation.py tests/test_path_drift.py` (+ full suite).
4. `python scripts/validate-repo.py` (registry/workflow cross-references).
5. `repair-verifier`: re-probe; verify each original finding no longer reproduces. **Closure rule (owner):** if the untouched `skills/workflow-planner/SKILL.md` semantics prevent full closure of the vocabulary/routing finding, report **partial closure + F4 follow-up** — do not weaken the closure criterion to manufacture a full PASS.

**Awaiting `review_reconciliation_patch` approval of this exact diff. No mutation has been applied.**
