# UI Routing Test Plan

## Overview
This document describes how to validate the UI diagnostic and implementation routing system introduced in the workflow improvements.

## Test Scenarios

### Scenario 1: UI Fog Detection & Routing (Positive Case)

**Objective**: Verify that a repository with clear UI fog signals is correctly classified as `ui_fog` and routed to the UI diagnostic/implementation workflows.

**Repository Characteristics**:
- Multiple screen files (`.tsx`, `.jsx`, `.vue`) scattered across different directories
- No central component library or `components/` directory
- Routing logic spread across 5+ files (not centralized)
- No design tokens or design system documentation
- Minimal documentation of user flows or screen layouts

**Setup**:
1. Create a test repository with these characteristics OR use an existing one matching this profile
2. Run: `python scripts/workflow-runtime.py --mode guided_execution --use-fixtures`
3. Provide user intent: "We need to improve our dashboard UX and navigation"

**Expected Outcome**:
- ✅ `repo-sensemaker` detects `primary_fog_type: ui_fog` (cites Tier 1 signals from ui-fog-signals.md)
- ✅ `workflow-planner` recommends `recommended_workflow_id: ui-diagnostic-workflow`
- ✅ Validation logs: `[OK] Workflow fog alignment validated: ui_fog → ui-diagnostic-workflow`
- ✅ Auto-invocation chains to `ui-diagnostic-workflow`
- ✅ `ui-brief` runs and produces `ui_specification` artifact
- ✅ `ui-flow` runs (from ui-implementation-workflow auto-invocation)

**Pass Criteria**:
- Run completes with exit code 0
- All artifacts produced with valid structure
- Run log shows fog type classification and routing decisions

---

### Scenario 2: Architecture Fog vs. UI Fog (Negative Case)

**Objective**: Verify that a repository with UI code but primary problem is architecture doesn't misclassify as UI fog.

**Repository Characteristics**:
- Well-organized UI code with clear component structure
- Proper design system in place
- User flows documented
- BUT: Module boundaries are unclear, high coupling between frontend and backend, circular dependencies

**Setup**:
1. Create or use a test repository matching these characteristics
2. Run: `python scripts/workflow-runtime.py --mode guided_execution --use-fixtures`
3. Provide user intent: "Our system is too slow and tightly coupled"

**Expected Outcome**:
- ✅ `repo-sensemaker` detects `primary_fog_type: architecture_fog` (despite UI code being present)
- ✅ `workflow-planner` recommends `recommended_workflow_id: implementation-workflow`
- ✅ Validation logs: `[OK] Workflow fog alignment validated: architecture_fog → implementation-workflow`
- ✅ Auto-invocation chains to `implementation-workflow`, NOT to ui-diagnostic-workflow

**Pass Criteria**:
- Run completes with exit code 0
- Correct fog type classification despite UI code presence
- Correct workflow routing (NOT ui-diagnostic-workflow)

---

### Scenario 3: Intent Override with Fog Type Conflict

**Objective**: Verify that when user intent conflicts with codebase diagnosis, system logs the conflict and uses intent as tiebreaker (soft context routing).

**Repository Characteristics**:
- Mixed signals: Some UI complexity but also architecture coupling
- No clear dominant fog type

**Setup**:
1. Create test repository with ambiguous signals
2. Run: `python scripts/workflow-runtime.py --mode guided_execution --use-fixtures`
3. Provide explicit user intent: "This is a UI redesign project" (implies ui_fog)

**Expected Outcome**:
- ✅ `repo-sensemaker` detects `diagnosis_conflict: true`
- ✅ `repo-sensemaker` records `user_implied_fog_type: ui_fog` vs `primary_fog_type: architecture_fog`
- ✅ `workflow-planner` acknowledges conflict and uses intent as tiebreaker
- ✅ `routing_divergence: true` logged with reason "intent_tiebreaker"
- ✅ Routes to `ui-diagnostic-workflow` based on user intent

**Pass Criteria**:
- Run completes with exit code 0
- Conflict explicitly logged in artifacts
- Routing decision documented with tiebreaker reason

---

## Validation Methods

### Method 1: Manual End-to-End Test

Run a complete workflow with guided execution and review each step:

```bash
python scripts/workflow-runtime.py --mode guided_execution
```

At each gate, review the artifact and verify:
- Fog type classification and evidence
- Workflow recommendation and routing logic
- Workflow alignment validation result

### Method 2: Automated Validation

Run the validator scripts on produced artifacts:

```bash
# Validate brief
python scripts/validate-artifact.py repository_sensemaking_brief artifacts/*/03-*.md

# Validate orchestration plan
python scripts/validate-artifact.py workflow_orchestration_plan artifacts/*/04-*.md

# Check routing alignment in run log
grep "workflow_routing_validated" artifacts/*/run-log.md
```

### Method 3: Regression Testing

After changes, run existing test suites to ensure no regressions:

```bash
python -m pytest examples/skill-tests/ -v
```

---

## Metrics to Track

For each test scenario, record:

1. **Fog Type Classification**:
   - Did `repo-sensemaker` correctly identify the primary fog type?
   - Did it cite Tier 1 signals from `ui-fog-signals.md`?

2. **Routing Decision**:
   - Did `workflow-planner` recommend the expected workflow?
   - If there was a conflict, was intent used as tiebreaker?

3. **Validation Results**:
   - Did `_validate_workflow_fog_alignment()` pass?
   - If not, was the mismatch reason logged?

4. **Auto-Invocation**:
   - Did the next workflow chain correctly?
   - Did all steps execute with expected artifacts?

5. **Run Log Completeness**:
   - Are all fog type decisions recorded?
   - Are routing divergences documented?
   - Are validation results included?

---

## Known Test Gaps

- **UI-specific fixtures**: No pre-built fixture repositories exist yet. Tests must create them dynamically or use real repositories.
- **E2E validation**: No automated test script exists to validate the full routing chain. Manual testing required for now.
- **Regression suite**: Existing test suite (`examples/skill-tests/`) needs updates to cover UI routing scenarios.

---

## Future Improvements

1. Create mock UI repositories in `examples/` with characteristic fog type signals
2. Build automated test runner for UI routing scenarios
3. Add UI routing validation to the continuous integration pipeline
4. Create performance benchmarks for fog type classification accuracy
