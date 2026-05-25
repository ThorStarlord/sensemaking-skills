# Validator JSON Refactoring Guide

**Purpose**: Convert all Phase 1 validators to output structured JSON errors instead of human prose.

**Why**: Agents must parse validator errors reliably. JSON enables deterministic parsing; prose requires agent reasoning (hallucination risk).

**Target validators**:
- `scripts/validate-artifact.py` (generic checks)
- `scripts/validate-brief.py` (repository_sensemaking_brief specific)
- `scripts/validate-plan.py` (workflow_orchestration_plan specific)

**Timeline**: Week 2, Task 2.1

---

## JSON Error Format

All Phase 1 validators output JSON to stdout in this format. **This JSON is NOT written to the artifact file.** Validators emit it for agents/scripts to read and act on.

```json
{
  "valid": true/false,
  "artifact_id": "repository_sensemaking_brief",
  "artifact_path": "/path/to/artifact.md",
  "error_type": null,
  "field": null,
  "current_value": null,
  "message": "Artifact passed all validation checks.",
  "suggested_fixes": [],
  "reference": null,
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**Key principle**: Artifacts contain work product data only. Validation is transient (output by validators, recorded in run logs, not stored in artifacts).

### Field Definitions

| Field | Type | When used | Description |
|-------|------|-----------|-------------|
| `valid` | boolean | always | true if artifact passed validation, false if failed |
| `artifact_id` | string | always | ID of artifact being validated (e.g., "repository_sensemaking_brief") |
| `artifact_path` | string | always | Full path to artifact file |
| `error_type` | string \| null | on failure | Category of error: `missing_field`, `unknown_value`, `semantic_conflict`, `logic_error`, `type_error` |
| `field` | string \| null | on failure | Name of the field that failed validation |
| `current_value` | any | on failure | The actual value in the artifact (can be string, number, null, object) |
| `message` | string | always | Human-readable explanation of result |
| `suggested_fixes` | array | on failure | List of suggested corrections (each is actionable) |
| `reference` | string | on failure | Link to ADR or docs explaining why this rule exists |
| `validation_timestamp` | ISO 8601 | always | When validation ran (use `datetime.utcnow().isoformat() + "Z"`) |

---

## Error Types & Examples

### 1. missing_field

**When**: A required field is absent from the artifact.

**Example**:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "error_type": "missing_field",
  "field": "primary_fog_type",
  "current_value": null,
  "message": "Required field 'primary_fog_type' is missing. Every sensemaking brief must classify the primary problem type.",
  "suggested_fixes": [
    "Add field: primary_fog_type: product_fog",
    "Add field: primary_fog_type: ui_fog",
    "Add field: primary_fog_type: docs_fog",
    "Add field: primary_fog_type: architecture_fog"
  ],
  "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**How to detect**:
```python
required_fields = ['primary_fog_type', 'evidence', 'recommended_workflow_id']
for field in required_fields:
    if field not in artifact_data:
        # Emit missing_field error
```

---

### 2. unknown_value

**When**: A field value is not in the allowed enum.

**Example**:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "error_type": "unknown_value",
  "field": "primary_fog_type",
  "current_value": "ui",
  "message": "Field 'primary_fog_type' has value 'ui', which is not recognized. Did you mean 'ui_fog'?",
  "suggested_fixes": [
    "Change to: primary_fog_type: ui_fog",
    "Check canonical values in: docs/canonical-vocabulary.yaml"
  ],
  "reference": "docs/adr/0011-canonical-vocabulary-enforcement.md",
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**How to detect**:
```python
valid_values = ['product_fog', 'ui_fog', 'docs_fog', 'architecture_fog']
if artifact_data.get('primary_fog_type') not in valid_values:
    # Emit unknown_value error
```

---

### 3. semantic_conflict

**When**: Field values contradict each other or contradict evidence.

**Example**:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "error_type": "semantic_conflict",
  "field": "primary_fog_type",
  "current_value": "ui_fog",
  "message": "Primary fog type is 'ui_fog', but evidence section cites only architectural patterns (coupling, layer violations). Evidence should support the fog classification. Either change fog_type to 'architecture_fog' OR add UI-specific evidence (design system inconsistencies, navigation patterns).",
  "suggested_fixes": [
    "Change primary_fog_type to: architecture_fog",
    "Add UI evidence: design system inconsistencies (e.g., three different modal implementations)",
    "Add UI evidence: navigation complexity (e.g., routing logic in multiple places)"
  ],
  "reference": "docs/adr/0007-soft-context-routing.md",
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**How to detect**:
```python
# Check if evidence matches fog_type
fog_type = artifact_data.get('primary_fog_type')
evidence = artifact_data.get('evidence')
if fog_type == 'ui_fog' and not evidence_contains_ui_signals(evidence):
    # Emit semantic_conflict error
