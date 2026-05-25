# Phase 1: Consistency Review Report

**Review Date**: 2026-05-24  
**Scope**: Consistency across three Phase 1 planning artifacts  
**Status**: ⚠️ INCONSISTENCIES FOUND — EDITS REQUIRED BEFORE IMPLEMENTATION

---

## Summary

The three Phase 1 artifacts are **80% consistent** with clear vision and aligned scope, but **5 material inconsistencies** and **2 clarifications** must be resolved before implementation begins.

**Risk level**: MEDIUM
- None of the inconsistencies will cause implementation to fail
- But they will cause confusion during execution and create rework
- All issues are fixable with targeted edits (no major rewrites needed)

---

## Detailed Findings

### ✅ CONSISTENT ACROSS ALL THREE ARTIFACTS

These elements are properly aligned:

| Element | Status | Evidence |
|---------|--------|----------|
| **Artifact IDs** | ✅ Consistent | `repository_sensemaking_brief`, `workflow_orchestration_plan`, `user_intent` all referenced consistently |
| **Primary fog types** | ✅ Consistent | All three mention: product_fog, ui_fog, docs_fog, architecture_fog |
| **Validator output format** | ✅ Consistent | JSON structure with valid, error_type, field, message, suggested_fixes, reference all agree |
| **Exit codes** | ✅ Consistent | All say exit 0 on pass, exit 1 on fail |
| **CLI compatibility** | ✅ Consistent | All refer to CLI as "compatibility layer" not "orchestrator" |
| **Source of truth** | ✅ Consistent | artifact-contracts.yaml identified as canonical in all three |
| **Phase 1 scope** | ✅ Consistent | All target fast-path-workflow (repo-sensemaker → workflow-planner → handoff) |
| **Run log recording** | ✅ Consistent | All say helper scripts (not agents) create run logs |

---

## ⚠️ INCONSISTENCIES REQUIRING EDITS

### INCONSISTENCY #1: Error Type Naming (CRITICAL)

**Location**: Bootstrap skill vs. Validator guide  
**Severity**: HIGH (affects agent understanding)

**The Problem**:

Bootstrap skill uses **informal error categories** in section "Handling Validation Errors":
```
Type 1: Syntactic Error (Agent can auto-fix)
Type 2: Semantic Error (Agent can auto-fix with reasoning)  
Type 3: Logic Error (Needs human judgment)
```

But shows formal `error_type` values in examples:
```json
"error_type": "missing_field"
"error_type": "semantic_conflict"
"error_type": "logic_error"
```

Validator guide defines **formal error_type values**:
- `missing_field`
- `unknown_value`
- `semantic_conflict`
- `logic_error`
- `type_error`

**Mapping is incomplete**:
- "Syntactic Error" = missing_field + unknown_value + type_error (but guide lists 3 types, doc lists 5 error_types)
- "Semantic Error" = semantic_conflict (✓ clear)
- "Logic Error" = logic_error (✓ clear)

**Impact**: Agents may be confused about which formal error_type corresponds to which action. "Syntactic Error" doesn't directly map to error_type values.

**Required Edit**:
1. Update bootstrap skill section "Three Types of Validation Errors" to use formal error_type names as headings
2. Change section structure from:
   ```
   Type 1: Syntactic Error (Agent can auto-fix)
   Type 2: Semantic Error
   Type 3: Logic Error
   ```
   To:
   ```
   Missing or Invalid Fields (Agent can auto-fix)
   - missing_field, unknown_value, type_error
   
   Semantic Conflicts (Agent can fix with reasoning)
   - semantic_conflict
   
   Logic Errors (Needs escalation)
   - logic_error
   ```
3. Update the table "When to Auto-Fix vs. Escalate" to reference formal error_types

---

### INCONSISTENCY #2: validation_status Field Placement (CRITICAL)

**Location**: Bootstrap skill vs. Checklist vs. Validator guide  
**Severity**: HIGH (affects artifact structure design)

**The Problem**:

Bootstrap skill **shows validation_status as a field stored IN the artifact**:
```json
{
  "artifact_id": "repository_sensemaking_brief",
  "primary_fog_type": "product_fog",
  "validation_status": {
    "valid": true,
    "error_type": null,
    "message": "Brief passed all validation checks"
  }
}
```
*Agents read `validation_status` from the artifact.*

