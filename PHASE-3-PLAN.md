# Phase 3 Implementation Plan: Domain-Specific Workflows

**Date**: 2026-05-25  
**Phase Status**: Planning  
**Prior Phase**: Phase 2 complete (workflow-planner proven, Scenario 4 passing)

---

## Overview

Phase 3 implements and tests the four domain-specific implementation workflows that Phase 2's orchestration system will route to. These workflows take the diagnostic output from Phase 1 and execute concrete implementation work.

### What Phase 3 Delivers

1. **Four hardened implementation workflows**:
   - `product-implementation-workflow` (discovery → PRD → issues → implementation)
   - `ui-implementation-workflow` (flows → screens → issues → implementation)
   - `docs-implementation-workflow` (domain alignment → docs spec → handoff)
   - `architecture-implementation-workflow` (domain alignment → refactoring plan → handoff)

2. **Realistic failure scenarios for Scenario 5**:
   - Workflows that can fail and produce meaningful validation errors
   - Retry logic testing (3 attempts max)
   - Escalation testing (graceful handoff after max retries)

3. **End-to-end Phase 1 → Phase 2 → Phase 3 orchestration proof**:
   - Agent diagnoses repo → produces brief
   - Workflow-planner routes to implementation workflow
   - Implementation workflow executes steps
   - System logs results and confirms completion

---

## Critical Gap: Missing architecture-implementation-workflow

**Current State**:
- workflow-planner.py lines 18-23 reference "architecture-implementation-workflow" in routing logic
- workflow-registry.yaml does NOT define architecture-implementation-workflow
- Scenario 5 (Budget Exhaustion) will test this workflow's failure handling

**Action**: Add architecture-implementation-workflow to workflow-registry.yaml before Phase 3 implementation.

**Definition** (based on pattern of other implementation workflows):
```yaml
- id: architecture-implementation-workflow
  display_name: Architecture Implementation Workflow
  purpose: For architecture/refactoring problems. Aligns domain, creates refactoring spec, 
    decomposes into issues, and implements via TDD.
  initial_inputs:
  - id: context_artifacts
    type: artifact
    required: true
    description: Artifacts from sensemaking pipeline (problem-frame, unknowns-map,
      sensemaking-brief, orchestration-plan).
  allowed_execution_modes:
  - guided_execution
  - autonomous_execution
  requires_run_log: true
  steps:
  - id: 1
    skill: docs-aligner
    step_type: local_execution
    gate: review
    input_artifact: context_artifacts
    output_artifact: domain_alignment_report
    description: Domain alignment - refine understanding and create CONTEXT.md
  - id: 2
    skill: refactoring-planner
    step_type: local_execution
    gate: review
    input_artifact: domain_alignment_report
    output_artifact: refactoring_plan
    description: Architecture spec - define refactoring strategy and module boundaries
  - id: 3
    skill: to-issues
    step_type: local_execution
    gate: review
    input_artifact: refactoring_plan
    output_artifact: issue_list
    description: Implementation decomposition - break into issues
  - id: 4
    skill: triage
    step_type: local_execution
    gate: review
    input_artifact: issue_list
    output_artifact: agent_brief
    description: Issue preparation - create agent briefs
  - id: 5
    skill: tdd
    step_type: local_execution
    gate: review
    input_artifact: agent_brief
    output_artifact: code_patch
    description: Implementation - execute TDD cycles
  - id: 6
    skill: handoff
    step_type: local_execution
    gate: session_close
    input_artifact: code_patch
    output_artifact: session_summary
    description: Completion summary - document session
```

---

## Phase 3 Scope

### 3a: Registry Completion
1. Add architecture-implementation-workflow to workflow-registry.yaml
2. Verify all four implementation workflows are present and valid

### 3b: Implementation Workflow Hardening
Each workflow is already registered in workflow-registry.yaml with steps defined. Phase 3 validates:

**3b.1: product-implementation-workflow** (8 steps: docs-aligner → discovery → opportunity-tree → to-prd → to-issues → triage → tdd → handoff)
- Verify each step is properly routed
- Confirm input/output artifact expectations match artifact-contracts.yaml
- Test that discovery and opportunity-tree steps can produce realistic findings

**3b.2: ui-implementation-workflow** (7 steps: docs-aligner → ui-flow → ui-screen-spec → to-issues → triage → tdd → handoff)
- Verify UI-specific steps (ui-flow, ui-screen-spec) are properly defined
- Test screen spec generation from domain alignment
- Confirm TDD integration for UI components

**3b.3: docs-implementation-workflow** (3 steps: docs-aligner → to-prd → handoff)
- Shortest workflow path: validate minimal steps execute correctly
- Test docs-specific output generation
- Confirm handoff readiness

**3b.4: architecture-implementation-workflow** (6 steps: docs-aligner → refactoring-planner → to-issues → triage → tdd → handoff)
- NEW: Add to registry, define refactoring-planner skill expectations
- Test architecture-focused specification generation
- Verify code decomposition and TDD integration

### 3c: Scenario 5 Testing (Budget Exhaustion)
Create realistic failure scenarios where workflows encounter issues:

