# Task 2.3: Record-Validation Logging

**Status**: ✅ COMPLETE  
**Date**: 2026-05-25  
**Purpose**: Durable audit trail for validation attempts  

---

## What This Solves

Validation results should not vanish. When agents validate artifacts and make decisions based on errors, there should be a persistent record:

```bash
# Validate artifact and record the result
python3 scripts/validate-and-report.py artifact.md | \
python3 scripts/record-validation.py --run-log runs.log
```

The run log becomes the audit trail:
- What was validated and when
- Which validator was used
- What errors were found
- What the agent decided to do next

This enables:
- **Traceability**: "Why did the agent escalate?"
- **Debugging**: "What errors did we encounter on attempt 2?"
- **Reporting**: "How many artifacts passed validation?"
- **Compliance**: "Here's the complete history of decisions"

---

## Files Created

| File | Purpose | Status |
|------|---------|--------|
| `scripts/record-validation.py` | Log validation results to persistent run log | ✅ Created |
| `tests/run_record_validation_tests.py` | Comprehensive test suite (8 tests) | ✅ Created |

---

## How It Works

### Simple Pipeline

```bash
# Validate and log in one pipeline
validate-and-report.py artifact.md | record-validation.py --run-log runs.log
```

The script:
1. Reads validation JSON from stdin (or file with `--validation-json`)
2. Formats it as a markdown log entry
3. Appends to the run log
4. Never modifies the artifact itself

### Entry Format

Each validation attempt becomes a timestamped log entry:

```markdown
## Validation Attempt — 2026-05-25T10:30:00Z

- Artifact: `repository_sensemaking_brief`
- Path: `/path/to/artifact.md`
- Validator: `validate-brief.py`
- Result: **INVALID**
- Error count: 3

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `repository_sensemaking_brief.primary_fog_type.missing_field` | missing_field | primary_fog_type | Required field 'primary_fog_type' is missing. | Add primary_fog_type: product_fog |
| `repository_sensemaking_brief.evidence.missing_field` | missing_field | evidence | Required field 'evidence' is missing. | Add evidence as a list of file-level citations |
| `repository_sensemaking_brief.recommended_workflow_id.missing_field` | missing_field | recommended_workflow_id | Required field 'recommended_workflow_id' is missing. | Add recommended_workflow_id: product-implementation-workflow |

References:
- `skills/workflow-planner/references/artifact-contracts.yaml`

---
```

---

## Usage

### Simplest: Pipe Validation Result

```bash
python3 scripts/validate-and-report.py artifact.md | \
python3 scripts/record-validation.py --run-log runs.log
```

### With File Input

```bash
python3 scripts/record-validation.py \
  --validation-json validation-result.json \
  --run-log runs.log
```

### Exit Codes

- `0` = Successfully recorded
- `1` = Invalid JSON input
- `1` = Unable to write run log

---

## Log Structure

### Header (Created Once)

```markdown
# Validation Run Log

This log records all validation attempts for artifacts in this repository.
Each entry preserves the complete validation result for auditing.
```

### Entry Format

**Valid Artifact**:
```markdown
## Validation Attempt — 2026-05-25T10:30:00Z

- Artifact: `repository_sensemaking_brief`
- Path: `/path/to/artifact.md`
- Validator: `validate-brief.py`
- Result: **VALID**
- Errors: 0

---
```

**Invalid Artifact**:
```markdown
## Validation Attempt — 2026-05-25T10:31:00Z

- Artifact: `workflow_orchestration_plan`
- Path: `/path/to/plan.md`
- Validator: `validate-plan.py`
- Result: **INVALID**
- Error count: 2

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `workflow_orchestration_plan.primary_fog_type.missing_field` | missing_field | primary_fog_type | Required field 'primary_fog_type' is missing. | Add primary_fog_type: product_fog |
| `workflow_orchestration_plan.chosen_workflow_id.semantic_conflict` | semantic_conflict | chosen_workflow_id | Workflow 'ui-implementation-workflow' does not align with primary_fog_type 'product_fog'. | Change chosen_workflow_id to: product-implementation-workflow |

References:
- `docs/adr/0007-soft-context-routing.md`
- `skills/workflow-planner/references/artifact-contracts.yaml`

---
```

---

## Integration with Agent Loop

Agents use the two-script pipeline:

```python
import json
import subprocess

# 1. Validate artifact
result = subprocess.run(
    ["python3", "scripts/validate-and-report.py", artifact_path],
    capture_output=True,
    text=True
)
validation = json.loads(result.stdout)

# 2. Log the attempt
subprocess.run(
    ["python3", "scripts/record-validation.py", "--run-log", "runs.log"],
    input=result.stdout,
    text=True
)

# 3. Make decisions based on validation
if not validation["valid"]:
    # Implement auto-fix or escalation logic here
    for error in validation["errors"]:
        if error["error_type"] == "missing_field":
            artifact[error["field"]] = auto_fix(error)
```

---

## Test Results

