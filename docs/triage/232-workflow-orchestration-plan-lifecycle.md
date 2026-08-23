# #232 Triage Record - workflow_orchestration_plan lifecycle/contract drift (REVISED)

Superseded note (2026-08-23): the owner ratified Option A via
`docs/adr/0025-workflow-orchestration-plan-lifecycle.md`; issue #232 was
transitioned to `ready-for-agent`. This file remains the investigation/evidence record.

Status: **REMAIN_NEEDS_TRIAGE** (revised 2026-08-23 after owner review; supersedes the
earlier draft READY_FOR_AGENT conclusion from the same session)
Branch/commit this records: current `main` = `52812d3` (PR #231 merged on top of PR #228).
Producer attribution verified against a detached worktree at `52812d3` and `1ffde16`.

This record is a triage/analysis artifact only. It contains NO code mutation, NO issue
label change, NO PR. It records findings and an owner-decision draft (Option A below)
that is pending the owner's formal ratification.

---

## 1. Decision

**REMAIN_NEEDS_TRIAGE** - until the owner ratifies one plan-lifecycle model (draft:
Option A, two-stage finalization, below). After ratification the issue becomes
`ready-for-agent` with the bounded scope in section 6.

Why not READY_FOR_AGENT: the reproduced missing-field failure is real, but
`primary_fog_type` is NOT a mechanical missing field. The runtime authors the
orchestration plan at Phase 2 (workflow-runtime.py:2564-2568), BEFORE the
repository_sensemaking_brief (and therefore the diagnosed fog) exists
(repo-sensemaker is step 4 of full-local-sensemaking). At plan-generation time
`primary_fog_type` is unknowable, yet the current contract lists it as REQUIRED.
Additionally, the validator's fog->workflow alignment check (validate-plan.py:548-577)
treats the plan as a fog-informed routing decision, while the runtime plan describes
the workflow being executed. That is a lifecycle/artifact-semantics fork, not a
missing-field bug. An AFK agent cannot resolve that fork by itself without either
fabricating a fog value (evidence violation) or silently picking one of two competing
artifact models.

Why not READY_FOR_HUMAN: no human needs to write code. A single owner decision on the
plan lifecycle unlocks a fully bounded agent implementation.

## 2. Reproduced defect (demonstrated facts)

- `tests/test_generate_plan_conformance.py` drives the REAL canonical producer
  `OrchestrationRunner.generate_plan()` (scripts/workflow-runtime.py), not
  scripts/workflow-planner.py.
- Both tests FAIL on current main with exactly:
  - ERROR [missing_field] primary_fog_type: Required field 'primary_fog_type' is missing.
  - ERROR [missing_field] workflow_steps: Required field 'workflow_steps' is missing.
  - ERROR [missing_field] created_at: Required field 'created_at' is missing.
- Runtime's emitted machine block (probe-verified) contains artifact_id,
  source_intent_ref, chosen_workflow_id, execution_mode, system_recommended_workflow,
  selected_workflow, routing_divergence, routing_decision_method, escalation_recommended,
  auto_escalation_allowed, scope_expansion_requires_approval, status, session_id,
  initial_inputs, steps (legacy name), approval_gates, gate_behavior, stop_conditions,
  subset_run, subset_reason, included_steps, excluded_steps. Missing: primary_fog_type,
  workflow_steps, created_at.
- Identical failure reproduced at pristine `1ffde16` (PR #228 base). Pre-existing; NOT a
  #229/#231 regression; not environment-specific.
- Separately, scripts/workflow-planner.py (standalone CLI) DOES emit primary_fog_type /
  workflow_steps / created_at. Its actual validate-plan.py failures are different
  (missing status, missing initial_inputs, step_id-vs-id shape drift, no status/step_type
  per step, approval-gates/stop-conditions mismatch). The issue's attribution of the
  three-field failure to that file is therefore incorrect; the file is orphaned dead
  code (no callers, no tests, no skill references; last touched 2026-05-25, `2849043`).

## 3. Root cause (derived conclusion, evidence-grounded)

Timeline:
- 2026-05-22 `798eae7`: runtime made canonical plan producer (ADR 0010 extension);
  test_generate_plan_conformance.py added. Producer written against the then-current
  contract.
- 2026-05-25 `2849043`: workflow_orchestration_plan contract changed - primary_fog_type
  moved to REQUIRED, routing_decision_method / workflow_steps / created_at added,
  required sections reshaped. The runtime producer was NEVER reconciled to this contract.
- PR #228 (1ffde16) and PR #231 (631061a) do not touch workflow-runtime.py, the plan
  contract, or scripts/workflow-planner.py (verified via their diffs), so the drift
  survived both merges. The conformance test has been red since 2026-05-25.

Deeper mismatch (the reason a pure producer patch is insufficient):
- Contract + validator: primary_fog_type is REQUIRED in the plan, and the validator
  enforces fog->implementation-workflow alignment (validate-plan.py:548-577).
- Runtime reality: the plan is authored at Phase 2, before fog exists; and the plan's
  chosen_workflow_id is the workflow being executed (e.g. fast-local-diagnostic), which
  is not a fog-mapped implementation workflow. Copying a fog value into such a plan can
  trigger the alignment check (product_fog + fast-local-diagnostic would be rejected).
- The contract itself carries a contradictory note (artifact-contracts.yaml, under
  recommended_machine_fields, ~line 480): "If absent, the runtime falls back to the
  repository_sensemaking_brief" - and the runtime consumer implements exactly that
  fallback (_resolve_fog_type docstring: "may not be present in the orchestration plan").
  So absence-with-fallback is already the runtime's model; the REQUIRED status is not.

## 4. The semantic fork (two competing meanings of workflow_orchestration_plan)

- Model A - execution plan: "this artifact describes the workflow currently running"
  (chosen_workflow_id = fast-local-diagnostic; authored Phase 2, pre-brief).
- Model B - routing-decision plan: "this artifact records which implementation workflow
  was selected from a diagnosed fog" (primary_fog_type + chosen_workflow_id =
  product-implementation-workflow; authored post-brief).

These are not the same artifact semantics. The current contract and validator encode
Model B; the runtime producer and its consumer fallback encode Model A. Three coherent
resolutions exist (owner decision required):

- Option A (RECOMMENDED) - two-stage plan lifecycle: Phase-2 artifact is a provisional
  execution skeleton (no fog); after repo-sensemaker produces the brief, the runtime
  FINALIZES the canonical plan with primary_fog_type, routing audit, workflow_steps,
  created_at; validate-plan.py must pass on the finalized artifact. No fog value is ever
  fabricated before diagnosis.
- Option B - make primary_fog_type optional/fallback-capable in the plan contract
  (fog stays authoritative in the brief). This matches the existing contract comment and
  runtime fallback, but is a product-contract change.
- Option C - do not author the canonical plan at Phase 2; author it only after
  diagnosis. Cleanest semantics, but changes more runtime architecture; not preferred
  without stronger reason.

## 5. Corrected decomposition

#232 CORE
  Canonical workflow_orchestration_plan lifecycle / producer contract
    - runtime producer conformance (workflow-runtime.py generate_plan)
    - pre-diagnosis vs post-diagnosis artifact state (the fork above)
    - workflow_steps naming (steps -> workflow_steps)
    - created_at

RELATED SEMANTIC DRIFT (same skill package, same producer surface)
  skills/workflow-planner/references/workflow-orchestration-template.md
    - stale `steps` (should be workflow_steps)
    - missing fog field in the machine block
    - stale "This determines which implementation workflow will be automatically invoked."

DEAD LEGACY COMPONENT (NOT part of first #232 implementation)
  scripts/workflow-planner.py
    - disposition deferred: delete / archive / annotate (separate decision)

#230 (SEPARATE - confirmed)
  registry/runtime automatic-chaining compatibility
    - workflow-registry.yaml auto_invoke_next_workflow entries
    - runtime auto-invocation read machinery (_should_auto_invoke_next,
      _extract_recommended_workflow, src/sensemaking_skills/runner.py legacy path)
  The generator repair requires zero registry/runtime-behavior change; validate-repo.py
  and the validate-plan fixture suite are green on current main.

## 6. Bounded implementation scope (only AFTER owner ratifies a lifecycle model)

Draft scope (Option A):
- scripts/workflow-runtime.py - generate_plan(): emit created_at; emit workflow_steps
  (rename from steps); implement two-stage finalization so the finalized plan carries
  primary_fog_type + routing audit sourced from the brief (never fabricated); correct
  stale auto-invocation prose in comments/docstrings.
- tests/test_generate_plan_conformance.py - extend/lock the lifecycle: provisional plan
  valid as skeleton; finalized plan (after brief) passes validate-plan.py.
- skills/workflow-planner/references/workflow-orchestration-template.md - reconcile
  steps->workflow_steps, add fog field, remove automatic-invocation wording.
- Possibly a small artifact-contracts.yaml comment clarification (the contradictory
  "If absent..." note under a REQUIRED field). Contract FIELD REQUIREMENTS themselves
  must not be weakened unless Option B is chosen.

Explicit non-scope for the first implementation:
- workflow-registry.yaml, auto_invoke_next_workflow (#230)
- src/sensemaking_skills/runner.py (#230)
- scripts/workflow-planner.py (dead-code disposition deferred)
- validators (validate-plan.py / validate-artifact.py) must NOT be weakened.

## 7. Verification plan

- tests/test_generate_plan_conformance.py: green on the REAL generate_plan path.
- python scripts/validate-plan.py <finalized-plan> --repo-root . and
  python scripts/validate-artifact.py workflow_orchestration_plan <finalized-plan> --repo-root .: PASS.
- python -m pytest tests/test_field_contract_agreement.py: PASS (field-read aliases stay declared).
- python scripts/test-validators.py: 0 failures (validate-plan fixtures unchanged).
- python scripts/validate-repo.py: PASS.
- Strongest closure: generate a plan through the canonical producer, finalize it after a
  real brief, and validate the resulting artifact against the current contract without
  manual repair. Structural/unit checks alone do not close this issue.

## 8. Recommended next action

1. Owner ratifies Option A (two-stage plan lifecycle) - draft decision text in section 9.
2. Record this triage + the decision (this file; paste to #232 when write access exists).
3. Correct #232's producer attribution (runtime producer, not scripts/workflow-planner.py).
4. Transition #232: needs-triage -> ready-for-agent.
5. Start a fresh implementation session with the section-6 scope.

## 9. Owner-decision draft (Option A)

"Approve two-stage orchestration-plan finalization: the Phase-2 runtime artifact is a
provisional execution skeleton; after repo-sensemaker produces the brief, the runtime
finalizes the canonical workflow_orchestration_plan with primary_fog_type, routing
audit, workflow_steps, and created_at, after which validate-plan.py must pass. No fog
value may be fabricated before diagnosis."

## 10. Reasoning discipline notes

- DEMONSTRATED FACTS: the 3-field runtime failure (reproduced at 52812d3 and 1ffde16);
  runtime machine-block field list; standalone producer's emitted fields and distinct
  failure; contract's six required fields; test drives the runtime; Phase-2 pre-brief
  authoring (workflow-runtime.py:2564-2568; repo-sensemaker step 4); validator alignment
  check (validate-plan.py:548-577); contract fallback note + runtime _resolve_fog_type
  fallback; #228/#231 diffs untouched producer/contract; green validator/field-contract/
  validate-repo baselines.
- DERIVED CONCLUSIONS: root-cause timeline; producer-attribution correction; single
  bounded responsibility AFTER lifecycle ratification; #230 separation.
- INTERPRETATION: the issue body's "workflow-planner.py missing fields" framing is
  inaccurate; the fork is a lifecycle-contract mismatch, not a field bug.
- HYPOTHESES / UNKNOWNS: Option B/C vs A remain open until owner ratification; dead-script
  disposition open; whether the finalized-plan step requires runtime sequencing changes
  (e.g. finalize after step 4) is implementation detail for the future session.
- Correction to prior draft: the earlier READY_FOR_AGENT conclusion treated the three
  fields as a uniform mechanical repair and asserted "no product decision required"
  without resolving the Model-A/Model-B fork. That conclusion is withdrawn.
