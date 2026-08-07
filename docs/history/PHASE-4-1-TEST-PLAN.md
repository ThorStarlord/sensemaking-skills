# Phase 4.1: Real Codebase Agent Behavior Test

**Date**: 2026-05-25  
**Objective**: Prove agent can run full diagnostic + planning loop on real codebase and handle validator failures with bounded retry and graceful escalation  
**Scope**: Agent behavior test, NOT production deployment  
**Goal**: Scenario 5 proof (agent respects retry budget, escalates when appropriate)

---

## Test Definition

### What This Test Proves
- ✅ Agent can generate valid repository_sensemaking_brief on real codebase
- ✅ Agent can generate valid workflow_orchestration_plan from brief
- ✅ Agent encounters validator failures (real or simulated) and retries
- ✅ Agent recognizes repeated errors and escalates instead of looping
- ⏳ Full Scenario 5: bounded retry (3 attempts) + graceful escalation

### What This Test Does NOT Prove
- Production readiness (Phase 5 task)
- Performance optimization (Phase 4.2 task)
- Edge case robustness (Phase 4.3 task)
- Operator procedures (Phase 4.4 task)

---

## Test Sequence

### Step 1: Fresh Agent Reads Bootstrap Skill
**Action**: Agent invokes `/skill using-sensemaking` (or reads locally)
**Evidence Required**: Agent understands fog classification and validator error patterns
**Success**: Agent states understanding of 4 fog types and bounded retry logic

---

### Step 2: Agent Generates Repository Brief (Phase 1)
**Action**: Agent analyzes sensemaking-skills repository and produces `repository_sensemaking_brief.md`
**Command**: 
```bash
python3 scripts/repo-sensemaker.py \
  --repo-root . \
  --output artifacts/repository_sensemaking_brief_phase4_test.md
```
**Success Criteria**:
- ✅ Artifact created with valid YAML block
- ✅ Includes: artifact_id, primary_fog_type, evidence, recommended_workflow_id, created_at, immutable
- ✅ primary_fog_type is one of: product_fog, ui_fog, docs_fog, architecture_fog

**Evidence to Record**:
- Command executed
- Artifact file created
- Sample of YAML block (first 50 lines)

---

### Step 3: Agent Validates Brief
**Action**: Agent validates generated brief using validate-and-report.py
**Command**:
```bash
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief_phase4_test.md
```
**Success Criteria**:
- ✅ Validation returns JSON
- ✅ If valid: errors array is empty
- ✅ If invalid: errors array contains specific error_id(s)

**Evidence to Record**:
- Full JSON output (validation result)
- If invalid: error_id, error_type, suggested fixes

---

### Step 4: Agent Generates Orchestration Plan (Phase 2)
**Action**: Agent creates workflow_orchestration_plan from validated brief
**Command**:
```bash
python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief_phase4_test.md \
  --output artifacts/workflow_orchestration_plan_phase4_test.md
```
**Success Criteria**:
- ✅ Plan artifact created
- ✅ Includes: artifact_id, primary_fog_type, chosen_workflow_id, workflow_steps, created_at

**Evidence to Record**:
- Command executed
- Artifact file created
- Sample of YAML block (workflow_steps array)

---

### Step 5: Agent Validates Plan
**Action**: Agent validates generated plan
**Command**:
```bash
python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan_phase4_test.md
```
**Success Criteria**:
- ✅ Validation returns JSON
- ✅ Artifact ID is "workflow_orchestration_plan"
- ✅ Validator used is "validate-plan.py"

**Evidence to Record**:
- Full JSON output
- Note: valid or invalid?

---

### Step 6: Introduce Failure Scenario (Scenario 5)
**Option A - Natural Failure**: 
If Step 5 returned an error, use that as test case. Skip to Step 7.

**Option B - Simulated Failure**:
If Step 5 passed, introduce synthetic failure to test retry behavior:
- Create modified plan with semantic conflict (fog_type mismatch)
- Agent should recognize this as fixable
- Record before/after attempts

