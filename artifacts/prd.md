# PRD: Complete Execution Mode Coverage & Live Validator Proof

**Date**: 2026-05-16  
**Source**: Domain Alignment Report on Sensemaking-Skills Orchestration System  
**Goal**: Prove all 5 execution modes through live runs and establish the repeatable failure boundary for hardening decisions

---

## Problem Statement

The sensemaking-skills automation system aims to run real projects end-to-end with high reliability. The orchestration infrastructure exists (runner, validators, gates, workflows), but **only 1 of 5 execution modes has been proven in live execution**. Critical components remain untested:

1. **Mode Coverage Gap**: `plan_only`, `prompt_chain`, and `autonomous_execution` have zero run evidence
2. **Validator Gap**: 3 of 5 Level-3 validators (validate-plan.py, validate-skill-improvement-plan.py, validate-usage-research-report.py) have never executed against real artifacts
3. **Gate Infrastructure Gap**: No run log documents an actual approval event (`gate_result: approved_by_user`) or denial event
4. **Failure Pattern Gap**: No repeatable failure boundary has been established to trigger systemic hardening

This blocks the transition from "system proof-of-concept" to "production-ready automation."

---

## Solution

Systematically execute workflows across all 5 execution modes in a defined order, exercising all validators and gate infrastructure, while documenting repeatable failure patterns. Each mode proven via live run; each validator invoked on real artifacts; each gate decision recorded. Hardening added only when repeatable failure boundary emerges across independent runs.

### Execution Mode Proving Strategy

**Order 1: `plan_only` (lowest risk)**
- Workflow: `fast-local-diagnostic`
- Goal: Produce orchestration plan (Section 11) and exercise `validate-plan.py` live
- Risk: None (read-only, no mutation)
- Expected artifact: `plan_fast-local-diagnostic.md`

**Order 2: `prompt_chain` (low risk)**
- Workflow: `fast-local-diagnostic`
- Goal: Produce copy-paste prompts and exercise `validate-prompt-handoff.py` live
- Risk: None (read-only, no mutation)
- Expected artifacts: `prompt_handoff` with all sections validated

**Order 3: `guided_execution` full (medium risk)**
- Workflow: `docs-contract-reconciliation` (already started, Step 1 complete)
- Goal: Complete all 3 steps, exercise all gates with human approval
- Risk: Medium (requires gate approvals, potential data issues)
- Expected artifacts: `repository_sensemaking_brief`, `docs_contract_reconciliation_report`, `prompt_handoff`

**Order 4: `autonomous_execution` (medium risk)**
- Workflow: `fast-local-diagnostic`
- Goal: Exercise gates with automated approval (no human intervention)
- Risk: Medium (requires opt-in gate policy)
- Expected artifacts: All 2-step outputs with automated gate decisions

**Order 5: `yolo_execution` on new workflow (high risk)**
- Workflow: `full-local-sensemaking`
- Goal: Execute 4 steps end-to-end, bypass gates, exercise every core sensemaking skill
- Risk: High (full mutation, no gates, fast execution)
- Expected artifacts: Final `prompt_handoff` with all sensemaking outputs

---

## User Stories

1. As an automation engineer, I want to run `plan_only` mode and see a complete orchestration plan, so that I can understand what a workflow will do before executing it

2. As a workflow designer, I want to see `validate-plan.py` errors caught in live execution (not just fixtures), so that I can trust the validator to catch workflow definition errors

3. As a system operator, I want to execute `prompt_chain` mode and get copy-paste prompts for each skill, so that I can compose handoffs for downstream teams

4. As a reliability engineer, I want to execute `guided_execution` workflows with explicit gate approvals recorded in run logs, so that I have an audit trail of who approved what and when

5. As an automation engineer, I want to run `autonomous_execution` mode with automated gate approvals, so that I can unblock ci/cd pipelines without manual intervention

6. As a gate infrastructure maintainer, I want to see gate events (approval, denial, bypass, automated) documented in every run log, so that I can trust the gate system is working as designed

7. As a validator maintainer, I want to see all 5 Level-3 validators invoked on real artifacts in live runs, so that I can catch validator bugs early

8. As a hardening decision-maker, I want to see "repeatable failure boundaries" defined clearly (same failure class across 2+ independent runs), so that I know when to add systemic hardening vs. just fixing artifacts

9. As an orchestration engineer, I want to run multiple workflows in parallel and see aggregated results, so that I understand portfolio execution patterns

10. As a developer on this repo, I want the orchestration system to provide clear error messages when modes conflict with workflow definitions, so that I don't waste time debugging unexpected mode restrictions

11. As a CI/CD engineer, I want to integrate `autonomous_execution` mode into GitHub Actions, so that I can automatically run sensemaking workflows on PRs without human gates

12. As a product manager, I want to see all 5 execution modes proven across real project workflows (not just test fixtures), so that I know which modes are safe for customer use

---

## Implementation Decisions

### 1. Execution Mode Proving Order is Sequential, Not Parallel
**Decision**: Prove modes in order (plan_only → prompt_chain → guided → autonomous → yolo), not in parallel.

