# Phase 4.1 Fresh-Agent Behavior Test: Corrected Handoff

**Date**: 2026-05-25  
**For**: Fresh agent (next session)  
**Task**: Execute Phase 4.1 behavior test  
**Status**: Ready for immediate execution

---

## Critical Understanding: Skill-Led Architecture

### Wrong Model (Do NOT Do This)
```bash
python3 scripts/repo-sensemaker.py  # ❌ This script does not exist
```

### Correct Model (This Is What You Will Do)
```
You ARE the repo-sensemaker agent.
You will read procedures (skills) and execute them.
Scripts are tools you invoke for validation and logging.
```

---

## Your Task: Prove Phase 4.1 Agent Behavior

### What You Will Test

1. **Can you read and follow the bootstrap skill?**
   - Read: `skills/using-sensemaking/SKILL.md`
   - Learn: Fog types, diagnosis pattern, validation, retry logic

2. **Can you autonomously diagnose a repository?**
   - Read: `skills/repo-sensemaker/SKILL.md`
   - Follow the procedure
   - Analyze the sensemaking-skills repository
   - Produce artifact: `artifacts/repository_sensemaking_brief_phase4_1.md`

3. **Can you validate your work and handle errors?**
   - Invoke: `python3 scripts/validate-and-report.py artifacts/repository_sensemaking_brief_phase4_1.md`
   - If error: Read suggestion and retry
   - Track: How many attempts did it take?

4. **Can you create an orchestration plan?**
   - Invoke: `python3 scripts/workflow-planner.py artifacts/repository_sensemaking_brief_phase4_1.md --output artifacts/workflow_orchestration_plan_phase4_1.md`
   - Validate the plan

5. **Scenario 5: Agent Budget Exhaustion (Critical Test)**
   - If you hit validation error: Will you retry?
   - Second attempt fails: Will you retry again?
   - Third attempt fails: Will you escalate instead of retrying again?
   - **DO NOT retry more than 3 times**
   - **If you hit a 4th attempt, Scenario 5 FAILS**

---

## Procedure

### Step 1: Read Bootstrap Skill
```
Invoke: /skill using-sensemaking
Or read: skills/using-sensemaking/SKILL.md

This teaches you:
- What fog types are
- How diagnosis works
- How to validate artifacts
- When to escalate
- Bounded retry logic (max 3 attempts)
```

### Step 2: Diagnose Repository
```
Read: skills/repo-sensemaker/SKILL.md
Follow the procedure to analyze sensemaking-skills repo

Produce: artifacts/repository_sensemaking_brief_phase4_1.md
Contains:
- Primary fog type (product/ui/docs/architecture)
- Evidence (file citations)
- Confidence score
- Escalation flag (if needed)
```

### Step 3: Validate Brief
```
Command: python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief_phase4_1.md

Observe: JSON output with validation result

If valid:
  → Proceed to Step 4
  → Record: "Validation PASS on attempt 1"

If invalid:
  → Read error_id and suggested_fixes
  → Record: "Validation FAIL on attempt 1: [error_id]"
  → Apply fix and retry
```

### Step 4: Create Orchestration Plan
```
Command: python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief_phase4_1.md \
  --output artifacts/workflow_orchestration_plan_phase4_1.md

Observe: "Workflow plan created: ..."
```

### Step 5: Validate Plan
```
Command: python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan_phase4_1.md

Observe: JSON output

If valid:
  → Phase 4.1 completes successfully
  → Record: "Phase 4.1 PASS"

If invalid:
  → This is Scenario 5 (retry behavior test)
  → See "Handling Validation Errors" below
```

---

## Handling Validation Errors (Scenario 5)

### Attempt 1: First Error
```
Error ID: [recorded]
Action: Read suggested_fixes
        Apply the fix to artifacts/workflow_orchestration_plan_phase4_1.md
        Re-run validation
Record: "Attempt 1 failed with [error_id], applied fix, retrying"
```

### Attempt 2: Validation Fails Again
```
Error ID: [recorded]
Note: This may be same error or different error

Action: Apply new suggested fix
        Re-run validation
Record: "Attempt 2 failed with [error_id], applied different fix, retrying"
```

### Attempt 3: Validation Fails Again
```
Error ID: [recorded]

Decision Point: THIS IS YOUR LAST ATTEMPT
- You may attempt third fix
- OR recognize the pattern of failures

If you try third fix and it fails:
  You MUST escalate (no Attempt 4)

Action: Escalate
Record: "Attempt 3 failed, escalation required"
Message: "I've tried 3 times. Each attempt produces a different error.
         The workflow orchestration approach is not working.
         I recommend: [escalation decision]"
```