```

---

### 4. logic_error

**When**: Data is structurally valid but logically incomplete or inconsistent.

**Example**:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "error_type": "logic_error",
  "field": "evidence",
  "current_value": [],
  "message": "Evidence section is empty. Cannot verify that fog type classification is grounded in actual repository analysis.",
  "suggested_fixes": [
    "Add file-level evidence (e.g., 'README.md lines 15-22: feature list is vague')",
    "Add architectural evidence (e.g., 'service/User.ts imports service/Order.ts: circular dependency')",
    "Run repo-sensemaker again to populate evidence from actual analysis"
  ],
  "reference": "docs/adr/0003-artifact-composition-pattern.md",
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**How to detect**:
```python
if not artifact_data.get('evidence') or len(artifact_data['evidence']) == 0:
    # Emit logic_error
```

---

### 5. type_error

**When**: Field value is wrong data type (e.g., string instead of array, number instead of boolean).

**Example**:
```json
{
  "valid": false,
  "artifact_id": "repository_sensemaking_brief",
  "error_type": "type_error",
  "field": "evidence",
  "current_value": "coupling in data layer",
  "message": "Field 'evidence' should be an array of strings, but got string. Each evidence item should be a separate entry.",
  "suggested_fixes": [
    "Change to: evidence: ['coupling in data layer', 'layer violations in UI code', ...]"
  ],
  "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
  "validation_timestamp": "2026-05-24T15:30:00Z"
}
```

**How to detect**:
```python
if not isinstance(artifact_data.get('evidence'), list):
    # Emit type_error
```

---

## Refactoring Steps (for each validator)

### Step 1: Identify what the validator currently checks

Open the validator script and identify:
- What fields does it validate?
- What are the validation rules?
- What error messages does it produce?

**Example** (validate-brief.py):
```python
# Currently checks:
# - primary_fog_type is present and one of [product_fog, ui_fog, docs_fog, architecture_fog]
# - evidence is non-empty array
# - recommended_workflow_id exists in workflow registry
# - weakness_type is one of [architectural, product, ui, docs]
```

### Step 2: Create JSON output structure

For each validation rule, define what the JSON error will look like.

**Skeleton**:
```python
def emit_error(error_type, field, current_value, message, suggested_fixes, reference):
    return {
        "valid": False,
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": artifact_path,
        "error_type": error_type,
        "field": field,
        "current_value": current_value,
        "message": message,
        "suggested_fixes": suggested_fixes,
        "reference": reference,
        "validation_timestamp": datetime.utcnow().isoformat() + "Z"
    }

