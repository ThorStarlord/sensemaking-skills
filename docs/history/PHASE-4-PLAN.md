# Phase 4 Plan: Production Integration and Hardening

**Date**: 2026-05-25  
**Status**: Planning  
**Prior Phase**: Phase 3 complete (workflows verified, Scenario 5 tested)

---

## Overview

Phase 4 transitions the sensemaking-skills system from laboratory (phases 1-3) to production by:
1. Testing on real codebases (not just artifacts and fixtures)
2. Measuring time and token budget for each workflow
3. Identifying performance bottlenecks
4. Hardening error handling for edge cases
5. Creating operator runbooks for production use
6. Documenting known limitations and tradeoffs

---

## Phase 4 Goals

### Goal 1: Real Codebase Testing
Run the complete Phase 1 → Phase 2 → Phase 3 loop on actual repositories:
- ✅ Diagnose sensemaking-skills repository itself
- ✅ Route to appropriate implementation workflow
- ✅ Execute workflow steps and produce real artifacts
- ✅ Verify results are meaningful (not just structurally valid)

### Goal 2: Performance Baseline
Measure and document:
- Time required per workflow phase (Phase 1, 2, 3)
- Token budget consumed per phase
- Cost per operation (if applicable)
- Bottlenecks and optimization opportunities

### Goal 3: Error Robustness
Test edge cases:
- Large repositories (>1000 files)
- Complex domain models (>100 concepts)
- Broken or incomplete codebase state
- Missing documentation or context
- Conflicting signals (multiple fog types equally probable)

### Goal 4: Operator Readiness
Create runbooks and documentation:
- How to run workflows on new repositories
- How to interpret validation errors
- How to escalate when agent hits limits
- Troubleshooting guide for common issues
- Cost/time tradeoffs for different execution modes

### Goal 5: Production Gate Review
Decide what's ready for production:
- Which workflows are production-ready?
- Which workflows need more hardening?
- What guardrails and constraints are required?
- What monitoring and logging is needed?

---

## Phase 4 Scope

### Task 4.1: Real Codebase Test - sensemaking-skills
**Objective**: Test end-to-end workflow on the project itself

**Process**:
1. Agent reads using-sensemaking skill
2. Agent diagnoses sensemaking-skills repository
3. workflow-planner routes to appropriate workflow
4. Selected workflow executes (e.g., docs-implementation-workflow)
5. Artifacts are generated and validated
6. Results are logged and reviewed

**Success Criteria**:
- ✅ Brief artifact is generated and semantically valid
- ✅ Plan artifact routes to correct implementation workflow
- ✅ Workflow steps produce meaningful output
- ✅ Artifacts are placed in expected locations
- ✅ Validation passes on all generated artifacts

**Expected Outcome**:
- Confirms system works end-to-end on real repository
- Identifies any missing skills or broken references
- Provides real performance baseline

---

### Task 4.2: Token Budget and Time Measurement
**Objective**: Quantify cost of different workflow phases

**Measurement Points**:
1. **Phase 1 - repo-sensemaker**
   - Input: Repository state (files, docs, git history)
   - Output: repository_sensemaking_brief
   - Measure: Time, tokens, complexity factors

2. **Phase 2 - workflow-planner**
   - Input: repository_sensemaking_brief
   - Output: workflow_orchestration_plan
   - Measure: Time, tokens (typically small)

3. **Phase 3 - implementation workflows**
   - Input: orchestration_plan + repository state
   - Output: Implementation artifacts (code, docs, specs)
   - Measure: Time, tokens PER WORKFLOW (different for each)
     - product-implementation-workflow (longest - includes discovery)
     - ui-implementation-workflow (medium - UI-specific steps)
     - docs-implementation-workflow (short - 3 steps)
     - architecture-implementation-workflow (medium - refactoring steps)

**Tools**:
- Use Claude API instrumentation (if available) to measure tokens
- Use timestamps to measure wall-clock time
- Document results in PHASE-4-PERFORMANCE.md

**Output**:
- Cost table: workflow → tokens → time
- Breakdown: per-phase and per-step
- Optimization recommendations

---

### Task 4.3: Edge Case Testing
**Objective**: Identify failure modes and limits

**Test Cases**:

**4.3a: Large Repository**
- Repository with >1000 files
- Expected impact: Higher token usage in Phase 1
- Success: Agent produces brief without truncation
- Failure mode: Agent hits context limit

**4.3b: Complex Domain Model**
- Repository with >100 defined concepts
- Expected impact: More evidence items, longer brief
- Success: Brief captures all major concepts
- Failure mode: Brief oversimplifies or omits key concepts

**4.3c: Broken Codebase**
- Repository with syntax errors, missing dependencies
- Expected impact: Agent struggles with diagnosis
- Success: Brief identifies issues as "broken state"
- Failure mode: Brief produces incorrect fog_type

**4.3d: Missing Context**
- Repository with no README, minimal docs
- Expected impact: Agent relies on code analysis only
- Success: Brief is honest about uncertainty
- Failure mode: Brief makes unfounded claims

**4.3e: Mixed Signals**
- Repository with evidence for multiple fog types
- Example: UI problems AND architecture problems equally prominent
- Expected impact: diagnosis_conflict flag in brief
- Success: Escalation to full-fog-workflow recommended
- Failure mode: Arbitrary choice without escalation

---

### Task 4.4: Operator Runbooks
**Objective**: Document how to operate the system in production

**Runbooks to Create**:

**4.4a: Getting Started**
- How to invoke sensemaking system on a new repository
- What inputs are required (repository access, context)
- What outputs to expect
- Typical execution time

**4.4b: Interpretation Guide**
- How to read and understand the brief artifact
- What each fog type indicates
- How to recognize escalation recommendations
- What to do if escalation_recommended = true

