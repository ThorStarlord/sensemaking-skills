# PRD: Mode Proving & Pressure-Tested Automation

## Problem Statement

The `sensemaking-skills` repository has a complete automation system: 5 execution modes, 11 registered workflows, a three-level validator hierarchy (7 scripts, 42 passing fixture tests), and one successful YOLO execution that proved the validator chain works end-to-end. But beyond that single YOLO run, the system's safety claims are untested:

- **3 of 5 execution modes** have zero live-run evidence. `plan_only`, `prompt_chain`, and `autonomous_execution` exist only in SKILL.md definitions and registry entries — no orchestrator has ever executed them and produced a run log.
- **3 of 5 Level 3 validators** have never been invoked outside fixture tests. `validate-plan.py`, `validate-skill-improvement-plan.py`, and `validate-usage-research-report.py` have comprehensive negative fixture coverage but have never run against a real artifact produced by a live execution.
- **Approval gates have never been exercised** in any mode, on any workflow. The gate system — approval prompts, `gate_result: approved_by_user` timestamps, gate-name validation against the workflow registry — is entirely theoretical. The partial `guided_execution` run paused before reaching its first gate; the YOLO run bypassed all gates.
- **One workflow** (`fast-local-diagnostic`, 2 steps) has been run. The other 10 workflows — including the 4-step `full-local-sensemaking` that exercises the flagship pipeline and the 8-step `product-autonomous-sprint` — have never been executed in any mode.

Without systematic mode proving, the system has a coverage hole: the components that will matter most in high-risk execution (`autonomous_execution` gates, `validate-plan.py` live behavior, multi-step artifact flow) are the least tested. This PRD closes that gap.

## Solution

Prove every execution mode through live runs on eligible workflows, following a strict risk gradient from lowest to highest blast radius. No code changes are required — the SKILL.md protocols, validator scripts, artifact contracts, and workflow registries are already deployed. The "implementation" is execution of the existing protocol, not new infrastructure.

The five proving runs, in order:

1. **`plan_only` on `fast-local-diagnostic`** — Produce the first live orchestration plan with Section 11 (machine-readable plan). Exercising `validate-plan.py` against a real artifact for the first time. Zero risk: no mutation, no gates.
2. **`prompt_chain` on `fast-local-diagnostic`** — Produce the first live prompt chain. Exercises `validate-prompt-handoff.py` on chain output. Zero risk: no mutation.
3. **`guided_execution` (full completion) on `docs-contract-reconciliation`** — Complete the run that paused at Step 1's gate. This proves the gate protocol works: approval prompts fire, `gate_result: approved_by_user` gets recorded, and the next step actually starts. Low risk: human approval gates at every step.
4. **`autonomous_execution` on `fast-local-diagnostic`** — First test of the opt-in gate mechanism. The orchestrator must receive the explicit opt-in string, then execute all steps with automated gate halts. Medium risk: feature branch, run log required.
5. **`yolo_execution` (second workflow) on `full-local-sensemaking`** — 4 steps instead of 2. Exercises the full core sensemaking pipeline (problem-framer → unknowns-mapper → repo-sensemaker → handoff). Proves the YOLO protocol scales beyond the simplest 2-step path. High risk: feature branch, post-step verification, zero-tolerance validators.

Per the **Harden Only Where Pressured** principle (sharpened to require **Repeatable Failure Boundaries**), hardening is deferred until a failure class recurs across independent runs. Single-occurrence data issues are corrected at the artifact level via the TDD Validator Cycle and do not trigger system-level changes.

## User Stories

1. As a **repository owner**, I want every execution mode to have at least one live run with a published run log, so that I can make safety claims based on evidence rather than design theory.

2. As a **workflow-orchestrator agent**, I want a proven mode protocol (pre-flight → step execution → validator invocation → run log) for all five modes, so that I execute consistently regardless of which mode is selected.

3. As a **safety reviewer**, I want `validate-plan.py` exercised against a real orchestration plan artifact, so that I can verify its Section 11 enforcement, approval gate matching, and disallowed-mode detection work on actual output.

