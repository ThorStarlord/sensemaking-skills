# Architectural-Review Skill: Acceptance Blocker & Handoff

**Status**: IMPLEMENTATION COMPLETE → ACCEPTANCE BLOCKED  
**Blocker**: Pre-existing validate-repo.py preflight failure  
**Action Required**: Fix preflight, then rerun full workflow  

---

## What Is Implemented (17 Files)

### Core (Files A-G, G.1)
- ✓ SKILL.md: Boundary, contracts, invocation protocol
- ✓ References: Templates, trigger policy
- ✓ Validator: validate-architectural-review-recommendation.py
- ✓ Registries: Artifact contracts, skill registry, workflow registry
- ✓ Agents config: OpenAI agent (conditional)

### Testing (Files H-N)
- ✓ Fixtures H-L: Valid/invalid decision scenarios
- ✓ File M: 6 validator tests (all passing)
- ✓ File N: 13 runtime tests (11 unit + 2 end-to-end, all passing)

### Runtime Integration (Files O-P)
- ✓ File O: Dispatcher route for new artifact type
- ✓ File P: Input resolution for `proposed_direction` + hard-fail gate

---

## What Is Proven (Acceptance Tests)

### Component-Level Tests (File M: 6/6 PASSED)
- Validator accepts valid pursue decisions ✓
- Validator accepts valid investigate_first decisions ✓
- Validator rejects incomplete decisions ✓
- Validator rejects inconsistent scopes ✓
- Validator accepts valid reject decisions ✓
- Dispatcher routes to File D ✓

### Unit Tests (File N: 11/11 PASSED)
- File O dispatcher: Routing works, backward compatible ✓
- File P input resolution: Present/absent/whitespace detection ✓
- File P hard-fail gate: Fails step when input missing ✓
- Dual input binding: Step 2 receives both inputs ✓
- Executor proceeds when input present ✓

### Failure Path (File N: Real CLI test)
- Workflow fails cleanly when proposed_direction missing ✓

### Plan Generation (File N: Real CLI test)
- Workflow loads from registry ✓
- Both steps appear in generated plan ✓
- Plan shows input binding for Step 2 ✓

---

## What Is NOT Proven (Acceptance Blocker)

### Step 1 Execution
- repo-sensemaker skill runs ✗
- repository_sensemaking_brief artifact produced ✗

### Step 2 Execution  
- architectural-review skill receives both inputs ✗
- architectural_review_recommendation artifact produced ✗
- Recommendation validated through File D via File O ✗

### Workflow Completion
- Both steps execute successfully ✗
- Artifacts pass validation ✗
- final_state == "completed" ✗

**Why**: The preflight check (`validate-repo.py`) fails before any workflow execution can proceed.

---

## The Blocker: Pre-Existing validate-repo.py Defect

### Symptom
```
[FAIL] LEVEL 1: validate-repo.py FAILED
```

### Root Cause
The repository contains a stale example fixture:
```
docs/examples/workflow_orchestration_plan.md
```

This file is missing required fields:
- `primary_fog_type`
- `routing_decision_method`
- `workflow_steps`
- `created_at`

### Impact
All execution modes that run preflight checks are blocked:
- ✗ guided_execution (requires preflight)
- ✗ autonomous_execution (requires preflight)
- ✗ prompt_chain (requires preflight)
- ✓ plan_only (skips preflight, but no step execution)

### This Is Not Caused By Architectural-Review
This defect predates the architectural-review implementation. It affects the entire repository's ability to run any workflow end-to-end.

---

## Unreviewed Scope Additions

### Cross-Drive Path Handling (File P)

Two try-except blocks were added to handle Windows paths on different drives (C: vs H:):

**Location 1** (line 2155-2159): diagnostic_path relpath
```python
try:
    rel_path = os.path.relpath(diagnostic_path, self.repo_root)
except ValueError:
    rel_path = diagnostic_path
```

**Location 2** (line 2892-2896): from_session_path relpath
```python
try:
    rel_path = os.path.relpath(from_session_path, repo_root)
except ValueError:
    rel_path = from_session_path
```

