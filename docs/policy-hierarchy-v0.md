# Policy Hierarchy v0

**Status:** canonical agent-control architecture under Policy Hierarchy Completion v0  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, the Four-Level Control Model, and existing authority contracts  
**Construction authority:** Issue #399  
**Runtime status:** semantic policy contracts; not separate runtime services or deterministic semantic oracles

## 1. Purpose

Sensemaking already has strong strategy, durable decision state, authority, execution,
provenance, and assurance surfaces. Policy Hierarchy v0 makes the currently implicit
middle reasoning policies explicit so a capable coding agent can decide **what to learn,
how much reasoning to spend, when to broaden search, what is warranted, and what to
update after evidence returns** without turning those judgments into mandatory engines.

Canonical shape:

```text
VALUE / PURPOSE
      ↓
STRATEGIC POLICY
      ↓
INQUIRY POLICY
      ↓
METAREASONING POLICY
      ↓
EXPLORATION POLICY
      ↓
WARRANT / CHOICE POLICY
      ↓
ACTION / EXECUTION
      ↓
REALITY / EVIDENCE
      ↓
LEARNING / RECONCILIATION POLICY
      └──────────────────────────↺
```

These are semantic ownership layers, not a required phase machine.

## 2. Core laws

```text
policy layer
!= runtime service
!= mandatory ceremony
!= deterministic semantic oracle

capability exists
!= policy must activate

unresolved uncertainty
!= inquiry required

candidate exists
!= responsibility warranted

selection
!= authorization

mechanical validation
!= semantic correctness
```

The active semantic agent owns policy application unless authority is explicitly
delegated. Deterministic machinery may validate representation and integrity only where
the fact is mechanically decidable.

## 3. Existing layers reused unchanged

Policy Hierarchy Completion does not replace:

- Level 4 Product Thesis / Strategy Revision;
- Level 3 Strategic Repository Evolution;
- the Semantic Architecture evidence-to-decision grammar;
- Campaign / Responsibility / Uncertainty / Authority semantics;
- existing provenance, handoff, currentness, and durable-state surfaces;
- deterministic assurance and CI;
- the Execution Interface and external executor interchange.

## 4. Policy layers

### 4.1 Strategic Policy — existing

Level 3 asks what consequential repository-level responsibility is warranted next, if
any. Strategic alternatives may be zero or many. Strategic candidate generation is
conditional, not mandatory.

### 4.1.1 Stable Strategic Alternatives surface — Package 6 / integrated

Policy Hierarchy does not create a separate StrategicPlanner or alternatives engine.
The stable Level-3 alternatives surface is the existing
`strategic_repository_analysis.construction_paths` representation owned by
Strategic Repository Sensemaking v1.

Its cardinality is conditional:

```text
0–5 materially real construction paths

zero paths
= valid when no coherent construction trajectory is currently warranted/representable

BUILD
-> at least one real path
-> selected_path_id references that path
```

Alternative generation remains semantic-agent work. Mechanical validation checks
representation integrity only; it does not generate, rank, or select a path.

### 4.2 Inquiry Policy — Package 1 / integrated

Inquiry Policy asks:

> Given the current decision and epistemic state, what should we learn next, if
> anything?

It identifies whether additional evidence could materially change responsibility,
scope, authority path, continuation, verification, or closure and whether obtaining that
evidence is worth its cost.

Zero inquiry is a valid successful outcome.

Canonical agent-facing contract:
`skills/using-sensemaking/references/inquiry-policy-v0.md`.

### 4.3 Metareasoning Policy — Package 2 / integrated

Metareasoning Policy asks:

> Given the current decision, Inquiry Policy result, evidence, consequence,
> reversibility, authority, and resource cost, what kind of control move should
> consume the next unit of effort?

Canonical moves are:

```text
ACT
INQUIRE
CHALLENGE
EXPLORE
VERIFY
ESCALATE
STOP
```

These are semantic dispositions, not runtime enums or a required phase sequence.

Canonical agent-facing contract:
`skills/using-sensemaking/references/metareasoning-policy-v0.md`.

Inquiry Policy decides whether/what information is worth obtaining; Metareasoning
Policy decides what kind of effort should happen next in the broader decision context.

It remains qualitative and agent-owned.

### 4.4 Exploration Policy — Package 3 / integrated

Exploration Policy asks:

> Given meaningful search history, current evidence, uncertainty, resources, and
> decision context, where should iterative search effort go next?

Canonical qualitative search modes are:

```text
EXPLOIT
EXPLORE
CHALLENGE
DIAGNOSE
RECOMBINE
RESTART
VERIFY
EXIT_SEARCH
```

It becomes explicit only when search is materially iterative. One-shot reversible work
should normally keep this policy implicit.

Search history is a projection of existing evidence/provenance, not a new persisted
truth system.

