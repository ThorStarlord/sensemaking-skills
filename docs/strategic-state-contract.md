# Strategic Repository Evolution State Contract

**Status:** canonical conceptual contract for Level-3 strategic state  
**Authority:** subordinate to `docs/product-strategy.md` and ratified ADRs  
**Current operational surface:** `STATUS.md`  
**Runtime status:** documentation contract only; no new schema or validator is implied

## 1. Purpose

This contract defines the minimum durable information needed for a fresh
maintainer or coding agent to reconstruct the **Strategic Repository Evolution
Loop** without depending materially on conversation history.

It answers:

> Given the current product strategy, where is repository/product evolution now,
> what consequential boundary is active, why was it selected, and what outcome
> should cause strategic reassessment?

`STATUS.md` is the current Level-3 operational projection. This document defines
what that projection means; it does not require every concept below to become a
machine field.

## 2. Authority boundary

Level 3 may interpret repository/product evidence and select a warranted
repository-level responsibility within granted authority.

Level 3 does not own product-thesis commitments such as the primary user,
problem, JTBD, external product boundary, or major strategic non-goals. When
those commitments become decision-changing, Level 3 records
`THESIS_REVIEW_REQUIRED` and escalates to Level 4.

Likewise:

```text
strategic state != product thesis
strategic frontier != backlog
active frontier != automatic authorization
repository-qualified != product-value demonstrated
implementation complete != integrated main
```

## 3. Required reconstruction questions

A valid Level-3 state surface should let a fresh reader answer these questions:

1. What current product mission/strategy governs this repository?
2. What product/repository capabilities are currently established?
3. What material limitations or evidence ceilings remain?
4. What recent changes materially altered the capability state?
5. What unresolved boundaries currently form the Strategic Frontier?
6. Which boundary is currently highest leverage, if one has been selected?
7. What decision-changing uncertainty makes that boundary consequential?
8. What repository-level responsibility is currently warranted?
9. What Campaign, work package, or branch is executing that responsibility?
10. What evidence would establish completion or invalidate the rationale?
11. What authority is available and what authority is reserved?
12. Which directions are deferred, rejected, superseded, or outside scope?
13. Is Level-4 product-thesis review required?
14. What condition causes Level-3 reassessment or stopping?

If the answers require reconstructing hidden conversation context, the durable
strategic state is incomplete.

## 4. Canonical Level-3 sections

`STATUS.md` should preserve the following conceptual sections, though headings
may remain optimized for readability.

### 4.1 Product mission and strategy reference

Record the current Level-4 authority rather than duplicating its entire text.

Minimum content:

```text
CURRENT PRODUCT STRATEGY
CURRENT PRODUCT PURPOSE / MISSION SUMMARY
STRATEGY AUTHORITY / VERSION OR DATE
```

If Level 3 needs to challenge that authority, record an escalation; do not
silently rewrite the strategy summary into a new thesis.

### 4.2 Current product/repository capability state

Summarize capabilities that materially affect current repository evolution.

Prefer status statements with evidence ceilings such as:

```text
implemented
repository-qualified
native-harness qualified
portable
ratified
integrated on main
```

Avoid compressing distinct qualification states into one word such as
"complete" when stronger claims remain unestablished.

### 4.3 Material limitations and evidence ceilings

Record limitations that could change the next strategic decision.

Examples:

- implementation exists but is not integrated;
- repository qualification exists but native-harness evidence does not;
- architecture is documented but not mechanically enforced;
- a current capability cannot address a named repository class;
- authority for a consequential action is reserved.

Do not turn every known limitation into an active frontier item.

### 4.4 Strategic Frontier

The Strategic Frontier is the set of currently material unresolved boundaries
that could meaningfully change progress toward the product mission.

Each frontier item should preserve, in prose or a compact table:

```text
FRONTIER ID OR NAME
BOUNDARY / QUESTION
WHY IT MATTERS TO THE PRODUCT MISSION
EVIDENCE BASIS
CURRENT DISPOSITION
EVIDENCE CEILING / UNKNOWN
REOPEN OR ESCALATION CONDITION, WHEN RELEVANT
```

Recommended dispositions:

```text
ACTIVE
CANDIDATE
DEFERRED
REJECTED
NO_CHANGE_WARRANTED
SUPERSEDED
OWNER_DECISION_REQUIRED
THESIS_REVIEW_REQUIRED
```

These are documentation-level vocabulary in this contract. They are not new
Campaign enums.

### 4.5 Current highest-leverage boundary

When Level 3 has selected a current strategic focus, state exactly one primary
boundary and explain why it outranks nearby alternatives **as an attributed
agent judgment**.

This is not a deterministic priority score.

Record:

```text
CURRENT STRATEGIC BOUNDARY
WHY IT IS MATERIAL NOW
ALTERNATIVES CONSIDERED, WHEN CONSEQUENTIAL
ATTRIBUTED SELECTOR
```

If no single boundary is warranted, say so rather than manufacturing one.

### 4.6 Strategic decision-changing uncertainty

Record the unresolved question that could make the selected repository-level
responsibility wrong or premature.

```text
UNCERTAINTY
DECISION AFFECTED
CHEAPEST SUFFICIENT EVIDENCE, IF KNOWN
WHAT WOULD CHANGE THE CURRENT RESPONSIBILITY
```

