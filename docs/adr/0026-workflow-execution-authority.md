# ADR 0026: Execution Authority for `auto_invoke_next_workflow`

**Status**: ACCEPTED — owner decision 2026-08-24 (ratified after the #230
triage): the authority-gated-consumer model. `auto_invoke_next_workflow` may
remain as compatibility metadata but is NOT execution authority. Merge to
`main` is a separate repository action, pending and not part of this record.

**Date**: 2026-08-24

**Resolves**: Issue #230 (the registry/runtime auto-invocation
compatibility/authority drift decision uncovered by its triage; the issue
remains open as the tracker for the bounded implementation)

**Depends on**:
- ADR 0013 (Accepted — agent-native orchestration is the primary model; the
  active coding agent owns the recursive control loop, and
  `workflow-runtime.py` is a separate automation/compatibility path, not the
  semantic definition of Skill execution)
- ADR 0014 (Accepted — product boundary: automatic downstream routing is
  deferred; a recommendation is not execution authority; the runtime
  orchestrates only this product's own chain)
- ADR 0025 (Accepted — two-stage `workflow_orchestration_plan` lifecycle; the
  provisional skeleton is a different knowledge state; finalization is
  explicit-method-only and non-ratified for automatic chaining; #230 remains
  separate)
- ADR 0018 (SUPERSEDED 2026-08-18 — historical deterministic-routing proposal;
  its disposition states `primary_fog_type` does not grant execution or
  routing authority and no replacement automatic-routing policy is Accepted)
- `CONTEXT.md` (line 93: automatic routing is not ratified product behavior;
  runtime routing paths are compatibility machinery unless separately
  ratified) and `docs/decision-orchestration-boundary.md` (guardrail 2)

---

## 1. Context and problem statement

`skills/workflow-planner/references/workflow-registry.yaml` still carries
`auto_invoke_next_workflow` entries that historically encoded automatic
chaining from one registered workflow to the next. The same field (and the
`auto_invoke_source` / `auto_invoke_next_workflow_id` companions) is consumed
by two runtime consumers and mirrored across two registry copies.

The ratified authority model that governs the product today (ADR 0013, ADR
0014, ADR 0018 disposition, ADR 0025, CONTEXT.md, and the
decision-orchestration-boundary guardrails) establishes that a
recommendation, a selection, or the mere existence of a registry flag must
**not** be treated as execution authority. The #230 triage confirmed that no
ratified material grants execution authority to the registry boolean, and that
the mechanism's effective "authority" today is only that boolean plus a
workflow ID extracted from an artifact.

This leaves a semantic contradiction alive: the registry field presents
legacy deterministic automatic-chaining as if it were a forward, authorized
path. The #230 triage additionally observed that this is currently mostly
dormant (the ADR-0025 provisional plan fails `validate-plan.py`, deterministic
executors stop earlier), but **unreachability is not an authority model** — a
later improvement could resurrect the latent subprocess chaining behavior.

## 2. Decision

Ratified invariant:

> **recommendation ≠ selection ≠ execution authorization.**

`auto_invoke_next_workflow: true` means, at most:

> "Legacy/compatibility metadata indicates that this workflow historically had
> a possible next-workflow relationship."

It does **not** mean: "the runtime is authorized to spawn that workflow."

Precisely:

1. `auto_invoke_next_workflow: true` cannot itself authorize a child workflow.
2. `recommended_workflow_id`, `chosen_workflow_id`, `selected_workflow`,
   `primary_fog_type`, successful validation, a finalized ADR-0025 plan, or
   the current execution mode cannot independently grant chaining authority.
3. A next workflow may execute only after a **separate explicit authority
   event** from the active agent/human authority model.
4. If no such authority event exists, the runtime must **fail closed**: it may
   surface/log a candidate next workflow, but must not spawn it.
5. Existing registry metadata and compatibility parsing may be retained where
   needed; this decision does NOT require broad deletion.
6. No generic automatic-routing policy is being ratified.
7. ADR-0025 finalization remains recommendation/planning state, not execution
   authority.
8. Full-run `finalize_plan()` integration is a later responsibility; #230's
   job is to remove the latent authority ambiguity that currently makes such
   integration unsafe.

## 3. Consequences

- **Durable invariant, cross-consumer**: the invariant above governs
  `scripts/workflow-runtime.py`, `src/sensemaking_skills/registry.py`, and
  `src/sensemaking_skills/runner.py` — the script runtime's Phase-7
  same-mode subprocess auto-invocation path, plus the packaged library's
  parallel `_handle_auto_invocation` consumer. When #230 is implemented, all
  consumers must reconcile to "no explicit authority event → surface/log, do
  not spawn."
- **Registry semantics**: `auto_invoke_next_workflow` becomes compatibility /
  historical-transition metadata. It does not, by itself, authorize spawning.
- **Metadata retention**: existing registry fields and parsing may remain;
  this is deliberate — remove authority, not necessarily representation.
- **#230 implementation scope (for the future implementation session)**:
  - IN: reconcile both runtime consumers (script runtime + packaged
    library) and both registry copies
    (`skills/workflow-planner/references/workflow-registry.yaml` and
    `src/sensemaking_skills/defaults/workflow-registry.yaml`), update
    `tests/test_auto_invocation_target_repo.py` / `test_registry.py` and
    documentation to encode the authority-gated model, and gate any automatic
    spawn behind the explicit-authority event, failing closed when it is
    absent.
  - OUT: wiring ADR-0025 `finalize_plan()` into `run()` full-run finalization;
    deleting `auto_invoke_next_workflow` outright; inventing a new generic
    authority framework inside #230; unrelated residual cleanup (orphaned
    `scripts/workflow-planner.py`, legacy `manual_override` alias,
    `user_implied_fog_type` fallback, ADR-0008 metadata).
