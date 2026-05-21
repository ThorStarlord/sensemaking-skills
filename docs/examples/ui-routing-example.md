# UI Routing Example

## Scenario: Dashboard Redesign Project

### Problem Statement
"Our React dashboard has grown to 30+ screens with inconsistent UI patterns. We need to understand the scope of redesign work before starting implementation."

### Execution

```bash
python scripts/workflow-runtime.py --mode guided_execution
```

**Input**: User's problem statement implies `ui_fog` (screen design, inconsistent patterns)

---

## Workflow Execution

### Phase 1-4: Diagnosis (full-local-sensemaking)

**Step 1: problem-framer**
- Frames the problem: "Inconsistent UI across 30+ screens"
- Object under pressure: "Dashboard screen consistency"
- Output: `problem_frame.md`

**Step 2: unknowns-mapper**
- Unknown: "What is the current design system state?"
- Unknown: "Which screens are most problematic?"
- Unknown: "How many component patterns are we dealing with?"
- Output: `unknowns_map.md` with `research_needed: true`

**Step 3: discovery** (conditionally invoked due to high uncertainty)
- Researches current screen inventory
- Identifies design pattern conflicts
- Output: `discovery_findings.md`

**Step 4: repo-sensemaker**
**Analysis Output** (machine-readable section):
```yaml
fog_type: ui_fog
evidence:
  - type: "Tier 1 Signal: Missing UI flow documentation"
    details: "Found 30+ screen files in /src/pages/ but no flow documentation in /docs/"
    file_path: "src/pages/"
  - type: "Tier 1 Signal: Components scattered without boundaries"
    details: "Component logic mixed with screen logic; no /components/ directory"
    file_path: "src/pages/"
  - type: "Tier 2 Signal: Low UI test coverage"
    details: "Only 2 E2E tests; no component tests"
    file_path: "test/"
user_implied_fog_type: ui_fog
diagnosis_conflict: false
escalation_recommended: false
```
- Output: `repository_sensemaking_brief.md`

**Step 5: workflow-planner**
**Decision Logic**:
```
fog_type = "ui_fog" (from repo-sensemaker)
→ Map to implementation workflow
→ recommend_workflow_id: "ui-implementation-workflow"
```
**Output** (machine-readable section):
```yaml
fog_type: ui_fog
recommended_workflow_id: ui-implementation-workflow
routing_alignment:
  fog_type_matches_workflow: true
  confidence: high
rationale: |
  Multiple Tier 1 signals confirm UI fog. User intent aligns with codebase diagnosis.
  Recommendation: Use ui-implementation-workflow to build out flows, screen specs, and implementation.
```
- Output: `workflow_orchestration_plan.md`

### Phase 7: Auto-Invocation Check

**Validation** (in workflow-runtime.py):
```
fog_type: "ui_fog"
workflow_id: "ui-implementation-workflow"
→ Validation: "ui_fog" → "ui-*-workflow" ✓ PASS
→ Log: "[OK] Workflow fog alignment validated: ui_fog → ui-implementation-workflow"
```

**Auto-Invocation Decision**:
- Source artifact: `workflow_orchestration_plan.md`
- Source field: `recommended_workflow_id: ui-implementation-workflow`
- → Chain to `ui-implementation-workflow`

---

## UI Implementation Workflow

### Step 1: docs-aligner
- Aligns CONTEXT.md with actual UI codebase state
- Creates shared terminology (button, form, card, modal)
- Output: `domain_alignment_report.md`

### Step 2: ui-flow
- Documents user journeys for 3-4 core workflows
- Maps screen transitions and navigation paths
- Output: `ui_flows.md`

### Step 3: ui-screen-spec
- Produces detailed specs for high-priority screens
- Documents component breakdowns
- Specifies interaction behaviors
- Output: `screen_specs.md`

### Step 4: to-issues
- Decomposes screen specs into implementation issues
- Groups related changes (e.g., Button redesign affects 12 screens)
- Creates tracer-bullet vertical slices
- Output: `issue_list.md`

### Step 5: triage
- Assigns issues to agent briefs
- Prioritizes by impact and dependency
- Output: `agent_brief.md`

### Step 6: tdd
- Implements changes using test-driven development
- Tests UI interactions, accessibility, responsive design
- Output: `code_patch.md` (git diff ready to apply)

### Step 7: handoff
- Summarizes session: what changed, what was learned
- Documents any scope expansions or conflicts
- Output: `session_summary.md`

---

## Validation Results

### Fog Type Classification
✅ **Correctly detected**: `ui_fog`  
Evidence cited:
- 3+ Tier 1 signals from `ui-fog-signals.yaml`
- User intent aligned with diagnosis
- No conflicts escalated

### Workflow Routing
✅ **Correctly routed**: → `ui-implementation-workflow`  
Validation:
- Fog type "ui_fog" requires workflow matching pattern "ui-*"
- Selected workflow "ui-implementation-workflow" matches
- Alignment: VALID

### Auto-Invocation Chain
✅ **Chaining successful**: `full-local-sensemaking` → `ui-implementation-workflow`  
Artifacts produced:
1. `repository_sensemaking_brief.md`
2. `workflow_orchestration_plan.md`
3. `domain_alignment_report.md`
4. `ui_flows.md`
5. `screen_specs.md`
6. `issue_list.md`
7. `agent_brief.md`
8. `code_patch.md`
9. `session_summary.md`

---

## Key Improvements Demonstrated

### 1. UI Fog Detection
- Explicitly checks for UI signals (flows, components, routing, design system)
- References `ui-fog-signals.yaml` for checkable indicators
- No longer vague classification

### 2. Fog Type Routing
- `workflow-planner` reads fog type from diagnosis
- Routes to appropriate implementation workflow
- Not hardcoded to one default

### 3. Validation & Auditing
- `_validate_workflow_fog_alignment()` prevents misrouting
- Logs fog type decision and validation result
- Audit trail in run log

### 4. UI-Specific Workflows
- `ui-diagnostic-workflow` for assessment-only runs
- `ui-implementation-workflow` for building solutions
- Both leverage the built-in UI skills (ui-brief, ui-flow, ui-screen-spec)

---

## Comparison: Before vs. After

| Aspect | Before | After |
|--------|--------|-------|
| **UI fog detection** | Vague, mentioned but not actionable | Explicit Tier 1/2/3 signals from registry |
| **Routing logic** | Hardcoded to `implementation-workflow` | Dynamic based on fog_type from workflow-planner |
| **UI workflows** | Existed but never invoked | Auto-invoked when `ui_fog` detected |
| **Validation** | No routing validation | Fog type alignment validated in Phase 7 |
| **User experience** | One-size-fits-all flow | Tailored workflows for each fog type |
| **Audit trail** | Limited fog type documentation | Complete fog type classification + routing decision log |

---

## Next Steps for This Project

1. **Diagnostic Phase Complete**: Review the `workflow_orchestration_plan.md`
2. **Plan Review Gate**: Approve the recommended workflow and scope
3. **Implementation Phase**: Execute `ui-implementation-workflow` in guided or autonomous mode
4. **Spec Review**: At each step (flows, screens, issues), review and approve before proceeding
5. **Implementation & Testing**: TDD cycles to implement the redesigned screens
6. **Delivery**: Code patch ready to apply to the repository
