# Task 2.1a Enhancement: Stable error_id Fields

**Status**: ✅ COMPLETE  
**Date**: 2026-05-25  
**Enhancement**: Added `error_id` to all validation errors for agent retry tracking  

---

## Why error_id Matters

Agents need to distinguish between:
1. **Same error repeating** → triggers escalation (Attempt 2 rule)
2. **New error appearing** → try different approach
3. **Previous error resolved** → continue retrying other errors
4. **Error auto-fixable** → attempt fix automatically

Without stable `error_id`, agents can't reliably track these state changes across retries.

---

## error_id Format

```
<artifact_id>.<field>.<error_type>
```

**Examples**:
```
repository_sensemaking_brief.primary_fog_type.missing_field
repository_sensemaking_brief.evidence.type_error
repository_sensemaking_brief.evidence.logic_error
repository_sensemaking_brief.recommended_workflow_id.unknown_value
```

---

## Implementation

### Changes to validate-brief.py

Every `ValidationError` now includes `error_id` field:

```python
class ValidationError(TypedDict, total=False):
    error_id: str  # e.g., repository_sensemaking_brief.primary_fog_type.missing_field
    error_type: str
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str
```

### Changes to Tests

Added 3 new tests to verify error_id:
- **TEST 6**: All errors have error_id field
- **TEST 7**: error_id follows correct format
- **TEST 8**: error_ids are unique (for retry tracking)

---

## Test Results

```
[TEST 6] error_id in all errors
  PASSED: All 3 errors have error_id
    - repository_sensemaking_brief.primary_fog_type.missing_field
    - repository_sensemaking_brief.evidence.missing_field
    - repository_sensemaking_brief.recommended_workflow_id.missing_field

[TEST 7] error_id format validation
  PASSED: All error_ids follow correct format

[TEST 8] error_id usefulness for retry logic
  PASSED: All error_ids are unique (can track retries)

[SUMMARY] 8/8 tests passed
```

---

## Example JSON Output with error_id

```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "validator": "validate-brief.py",
  "errors": [
    {
      "error_id": "repository_sensemaking_brief.primary_fog_type.missing_field",
      "error_type": "missing_field",
      "field": "primary_fog_type",
      "current_value": null,
      "message": "Required field 'primary_fog_type' is missing.",
      "suggested_fixes": [
        "Add primary_fog_type: product_fog",
        "Add primary_fog_type: ui_fog",
        "Add primary_fog_type: docs_fog",
        "Add primary_fog_type: architecture_fog"
      ],
      "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
    },
    {
      "error_id": "repository_sensemaking_brief.evidence.missing_field",
      "error_type": "missing_field",
      "field": "evidence",
      "current_value": null,
      "message": "Required field 'evidence' is missing.",
      "suggested_fixes": [
        "Add evidence as a list of file-level citations",
        "Example: evidence: ['README.md (lines 5-12): vague feature requirements', ...]"
      ],
      "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
    }
  ],
  "validation_timestamp": "2026-05-25T00:23:55.613344Z"
}
```

---

## Agent Retry Logic Pattern

With stable `error_id`, agents can now implement robust retry logic:

```python
errors_by_id = {e['error_id']: e for e in validation_result['errors']}
previous_errors = {}

for attempt in range(1, 4):
    errors = validate(artifact)
    new_error_ids = {e['error_id']: e for e in errors}
    
    # Check for same error repeating
    repeated_errors = set(previous_errors.keys()) & set(new_error_ids.keys())
    if repeated_errors:
        # Same error came back - escalate (don't retry)
        escalate_to_user([new_error_ids[eid] for eid in repeated_errors])
        return
    
    # Try to fix new errors
    for error in errors:
        if error['error_type'] in ['missing_field', 'type_error', 'unknown_value']:
            fix_error_auto(artifact, error)
    
    previous_errors = new_error_ids

# All retries exhausted
if errors:
    escalate_to_user(errors)
```

---

## Pattern Ready for Other Validators

This enhancement establishes the pattern for:
- **Task 2.1b**: `validate-plan.py` (same error_id format)
- **Task 2.1c**: `validate-artifact.py` (same error_id format)

All validators will use: `<artifact_id>.<field>.<error_type>`

---

## Files Modified

| File | Changes |
|------|---------|
| `scripts/validate-brief.py` | Added `error_id` to 6 validation error objects |
| `tests/run_validate_brief_tests.py` | Added `error_id` to test errors; added 3 new tests |
| `docs/task-2-1a-error-id-enhancement.md` | This file (documentation) |

---

## Backward Compatibility

✅ **No breaking changes**
- `error_id` is an additional field, not a replacement
- Existing code consuming errors still works
- JSON structure remains valid

---

## Ready for Task 2.1b

validate-brief.py is now a **complete reference implementation** with:
- ✅ JSON output support
- ✅ Multi-error schema
- ✅ Stable error_id fields
- ✅ Backward-compatible prose mode
- ✅ Comprehensive tests (8/8 passing)

**Next**: Apply same pattern to `validate-plan.py`

---

**Created**: 2026-05-25  
**Quality**: Reference-grade (for reuse across all validators)  
**Impact**: Enables robust agent retry logic based on error tracking