**4.4c: Validation Error Troubleshooting**
- Common validation errors and fixes
- How to tell if error is fixable vs. requires escalation
- When to retry vs. when to escalate
- Error logs and where to find them

**4.4d: Performance Tuning**
- How to reduce token usage
- How to speed up execution
- Tradeoffs between speed and accuracy
- When to use which execution mode (plan_only vs. autonomous_execution)

**4.4e: Escalation Procedures**
- When to escalate to human review
- What information to include in escalation
- How to hand off to next phase
- Recovery procedures

---

### Task 4.5: Production Gate Review
**Objective**: Decide what's ready for production and what needs more work

**Workflows to Assess**:

1. **Phase 1 - repo-sensemaker**
   - Status: Proven in Phase 1 testing ✅
   - Production Ready: YES (with cost monitoring)
   - Constraints: Max ~5000 lines of code for detailed analysis

2. **Phase 2 - workflow-planner**
   - Status: Proven in Phase 2 testing ✅
   - Production Ready: YES
   - Constraints: Requires valid brief as input

3. **product-implementation-workflow**
   - Status: Defined and validated in Phase 3
   - Production Ready: CONDITIONAL (depends on real-world testing)
   - Blockers: Needs testing on actual product codebases
   - Constraints: Long execution time due to discovery steps

4. **ui-implementation-workflow**
   - Status: Defined and validated in Phase 3
   - Production Ready: CONDITIONAL
   - Blockers: Needs testing on actual UI codebases
   - Constraints: Requires UI-specific skills (ui-flow, ui-screen-spec)

5. **docs-implementation-workflow**
   - Status: Defined and validated in Phase 3
   - Production Ready: LIKELY (shortest, simplest workflow)
   - Blockers: Needs testing on documentation projects
   - Constraints: Produces specs, not finished docs

6. **architecture-implementation-workflow**
   - Status: Newly added in Phase 3
   - Production Ready: NEEDS MORE TESTING
   - Blockers: No real-world tests yet
   - Constraints: Requires deep codebase understanding

**Gate Criteria**:
- Has been tested on real codebase (not just fixtures)
- Performance is within acceptable limits
- Error handling is robust
- Operator runbooks exist
- Known limitations are documented

---

## Implementation Order

### Phase 4.1: Execute Real Codebase Test
**Time**: 1-2 hours
**Outcome**: Confirm end-to-end system works
**Blocker for**: Everything else (foundational test)

### Phase 4.2: Measure Performance Baseline
**Time**: 2-3 hours
**Outcome**: Concrete numbers on cost/time
**Prerequisites**: 4.1 complete

### Phase 4.3: Test Edge Cases
**Time**: 2-4 hours
**Outcome**: Identify failure modes and limits
**Prerequisites**: 4.1 complete

### Phase 4.4: Create Operator Runbooks
**Time**: 2-3 hours
**Outcome**: Production documentation
**Prerequisites**: 4.1-4.3 complete

### Phase 4.5: Production Gate Review
**Time**: 1 hour
**Outcome**: Go/no-go decision for each workflow
**Prerequisites**: 4.1-4.4 complete

---

## Critical Success Factors

1. **Real Testing Required**
   - Cannot use just fixtures and validation artifacts
   - Must run actual agent sessions on real repositories
   - Must measure real tokens and time

2. **Honest Assessment**
   - Document what works and what doesn't
   - Be clear about limitations and tradeoffs
   - Don't oversell readiness

3. **Operator Focus**
   - Documentation is for people who will RUN this system
   - Runbooks must be practical and actionable
   - Include troubleshooting and recovery procedures

4. **Cost Transparency**
   - Make costs explicit (tokens, time, money)
   - Provide cost/quality tradeoffs
   - Help operators make informed decisions

---

## Files to Create/Modify

| File | Purpose |
|------|---------|
| `PHASE-4-REAL-CODEBASE-TEST.md` | Results from Task 4.1 |
| `PHASE-4-PERFORMANCE.md` | Performance measurements from Task 4.2 |
| `PHASE-4-EDGE-CASES.md` | Edge case test results from Task 4.3 |
| `docs/runbooks/GETTING-STARTED.md` | Operator runbook from Task 4.4a |
| `docs/runbooks/INTERPRETATION-GUIDE.md` | Interpretation guide from Task 4.4b |
| `docs/runbooks/ERROR-TROUBLESHOOTING.md` | Troubleshooting from Task 4.4c |
| `docs/runbooks/PERFORMANCE-TUNING.md` | Performance tuning from Task 4.4d |
| `docs/runbooks/ESCALATION-PROCEDURES.md` | Escalation guide from Task 4.4e |
| `PHASE-4-PRODUCTION-GATE-REVIEW.md` | Gate review from Task 4.5 |
| `PHASE-4-COMPLETE.md` | Phase 4 completion summary |

---

## Success Metrics for Phase 4

- ✅ Real codebase test: Complete end-to-end execution
- ✅ Performance baseline: Concrete numbers for all workflows
- ✅ Edge cases tested: Identified failure modes and limits
- ✅ Operator runbooks: Complete documentation for production use
- ✅ Production gate review: Go/no-go decision for each component
- ✅ Known limitations documented: Clear scope boundaries
- ✅ Cost transparency: Explicit tokens/time/money metrics

---

## Phase 5 and Beyond

Once Phase 4 is complete:
- **Phase 5**: Production deployment and monitoring
- **Phase 6**: Continuous improvement based on real-world usage
- **Phase 7**: Scaling and optimization

But Phase 4 is the gate. Nothing moves to production without Phase 4 approval.

---

**Next Action**: Execute Task 4.1 - Real codebase test on sensemaking-skills repository.
