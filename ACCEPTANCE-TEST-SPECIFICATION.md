# Architectural-Review Skill: Acceptance Test Specification

## Context
This specification defines the acceptance test that MUST pass after the preflight validation defect is separately repaired. The test uses a suitable execution-capable executor (TBD) instead of `dry-run`.

## Prerequisites
- Preflight defect in validate-repo.py is fixed or a production-representative validation policy is approved
- An executor with `supports_real_execution = True` is selected for this test
- Proposed_direction input resolution (File P) is functional
- Hard-fail gate (File P) is functional
- Validator (File D) is functional
- Workflow registry contains architectural-review-planning-workflow

## Test Setup

### Input Preparation
Create a temporary session directory with the following structure:

```
<session-dir>/
├── 00-user-intent.md
└── proposed_direction.md
```

### File: 00-user-intent.md
**Valid schema (required fields)**:
```markdown
# User Intent

## Machine-readable intent

```yaml
artifact_id: user_intent
intent_source: acceptance-test
scope_mode: focused
raw_problem_statement: "Test architectural review with multi-step proposal"
created_at: "2026-07-18T12:00:00Z"
created_by: "acceptance-test-runner"
immutable: false
```
```

### File: proposed_direction.md
**Valid content (required: non-empty, non-whitespace)**:
```markdown
# Proposed Direction

## Summary
Add a new capability for handling multi-tenant scenarios.

## Approach
Implement a tenant isolation layer with read-only workspace separation.

## Machine-readable metadata

```yaml
artifact_id: proposed_direction
created_at: "2026-07-18T12:00:00Z"
created_by: "acceptance-test-runner"
```
```

## Test Execution

### Command
```bash
python scripts/workflow-runtime.py \
  --workflow architectural-review-planning-workflow \
  --from-session <session-dir> \
  --executor <execution-capable-executor> \
  --mode guided_execution
```

Where `<execution-capable-executor>` is an executor with:
- `supports_real_execution = True`
- Deterministic or reproducible output for testing
- Participates through normal runtime boundary (no bypass)

### Expected Exit Code
```
0 (success)
```

## Assertions to Verify

### 1. Workflow Loads (Proof: stdout/run.log)
- Output contains: `[OK]` message about loading workflow
- Workflow registry resolution succeeds

### 2. Step 1 Executes: repo-sensemaker
**Assertion**: run.log contains evidence of Step 1 execution

Required evidence:
- `STEP 1/2` or `Step 1` or `repo-sensemaker` appears in run.log
- Skill invocation record present (executor invoke_skill called)
- Step status is not FAILED or SKIPPED

### 3. repository_sensemaking_brief Produced
**Assertion**: Brief artifact exists in session directory and is schema-valid

Required:
- File exists at `<session-dir>/repository_sensemaking_brief.md` or similar
- File is non-empty
- Contains `artifact_id: repository_sensemaking_brief`
- Can be parsed by validate-brief.py without errors

### 4. Step 2 Executes: architectural-review
**Assertion**: run.log contains evidence of Step 2 execution

Required evidence:
- `STEP 2/2` or `Step 2` or `architectural-review` appears in run.log
- Skill invocation record present (executor invoke_skill called)
- Step status is not FAILED or SKIPPED

### 5. Step 2 Receives Both Required Inputs
**Assertion**: Step 2 context shows both inputs are resolved

Required evidence in run.log or step output:
- `repository_sensemaking_brief` is present in resolved_inputs or skill context
- `proposed_direction` is present in resolved_inputs or skill context
- Both inputs have content (not empty)
- `present: true` flag for both inputs

### 6. architectural_review_recommendation Produced
**Assertion**: Recommendation artifact exists in session and is schema-valid

Required:
- File exists at `<session-dir>/architectural_review_recommendation.md`
- File is non-empty
- Contains `artifact_id: architectural_review_recommendation`
- Contains `decision:` field with value from {pursue, pursue_narrowed, investigate_first, defer, reject}
- Contains `confidence:` field with value from {high, medium, low}

### 7. File O Routes to File D
**Assertion**: Recommendation artifact is validated through the dispatcher

Required evidence:
- run.log shows `validate-and-report.py` is invoked with architectural_review_recommendation
- `select_validator("architectural_review_recommendation")` routes to `validate-architectural-review-recommendation.py`
- Validation output shows validator used: `validate-architectural-review-recommendation.py`

### 8. Recommendation Passes Validation
**Assertion**: Recommendation passes File D validation rules

