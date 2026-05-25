# Phase 1: Required Edits Summary

**Purpose**: Clear list of all edits needed before implementation  
**Triggered by**: Consistency review findings  
**Status**: AWAITING DECISIONS 1 & 2

---

## Decision Requirements

Before edits can be completed, you must decide:

### Decision 1: validation_status Placement
- **PATH A**: Store in artifact file (validation_status is an artifact field)
- **PATH B**: Output only (validation_status is not in artifact; only in validator output + run log)

### Decision 2: Autonomy Definition  
- **DEFINITION A**: Fully autonomous (agent never asks user)
- **DEFINITION B**: Graceful escalation (agent can ask user if stuck)

---

## Conditional Edits (based on Path A vs B)

### IF Decision 1 = PATH A (validation_status in artifact)

#### File: docs/validator-json-refactor-guide.md

**Section**: "JSON Error Format" → Add paragraph after field definitions:

```
**IMPORTANT**: The JSON shown above is the VALIDATOR OUTPUT (stdout). 
After validation, the skill must write validation_status to the artifact file.

The validation_status field in the artifact should match this structure:
{
  "valid": true/false,
  "error_type": null or error_type_string,
  "message": "Human-readable explanation",
  "field": null or field_name,
  "reference": null or reference_url
}

Helper script validate-and-report.py returns this JSON for the skill to embed.
```

**Section**: "Template: Refactored Validator" → Add after function definitions:

```python
# Helper code for skills to write validation_status to artifact
def write_validation_status_to_artifact(artifact_path, validation_result_json):
    """Write validation_status field to artifact after validation."""
    with open(artifact_path) as f:
        artifact = yaml.safe_load(f)
    
    artifact['validation_status'] = json.loads(validation_result_json)
    
    with open(artifact_path, 'w') as f:
        yaml.dump(artifact, f)
```

#### File: docs/phase-1-agent-native-implementation-checklist.md

**Task 1.4**: Update "What changes" section:

Add after `Add 'validation_status' to all Phase 1 artifacts`:
```
- [ ] Update artifact-contracts.yaml to define validation_status field structure
- [ ] Document that validation_status is written by helper scripts after validation
```

**Task 2.2** (validate-and-report.py): Update "What it does" section:

Add bullet:
```
- [ ] Returns JSON that skills will embed in artifact's validation_status field
```

**Task 2.3** (record-validation.py): Update description:

Change "Calls record-validation.py to log the validation attempt" to:
```
- [ ] Helper script returns JSON validation result
- [ ] Helper script also logs validation to run_log.md
- [ ] Skill writes JSON to artifact's validation_status field (see Task 2.2)
```

---

### IF Decision 1 = PATH B (validation_status NOT in artifact)

#### File: skills/using-sensemaking/SKILL.md.template

**Section**: "Reading Artifacts & Making Decisions" → Artifact: repository_sensemaking_brief

**Current**:
```json
{
  "artifact_id": "repository_sensemaking_brief",
  "primary_fog_type": "product_fog",
  "evidence": [...],
  "recommended_workflow_id": "product-implementation-workflow",
  "validation_status": {
    "valid": true,
    "error_type": null,
    "message": "Brief passed all validation checks"
  }
}
```

**Change to**:
```json
{
  "artifact_id": "repository_sensemaking_brief",
  "primary_fog_type": "product_fog",
  "evidence": [...],
  "recommended_workflow_id": "product-implementation-workflow"
}
```

**Section**: "Reading Artifacts & Making Decisions" → Change step 4:

**Current**:
```
4. Read `validation_status` — this tells you if the artifact is valid (see [Handling Validation Errors](#handling-validation-errors))
```

**Change to**:
```
4. Artifact validation is separate — validators output JSON with results (see [Handling Validation Errors](#handling-validation-errors))
   - You do NOT read validation_status from the artifact
   - You read validation_status from the validator output or run_log
```

**Section**: "Artifact: workflow_orchestration_plan"

**Current**:
```json
{
  "artifact_id": "workflow_orchestration_plan",
  "fog_type": "product_fog",
  "chosen_workflow_id": "product-implementation-workflow",
  "workflow_steps": [...],
  "validation_status": {
    "valid": true,
    "error_type": null,
    "message": "Plan passed validation"
  }
}
```

**Change to**:
```json
{
  "artifact_id": "workflow_orchestration_plan",
  "fog_type": "product_fog",
  "chosen_workflow_id": "product-implementation-workflow",
  "workflow_steps": [...]
}
```

**Section**: "Handling Validation Errors" → opening paragraph

**Current**:
```
Sometimes artifacts fail validation. When that happens, the artifact includes a `validation_status` field with error details **in JSON format**.
```

**Change to**:
```
Sometimes artifacts fail validation. When that happens, the validator outputs a JSON error message with details. Validation results are NOT stored in the artifact; they are output by the validator and recorded in the run_log.
```

#### File: docs/phase-1-agent-native-implementation-checklist.md

**Task 1.4**: Update "What changes" section:

**Current**:
```
- [ ] Add `validation_status` to all Phase 1 artifacts
```

**Change to**:
```
- [ ] DO NOT add validation_status to Phase 1 artifacts (validation is separate from artifact data)
```

**Task 1.4**: Update success criteria:

**Current**:
```
- [ ] All Phase 1 artifacts include `validation_status` field
```

**Change to**:
```
- [ ] All Phase 1 artifacts do NOT include validation_status (validation is transient)
```

---

## Conditional Edits (based on Definition A vs B)

### IF Decision 2 = DEFINITION A (Fully Autonomous)

#### File: skills/using-sensemaking/SKILL.md.template

**Section**: "Retry Logic & Escalation" → Remove the "Escalation Template" subsection

**Remove entirely**:
```
### Escalation Template

When you can't auto-fix, escalate to the user with structured information:

I attempted to fix the artifact 3 times, but validation keeps failing.
...
What would you like me to do?
  1. Change to architecture_fog
  2. Re-analyze the codebase for UI signals
  3. Something else
```

**Replace with**:
```
### When Auto-Fix Fails

If you attempt to auto-fix 3 times and validation still fails:
1. Stop the workflow
2. Output the validation error details to the user
3. Do NOT ask the user for guidance; show the error and stop
```

**Section**: "When to Auto-Fix vs. Escalate" → Rewrite table:

**Current**:
```
| Empty evidence section | No | Escalate; requires re-analysis |
| Unclear what the problem is | No | Escalate; show error message to user |
```

**Change to**:
```
| Empty evidence section | No | Stop; show error message to user |
| Unclear what the problem is | No | Stop; show error message to user |
```

#### File: docs/phase-1-agent-native-implementation-checklist.md

**Task 3.1**: Change success criteria:

**Current**:
```
- [ ] Agent never asks you a question (fully autonomous)
```

**Change to**:
```
- [ ] Agent completes workflow without user input (fully autonomous)
- [ ] On error: agent shows error message and stops (doesn't ask for guidance)
```

---

### IF Decision 2 = DEFINITION B (Graceful Escalation)

#### File: docs/phase-1-agent-native-implementation-checklist.md

**Task 3.1**: Update success criteria:

**Current**:
```
- [ ] Agent never asks you a question (fully autonomous)
```

**Change to**:
```
- [ ] Agent completes workflow autonomously OR escalates gracefully when stuck
- [ ] If escalation occurs: agent shows structured error + asks for guidance
```

**Task 3.1**: Add new success criteria:

Add after autonomy criteria:
```
- [ ] If agent gets stuck after 3 retries, it shows:
  - [ ] Artifact being validated
  - [ ] Error type (from JSON error_type field)
  - [ ] Suggested fixes (from JSON suggested_fixes field)
  - [ ] Reference documentation (from JSON reference field)
  - [ ] Offers user choices: "What would you like to do?"
```

#### File: skills/using-sensemaking/SKILL.md.template

**No changes needed** (escalation template is already correct for Definition B)

---

## Unconditional Edits (apply regardless of Decisions)

These edits must be made regardless of which path/definition you choose.

### EDIT 1: Error Type Naming (CRITICAL)

**File**: skills/using-sensemaking/SKILL.md.template

**Section**: "Three Types of Validation Errors"

**Current**:
```markdown
#### **Type 1: Syntactic Error** (Agent can auto-fix)
**Example**: Missing required field

#### **Type 2: Semantic Error** (Agent can auto-fix with reasoning)
**Example**: Field value contradicts evidence

#### **Type 3: Logic Error** (Needs human judgment)
**Example**: Evidence is missing or insufficient
```

**Change to**:
```markdown
#### **Missing or Invalid Fields** (Agent can auto-fix)
Formal error types: `missing_field`, `unknown_value`, `type_error`

**Example (missing_field)**:
{
  "error_type": "missing_field",
  "field": "primary_fog_type",
  ...
}

**Your action**: Add the missing field. Check suggested_fixes for allowed values.

#### **Semantic Conflicts** (Agent can auto-fix with reasoning)
Formal error type: `semantic_conflict`

**Example**:
{
  "error_type": "semantic_conflict",
  "field": "primary_fog_type",
  "current_value": "ui_fog",
  ...
}

**Your action**: Read the evidence. Reason about whether fog_type is correct. Fix if confident, retry.

#### **Logic Errors** (Needs escalation)
Formal error type: `logic_error`

**Example**:
{
  "error_type": "logic_error",
  "message": "Evidence section is empty...",
  ...
}

**Your action**: This requires context or re-analysis. Escalate or stop (depending on your phase definition).
```

**Section**: "When to Auto-Fix vs. Escalate" → Update table to reference formal error_type values:

**Current**:
```
| Scenario | Auto-Fix? | Example |
|----------|-----------|---------|
| Missing field | Yes | Add `primary_fog_type: product_fog` |
| Wrong enum value | Yes if suggested_fixes exist | Change `ui_fog` → `architecture_fog` |
```

