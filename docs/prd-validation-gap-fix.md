# PRD Validation Gap: Root Cause & Fix Plan

**Date**: 2026-05-16  
**Issue**: docs-architecture guided_execution (step 2: to-prd) claims to produce prd.md but artifact doesn't exist on disk. Validator dispatcher marked as "none (no artifact to validate)" instead of validating or failing.  
**Priority**: Medium (affects future workflows that consume prd: to-issues, product sprints)  
**Impact**: Low immediate (prd is not yet used in active workflows, but will be needed for product-to-issues workflow)

---

## Root Cause Analysis

### What Happened
1. **Step 1 (grill-with-docs)**: Produced domain_alignment_report.md ✅
2. **Step 2 (to-prd)**: Claimed to complete with status COMPLETED, but:
   - No prd.md file exists on disk
   - Validator stack marked as "none (no artifact to validate)"
   - No PASSED or FAILED result for validator
3. **Step 3 (handoff)**: Claimed step 2's prd as input, but file doesn't exist
   - How did handoff complete without its required input?
   - Possible: handoff fell back to using domain_alignment_report directly, or never required the file to exist

### Why This Happened
The orchestration runner has lenient artifact checking:
```python
# Line 430-447 in orchestration-runner.py
if artifact_path and os.path.exists(artifact_path):
    # Validate if it exists
else:
    # Just print a message and continue
    print(f"  ~ Artifact '{output_artifact}' not yet produced...")
```

This is appropriate for `plan_only` mode (no artifacts should exist yet), but NOT for `guided_execution` or `yolo_execution` modes where skills actually execute and produce artifacts.

### The Real Problem
The orchestrator doesn't distinguish between:
1. **Plan mode**: Artifacts don't exist because we're not executing (OK to skip validation)
2. **Execution modes**: Artifacts should exist because skills actually ran (NOT OK to skip validation)

For execution modes, missing artifacts should trigger:
- Either a validation failure (if the contract requires validation)
- Or at least a clear ERROR/FAILED status in the run log

---

## Three Possible Fixes

### Option A: Enforce Strict Artifact Validation in Execution Modes (RECOMMENDED)
**Rule**: For guided_execution, autonomous_execution, and yolo_execution modes:
- If a step claims `output_artifact: X` and contract exists, the file MUST exist after execution
- If file doesn't exist, mark step as FAILED with error code ARTIFACT_NOT_FOUND
- If file exists, MUST validate through validate-output.py dispatcher
- No "none (no artifact to validate)" for execution modes

**Why**: Catches skill execution failures early. If to-prd doesn't produce prd.md, we know immediately.

**Implementation**:
```python
# In orchestration-runner.py, after skill execution
if mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
    if output_artifact and contract_exists(artifact_id):
        if not os.path.exists(artifact_path):
            # FAIL: artifact expected but not produced
            result["status"] = "FAILED"
            errors.append(ARTIFACT_NOT_FOUND)
            return result
```

### Option B: Move PRD to a Later Workflow Step (CONDITIONAL)
**Rule**: PRD generation should happen only when PRD will actually be consumed.

**Current workflow**:
```
docs-architecture workflow:
  Step 1: grill-with-docs → domain_alignment_report
  Step 2: to-prd → prd (but prd is not consumed in this workflow!)
  Step 3: handoff → prompt_handoff
```

**Proposed**:
```
docs-architecture workflow:
  Step 1: grill-with-docs → domain_alignment_report
  Step 2: handoff → prompt_handoff

product-to-issues workflow (NEW):
  Step 1: to-prd (domain_alignment_report) → prd
  Step 2: to-issues (prd) → issue_list
  Step 3: triage (issue_list) → agent_brief
```

**Why**: PRD is only consumed by to-issues and product workflows. Generating it in docs-architecture is premature.

**Tradeoff**: Requires creating a new workflow and adjusting workflow composition logic.

### Option C: Make PRD Optional in docs-architecture
**Rule**: Mark the step 2 artifact as optional if it's not consumed downstream.

