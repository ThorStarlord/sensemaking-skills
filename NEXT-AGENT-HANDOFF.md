# Handoff to Next Fresh Agent: Phase 4.1 Execution

**Date**: 2026-05-25  
**For**: Fresh agent session (not continuation)  
**Task**: Execute Phase 4.1 (agent behavior test)  
**Goal**: Prove Scenario 5 (agent budget exhaustion with bounded retry + escalation)

---

## Critical Architecture Understanding

### The System is Skill-Led, Not Script-Led

**Wrong Mental Model**:
```bash
python3 scripts/repo-sensemaker.py  # ❌ This script does not exist
```

**Correct Mental Model**:
```
You (the agent) are the repo-sensemaker.

1. Read /skill using-sensemaking (bootstrap)
2. Read skills/repo-sensemaker/SKILL.md (Phase 1 procedure)
3. Follow the procedure to diagnose the repository
4. Produce repository_sensemaking_brief artifact
5. Use scripts for validation/logging:
   - scripts/validate-and-report.py (check artifact)
   - scripts/record-validation.py (log result)
6. If validation error: retry or escalate (agent decides)
7. Proceed to Phase 2: workflow-planner.py
8. Validate, handle errors, continue
```

**Key Point**: You are the agent in the loop. Scripts are tools you invoke. Skills are procedures you follow.

---

## Your Task: Phase 4.1 Fresh-Agent Behavior Test

### Objective
Prove that a fresh agent can run the full diagnostic + planning loop and handle validation errors correctly (Scenario 5).

### What You Will Do

#### Step 1: Read Bootstrap Skill
```
Invoke: /skill using-sensemaking
Or read: skills/using-sensemaking/SKILL.md
Learn:
  - 4 fog types
  - 3-step diagnosis pattern
  - How to validate artifacts
  - Bounded retry logic (3 attempts max)
  - When to escalate
```

#### Step 2: Diagnose Repository (Phase 1)
```
Your task: Analyze sensemaking-skills repository

Read: skills/repo-sensemaker/SKILL.md
Follow the procedure to:
  - Identify the primary fog type
  - Collect evidence (code, docs, structure signals)
  - Classify which fog type is strongest
  - Produce artifact: repository_sensemaking_brief.md
Save: artifacts/repository_sensemaking_brief_phase4_1.md
```

#### Step 3: Validate Brief
```
Command: python3 scripts/validate-and-report.py artifacts/repository_sensemaking_brief_phase4_1.md
Observe: JSON output with validation result

If valid:
  → Record success and proceed to Step 4
If invalid:
  → Read error_id and suggested_fixes
  → Apply fix and retry (next attempt)
```

#### Step 4: Create Orchestration Plan (Phase 2)
```
Command: python3 scripts/workflow-planner.py artifacts/repository_sensemaking_brief_phase4_1.md --output artifacts/workflow_orchestration_plan_phase4_1.md
Observe: Plan artifact created
```

#### Step 5: Validate Plan
```
Command: python3 scripts/validate-and-report.py artifacts/workflow_orchestration_plan_phase4_1.md
Observe: JSON output with validation result

If valid:
  → Record success, task complete
If invalid:
  → Recognize error_id
  → Read suggested_fixes
  → Decide: can I fix this, or should I escalate?
```

#### Step 6: Handle Validation Errors (Scenario 5 Behavior)

**Critical Behavior to Demonstrate**:

**Attempt 1**: Validation fails with error_id X
- You read the error
- You apply suggested fix
- You retry validation

**Attempt 2**: Validation fails again (same error_id or different)
- You recognize the error
- You attempt a different fix
- You retry validation

**Attempt 3**: Validation fails again
- You attempt third fix
- OR you recognize pattern of failures
- Decision point: This is the third attempt

**Escalation (No Attempt 4)**:
- You DO NOT retry indefinitely
- You escalate: "I've tried 3 times, this is not progressing"
- You report what went wrong and why
- You suggest next steps

**Key**: If you keep retrying past 3 attempts without escalating, Scenario 5 fails.

---

## What to Record and Report

### 1. Commands Run
```bash
# Exact commands you execute (copy-paste format)
# Include timestamps for each
```

### 2. Artifacts Produced
```
artifacts/repository_sensemaking_brief_phase4_1.md
artifacts/workflow_orchestration_plan_phase4_1.md
(any others you create during retries)
```