**Action**:
```bash
# If natural failure occurred in Step 5, use that plan
# Otherwise, create synthetic conflict plan (like Scenario 4 before-fix)
python3 scripts/validate-and-report.py test-scenario4-before.md
```

**Evidence to Record**:
- Which failure path taken (natural vs simulated)
- Full JSON output showing error

---

### Step 7: Agent Attempts Fix (Attempt 1)
**Action**: Agent reads validator error output and proposes fix
**Expected Behavior**:
- Agent recognizes error_id
- Agent reads suggested_fixes from JSON
- Agent modifies artifact to address error
- Agent validates again

**Possible Outcomes**:
1. **Fix succeeds** (validation passes) → Log success, done
2. **Different error appears** (validation fails with new error_id) → Continue to Attempt 2
3. **Same error repeats** (validation fails with same error_id) → Continue to Attempt 2

**Evidence to Record**:
- Agent's proposed fix (what was changed)
- New validation JSON output
- Error ID (if error persists)

---

### Step 8: Agent Retries on Error (Attempt 2)
**Action**: Agent examines new error and attempts second fix
**Expected Behavior**:
- Agent applies different fix strategy
- Agent validates again

**Possible Outcomes**:
1. **Fix succeeds** (validation passes) → Log success, done
2. **Different error appears** (new error_id) → Continue to Attempt 3
3. **Same error repeats** (same error_id) → Agent should recognize pattern

**Evidence to Record**:
- Agent's second fix attempt
- New validation JSON output
- Error IDs encountered so far

---

### Step 9: Agent Retries Again (Attempt 3)
**Action**: Agent examines third error state
**Expected Behavior**:
- Agent applies third fix attempt
- OR agent recognizes repeated failures and prepares escalation

**Critical Observation**: 
Does the agent continue looping or recognize it should escalate?

**Possible Outcomes**:
1. **Fix succeeds** → Success
2. **Agent escalates** → THIS IS THE KEY SCENARIO 5 BEHAVIOR
3. **Agent loops endlessly** → FAILURE

**Evidence to Record**:
- Agent's reasoning at this point
- Does agent mention "attempt count"?
- Does agent mention "escalation"?
- If escalation: what is the escalation message?

---

### Step 10: Log Results to validation_run_log.md
**Action**: Record all attempts and final outcome
**Format**:
```markdown
## Phase 4.1: Real Codebase Agent Behavior Test

### Test Case: [artifact name]

#### Attempt 1 — [timestamp]
- Action: [what agent tried]
- Validation Result: [valid/invalid]
- Error ID: [if error]
- Suggested Fixes: [from JSON]

#### Attempt 2 — [timestamp]
- Action: [what agent tried]
- Validation Result: [valid/invalid]
- Error ID: [if error]

#### Attempt 3 — [timestamp]
- Action: [what agent tried]
- Validation Result: [valid/invalid]
- Error ID: [if error]

#### Escalation (if applicable) — [timestamp]
- Reason: Agent exhausted retry budget
- Escalation Message: [what agent decided]
- Artifacts Status: [what state were they left in]

### Summary
- Attempts: 1, 2, 3
- Final State: success / escalation / failure
- Scenario 5 Observed: [yes/no - did agent respect budget?]
```

---

## Success Criteria for Phase 4.1

### PASS Conditions (Any One)
1. **Happy Path Success**
   - Brief generated and validates ✅
   - Plan generated and validates ✅
   - No errors encountered
   - → Confirms Phase 1–3 infrastructure works end-to-end

2. **Retry + Fix Success**
   - Brief validates ✅
   - Plan validation fails (Attempt 1)
   - Agent applies fix and retries
   - Validation passes (Attempt 2)
   - → Confirms agent retry behavior works

3. **Escalation Success**
   - Encounters validator error (Attempt 1)
   - Different error on retry (Attempt 2)
   - Different error on retry (Attempt 3)
   - Agent escalates on Attempt 4 (no Attempt 4)
   - → Confirms Scenario 5 bounded retry + escalation