**Test Case 5.1: Missing Input Artifact**
- Orchestration plan specifies step that requires artifact X
- Artifact X is not produced by previous step
- Validation detects missing_field error
- Agent attempts fix (Attempt 1 fails)
- Retries with correction (Attempt 2 fails differently)
- Retries again (Attempt 3 fails)
- Agent escalates gracefully after 3 attempts

**Test Case 5.2: Semantic Conflict in Workflow**
- Step produces artifact type A, but next step expects type B
- Validator detects type_error
- Agent recognizes incompatibility and escalates after 3 attempts

**Test Case 5.3: Logic Error in Workflow Output**
- Step produces artifact with incomplete data (e.g., empty issue list)
- Validation detects logic_error
- Agent applies fixes and retries
- After 3 attempts, escalates with clear error context

### 3d: End-to-End Testing
Chain Phase 1 → Phase 2 → Phase 3:
1. Agent reads using-sensemaking skill
2. Agent diagnoses repository → produces brief (Phase 1)
3. workflow-planner routes to implementation workflow → produces plan (Phase 2)
4. Implementation workflow executes selected workflow → produces results (Phase 3)
5. Validation confirms all artifacts are valid
6. Logging captures complete execution trace

---

## Implementation Order

### Task 3.1: Add architecture-implementation-workflow to Registry
**File**: `skills/workflow-planner/references/workflow-registry.yaml`  
**Changes**:
- Insert architecture-implementation-workflow definition (lines ~590, before skill-evaluation-workflow)
- Validate YAML syntax
- Verify all 4 implementation workflows are present
- Test workflow-planner routing with architecture_fog input

### Task 3.2: Verify Implementation Workflow Definitions
**Files to check**:
- `skills/workflow-planner/references/workflow-registry.yaml` — each workflow has all required steps
- `skills/workflow-planner/references/artifact-contracts.yaml` — all input/output artifacts defined
- Verify skill references in each step exist or have stubs

**Success criteria**:
- ✅ All 4 workflows present in registry
- ✅ All steps have input_artifact, output_artifact, gate, description
- ✅ Artifact contracts match expected inputs/outputs
- ✅ No broken references (skills that don't exist)

### Task 3.3: Create Scenario 5 Test Fixtures
**Files to create**:
- `test-results/phase3/scenario5-fixtures/` directory
- Multiple test artifacts designed to trigger failures
- Test manifest documenting expected failure modes

**Test fixture types**:
1. Missing artifact dependency (breaks orchestration)
2. Type mismatch (wrong artifact type produced)
3. Logic error (incomplete data in artifact)
4. Repeated error (same validation error on retry)

### Task 3.4: Execute Scenario 5 Testing
**Process**:
1. Use validate-and-report.py on each test fixture
2. Simulate agent retrying 3 times
3. Verify escalation occurs after Attempt 3
4. Log results to validation_run_log.md

**Expected output**:
- validation_run_log.md records Scenario 5 execution
- Shows Attempts 1-3 with different/same error_ids
- Shows graceful escalation message

### Task 3.5: End-to-End Phase 1→2→3 Test
**Process**:
1. Fresh agent session invokes using-sensemaking skill
2. Agent diagnoses repository (Phase 1)
3. Agent invokes workflow-planner (Phase 2)
4. Agent executes selected implementation workflow (Phase 3)
5. System validates and logs results

**Success criteria**:
- ✅ Brief produced and validates
- ✅ Plan produced and validates
- ✅ Workflow executes selected steps
- ✅ All artifacts exist and are valid
- ✅ validation_run_log.md captures complete trace

---

## Critical Files and Modifications

| File | Change | Status |
|------|--------|--------|
| `skills/workflow-planner/references/workflow-registry.yaml` | Add architecture-implementation-workflow | Task 3.1 |
| `PHASE-3-COMPLETE.md` | Document Phase 3 completion and Scenario 5 results | Task 3.5 |
| `validation_run_log.md` | Append Scenario 5 execution records | Task 3.4 |
| `PHASE-3-PLAN.md` | This file | Planning |

---

## Success Criteria for Phase 3

- ✅ architecture-implementation-workflow added to registry
- ✅ All 4 implementation workflows properly defined with steps
- ✅ All artifact contracts match workflow expectations
- ✅ Scenario 5 (Budget Exhaustion) execution → validation detects failures → agent escalates gracefully after 3 attempts
- ✅ validation_run_log.md captures Scenario 5 execution with attempt records
- ✅ End-to-end Phase 1 → Phase 2 → Phase 3 test passes
- ✅ PHASE-3-COMPLETE.md documents all results

---

## Phase 4 Readiness (Post-Phase 3)

Once Phase 3 is complete:
- Implementation workflows are proven (Scenarios 5 passes)
- Agent orchestration loop works end-to-end
- System can diagnose and route to implementation

**Phase 4 begins with**: Real codebase integration testing and production hardening.
- Test on actual sensemaking-skills repository
- Verify workflow execution produces meaningful artifacts
- Measure time and cost (token budget) for each workflow
- Identify optimization opportunities

---

**Next action**: Execute Task 3.1 (Add architecture-implementation-workflow to registry)
