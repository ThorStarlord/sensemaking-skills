# Delegated Goal Patterns

Use this reference when a user gives the active coding agent a repository-level outcome, terminal mission, or broad repair/improvement goal rather than one mechanically narrow implementation task.

These are **delegation contracts**, not prompt-engineering tricks. They clarify the desired outcome, authoritative scope, operating policy, authority boundary, and stopping conditions while leaving semantic responsibility selection with the active agent.

For adaptive scaffolding/rigor/durability guidance, see [`adaptive-guidance-v0.md`](adaptive-guidance-v0.md). This document does not replace those rules and does not define scores, modes, automatic routing, or automatic Campaign selection.

## Contents

1. [Core structure](#1-core-structure)
2. [Pattern: bounded implementation](#2-pattern-bounded-implementation)
3. [Pattern: repository diagnosis](#3-pattern-repository-diagnosis)
4. [Pattern: next warranted improvement](#4-pattern-next-warranted-improvement)
5. [Pattern: complete authoritative product scope](#5-pattern-complete-authoritative-product-scope)
6. [Pattern: repair to verified closure](#6-pattern-repair-to-verified-closure)
7. [Pattern: architecture/design reconciliation](#7-pattern-architecture--design-reconciliation)
8. [Pattern: long-running delegated development](#8-pattern-long-running-delegated-development)
9. [Prompt anti-patterns](#9-prompt-anti-patterns)
10. [Choosing a pattern](#10-choosing-a-pattern)

## 1. Core structure

A strong high-delegation repository goal normally contains five parts:

```text
GOAL
What outcome should become true?

OPERATING POLICY
How should the agent determine warranted intermediate responsibilities?

SCOPE DISCIPLINE
Which sources define required work, and which sources are merely ideas/history?

AUTHORITY DISCIPLINE
What judgment is delegated, and which actions/decisions remain reserved?

STOP CONDITIONS
What makes the mission legitimately terminal?
```

The user may omit parts when they are already established elsewhere. Do not demand boilerplate for a narrow task.

The central rule is:

```text
high delegation
!= unlimited scope
!= unlimited authority
!= permission to invent work
```

## 2. Pattern: bounded implementation

### When to use

Use when the responsibility, intended behavior, and affected boundary are already sufficiently known.

### Ready-to-copy prompt

```text
Goal: Implement the specified change within the established scope and satisfy its applicable acceptance criteria.

Operating policy: Reconstruct the current affected state before editing. Resolve any local decision-changing uncertainty that could make the specified implementation wrong. Keep the responsibility bounded; do not broaden into repository strategy unless current evidence shows the requested responsibility is invalid or unsafe.

Scope discipline: Change only the surfaces required by the established specification and their necessary tests/docs/contracts.

Authority discipline: Perform only authorized repository-local/reversible work. Do not infer merge, release, deployment, publication, or destructive-mutation authority from implementation success.

Stop conditions: Stop when the scoped change is implemented and qualified, when evidence invalidates the requested responsibility, or when a reserved owner/authority decision is required.
```

### Must not infer

A bounded implementation request does not authorize unrelated cleanup, speculative refactoring, backlog work, or product-thesis changes.

## 3. Pattern: repository diagnosis

### When to use

Use when the user wants understanding before modification, or when repository-wide evidence may change the apparent problem.

### Ready-to-copy prompt

```text
Goal: Diagnose the repository sufficiently to identify the consequential boundary, current evidence, and the nearest decision-changing uncertainty.

Operating policy: Use Sensemaking and repo-sensemaker when repository-wide diagnosis is warranted. Verify current state rather than treating plans, trackers, or historical documentation as current truth.

Scope discipline: Diagnose; do not convert findings into implementation work unless separate authority explicitly grants that responsibility.

Authority discipline: Findings and recommendations are not authorization to modify the repository.

Stop conditions: Stop when the diagnosis is sufficient for the next consequential decision, when the repository cannot answer an owner-intent question, or when the authorized evidence surface is exhausted.
```

### Must not infer

`finding != authorization to fix`.

## 4. Pattern: next warranted improvement

### When to use

Use when the user wants the coding agent to determine what should change next rather than supplying the next feature/task directly.

### Ready-to-copy prompt

```text
Goal: Determine and complete the next warranted repository-level improvement that materially advances the current authoritative product mission.

Operating policy: Reconstruct current product/repository state, identify the nearest decision-changing uncertainty, and select one responsibility before selecting a Skill, workflow, tool, or patch. Use repo-sensemaker when repository-wide evidence could materially change that responsibility.

Scope discipline: Treat candidate directions, backlog items, TODOs, and historical plans as evidence or idea memory, not automatic work. Select work only when current evidence and product authority warrant it.

Authority discipline: Exercise delegated engineering judgment within granted authority. Escalate product-thesis/owner-intent decisions and reserved external actions.

Stop conditions: Stop after the selected bounded responsibility is qualified and repository state is reassessed; also stop if no change is warranted or a reserved decision/blocker is reached.
```

### Must not infer

The existence of more possible improvements does not mean another improvement is warranted now.

## 5. Pattern: complete authoritative product scope

### When to use

Use for a terminal repository-building mission where the user wants the agent to continue across multiple bounded responsibilities until the **currently authoritative required product scope** is satisfied.

Prefer **authoritative product scope** over vague phrases such as “all features” or “everything in the repository.” Product strategy may define purpose/user/JTBD while PRDs, capability contracts, accepted product/design decisions, and acceptance criteria define required realization.

### Ready-to-copy prompt

```text
Goal: Build this repository until every feature and capability explicitly required by the current authoritative product scope is implemented and satisfies its applicable acceptance and repository-qualification criteria.

Operating policy: Use Sensemaking to determine the warranted repository responsibility at each step. Reconstruct current repository reality before assuming documented work is still missing. Resolve decision-changing uncertainty before implementation. Use repo-sensemaker when repository-wide diagnosis could materially change the next responsibility. Use durable Campaign state when continuation complexity makes transient context unreliable. After each bounded responsibility, reconcile the resulting capability state and reassess what, if anything, is warranted next.

Scope discipline: Treat only current authoritative product commitments as requirements. Do not convert backlog items, candidate directions, speculative improvements, historical plans, stale issues, or optional future capabilities into required work unless an authoritative product/repository decision has promoted them.

Authority discipline: Desired delegation does not expand granted authority. Do not silently revise product-thesis commitments, perform reserved external actions, merge, release, deploy, publish, or make destructive changes unless those actions are authorized.

Stop conditions: Stop when all authoritative requirements are satisfied or legitimately dispositioned and no unresolved decision-changing gap prevents claiming scope completion; when no further repository change is warranted; when progress requires a reserved owner/product-thesis decision; or when an external blocker prevents further authorized work.
```

### What the agent should infer

The mission may legitimately traverse different repository-level responsibility classes over time:

```text
product-definition clarification
-> product/design reconciliation
-> domain-model or architecture reconciliation
-> bounded capability/feature implementation
-> documentation/integrity repair
-> qualification
-> Level-3 reassessment
```

That sequence is illustrative, not mandatory. Responsibility selection remains evidence-driven.

### Must not infer

- every open issue is required scope;
- every candidate direction is a missing feature;
- every documented TODO is current;
- one giant Campaign should represent the entire repository mission;
- “continue autonomously” grants product-thesis, merge, release, deployment, publication, or destructive authority;
- repository qualification proves broader product value or external/native-harness usefulness.

For long missions, the terminal product goal belongs conceptually above individual bounded Level-2 responsibilities. Campaign may preserve one continuation-heavy responsibility; it is not automatically the whole Level-3 repository-evolution mission.

## 6. Pattern: repair to verified closure

### When to use

Use when one or more prior findings are established and the user wants repair rather than general improvement.

### Ready-to-copy prompt

```text
Goal: Repair the established findings within scope and verify finding-specific closure against fresh repository evidence.

Operating policy: Preserve each original finding and its evidence. Select the smallest warranted repair responsibility, implement it, run applicable mechanical qualification, reconcile material work claims, and use repair verification against the original diagnosis.

Scope discipline: Do not broaden from the scoped findings into unrelated improvements merely because nearby opportunities are visible.

Authority discipline: Repair authority does not imply merge/release/publication authority and does not authorize changing the original product/architecture contract merely to make the finding disappear.

Stop conditions: Stop when every scoped finding is closed or explicitly remains with a legitimate disposition, when evidence shows the original diagnosis was wrong/superseded, or when further repair requires reserved authority.
```

### Must not infer

`green CI != original-finding closure`.

## 7. Pattern: architecture / design reconciliation

### When to use

Use when product behavior, architecture authority, implementation, and/or documentation appear inconsistent and the user wants the correct boundary restored rather than a predetermined refactor.

### Ready-to-copy prompt

```text
Goal: Reconcile the relevant product/design/architecture/implementation boundary so the repository has one current, evidence-supported interpretation of the intended responsibility.

Operating policy: Establish which authority is current before editing. Distinguish stale documentation from implementation drift and both from unresolved product intent. Use repo-sensemaker or architectural/product analysis when that evidence could change the responsibility.

Scope discipline: Repair the demonstrated boundary; do not rewrite higher-level product commitments to justify accidental implementation state and do not refactor architecture merely because a different design is aesthetically preferable.

Authority discipline: Escalate owner-intent or Level-4 product-thesis questions instead of silently resolving them in code.

Stop conditions: Stop when the relevant authority and realization agree and the original contradiction is verified closed, when no change is warranted, or when the remaining disagreement is owner-reserved.
```

### Must not infer

Observed dependency structure alone does not establish intended architecture.

## 8. Pattern: long-running delegated development

### When to use

Use when the goal is broader than one bounded responsibility and repository-specific decision state must survive contexts, agents, machines, or handoffs.

### Ready-to-copy prompt

```text
Goal: Continue progressing toward the stated repository mission across bounded responsibilities while preserving enough durable state for a fresh agent to reconstruct the current decision context.

Operating policy: Apply Sensemaking recursively. Keep the current responsibility bounded, preserve decision-changing evidence/authority/provenance when continuation complexity warrants it, and reassess the higher-level mission after each qualified result.

Scope discipline: Durable continuation is not permission to keep generating work. Preserve deferred/rejected/superseded directions without converting them into TODOs.

Authority discipline: Carry authority boundaries forward explicitly; continuation across contexts does not broaden them.

Stop conditions: Stop when the mission's authoritative terminal condition is satisfied, no further responsibility is warranted, continuation is blocked by reserved authority/external dependency, or the current durable state is insufficient and requires owner clarification rather than inference.
```

### Must not infer

Campaign longevity is not evidence that the Campaign should continue.

## 9. Prompt anti-patterns

These anti-patterns concern **goal formulation**. For process/adaptive-rigor anti-patterns, also read [`adaptive-guidance-v0.md`](adaptive-guidance-v0.md).

### “Build everything in the repo.”

Why it fails: “everything” has no authority boundary. Backlog ideas, old plans, TODOs, experiments, and optional capabilities can become accidental requirements.

Better: name the authoritative product scope and terminal qualification condition.

### “Keep improving until nothing can be improved.”

Why it fails: there is always another conceivable improvement. The goal has no stable stopping condition and encourages manufactured work.

Better: stop after one warranted improvement and reassess, or define a finite authoritative desired state.

### “Implement every open issue.”

Why it fails:

```text
open issue
!= authoritative requirement
!= currently warranted responsibility
!= implementation authorization
```

Better: use issues as evidence/work vehicles only after current product/repository authority warrants them.

### “Use every Sensemaking Skill to finish the project.”

Why it fails: it reverses the control law.

```text
wrong: available capability -> manufacture responsibility
right: warranted responsibility -> select capability if useful
```

### “Do not stop until the repository is perfect.”

Why it fails: “perfect” is not mechanically or semantically finite enough to govern closure.

Better: state accepted scope plus observable qualification/closure conditions.

### “Make every decision yourself and never ask me anything.”

Why it fails: desired delegation does not create owner intent or reserved authority.

Better: delegate repository-answerable engineering judgment while explicitly preserving owner/product-thesis and external-action boundaries.

### “All tests pass, therefore stop.”

Why it fails: tests may establish mechanical qualification without establishing that all authoritative requirements are satisfied, material work claims are reconciled, or prior findings are actually closed.

Better: treat qualification as evidence inside the terminal-condition decision.

## 10. Choosing a pattern

Use the narrowest pattern that matches the user's real goal:

```text
responsibility already established
-> bounded implementation

need understanding before modification
-> repository diagnosis

want one best next improvement
-> next warranted improvement

want to realize a finite authoritative product scope
-> complete authoritative product scope

known findings must be closed
-> repair to verified closure

intent/design/architecture/implementation disagree
-> architecture / design reconciliation

work must span fresh contexts
-> long-running delegated development
```

Patterns can be combined when the combination represents a real goal. Do not concatenate every clause by default.

A good delegation contract leaves the agent enough freedom to select warranted intermediate responsibilities while keeping four boundaries explicit:

```text
authoritative desired state
+ evidence-driven responsibility selection
+ granted authority
+ legitimate terminal conditions
```
