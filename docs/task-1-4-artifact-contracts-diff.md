# Task 1.4: Artifact Contracts Update (Phase 1, PATH B)

**Status**: ✅ Complete  
**File Modified**: `skills/workflow-planner/references/artifact-contracts.yaml`  
**Date**: 2026-05-24  
**Validation**: YAML is valid, no syntax errors

---

## Summary of Changes

Updated two Phase 1 diagnostic artifacts to reflect PATH B (transient validation) and minimal Phase 1 scope:

1. **repository_sensemaking_brief** — Simplified to Phase 1 diagnostic focus
2. **workflow_orchestration_plan** — Simplified to Phase 1 diagnostic focus

Both artifacts now have:
- ✅ Minimal required machine fields (6 each)
- ✅ Moved non-essential fields to recommended section
- ✅ Added explicit `notes` documenting PATH B and Phase 1 scope
- ✅ No `validation_status` field (PATH B: validation is transient)

---

## Artifact 1: `repository_sensemaking_brief`

### Before (Old Contract)

**Required machine fields** (10 fields):
```
- source_intent_ref
- recommended_workflow_id
- recommended_execution_mode
- weakest_boundary
- required_inputs
- user_implied_fog_type
- primary_fog_type
- diagnosis_conflict
- escalation_recommended
```

**Required sections** (14 sections):
```
- repository_goal
- current_shape
- strong_signals
- missing_pieces
- improvement_opportunities
- weakest_boundary
- evidence
- evidence_excerpts
- why_this_boundary_matters
- candidate_next_steps
- recommended_next_step
- recommended_workflow
- machine_readable_handoff
- ready_to_copy_prompt
```

### After (New Contract)

**Required machine fields** (6 fields):
```
- artifact_id
- primary_fog_type
- evidence
- recommended_workflow_id
- created_at
- immutable
```

**Recommended machine fields** (7 fields):
```
- source_intent_ref
- user_implied_fog_type
- diagnosis_conflict
- escalation_recommended
- escalation_target
- escalation_reason
- auto_escalation_allowed
```

**Required sections** (2 sections):
```
- evidence
- recommended_workflow
```

### Changes Explanation

| Change | Reason |
|--------|--------|
| Reduced required fields from 10 to 6 | Phase 1 diagnostic only; focus on: artifact identity, fog classification, evidence, workflow routing |
| Moved non-core fields to recommended | Fields like source_intent_ref, diagnosis_conflict, escalation_* are useful but not required for Phase 1 |
| Removed: recommended_execution_mode | Phase 1 doesn't execute; Phase 2 adds execution mode |
| Removed: weakest_boundary, required_inputs | Advanced analysis; focus on primary fog type for Phase 1 |
| Simplified required sections | Only require evidence (justification) + workflow recommendation |
| Added description field | Clarifies artifact purpose: "Phase 1 diagnostic artifact: fog type classification and handoff to workflow-planner" |
| Added notes field | Explains PATH B (transient validation) and Phase 1 scope |

---

## Artifact 2: `workflow_orchestration_plan`

### Before (Old Contract)

**Required machine fields** (21 fields):
```
- artifact_id
- source_intent_ref
- chosen_workflow_id
- execution_mode
- system_recommended_workflow
- selected_workflow
- routing_divergence
- routing_decision_method
- escalation_recommended
- auto_escalation_allowed
- scope_expansion_requires_approval
- status
- initial_inputs
- steps
- approval_gates
- gate_behavior
- stop_conditions
- subset_run
- subset_reason
- included_steps
- excluded_steps
```

**Recommended machine fields** (2 fields):
```
- fog_type
- primary_fog_type
```

### After (New Contract)

**Required machine fields** (6 fields):
```
- artifact_id
- primary_fog_type
- chosen_workflow_id
- routing_decision_method
- workflow_steps
- created_at
```