- **Fail-closed default**: in the absence of a ratified authority primitive
  that semantically fits, the runtime must disable/fail-close the automatic
  spawn path and report the missing authority primitive as a later
  responsibility — not invent new machinery inside #230.

## 4. Supporting evidence

The evidence preserved from the completed #230 triage:

- **Four registry entries** with `auto_invoke_next_workflow: true` in the
  runtime-loaded copy (`skills/workflow-planner/references/workflow-registry.yaml`):
  `fast-path-workflow`, `full-fog-workflow` (source
  `workflow_orchestration_plan.recommended_workflow_id`),
  `full-local-sensemaking` (source `workflow_orchestration_plan`), and
  `ui-diagnostic-workflow` (source `ui_specification` **plus explicit**
  `auto_invoke_next_workflow_id: ui-implementation-workflow`).
- **Script-runtime + packaged-library consumers**:
  `scripts/workflow-runtime.py` (Phase-7 `_should_auto_invoke_next` →
  `_extract_recommended_workflow` → `_invoke_next_workflow`) and
  `src/sensemaking_skills/runner.py` / `src/sensemaking_skills/registry.py`
  (`_handle_auto_invocation`, `has_auto_invocation`,
  `get_recommended_next_workflow`).
- **Current Phase-7 behavior**: same-mode subprocess invocation
  (`scripts/workflow-runtime.py` line ~1665-1709, spawning
  `workflow-runtime.py --workflow NEXT --mode SAME --executor SAME --chained`),
  gated by source artifact state in `{VALIDATED, EXECUTED, APPROVED}`.
- **ADR-0025 provisional-plan interaction**: `run()` writes the provisional
  skeleton at Phase 2; the workflow-planner step does not re-author it; the
  provisional plan fails `validate-plan.py` (missing `primary_fog_type`,
  `workflow_steps`, `created_at`), so plan-producing workflows do not reach
  Phase 7.
- **Currently dormant/unreachable behavior** for plan-producing workflows:
  verified empirically — `fast-path-workflow` in `autonomous_execution` on a
  clean `main` halts at Step 1 (`failed`) before Phase 7.
- **`ui-diagnostic-workflow` explicit-next path**: reachable *in principle*
  if its `ui_specification` source reaches a valid state, via the explicit
  `auto_invoke_next_workflow_id` (the only auto-invoke entry that does not
  depend on the plan artifact for its target).
- **Two registry-copy drift**: the packaged defaults copy
  (`src/sensemaking_skills/defaults/workflow-registry.yaml`) and the runtime
  copy (`skills/...`) are not byte-identical and must both be reconciled.

## 5. Missing evidence / experiment triggers

- Whether an existing ratified authority primitive already semantically fits
  the "explicit authority event" requirement for auto-invocation is not
  established; if none exists, #230 must fail-close the spawn path and report
  the gap as a later responsibility rather than invent new machinery.
- Revisit this ADR if the owner later ratifies automatic workflow chaining, or
  if a consumer is found that requires automatic spawn without a separate
  authority event.

## 6. Status rationale

ACCEPTED: the owner ratified the authority-gated-consumer model on 2026-08-24
after the #230 triage established that the executable surface is understood and
that the remaining uncertainty is an owner authority decision, not missing
technical evidence. Per the repository convention in `docs/adr/README.md`,
"Accepted" records the operative decision; the merge of the carrying branch to
`main` is a separate repository action, not part of this record's content.
