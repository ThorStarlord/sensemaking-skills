# ADR 0025: Two-stage workflow_orchestration_plan lifecycle

**Status**: ACCEPTED — owner decision 2026-08-23 (ratified during #232 triage
review): approve two-stage orchestration-plan finalization as specified in the
Decision section. Merge to `main` is a separate repository action, pending and
not part of this record.

**Date**: 2026-08-23

**Resolves**: Issue #232 (the plan-lifecycle decision uncovered by its triage;
the issue remains open as the tracker for the bounded implementation)

**Depends on**:
- ADR 0010 (Accepted — the runtime owns artifact path resolution and is the
  canonical producer of `workflow_orchestration_plan`; "extends this from paths
  to the plan itself")
- ADR 0013 (Accepted — agent-native orchestration is the primary model;
  `workflow-runtime.py` is a separate automation/compatibility path, not the
  semantic definition of Skill execution)
- ADR 0014 (Accepted — product boundary: automatic downstream routing is
  deferred; a recommendation is not execution authority)
- ADR 0005 (Accepted, historical — "orchestrator chains skills automatically";
  superseded in effect by the ratified recommendation-not-authority boundary in
  CONTEXT.md and docs/decision-orchestration-boundary.md, guardrail 2)

---

## 1. Context and problem statement

`tests/test_generate_plan_conformance.py` fails on current `main` (and on the
pristine PR #228 base `1ffde16`) because the runtime's generated plan is missing
three contract-required machine fields: `primary_fog_type`, `workflow_steps`
(the producer emits the legacy `steps` name), and `created_at`.

Two of the three fields are mechanical reconciliation problems:

- `created_at` — the producer knows the current time; emitting it is trivial.
- `workflow_steps` — the producer already holds the steps; this is a
  representation/schema rename (`steps` -> `workflow_steps`).

`primary_fog_type` is fundamentally different. The runtime authors the plan at
Phase 2 (`scripts/workflow-runtime.py` `run()`, `PHASE 2: GENERATE PLAN`,
line ~2564-2568), BEFORE any workflow step executes. The diagnosed fog type is
produced later, by `repo-sensemaker` (step 4 of `full-local-sensemaking`), in
the `repository_sensemaking_brief`. At plan-generation time:

```text
primary_fog_type = UNKNOWN
```

yet the artifact contract lists `primary_fog_type` as REQUIRED. The plan is
therefore finalized before the evidence required to populate a required field
exists. This is premature finalization, not a missing-field bug.

There is a second, deeper semantic collision. The runtime plan describes the
workflow currently being executed (Model A):

```text
chosen_workflow_id = fast-local-diagnostic
```

while the validator's fog-alignment check (`scripts/validate-plan.py`, semantic
conflict check on `primary_fog_type` vs `chosen_workflow_id`) treats the plan as
a fog-informed routing decision to an implementation workflow (Model B):

```text
primary_fog_type = product_fog
chosen_workflow_id = product-implementation-workflow
```

Blindly copying a fog value into an execution-plan artifact would recreate the
validator contradiction (e.g. `primary_fog_type: product_fog` with
`chosen_workflow_id: fast-local-diagnostic`). The two models are not the same
artifact semantics.

The contract itself already contains the tension: `primary_fog_type` sits in
`required_machine_fields`, while an attached note in
`skills/workflow-planner/references/artifact-contracts.yaml` says "If absent,
the runtime falls back to the repository_sensemaking_brief", and the runtime
consumer (`OrchestrationRunner._resolve_fog_type`) implements exactly that
fallback. Absence-with-fallback is already the runtime's operating model; the
REQUIRED status is not reconciled with it.

## 2. Decision

Two-stage orchestration-plan lifecycle (ratified verbatim from the owner
decision):

> **Two-stage orchestration-plan lifecycle is approved.**
>
> During Phase 2, the runtime may construct a **provisional execution skeleton**
> containing information already known about the workflow currently being
> executed. This provisional state is **not yet the canonical, contract-valid
> `workflow_orchestration_plan`** and must not fabricate diagnosis-dependent
> fields.
>
> After `repo-sensemaker` produces a valid `repository_sensemaking_brief`, the
> orchestration plan is **finalized** from fresh evidence. Finalization supplies
> the diagnosis-dependent routing state, including `primary_fog_type`, the final
> routing audit and contract-valid workflow selection, and produces the
> canonical `workflow_orchestration_plan`.
>
> Only the finalized artifact is required to satisfy `validate-plan.py`.
>
> `primary_fog_type` must never be guessed or synthesized before diagnosis
> merely to satisfy the schema.
>
> The Phase-2 execution skeleton and the finalized orchestration plan therefore
> represent **different knowledge states**, even if implementation retains them
> within one runtime lifecycle.
>
> This decision does not authorize automatic workflow chaining. Recommendation
> remains distinct from execution authority, and #230 remains separate.

**Stronger invariant (adopted with the decision):**

> **The Phase-2 skeleton's workflow identity must not silently become the final
> plan's routing decision.**

Before diagnosis the runtime knows only "this diagnostic workflow is executing"
(e.g. `fast-local-diagnostic`). After diagnosis the final plan records the
diagnosis-dependent routing state (e.g. `primary_fog_type: product_fog`,
`system_recommended_workflow`, and a contract-valid `chosen_workflow_id` such as
`product-implementation-workflow`, or another explicitly authorized selection).
These are different facts. Finalization must not merely append
`primary_fog_type` to the skeleton's execution identity; it must produce the
final routing decision from the brief's evidence.

## 3. Consequences

- **Lifecycle model**: the Phase-2 artifact is a provisional execution skeleton
  (a different knowledge state from the canonical plan). The canonical
  `workflow_orchestration_plan` exists only after finalization, which occurs
  once a valid brief exists.
- **Validation boundary**: only the finalized artifact is required to pass
  `validate-plan.py`. The provisional skeleton is not required to satisfy the
  full plan contract and must not fabricate diagnosis-dependent fields.
- **`chosen_workflow_id` semantics**: before finalization it denotes the
  workflow currently being executed; after finalization it denotes the
  contract-valid routing decision (fog-aligned implementation workflow or an
  explicitly authorized selection with an appropriate
  `routing_decision_method`). The skeleton's execution identity must not
  silently become the final routing decision.
- **No fabricated diagnosis**: `primary_fog_type` (and any other
  diagnosis-dependent field) may be emitted only from brief evidence, never
  synthesized to satisfy the schema.
- **Recommendation is not execution authority** (unchanged, ADR 0014 /
  CONTEXT.md): the finalized plan is a planning artifact; automatic workflow
  chaining remains non-ratified.
- **#230 remains separate**: this decision does not touch
  `workflow-registry.yaml` `auto_invoke_next_workflow` compatibility or the
  runtime's automatic-chaining read machinery. The generator repair requires
  zero registry/runtime-behavior change.
- **First #232 implementation scope** (for the future implementation session):
  - IN: `scripts/workflow-runtime.py` (provisional skeleton + finalization in
    `generate_plan` and its callers; `workflow_steps` rename; `created_at`;
    stale auto-invocation prose in comments), `tests/test_generate_plan_conformance.py`
    (prove BOTH states: provisional generation does not fabricate diagnosis;
    finalization after real/fixture brief produces a valid canonical plan),
    `skills/workflow-planner/references/workflow-orchestration-template.md`
    (`steps` -> `workflow_steps`, add fog field, remove automatic-invocation
    wording), and a minimal artifact-contracts.yaml comment clarification if
    needed.
  - OUT: `scripts/workflow-planner.py` (orphaned legacy producer; dead-code
    disposition is a separate future question), `workflow-registry.yaml`,
    `auto_invoke_next_workflow`, `src/sensemaking_skills/runner.py`, validators
    (must not be weakened), and #230.

## 4. Supporting evidence

- Reproduction (current `main` `52812d3` and pristine PR #228 base `1ffde16`):
  `tests/test_generate_plan_conformance.py` fails identically with the three
  missing-field errors for `full-local-sensemaking` and `fast-local-diagnostic`.
- Runtime machine block (probe-verified) contains 21+ fields including `steps`
  (legacy) but omits `primary_fog_type`, `workflow_steps`, `created_at`.
- Plan authoring precedes the brief: `run()` calls `self.generate_plan()` at
  Phase 2 (`scripts/workflow-runtime.py` ~2564-2568) before steps execute;
  `repo-sensemaker` (brief producer) is step 4 of `full-local-sensemaking` in
  `skills/workflow-planner/references/workflow-registry.yaml`.
- Validator semantics: `scripts/validate-plan.py` requires all six
  contract fields and enforces the fog->workflow alignment check on
  `primary_fog_type` vs `chosen_workflow_id`.
- Producer/contract timeline: runtime became canonical producer 2026-05-22
  (`798eae7`, conformance test added); the plan contract was changed 2026-05-25
  (`2849043` — `primary_fog_type` moved to REQUIRED, `routing_decision_method` /
  `workflow_steps` / `created_at` added, `steps` renamed to `workflow_steps`);
  the producer was never reconciled afterward. PR #228 (`1ffde16`) and PR #231
  (`631061a`) do not touch the producer, the contract, or
  `scripts/workflow-planner.py`.
- Fallback semantics already present: artifact-contracts.yaml note ("If absent,
  the runtime falls back to the repository_sensemaking_brief") and
  `OrchestrationRunner._resolve_fog_type` ("may not be present in the
  orchestration plan ... falls back to the brief").
- Full triage record with reasoning discipline: `docs/triage/232-workflow-orchestration-plan-lifecycle.md`.

## 5. Missing evidence / experiment triggers

- Implementation mechanics of finalization (where in the runtime lifecycle the
  finalized plan is produced from the brief, and whether the provisional
  skeleton carries any lightweight validation) are deliberately left to the
  implementation session; this ADR ratifies the semantics, not the sequencing
  details.
- Revisit this ADR if: a consumer is found that requires the provisional
  Phase-2 skeleton itself to be contract-valid (e.g. a tool that validates
  plans before the brief exists); or the owner decides to ratify automatic
  workflow chaining (which would additionally implicate #230).
- Dead-code disposition of `scripts/workflow-planner.py` (delete / archive /
  annotate) is explicitly out of scope and deferred to a separate decision.

## 6. Status rationale

ACCEPTED: the owner ratified the two-stage lifecycle decision on 2026-08-23
during review of the #232 triage, including the stronger invariant that the
Phase-2 skeleton's workflow identity must not silently become the final plan's
routing decision. Per the repository convention in `docs/adr/README.md`,
"Accepted" records the operative decision; the merge of the carrying branch to
`main` is a separate repository action, not part of this record's content.