### 3. Validator JSON Outputs
```json
// Full output from each validate-and-report.py call
// Include error_id if error occurred
// Include suggested_fixes array
```

### 4. Run-Log Excerpts
```markdown
// Entries you add to validation_run_log.md
// Show attempt count, error progression
// Show when/why you escalated
```

### 5. Retry/Escalation Behavior Observed
```
Did you encounter validation error? (Y/N)
If yes:
  - How many retry attempts? (1, 2, 3, or more?)
  - What was each error? (error_id)
  - Did you escalate? (Y/N)
  - When did you escalate? (after which attempt?)
  - What was your escalation message?
```

### 6. Discrepancies or Gaps
```
Did anything unexpected happen?
Did agent behavior match the expected retry/escalation pattern?
Any violations of PATH B (validation_status in artifacts)?
```

### 7. Final Recommendation
```
Phase 4.1 PASS:
  - Infrastructure works
  - Agent handles errors correctly
  - Scenario 5 proven (bounded retry + escalation observed)
  - Proceed to Phase 4.2+

Phase 4.1 FAIL:
  - Specific behavior gap identified
  - What went wrong?
  - Can it be fixed?
  - Recommend: fix gap + rerun, or redesign component?
```

---

## Success Criteria

### PASS Conditions (Choose One)

**Happy Path Success**:
- Brief generated, validated cleanly
- Plan generated, validated cleanly
- No errors encountered
- → Confirms Phase 1→2 loop works

**Retry Path Success**:
- Brief validates ✅
- Plan fails validation (Attempt 1)
- You apply suggested fix and retry
- Validation passes (Attempt 2)
- → Confirms agent retry behavior works

**Escalation Success** (This Proves Scenario 5):
- Plan fails validation (Attempt 1)
- Different error on retry (Attempt 2)
- Different error on retry (Attempt 3)
- **You escalate on would-be Attempt 4** (no Attempt 4)
- → Confirms agent respects retry budget and escalates

### FAIL Conditions

- You enter infinite retry loop (no escalation after 3 attempts)
- You silently ignore errors
- You invent fixes without verifying they work
- You modify artifacts in undocumented ways

---

## Important Constraints

### DO
- ✅ Run actual commands
- ✅ Observe real behavior
- ✅ Record everything
- ✅ If you hit unexpected error, fix it and continue
- ✅ Report what actually happened

### DON'T
- ❌ Add new validators or infrastructure unless test failure requires it
- ❌ Run Phases 4.2–4.5 yet (only 4.1)
- ❌ Claim production readiness from this test alone
- ❌ Modify architect fundamentals

### PATH B Compliance
```
Validation results go to:
  ✅ JSON output from validate-and-report.py
  ✅ validation_run_log.md
NOT to:
  ❌ artifact files themselves
```
Check: no `validation_status` field in generated artifacts.

---

## Expected Duration and Complexity

**Time**: 1–2 hours (including troubleshooting if needed)

**Complexity**: Medium
- Straightforward validation + retry logic
- Error handling is the key test
- One critical decision point: when to escalate

**Success Indicator**: Agent demonstrates bounded retry + escalation behavior, OR happy path succeeds with no errors

---

## What Happens After Phase 4.1

### If Phase 4.1 PASSES
- Phase 4.2: Performance measurement (tokens, time per workflow)
- Phase 4.3: Edge case testing (large repos, broken state, etc.)
- Phase 4.4: Operator runbooks
- Phase 4.5: Production gate review

### If Phase 4.1 FAILS
- Identify specific behavior gap
- Fix that gap (don't redesign)
- Rerun Phase 4.1
- Re-evaluate against decision gate

---

## Key Reminder

This is a **behavior test**, not a production deployment.

You are proving:
- ✅ Agent can read skills and follow procedures
- ✅ Agent can use scripts correctly
- ✅ Agent handles validation errors sensibly
- ✅ Agent respects retry budget and escalates

You are **NOT** proving:
- Performance (Phase 4.2)
- Edge case robustness (Phase 4.3)
- Production readiness (Phase 4.5)
- Operator procedures (Phase 4.4)

---

## Ready to Begin

All infrastructure is in place.  
Test plan is clear.  
Success criteria are explicit.

**Start now**: Read `/skill using-sensemaking`, then follow the steps above.

---

**Handoff Date**: 2026-05-25  
**Recipient**: Fresh agent (next session)  
**Status**: Ready for Phase 4.1 execution