```
[TEST 1] Valid artifact validation logs correctly
  PASSED: Valid result logged with correct content

[TEST 2] Invalid artifact validation logs all error_ids
  PASSED: All error_ids logged with error count

[TEST 3] stdin input works
  PASSED: stdin input processed successfully

[TEST 4] file input works
  PASSED: file input processed successfully

[TEST 5] invalid JSON handled gracefully
  PASSED: invalid JSON rejected gracefully

[TEST 6] script does not modify artifact
  PASSED: artifact not modified by record-validation.py

[TEST 7] log file created if missing
  PASSED: log file created with parent directories

[TEST 8] multiple entries append correctly
  PASSED: multiple entries appended correctly

[SUMMARY] 8/8 tests passed
```

---

## Design Principles

### Separation of Concerns

- **validate-and-report.py**: Route validators, return JSON
- **record-validation.py**: Format entries, append to log
- **Agent logic**: Make decisions based on validation results
- **Orchestration**: Implement retry, auto-fix, escalation

### No Side Effects

- Does not modify artifacts
- Does not modify validation JSON
- Purely append-only to log
- Idempotent: running twice logs twice (intentional)

### Simple and Boring

This script is intentionally simple:
- No validation logic
- No business rules
- No auto-fix logic
- No routing logic
- Just reads JSON, formats it, appends to file

This keeps it maintainable and predictable.

---

## Format Decisions

### Why Markdown?

- Human-readable in editors and git diffs
- Works in any text editor
- Can be rendered to HTML/PDF
- Diff-friendly (each entry is separate)
- Easy to search with grep

### Why Table Format?

- Quick scan of error_ids
- Easy to count errors
- Preserves all error metadata
- Can be converted to CSV/JSON later if needed

### Why Append-Only?

- Never loses history
- Idempotent: safe to re-run
- Audit trail persists even if agent crashes
- Can be inspected later for decision-making

---

## Example Run Log

```markdown
# Validation Run Log

This log records all validation attempts for artifacts in this repository.
Each entry preserves the complete validation result for auditing.

## Validation Attempt — 2026-05-25T09:00:00Z

- Artifact: `repository_sensemaking_brief`
- Path: `/artifacts/brief.md`
- Validator: `validate-brief.py`
- Result: **INVALID**
- Error count: 2

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `repository_sensemaking_brief.primary_fog_type.missing_field` | missing_field | primary_fog_type | Required field 'primary_fog_type' is missing. | Add primary_fog_type: product_fog |
| `repository_sensemaking_brief.evidence.logic_error` | logic_error | evidence | Evidence list is empty. Cannot verify fog type classification is grounded in analysis. | Add file-level evidence |

References:
- `skills/workflow-planner/references/artifact-contracts.yaml`
- `docs/adr/0003-artifact-composition-pattern.md`

---

## Validation Attempt — 2026-05-25T09:05:00Z

- Artifact: `repository_sensemaking_brief`
- Path: `/artifacts/brief.md`
- Validator: `validate-brief.py`
- Result: **VALID**
- Errors: 0

---

## Validation Attempt — 2026-05-25T10:00:00Z

- Artifact: `workflow_orchestration_plan`
- Path: `/artifacts/plan.md`
- Validator: `validate-plan.py`
- Result: **INVALID**
- Error count: 1

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `workflow_orchestration_plan.chosen_workflow_id.semantic_conflict` | semantic_conflict | chosen_workflow_id | Workflow 'ui-implementation-workflow' does not align with primary_fog_type 'product_fog'. Expected 'product-implementation-workflow' unless routing_decision_method is 'manual_override'. | Change chosen_workflow_id to: product-implementation-workflow |

References:
- `docs/adr/0007-soft-context-routing.md`

---
```

---

## Auditing the Run Log

Humans can review the log to understand:

```bash
# Count all validation attempts
grep "## Validation Attempt" runs.log | wc -l

# Find all invalid attempts
grep "Result: \*\*INVALID\*\*" runs.log

# Find a specific artifact's history
grep -A 20 "Artifact: \`repository_sensemaking_brief\`" runs.log

# Find what errors appeared most often
grep "error_id" runs.log | sort | uniq -c | sort -rn

# Find all escalation-worthy errors (semantic_conflict, logic_error)
grep "semantic_conflict\|logic_error" runs.log
```

---

## Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `scripts/record-validation.py` | Append validation results to run log | ✅ Created |
| `tests/run_record_validation_tests.py` | Test suite (8 tests, all passing) | ✅ Created |

---

**Task 2.3 Status**: ✅ COMPLETE (record-validation.py created as durable logging layer)

**Validation Pipeline Complete**:
- ✅ Task 2.1a-2.1c: Three unified validators
- ✅ Task 2.2: validate-and-report.py (routing entrypoint)
- ✅ Task 2.3: record-validation.py (durable audit trail)

**Ready for**: Agent integration into orchestration-runner.py

---

**Created**: 2026-05-25  
**Implementation**: Claude Code Agent  
**Quality**: Production-ready (simple, append-only, audit-trail focused)
