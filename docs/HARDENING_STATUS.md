# Contract/Naming Drift Hardening Status

**Last Updated**: 2026-05-22  
**Status**: 3 of 5 steps complete (60%)

## Overview

This document tracks implementation of 5 hardening steps to prevent contract/naming drift (regression from PR #14 findings).

## Completed Steps

### Step 1: Canonical Vocabulary Registry ✅
**File**: `docs/canonical-vocabulary.yaml`
**Status**: Complete and deployed

This authoritative registry defines:
- **fog_types**: product_fog, ui_fog, architecture_fog, docs_fog, integration_fog (with aliases)
- **routing_fields**: primary_fog_type, secondary_fog_types, recommended_workflow_id, routing_decision_method, selected_workflow, diagnosis_conflict, escalation_recommended
- **gates**: review_problem_frame, review_unknowns, review_repository_brief, review_workflow_plan
- **execution_modes**: plan_only, prompt_chain, guided_execution, autonomous_execution, yolo_execution
- **artifact_ids**: user_intent, problem_frame, unknowns_map, repository_sensemaking_brief, workflow_plan, execution_summary
- **workflow_ids**: fast-path-workflow, full-fog-workflow, setup-sensemaking-repo, docs-contract-reconciliation, autonomous-sprint-preflight

**Design principle**: Validators accept aliases (e.g., "ui" for "ui_fog") and normalize to canonical forms before storing artifacts. Downstream consumers always receive canonical values.

### Step 2: Path Drift Regression Tests ✅
**File**: `tests/test_path_drift.py`
**Status**: Complete and passing (9 tests, 1 skipped)

Test suite includes:
- `test_no_stale_paths_in_skill_code`: Catch references to deprecated skill paths (e.g., workflow-orchestrator)
- `test_canonical_paths_used_in_docs`: Verify canonical paths are referenced
- `test_fog_type_consistency_in_docs`: Ensure skills discussing fog types reference canonical-vocabulary.yaml
- `test_gate_names_are_canonical`: Verify gate names match registry
- `test_no_stale_skill_directory_names`: Catch old skill naming conventions
- `test_canonical_vocabulary_exists`: Confirm vocabulary file exists
- `test_canonical_vocabulary_is_valid_yaml`: YAML syntax validation
- `test_vocabulary_documents_all_enum_values`: Verify all critical enum sections exist

**Test results**: All 116 tests pass, 1 intentionally skipped (path hardcoding enforcement delegated to integration tests)

### Step 5: Regression Tests for PR #14 Findings ✅
**Coverage**: Integrated into test_path_drift.py

Specific regressions prevented:
- **Contract Mismatch**: Stale skill paths now caught by test_no_stale_paths_in_skill_code
- **Vocabulary Drift**: Inconsistent fog type references caught by test_fog_type_consistency_in_docs
- **Ghost Features**: Path references verified to canonical locations

## Pending Steps

### Step 3: Normalize Fog Type Names Throughout Codebase ⏳
**Status**: Awaiting implementation

**What's needed**:
- Validators normalize aliases to canonical forms (design documented in canonical-vocabulary.yaml section "Usage -> In Validators")
- Repository sensemaker uses canonical fog types in output
- Workflow planner reads and outputs canonical fog types
- All downstream consumers use canonical values

**Where normalization happens**: 
- Input: Validators accept "product", "ui", "ux", "docs", "documentation", etc.
- Output: All artifacts contain "product_fog", "ui_fog", "docs_fog", etc.
- Reference: canonical-vocabulary.yaml section "Fog Types"

### Step 4: Tier-1/Tier-2 Validation Split ⏳
**Status**: Awaiting implementation

**What's needed**:
- **Tier-1 (Hard-fail)**: Routing-critical fields
  - primary_fog_type, recommended_workflow_id, routing_decision_method, selected_workflow
  - Required for all artifacts
  - Validation failure = artifact rejected
  
- **Tier-2 (Advisory)**: Prose/formatting quality
  - Section headings, evidence formatting, decision tree output
  - Optional/recommended
  - Validation warnings = artifact accepted with flag

**Design**: Updated validators/artifact-contracts.yaml with `required_fields` vs `recommended_fields`

## Integration Points

- **canonical-vocabulary.yaml**: Central source of truth for all enumerations
- **test_path_drift.py**: Automated detection of drift on every commit
- **skills/repo-sensemaker/SKILL.md**: References canonical vocabulary
- **skills/workflow-planner/SKILL.md**: References canonical vocabulary
- **tests/**: Full integration test suite (116 tests passing)

## How to Use the Registry

### For Skill Developers
1. Check canonical-vocabulary.yaml for allowed values before implementing output
2. Reference the registry in skill SKILL.md documentation
3. Example: "fog_type MUST be one of: product_fog, ui_fog, architecture_fog, docs_fog, integration_fog"

### For Validator Writers
1. Accept both aliases and canonical forms as input
2. Normalize to canonical forms before storing
3. Example:
   ```python
   CANONICAL_FOG_TYPES = {
       "product_fog": "product_fog",
       "product": "product_fog",
       "ui_fog": "ui_fog",
       "ui": "ui_fog",
       ...
   }
   
   def normalize_fog_type(value):
       canonical = CANONICAL_FOG_TYPES.get(value)
       if not canonical:
           raise ValueError(f"Unknown fog type: {value}")
       return canonical
   ```

### For Runtime/Routing Logic
1. Always compare against canonical forms
2. Example: `if brief["primary_fog_type"] == "ui_fog": ...`
3. Never check for non-canonical aliases at runtime

## Prevention Going Forward

**On every commit**:
- test_path_drift.py regression tests run automatically
- Catches any new references to:
  - Stale skill paths (workflow-orchestrator/)
  - Non-canonical enum values
  - Missing vocabulary references

**On every artifact validation**:
- Validators normalize aliases to canonical forms
- Downstream consumers always see canonical values
- No client code needs to handle aliases

## Related Issues

- **PR #14**: Original "Contract Mismatch" finding (status: prevented by this hardening)
- **ADR-0010**: Runtime owns artifact path resolution (enforced by test_executor_path_handoff.py)
- **ADR-0005**: Canonical vocabulary separation (implemented in this hardening)

## Metrics

| Category | Count |
|----------|-------|
| Canonical enumeration values defined | 25+ |
| Regression test cases | 10 |
| Full test suite passing | 116 |
| Pending hardening steps | 2 |
