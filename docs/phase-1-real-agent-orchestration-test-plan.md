# Phase 1: Real-Agent Orchestration Test Plan

**Purpose**: Verify that a fresh agent can use Phase 1 end-to-end, not just that scripts pass tests  
**Scope**: Agent behavior + script integration (not Phase 2 workflows)  
**Success Criteria**: Agent successfully diagnoses a repository, validates output, handles errors, and escalates gracefully  

---

## Test Flow Overview

```
Fresh Agent Session
    ↓
SessionStart Hook Surfaces using-sensemaking
    ↓
Agent Reads Bootstrap Skill
    ↓
Agent Understands Fog Classification + Retry Logic
    ↓
Agent Initiates Diagnosis (invoke repo-sensemaker)
    ↓
Agent Produces repository_sensemaking_brief
    ↓
Agent Validates with validate-and-report.py
    ↓
Agent Handles Result:
  ├─ If valid → Logs and completes Phase 1
  ├─ If invalid (missing field) → Auto-fixes and retries
  ├─ If semantic conflict → Reasons and fixes
  ├─ If logic_error or same error repeats → Escalates
  └─ After 3 attempts → Escalates to user
    ↓
Agent Records All Attempts to validation_run_log.md
    ↓
Agent Reports Final State
```

---

## Test Scenarios

### Scenario 1: Happy Path (Valid Diagnosis)
**Setup**: Fresh agent, repository with clear primary fog type signals  
**Expected Flow**:
1. Agent reads skill
2. Agent diagnoses repo
3. Produces brief with clear evidence
4. validate-and-report.py returns valid=true
5. record-validation.py logs entry
6. Agent completes Phase 1
7. Agent recommends next workflow

**Pass Criteria**:
- ✅ Agent produces valid brief
- ✅ Validation passes
- ✅ Run log has entry with VALID result
- ✅ No errors during process

---

### Scenario 2: Auto-Fix Path (Missing Field)
**Setup**: Fresh agent, repository where initial brief is missing evidence  
**Expected Flow**:
1. Agent diagnoses repo
2. Produces brief without evidence section
3. validate-and-report.py returns error_id: `repository_sensemaking_brief.evidence.logic_error`
4. Agent recognizes: "logic_error → needs re-analysis"
5. Agent re-reads codebase, adds evidence
6. Agent retries (Attempt 2)
7. validate-and-report.py returns valid=true
8. Agent completes Phase 1

**Pass Criteria**:
- ✅ First validation fails with specific error_id
- ✅ Agent detects it's fixable (logic_error)
- ✅ Agent retries with improved evidence
- ✅ Second validation passes
- ✅ Run log shows 2 entries (Attempt 1 FAILED, Attempt 2 VALID)
- ✅ error_id same in both entries (proof of tracking)

---

### Scenario 3: Escalation Path (Repeated Error)
**Setup**: Fresh agent, repository where same error repeats across retries  
**Expected Flow**:
1. Agent diagnoses repo (Attempt 1)
2. Validation fails: error_id = `repository_sensemaking_brief.primary_fog_type.missing_field`
3. Agent auto-fixes (Attempt 2)
4. Validation fails again: error_id = `repository_sensemaking_brief.primary_fog_type.missing_field` (SAME)
5. Agent detects: "Same error came back → don't retry again"
6. Agent escalates to user with structured info
7. User provides context or guidance
8. Agent retries with user input (Attempt 3)

**Pass Criteria**:
- ✅ Attempt 1: failure with error_id
- ✅ Attempt 2: failure with SAME error_id
- ✅ Agent escalates instead of retrying blindly
- ✅ Escalation message includes error_id, message, suggested_fixes
- ✅ Run log shows all 3 attempts with error_id tracking

---