**Rationale**: Each mode builds on lessons from the previous. `plan_only` proves the plan validator. `prompt_chain` proves the prompt validator. `guided_execution` proves gate infrastructure. `autonomous_execution` proves automated gates. `yolo_execution` on a new workflow proves the full pipeline.

**Implementation**: Run orchestration-runner.py with each mode on designated workflows per the proving strategy above.

### 2. Repeatable Failure Boundary Requires 2+ Independent Runs
**Decision**: A failure class must occur in 2 or more independent runs to trigger systemic hardening.

**Rationale**: Single-run failures could be data-quality flukes (typo in artifact, artifact generated in unexpected state). Repeatability indicates a systemic gap that should be hardened.

**Implementation**: Track failure patterns in `analyze-run-failures.py`. When a failure recurs, flag it for hardening review.

### 3. Gate Infrastructure Must Record All Gate Events in Run Logs
**Decision**: Every run log must include `gate_decisions` section with fields: step, gate, result, timestamp, approved_by.

**Rationale**: Without complete gate audit trails, we can't verify the gate system works as designed or diagnose gate bugs.

**Implementation**: Run logs already support this. Ensure all gate types (approval, denial, bypass, automated) are exercised and recorded.

### 4. Validators Are "Live Exercised" Only When Invoked on Real Artifacts in Real Runs
**Decision**: Fixture tests don't count toward "proven" — only live run invocations count.

**Rationale**: Validators can have latent bugs that only surface on diverse real artifacts. Fixture tests are necessary but not sufficient.

**Implementation**: Track validator invocations in run logs. Each validator must have at least one live run invocation per mode before claiming "mode proven."

### 5. Input Artifact Passing Requires Either File-Based or Skill-Context-Based Approach
**Decision**: For now, workflows use file-based artifacts. Skills read from and write to the `artifacts/` directory per contracts. Future: skill invocation framework could pass artifact contents as context.

**Rationale**: File-based approach is stateless and portable. Context-based approach requires skill invocation framework not yet implemented.

**Implementation**: Skills follow artifact contracts (`ARTIFACT_CONTRACTS.md`). Orchestrator validates outputs against contracts.

---

## Testing Decisions

### What Makes a Good Test
- **Integration test**: Full workflow execution from step 1 to final artifact; exercises validators and gates; records decisions
- **Validator test**: Validator invoked on real artifact; both pass and fail cases tested
- **Gate test**: All gate types (approval, denial, bypass, automated) tested with proper audit trail

### Test Coverage

| Mode | Test Type | Artifact | Validator Stack | Gate Exercise | Run Log | Status |
|------|-----------|----------|-----------------|----------------|---------|--------|
| plan_only | Integration | plan.md | validate-plan.py | N/A | Yes | TODO |
| prompt_chain | Integration | prompt_handoff | validate-prompt-handoff.py | N/A | Yes | TODO |
| guided_execution | Integration | All 3-step outputs | All Level-2/3 | All gates approved | Yes | IN PROGRESS (1/3 steps done) |
| autonomous_execution | Integration | All 2-step outputs | All Level-2/3 | All gates automated | Yes | TODO |
| yolo_execution | Integration | Final output | All validators | Bypassed | Yes | DONE (fast-local-diagnostic) |

### Prior Art
- `test_orchestration_runner.py`: Fixture-based tests for plan generation, artifact resolution, validator dispatch
- `test_validator_utils.py`: Unit tests for validator behavior on positive and negative cases
- Run logs in `artifacts/run_log_*.md`: Live execution traces with decisions recorded

---

## Out of Scope

1. **Skill Invocation Framework**: Orchestrator doesn't invoke skills directly; skills are invoked externally (by Claude or other agents)
2. **Parallel Portfolio Execution**: Portfolio orchestrator exists but not proven in value-production runs
3. **Failure Recovery**: Auto-recovery on validator failures is out of scope; gates enable human intervention
4. **Custom Skill Development**: No new skills built in this phase; existing skills (to-prd, to-issues, triage, etc.) are used as-is
5. **Performance Optimization**: Execution speed is not a constraint; completeness and audit trails are
6. **Cloud Deployment**: All execution assumes local repository; CI/CD integration is future work

---

## Further Notes

### Critical Path to "Production Ready"
1. Prove `plan_only` mode (exercises validate-plan.py)
2. Prove `guided_execution` full cycle with approved gates
3. Prove `autonomous_execution` with automated approval
4. Define hardening policy based on repeatable failures observed
5. Prove remaining modes on additional workflows

### Key Metrics to Track
- **Mode Coverage**: % of modes with 1+ live run
- **Validator Coverage**: % of validators with 1+ live run invocation
- **Gate Coverage**: % of gate types (approval, denial, bypass, automated) recorded in real runs
- **Repeatable Failure Count**: # of distinct failure classes seen in 2+ independent runs

### Success Criteria
- All 5 execution modes proven via live runs
- All 5 Level-3 validators invoked on real artifacts in live execution
- All gate types exercised and recorded in run logs
- Repeatable failure boundary defined and zero repeatable failures currently blocking production use
- Complete audit trails in run logs (timestamps, decision-makers, reasons)
