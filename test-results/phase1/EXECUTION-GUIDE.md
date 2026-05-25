# Phase 1 Real-Agent Orchestration Test - Execution Guide

## Before You Start

1. Open fresh Claude Code / Cursor session
2. No prior context about sensemaking-skills
3. SessionStart hook will surface the bootstrap skill automatically

---

## Scenario 1: Happy Path

### User Task
"Diagnose this repository using sensemaking-skills.
Read the bootstrap skill if you haven't seen it yet.
Follow the three-step diagnosis pattern."

### What Agent Should Do
1. Read skills/using-sensemaking/SKILL.md
2. Invoke repo-sensemaker skill
3. Produce repository_sensemaking_brief
4. Call python3 scripts/validate-and-report.py
5. Get valid=true response
6. Call python3 scripts/record-validation.py
7. Complete Phase 1

### Capture
- [ ] Agent transcript
- [ ] repository_sensemaking_brief artifact
- [ ] validate-and-report.py JSON response
- [ ] validation_run_log.md entry
- [ ] Final summary from agent

### Pass Criteria
- Agent completes without errors
- Validation returns valid=true
- Run log has 1 entry with VALID result

---

## Scenario 2: Auto-Fix Path

### Setup
Same as Scenario 1, but the agent initially misses the evidence section.

### What Agent Should Do
1. Diagnose (Attempt 1)
2. Validate -> error_id: repository_sensemaking_brief.evidence.logic_error
3. Agent recognizes: "logic_error, needs re-analysis"
4. Agent re-reads codebase, adds evidence
5. Retry (Attempt 2)
6. Validate -> valid=true
7. Complete

### Capture
- [ ] Both validation attempts in run-log
- [ ] error_id appears in both (shows tracking)
- [ ] Attempt 2 result is VALID
- [ ] Agent's reasoning for fix

### Pass Criteria
- Attempt 1 fails with specific error_id
- Attempt 2 passes
- Agent doesn't retry blindly, solves the problem

---

## Scenario 3: Escalation Path

### Setup
Repository where same error repeats.

### What Agent Should Do
1. Attempt 1: diagnose, validate -> error_id: X
2. Attempt 2: agent retries, validate -> error_id: X (SAME)
3. Agent detects: "same error came back, don't retry"
4. Agent escalates to user
5. User provides input or guidance
6. Attempt 3: retry with user context
7. Complete or escalate again

### Capture
- [ ] Both error_ids in run-log (showing they're the same)
- [ ] Agent's escalation message
- [ ] User input
- [ ] Attempt 3 result

### Pass Criteria
- Agent escalates on repeat error, doesn't retry blindly
- Escalation message includes error_id, message, suggested_fixes
- Agent respects bounded retry

---

## Scenario 4: Semantic Conflict

### Setup
Repository where fog type doesn't match workflow choice.

### What Agent Should Do
1. Diagnose brief: primary_fog_type = product_fog [OK]
2. Plan workflow: chosen_workflow_id = ui-implementation-workflow [WRONG]
3. Validate plan -> semantic_conflict detected
4. Agent recognizes: "workflow routing mismatch"
5. Agent corrects to: product-implementation-workflow
6. Retry -> valid=true

### Capture
- [ ] Semantic conflict detection in validation JSON
- [ ] Agent's decision to correct workflow
- [ ] Retry result

### Pass Criteria
- semantic_conflict error_type detected
- Agent understands it's a routing error
- Agent fixes workflow choice
- Retry passes

---

## Scenario 5: Budget Exhaustion

### Setup
Repository with unfixable issue.

### What Agent Should Do
1. Attempt 1: diagnose, validate -> error (logic_error)
2. Attempt 2: retry with different approach -> error (different error_id)
3. Attempt 3: retry again -> still not valid
4. Agent escalates: "Tried 3 times, still stuck"

### Capture
- [ ] 3 validation attempts in run-log
- [ ] Different error_ids across attempts
- [ ] Agent respects 3-attempt limit
- [ ] Escalation summary

### Pass Criteria
- Agent respects bounded retry (max 3)
- Agent escalates with summary
- No infinite loops or retry past 3

---

## Recording Results

After each scenario, create a result entry in results/test-results.json:
- scenario: 1
- status: passed
- attempts: [list of validation attempts]
- artifact_path: artifacts/repository_sensemaking_brief.md
- validation_result.valid: true
- notes: Agent successfully completed Phase 1 on first try

---

## Final Deliverable

After all scenarios, produce:

1. Test execution transcript (what agent did)
2. Artifacts (briefs, plans, validation outputs)
3. Run-log (validation_run_log.md)
4. Results JSON (structured test results)
5. Recommendation (Phase 1 agent-proven or needs fixes)

---

## Decision Gate

PASS -> Phase 1 is agent-proven. Begin Phase 2.
FAIL -> Fix the identified gap, rerun the scenario.

---

Execution Date: 2026-05-24T23:57:42.852079