### Scenario 4: Semantic Conflict Path (Workflow Routing)
**Setup**: Fresh agent, repository where fog type doesn't align with workflow choice  
**Expected Flow**:
1. Agent diagnoses repo
2. Produces brief: primary_fog_type = "product_fog"
3. Agent then plans workflow (workflow-planner)
4. Agent chooses: chosen_workflow_id = "ui-implementation-workflow"
5. validate-and-report.py detects: semantic_conflict between product_fog and ui-implementation-workflow
6. Agent recognizes: "This is a routing error, not a content error"
7. Agent corrects workflow choice to "product-implementation-workflow"
8. Retries validation
9. validate-and-report.py returns valid=true

**Pass Criteria**:
- ✅ Semantic conflict detected with error_type="semantic_conflict"
- ✅ Agent understands it's a routing problem
- ✅ Agent fixes workflow choice
- ✅ Retry passes
- ✅ Run log shows both attempts

---

### Scenario 5: Budget Exhaustion (3 Attempts Limit)
**Setup**: Fresh agent, repository with unfixable issue (requires human judgment)  
**Expected Flow**:
1. Agent diagnoses repo (Attempt 1)
2. Validation fails: logic_error (unfixable by agent)
3. Agent detects: "logic_error → escalate immediately"
4. Agent escalates to user
5. User provides guidance
6. Agent retries with user input (Attempt 2)
7. Still fails with different error
8. Agent retries (Attempt 3)
9. Still fails
10. Agent escalates: "Tried 3 times, can't proceed without help"

**Pass Criteria**:
- ✅ Attempt 1: logic_error (agent escalates)
- ✅ Attempt 2: different error (agent adapts)
- ✅ Attempt 3: still not fixed
- ✅ Agent escalates with structured summary
- ✅ Run log shows all 3 attempts with different error_ids
- ✅ Agent follows bounded retry rule (3 max)

---

## Test Fixtures

### Fixture 1: Simple Valid Repository
**Type**: Test repo with clear signals for one fog type  
**Contents**:
- Clear README with user workflows
- Issue templates with acceptance criteria
- Users/personas documented
- Primary fog type: `product_fog` (clear)

**Expected**: Valid brief on first try

### Fixture 2: Repository Missing Evidence
**Type**: Valid repo structure but agent needs to add evidence  
**Contents**:
- Good code structure but documentation unclear
- Agent must read code and find evidence lines
- Primary fog type: `architecture_fog` (from code analysis)

**Expected**: First validation fails (empty evidence), agent adds evidence, second try succeeds

### Fixture 3: Misaligned Fog/Workflow
**Type**: Repo with fog type that doesn't match initial workflow choice  
**Contents**:
- Primary fog type: `product_fog`
- Initial workflow choice: `ui-implementation-workflow` (wrong)
- Should be: `product-implementation-workflow`

**Expected**: Semantic conflict detected, agent corrects, validation passes

### Fixture 4: Ambiguous Fog Type (Requires Human Judgment)
**Type**: Repo with signals for multiple fog types  
**Contents**:
- Product unclear AND architecture messy
- Evidence for both `product_fog` and `architecture_fog`
- No clear "primary" without domain knowledge

**Expected**: Agent escalates with: "Please clarify which is the blocking issue"

---

## Test Execution Commands

### Command 1: Start Fresh Agent Session
```bash
# In Claude Code or Cursor:
# File → New Session
# Open this repo

# Agent will see SessionStart hook automatically
```

### Command 2: Agent Invokes Diagnosis
```
User: "Diagnose this repository using sensemaking-skills. Follow the bootstrap skill."

Agent reads: /skill using-sensemaking
Agent invokes: repo-sensemaker skill
Agent produces: artifacts/repository_sensemaking_brief.md
```

### Command 3: Agent Validates
```
Agent calls: python3 scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
Agent gets: JSON response
Agent parses: valid, artifact_id, errors, error_id
```

### Command 4: Agent Records
```
Agent pipes: validate-and-report.py output to record-validation.py
Agent creates: validation_run_log.md entry
Agent logs: All validation attempts with timestamps
```

