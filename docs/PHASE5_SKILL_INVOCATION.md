# Phase 5: Skill Invocation Framework

**Status**: 🔄 In Progress  
**Date Started**: 2026-05-16  
**Objective**: Implement skill invocation mechanism to enable `yolo_execution` mode and true end-to-end automation

## Executive Summary

The sensemaking-skills orchestration system has successfully proven 4 of 5 execution modes (plan_only, prompt_chain, guided_execution, autonomous_execution) with zero repeatable failures. However, a critical gap exists: **the orchestrator validates artifacts and manages gates, but does not invoke skills**.

Phase 5 addresses this architectural gap by implementing a skill invocation framework that allows workflows to execute skills directly without external agent intervention. This enables:
- Full `yolo_execution` mode capability
- True end-to-end automation without manual Claude invocation
- Production readiness for 100% of execution modes

## Current State (Pre-Phase 5)

### Success Metrics from Phase 4
- **4 of 5 execution modes** fully proven and production-ready
- **Zero repeatable failures** across 21 independent runs
- **3 of 5 Level-3 validators** proven in live workflows
- **100% classification accuracy** for project routing
- **Parallel execution** working across 2-5 concurrent workers

### Identified Gap
The orchestrator layer (orchestration-runner.py) currently:
- ✅ Reads workflow definitions
- ✅ Manages execution gates and modes
- ✅ Validates artifact contracts
- ❌ **Does NOT invoke skills**

Skills are invoked manually by:
- Claude agents reading prompts and executing steps
- External CI/CD systems
- Human operators

This blocks:
- `yolo_execution` mode (requires automatic gate decisions)
- Full automation on new workflows (skill-maintenance-loop, product-to-issues, etc.)

## Phase 5 Success Criteria

**All items must be complete before Phase 5 is considered done:**

- [x] All 5 Level-3 validators exist and are executable (test coverage verified)
- [ ] Skill invocation mechanism selected and implemented
- [ ] All 5 Level-3 validators exercised in live workflow runs
- [ ] `yolo_execution` mode fully proven on at least one new workflow
- [ ] Manual gate approval workflow tested (not auto-approve simulation)
- [ ] Zero repeatable failures maintained
- [ ] Documentation updated with validator coverage and invocation design

## Level 3 Validator Coverage Matrix

All 5 required Level-3 validators are present and executable:

| Validator | Purpose | Triggered By | Workflow(s) | Status | Coverage |
|-----------|---------|-------------|-----------|--------|----------|
| `validate-plan.py` | Validates orchestration execution plans | orchestration-runner.py planning phase | plan_only, prompt_chain, autonomous_execution | ✅ PROVEN | 3 runs |
| `validate-prompt-handoff.py` | Validates prompt handoff artifacts for downstream Claude invocation | handoff skill output validation | All 4 proven modes | ✅ PROVEN | 4 runs (all) |
| `validate-brief.py` | Validates brief artifacts (sensemaking, problem frames, personas, etc.) | repository_sensemaking_brief, problem_frame outputs | fast-local-diagnostic, full-local-sensemaking | ✅ PROVEN | 3 runs |
| `validate-skill-improvement-plan.py` | Validates skill improvement proposals | skill-maintenance-loop workflow output | skill-maintenance-loop (pending Phase 5) | ⚠️ PENDING | 0 runs |
| `validate-usage-research-report.py` | Validates usage research findings for improvement tracking | usage-researcher skill output | skill-maintenance-loop (pending Phase 5) | ⚠️ PENDING | 0 runs |

### Key Findings

1. **Already Proven (3 of 5)**
   - validate-plan.py: Verified in plan_only, prompt_chain modes
   - validate-prompt-handoff.py: Proven in ALL 4 successful Phase 4 runs
   - validate-brief.py: Proven in diagnostic and sensemaking workflows

2. **Pending Phase 5 Exercises (2 of 5)**
   - validate-skill-improvement-plan.py: Requires skill-maintenance-loop to be executed
   - validate-usage-research-report.py: Requires usage-researcher skill to be invoked in a workflow

3. **Coverage Approach**
   - Validators are Python executables in scripts/ directory
   - Each is triggered by orchestration-runner.py based on artifact type
   - Dispatcher pattern: validate-output.py routes to specialized Level-3 validators
   - All validators use artifact contract checking for type validation

## Validator Dispatcher Architecture

```
orchestration-runner.py (validates all outputs)
    ↓
validate-output.py (generic dispatcher)
    ├─→ validate-artifact.py (Level 2: generic contract validation)
    │
    └─→ Level 3 Validators (specialized contract validation)
        ├─→ validate-plan.py (orchestration plans)
        ├─→ validate-prompt-handoff.py (prompts)
        ├─→ validate-brief.py (briefs/diagnostics)
        ├─→ validate-skill-improvement-plan.py (improvement proposals)
        └─→ validate-usage-research-report.py (research reports)
```

## Skill Invocation Options Under Consideration

