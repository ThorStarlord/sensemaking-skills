# Strategic Repository Evolution State Contract

**Status:** canonical conceptual contract for Level-3 strategic state  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, and ratified architecture decisions  
**Current operational surface:** `STATUS.md`  
**Runtime status:** bounded repository-local v0 representation validator implemented by `scripts/validate-strategic-state.py`; no strategic-state schema or semantic strategy validator is implied

## 1. Purpose

This contract defines the minimum durable information needed for a fresh
maintainer or coding agent to reconstruct the **Strategic Repository Evolution
Loop** without depending materially on conversation history.

It answers:

> Given the current product strategy, where is repository/product evolution now,
> what consequential strategic decision is being supported, what boundary and
> responsibility were selected, why, and what outcome should cause strategic
> reassessment?

`STATUS.md` is the current Level-3 operational projection. This document defines
what that projection means; it does not require every concept below to become a
machine field.

## 2. Authority boundary

Level 3 may interpret repository/product evidence and select a warranted
repository-level responsibility within granted authority.

Level 3 does not own product-thesis commitments such as the primary user,
problem, JTBD, external product boundary, or major strategic non-goals. When
those commitments become decision-changing, Level 3 records thesis review as
required and escalates to Level 4.

Likewise:

```text
strategic state != product thesis
strategic frontier != backlog
active frontier != automatic authorization
qualitative comparison != deterministic ranking
strategic decision stated != implementation authorized
thesis tension != thesis review required
repository-qualified != product-value demonstrated
strategic-state contract valid != strategy correct
```

## 3. Required reconstruction questions

A valid Level-3 state surface should let a fresh reader answer:

1. What current product mission/strategy governs this repository?
2. What product/repository capabilities are currently established?
3. What material limitations or evidence ceilings remain?
4. What recent changes materially altered the capability state?
5. What unresolved boundaries currently form the Strategic Frontier?
6. What consequential **Strategic Decision to Support** is current, if any?
7. Which boundary is highest leverage for that decision, if one is selected?
8. Why was that boundary preferred to nearby credible alternatives?
9. What decision-changing uncertainty could make that selection wrong or premature?
10. What evidence could change the strategic decision?
11. What repository-level responsibility is currently warranted?
12. Why is the proposed intervention the smallest sufficient one?
13. What Campaign/work package/branch is executing it?
14. What evidence would establish completion or invalidate the rationale?
15. What authority is available and what authority is reserved?
16. Which directions are deferred, rejected, superseded, or outside scope?
17. Are there recurring thesis tensions whose recurrence could matter later?
18. Is Level-4 product-thesis review required now?
19. If review is active, which work depends on the challenged commitment?
20. What condition causes Level-3 reassessment or stopping?

If the answers require hidden conversation context, durable strategic state is
incomplete.

The validator does **not** mechanically answer these semantic reconstruction
questions. It checks only stable representation anchors.

## 4. Canonical Level-3 concepts

### 4.1 Product mission and strategy reference

Record the current Level-4 authority rather than duplicating its entire text.

```text
CURRENT PRODUCT STRATEGY
CURRENT PRODUCT PURPOSE / MISSION SUMMARY
CURRENT PRODUCT-BOUNDARY AUTHORITY
STRATEGY AUTHORITY / VERSION OR DATE
```

If Level 3 challenges that authority, record escalation rather than silently
rewriting the thesis.

### 4.2 Current product/repository capability state

Summarize capabilities that materially affect current repository evolution.
Preserve meaningful evidence ceilings such as `implemented`,
`repository-qualified`, `native-harness qualified`, `portable`, `ratified`, or
`integrated on main`; do not compress distinct qualification states into one
ambiguous word.

### 4.3 Material limitations and evidence ceilings

Record limitations that could change the next strategic decision. Do not turn
every known limitation into an active frontier item.

### 4.4 Strategic Frontier

The Strategic Frontier is the currently material set of unresolved
product/repository boundaries that could meaningfully change progress toward the
product mission.

Each material item should preserve:

```text
FRONTIER ID OR NAME
BOUNDARY / QUESTION
WHY IT MATTERS TO PRODUCT MISSION
DECISION IT COULD AFFECT
EVIDENCE BASIS
CURRENT DISPOSITION
EVIDENCE CEILING / UNKNOWN
REOPEN OR ESCALATION CONDITION, WHEN RELEVANT
```

