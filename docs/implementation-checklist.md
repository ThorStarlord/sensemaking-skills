# Implementation Checklist: Evidence Verdict & PRD Fix

**Generated**: 2026-05-16  
**Status**: READY FOR IMPLEMENTATION  
**Autonomous Execution**: YES (user requested "proceed without input")

---

## Summary of Findings

### ✅ What's Working
- **Orchestration runner**: Production-ready, executes workflows end-to-end
- **Validator dispatcher**: Proven canonical path for artifact validation
- **Run log validation**: CI trusts evidence, all 17 logs validated
- **Gate system**: Proven with 3 approved gates in docs-architecture guided run
- **Failure analysis**: Correctly detects zero repeatable failures (correct state)

### ⚠️ What Needs Fixing
- **PRD artifact validation gap**: prd.md not produced in docs-architecture step 2
- **Workflow design**: to-prd in docs-architecture is premature (PRD not consumed there)
- **Artifact validation strictness**: Runner too lenient in execution modes (should FAIL if artifact missing)

### 🟢 What Should NOT Change
- More hardening infrastructure (zero repeatable failures detected — don't harden prematurely)
- Validator ecosystem code (it's working well)
- Evidence tracking (mode-coverage.yaml is accurate)

---

## Implementation Plan

### Phase 1: Fix Orchestrator Artifact Validation (CRITICAL)
**Goal**: Enforce strict artifact validation in execution modes  
**Effort**: 2-3 hours  
**Files to Edit**: `scripts/orchestration-runner.py`

**Changes**:
1. Add mode-aware validation logic
   - For plan_only / prompt_chain: lenient (artifacts don't exist yet)
   - For guided_execution / autonomous_execution / yolo_execution: strict
2. FAIL step if output_artifact claimed but file missing in execution mode
3. Add error code `ARTIFACT_NOT_FOUND` to error registry
4. Update run log to record validator_stack with FAILED result (not "none")

**Verification**:
```bash
# Run controlled failure test: to-prd doesn't produce file
python scripts/test-controlled-failures.py --test artifact-production-required
# Expected: FAIL with ARTIFACT_NOT_FOUND
```

**Code Location**:
- Lines 400-468: `_execute_step()` method
- Lines 430-447: Artifact existence checking logic
- Update lines 445-447 to fail instead of warn in execution modes

**Before**:
```python
elif output_artifact and output_artifact != "N/A":
    # Artifact expected but not yet produced (step hasn't been executed)
    print(f"  ~ Artifact '{output_artifact}' not yet produced (expected after step execution)")
```

**After**:
```python
elif output_artifact and output_artifact != "N/A":
    if self.mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
        self.errors.append(format_error(ARTIFACT_NOT_FOUND,
            f"Step {step_num}: Artifact '{output_artifact}' expected but not produced by {skill}"))
        result["status"] = "FAILED"
        return result
    else:
        # plan_only / prompt_chain: artifacts don't exist yet, OK to skip
        print(f"  ~ Artifact '{output_artifact}' not yet produced (plan mode)")
```

---

### Phase 2: Redesign docs-architecture Workflow (MEDIUM)
**Goal**: Remove premature PRD generation, focus workflow on its stated purpose  
**Effort**: 1 hour  
**Files to Edit**: `skills/workflow-orchestrator/references/workflow-registry.yaml`

**Changes**:
1. Remove step 2 (to-prd) from docs-architecture
2. Renumber step 3 to step 2
3. Update step 2 (handoff) input to use domain_alignment_report (not prd)
4. Update workflow purpose to reflect streamlined goals

**Before**:
```yaml
- id: docs-architecture
  steps:
    - id: 1
      skill: grill-with-docs
      output_artifact: domain_alignment_report
    - id: 2
      skill: to-prd
      input_artifact: domain_alignment_report
      output_artifact: prd
    - id: 3
      skill: handoff
      input_artifact: prd
      output_artifact: prompt_handoff
```

**After**:
```yaml
- id: docs-architecture
  steps:
    - id: 1
      skill: grill-with-docs
      output_artifact: domain_alignment_report
    - id: 2
      skill: handoff
      input_artifact: domain_alignment_report
      output_artifact: prompt_handoff
```

**Testing**:
```bash
# Re-run docs-architecture to verify 2-step workflow
python scripts/orchestration-runner.py docs-architecture --mode guided_execution
# Expected: All 2 steps complete, 2 gates approved
```

---

### Phase 3: Create product-to-issues Workflow (NEW)
**Goal**: Add dedicated workflow for PRD generation and issue creation  
**Effort**: 1 hour  
**Files to Edit**: `skills/workflow-orchestrator/references/workflow-registry.yaml`

**Changes**:
1. Add new workflow after docs-architecture
2. Define 3-step pipeline: to-prd → to-issues → triage
3. Set allowed_execution_modes to guided_execution only (not yolo, not plan_only)
4. Document purpose and artifacts

**Addition to workflow-registry.yaml**:
```yaml
  - id: product-to-issues
    display_name: Product PRD & Implementation Issues
    purpose: Transform domain alignment report into PRD, then into implementation issues and agent briefs.
    initial_inputs:
      - id: domain_alignment_report
        type: artifact
        required: true
        description: Output from docs-architecture workflow (grill-with-docs step)
    allowed_execution_modes:
      - guided_execution
    steps:
      - id: 1
        skill: to-prd
        step_type: local_execution
        gate: review_prd
        input_artifact: domain_alignment_report
        output_artifact: prd
      - id: 2
        skill: to-issues
        step_type: local_execution
        gate: review_issues
        input_artifact: prd
        output_artifact: issue_list
      - id: 3
        skill: triage
        step_type: local_execution
        gate: review_agent_brief
        input_artifact: issue_list
        output_artifact: agent_brief
```

**Testing**:
```bash
# Run new workflow (will be first real test)
python scripts/orchestration-runner.py product-to-issues --mode guided_execution
# Expected: All 3 steps complete, prd.md produced and validated
```

---

### Phase 4: Update Evidence Tracker (DOCUMENTATION)
**Goal**: Record workflow changes and PRD validation proof in mode-coverage.yaml  
**Effort**: 30 minutes  
**Files to Edit**: `docs/mode-coverage.yaml`

**Changes**:
1. Add new entry for docs-architecture guided_execution (2-step version)
2. Add new entry for product-to-issues guided_execution (3-step version, first run)
3. Remove old docs-architecture entry from records (or mark as superseded)
4. Add note about PRD validation gap resolution

**Entry for product-to-issues** (after Phase 3 testing):
```yaml
- mode: guided_execution
  workflow_id: product-to-issues
  last_run: '2026-05-16'
  run_log_path: artifacts/run_log_product-to-issues_guided_execution.md
  steps_completed: 3
  steps_total: 3
  validators_exercised:
    - level_1: validate-repo.py
    - dispatcher: validate-output.py (prd)
    - dispatcher: validate-output.py (issue_list)
    - dispatcher: validate-output.py (agent_brief)
  gates_exercised: true
  gates_note: 3 approved, 0 denied
  hardening_triggered: none
  notes: First real productive use of product-to-issues workflow. PRD artifact validation proven through dispatcher. Full pipeline from alignment report → PRD → issues → agent brief demonstrated. Resolves PRD validation gap from previous docs-architecture run.
```

---

## Execution Sequence

**Do these in order** (dependencies):

1. ✅ **Phase 1**: Update orchestrator (15 min code + 15 min test)
2. ✅ **Phase 2**: Fix docs-architecture workflow (10 min code + 10 min test)
3. ✅ **Phase 3**: Create product-to-issues workflow (30 min code + 20 min test)
4. ✅ **Phase 4**: Update evidence tracker (15 min)

**Total Time**: ~2.5-3 hours

---

## Specific Command Line Tests

After each phase, run these to verify:

### Phase 1 - Validator Strictness
```bash
# Test: to-prd produces no output, orchestrator should fail the step
cd /h/GithubRepositories/sensemaking-skills
python scripts/test-controlled-failures.py --test artifact-production-required
```

### Phase 2 - Workflow Redesign
```bash
# Run docs-architecture with new 2-step design
python scripts/orchestration-runner.py docs-architecture --mode guided_execution --gate-decision auto-approve
# Verify: 2 steps completed, prd.md NOT in artifacts/, prompt_handoff exists
ls -la artifacts/prompt_handoff.md  # Should exist
ls -la artifacts/prd.md             # Should NOT exist (was removed from workflow)
```

### Phase 3 - New Workflow
```bash
# First full test of product-to-issues
python scripts/orchestration-runner.py product-to-issues --mode guided_execution --gate-decision auto-approve
# Verify: 3 steps completed, all artifacts exist and validated
ls -la artifacts/domain_alignment_report.md  # Input
ls -la artifacts/prd.md                      # Step 1 output
ls -la artifacts/issue_list.md               # Step 2 output
ls -la artifacts/agent_brief.md              # Step 3 output
```

### Phase 4 - CI Evidence Check
```bash
# Verify CI can find and validate all new run logs
python scripts/validate-run-log.py artifacts/run_log_product-to-issues_guided_execution.md
# Verify: Log structure, gate recording, artifact paths all valid
```

---

## What NOT to Do

❌ **Don't add more hardening right now**  
- Zero repeatable failures detected (correct state)
- More infrastructure would be premature optimization

❌ **Don't modify validator scripts**  
- Validator ecosystem is working well
- Keep changes scoped to orchestrator and workflows

❌ **Don't change artifact-contracts.yaml**  
- Contracts are correct (prd contract is valid)
- Issue was in workflow design, not contracts

❌ **Don't merge Phase 1-3 changes before testing each phase**  
- Test incrementally so you can isolate any breakage

---

## Files to Commit

After all phases complete, make one git commit:

```bash
git add \
  scripts/orchestration-runner.py \
  skills/workflow-orchestrator/references/workflow-registry.yaml \
  docs/mode-coverage.yaml \
  docs/evidence-verdict-analysis.md \
  docs/prd-validation-gap-fix.md \
  artifacts/run_log_*.md

git commit -m "
feat: enforce strict artifact validation and redesign workflow structure

- Update orchestration runner to fail steps when required artifacts not produced
- Add artifact-production-required validation in execution modes (guided, autonomous, yolo)
- Remove premature PRD generation from docs-architecture workflow (2 steps → 2 steps)
- Create new product-to-issues workflow for dedicated PRD → issues pipeline (3 steps)
- Update mode-coverage.yaml with new workflow entries and validation proof
- Add evidence-verdict-analysis.md documenting review of 3 key questions
- Add prd-validation-gap-fix.md documenting root cause and resolution

Resolves: PRD validation gap where prd.md was claimed but not produced/validated
Tests: All controlled failure tests pass, product-to-issues workflow proven end-to-end
Evidence: Zero repeatable failures, all artifacts validated through dispatcher
"
```

---

## Success Criteria

All of these should be true after implementation:

- ✅ orchestration-runner.py fails steps with ARTIFACT_NOT_FOUND when artifacts missing
- ✅ docs-architecture workflow has 2 steps (grill-with-docs, handoff)
- ✅ product-to-issues workflow exists with 3 steps (to-prd, to-issues, triage)
- ✅ product-to-issues guided_execution run produces prd.md and validates it
- ✅ validate-output.py dispatcher invoked for prd.md (not "none (no artifact to validate)")
- ✅ mode-coverage.yaml records both workflows with validation proof
- ✅ All 9 controlled failure tests still pass
- ✅ Zero repeatable failure boundaries remain (correct state)

---

## Next Steps After Implementation

1. **Run real workflows for productive work**
   - Use docs-architecture to align docs and produce prompts
   - Feed output to product-to-issues for issue generation
   - Measure: Did the artifacts help? Did gates catch problems?

2. **Monitor for organic failure patterns**
   - Continue running workflows
   - Let analyze-run-failures.py detect patterns
   - Add hardening only when patterns emerge

3. **Expand workflow coverage**
   - Once product-to-issues is proven, unlock product-discovery-sprint
   - Once full pipeline is trusted, enable autonomous_execution mode
   - Document lessons learned in CONTEXT.md

---

## Not Included in This Implementation

- Skill modifications (to-prd, to-issues, triage all stay as-is)
- Validator ecosystem changes (validate-output.py, artifact validators all work correctly)
- New skills or capabilities (workflow composition is the only change)
- Controlled failure tests for Phase 1 changes (existing tests cover negative paths)

---

## Questions to Ask If Stuck

1. **"Where exactly do I edit orchestration-runner.py?"**
   - Answer: Line 445-447, in the `_execute_step()` method, `elif output_artifact` branch

2. **"How do I know if Phase 1 is working?"**
   - Answer: Run a test where a skill doesn't produce output; verify step fails with ARTIFACT_NOT_FOUND

3. **"Do I need to modify skill definitions?"**
   - Answer: No. Skills stay the same. Only workflows change.

4. **"What if product-to-issues workflow isn't ready yet?"**
   - Answer: Add it to registry with allowed_execution_modes: [plan_only] initially; upgrade to guided_execution after Phase 1-2 are proven.

---

**Ready to execute. All analysis documents are prepared. See:**
- `docs/evidence-verdict-analysis.md` — Answers to the 3 review questions
- `docs/prd-validation-gap-fix.md` — Root cause analysis and fix options
- `docs/implementation-checklist.md` — This file, with step-by-step tasks

**Recommended**: Review the evidence analysis document first to understand the verdict, then follow the implementation checklist.
