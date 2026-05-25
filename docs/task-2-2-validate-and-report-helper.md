# Task 2.2: Validate-and-Report Helper

**Status**: ✅ COMPLETE  
**Date**: 2026-05-25  
**Purpose**: Single agent-facing validation entrypoint  

---

## What This Solves

Instead of agents needing to know which validator to invoke:

```bash
# OLD: Agents had to choose the right validator
python3 scripts/validate-brief.py artifact.md --json
# OR
python3 scripts/validate-plan.py artifact.md --json
# OR
python3 scripts/validate-artifact.py artifact_id artifact.md --json
```

Now agents just call one helper:

```bash
# NEW: One call, unified JSON back
python3 scripts/validate-and-report.py artifact.md
```

The helper:
1. Extracts artifact_id from the file
2. Selects the correct validator automatically
3. Invokes it with --json
4. Returns the unified schema
5. Wraps any errors in the same schema (no exceptions leak)

---

## Files Created

| File | Purpose | Status |
|------|---------|--------|
| `scripts/validate-and-report.py` | Agent-facing validation entrypoint | ✅ Created |
| `tests/run_validate_and_report_tests.py` | Comprehensive test suite (7 tests) | ✅ Created |

---

## Routing Behavior

### Automatic Detection

The helper extracts `artifact_id` from the artifact's YAML block and routes accordingly:

```
artifact_id: repository_sensemaking_brief  →  validate-brief.py
artifact_id: workflow_orchestration_plan   →  validate-plan.py
artifact_id: <anything else>               →  validate-artifact.py (generic)
artifact_id: <not found>                   →  validate-artifact.py (generic)
```

### Extraction Strategy

Searches for YAML block in order of preference:
1. Section 13: Machine-readable handoff
2. Section 11: Machine-readable plan
3. Last ```yaml...``` block in the file

If artifact_id is found in the YAML, the specific validator is used.  
If not found, the generic `validate-artifact.py` is used (which will report missing artifact_id).

---

## Usage

### Simple invocation (agents use this)

```bash
python3 scripts/validate-and-report.py <artifact_path>
```

**Returns**: JSON to stdout, exit code 0 if valid, 1 if invalid

**Example**:
```bash
$ python3 scripts/validate-and-report.py artifacts/brief.md
{
  "valid": true,
  "artifact_id": "repository_sensemaking_brief",
  "artifact_path": "/path/to/brief.md",
  "validator": "validate-brief.py",
  "errors": [],
  "validation_timestamp": "2026-05-25T10:30:00Z"
}
```

### With repo root

```bash
python3 scripts/validate-and-report.py <artifact_path> --repo-root <root>
```

---

## JSON Schema (Unified)

All responses use the same top-level schema, regardless of which validator was invoked:

```json
{
  "valid": boolean,
  "artifact_id": string,
  "artifact_path": string (absolute),
  "validator": string (name of validator that was invoked),
  "errors": [
    {
      "error_id": string,
      "error_type": string,
      "field": string | null,
      "current_value": any,
      "message": string,
      "suggested_fixes": [string, ...],
      "reference": string
    },
    ...
  ],
  "validation_timestamp": string (ISO 8601 with Z)
}
```

---

## Error Handling: Graceful Degradation

If a validator fails (not found, invalid JSON output, subprocess error), the helper wraps the error in the same schema instead of raising an exception:

### Validator not found

```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "artifact_path": "/path/to/artifact.md",
  "validator": "validate-and-report.py",
  "errors": [
    {
      "error_id": "repository_sensemaking_brief.validator.execution_error",
      "error_type": "logic_error",
      "field": "validator",
      "current_value": "scripts/validate-brief.py",
      "message": "Validator not found: scripts/validate-brief.py",
      "suggested_fixes": [
        "Ensure validator script exists",
        "Check scripts directory path"
      ],
      "reference": "docs/validator-json-refactor-guide.md"
    }
  ],
  "validation_timestamp": "2026-05-25T10:30:00Z"
}
```

### Validator returns invalid JSON

```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "artifact_path": "/path/to/artifact.md",
  "validator": "validate-and-report.py",
  "errors": [
    {
      "error_id": "repository_sensemaking_brief.validator.execution_error",
      "error_type": "logic_error",
      "field": "validator",
      "current_value": "scripts/validate-brief.py",
      "message": "Validator returned invalid JSON: Expecting value: line 1 column 1 (char 0)",
      "suggested_fixes": [
        "Run the validator directly with --json",
        "Check validator stderr for syntax or dependency errors"
      ],
      "reference": "docs/validator-json-refactor-guide.md"
    }
  ],
  "validation_timestamp": "2026-05-25T10:30:00Z"
}
```

### Missing artifact file

```json
{
  "valid": false,
  "artifact_id": "unknown",
  "artifact_path": "/path/to/nonexistent.md",
  "validator": "validate-and-report.py",
  "errors": [
    {
      "error_type": "missing_field",
      "field": "artifact",
      "current_value": null,
      "message": "Artifact file not found: /path/to/nonexistent.md",
      "suggested_fixes": [
        "Ensure artifact exists at: /path/to/nonexistent.md"
      ],
      "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
    }
  ],
  "validation_timestamp": "2026-05-25T10:30:00Z"
}
```

### Cannot determine artifact_id (falls back to generic validator)

```json
{
  "valid": false,
  "artifact_id": "unknown",
  "artifact_path": "/path/to/artifact.md",
  "validator": "validate-and-report.py",
  "errors": [
    {
      "error_id": "unknown.artifact_id.missing_field",
      "error_type": "missing_field",
      "field": "artifact_id",
      "current_value": null,
      "message": "Cannot determine artifact_id from file. Generic validator requires artifact_id to be present in YAML block.",
      "suggested_fixes": [
        "Add artifact_id field to machine-readable handoff YAML block"
      ],
      "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
    }
  ],
  "validation_timestamp": "2026-05-25T10:30:00Z"
}
```