4. As an **operator monitoring `autonomous_execution`**, I want the opt-in gate to actually halt execution before the first step, so that I can confirm the safety mechanism works before trusting it for higher-risk workflows.

5. As a **developer debugging a failed `guided_execution` run**, I want a complete run log showing which gates were approved, by whom, and at what time, so that I can audit the human decision trail.

6. As a **contributor expanding the workflow registry**, I want the `fast-local-diagnostic` workflow to serve as a reference proving run for all eligible modes, so that I can replicate the protocol pattern for new workflows.

7. As a **maintainer assessing system health**, I want a mode-coverage tracker that records which mode-workflow combinations have been proven and where the run logs live, so that I can see at a glance what is and isn't covered.

8. As an **operator running `full-local-sensemaking` in YOLO mode**, I want the post-step validator stack to catch failures across all 4 steps (problem_frame → unknowns_map → brief → handoff), so that I can trust the automation pipeline at scale.

9. As a **safety reviewer auditing the system**, I want the hardening threshold explicitly documented (repeatable failure boundary = same failure across 2+ independent runs), so that I can evaluate whether skipped hardening was a correct call.

10. As a **developer adding a new YOLO-eligible workflow**, I want the `full-local-sensemaking` YOLO run to serve as a reference for multi-step YOLO execution, so that I can follow the same pattern without reinventing the protocol.

11. As a **workflow-orchestrator agent**, I want to know which mode a workflow does NOT support before attempting execution, so that I never attempt `yolo_execution` on a workflow that only allows `guided_execution`.

12. As a **usage researcher evaluating the system**, I want the `prompt_chain` mode proven by a live run, so that I can evaluate whether the produced prompts are actually useful without modifications.

13. As a **developer testing the TDD Validator Cycle**, I want to see the cycle operate across different modes and validators, so that I can confirm the RED → GREEN → REFACTOR pattern is consistent regardless of execution mode.

14. As a **contributor reviewing the `plan_only` run**, I want the produced orchestration plan to contain a complete Section 11 (machine-readable plan) that passes `validate-plan.py`, so that I can trust the plan is machine-verifiable.

15. As a **maintainer**, I want each proving run to produce a feature branch with all artifacts and the run log, so that rollback and review are always possible without losing forensic data.

## Implementation Decisions

### Module 1: Mode Proving Protocol (Deep Module)

The central deep module. Each proving run follows the same protocol; the mode determines which steps are active:

```
Pre-flight:
  - git status --porcelain must be clean
  - Current branch is NOT main/master (for mutating modes)
  - python scripts/test-validators.py (exit 0 or halt)
  - python scripts/validate-repo.py (exit 0 or halt) for mutating modes
  - HEAD SHA captured for rollback target
  - Feature branch created if mode requires mutation

Execution:
  - plan_only: produce orchestration plan with Section 11 → validate-plan.py → stop
  - prompt_chain: produce prompt artifacts → validate-prompt-handoff.py → stop
  - guided_execution: execute one step → validate (L2 + L3) → present gate → record approval → next step
  - autonomous_execution: execute with opt-in → present gates → wait for approval → continue
  - yolo_execution: execute all → validate (L2 + L3) after each step → hard stop on failure

Post-step validation:
  - Look up artifact_id in artifact-contracts.yaml
  - Run generic_validator (Level 2)
  - Run all specialized_validators (Level 3)
  - aggregate: pass if all pass, halt if any fails

Recording:
  - Run log written per run-log-template.md
  - All validator invocations and results recorded
  - Gate approvals/denials/bypasses timestamped
```

This is a deep module because the interface is simple ("prove mode X on workflow Y") while the encapsulated complexity is high: pre-flight checks, step execution, validator stack dispatch, gate handling, TDD cycle management, run log writing, and rollback advice. Each concern can be verified independently (e.g., pre-flight against a dirty worktree, validator dispatch against artifact-contracts.yaml).

The protocol is already partially defined in `workflow-orchestrator/SKILL.md` for YOLO mode. This PRD formalizes it across all five modes. No code change is needed — the orchestrator SKILL.md already specifies the behavior; the proving runs test compliance.

