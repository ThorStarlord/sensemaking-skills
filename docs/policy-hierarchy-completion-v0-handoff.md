# Policy Hierarchy Completion v0 — Closeout Handoff

**Milestone authority:** Issue #399  
**Status:** completion candidate; becomes integrated closeout when the final Package 7 PR is merged and exact-main qualification passes  
**Primary product boundary:** agent-native repository decision support with semantic judgment owned by the active agent

## 1. Objective

Complete the missing middle semantic-control layers between Level-3 strategy and action/evidence/learning without building a generic autonomous-agent runtime.

Canonical composition:

```text
STRATEGIC POLICY
-> INQUIRY POLICY
-> METAREASONING POLICY
-> EXPLORATION POLICY
-> WARRANT / CHOICE POLICY
-> ACTION / EXECUTION
-> REALITY / EVIDENCE
-> LEARNING / RECONCILIATION POLICY
-> reassess
```

Adaptive Policy Coordinator v0 controls progressive disclosure of these questions; it is not another runtime layer.

## 2. Integrated package set

### Package 1 — Inquiry Policy v0

Decides what to learn next, if anything. `NO_INQUIRY_NEEDED` is valid; uncertainty does not automatically justify investigation.

### Package 2 — Metareasoning Policy v0

Allocates the next unit of effort qualitatively across `ACT / INQUIRE / CHALLENGE / EXPLORE / VERIFY / ESCALATE / STOP` without a control engine or score.

### Package 3 — Exploration Policy v0

Allocates materially iterative search across `EXPLOIT / EXPLORE / CHALLENGE / DIAGNOSE / RECOMBINE / RESTART / VERIFY / EXIT_SEARCH` while reusing existing evidence/provenance rather than creating SearchState.

### Package 4 — Warrant / Choice Policy v0

Adjudicates a specific target using current evidence/state/constraints/authority. Warrant remains target-specific, defeasible, and non-authorizing; `NO_SELECTION` is valid.

### Package 5 — Learning / Reconciliation Policy v0

Interprets consequential returned evidence into explicit claim/uncertainty/responsibility/continuation/strategic changes. `NO_MODEL_CHANGE` is valid; evidence does not mutate semantic state automatically.

### Package 6 — Stable Strategic Alternatives surface

Reuses Strategic Repository Sensemaking v1 rather than adding a planner. `construction_paths` supports 0–5 materially real paths; zero is valid when no coherent construction trajectory is currently warranted/representable, while `BUILD` requires a selected real path.

### Package 7 — Adaptive Policy Coordinator v0

Selects the smallest decision-relevant composition of semantic policy questions. Zero explicit policy layers is valid for clear bounded work; policy ceremony collapses when its decision value disappears.

## 3. Canonical laws preserved

```text
policy layer
!= runtime service
!= mandatory ceremony
!= deterministic semantic oracle

capability exists
!= policy must activate

selection
!= authorization

mechanical validation
!= semantic correctness

desired delegation
!= granted authority
```

## 4. Reused product surfaces

No parallel truth system was introduced. The milestone reuses:

- Strategic Repository Sensemaking / Level-3 state;
- Campaign / Responsibility / Uncertainty / Authority semantics;
- existing handoff/resume/evidence/provenance surfaces;
- ADR and product-strategy authority;
- deterministic validators and CI;
- Execution Interface / external executor evidence return;
- existing adaptive guidance and progressive disclosure.

## 5. Explicit non-goals preserved

The milestone does **not** establish or authorize:

- generic AgentState or CoordinatorState;
- generic memory / search-tree / belief database;
- Campaign schema v3 merely to mirror policies;
- WarrantEngine, LearningEngine, StrategicPlanner, OuterLoopEngine, or PolicyCoordinator runtime service;
- numeric inquiry/warrant/priority/intelligence/policy-activation scores;
- deterministic semantic routing;
- automatic Skill/workflow/Campaign selection;
- automatic product-thesis revision;
- autonomous merge, release, deployment, or publication authority;
- comparative superiority, native-harness usefulness, or product-market-value claims;
- RC3 freeze or PyPI publication.

## 6. Completion claim

Policy Hierarchy Completion v0 is complete when Package 7 is integrated and exact-main Product Validation / Release Candidate Distribution are green.

The completion claim is limited to:

- explicit canonical agent-facing contracts;
- coherent composition with existing strategy/execution/evidence surfaces;
- zero-work/zero-ceremony outcomes;
- preserved authority/evidence boundaries;
- repository-mechanical qualification of those representation contracts.

It does not establish semantic optimality or empirical superiority.

## 7. Post-closeout repository state

Policy Hierarchy becomes a **composable capability baseline**, not the active construction program.

The active Level-3 construction program remains Strategic Repository Sensemaking v1 under Issue #401 until that independently reaches its own closeout.

```text
POLICY HIERARCHY COMPLETION V0
-> COMPLETE / INTEGRATED / COMPOSABLE

STRATEGIC REPOSITORY SENSEMAKING V1
-> remains separately active
```

## 8. Reopen condition

Reopen Policy Hierarchy construction only when normal use exposes a concrete decision-support gap that cannot be addressed by the existing semantic contracts, adaptive composition, or current durable surfaces.

Do not reopen merely because additional policy machinery can be imagined.
