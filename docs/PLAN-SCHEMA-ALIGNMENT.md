# Plan Schema Alignment Findings

**Date**: 2026-05-19  
**Phase**: Phase 0 Investigation  
**Status**: Format Divergence Confirmed

---

## Issue Summary

The `orchestration-runner.py` generates orchestration plans with a different `initial_inputs` format than what `validate-plan.py` expects. This causes potential validation failures.

---

## Format Divergence

### What Workflow Registry Declares (Source of Truth)

**Location**: `skills/workflow-orchestrator/references/workflow-registry.yaml`

```yaml
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
    description: Current repository files, folder structure, README, documentation, and git state.
```

**Schema**: List of objects with required fields `id`, `type`, `required`, `description`

---

### What orchestration-runner.py Generates (Current)

**Location**: `scripts/orchestration-runner.py` lines 365-368

```yaml
initial_inputs:
  repository_state: external_context
  user_intent: artifact
```

**Schema**: Dict/mapping where keys are input IDs and values are types. **Missing**: `required` field, `description` field.

---

### What validate-plan.py Expects

**Location**: `scripts/validate-plan.py` lines 164-175

```python
plan_inputs = plan_data.get("initial_inputs", [])
reg_inputs = workflow.get("initial_inputs", [])

plan_input_ids = {i["id"] for i in plan_inputs}  # Expects list of objects with "id"
reg_input_ids = {i["id"] for i in reg_inputs}

if plan_input_ids != reg_input_ids:
    errors.append(...)

for i in plan_inputs:
    if "type" not in i or "required" not in i:  # Expects both fields
        errors.append(...)
```

**Schema**: List of objects. Will **FAIL** if runner generates dict/mapping.

---

## Impact

1. **Validation will fail** when validate-plan.py tries to iterate over `initial_inputs` as a list and access `["id"]` field
2. **Type checking will fail** if input object doesn't have `required` field
3. **Validator error message** will be confusing (tries to call `.get("id")` on a string key)

---

## Root Cause

- **orchestration-runner.py** (lines 365-368) was written to generate a simplified dict format for readability
- **validate-plan.py** (lines 164-175) was written to validate against the registry's list format
- The two were never aligned

---

## Recommended Fix

**Align orchestration-runner.py to match the registry format.**

### Option A: Runner Generates List Format (Recommended)

Update `orchestration-runner.py` lines 365-368 to generate:

```python
lines.append(f"initial_inputs:")
for inp in initial_inputs:
    lines.append(f"  - id: {inp['id']}")
    lines.append(f"    type: {inp.get('type', '?')}")
    lines.append(f"    required: {inp.get('required', False)}")
    if inp.get('description'):
        lines.append(f"    description: {inp.get('description', '')}")
```

**Pros**: Matches registry exactly, no validator changes needed, audit trail is complete  
**Cons**: Plan YAML is slightly longer

### Option B: Validator Accepts Both Formats

Update `validate-plan.py` to detect format and handle both dict and list.

**Pros**: Backward compatible  
**Cons**: Adds complexity, two formats are confusing

---

## Recommendation

**Use Option A** (align runner to list format).

**Rationale:**
- Registry format (list) is the source of truth
- Validator is correct; runner should match
- List format is more explicit (includes `required`, `description` fields)
- Aligns with artifact contract philosophy: all contracts should be explicit

---

## Implementation Steps

1. Update `orchestration-runner.py` lines 365-375 to generate list format
2. Run test: `python scripts/validate-plan.py artifacts/*/04-*.md` (should pass)
3. Verify no regressions in existing runs
4. Document this change in commit message

---

## Testing

### Before Fix
```bash
python scripts/orchestration-runner.py fast-local-diagnostic --mode plan_only
# Generates dict format
python scripts/validate-plan.py artifacts/*/04-*.md
# FAILS: tries to iterate over dict, can't find "id" field
```

### After Fix
```bash
python scripts/orchestration-runner.py fast-local-diagnostic --mode plan_only
# Generates list format
python scripts/validate-plan.py artifacts/*/04-*.md
# PASSES: dict and list are aligned
```

---

## Related Artifacts

- Workflow Registry: `skills/workflow-orchestrator/references/workflow-registry.yaml`
- Runner: `scripts/orchestration-runner.py` (lines 282, 315, 365–368)
- Validator: `scripts/validate-plan.py` (lines 164–175)
- Artifact Contract: `skills/workflow-orchestrator/references/artifact-contracts.yaml`
