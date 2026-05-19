# Value-Production Phase 1: Findings & Architecture Gaps

## Date
2026-05-16

## Session
orchestration-20260516-202919-9a1fb449

## Objective
Run real projects through the pipeline to identify practical issues beyond system-proving tests.

## What Was Attempted
Execute the `product-to-issues` workflow in `guided_execution` mode to transform a domain alignment report into PRD, issues, and agent briefs.

```bash
python scripts/orchestration-runner.py product-to-issues --mode guided_execution
```

## Results

### ✅ What Worked
1. **Orchestration runner pre-flight checks** - Correctly validated git state, artifact contracts, and repo structure
2. **Plan generation** - Generated complete workflow plan with all 3 steps (to-prd → to-issues → triage)
3. **Artifact validation framework** - Correctly configured validators and dispatcher
4. **Mode coverage tracking** - Updated mode-coverage.yaml with run attempts

### ❌ Critical Gaps Found

#### Gap 1: No Skill Invocation Mechanism
**Problem**: The orchestration runner does not invoke skills. It only checks if output artifacts exist.
- Step 1 executed `docs-aligner` skill but the runner never actually invoked it
- The runner waited for the skill output but had no mechanism to trigger the skill's execution
- Result: Artifact missing → FAILED

**Impact**: Complete blocker for end-to-end automation. Workflows cannot execute without manual skill invocation.

**Evidence**: 
- Run log shows: `[ARTIFACT_NOT_FOUND]` for `prd.md`
- No skill invocation code paths in orchestration-runner.py
- Workflow registry defines skills but orchestrator doesn't use them

#### Gap 2: No Input Artifact Passing
**Problem**: Steps don't receive input artifacts from previous steps or external sources.
- Workflow registry defines `input_artifact: domain_alignment_report` for step 1
- Orchestrator doesn't pass this artifact to the skill
- Skills can't consume previous outputs

**Impact**: Can't chain workflows or pass data between steps. Each workflow is isolated.

**Evidence**:
- `product-to-issues` requires `domain_alignment_report` but runner has no code to provide it
- `workflow-registry.yaml` specifies `input_artifact` but orchestrator never uses it

#### Gap 3: No Interactive Gate Bypass for Automation
**Problem**: Runner waits for stdin input at gates even in non-interactive mode.
- `_manage_gate()` calls `input()` which fails in automation (EOFError)
- No `--auto-approve` or `--skip-gates` flag for unattended execution

**Impact**: Can't run workflows end-to-end in CI/CD without manual intervention.

**Evidence**:
- Error: `EOFError: EOF when reading a line` when running in bash without TTY
- No command-line flag to auto-approve gates

## Architectural Assessment

The orchestration runner currently implements a **validation pipeline** but not an **execution pipeline**:

```
Current Design:
Plan Generation → (No Skill Invocation) → Validator → Gate Management → Run Log

Needed Design:
Plan Generation → Skill Invocation + Input Passing → Validator → Gate Management → Run Log
```

### Design Implications

1. **Skill invocation is required** - Orchestrator must either:
   - Invoke skills directly (requires skill registration and execution context)
   - Delegate to agents (requires agent framework integration)
   - Queue skills for external runner (requires async coordination)

2. **Input/output chaining is required** - Each step must:
   - Receive input artifacts from previous steps or external sources
   - Make them available to the skill
   - Capture skill output
   - Validate output before next step

3. **Unattended execution requires gate policy** - Runner must support:
   - Auto-approval for high-confidence outputs
   - Gate bypass for automation modes
   - Conditional gate triggers based on validator results

## Recommendations

### Phase 1.1: Implement Skill Invocation (Critical Path)

1. **Add Skill Registry Integration**
   - Load skill metadata from `skills/*/SKILL.md`
   - Map workflow skill names to skill definitions
   - Validate skill availability

2. **Implement Direct Skill Invocation**
   - Create `invoke_skill()` method in runner
   - Pass input artifacts as context
   - Capture output artifacts
   - Handle errors and timeouts

3. **Add Input Artifact Resolution**
   - `resolve_input_artifacts()` for each step
   - Load artifact contents and pass to skill context
   - Support both file-based and structured inputs

### Phase 1.2: Add Gate Automation (Unlocks CI/CD)

1. **Add `--auto-approve` flag** - Auto-approve all gates
2. **Add `--confidence-threshold` flag** - Auto-approve gates above confidence level  
3. **Make stdin-dependent code resilient** - Detect TTY availability

### Phase 1.3: Test End-to-End Execution

1. Run `docs-architecture` workflow fully (already has artifacts)
2. Run `product-to-issues` workflow with artifact passing
3. Verify all 3 steps execute, validate, and produce outputs
4. Test gate decisions and approvals

## Success Criteria

- [ ] `product-to-issues` workflow runs end-to-end without manual intervention
- [ ] All 3 steps execute skills and produce expected artifacts
- [ ] Input artifacts passed correctly between steps
- [ ] Validators run and detect issues
- [ ] Gates managed with auto-approval option
- [ ] Run log shows complete execution trace
- [ ] No repeatable failures across 3+ runs

## Next Action
Implement Phase 1.1 (Skill Invocation) to unblock end-to-end workflow execution.