Documentation-level dispositions may include `ACTIVE`, `CANDIDATE`, `DEFERRED`,
`REJECTED`, `NO_CHANGE_WARRANTED`, `SUPERSEDED`, `OWNER_DECISION_REQUIRED`, and
`THESIS_REVIEW_REQUIRED`. They are not Campaign runtime enums.

### 4.5 Strategic decision to support

Before selecting a boundary for active repository work, state the consequential
strategic decision that resolving it is meant to improve.

```text
STRATEGIC DECISION TO SUPPORT
MATERIAL ALTERNATIVES / OPTIONS, WHEN RELEVANT
WHAT CHANGES IF THE DECISION GOES ONE WAY VS ANOTHER
WHY THE DECISION MATTERS TO PRODUCT MISSION
```

This is agent/owner-authored semantic context, not a score or automatic field.
A frontier entry with no meaningful decision it can change is normally idea
memory or backlog rather than current strategic work.

### 4.6 Current highest-leverage boundary and comparison rationale

When Level 3 selects a focus, state one primary boundary and enough attributed
rationale to reconstruct why it is preferred now.

Qualitative lenses may include mission relevance, decision value, blocking
power, evidence sufficiency/resolvability, consequence of error, deferral cost,
reversibility, authority availability, dependency, and smallest warranted
intervention.

```text
qualitative comparison != deterministic ranking
agent judgment != unexplained intuition
```

If no boundary is warranted, say so.

### 4.7 Strategic decision-changing uncertainty

Record the unresolved question that could make the strategic decision, boundary,
or responsibility wrong or premature.

```text
UNCERTAINTY
DECISION AFFECTED
CHEAPEST SUFFICIENT EVIDENCE, IF KNOWN
WHAT WOULD CHANGE THE CURRENT DECISION / RESPONSIBILITY
```

### 4.8 Current warranted repository-level responsibility

Record the semantic responsibility rather than merely an implementation task.

```text
RESPONSIBILITY
STRATEGIC BOUNDARY SERVED
STRATEGIC DECISION SUPPORTED
WHY THIS RESPONSIBILITY IS WARRANTED
SCOPE
AUTHORITY
SMALLEST WARRANTED INTERVENTION
SUCCESS / CLOSURE CONDITIONS
```

### 4.9 Active execution vehicle

Name the Campaign, work package, branch, issue, or other bounded execution unit.
Distinguish selected responsibility from branch existence, PR state,
qualification, and merge state.

### 4.10 Expected evidence and reassessment condition

Record:

```text
EXPECTED EVIDENCE OF PROGRESS
REJECTION / INVALIDATION EVIDENCE
REASSESSMENT CONDITION
```

This prevents continuation merely because implementation can continue.

### 4.11 Authority and owner decisions

Record both available and reserved authority:

```text
AUTHORIZED NOW
OWNER-RATIFIED DECISIONS REQUIRED
EXTERNAL AUTHORITY REQUIRED
PROHIBITED / OUTSIDE PRODUCT BOUNDARY
```

### 4.12 Deferred, rejected, and superseded directions

Preserve consequential non-active directions only when forgetting them would
cause repeated/reopened work. The goal is durable decision memory, not backlog
accumulation.

### 4.13 Thesis tension

A **Thesis Tension** records a material but not-yet-decision-changing signal
about a Level-4 commitment when recurrence itself could matter later.

```text
AFFECTED STRATEGY COMMITMENT
OBSERVED INCIDENTS / EVIDENCE
CURRENT INTERPRETATION
WHY LEVEL-4 REVIEW IS NOT YET REQUIRED
WHAT RECURRENCE / EVIDENCE WOULD TRIGGER REVIEW
ATTRIBUTED AUTHOR
```

```text
thesis tension != thesis contradiction
thesis tension exists != thesis review required
repeated weak signals may become material evidence
```

Do not preserve every minor disagreement. Preserve only tensions whose loss
would weaken later strategy reconstruction.

### 4.14 Level-4 escalation and dependent-work state

When repository evolution exposes a decision-changing product-thesis question,
record:

```text
THESIS_REVIEW_REQUIRED
AFFECTED STRATEGY COMMITMENT
CURRENT COMMITMENT
EVIDENCE / CONTRADICTION
RELATED THESIS TENSIONS, WHEN MATERIAL
WHY LEVEL 3 CANNOT RESOLVE IT
AVAILABLE ALTERNATIVES
AUTHORITY REQUIRED
AFFECTED ACTIVE RESPONSIBILITIES / CAMPAIGNS
```

