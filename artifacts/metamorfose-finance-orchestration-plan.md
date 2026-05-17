# Workflow Orchestration Plan: Metamorfose Finance UI Improvement

## 1. Diagnosis summary

**Problem Frame**: Finance UI lacks spec-driven architecture; UI has grown organically without clear domain model or specifications.

**Unknowns Map**: 9 explicit unknowns identified; clarity_assessment = medium; research_needed = true

**Weakest Boundary**: Implicit data contract between Dashboard → Aggregation Layer → n8n Workflows. Dashboard state machine, action semantics, and error recovery are undefined.

**Dynamic Routing Signal Triggered**: research_needed = true → discovery/research skills should be inserted before implementation.

## 2. Recommended workflow sequence

### Phase 1: Domain Discovery (External Skills)
**Workflow:** `product-discovery-sprint`

**Objective**: Convert implicit finance workflows into explicit domain specification

**Skills to run:**
1. `persona` — Identify finance operator personas and their mental models
2. `discovery` — Interview operators about current workflows, pain points, decision logic
3. `interview-synthesis` — Extract patterns from operator interviews
4. `opportunity-tree` — Map problems (UI complexity, confusion about state) to solutions (clear spec, clearer UX)
5. `hypothesis` — Define testable bet: "A clear domain spec + spec-driven UI will reduce operator errors and onboarding time"

**Expected outputs:**
- Persona definition for finance operators
- Discovery findings detailing current workflows
- Synthesis report extracting domain concepts
- Opportunity map showing root causes of complexity
- Validated hypothesis about benefits of spec-driven approach

**Duration estimate**: 4-6 hours (includes operator interviews)

---

### Phase 2: UI Flow & Screen Specification (Interface Skills)
**Workflow:** TBD (custom composition using interface-skills)

**Objective**: Convert domain spec into concrete UI specifications

**Skills to run (in sequence):**
1. `ui-flow` — Document multi-screen journeys:
   - Finance Capture-to-Reconciliation Flow (inbox → review → post → verify → reconcile → close)
   - Transaction Detail & Verification Flow
   - Month Closing & Reporting Flow
   - Error Recovery Flow (what to do when validation fails)
   
2. `ui-screen-spec` — Specify each finance screen:
   - Dashboard (what state should it show, what actions should it enable)
   - Inbox (what is an "item", what are valid transitions)
   - Transaction Ledger (what fields, what validations, what verification workflow)
   - Reconciliation (what is being reconciled, what are decision points)
   - Reports (what reports, what data, what export formats)

**Expected outputs:**
- UI Flow documentation for each finance journey
- Screen specs for each finance page
- Data model clarifications grounded in UI requirements

**Duration estimate**: 6-8 hours

---

### Phase 3: Implementation (Local Skills)
**Workflow:** TBD (custom code-generation or TDD workflow using Matt Pocock skills)

**Objective**: Implement spec-driven refactoring of finance UI

**High-level approach:**
1. Extract domain model into TypeScript types (Account, Transaction, Category, Month, ReconciliationItem)
2. Define state machine explicitly (use a library like XState or simple enum switch)
3. Refactor Dashboard aggregation layer (split into smaller, independently testable functions)
4. Create UI component library with consistent styling/patterns
5. Update error handling to match error recovery flows

**Expected outputs:**
- Refactored finance subsystem
- Domain types file
- State machine definition
- Improved test coverage
- Updated error messages to match spec

**Duration estimate**: 2-3 days

---

## 3. Execution mode

**Recommended mode**: `guided_execution` (plan_only initially, then step through with approval gates)

**Rationale**:
- Phase 1 (discovery) requires external team input (operator interviews) → plan_only to confirm approach
- Phase 2 (UI specs) can be autonomous but benefits from periodic review → guided execution with checkpoints
- Phase 3 (implementation) should be spec-driven TDD → guided with test/commit gates

---

## 4. Approval gates

| Phase | Gate | Approval Criteria |
|-------|------|-------------------|
| 1 | review_discovery_findings | Operator interviews are complete and 5+ pain points are documented |
| 1 | review_domain_spec | Domain spec defines state machine, all valid transitions, and operator personas |
| 2 | review_ui_flows | All finance journeys are documented with decision points and error cases |
| 2 | review_screen_specs | Each screen spec matches domain spec and UX requirements are unambiguous |
| 3 | review_code_refactor | Refactored code passes tests and domain types are used consistently |

---

## 5. Stop conditions

**Phase 1 stops when:**
- All 5+ pain points are traced to root causes
- Domain concepts are named and bounded (Account vs. Budget, Transaction vs. Ledger Entry, etc.)
- State machine transitions are enumerated and validated with operators

**Phase 2 stops when:**
- Every finance screen has a spec
- Every spec includes happy path + error cases
- Specs are validated against domain spec (no conflicts)

**Phase 3 stops when:**
- All tests pass
- Code compiles without type errors
- Domain types are used in all finance-related functions
- Error handling matches error recovery flows from spec

---

## 6. Why this sequence

1. **Discovery first** (product-discovery-sprint): Operators know what they need, but it's tacit knowledge. Extracting it into a spec prevents implementation of the "wrong thing faster."