### Command 5: Agent Handles Errors
```
If valid: Agent completes Phase 1
If error: Agent decides:
  - missing_field → auto-fix and retry
  - unknown_value → auto-fix and retry
  - semantic_conflict → reason and fix if confident
  - logic_error → escalate to user
  - same error_id on Attempt 2 → escalate (don't retry)
  - 3 attempts exhausted → escalate with summary
```

---

## Expected Artifacts

### From Agent Diagnosis
- `artifacts/repository_sensemaking_brief.md` with:
  - artifact_id: "repository_sensemaking_brief"
  - primary_fog_type: (one of 4 types)
  - evidence: (file-level citations from codebase)
  - recommended_workflow_id: (matching fog type)
  - created_at: (ISO 8601)

### From Validation
- `artifacts/validation_run_log.md` with:
  - Header: "# Validation Run Log"
  - Multiple entries (one per attempt):
    - Timestamped: `## Validation Attempt — 2026-05-24T...Z`
    - Artifact metadata
    - Result (VALID or INVALID)
    - Error table (if invalid):
      - error_id
      - error_type
      - field
      - message
      - suggested_fix
    - References

### From Agent Summary
- Final report including:
  - Primary fog type identified
  - Evidence supporting classification
  - Recommended workflow
  - Validation status (valid after N attempts)
  - Any escalations or notes

---

## Pass/Fail Criteria

### PASS Scenario 1 (Happy Path)
- [x] Agent reads skill
- [x] Agent diagnoses repo
- [x] Produces valid brief
- [x] validate-and-report.py returns valid=true (exit code 0)
- [x] record-validation.py logs entry
- [x] Agent completes without errors
- [x] Run log shows: 1 entry, VALID result, 0 errors

### PASS Scenario 2 (Auto-Fix)
- [x] Attempt 1: validation fails
- [x] Attempt 2: agent adds evidence or fixes missing field
- [x] Attempt 2: validation passes (valid=true)
- [x] Agent completes successfully
- [x] Run log shows: 2 entries, both with same error_id in row 1, second is VALID
- [x] Agent explains: "Fixed evidence section, validation passed"

### PASS Scenario 3 (Escalation on Repeat)
- [x] Attempt 1: validation fails with error_id X
- [x] Attempt 2: same error_id X appears
- [x] Agent escalates instead of retrying
- [x] Agent message includes: error_id, suggested_fixes, request for user input
- [x] Run log shows: both attempts with matching error_id

### PASS Scenario 4 (Semantic Conflict)
- [x] Semantic conflict detected (error_type="semantic_conflict")
- [x] Agent identifies: workflow routing mismatch
- [x] Agent corrects workflow choice
- [x] Retry passes (valid=true)
- [x] Agent explains: "Corrected workflow routing"

### PASS Scenario 5 (3-Attempt Budget)
- [x] Attempt 1: error (agent escalates if logic_error)
- [x] Attempt 2: different error (agent adapts)
- [x] Attempt 3: still not valid
- [x] Agent escalates: "Tried 3 times, still stuck"
- [x] Run log shows: 3 entries with progression of attempts
- [x] Agent respects bounded retry limit

### FAIL Criteria
- ❌ Agent doesn't read bootstrap skill
- ❌ Agent doesn't invoke validate-and-report.py
- ❌ Agent doesn't log to record-validation.py
- ❌ Agent retries same error more than once
- ❌ Agent doesn't escalate after 3 attempts
- ❌ Validation JSON malformed or missing required fields
- ❌ Run log not created or incomplete

---

## Success Transcript Outline

### Scenario 1 (Happy Path) - Expected Transcript

```
User: Diagnose this repository.

Agent: I'll analyze your repository to identify the primary problem.
[reads using-sensemaking skill]
[invokes repo-sensemaker skill]

Agent: I've identified the primary fog type: product_fog

Evidence:
- README.md (lines 5-12): Feature list vague, no user context
- No ARCHITECTURE.md
- 30+ issues marked 'needs-clarification'

I'll now validate this diagnosis.

[validates with validate-and-report.py]

Agent: Validation successful ✅
Artifact: repository_sensemaking_brief
Status: VALID
Errors: 0

Your repository has a product fog problem. I recommend the product-implementation-workflow.

[logs to validation_run_log.md]

Phase 1 diagnosis complete.
```