If review is required, classify active work by dependency on the challenged
commitment:

```text
THESIS_DEPENDENT
-> strategic advancement is held until Level-4 disposition + Level-3 reconciliation

UNAFFECTED
-> may continue if independently warranted and authorized
```

This is semantic agent judgment, not automatic dependency inference.

## 5. Strategic state lifecycle

```text
reconstruct strategy + repository state
-> identify frontier
-> state strategic decision to support
-> compare credible boundaries qualitatively
-> select or decline a boundary
-> identify decision-changing uncertainty / sufficient evidence
-> select one repository-level responsibility
-> choose smallest warranted intervention
-> delegate bounded execution
-> receive qualified result/evidence
-> reconcile capability state + strategic decision
-> preserve material thesis tension or escalate when needed
-> update frontier
-> reassess mission
```

Possible outcomes include `CONTINUE`, `NO_FURTHER_REPOSITORY_WORK_WARRANTED`,
`DEFER`, `REJECT`, `NO_CHANGE`, `OWNER_DECISION_REQUIRED`,
`THESIS_REVIEW_REQUIRED`, `EXTERNAL_BLOCKER`, and `STOP`. These are conceptual
outcomes, not runtime terminal-state additions.

## 6. Level-3 to Level-2 handoff

A handoff should preserve:

```text
STRATEGIC BOUNDARY
STRATEGIC DECISION TO SUPPORT
DECISION-CHANGING UNCERTAINTY
WHY THIS MATTERS TO PRODUCT MISSION
BOUNDED REPOSITORY RESPONSIBILITY
SMALLEST WARRANTED INTERVENTION
AUTHORITY
EXPECTED RESULT
EXPECTED EVIDENCE
INVALIDATION EVIDENCE
STOP CONDITIONS
```

Level 2 may narrow implementation details but must not silently substitute a
materially different strategic responsibility.

## 7. Currentness and Level-4 reconciliation

`STATUS.md` represents current Level-3 operational state. Historical roadmaps,
Campaign reports, handoffs, dated audits, ADRs, and research artifacts may
remain valuable evidence but must not compete silently for current direction.

```text
STATUS.md = current strategic projection
linked ADRs / handoffs / qualification records = durable historical evidence
```

After every material Level-4 disposition, Level 3 must reconcile before
thesis-dependent strategic work resumes. At minimum reconsider:

- Strategic Frontier;
- Strategic Decision to Support;
- highest-leverage boundary;
- active/deferred responsibilities;
- capability-state relevance;
- architecture assumptions tied to the reviewed commitment;
- open Campaigns whose mission depends on it;
- public documentation and claim ceilings.

For each materially affected item, record an attributed classification such as:

```text
STILL_RELEVANT
STALE
SUSPECT
CONTRADICTORY
SUPERSEDED
OWNER_DECISION_REQUIRED
```

Then explicitly continue, revise, close, supersede, defer, or seek authority.

```text
Level-4 disposition != automatic Level-3 work plan
Level-4 disposition -> Level-3 reassessment -> responsibility only if warranted
```

The validator does not query remote state or make these semantic classifications.

## 8. Bounded mechanical validator v0

Repository implementation:

```text
scripts/validate-strategic-state.py
```

It currently checks only required authority surfaces, required Markdown anchors,
canonical pointers, the single YES/NO thesis-review marker, and Strategic
Frontier identity uniqueness.

Current stable v0 anchors are:

```text
## Strategic Repository Evolution state — Level 3
### Current product strategy
### Current capability state
### Material limitations and evidence ceilings
### Strategic Frontier
### Current highest-leverage boundary
### Current decision-changing uncertainty
### Current warranted repository-level responsibility
### Authority / owner direction
### Thesis review state
## Current next step
```

Strategic Outer Loop Precision v1 makes `Strategic Decision to Support`
conceptually required. Whether it becomes an additional mechanical anchor is
reassessed only after semantic integration.

The validator always preserves:

```text
semantic_truth_established: false
```

It deliberately does not decide frontier leverage, strategic-decision value,
comparison quality, thesis-tension materiality, work dependency on a thesis,
strategy quality, architecture correctness, or responsibility warrant.

## 9. Implementation and evolution rule

Future checks may be added only when independently mechanically justified. Do
not add a strategic priority score, remote-currentness query, frontier router,
semantic decision judge, thesis-tension counter, automatic escalation detector,
or responsibility selector as an implementation shortcut.