```yaml
steps:
  - id: 2
    skill: to-prd
    step_type: local_execution
    gate: review_prd
    input_artifact: domain_alignment_report
    output_artifact: prd
    optional: true  # NEW: skip validation if not produced
    validation: none  # NEW: intentionally unvalidated
```

**Why**: Allows the workflow to continue even if to-prd doesn't produce output.

**Tradeoff**: Reduces confidence in the system (why even run to-prd if we don't validate?).

---

## Recommendation: Option A + Option B

### Why
1. **Option A** (enforce strict validation) fixes the system's ability to detect failures early
2. **Option B** (move PRD to later workflow) fixes the workflow design to match the data flow

Combined:
- Enforce strict validation in all execution modes (catches bugs immediately)
- Move prd generation to a workflow that actually consumes it (better design)
- Keep docs-architecture focused on its stated purpose: "Turn an approved brief or PRD into copy-paste prompts"

### Implementation Steps

#### Step 1: Update orchestration-runner.py
- Add mode-aware artifact validation logic
- For execution modes: FAIL if artifact expected but not produced
- For plan modes: OK to skip (artifacts don't exist yet)

#### Step 2: Create product-to-issues workflow
```yaml
- id: product-to-issues
  display_name: Product PRD to Implementation Issues
  purpose: Transform PRD into implementation issues and agent briefs
  initial_inputs:
    - id: domain_alignment_report
      type: artifact
      required: true
      description: Previous domain alignment output
  allowed_execution_modes:
    - guided_execution
    - autonomous_execution
  steps:
    - id: 1
      skill: to-prd
      input_artifact: domain_alignment_report
      output_artifact: prd
    - id: 2
      skill: to-issues
      input_artifact: prd
      output_artifact: issue_list
    - id: 3
      skill: triage
      input_artifact: issue_list
      output_artifact: agent_brief
```

#### Step 3: Update docs-architecture workflow
Remove step 2 (to-prd) entirely. Workflow becomes:
```yaml
- id: docs-architecture
  steps:
    - id: 1
      skill: grill-with-docs
      output_artifact: domain_alignment_report
    - id: 2  # was step 3
      skill: handoff
      input_artifact: domain_alignment_report
      output_artifact: prompt_handoff
```

#### Step 4: Update mode-coverage.yaml
Document the PRD validation gap as an implementation decision:
- Root cause: to-prd not needed in docs-architecture workflow (PRD is only consumed by to-issues)
- Resolution: Moved PRD generation to product-to-issues workflow
- Validator coverage: prd now validated when actually produced (in product-to-issues)

---

## Testing Plan

After implementing the fix:

1. **Strict Validation Enforcement**:
   - Run controlled failure test: to-prd returns early without producing prd.md
   - Verify: Step 2 fails with ARTIFACT_NOT_FOUND
   - Verify: Run log records validator_stack with FAILED result

2. **Workflow Redesign**:
   - Run docs-architecture (shortened version, 2 steps)
   - Verify: All steps complete successfully
   - Verify: Only domain_alignment_report and prompt_handoff produced

3. **New product-to-issues Workflow**:
   - Run product-to-issues with domain_alignment_report input
   - Verify: All 3 steps complete
   - Verify: prd.md validated via dispatcher
   - Verify: issue_list produced and validated

4. **Evidence Coverage**:
   - Update mode-coverage.yaml to reflect new workflows
   - Verify: All artifact contracts are now satisfied in their respective workflows

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Strict validation too aggressive | Add `optional: true` flag for intentionally un-produced artifacts (future feature) |
| Removing step from docs-architecture breaks users | No documented users yet; workflow is under active development |
| product-to-issues workflow not needed yet | Add to registry as `plan_only` initially, enable guided_execution when to-issues is tested |
| Validation changes break existing runs | Runs are ephemeral; only mode-coverage.yaml is long-lived (update it) |

---

## Not Recommended

❌ **Option C (make PRD optional)**: Reduces system confidence. If prd is not needed, don't try to produce it. If it is needed, validate it.

❌ **Keep current state**: Leaves a gap in the evidence layer that will multiply as more artifacts are added.

---

## Next Action

Proceed with Option A + Option B once the user confirms direction.