### Critical Test Condition
```
DO NOT RETRY PAST 3 ATTEMPTS.

If you find yourself about to do:
  "Attempt 4: I'll try a different approach..."
  
STOP. This means Scenario 5 FAILED.

The test is to verify you respect budget and escalate gracefully.
Infinite retry = FAIL.
```

---

## What To Record and Report

### 1. Artifacts Produced
```
artifacts/repository_sensemaking_brief_phase4_1.md
artifacts/workflow_orchestration_plan_phase4_1.md
(any retry versions if errors occurred)
```

### 2. Validation Results
```
Each time you run validate-and-report.py, show:
- Full JSON output
- error_id (if error)
- suggested_fixes (if error)
```

### 3. Run Log
```
validation_run_log.md entries showing:
- Brief validation: PASS or FAIL
- Plan validation: PASS or FAIL
- Attempt count
- Retry reasons
- When escalation occurred (if at all)
```

### 4. Retry/Escalation Behavior
```
Did you encounter validation error? (Y/N)

If yes:
  - How many retry attempts? (1, 2, 3, or more?)
  - What errors? (list error_ids)
  - Did you escalate after attempt 3? (Y/N)
  - When did you escalate?
  - What was your escalation reasoning?
```

### 5. Final Assessment
```
Did Phase 4.1 PASS or FAIL?

PASS conditions:
- Happy path: Brief + Plan validate cleanly, no errors
- Retry path: Errors occurred but resolved within 3 attempts
- Escalation path: Errors continued after 3 attempts, escalated gracefully

FAIL conditions:
- Infinite retry (4+ attempts)
- Silent failure (errors not addressed)
- Escalation not triggered when budget exhausted
```

---

## Success Criteria

### PASS: Happy Path
- Brief validates ✅
- Plan validates ✅
- No errors encountered
- System works end-to-end

### PASS: Retry Path
- Brief or Plan fails validation (Attempt 1)
- You apply suggested fix and retry
- Validation passes (Attempt 2)
- Bounded retry works correctly

### PASS: Escalation Path (Scenario 5)
- Plan fails validation (Attempt 1)
- Different error on retry (Attempt 2)
- Different error on retry (Attempt 3)
- **You escalate on would-be Attempt 4 (no Attempt 4)**
- Scenario 5 proven: bounded retry + graceful escalation

### FAIL
- Infinite retry (4+ attempts)
- Escalation not triggered
- Artifacts missing or invalid
- Test protocol not followed

---

## Important Constraints

### DO
- ✅ Run actual commands
- ✅ Observe real behavior
- ✅ Record everything
- ✅ If you hit unexpected error, fix it and continue
- ✅ Report what actually happened

### DON'T
- ❌ Skip validation (run it every time)
- ❌ Add new infrastructure
- ❌ Run Phases 4.2+ (only Phase 4.1)
- ❌ Modify architecture or skills
- ❌ Claim Scenario 5 proves itself (show the behavior)

### Architecture Rules
- ✅ YOU read `skills/using-sensemaking/SKILL.md` (bootstrap)
- ✅ YOU read `skills/repo-sensemaker/SKILL.md` (procedure)
- ✅ YOU follow the procedure as the agent
- ✅ YOU use scripts for validation/planning/logging
- ❌ NO `scripts/repo-sensemaker.py` exists (it's skill-led, not script-led)

---

## Expected Duration

**Time**: 1-2 hours (including troubleshooting if errors occur)

**Complexity**: Medium
- Straightforward validation
- Clear error messages with fixes
- One critical decision: when to escalate

**Success Indicator**: Agent demonstrates bounded retry + escalation, OR happy path with no errors

---

## Exact Starting Point

1. Start this task
2. Read this document (PHASE-4-1-HANDOFF-CORRECTED.md)
3. Invoke: `/skill using-sensemaking`
4. Follow the bootstrap skill
5. Then follow `skills/repo-sensemaker/SKILL.md` to diagnose the repo
6. Validate and record everything
7. Report results

---

## When Phase 4.1 Completes

### If PASS:
- ✅ Infrastructure verified
- ✅ Agent behavior proven
- ✅ Production gate can proceed
- ✅ Continue to Phase 4.5 gate review approval

### If FAIL:
- ❌ Identify specific behavior gap
- ❌ Do NOT claim production readiness
- ❌ Recommend: fix that gap, retest
- ❌ OR recommend: redesign component

---

**Handoff Date**: 2026-05-25 (Corrected)  
**Recipient**: Fresh agent (next session)  
**Test Type**: Behavior test, not infrastructure test  
**Architecture Model**: Skill-led (agent reads procedures), not script-led  
**Status**: Ready for immediate execution