### Scenario 2 (Auto-Fix) - Expected Transcript

```
User: Diagnose this repository.

Agent: [diagnoses, produces brief]

Agent: Now validating the diagnosis...
[calls validate-and-report.py]

Agent: Validation found an issue:
error_id: repository_sensemaking_brief.evidence.logic_error
message: Evidence section is empty. Cannot verify fog type classification.

Let me re-analyze the codebase to add evidence.

[reads codebase, finds evidence lines]

Agent: I've identified evidence supporting product_fog:
- /src/services/UserService.ts: No user context in API contracts
- /docs/README.md: Feature list lacks acceptance criteria
- /issues: 30+ marked 'needs-clarification' with no owners assigned

[retries validation with evidence]

Agent: Validation successful on attempt 2 ✅
Artifact: repository_sensemaking_brief
Status: VALID (after 1 auto-fix)
Errors: 0

Phase 1 diagnosis complete.
```

### Scenario 3 (Escalation) - Expected Transcript

```
User: Diagnose this repository.

Agent: [Attempt 1: diagnoses, validates]

Agent: Validation failed with error:
error_id: repository_sensemaking_brief.primary_fog_type.missing_field
message: Required field 'primary_fog_type' is missing.

Let me re-read the codebase and add the missing field.

[Attempt 2: re-analyzes]

Agent: [validates again]

Agent: Same error returned:
error_id: repository_sensemaking_brief.primary_fog_type.missing_field

This error has come back twice. Following the retry rule, I should not try again.

I need your help to resolve this:

**Error Details**:
- Field: primary_fog_type
- Error: Required field missing
- Suggestions from validator:
  1. Add primary_fog_type: choose from [product_fog, ui_fog, docs_fog, architecture_fog]
  2. Review evidence to determine which fog type is primary

Please tell me: Based on your knowledge of this codebase, which is the primary problem?
1. User needs unclear (product_fog)
2. Design system inconsistent (ui_fog)
3. Architecture undocumented (docs_fog)
4. Code structure messy (architecture_fog)

User: It's definitely architecture - the code is tightly coupled.

Agent: [Attempt 3: updates primary_fog_type to architecture_fog]
[validates again]

Agent: Validation successful ✅
Artifact: repository_sensemaking_brief
Status: VALID (after 2 escalations)

Phase 1 diagnosis complete. Your repository has architecture_fog.
```

---

## Running the Test

### Prerequisites
- Fresh Claude Code / Cursor session in this repo
- SessionStart hook available
- `skills/using-sensemaking/SKILL.md` readable
- All Phase 1 scripts present

### Steps
1. Open fresh session
2. Verify SessionStart hook surfaces
3. Run one or more scenarios (start with Scenario 1)
4. Agent follows the diagnosis flow
5. Check outputs:
   - `artifacts/repository_sensemaking_brief.md` created
   - `artifacts/validation_run_log.md` created with entries
   - Agent handled errors according to script
   - Agent escalated appropriately

### Success Criteria
- Agent completes one full scenario without errors
- Validation logs created and readable
- Agent decision logic follows bounded retry rules
- No exceptions or missing JSON fields

---

## Next Steps After Test

### If Test PASSES ✅
- Phase 1 is proven with real agent
- Ready to start Phase 2 implementation workflows
- Confidence in agent behavior is high

### If Test FAILS ❌
- Identify which step broke
- Debug agent reasoning or script integration
- Fix root cause
- Rerun test

---

**Status**: Ready for execution  
**Estimated Duration**: 1-2 hours to run through all scenarios  
**Outcome**: Proof that agents can use Phase 1 system as designed  