Canonical agent-facing contract:
`skills/using-sensemaking/references/exploration-policy-v0.md`.

### 4.5 Warrant / Choice Policy — Package 4 / integrated

Warrant / Choice Policy asks:

> Given a specific contemplated target, current state, evidence, constraints, and
> authority, what is justified now—and if several targets are credibly warranted,
> which one should be selected, if any?

It is target-specific and defeasible.

Documentation-level dispositions include:

```text
WARRANTED
NOT_WARRANTED
MORE_EVIDENCE_REQUIRED
AUTHORITY_REQUIRED
OWNER_DECISION_REQUIRED
CHALLENGE_REQUIRED
EXPLORATION_REQUIRED
VERIFICATION_REQUIRED
SMALLER_INTERVENTION_PREFERRED
NO_SELECTION
```

It must preserve:

```text
warrant != confidence score
warrant != authorization
warrant for target A != warrant for target B
candidate set exists != one candidate must be selected
```

Canonical agent-facing contract:
`skills/using-sensemaking/references/warrant-choice-policy-v0.md`.

### 4.6 Learning / Reconciliation Policy — Package 5 / integrated

Learning / Reconciliation Policy asks:

> Given returned evidence and the current explicit decision model, what should change
> in claims, uncertainties, responsibility, continuation state, or strategic frame—if
> anything?

Canonical documentation-level dispositions include:

```text
NO_MODEL_CHANGE
CONFIRM
REVISE_CLAIM
RESOLVE_UNCERTAINTY
OPEN_NEW_UNCERTAINTY
CHANGE_RESPONSIBILITY
CONTINUE
STOP
ESCALATE
REOPEN_STRATEGY
THESIS_REVIEW_REQUIRED
```

Returned evidence does not mutate semantic state automatically. Reconciliation writes
through existing Campaign/STATUS/ADR/handoff/evidence/strategic surfaces rather than
creating a generic belief database.

Canonical agent-facing contract:
`skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`.

### 4.7 Adaptive Policy Coordinator — Package 7 / integrated

Adaptive Policy Coordinator v0 asks:

> Which policy questions are decision-relevant now, and what is the smallest
> sufficient composition that preserves evidence, authority, and stopping
> boundaries?

Its governing rule is:

```text
clear + local + reversible + sufficiently evidenced
-> direct bounded work + relevant verification

ambiguous / consequential / iterative / authority-sensitive
-> expose only the policy questions that can materially change the decision
```

Zero explicitly surfaced policy layers is valid for obvious bounded work. The
coordinator is semantic composition guidance owned by the active agent; it is not a
router, planner, scheduler, state machine, score, or runtime service.

Canonical agent-facing contract:
`skills/using-sensemaking/references/adaptive-policy-coordinator-v0.md`.

## 5. Activation principle

Visible policy structure should scale with decision pressure.

Useful triggers include:

- consequential unresolved uncertainty;
- low reversibility;
- protected external commitments;
- multiple credible responsibility boundaries;
- repeated failure;
- narrow or unstable option sets;
- costly continuation across contexts;
- weak evidence behind a strong commitment;
- unclear closure or verification.

For an obvious local reversible task, most policy reasoning may remain implicit.

## 6. Durability

Persist policy results only when a fresh context or another actor needs them to
reconstruct a consequential decision.

Use existing surfaces first:

- `STATUS.md`;
- Campaign state / handoff / evidence;
- ADRs;
- semantic-state companions;
- execution handoff/result;
- repository history.

Do not persist hidden chain-of-thought.

## 7. Construction sequence

Policy Hierarchy Completion v0 proceeds as bounded packages:

1. Inquiry Policy v0 — integrated;
2. Metareasoning Policy v0 — integrated;
3. Exploration Policy v0 — integrated;
4. Warrant / Choice Policy v0 — integrated;
5. Learning / Reconciliation Policy v0 — integrated;
6. stable Strategic Alternatives surface — integrated through Strategic Repository Sensemaking v1;
7. Adaptive Policy Coordinator v0 — integrated.

A later package may revise the order only when a concrete dependency warrants it.

## 8. Explicit non-goals

This architecture does not authorize:

- generic `AgentState`;
- generic memory or search-tree database;
- Campaign schema v3 merely to mirror policy concepts;
- deterministic semantic routing;
- numeric inquiry, warrant, priority, or intelligence scores;
- automatic Skill/workflow/Campaign selection;
- an `OuterLoopEngine` finite-state controller;
- automatic product-thesis revision;
- autonomous merge, release, deployment, or publication authority.

## 9. Completion criterion

Policy Hierarchy Completion v0 is complete when the missing middle policies have
explicit agent-facing contracts, compose coherently with existing strategy/execution
surfaces, preserve zero-work outcomes and authority boundaries, and can be used through
ordinary repository work without requiring a parallel truth system.