2. **UI flows second** (ui-flow + ui-screen-spec): Flows show the journey; screen specs show the detailed requirements. This order ensures we understand workflows before specifying individual screens.

3. **Implementation third** (TDD): With specs in place, implementation becomes straightforward translation of spec to code.

4. **Gated execution**: Each gate ensures the next phase has correct input (spec from discovery drives UI specs, UI specs drive code).

---

## 7. Decision policy

**Business decisions are proposed until approved:**
- Phase 1 may discover that operators need a different state machine than what's currently implemented
- Phase 2 may discover that current UI structure doesn't match operator mental models
- These are design decisions that should be reviewed before committing to implementation

**Technical decisions can be made autonomously:**
- How to implement state machine (XState vs. enum switch vs. custom)
- Whether to extract a shared component library
- Testing strategy

---

## 8. Risks & mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Operators unavailable for interviews | Phase 1 blocked | Schedule interviews early; offer async alternatives (Slack, written Q&A) |
| Domain spec contradicts current code | Phase 2 blocked | Treat as discovery signal; code may be buggy or outdated; validate with operators |
| Screen specs are too detailed for implementers | Phase 3 slowed | Keep specs at "what" level, not "how" level; let implementers choose implementation |
| Spec refactoring breaks existing workflows | Phase 3 regression | Run full finance workflow tests during implementation; test migration strategy |

---

## 9. Success metrics

- **Phase 1**: Operators feel the spec reflects their actual workflow (subjective) + state machine has 0 ambiguous transitions (objective)
- **Phase 2**: Screen specs are detailed enough for 2 independent implementers to build identical UIs (testable) + 100% coverage of finance screens (objective)
- **Phase 3**: All tests pass + 0 type errors + operators report reduced confusion about system state (subjective)

---

## 10. Machine-readable handoff

```yaml
workflow_selected: product-discovery-sprint
execution_mode: guided_execution
gate_sequence:
  - review_discovery_findings
  - review_domain_spec
  - review_ui_flows
  - review_screen_specs
  - review_code_refactor
phase_1_skills:
  - persona
  - discovery
  - interview-synthesis
  - opportunity-tree
  - hypothesis
phase_2_skills:
  - ui-flow
  - ui-screen-spec
phase_3_skills:
  - tdd
weakest_boundary_addressed: |
  Dashboard → Aggregation Layer implicit contract
  Solution: Explicit domain spec → state machine → UI specs → refactored code
```

---

## 11. Next immediate steps

1. **Confirm Phase 1 approach** ← APPROVAL GATE
   - Schedule operator interview(s) (target: 1-2 hours)
   - Prepare discovery interview script based on problem frame

2. **Run product-discovery-sprint workflow**
   - Execute persona skill
   - Execute discovery skill (with operator input)
   - Execute interview-synthesis + opportunity-tree + hypothesis
   - Gather outputs: domain spec, state machine, validated hypothesis

3. **Review discovery outputs** ← APPROVAL GATE
   - Confirm spec aligns with actual operator workflows
   - Validate state machine with operators

4. **Schedule Phase 2** (UI flows & specs)
   - Confirm operator availability for spec validation

---

## 12. Ready-to-copy prompts

### Prompt 1: Start product-discovery-sprint
> I'm using product-discovery-sprint to understand the domain workflows of Metamorfose Edutech's finance system. The system captures, validates, reconciles, and reports on financial transactions. The dashboard is complex (20+ UI sections, 40+ state variables) and operators struggle to understand readiness state and know what action to take next.
>
> Input: Repository Sensemaking Brief identifying the dashboard ↔ aggregation layer as the weakest boundary.
>
> Goal: Extract the implicit finance workflows into an explicit domain spec including:
> - What a "transaction" is and its lifecycle
> - What "verify" means and when it's required
> - What "reconciliation" means and how it differs from verification
> - What makes a month "ready to close"
> - What the dashboard should tell operators about each of these concepts
>
> Please run: persona → discovery → interview-synthesis → opportunity-tree → hypothesis

### Prompt 2: Start ui-flow after discovery
> I have a domain specification for the Metamorfose finance system. Now I need to document the user journeys that operators follow to accomplish key tasks.
>
> Key journeys to document:
> 1. Finance Capture-to-Reconciliation (inbox → review → post → verify → reconcile → close month)
> 2. Transaction Verification (find unverified transaction → review details → mark as verified)
> 3. Error Recovery (validation fails → understand error → fix → retry)
>
> The domain spec clarifies concepts but the journeys show how operators actually move through the system. Please create a UI Flow documenting these journeys with screens, decisions, and error cases.

---

## 13. Handoff to downstream skills

This plan is ready to hand off to:
- **product-discovery-sprint** workflow (Phase 1)
- **ui-flow** skill (Phase 2, journey documentation)
- **ui-screen-spec** skill (Phase 2, screen-level requirements)
- **tdd** workflow (Phase 3, implementation)

Each downstream skill receives:
- This orchestration plan
- Repository sensemaking brief
- Problem frame & unknowns map
- One validated artifact from the previous phase
