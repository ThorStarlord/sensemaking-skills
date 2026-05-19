# Fog Type Routing Test

## Test Case: Metamorfose Finance UI Problem

**Source**: `artifacts/01-metamorfose-finance/04-orchestration-plan.md`

### Analysis

**Problem Statement**: Finance UI lacks spec-driven architecture; UI has grown organically without clear domain model or specifications.

**Weakest Boundary**: Implicit data contract between Dashboard → Aggregation Layer. Dashboard state machine, action semantics, and error recovery are undefined.

**Recommended Workflow Sequence**:
- Phase 1: Domain Discovery (persona, discovery, interview-synthesis, opportunity-tree)
- Phase 2: UI Flow & Screen Specification (ui-flow, ui-screen-spec)
- Phase 3: Implementation (TDD)

### Fog Type Classification

**Classified as**: `ui_fog` ✓

**Reasoning**:
- Weakest boundary is UI-related (Dashboard state machine, screen specifications)
- Recommended workflow explicitly includes ui-flow and ui-screen-spec skills
- Problem is about UI complexity, navigation, and screen design
- research_needed = true indicates need for discovery before implementation

### Routing Decision

**Workflow Selected**: `ui-implementation-workflow`

**Sequence**:
1. grill-with-docs → align domain understanding, create CONTEXT.md (gate: none ✓)
2. ui-flow → document user journeys and transitions (gate: none ✓)
3. ui-screen-spec → specify each screen's content and interactions (gate: none ✓)
4. to-issues → break into implementation issues (gate: none ✓)
5. triage → create agent briefs (gate: none ✓)
6. tdd → implement via TDD cycles (gate: none ✓)
7. handoff → completion summary (gate: session_close ⏸)

### Expected Behavior (Autonomous Execution)

1. Sensemaking pipeline runs (problem-framer → unknowns-mapper → repo-sensemaker)
2. Repo-sensemaker produces brief with `fog_type: ui_fog`
3. Orchestrator reads fog_type and selects `ui-implementation-workflow`
4. All 6 implementation steps execute automatically without pausing between steps
5. Artifacts flow: context → ui_flows → screen_specs → issue_list → agent_brief → code_patch → completion_summary
6. Final gate (session_close) pauses for user review before completing

---

## Other Test Cases (Expected Behavior)

### Product Fog Example
**Problem**: "Unclear what finance operators actually need; workflows are implicit knowledge"
**Fog Type**: `product_fog`
**Workflow**: `product-implementation-workflow`
**Sequence**: grill-with-docs → discovery → opportunity-tree → to-prd → to-issues → triage → tdd → handoff

### Architecture Fog Example
**Problem**: "Code structure is unclear; no domain types; state management is implicit"
**Fog Type**: `architecture_fog`
**Workflow**: `implementation-workflow` (default)
**Sequence**: grill-with-docs → to-prd → to-issues → triage → tdd → handoff

### Docs Fog Example
**Problem**: "Documentation is missing; no spec for what system does"
**Fog Type**: `docs_fog`
**Workflow**: `docs-implementation-workflow`
**Sequence**: grill-with-docs → to-prd → handoff

---

## Validation Checklist

- [x] Fog type classification added to repo-analysis-template
- [x] Repo-sensemaker workflow includes classification step
- [x] Orchestration-plan template includes fog_type field
- [x] Machine-readable plan includes fog_type and recommended_implementation_workflow
- [x] Workflow-orchestrator skill has routing logic documented
- [x] 4 specialized implementation workflows created (product, ui, docs, architecture)
- [x] All implementation workflows use gate: none for high-velocity execution
- [ ] End-to-end test run with real repository (next step)

---

## Next Steps

1. Run full-local-sensemaking on a test repository to verify repo-sensemaker classifies fog_type
2. Verify orchestration-plan includes fog_type field
3. Test routing: confirm orchestrator invokes correct implementation workflow
4. Monitor artifact flow between steps
5. Verify all 6 implementation steps execute without pausing (when using autonomous_execution)