def emit_success(artifact_id, artifact_path):
    return {
        "valid": True,
        "artifact_id": artifact_id,
        "artifact_path": artifact_path,
        "error_type": None,
        "field": None,
        "current_value": None,
        "message": "Artifact passed all validation checks.",
        "suggested_fixes": [],
        "reference": None,
        "validation_timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

### Step 3: Refactor validation logic

For each check in the validator, emit JSON instead of printing human text.

**Before**:
```python
if primary_fog_type not in VALID_FOG_TYPES:
    print(f"ERROR: Unknown fog type: {primary_fog_type}")
    print(f"Valid values: {VALID_FOG_TYPES}")
    sys.exit(1)
```

**After**:
```python
if primary_fog_type not in VALID_FOG_TYPES:
    error = emit_error(
        error_type="unknown_value",
        field="primary_fog_type",
        current_value=primary_fog_type,
        message=f"Field 'primary_fog_type' has value '{primary_fog_type}', which is not recognized. Valid values are: {', '.join(VALID_FOG_TYPES)}",
        suggested_fixes=[
            f"Change to: primary_fog_type: {valid}" for valid in VALID_FOG_TYPES
        ],
        reference="docs/adr/0011-canonical-vocabulary-enforcement.md"
    )
    print(json.dumps(error))
    sys.exit(1)
```

### Step 4: Test JSON output

For each error condition, verify the JSON is valid.

```bash
# Test syntactic error
python scripts/validate-brief.py artifacts/invalid-brief-missing-fog-type.md
# Output should be valid JSON that can be parsed

python -c "
import json
with open('output.json') as f:
    error = json.load(f)
    assert error['valid'] == False
    assert error['error_type'] == 'missing_field'
"
```

### Step 5: Verify backwards compatibility

Exit codes must remain the same:
- Exit code 0 on success
- Exit code 1 on validation failure

```bash
# Success case
python scripts/validate-brief.py artifacts/valid-brief.md
echo $?  # Should be 0

# Failure case
python scripts/validate-brief.py artifacts/invalid-brief.md
echo $?  # Should be 1
```

---

## Template: Refactored Validator

Here's a template structure for a refactored validator:

```python
#!/usr/bin/env python3
"""
Validate repository_sensemaking_brief artifacts.
Outputs structured JSON to stdout.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import yaml

# Load canonical values
VALID_FOG_TYPES = ['product_fog', 'ui_fog', 'docs_fog', 'architecture_fog']
VALID_WEAKNESS_TYPES = ['architectural', 'product', 'ui', 'docs']

def emit_error(error_type, field, current_value, message, suggested_fixes, reference):
    """Emit structured JSON error."""
    return {
        "valid": False,
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": str(artifact_path),
        "error_type": error_type,
        "field": field,
        "current_value": current_value,
        "message": message,
        "suggested_fixes": suggested_fixes,
        "reference": reference,
        "validation_timestamp": datetime.utcnow().isoformat() + "Z"
    }

def emit_success(artifact_path):
    """Emit success JSON."""
    return {
        "valid": True,
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": str(artifact_path),
        "error_type": None,
        "field": None,
        "current_value": None,
        "message": "Artifact passed all validation checks.",
        "suggested_fixes": [],
        "reference": None,
        "validation_timestamp": datetime.utcnow().isoformat() + "Z"
    }

def validate_brief(artifact_path):
    """Validate repository_sensemaking_brief artifact."""
    
    # Read artifact
    with open(artifact_path) as f:
        content = f.read()
    
    # Parse YAML front matter
    try:
        # Extract YAML from markdown
        lines = content.split('\n')
        yaml_start = lines.index('---')
        yaml_end = lines.index('---', yaml_start + 1)
        yaml_content = '\n'.join(lines[yaml_start+1:yaml_end])
        artifact_data = yaml.safe_load(yaml_content)
    except Exception as e:
        error = emit_error(
            error_type="logic_error",
            field=None,
            current_value=None,
            message=f"Could not parse artifact YAML: {str(e)}",
            suggested_fixes=["Ensure artifact has valid YAML front matter between --- markers"],
            reference="skills/workflow-planner/references/artifact-contracts.yaml"
        )
        print(json.dumps(error))
        return False
    
    # Check 1: primary_fog_type exists
    if 'primary_fog_type' not in artifact_data:
        error = emit_error(
            error_type="missing_field",
            field="primary_fog_type",
            current_value=None,
            message="Required field 'primary_fog_type' is missing.",
            suggested_fixes=[f"Add: primary_fog_type: {ft}" for ft in VALID_FOG_TYPES],
            reference="skills/workflow-planner/references/artifact-contracts.yaml"
        )
        print(json.dumps(error))
        return False
    
    # Check 2: primary_fog_type is valid
    fog_type = artifact_data.get('primary_fog_type')
    if fog_type not in VALID_FOG_TYPES:
        error = emit_error(
            error_type="unknown_value",
            field="primary_fog_type",
            current_value=fog_type,
            message=f"Field 'primary_fog_type' has value '{fog_type}', which is not recognized.",
            suggested_fixes=[f"Change to: primary_fog_type: {ft}" for ft in VALID_FOG_TYPES],
            reference="docs/canonical-vocabulary.yaml"
        )
        print(json.dumps(error))
        return False
    
    # Check 3: evidence exists and is non-empty
    evidence = artifact_data.get('evidence')
    if not evidence:
        error = emit_error(
            error_type="logic_error",
            field="evidence",
            current_value=evidence,
            message="Evidence section is empty or missing.",
            suggested_fixes=[
                "Add evidence items with specific file locations",
                "Example: evidence: ['README.md (lines 15-22): vague feature list', ...]"
            ],
            reference="docs/adr/0003-artifact-composition-pattern.md"
        )
        print(json.dumps(error))
        return False
    
    # Check 4: recommended_workflow_id exists
    workflow_id = artifact_data.get('recommended_workflow_id')
    if not workflow_id:
        error = emit_error(
            error_type="missing_field",
            field="recommended_workflow_id",
            current_value=None,
            message="Required field 'recommended_workflow_id' is missing.",
            suggested_fixes=["Add: recommended_workflow_id: <workflow-id>"],
            reference="skills/workflow-planner/references/workflow-registry.yaml"
        )
        print(json.dumps(error))
        return False
    
    # Check 5: recommended_workflow_id is valid (optional in Phase 1)
    # In Phase 2, add validation against workflow registry
    
    # All checks passed
    result = emit_success(artifact_path)
    print(json.dumps(result))
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-brief.py <artifact_path>")
        sys.exit(1)
    
    artifact_path = Path(sys.argv[1])
    if not artifact_path.exists():
        error = emit_error(
            error_type="logic_error",
            field=None,
            current_value=None,
            message=f"Artifact file not found: {artifact_path}",
            suggested_fixes=["Check that artifact path is correct"],
            reference=None
        )
        print(json.dumps(error))
        sys.exit(1)
    
    success = validate_brief(artifact_path)
    sys.exit(0 if success else 1)
```

---

## Phase 1 Validators to Refactor

### 1. validate-artifact.py

**What it checks**:
- Generic checks (required sections, no absolute paths, etc.)
- Applied to ALL artifacts, not just Phase 1

**Refactoring priority**: HIGH (used by all validators)

**Error types to emit**:
- `missing_field` — required section not found
- `type_error` — wrong data type
- `logic_error` — data is malformed

---

### 2. validate-brief.py

**What it checks**:
- `primary_fog_type` is present and valid
- `evidence` is non-empty
- `recommended_workflow_id` is present
- `weakness_type` is recognized

**Refactoring priority**: HIGH (critical for Phase 1)

**Error types to emit**:
- `missing_field` — any required field missing
- `unknown_value` — enum field has invalid value
- `semantic_conflict` — fog_type contradicts evidence
- `logic_error` — evidence is empty or insufficient

---

### 3. validate-plan.py

**What it checks**:
- `chosen_workflow_id` is valid
- `fog_type` matches `chosen_workflow_id` (alignment check)
- Workflow steps are valid

**Refactoring priority**: MEDIUM (Phase 1, but less critical than brief)

**Error types to emit**:
- `unknown_value` — invalid workflow ID
- `semantic_conflict` — fog_type doesn't match workflow
- `logic_error` — workflow steps are invalid

---

## Testing Your Refactored Validators

### Unit Test Template

```python
import json
import subprocess

def test_missing_field_error():
    """Test that validator emits JSON on missing field."""
    result = subprocess.run(
        ["python", "scripts/validate-brief.py", "fixtures/brief-missing-fog-type.md"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1, "Should fail on missing field"
    
    error = json.loads(result.stdout)
    assert error['valid'] == False
    assert error['error_type'] == 'missing_field'
    assert error['field'] == 'primary_fog_type'
    assert isinstance(error['suggested_fixes'], list)
    assert len(error['suggested_fixes']) > 0

def test_success_case():
    """Test that validator emits success JSON."""
    result = subprocess.run(
        ["python", "scripts/validate-brief.py", "fixtures/brief-valid.md"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Should pass on valid artifact"
    
    success = json.loads(result.stdout)
    assert success['valid'] == True
    assert success['error_type'] is None
```

---

## Backwards Compatibility Notes

### What stays the same
- Exit codes (0 on success, 1 on failure)
- Validation rules (only output format changes)
- Test fixtures (same artifacts are valid/invalid)

### What changes
- Stdout format (human prose → JSON)
- Error messages (in JSON `message` field)

### Fallback for old consumers

If any CLI code expects human-readable output, it will break. But:
1. Phase 1 only affects Phase 1 validators (validate-artifact, validate-brief, validate-plan)
2. Other validators (validate-run-log, validate-output, etc.) remain unchanged
3. Helper script `validate-and-report.py` handles JSON output

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Forgetting to include `reference` field | Always include; points to ADR explaining the rule |
| Making `suggested_fixes` too vague | Be specific: "Change to: primary_fog_type: ui_fog" not "Fix the field" |
| Not setting correct exit code | Exit 0 on success, 1 on failure (backwards compatible) |
| Using non-ISO timestamps | Use `datetime.utcnow().isoformat() + "Z"` |
| Emitting multiple JSON objects | Emit ONE object per run, with `valid: true/false` |
| Not testing JSON validity | Always test: `json.loads(output)` must not raise |

---

## Summary: Refactoring Checklist

For each Phase 1 validator:

- [ ] Identify current validation rules
- [ ] Design JSON error structure for each rule
- [ ] Replace print statements with `emit_error()` calls
- [ ] Keep exit codes unchanged (0 = success, 1 = failure)
- [ ] Test JSON is valid (use `json.loads()`)
- [ ] Test success case produces valid JSON
- [ ] Test failure cases produce appropriate error_type
- [ ] Test backwards compatibility (exit codes work)
- [ ] Document suggested_fixes with concrete examples
- [ ] Add reference links to ADRs/docs

---

## When Refactoring is Complete

All Phase 1 validators:
- ✅ Output JSON to stdout
- ✅ Include all required fields (valid, error_type, field, message, suggested_fixes, reference, timestamp)
- ✅ Use correct error_type (missing_field, unknown_value, semantic_conflict, logic_error, type_error)
- ✅ Keep exit codes unchanged
- ✅ Have JSON tests passing

Agents can then:
- ✅ Parse validator output reliably
- ✅ Understand what went wrong
- ✅ Know what fixes to try
- ✅ Decide whether to retry or escalate
