# Phase 4 Launch: Production Integration Testing

**Date**: 2026-05-25  
**Status**: Ready to begin  
**Prior Phases**: 1, 2, 3 complete and proven

---

## What Phase 4 Does

Phase 4 takes the **proven infrastructure** from Phases 1-3 and tests it on **real work**:

1. Run actual agent sessions (not fixtures)
2. Test on the sensemaking-skills repository itself
3. Measure real performance (tokens, time, cost)
4. Identify edge cases and limitations
5. Determine production readiness
6. Create operator documentation

---

## Phase 4 Entry State

### What's Ready ✅
- Phase 1: Diagnostic loop proven (Scenarios 1-3)
- Phase 2: Orchestration proven (Scenario 4)
- Phase 3: Workflows defined (Scenario 5 fixtures)
- All validators working correctly
- All artifact contracts aligned
- Error detection proven on realistic cases

### What's Needed ❌
- Real end-to-end test on actual repository
- Concrete performance measurements
- Edge case testing
- Operator documentation
- Production gate decision

---

## Phase 4 Task 4.1: Real Codebase Test

### Objective
Execute the full Phase 1 → Phase 2 → Phase 3 loop on sensemaking-skills repository.

### Process

**Step 1: Agent Reads Bootstrap Skill**
```
Agent invokes: /skill using-sensemaking
Agent reads: skills/using-sensemaking/SKILL.md
Agent understands:
  - Fog classification system
  - 3-step diagnosis pattern
  - How to validate artifacts
  - Bounded retry logic
```

**Step 2: Agent Diagnoses Repository (Phase 1)**
```
Agent task: Analyze sensemaking-skills repository
Agent executes: repo-sensemaker analysis (or reads SKILL.md for procedure)
Agent produces: repository_sensemaking_brief artifact
Agent saves: artifacts/repository_sensemaking_brief_phase4.md
Agent validates: python scripts/validate-and-report.py artifacts/repository_sensemaking_brief_phase4.md
```

**Expected Output**:
- Brief artifact with:
  - artifact_id: "repository_sensemaking_brief"
  - primary_fog_type: (one of: product_fog, ui_fog, docs_fog, architecture_fog)
  - evidence: list of code/docs signals supporting fog type
  - recommended_workflow_id: which implementation workflow to use
  - created_at: ISO 8601 timestamp
  - immutable: true

**Success Criteria**:
- ✅ Brief artifact is created
- ✅ Brief validates successfully
- ✅ Primary fog type is reasonable for sensemaking-skills
- ✅ Evidence supports the classification

---

**Step 3: workflow-planner Routes (Phase 2)**
```
Agent task: Create orchestration plan from brief
Agent executes: workflow-planner with phase4 brief artifact
Agent produces: workflow_orchestration_plan artifact
Agent saves: artifacts/workflow_orchestration_plan_phase4.md
Agent validates: python scripts/validate-and-report.py artifacts/workflow_orchestration_plan_phase4.md
```

**Expected Output**:
- Plan artifact with:
  - artifact_id: "workflow_orchestration_plan"
  - primary_fog_type: (copied from brief)
  - chosen_workflow_id: (routed from fog_type)
  - workflow_steps: array of steps from selected workflow
  - created_at: ISO 8601 timestamp
  - immutable: true

**Success Criteria**:
- ✅ Plan artifact is created
- ✅ Plan validates successfully
- ✅ chosen_workflow_id matches primary_fog_type (no semantic conflicts)
- ✅ workflow_steps are properly populated

---

**Step 4: Execute Selected Workflow (Phase 3)**
```
Agent task: Execute the workflow specified in orchestration plan
Agent reads: workflow from chosen_workflow_id
Agent executes: First 2-3 steps of workflow
  - Step 1: docs-aligner (creates domain_alignment_report)
  - Step 2: (varies by workflow - could be discovery, to-prd, ui-flow, etc.)
Agent validates: Each step output
Agent saves: Artifacts to expected locations
```

**Expected Output**:
- Artifacts from workflow execution:
  - domain_alignment_report (from docs-aligner)
  - Plus output from Step 2+ (depends on workflow)

**Success Criteria**:
- ✅ Workflow steps execute without errors
- ✅ Each step produces expected artifact
- ✅ Artifacts validate successfully
- ✅ Artifacts are placed in correct locations

---

**Step 5: Log Results**
```
Agent task: Record all validation results
Agent appends: validation_run_log.md with:
  - Phase 4 Real Codebase Test entry
  - All artifact paths
  - All validation results
  - Any errors encountered and how they were resolved
Agent creates: PHASE-4-REAL-CODEBASE-TEST.md with findings
```

### Success Metrics for Task 4.1
- ✅ Brief artifact produced and validates
- ✅ Plan artifact produced and validates
- ✅ Selected workflow executes at least 2 steps
- ✅ All output artifacts are valid
- ✅ Results logged to validation_run_log.md
- ✅ No validation errors in final artifacts

### Failure Handling
If any step fails:
1. Record the exact error
2. Attempt to understand why
3. If fixable: fix and retry
4. If not fixable: document as limitation/blocker
5. Escalate if 3 attempts fail

---

## Phase 4 Task 4.2: Performance Measurement

### Objective
Measure time and token consumption for each phase.

### Measurement Points

**Phase 1 Measurement**:
- Input: sensemaking-skills repository (~100 files, ~20K lines of code)
- Output: Brief artifact (~2 KB)
- Measure: 
  - Wall-clock time from start to completion
  - Tokens consumed (if measurable via API instrumentation)
  - Document in PHASE-4-PERFORMANCE.md

**Phase 2 Measurement**:
- Input: Brief artifact (~2 KB)
- Output: Plan artifact (~3 KB)
- Measure:
  - Wall-clock time
  - Tokens (typically small)
  - Document in PHASE-4-PERFORMANCE.md

