# Scenario 5: Budget Exhaustion - Test Manifest

**Date**: 2026-05-25  
**Purpose**: Test bounded retry logic (3 attempts max) and graceful escalation

---

## Overview

Scenario 5 verifies that agents escalate gracefully when workflow validation failures exceed 3 attempts. Each test fixture is designed to trigger a specific validation error that will persist across retries.

---

## Test Fixtures

### Fixture 5.1: Missing Workflow Steps (workflow_steps null)

**File**: `orchestration_plan_s5_fixture1.md`

**What it tests**:
- Validation catches `workflow_steps` field is null (required field)
- Error type: `missing_field`
- Error ID: `workflow_orchestration_plan.workflow_steps.missing_field`

**Expected behavior**:
- Attempt 1: validate-and-report.py detects missing_field error
- Attempt 2: agent adds empty array, validation detects logic_error (empty)
- Attempt 3: agent adds placeholder steps, validation detects type_error
- Attempt 4 (escalation): agent recognizes pattern of failures, escalates

**Success criteria**:
- validation_run_log.md shows 3 attempts with different error_ids
- Attempt 4 is escalation message, not retry attempt

---

### Fixture 5.2: Empty Workflow Steps (workflow_steps empty array)

**File**: `orchestration_plan_s5_fixture2.md`

**What it tests**:
- Validation catches `workflow_steps` array is empty (must have at least 1 step)
- Error type: `logic_error`
- Error ID: `workflow_orchestration_plan.workflow_steps.logic_error`

**Expected behavior**:
- Attempt 1: validate-and-report.py detects logic_error (empty array)
- Attempt 2: agent adds first step, validation detects incomplete_step
- Attempt 3: agent adds more steps, validation detects another error
- Attempt 4 (escalation): agent escalates after 3 failed attempts

**Success criteria**:
- Each attempt produces validation error
- Escalation occurs on Attempt 4 (no further retries)
- Log shows all error_ids encountered

---

### Fixture 5.3: Semantic Conflict (fog_type != chosen_workflow)

**File**: `orchestration_plan_s5_fixture3.md`

**What it tests**:
- Validation detects fog_type (architecture_fog) doesn't match chosen_workflow (product-implementation-workflow)
- Error type: `semantic_conflict`
- Error ID: `workflow_orchestration_plan.chosen_workflow_id.semantic_conflict`

**Expected behavior**:
- Attempt 1: validate-and-report.py detects semantic_conflict
  - Suggests: "Change chosen_workflow_id to architecture-implementation-workflow OR set routing_decision_method to manual_override"
- Attempt 2: agent changes routing_decision_method to manual_override, validation passes
  - OR agent changes chosen_workflow_id to match fog_type
  - Either change should resolve the conflict
- Attempt 3: not needed if Attempt 2 succeeds

**Alternative behavior** (if agent keeps trying same fix):
- Attempt 1: semantic_conflict error
- Attempt 2: agent applies wrong fix, same error appears
- Attempt 3: agent recognizes repeated error_id, escalates before Attempt 4

**Success criteria**:
- semantic_conflict error is detected
- Error message suggests specific fixes
- Agent applies a fix by Attempt 2 (or recognizes repeated error by Attempt 3)

---

## Test Execution Plan

### Phase 1: Run Each Fixture
```bash
# Attempt 1: Initial validation
python3 scripts/validate-and-report.py test-results/phase3/scenario5-fixtures/orchestration_plan_s5_fixture1.md

# This produces JSON output with validation errors
# Log the result as "Attempt 1" in validation_run_log.md
```

### Phase 2: Simulate Agent Retry
Agent reads the error JSON and decides how to fix it.

**If error is fixable** (missing field, unknown value):
- Agent modifies artifact to address the error
- Invoke validation again

**If error is repeated** (same error_id on Attempt 2 and 3):
- Agent recognizes escalation pattern
- Agent escalates instead of retrying Attempt 4

### Phase 3: Log Results
Append to `validation_run_log.md`:
```
## Scenario 5 Execution (Fixture 5.1)

Artifact: orchestration_plan_s5_fixture1
Validator: validate-plan.py

### Attempt 1
Error ID: workflow_orchestration_plan.workflow_steps.missing_field
Error Message: workflow_steps field is required and must be non-null

### Attempt 2
[After agent fix]
Error ID: workflow_orchestration_plan.workflow_steps.logic_error
Error Message: workflow_steps array must have at least 1 step

### Attempt 3
[After agent fix]
Error ID: workflow_orchestration_plan.workflow_steps.unknown_value
Error Message: workflow_steps[0].skill = "invalid_skill" is not defined

### Escalation (No Attempt 4)
Agent escalated after 3 attempts with continuing errors.
Recommended next step: Review workflow-registry.yaml to understand valid skill names.
```

---

## Success Criteria for Scenario 5

- ✅ Fixture 5.1 triggers at least 3 different validation attempts
- ✅ Fixture 5.2 triggers logic_error that persists across retries
- ✅ Fixture 5.3 triggers semantic_conflict error with clear suggestions
- ✅ Agent respects 3-attempt limit before escalating
- ✅ Escalation message includes:
  - All error_ids seen
  - Error context
  - Suggested next steps or resolution paths
- ✅ validation_run_log.md captures all attempts and escalation
- ✅ No Attempt 4 (or if Attempt 4 exists, it's escalation message, not retry)

---

## Expected Outcomes

### Scenario 5a: Fixture 5.1 (Missing Field)
- Attempts: 1-3 with different errors
- Resolution: Agent recognizes proper YAML structure needed
- Escalation: On Attempt 4 if issues persist

### Scenario 5b: Fixture 5.2 (Empty Array)
- Attempts: 1-3 with logic_error initially
- Resolution: Agent adds steps, but each step may have new errors
- Escalation: After 3 attempts if fundamental issue remains

### Scenario 5c: Fixture 5.3 (Semantic Conflict)
- Attempts: 1-2 typically (conflict is solvable)
- Resolution: Agent fixes fog_type mismatch
- Success: Attempt 2 should validate OK
- Escalation: Only if agent applies wrong fix twice

---

## Assumptions

1. **validate-and-report.py** correctly routes to validate-plan.py
2. **validate-plan.py** correctly detects errors and returns proper error_ids
3. **Agent** reads JSON output and attempts intelligent fixes
4. **Agent** recognizes when same error appears twice (escalation trigger)
5. **record-validation.py** correctly logs attempts to validation_run_log.md

---

## Files to Check

- `validation_run_log.md` — Append Scenario 5 execution records
- `scripts/validate-plan.py` — Error detection logic
- `scripts/validate-and-report.py` — Error routing
- `scripts/record-validation.py` — Logging

---

**Ready to execute**: Phase 3 testing infrastructure complete.