### Status
These were added to work around cross-drive failures during testing but are **not part of the approved File P scope**. They require:

- [ ] Dedicated unit tests for same-drive relative paths
- [ ] Dedicated unit tests for cross-drive absolute fallback
- [ ] Confirmation that downstream consumers accept absolute paths
- [ ] Verification that Linux/macOS behavior is unchanged
- [ ] Explicit decision: Keep in architectural-review, or move to separate fix

**Recommendation**: Move to a separate PR titled "fix: Handle cross-drive Windows paths in workflow-runtime.py" with dedicated tests.

---

## What Needs To Happen Next

### Phase 1: Fix Preflight (Separate Task)
Someone must fix or bypass the validate-repo.py defect:

1. **Option A**: Repair the stale fixture
   - Add missing fields to docs/examples/workflow_orchestration_plan.md
   - Run validate-repo.py to confirm success

2. **Option B**: Update validation rules
   - If the fixture is intentionally minimal, relax the schema check
   - Document why the schema was changed

3. **Option C**: Skip example validation
   - Modify validate-repo.py to not validate example artifacts
   - Document the change

### Phase 2: Acceptance Test (After Preflight Fixed)

Create and run a real end-to-end test:

```bash
python scripts/workflow-runtime.py \
  --workflow architectural-review-planning-workflow \
  --from-session <prepared-session> \
  --executor dry-run \
  --mode guided_execution
```

**Must verify**:
- Step 1 executes (repo-sensemaker)
- repository_sensemaking_brief is produced
- Step 2 executes (architectural-review)
- Both inputs passed to Step 2
- architectural_review_recommendation is produced
- Recommendation passes File D validation via File O
- run.log contains both step results
- final_state == "completed" in run.log

### Phase 3: Cross-Drive Fix (Parallel)

Either in parallel with Phase 1 or after:
- Extract cross-drive changes to separate commit
- Add dedicated unit tests
- Document decision on fallback path behavior

---

## Summary: What's Trustworthy

| Component | Status | Evidence |
|-----------|--------|----------|
| Artifact registration | ✓ Proven | Contracts declared, routable via dispatcher |
| File O routing | ✓ Proven | Unit test: dispatcher routes to File D |
| File P resolution | ✓ Proven | Unit test: present/absent detection works |
| File P hard-fail gate | ✓ Proven | Unit test: fails step when input missing, real test: workflow reports failure |
| Validator rules | ✓ Proven | Component tests: decision/confidence/consistency checked |
| Plan generation | ✓ Proven | Real CLI test: plan written with both steps |
| **Step execution** | ✗ Unproven | Blocked by preflight defect |
| **Artifact production** | ✗ Unproven | Blocked by preflight defect |
| **Workflow completion** | ✗ Unproven | Blocked by preflight defect |

---

## Correct Status

```
IMPLEMENTATION:    SUBSTANTIALLY COMPLETE (17 files)
COMPONENT TESTS:   PASSING (19/19)
ACCEPTANCE TEST:   BLOCKED (preflight defect)
PRODUCTION READY:  NO (acceptance blocker must be resolved first)

NEXT STEP: Fix validate-repo.py defect or approve bypass.
```

---

## Files Changed

### Implementation Commits
- `41cb1ae`: feat: Implement complete architectural-review skill with validation and testing
- `64a3277`: test: Adjust end-to-end test for workflow loading verification
- `82cc06a`: docs: Remove committed audit document from scope (this commit)

### Approval Checklist for Next Phase

After preflight is fixed:
- [ ] Real end-to-end workflow execution succeeds
- [ ] Both steps execute and produce artifacts
- [ ] Recommendation passes validation
- [ ] final_state logged as "completed"
- [ ] Cross-drive changes extracted and tested separately (if keeping them)
- [ ] All 19 component tests still pass
- [ ] No regressions in existing workflows

Then: **APPROVED FOR PRODUCTION DEPLOYMENT**