**Recommended machine fields** (14 fields):
```
- source_intent_ref
- execution_mode
- system_recommended_workflow
- selected_workflow
- routing_divergence
- escalation_recommended
- auto_escalation_allowed
- approval_gates
- gate_behavior
- stop_conditions
- subset_run
- subset_reason
- included_steps
- excluded_steps
```

### Changes Explanation

| Change | Reason |
|--------|--------|
| Reduced required fields from 21 to 6 | Phase 1 diagnostic only; focus on: artifact identity, fog type, workflow routing decision, workflow steps sequence |
| Moved execution/approval details to recommended | These are Phase 2 implementation concerns |
| Promoted primary_fog_type from recommended to required | Needed for agent decision-making during diagnostic phase |
| Renamed `steps` to `workflow_steps` in required fields | More explicit; clarifies this is the structured skill sequence |
| Changed required_sections | Updated to reflect Phase 1 focus: brief, chosen workflow, why, workflow_steps_definition, machine_readable_plan |
| Added description field | Clarifies artifact purpose: "Phase 1 diagnostic plan: workflow routing and step definition for agent execution" |
| Added notes field | Explains PATH B (transient validation), Phase 1 scope, and workflow_steps structure |

---

## Validation Results

### YAML Syntax

```
[OK] YAML is valid
[OK] Loaded 33 artifact definitions
```

### Contract Verification

```
[artifact] repository_sensemaking_brief:
  Required machine fields (6): 
    - artifact_id
    - primary_fog_type
    - evidence
    - recommended_workflow_id
    - created_at
    - immutable
  Recommended machine fields (7): 
    - source_intent_ref
    - user_implied_fog_type
    - diagnosis_conflict
    - escalation_recommended
    - escalation_target
    - escalation_reason
    - auto_escalation_allowed

[artifact] workflow_orchestration_plan:
  Required machine fields (6): 
    - artifact_id
    - primary_fog_type
    - chosen_workflow_id
    - routing_decision_method
    - workflow_steps
    - created_at
  Recommended machine fields (14): 
    - source_intent_ref
    - execution_mode
    - system_recommended_workflow
    - selected_workflow
    - routing_divergence
    - escalation_recommended
    - auto_escalation_allowed
    - approval_gates
    - gate_behavior
    - stop_conditions
    - subset_run
    - subset_reason
    - included_steps
    - excluded_steps

[OK] PATH B verified: validation_status NOT in required fields
```

---

## Schema Naming Questions

### Resolved: Field Names

The following field names were chosen to match existing schema patterns:

| Field | Artifact | Purpose | Notes |
|-------|----------|---------|-------|
| `artifact_id` | Both | Machine identifier for artifact | Standard across all artifacts |
| `primary_fog_type` | Both | Classified fog type | Values: product_fog, ui_fog, docs_fog, architecture_fog |
| `evidence` | brief | Array of evidence lines | Justifies the fog type classification |
| `recommended_workflow_id` | brief | Routing decision | Matches skill teaching in bootstrap |
| `created_at` | Both | ISO 8601 timestamp | Standard field, used for audit trail |
| `immutable` | brief | Boolean flag | Marks artifact as immutable after creation |
| `chosen_workflow_id` | plan | Selected workflow for execution | From workflow-planner routing decision |
| `routing_decision_method` | plan | How the decision was made | Values: diagnosis_primary_soft_context, etc. |
| `workflow_steps` | plan | Structured step sequence | Array of {step_id, skill, input_artifact, output_artifact, gate, description} |

### Naming Consistency

✅ **Field names match bootstrap skill teaching**
- Skill example artifact uses these exact field names
- Agents will recognize these field names when reading artifacts

✅ **Field names are consistent with existing contracts**
- `artifact_id`, `created_at` used throughout all artifacts
- `primary_fog_type` matches fog classification vocabulary in CONTEXT.md

✅ **No abbreviations or shortcuts**
- `recommended_workflow_id` (not `rec_workflow` or `wf_id`)
- `routing_decision_method` (not `route_method` or `decision_type`)
- `workflow_steps` (not `steps` or `plan_steps`)