### Module 2: Mode Coverage Tracker

A lightweight record that tracks which mode-workflow combinations have been proven. Stored as a section in the existing run log index or as a separate reference file:

```
mode_coverage:
  - mode: yolo_execution
    workflow: fast-local-diagnostic
    last_run: 2026-05-16
    run_log: <link to run log>
    steps_completed: 2/2
    validators_exercised: [L1, L2, brief-L3, handoff-L3]
    gates_exercised: false (bypassed by design)
    hardening_triggered: none

  - mode: guided_execution
    workflow: docs-contract-reconciliation
    last_run: 2026-05-14
    run_log: runs/run_log_20260514.md
    steps_completed: 1/3
    validators_exercised: [L2]
    gates_exercised: false (paused before first gate)
    hardening_triggered: none
```

This tracker makes coverage gaps visible at a glance and prevents regressing to unproven states.

### Module 3: Gate Exerciser Protocol

The approval gate protocol that `guided_execution` and `autonomous_execution` share. It has never been exercised, so the proving runs test it for the first time:

```
1. Identify the next gate from workflow-registry.yaml step definition
2. Present gate to user with: workflow context, artifact produced, risk summary
3. Record response:
   - approved_by_user: continue to next step (timestamp + user recorded)
   - denied: stop execution, write run log, recommend rollback if applicable
4. In autonomous_execution: same protocol, but opt-in at start replaces per-gate user presence
5. In yolo_execution: gate_behavior set to bypassed_by_yolo, no user prompt
```

The key testable behaviors:
- Does the gate name match a valid gate in the workflow registry?
- Is the approval/denial correctly timestamped and attributed?
- Does a denial actually halt execution?

### Ordering Rationale

The proving order follows a strict risk gradient:

```
plan_only → prompt_chain → guided_execution → autonomous_execution → yolo_execution
(no mutation)              (human gates)           (opt-in gates)    (full automation)
```

Each mode builds on the previous: `plan_only` proves the orchestrator can produce a valid plan; `prompt_chain` proves it can produce valid prompts; `guided_execution` proves gates halt execution; `autonomous_execution` proves opt-in gates work without human per-step presence; `yolo_execution` proves zero-tolerance post-step verification for a more complex workflow.

This ordering ensures that if a mode fails, the failure is caught at the lowest-risk point: `plan_only` failure means the orchestrator can't produce a valid plan — finding this before attempting any mutating mode saves hours of recovery.

### Hardening Threshold

Per the **Repeatable Failure Boundary** definition sharpened in this session, system hardening is triggered only when the same failure class appears in 2+ independent runs. Single-occurrence failures are corrected at the artifact level (TDD Validator Cycle) and do not warrant systemic changes.

This threshold applies to:
- Validator script changes (new checks, new error codes)
- Contract schema changes (new required fields, structural changes)
- Template changes (new sections, new required patterns)
- Registry changes (new validation rules, new enforcement logic)

It does NOT apply to:
- Artifact content fixes (data quality)
- Run log corrections (factual accuracy)
- Documentation updates (clarity, completeness)
- Fixture additions (test coverage)

The first proving run established this threshold in practice: `UNKNOWN_WEAKNESS_TYPE` and `NO_LOGIC_TRACE` were single-occurrence data issues fixed in the artifact. They did not trigger system hardening. If either recurs in a subsequent run, hardening is warranted.

## Testing Decisions

### What Makes a Good Test

A good test in this context is a **live proving run** — not a unit test, but a complete execution of a workflow in a specific mode that exercises:
- The orchestrator's compliance with its SKILL.md protocol
- The validator stack against real artifacts
- The gate system with actual human or automated approval decisions
- The run log as a forensic record

Each proving run IS a test: it externalizes the result as a run log with pass/fail per step, validator invocation results, and gate outcomes. The existing fixture-based test suite continues to validate individual validators in isolation.

### What Gets Tested