Validator guide **shows validation_status as validator OUTPUT only**:
```python
def emit_error(...):
    return {
        "valid": false,
        "error_type": "missing_field",
        ...
    }
# This JSON is printed to stdout, not written to artifact
```
*Validators emit JSON; artifact file doesn't contain validation_status.*

Checklist Task 1.4 says:
- "Add `validation_status` to all Phase 1 artifacts"

But Task 2.2 & 2.3 (helper scripts) only handle validator output + run_log recording.

**The Question**: Should validation_status be:
- **Option A**: Stored IN the artifact file (so agents can read it later without re-validating)
- **Option B**: Only in validator output + run_log (so artifacts are pure data; validation is transient)

**Current state**: Inconsistent (bootstrap skill assumes A, validator guide assumes B, checklist is ambiguous)

**Impact**: 
- If A: Skills must write validation_status to artifact after validating (extra complexity)
- If B: Bootstrap skill examples are wrong (must be rewritten)

**Required Clarification & Edit**:

Choose ONE of these paths:

**Path A (validation_status in artifact)**:
1. Add validation_status to artifact-contracts.yaml (Task 1.4)
2. Update validator guide: show how skills write validation_status to artifact after validation
3. Keep bootstrap skill examples as-is
4. Update helper scripts to return validation_status (for agent to write to artifact)

