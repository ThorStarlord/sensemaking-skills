# Phase 1 Real-Agent Orchestration Test Execution Plan

## Test Scenarios

### Scenario 1: Happy Path (Valid Diagnosis)
- Agent reads bootstrap skill
- Agent diagnoses repository
- Produces valid brief
- Validation passes on first try
- Agent completes Phase 1

Expected: 1 validation attempt, VALID result

---

### Scenario 2: Auto-Fix Path (Missing Field)
- Agent diagnoses repository
- Produces brief with missing evidence
- Validation fails: logic_error
- Agent detects it's fixable
- Agent adds evidence and retries (Attempt 2)
- Validation passes

Expected: 2 validation attempts, Attempt 1 FAILED, Attempt 2 VALID

---

### Scenario 3: Escalation Path (Repeated Error)
- Agent diagnoses (Attempt 1)
- Validation fails with error_id X
- Agent retries (Attempt 2)
- Same error_id X appears
- Agent escalates instead of retrying blindly
- Agent presents structured escalation to user

Expected: Agent recognizes same error_id and escalates

---

### Scenario 4: Semantic Conflict (Workflow Routing)
- Agent diagnoses: primary_fog_type = product_fog
- Agent plans workflow: chosen_workflow_id = ui-implementation-workflow (wrong)
- Validation detects: semantic_conflict
- Agent corrects workflow choice
- Retry passes

Expected: semantic_conflict detected, agent fixes routing

---

### Scenario 5: Budget Exhaustion (3-Attempt Limit)
- Attempt 1: error (agent escalates if logic_error)
- Attempt 2: different error or retry (agent adapts)
- Attempt 3: still not fixed
- Agent escalates: "Tried 3 times, can't proceed"

Expected: Agent respects bounded retry limit

---

## Key Outputs to Capture

For each scenario, preserve:
1. Agent transcript (what it said/did)
2. repository_sensemaking_brief artifact
3. validate-and-report.py JSON output
4. validation_run_log.md entries
5. Any failures or behavior gaps

---

## Pass/Fail Criteria

### PASS Scenario 1
- [ ] Agent reads skill
- [ ] Agent diagnoses repo
- [ ] Produces valid brief
- [ ] validate-and-report.py returns valid=true
- [ ] record-validation.py logs entry
- [ ] Agent completes without errors

### PASS Scenario 2
- [ ] Attempt 1: validation fails with specific error_id
- [ ] Agent fixes the issue
- [ ] Attempt 2: validation passes
- [ ] Run log shows both attempts

### PASS Scenario 3
- [ ] Attempt 1: failure with error_id X
- [ ] Attempt 2: SAME error_id X appears
- [ ] Agent escalates instead of retrying
- [ ] Escalation message is structured and helpful

### PASS Scenario 4
- [ ] semantic_conflict detected
- [ ] Agent identifies routing problem
- [ ] Agent corrects workflow choice
- [ ] Retry passes

### PASS Scenario 5
- [ ] Attempt 1, 2, 3 executed
- [ ] Agent respects 3-attempt limit
- [ ] Agent escalates with summary

---

## Decision Gate

If ALL scenarios pass:
-> Phase 1 is agent-proven. Begin Phase 2.

If ANY scenario fails:
-> Identify the specific gap and fix.
-> Rerun the test.

---

Test Plan: docs/phase-1-real-agent-orchestration-test-plan.md
Milestone Criteria: docs/PHASE-1-NEXT-MILESTONE.md
Execution Date: 2026-05-24T23:57:42.852079