**Change to**:
```
| Scenario | Error Type | Auto-Fix? | Example |
|----------|-----------|-----------|---------|
| Missing field | missing_field | Yes | Add `primary_fog_type: product_fog` |
| Wrong enum value | unknown_value | Yes if suggested_fixes | Change `ui_fog` → `architecture_fog` |
| Type mismatch | type_error | Yes | Change array to string |
| Field contradicts evidence | semantic_conflict | Maybe | Fog type vs evidence |
| Empty/insufficient data | logic_error | No | Evidence is empty |
```

---

### EDIT 2: workflow_orchestration_plan Fields (CRITICAL)

**File**: docs/phase-1-agent-native-implementation-checklist.md

**Task 1.4**: Update artifact contract changes

**Current**:
```
- [ ] Add `chosen_workflow_id` to workflow_orchestration_plan
- [ ] Add `routing_decision_method` to workflow_orchestration_plan
```

**Change to**:
```
- [ ] Add `fog_type` to workflow_orchestration_plan
- [ ] Add `chosen_workflow_id` to workflow_orchestration_plan
- [ ] Add `routing_decision_method` to workflow_orchestration_plan
- [ ] Add `workflow_steps` to workflow_orchestration_plan
  - workflow_steps is an array of step objects
  - Each step object has: step_id, skill, input_artifact, output_artifact, gate, description
```

---

### EDIT 3: Phase 1 Scope Clarification (CRITICAL)

**File**: skills/using-sensemaking/SKILL.md.template

**Section**: "The Three-Step Diagnosis Pattern" → Add new subsection before Step 1:

```markdown
### Phase 1 Scope: What You Can Do

Phase 1 implements **diagnostic workflows only**. You can:
- ✅ Diagnose fog type (repo-sensemaker)
- ✅ Understand routing (workflow-planner)
- ✅ Prepare for implementation (handoff)

You CANNOT yet:
- ❌ Implement product workflows (Phase 2)
- ❌ Implement UI workflows (Phase 2)
- ❌ Implement docs workflows (Phase 2)
- ❌ Implement architecture workflows (Phase 2)

**If you encounter product-implementation-workflow or similar in examples, those are Phase 2 workflows not yet implemented.**
```

**Section**: "The Three-Step Diagnosis Pattern" → Step 3: Update example

**Current**:
```
**Your action:**
```
I detected primary_fog_type: "product_fog"
This indicates unclear user needs and feature scope.
Invoking product-implementation-workflow...
[invoke product-implementation-workflow skill]
```
```

**Change to**:
```
**Your action:**
```
I detected primary_fog_type: "product_fog"
This indicates unclear user needs and feature scope.

Phase 1 diagnosis complete. Implementation workflows (product-implementation-workflow, etc.) are available in Phase 2.
```
```

---

### EDIT 4: Retry Count Documentation

**File**: docs/phase-1-agent-native-implementation-checklist.md

**Task 2.4**: Update description

**Current**:
```
**What each SKILL.md now includes**:
...
**If validation fails**:
- Agent reads validation_status.error_type
- Agent reads validation_status.suggested_fixes
- Agent retries with adjustments (up to N times)
```

**Change to**:
```
**What each SKILL.md now includes**:
...
**If validation fails**:
- Agent reads error_type from validator output
- Agent reads suggested_fixes from validator output
- Agent retries with adjustments (up to 3 times max)
- On 4th attempt: agent escalates or stops (depending on phase definition)
```

---

## Edit Application Workflow

### Step 1: Make your decisions
Fill in Decision 1 and Decision 2 in `docs/phase-1-ready-for-implementation-checklist.md`

### Step 2: Apply conditional edits
- If PATH A: Apply all edits in "IF Decision 1 = PATH A" section
- If PATH B: Apply all edits in "IF Decision 1 = PATH B" section
- If DEFINITION A: Apply all edits in "IF Decision 2 = DEFINITION A" section
- If DEFINITION B: Apply all edits in "IF Decision 2 = DEFINITION B" section

### Step 3: Apply unconditional edits
Apply all edits in "Unconditional Edits" section (all 4 edits)

### Step 4: Verify
- All three artifacts have been updated
- No conflicting changes
- All examples are internally consistent
- Cross-references are correct

### Step 5: Mark as ready
Update `docs/phase-1-ready-for-implementation-checklist.md`:
- [ ] Sign off on all edits
- [ ] Mark as "READY FOR IMPLEMENTATION"
- [ ] Start Task 1.1

---

## Total Edit Effort

**Decision making**: 15-30 minutes  
**Conditional edits**: 30-45 minutes (depending on paths/definitions)  
**Unconditional edits**: 45-60 minutes  
**Verification**: 15-20 minutes  

**Total**: 1.5-2.5 hours before implementation can begin

---

## Questions?

If any edit is unclear:
1. Check the original inconsistency in `docs/phase-1-consistency-review.md`
2. Read the pro/con analysis for your decision
3. Ask for clarification before applying edits

No edits are applied until you've made both decisions and understand the rationale.