**Path B (validation_status NOT in artifact)**:
1. Remove validation_status from artifact-contracts.yaml (don't add in Task 1.4)
2. Keep validator guide as-is (output only)
3. Update bootstrap skill examples to NOT show validation_status in artifact
4. Update bootstrap skill to say "Agents read validation results from validator output, not artifact"
5. Update checklist Task 1.4 to NOT add validation_status

**Recommendation**: PATH B (validation_status NOT in artifact)
- Reason: Cleaner architecture (artifacts = data; validation = transient check)
- Reason: Simpler for skills (don't need to write back to artifact)
- Reason: Matches run_log model (validation is recorded separately, not in artifact)

---

### INCONSISTENCY #3: workflow_orchestration_plan Missing Fields (MEDIUM)

**Location**: Checklist Task 1.4 vs. Bootstrap skill  
**Severity**: MEDIUM (incomplete artifact definition)

**The Problem**:

Checklist Task 1.4 says to add to `workflow_orchestration_plan`:
- `chosen_workflow_id`
- `routing_decision_method`
- `validation_status`

Bootstrap skill example shows workflow_orchestration_plan has:
- `artifact_id`
- `fog_type` ← **Missing from checklist**
- `chosen_workflow_id`
- `workflow_steps` ← **Not mentioned in checklist**
- `validation_status`

**Missing from both**:
- `routing_decision_method` (checklist mentions it, bootstrap skill doesn't show it)

**Impact**: When updating artifact-contracts.yaml, unclear which fields to add.

**Required Edit**:

Checklist Task 1.4, update "What changes" to include:
- [ ] Add `fog_type` to workflow_orchestration_plan
- [ ] Add `workflow_steps` to workflow_orchestration_plan  
- [ ] Add `routing_decision_method` to workflow_orchestration_plan
- [ ] Add `chosen_workflow_id` to workflow_orchestration_plan
- [ ] Add `validation_status` to workflow_orchestration_plan (if using Path A above)

Or if using Path B: Remove `validation_status` from the list.

---

### INCONSISTENCY #4: Autonomy vs. Escalation (MEDIUM)

**Location**: Bootstrap skill vs. Checklist Task 3.1  
**Severity**: MEDIUM (affects success criteria definition)

**The Problem**:

Bootstrap skill escalation template shows agent **asking the user**:
```
"What would you like me to do?
  1. Change to architecture_fog
  2. Re-analyze the codebase for UI signals
  3. Something else"
```
*This implies agent waits for user input.*

Checklist Task 3.1 success criteria says:
- "Agent never asks you a question (fully autonomous)"

**Contradiction**: If agent escalates by asking questions, it's not "fully autonomous."

**Impact**: Unclear what "success" means for Phase 1.

**Required Clarification & Edit**:

Choose ONE definition:

**Definition A (Fully Autonomous, Never Asks)**:
- Agent handles all errors automatically
- If stuck after 3 retries, agent stops with error message (doesn't ask)
- Success criteria: "Agent completes workflow without requiring user input"

**Definition B (Autonomous with Graceful Escalation)**:
- Agent tries to fix automatically (retries 3x)
- If still stuck, agent escalates by showing structured error + asking for guidance
- Success criteria: "Agent completes workflow autonomously OR escalates gracefully with structured error details"

**Recommendation**: DEFINITION B (more realistic)
- Reason: Some errors require human judgment (can't auto-fix)
- Reason: Escalation is still "intelligent" (not blind)
- Reason: Better UX (user can help when needed)

**Required Edits**:
1. Update checklist Task 3.1 success criteria from:
   - "Agent never asks you a question (fully autonomous)"
   - To: "Agent completes workflow autonomously OR escalates gracefully with structured error + choices"
2. Add example to Checklist Task 3.1 showing what escalation looks like
3. Keep bootstrap skill escalation template as-is

---

### INCONSISTENCY #5: Implementation Workflows in Phase 1 (MEDIUM)

**Location**: Bootstrap skill vs. Checklist scope  
**Severity**: MEDIUM (may confuse agents, but not critical)

**The Problem**:

Bootstrap skill teaches routing to implementation workflows that **don't exist in Phase 1**:
```
"Agent invokes appropriate skill via Skill tool"
"Agent decides next step based on artifact"
"Agent invokes appropriate workflow" → product-implementation-workflow, ui-implementation-workflow, etc.
```

But Checklist Task 3.1 (End-to-end test) says:
- "Agent completes **fast-path-workflow** end-to-end"
- Workflows tested: repo-sensemaker → workflow-planner → handoff
- No product-implementation-workflow, ui-implementation-workflow exist yet

**Impact**: 
- Agents may try to invoke workflows that don't exist
- Agents may misunderstand Phase 1 scope (diagnostic only, not implementation)
- Agent will fail when it tries to invoke product-implementation-workflow in Phase 1

**Required Edit**:

Bootstrap skill section "The Three-Step Diagnosis Pattern" should clarify:
1. Add note: "Phase 1 implements diagnosis only (fast-path-workflow). Implementation workflows (product-implementation-workflow, etc.) are implemented in Phase 2."
2. Update Step 3 example to show routing to fast-path-workflow, not to product-implementation-workflow
3. Add section: "Phase 1 Scope: What's Implemented" explaining what agents can do in Phase 1

Current example shows:
```
Agent: "I detected primary_fog_type: 'product_fog'
Invoking product-implementation-workflow..."
```

Should be updated to Phase 1 scope:
```
Agent: "I detected primary_fog_type: 'product_fog'
Recommended next workflow: product-implementation-workflow (available in Phase 2)
Phase 1 scope complete."
```

---

## ✅ CLARIFICATIONS NEEDED (Not Inconsistencies, but Important)

### CLARIFICATION #1: Retry Count Consistency (LOW)

Bootstrap skill explicitly states **"Try Up To 3 Times, Then Escalate"** but this isn't mentioned in:
- Checklist (no retry count specified)
- Validator guide (validators don't retry)

**Fix**: Add to Checklist Task 2.4 (Update SKILL.md files):
- [ ] Document retry logic (3 attempts with backoff) in each skill's SKILL.md

---

### CLARIFICATION #2: artifact_path Field (LOW)

Validator guide shows both `artifact_id` and `artifact_path` in validator output, which is good.

Bootstrap skill doesn't mention `artifact_path`, which is OK (agents don't need it).

**Status**: No action needed, just noting it's correct.

---

## Summary: Required Edits Before Implementation

### CRITICAL (Must fix)

| Issue | File | Section | Edit Type |
|-------|------|---------|-----------|
| Error type naming | skills/using-sensemaking/SKILL.md.template | "Three Types of Validation Errors" | Rewrite to use formal error_type names |
| validation_status placement | All three files | Artifact definition | Clarify: store in artifact (Path A) or output only (Path B)? |
| workflow_orchestration_plan fields | docs/phase-1-agent-native-implementation-checklist.md | Task 1.4 | Add missing fields (fog_type, workflow_steps, routing_decision_method) |
| Autonomy definition | docs/phase-1-agent-native-implementation-checklist.md | Task 3.1 success criteria | Clarify: fully autonomous OR graceful escalation? |
| Phase 1 scope in bootstrap | skills/using-sensemaking/SKILL.md.template | "The Three-Step Diagnosis Pattern" | Add note explaining Phase 1 = diagnostic only |

### MEDIUM (Should fix)

| Issue | File | Section | Edit Type |
|-------|------|---------|-----------|
| Retry count consistency | docs/phase-1-agent-native-implementation-checklist.md | Task 2.4 | Document retry count (3 attempts) in SKILL.md updates |

---

## READY FOR IMPLEMENTATION CHECKLIST

Before you start implementation, complete these steps:

### Step 1: Choose Your Path (validation_status placement)
- [ ] Read INCONSISTENCY #2 above (two paths described)
- [ ] Choose PATH A (validation_status in artifact) OR PATH B (output only)
- [ ] Document your choice
- [ ] Notify me (affects 3 files)

### Step 2: Choose Your Definition (autonomy)
- [ ] Read INCONSISTENCY #4 above (two definitions described)
- [ ] Choose DEFINITION A (fully autonomous) OR DEFINITION B (with escalation)
- [ ] Document your choice
- [ ] Notify me (affects bootstrap skill + checklist)

### Step 3: Approve Required Edits
Once you choose Paths/Definitions, I will:
- [ ] Update all three artifacts with edits
- [ ] Cross-reference decisions across all files
- [ ] Mark as "READY FOR IMPLEMENTATION"

---

## Impact Analysis

### If edits are NOT made before implementation:

**Scenario A: Developer starts Task 2.1 (validators output JSON)**
- Developer reads validator guide (validation_status is output)
- Developer reads bootstrap skill (validation_status is in artifact)
- Developer asks: "Where does validation_status go?"
- **Blocker**: 2-4 hours lost to clarification

**Scenario B: Developer starts Task 1.4 (update artifact contracts)**
- Developer reads checklist (add chosen_workflow_id, routing_decision_method, validation_status)
- Developer reads bootstrap skill example (also shows fog_type, workflow_steps)
- Developer asks: "Which fields actually belong in the artifact?"
- **Blocker**: 1-2 hours lost to clarification

**Scenario C: Agent tests in Task 3.1**
- Agent reads bootstrap skill, understands Phase 1 = full diagnosis + implementation
- Agent tries to invoke product-implementation-workflow
- Agent fails: workflow doesn't exist
- **Blocker**: Test failure; unclear if Phase 1 is incomplete or agent is wrong

### If edits ARE made before implementation:

- ✅ All developers/agents have single source of truth
- ✅ No ambiguity during implementation
- ✅ Clear success criteria
- ✅ Tasks execute in sequence without blockers

---

## Recommended Next Step

**You have two choices:**

### Option 1: I make edits based on YOUR decisions
1. You choose Path A or B for validation_status
2. You choose Definition A or B for autonomy
3. I update all three artifacts
4. Artifacts marked "READY FOR IMPLEMENTATION"
5. You start Task 1.1

**Effort**: 30 minutes (your decisions) + 1 hour (my edits)

### Option 2: I create decision guide
1. I write detailed comparison of Path A vs B (validation_status)
2. I write detailed comparison of Definition A vs B (autonomy)
3. You review and decide
4. I make edits

**Effort**: 1.5 hours (guides) + decisions + 1 hour (edits)

**Which would you prefer?**

---

## Consistency Review Scorecard

| Category | Status | Notes |
|----------|--------|-------|
| **Artifact IDs & Names** | ✅ Excellent | All consistent |
| **Required Fields** | ⚠️ Needs clarification | workflow_orchestration_plan incomplete |
| **Validator JSON Format** | ✅ Excellent | error_type values clear |
| **Error Type Naming** | ❌ Inconsistent | Formal vs informal naming conflict |
| **Retry/Backoff Rules** | ✅ Good | 3 retries defined in bootstrap skill |
| **Escalation Rules** | ⚠️ Contradicts autonomy | Escalation = asking user |
| **CLI Compatibility** | ✅ Excellent | Consistent across all docs |
| **Source-of-Truth Hierarchy** | ✅ Excellent | artifact-contracts.yaml clear |
| **Phase 1 Scope Boundaries** | ⚠️ Unclear | Bootstrap skill teaches Phase 2 concepts |
| **Overall Score** | 7/10 | Ready with edits; not ready as-is |

---

**Report prepared**: 2026-05-24  
**Edits needed**: 5 critical, 1 medium  
**Time to resolve**: 1-2 hours  
**Status**: ⏳ AWAITING DECISIONS
