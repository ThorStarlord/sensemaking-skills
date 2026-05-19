# Implementation Workflow Guide

This guide explains how the dynamic workflow routing system works and how to use it effectively.

## Overview

The sensemaking-skills system now provides **end-to-end automation** from diagnosis to implementation:

```
Sensemaking Stage (Diagnosis)
  ↓
  problem-framer → unknowns-mapper → repo-sensemaker → workflow-orchestrator
  ↓ produces: orchestration-plan with fog_type classification
  ↓
Implementation Stage (Execution)
  ↓ automatic routing based on fog_type
  ↓
  → product-implementation-workflow (product problems)
  → ui-implementation-workflow (UI problems)
  → docs-implementation-workflow (docs problems)
  → implementation-workflow (architecture/code problems)
  ↓
  All steps execute automatically without approval pauses (in autonomous mode)
```

## Fog Type Classification

Sensemaking produces a **fog_type** that determines which implementation workflow to use:

### product_fog
**Symptoms**: Unclear user needs, vague feature requirements, undocumented workflows

**What repo-sensemaker looks for**:
- Missing persona documentation
- Undocumented business logic
- Implicit user workflows
- Unclear feature requirements

**Implementation workflow used**: `product-implementation-workflow`

**Sequence**:
1. grill-with-docs - align on domain
2. discovery - interview stakeholders
3. opportunity-tree - map problems to solutions
4. to-prd - create product specification
5. to-issues - decompose into issues
6. triage - prepare agent briefs
7. tdd - implement
8. handoff - complete

### ui_fog
**Symptoms**: Navigation complexity, screen design issues, interaction patterns unclear

**What repo-sensemaker looks for**:
- Complex navigation without documented flows
- Unclear screen purposes or interactions
- Missing UX specifications
- Weakest boundary involves UI/frontend

**Implementation workflow used**: `ui-implementation-workflow`

**Sequence**:
1. grill-with-docs - align on domain
2. ui-flow - document user journeys
3. ui-screen-spec - specify screens
4. to-issues - decompose into issues
5. triage - prepare agent briefs
6. tdd - implement
7. handoff - complete

### docs_fog
**Symptoms**: Missing documentation, unclear specifications, knowledge silos

**What repo-sensemaker looks for**:
- No CONTEXT.md or system documentation
- Missing API specifications
- Undocumented architecture
- Knowledge concentrated in one person

**Implementation workflow used**: `docs-implementation-workflow`

**Sequence**:
1. grill-with-docs - align understanding
2. to-prd - create documentation spec
3. handoff - complete

### architecture_fog (default)
**Symptoms**: Code structure problems, design boundaries unclear, implicit contracts

**What repo-sensemaker looks for**:
- Implicit state management
- Unclear module boundaries
- No domain types or models
- Weak contracts between systems

**Implementation workflow used**: `implementation-workflow`

**Sequence**:
1. grill-with-docs - align on domain
2. to-prd - create specification
3. to-issues - decompose into issues
4. triage - prepare agent briefs
5. tdd - implement
6. handoff - complete

## Execution Modes

### plan_only
Shows the orchestration plan and fog type classification. No execution.

```
User: Run full-local-sensemaking with plan_only
Result: See orchestration-plan.md with fog_type and recommended workflow
```

### guided_execution
Executes sensemaking stage step-by-step with approval gates. When sensemaking completes, asks user before starting implementation workflow.

```
User: Run full-local-sensemaking with guided_execution
Result: 
  1. Execute sensemaking step-by-step (with approval gates)
  2. Show orchestration-plan with fog_type
  3. Ask: "Continue to product-implementation-workflow?"
  4. If approved: Execute implementation workflow (steps run automatically without pausing)
  5. Final gate before completion summary
```

### autonomous_execution
Executes sensemaking, automatically routes to appropriate implementation workflow, runs all steps automatically. No approval gates between steps (except final gate before completion).