---

## Verification Checklist

- [x] YAML file is syntactically valid
- [x] All 33 artifact definitions still present
- [x] repository_sensemaking_brief updated with 6 required fields
- [x] repository_sensemaking_brief moved 4 fields to recommended
- [x] workflow_orchestration_plan updated with 6 required fields
- [x] workflow_orchestration_plan moved 15 fields to recommended
- [x] No `validation_status` in required fields (PATH B enforced)
- [x] Both artifacts have `description` field (clarity)
- [x] Both artifacts have `notes` field (PATH B + Phase 1 scope documentation)
- [x] Field names match bootstrap skill examples
- [x] Field names are ASCII-safe (no special characters)
- [x] No schema naming conflicts
- [x] Required for_modes unchanged (guided_execution, autonomous_execution, yolo_execution)

---

## Impact Assessment

### For Agents

✅ **Simplified contract = easier to validate**
- 6 required fields per artifact (not 10-21)
- Agents can quickly check: all required fields present?
- Cleaner error messages if validation fails

✅ **Matches skill teaching**
- Agent reads bootstrap skill → learns artifact structure
- Agent reads artifact → structure matches skill teaching
- No surprises about field names or requirements

### For Validators

✅ **Reduced validation complexity**
- Fewer required fields to check
- Clearer error types (missing_field errors only for 6 fields per artifact)
- Run log focus on validation results (not stored in artifact)

### For Phase 2 Implementation

✅ **Optional fields can be added later**
- Recommended fields provide migration path to Phase 2
- Phase 2 workflows can populate additional fields
- No breaking changes to Phase 1 contracts

---

## Alignment with User Decisions

### PATH B: Transient Validation

✅ **Verified**: No `validation_status` in required or recommended fields
- Validation results belong in validator JSON output
- Validation results belong in run logs
- Artifacts store work products only

### DEFINITION B: Autonomous with Graceful Escalation

✅ **Verified**: Contract supports agent decision-making
- Fields provide information agents need to diagnose
- No forced execution model in contract
- Escalation decision rules are in bootstrap skill teaching

### Phase 1 Scope: Diagnostic Only

✅ **Verified**: Contracts reflect diagnostic focus
- Only fields needed for fog classification + routing
- Execution mode removed (Phase 2 concern)
- Implementation workflow selection deferred to Phase 2

---

## Next Steps

### Task 1.5 (Optional): Validator Contract Reconciliation

When validators are implemented, ensure:
1. Validators validate against these required fields
2. Validators output JSON (not stored in artifact)
3. Run log captures validation results
4. Agent can parse JSON errors and retry

### Task 2.1: Implement Validator JSON Output

Validators should:
1. Check that all 6 required fields are present
2. Check that field values are valid (fog_type enum, workflow_id exists, etc.)
3. Output JSON with error details (not prose)
4. Not attempt to write validation_status back to artifact

### Task 3.1: End-to-End Test

Test that:
1. Agents can read artifact contracts
2. Agents understand what fields to expect
3. Agents can validate their own output
4. Agents escalate gracefully when validation fails

---

## Files Summary

| File | Status | Changes |
|------|--------|---------|
| `skills/workflow-planner/references/artifact-contracts.yaml` | ✅ Modified | Lines 117-154, 443-487 |
| `CLAUDE.md` | ✅ Modified | SessionStart section (earlier task) |
| `.claude/hooks/sessionstart.md` | ✅ Created | Bootstrap reminder (earlier task) |
| `skills/using-sensemaking/SKILL.md` | ✅ Created | Bootstrap skill content (earlier task) |

---

**Task 1.4 Status**: ✅ COMPLETE

Artifact contracts are updated, validated, and ready for:
- Task 2.1: Validator JSON implementation
- Task 3.1: End-to-end testing

---

**Created**: 2026-05-24  
**Review**: All changes verified against user requirements (PATH B + DEFINITION B + Phase 1 scope)