**Key benefit**: Agents always get JSON they can parse. No exceptions, no raw stderr, no stack traces.

---

## Example Routing Flows

### Flow 1: Valid Brief

```
Agent calls:
  validate-and-report.py brief.md

Helper extracts:
  artifact_id = "repository_sensemaking_brief" (from YAML)

Helper selects:
  scripts/validate-brief.py

Helper invokes:
  python3 scripts/validate-brief.py brief.md --repo-root . --json

Helper returns:
  {
    "valid": true,
    "artifact_id": "repository_sensemaking_brief",
    "validator": "validate-brief.py",
    "errors": [],
    ...
  }
```

### Flow 2: Invalid Plan

```
Agent calls:
  validate-and-report.py plan.md

Helper extracts:
  artifact_id = "workflow_orchestration_plan" (from YAML)

Helper selects:
  scripts/validate-plan.py

Helper invokes:
  python3 scripts/validate-plan.py plan.md --repo-root . --json

Helper returns:
  {
    "valid": false,
    "artifact_id": "workflow_orchestration_plan",
    "validator": "validate-plan.py",
    "errors": [
      { "error_id": "workflow_orchestration_plan.primary_fog_type.missing_field", ... },
      { "error_id": "workflow_orchestration_plan.chosen_workflow_id.semantic_conflict", ... }
    ],
    ...
  }
```

### Flow 3: Unknown Artifact Type

```
Agent calls:
  validate-and-report.py artifact.md

Helper extracts:
  artifact_id = "custom_artifact_type" (from YAML)

Helper selects:
  scripts/validate-artifact.py (generic fallback)

Helper invokes:
  python3 scripts/validate-artifact.py custom_artifact_type artifact.md --json

Helper returns:
  {
    "valid": false,
    "artifact_id": "custom_artifact_type",
    "validator": "validate-artifact.py",
    "errors": [
      { "error_id": "custom_artifact_type.artifact_id.unknown_value", ... }
    ],
    ...
  }
```

---

## Test Results

```
[TEST 1] Valid brief routes to validate-brief.py
  PASSED: Valid brief routed to validate-brief.py and returned clean result

[TEST 2] Valid plan routes to validate-plan.py
  PASSED: Valid plan routed to validate-plan.py and returned clean result

[TEST 3] Known artifact (brief) correctly detected and routed
  PASSED: Artifact with known ID correctly routed to validate-brief.py

[TEST 4] Invalid brief returns structured errors
  PASSED: Invalid brief returned 3 structured errors

[TEST 5] Non-existent file returns structured error
  PASSED: Non-existent file handled gracefully with structured error

[TEST 6] All results have unified schema
  PASSED: All results have unified schema with all required keys

[TEST 7] error_id preserved in routed validation
  PASSED: All errors have error_id fields

[SUMMARY] 7/7 tests passed
```

---

## Integration with Agent Loop

This helper is the bridge between agent logic and validators:

```python
# Agent code using validate-and-report.py

import json
import subprocess

# Validate artifact
result = subprocess.run(
    ["python3", "scripts/validate-and-report.py", artifact_path],
    capture_output=True,
    text=True
)

validation = json.loads(result.stdout)

if not validation["valid"]:
    # Get all errors
    errors = validation["errors"]
    
    # Track error_ids across attempts
    error_ids = {e["error_id"]: e for e in errors}
    
    # Attempt to auto-fix (if logic implements it)
    for error in errors:
        if error["error_type"] == "missing_field":
            # Try to fill in the field
            artifact[error["field"]] = default_value
        elif error["error_type"] == "semantic_conflict":
            # Can't auto-fix; escalate
            escalate_to_user(error)
    
    # Re-validate
    result = subprocess.run(...)
    validation = json.loads(result.stdout)
    new_error_ids = {e["error_id"]: e for e in validation["errors"]}
    
    # Check if same errors repeated
    if set(error_ids.keys()) & set(new_error_ids.keys()):
        # Same error came back → escalate (Attempt 3 rule)
        escalate_to_user(list(new_error_ids.values()))
```

---

## Design Principles

### Separation of Concerns

- **validate-and-report.py**: Route, invoke, return JSON
- **validate-brief.py, validate-plan.py, validate-artifact.py**: Validate against contracts
- **Auto-fix logic**: Belongs in agent/orchestration-runner (not in this helper)
- **Durable logging**: Belongs in record-validation.py (not in this helper)

### No Side Effects

- Does not write to artifacts
- Does not modify files
- Does not have state
- Pure function: artifact_path → JSON result

### Graceful Degradation

- All errors wrapped in unified schema
- No exceptions leak to stdout
- Subprocess failures become structured validation errors
- Agents can always parse the response

---

## Future Work

This helper is intentionally minimal:
- ✅ Route validators dynamically
- ✅ Return unified JSON
- ✅ Wrap errors gracefully
- ❌ NOT auto-fix (belongs in orchestration-runner)
- ❌ NOT logging (belongs in record-validation.py)
- ❌ NOT orchestration (belongs in agent)

That keeps the helper focused and reusable.

---

**Task 2.2 Status**: ✅ COMPLETE (validate-and-report.py created as single agent entrypoint)

**Ready for**: Task 2.3 (record-validation.py for durable run-log writing)

---

**Created**: 2026-05-25  
**Implementation**: Claude Code Agent  
**Quality**: Production-ready (agent-facing entrypoint with graceful error handling)