Required:
- Validation result is `valid: true`
- No validation errors in result
- All required decision-specific fields present and valid

### 9. Both Steps in Run Log
**Assertion**: Complete step history is recorded

Required evidence in run.log:
- Step 1 result with status (not FAILED)
- Step 2 result with status (not FAILED)
- Both show artifact inputs/outputs
- No missing step records

### 10. Workflow Completed Successfully
**Assertion**: `final_state == "completed"`

Required:
- run.log contains line: `final_state: completed` or `"final_state": "completed"`
- No error state (not "failed", "aborted", "timeout")
- Workflow summary shows completion

## Failure Path Test

### Setup
Create session with ONLY `00-user-intent.md`, NO `proposed_direction.md`

### Execution
```bash
python scripts/workflow-runtime.py \
  --workflow architectural-review-planning-workflow \
  --from-session <session-dir> \
  --executor <execution-capable-executor> \
  --mode guided_execution
```

### Expected Behavior
- Step 2 fails with FAILED status (hard-fail gate triggers)
- Error message mentions missing `proposed_direction`
- run.log shows: `Step 2: FAILED` or `FAILED ... proposed_direction`
- Recommendation artifact is NOT produced
- `final_state: failed` (not "completed")

## Test Output Requirements

### run.log Contents
Must contain (in order):
1. Workflow load confirmation
2. Step 1 execution record
3. Step 1 completion and output artifact path
4. Step 2 execution record
5. Step 2 completion and output artifact path
6. Both artifacts listed in final summary
7. Final state: `final_state: completed`

### Artifact Files
Session directory must contain after successful run:
- `00-user-intent.md` (input)
- `proposed_direction.md` (input)
- `repository_sensemaking_brief.md` (Step 1 output)
- `architectural_review_recommendation.md` (Step 2 output)
- `run.log` (execution log)

## Pass Criteria

**All 11 assertions must pass**:
- Step 1 executes (assertion 2)
- Brief produced (assertion 3)
- Step 2 executes (assertion 4)
- Both inputs received (assertion 5)
- Recommendation produced (assertion 6)
- Dispatcher routes correctly (assertion 7)
- Validation passes (assertion 8)
- Both steps in log (assertion 9)
- final_state == "completed" (assertion 10)
- Failure path works (separate test)

**No assertions may be waived or loosened.**

## Test Environment Notes

### Executor Selection Constraint
The executor must be:
- Reproducible (same inputs → same outputs, or at least deterministic for testing)
- Not dependent on external services that might be unavailable
- Able to write artifacts to the session directory
- Able to parse and hand off artifacts to Step 2

Current candidates:
- ClaudeAgentSdkSkillExecutor: requires Agent SDK, not deterministic
- ApiSkillExecutor: requires ANTHROPIC_API_KEY, depends on Claude API availability
- A test-mock executor: hypothetical; would need design and implementation

### Known Limitations (Preflight)
- Test cannot currently run until validate-repo.py preflight defect is fixed
- Preflight must pass before Step 1 can execute
- This test does NOT prove preflight behavior; that is a separate concern

## Next Steps
1. Identify or design an executor suitable for deterministic acceptance testing
2. Fix the preflight validation defect (separate task)
3. Implement this test using the identified executor
4. Run the test and verify all 11 assertions pass
5. Retain the failure-path test in the test suite

---

## Appendix: Why dry-run is Unsuitable

The `DryRunSkillExecutor` has `supports_real_execution = False`.

**What this means**:
- `invoke_skill()` does not actually invoke skills
- Input artifacts are not read
- Output artifacts are not written
- No artifact files created on disk
- No skill behavior observable

**Why assertions would fail with dry-run**:
- Assertion 2 (Step 1 executes): No skill execution, no proof
- Assertion 3 (Brief produced): No artifact written, file won't exist
- Assertion 4 (Step 2 executes): No skill execution
- Assertion 5 (Both inputs received): No skill receives inputs, can't verify
- Assertion 6 (Recommendation produced): No artifact written
- Assertion 7 (Dispatcher to validator): No validation runs, no routing proof
- Assertion 8 (Validation passes): Validator never runs
- Assertion 9 (Steps in log): May appear in log, but no real execution proof
- Assertion 10 (final_state): May be "completed" in plan, not after execution
- Assertion 11 (Failure path): Hard-fail gate works (unit-tested), but not full stack

**Conclusion**: `dry-run` proves workflow *planning* works. It does NOT prove step *execution* works.
