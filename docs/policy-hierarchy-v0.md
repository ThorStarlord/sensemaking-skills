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

### 4.4 Exploration Policy — planned

Exploration Policy will allocate effort across iterative search modes only when a real
search history exists. Candidate modes include exploit, explore, challenge, diagnose,
recombine, restart, and verify.

One-shot reversible work should normally keep this policy implicit.

### 4.5 Warrant / Choice Policy — planned

Warrant / Choice Policy will adjudicate whether a contemplated responsibility,
inquiry, action, continuation, verification, or closure claim is justified now.

It must preserve:

```text
warrant != confidence score
warrant != authorization
warrant != majority vote
```

### 4.6 Learning / Reconciliation Policy — planned

Learning / Reconciliation Policy will state what explicit repository-domain model
changes after evidence returns: claim revision, uncertainty resolution, responsibility
change, continuation, stop, escalation, or strategic reopening.

It will write through existing durable surfaces rather than creating a generic belief
database.

### 4.7 Adaptive Policy Coordinator — later composition

A later coordinator may compose the individual policy contracts after they exist. It
must permit compression:

```text
clear + local + reversible
-> direct bounded work + verification

ambiguous / consequential
-> expose only the policy layers needed for the decision
```

The coordinator must not require all layers on every task.

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
3. Exploration Policy v0;
4. Warrant / Choice Policy v0;
5. Learning / Reconciliation Policy v0;
6. stable Strategic Alternatives surface;
7. Adaptive Policy Coordinator v0.

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