```
User: Run full-local-sensemaking with autonomous_execution
Result:
  1. Sensemaking completes (no approval pauses)
  2. Orchestrator reads fog_type from orchestration-plan
  3. Routes to appropriate implementation workflow
  4. Implementation workflow executes end-to-end (all gate: none steps auto-continue)
  5. Final gate pauses for completion review
```

## Explicit Workflow Override

If you want to use a different implementation workflow than the one auto-selected:

**In the orchestration-plan**, add:

```yaml
fog_type: product_fog
recommended_implementation_workflow: ui-implementation-workflow  # override
```

The orchestrator will use the explicit override instead of the auto-selected workflow.

## Error Handling

If a step fails during implementation:

1. **Failure is recorded** in the run log with:
   - Step ID and skill name
   - Error type and message
   - Recommended recovery command

2. **Execution stops immediately** (fail-fast approach)

3. **Recommended next action** is provided:
   - Review error logs
   - Fix the underlying issue
   - Switch to guided_execution mode for inspection
   - Re-run with manual approval

4. **No automatic retry** - manual intervention required

## High-Velocity Execution

Implementation workflows use `gate: none` for steps between sensemaking and final completion:

```
1. grill-with-docs (gate: none ✓ auto-continue)
2. discovery (gate: none ✓ auto-continue)
3. to-prd (gate: none ✓ auto-continue)
4. to-issues (gate: none ✓ auto-continue)
5. triage (gate: none ✓ auto-continue)
6. tdd (gate: none ✓ auto-continue)
7. handoff (gate: session_close ⏸ pauses for review)
```

This allows the system to execute at high velocity without user intervention between steps, while still pausing at the final gate for human approval before completing.

## Graceful Degradation

If sensemaking cannot clearly classify the fog type:

1. **fog_type** is set to "uncertain" or "mixed"
2. **Default workflow** (`implementation-workflow`) is used
3. **Note is logged**: `fog_type_confidence: low`
4. System continues safely without routing errors

## Artifact Flow

Artifacts flow automatically between steps:

```
orchestration-plan (from sensemaking)
  ↓
grill-with-docs ← consumes plan, produces ↓ context.md
  ↓
discovery ← consumes context, produces ↓ discovery_findings
  ↓
opportunity-tree ← consumes findings, produces ↓ opportunity_map
  ↓
to-prd ← consumes map, produces ↓ prd
  ↓
to-issues ← consumes prd, produces ↓ issue_list
  ↓
triage ← consumes issues, produces ↓ agent_brief
  ↓
tdd ← consumes briefs, produces ↓ code_patch
  ↓
handoff ← consumes patch, produces ↓ completion_summary
```

Each step:
- Reads the previous step's output artifact
- Performs its function
- Produces a new artifact
- Automatically hands off to the next step

## Real-World Example: Metamorfose Finance UI

**Problem**: Finance UI lacks spec-driven architecture; unclear state management.

**Sensemaking diagnosis**:
```yaml
weakest_boundary: "Dashboard state machine, action semantics, and error recovery are undefined"
fog_type: ui_fog
recommended_workflow: ui-implementation-workflow
```

**Automatic routing**:
```
orchestrator sees fog_type: ui_fog
  ↓
invokes ui-implementation-workflow
  ↓
1. grill-with-docs → understand finance domain, create CONTEXT.md
2. ui-flow → document all finance UI journeys (capture→review→post→reconcile)
3. ui-screen-spec → specify each finance screen (Dashboard, Inbox, Ledger, Reports)
4. to-issues → break specs into implementation issues
5. triage → create agent briefs for each issue
6. tdd → implement screens with test-driven development
7. handoff → completion summary
```

**Result**: Spec-driven UI architecture with clear state machine, documented workflows, and type-safe implementations.

## Next Steps

1. **Run sensemaking** on your repository to get a fog type classification
2. **Review the orchestration-plan** to see which workflow will be used
3. **Choose execution mode**:
   - `plan_only` - review the plan first
   - `guided_execution` - step through with approval gates
   - `autonomous_execution` - full end-to-end automation
4. **Monitor the implementation workflow** as it executes
5. **Review artifacts** at each step to verify progress