**Phase 3 Measurement**:
- Input: Plan + artifacts
- Output: Workflow results
- Measure:
  - Time per workflow step
  - Total time to produce first implementation artifact
  - Tokens per step (if measurable)
  - Which steps are slow? Which are fast?
  - Document in PHASE-4-PERFORMANCE.md

### Output Format

Create `PHASE-4-PERFORMANCE.md` with table:

```markdown
## Performance Baseline: sensemaking-skills Repository

### Phase 1 - repo-sensemaker
- Input Size: ~100 files, ~20K LOC
- Output Size: ~2 KB
- Wall-Clock Time: XX minutes
- Estimated Tokens: ~XXX
- Cost: ~$X.XX (if applicable)

### Phase 2 - workflow-planner
- Input Size: ~2 KB
- Output Size: ~3 KB
- Wall-Clock Time: XX seconds
- Estimated Tokens: ~10
- Cost: <$0.01

### Phase 3 - [selected workflow]
- Input Size: ~5 KB
- Output Size: [varies]
- Wall-Clock Time: XX minutes
- Estimated Tokens: ~XXX
- Cost: ~$X.XX

### Total System Cost
- End-to-End Time: XX minutes
- Total Tokens: ~XXX
- Total Cost: ~$X.XX
```

---

## Phase 4 Tasks 4.3-4.5 (Following Task 4.1 Success)

Once Task 4.1 is successful, proceed with:

**Task 4.3: Edge Case Testing**
- Test with different repository characteristics
- Document findings for different repo sizes/complexities

**Task 4.4: Operator Runbooks**
- Create documentation for running system in production
- Include troubleshooting guides

**Task 4.5: Production Gate Review**
- Decide what's production-ready
- Document known limitations
- Create implementation roadmap for improvements

---

## Exact Command Sequences

### To Run Phase 4 Test Manually

```bash
# Phase 1: Diagnose repository
python3 scripts/repo-sensemaker.py \
  --repo-root . \
  --output artifacts/repository_sensemaking_brief_phase4.md

# Validate Phase 1 output
python3 scripts/validate-and-report.py \
  artifacts/repository_sensemaking_brief_phase4.md

# Phase 2: Create orchestration plan
python3 scripts/workflow-planner.py \
  artifacts/repository_sensemaking_brief_phase4.md \
  --output artifacts/workflow_orchestration_plan_phase4.md

# Validate Phase 2 output
python3 scripts/validate-and-report.py \
  artifacts/workflow_orchestration_plan_phase4.md

# Phase 3: Execute selected workflow steps
# (This is workflow-specific; varies by chosen_workflow_id)
```

### To Record Results

```bash
# Log validation results
python3 scripts/record-validation.py \
  --artifact-path artifacts/repository_sensemaking_brief_phase4.md \
  --validation-json <json output from validate-and-report.py>

python3 scripts/record-validation.py \
  --artifact-path artifacts/workflow_orchestration_plan_phase4.md \
  --validation-json <json output from validate-and-report.py>
```

---

## Expected Phase 4 Timeline

| Task | Time Estimate | Blocker |
|------|---------------|---------|
| 4.1: Real Codebase Test | 2-3 hours | None |
| 4.2: Performance Measurement | 1-2 hours | 4.1 complete |
| 4.3: Edge Case Testing | 2-4 hours | 4.1 complete |
| 4.4: Operator Runbooks | 2-3 hours | 4.1-4.3 complete |
| 4.5: Production Gate Review | 1 hour | 4.1-4.4 complete |
| **Total** | **8-13 hours** | Sequenced |

---

## Success Criteria for Phase 4

**Gate 1: Task 4.1 Successful**
- Real end-to-end test runs without fatal errors
- All three phases produce valid artifacts
- No validation errors on final outputs
- Results logged to validation_run_log.md

**Gate 2: Task 4.2 Complete**
- Concrete performance numbers documented
- Cost/time tradeoffs clear
- Identifies which phases are fast vs. slow

**Gate 3: Task 4.3 Complete**
- Edge case findings documented
- Known limitations identified
- Recommendations for improvements listed

**Gate 4: Task 4.4 Complete**
- Operator can follow runbooks to run system
- Troubleshooting guide covers common issues
- Production deployment procedure documented

**Gate 5: Task 4.5 Complete**
- Go/no-go decision made for each component
- Production readiness criteria met
- Limitations and constraints documented
- Roadmap for improvements created

---

## Failure Scenarios

### If Phase 4.1 Fails
- Document exact error
- Understand root cause
- Determine if it's:
  - Code bug (fix and retry)
  - Missing skill (add skill definition)
  - Architectural issue (re-design)
  - Limitation (document and note for Phase 5)

### If Performance is Unacceptable
- Identify bottleneck (which step is slow?)
- Optimize or design alternative
- Document tradeoff

### If Edge Cases Break System
- Document failure mode
- Understand root cause
- Decide: fix now or future phase?

---

## Phase 4 Exit Criteria

Phase 4 is COMPLETE when:
- ✅ Real codebase test successful
- ✅ Performance measured and documented
- ✅ Edge cases tested and documented
- ✅ Operator runbooks created
- ✅ Production gate review completed
- ✅ PHASE-4-COMPLETE.md written
- ✅ Go/no-go decision made for production

---

## Ready to Launch

All infrastructure is in place. Phase 4.1 can begin immediately.

**Current blockers**: None  
**Dependencies**: Phases 1-3 complete (✅ confirmed)  
**Next action**: Begin Task 4.1 - Real Codebase Test

---

**Launch Date**: 2026-05-25  
**Estimated Completion**: 2026-05-26  
**Status**: READY TO BEGIN