### Option 1: Skill Invocation Agent (Selected for Phase 5)
**Approach**: Create a dedicated agent that reads execution plans and invokes skills in sequence

**Advantages**:
- Minimal changes to orchestrator core
- Leverages existing Claude API and agent capabilities
- Can run asynchronously or synchronously
- Easy to add retry logic and error handling

**Complexity**: Moderate (4-6 hours of work)

**Implementation Path**:
1. Create skill_invoker.py with agent interface
2. Agent reads JSON execution plan
3. For each step, invokes corresponding skill
4. Tracks progress and logs results
5. Returns execution outcome

### Option 2: Orchestrator Skill Invocation
**Approach**: Add direct skill invocation to orchestration-runner.py

**Advantages**:
- Single code path for all execution
- No external agent needed
- Direct integration with gate management

**Disadvantages**:
- Higher complexity (skill registry, context loading, sandbox setup)
- Difficult to test and debug
- Requires significant orchestrator refactoring

**Complexity**: High (12+ hours of work)

### Option 3: External Skill Queue
**Approach**: Queue skills for execution via CI/CD pipeline or message broker

**Advantages**:
- Decoupled from orchestrator
- Easy to parallelize and scale
- Can integrate with existing infra

**Disadvantages**:
- Requires infrastructure setup
- Complex state management
- Async complexity

**Complexity**: Very High (20+ hours of work)

## Next Steps for Phase 5 Implementation

### Step 1: Skill Invocation Agent
- Create scripts/skill_invoker.py
- Implement agent that accepts execution plan JSON
- Test with plan_only execution first
- Validate all step outputs

### Step 2: Workflow Execution Test
- Run skill-maintenance-loop end-to-end
- Verify validate-skill-improvement-plan.py is exercised
- Check output contracts are met

### Step 3: Research Workflow
- Set up usage research data
- Run skill-maintenance-loop → skill-improvement-plan
- Exercise validate-usage-research-report.py
- Document findings

### Step 4: YOLO Mode Testing
- Enable skill invocation in autonomous_execution mode
- Test with yolo_execution flag
- Verify automated gates work correctly
- Validate error handling

### Step 5: Documentation & Testing
- Create Phase 5 execution summary
- Update coverage dashboard
- Run validator coverage tests
- Document architecture and decisions

## Validator Test Coverage

**File**: `tests/test_all_validators_coverage.py`

All 5 Level-3 validators are verified to exist and be executable:

```bash
$ pytest tests/test_all_validators_coverage.py -v
✅ test_all_level3_validators_exist
✅ test_validators_are_executable
```

## Architecture Decisions

### Decision: Multi-Level Validator Stack
- **Level 1 (Structural)**: validate-repo.py - repository structure
- **Level 2 (Generic)**: validate-artifact.py - contract enforcement
- **Level 2 (Dispatcher)**: validate-output.py - routing to specialized validators
- **Level 3 (Specialized)**: 5 domain-specific validators
  - validate-plan.py
  - validate-prompt-handoff.py
  - validate-brief.py
  - validate-skill-improvement-plan.py
  - validate-usage-research-report.py

**Rationale**: Separation of concerns allows for independent testing, easy extension, and fault isolation.

### Decision: Artifact Contract Enforcement
All validators enforce artifact contracts defined in:
- `skills/workflow-orchestrator/references/artifact-contracts.yaml`

**Benefits**:
- Type safety across workflow steps
- Early error detection
- Clear failure messages
- Enables confident chaining

## Production Readiness Checklist

### Before Phase 5 Completion
- [ ] Skill invocation mechanism implemented and tested
- [ ] All 5 validators exercised in live runs
- [ ] skill-maintenance-loop workflow executed end-to-end
- [ ] yolo_execution mode fully proven
- [ ] Zero new repeatable failures introduced
- [ ] Documentation complete
- [ ] All tests passing

### After Phase 5 Completion
- [ ] All 5 execution modes production-ready (100% coverage)
- [ ] All 5 Level-3 validators proven in live workflows
- [ ] Full end-to-end automation available
- [ ] Ready for production deployment
- [ ] Ready for customer onboarding

## Related Documents

- `docs/PHASE2_SUMMARY.md` - Low-Level Decision Automation (routing)
- `docs/PHASE3_SUMMARY.md` - Scale and Parallelism (multi-project)
- `EXECUTION_SUMMARY.md` - Overall execution summary
- `artifacts/coverage_dashboard.md` - Detailed validator and mode coverage

## Conclusion

Phase 5 is the final step toward full production readiness. By implementing skill invocation, we unlock the last execution mode (yolo_execution) and enable true end-to-end automation. The 5 Level-3 validators provide the quality gates needed to ensure safe, reliable workflow execution.

**Timeline**: 1-2 working days for implementation and testing  
**Risk Level**: Low (validator infrastructure proven, isolated from core)  
**Business Impact**: High (enables 100% automation for all use cases)