- **Proving Run 1 (plan_only):** Orchestrator produces Section 11 plan → validate-plan.py passes → run log written
- **Proving Run 2 (prompt_chain):** Orchestrator produces prompts → validate-prompt-handoff.py passes → run log written
- **Proving Run 3 (guided_execution):** Full 3-step completion → all gates exercised → Level 2 + Level 3 per step → run log with approval timestamps
- **Proving Run 4 (autonomous_execution):** Opt-in string validated → gates halt automatically → run log written
- **Proving Run 5 (yolo_execution):** 4-step pipeline → zero-tolerance validators per step → feature branch with full artifact set

### Prior Art

The YOLO execution on `fast-local-diagnostic` (Slice 1 + Slice 2) is the prior art. Its run log, TDD cycle handling, pre-flight checks, and post-step verification establish the pattern that all subsequent proving runs follow. The `docs-contract-reconciliation` guided_execution partial run provides prior art for gate-adjacent behavior (Step 1 completed, gate presented but not decided).

### What Is NOT Tested

- Individual validator edge cases: covered by the 42-case fixture suite and REGRESSIONS.yaml
- Workflows requiring external skills: `product-discovery-sprint` uses `external_routing` steps and cannot run locally
- CI/CD pipeline integration: the proving runs are agent-driven, not pipeline-driven
- Merging proving branches to main: each run produces a feature branch for review; merge requires separate human approval

## Out of Scope

- **No new validator scripts.** The existing 7 scripts (Level 1 + Level 2 + 5 Level 3) are sufficient for all proving runs. Adding validators for other artifact types is explicitly excluded.
- **No CI/CD pipeline changes.** Proving runs are agent-driven, executed by the workflow-orchestrator per its SKILL.md protocol. No GitHub Actions or other CI changes.
- **No external agent handoff.** The `prompt_handoff` artifacts are validated but not delivered to external agents. That is a separate integration concern.
- **No schema changes.** The existing YAML-based registries (workflow-registry.yaml, skill-registry.yaml, artifact-contracts.yaml) are unchanged. No migration to JSON Schema or Pydantic.
- **No `validate-repo.py` refactor.** It remains a structural validator, excluded from fixture coverage, with its own CLI interface.
- **No new workflows.** The 11 existing workflows are sufficient for proving all modes. No new workflow definitions.
- **No merging proving branches.** Each run produces a feature branch for review. Merging requires human approval outside this scope.
- **No LLM self-review step.** The proving runs use only script-based validators (Level 2 + Level 3). LLM-based post-step verification is advisory and excluded.
- **No hardening implementation.** Hardening is deferred per the Repeatable Failure Boundary principle. This PRD covers the proving runs that generate the evidence for future hardening decisions.
- **No `skill-maintenance-loop` workflow proving.** It only supports `guided_execution` and its skills (skill-maintainer, handoff) require a `usage_research_report` input that doesn't exist without a prior usage research run.

## Further Notes

- Pre-run prerequisite: `python scripts/test-validators.py` must pass (42/42) and `python scripts/validate-repo.py` must pass before each proving run. Both verified green as of 2026-05-16.
- The `fast-local-diagnostic` workflow is the proving workhorse: it supports all 5 modes, has 2 local-only steps, and already has a valid `repository_sensemaking_brief` artifact. It is the lowest-cost proving target for every mode except `guided_execution`.
- `guided_execution` proving uses `docs-contract-reconciliation` because the partial run already exists (Step 1 completed). Completing it costs less than starting a new guided run on a different workflow.
- `yolo_execution` proving uses `full-local-sensemaking` (not repeating `fast-local-diagnostic`) because the goal is to scale beyond the already-proven 2-step path. Four steps with 3 different skill types (framer, mapper, sensemaker, handoff) exercises significantly more of the validator ecosystem.
- The **TDD Validator Cycle** is expected to activate during proving runs. Each occurrence is an opportunity to observe whether the failure is a repeatable pattern warranting hardening or a single-occurrence data issue. Run logs should capture every cycle turn (RED → GREEN → REFACTOR) with the error code and fix applied.
- The term **automation slice** from the first YOLO run PRD is deprecated in favor of **proving run**, which more precisely describes the intent: not building new automation, but proving existing automation works across its full operational envelope.