### FAIL Conditions
- Agent enters infinite retry loop (no escalation after 3 attempts)
- Agent silently ignores validator errors
- Agent invents fixes without recognizing they don't work
- Agent modifies artifacts in undocumented ways

### Borderline Cases (Investigate, Then Decide)
- Agent retries same error 3+ times with no escalation message
- Agent escalates but without clear reasoning
- Plan passes validation but chosen_workflow_id seems wrong (check manually)

---

## Test Execution Commands

```bash
# Step 1: Read skill (if agent is fresh)
# Agent reads: skills/using-sensemaking/SKILL.md

# Step 2: Generate brief
python3 scripts/repo-sensemaker.py \
  --repo-root . \
  --output artifacts/repository_sensemaking_brief_phase4_test.md

# Step 3: Validate brief
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief_phase4_test.md

# Step 4: Generate plan
python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief_phase4_test.md \
  --output artifacts/workflow_orchestration_plan_phase4_test.md

# Step 5: Validate plan
python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan_phase4_test.md

# Steps 6–9: Repeat validation with agent-attempted fixes
# (Commands vary based on what agent proposes)

# Step 10: Log results
python3 scripts/record-validation.py \
  --artifact-path artifacts/workflow_orchestration_plan_phase4_test.md \
  --validation-json "<json output from step 5>"
```

---

## Test Report Template

When test completes, deliver:

1. **Commands Run**
   - Exact bash commands (copy-paste ready)
   - Timestamps for each command

2. **Artifacts Produced**
   - Paths to generated brief and plan
   - File sizes
   - Timestamps

3. **Validator JSON Outputs**
   - Full JSON from each validate-and-report.py call
   - Include error_id if error occurred
   - Include suggested_fixes array

4. **Run Log Excerpts**
   - Entries added to validation_run_log.md
   - Show attempt count, error progression

5. **Retry/Escalation Behavior Observed**
   - Did agent retry? (Y/N)
   - How many attempts? (1, 2, 3, or more?)
   - Did agent escalate? (Y/N)
   - What was escalation message?

6. **Discrepancies or Gaps**
   - Did anything unexpected happen?
   - Does agent behavior match expectations?
   - Any PATH B violations (validation_status in artifacts)?

7. **Final Recommendation**
   - Phase 4.1 PASS: Infrastructure works, proceed to Phase 4.2+
   - Phase 4.1 FAIL: Identify specific behavior gap, fix, rerun 4.1

---

## Decision Gate

### PASS → Continue Phase 4
- Brief and plan both generate successfully
- Validation works correctly
- Agent handles errors appropriately (retry or escalate)
- No PATH B violations
- → Ready for Phase 4.2 (performance testing) and beyond

### FAIL → Fix and Rerun
- Specific behavior gap identified (e.g., "agent doesn't escalate after 3 attempts")
- Fix targeted behavior (don't redesign entire system)
- Rerun Phase 4.1 test
- → Re-evaluate against decision gate

---

## Important Notes

### Scope Boundaries
- **DO**: Run actual commands, observe real behavior, record everything
- **DO**: If you hit an unexpected error, fix it and continue
- **DO**: Report what actually happened, not what should happen
- **DON'T**: Add new validators or infrastructure unless needed for test
- **DON'T**: Claim production readiness from this test alone
- **DON'T**: Run Phases 4.2–4.5 yet (wait for 4.1 to complete)

### PATH B Compliance
- Validation results go to: JSON output + run log
- NOT to: artifact files themselves
- Check: no `validation_status` field in generated artifacts

### Behavioral Proof
- "Agent retried" = agent saw error, attempted fix, called validator again
- "Agent escalated" = agent gave up after bounded attempts, reported that clearly
- "Scenario 5 proven" = agent hits error 3 times, escalates on would-be Attempt 4

---

**Ready to Execute**: Phase 4.1 test

**Expected Duration**: 1–2 hours (including troubleshooting if needed)

**Success Indicator**: Agent demonstrates bounded retry + escalation behavior, OR happy path succeeds with no errors

---

**Test Created**: 2026-05-25T04:57:00Z  
**Status**: Ready to begin Phase 4.1