The Level-3 uncertainty may be broader than a Level-2 Campaign uncertainty.
The latter should remain bounded to the delegated responsibility.

### 4.7 Current warranted repository-level responsibility

Record the semantic responsibility selected by the active agent, not merely the
implementation task.

Minimum shape:

```text
RESPONSIBILITY
STRATEGIC BOUNDARY SERVED
WHY THIS RESPONSIBILITY IS WARRANTED
SCOPE
AUTHORITY
SUCCESS / CLOSURE CONDITIONS
```

Possible responsibility classes include product-definition clarification,
product design, architecture reconciliation, capability development,
hardening, simplification/removal, qualification, migration, and ordinary
implementation. These classes remain conceptual unless a later contract
explicitly promotes them.

### 4.8 Active execution vehicle

Name the bounded Campaign, work package, branch, issue, or other execution unit
that currently owns the delegated responsibility.

```text
ACTIVE CAMPAIGN / WORK PACKAGE
BASE / TARGET STATE WHEN RELEVANT
STATUS
```

A Level-3 state surface should distinguish:

```text
selected responsibility
!= branch exists
!= PR open
!= PR qualified
!= merged on main
```

### 4.9 Expected evidence and reassessment condition

Record what evidence would cause Level 3 to close, revise, or abandon the
current responsibility.

```text
EXPECTED EVIDENCE OF PROGRESS
REJECTION / INVALIDATION EVIDENCE
REASSESSMENT CONDITION
```

This prevents the outer loop from continuing merely because implementation can
continue.

### 4.10 Authority and owner decisions

Record both available and reserved authority.

Examples:

```text
AUTHORIZED NOW
OWNER-RATIFIED DECISIONS REQUIRED
EXTERNAL AUTHORITY REQUIRED
PROHIBITED / OUTSIDE PRODUCT BOUNDARY
```

Do not infer that broad Campaign authority automatically authorizes every
strategic change.

### 4.11 Deferred, rejected, and superseded directions

Preserve consequential non-active directions when their absence would cause a
fresh agent to reopen already-resolved work.

For each material item record:

```text
DIRECTION
DISPOSITION
WHY
REOPEN WHEN
NOT REOPENED BY, WHEN USEFUL
```

The goal is durable decision memory, not backlog accumulation.

### 4.12 Level-4 escalation state

When repository evolution exposes a product-thesis question, record:

```text
THESIS_REVIEW_REQUIRED
AFFECTED STRATEGY COMMITMENT
EVIDENCE / CONTRADICTION
WHY LEVEL 3 CANNOT RESOLVE IT
AVAILABLE ALTERNATIVES
AUTHORITY REQUIRED
```

The canonical Level-4 process is defined in
[`product-thesis-revision.md`](product-thesis-revision.md).

## 5. Strategic state lifecycle

The normal Level-3 lifecycle is:

```text
reconstruct strategy + repository state
-> identify frontier
-> select or decline a strategic boundary
-> select one repository-level responsibility
-> delegate bounded execution
-> receive qualified result/evidence
-> reconcile capability state
-> update frontier
-> reassess mission
```

Possible outcomes include:

```text
CONTINUE
NO_FURTHER_REPOSITORY_WORK_WARRANTED
DEFER
OWNER_DECISION_REQUIRED
THESIS_REVIEW_REQUIRED
EXTERNAL_BLOCKER
STOP
```

These labels describe conceptual outcomes, not new runtime terminal states.

## 6. Level-3 to Level-2 handoff

When a Strategic Frontier item becomes active work, the handoff into a bounded
Campaign or work package should preserve:

```text
STRATEGIC BOUNDARY
DECISION TO SUPPORT
DECISION-CHANGING UNCERTAINTY
WHY THIS MATTERS TO PRODUCT MISSION
BOUNDED REPOSITORY RESPONSIBILITY
AUTHORITY
EXPECTED RESULT
EXPECTED EVIDENCE
STOP CONDITIONS
```

Level 2 may narrow implementation details but should not silently substitute a
materially different strategic responsibility.

## 7. Currentness and reconciliation

`STATUS.md` represents current Level-3 operational state. Historical roadmaps,
campaign reports, and research artifacts may remain valuable evidence but must
not compete silently with this surface for current-direction authority.

When strategy changes at Level 4, Level 3 must reconcile:

- current frontier items;
- active and deferred responsibilities;
- architecture assumptions;
- capability-state claims;
- historical directions that now require supersession markers.

Semantic classifications such as "still relevant" or "contradictory" remain
agent-authored unless an explicit mechanical rule exists.

## 8. Mechanical future boundary

A future validator may check only mechanically decidable parts of this contract,
for example:

- required authority surfaces exist;
- referenced files/ADRs/Campaigns resolve;
- status metadata is structurally present;
- declared current strategy pointers are unique and non-broken;
- historical-in-place documents are not simultaneously declared current.

It must not decide:

```text
which frontier is highest leverage
whether strategy is good
whether a feature should exist
whether architecture is correct
whether evidence semantically warrants a responsibility
```

No such validator is authorized merely by this document.

## 9. Initial implementation rule

For the current construction tranche:

> Improve durable strategic reconstruction in existing Markdown authority
> surfaces first. Add new schema/runtime machinery only after a concrete
> mechanically decidable integrity need appears.
