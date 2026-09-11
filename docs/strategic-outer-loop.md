# Strategic Outer Loop and Four-Level Control Model

**Status:** canonical conceptual model for repository-development scope  
**Version:** v0  
**Reasoning precision:** Strategic Outer Loop Precision v1 clarification over the frozen v0 control architecture  
**Construction state:** frozen operational baseline; reasoning semantics may be clarified from concrete pressure or explicit owner direction  
**Authority:** product strategy + ADRs 0013/0029; does not override executable contracts  
**Scope:** how Sensemaking separates product-thesis, repository-evolution, bounded responsibility, and execution reasoning

## 1. Purpose

Sensemaking already has a strong bounded responsibility loop. This document
makes the two higher-scope loops explicit so a capable coding agent can reason
about repository evolution without turning product strategy, architecture, or
feature development into a fixed workflow.

The model has four reasoning scopes:

```text
LEVEL 4 — PRODUCT THESIS / STRATEGY REVISION LOOP
What product should this be, for whom, and why?
                    |
                    v
LEVEL 3 — STRATEGIC REPOSITORY EVOLUTION LOOP
What should change in the product/repository next?
                    |
                    v
LEVEL 2 — RESPONSIBILITY / CAMPAIGN LOOP
What bounded responsibility resolves the selected decision?
                    |
                    v
LEVEL 1 — EXECUTION LOOP
What concrete steps correctly perform the bounded work?
                    |
                    v
                 RESULT
                    |
             evidence moves upward
                    v
        higher levels reassess when warranted
```

These levels describe **scope of reasoning and durable state**, not four
runtime engines. The active coding agent remains the semantic controller.

Outer Loop v0 remains the frozen control-architecture baseline. Strategic Outer
Loop Precision v1 clarifies reasoning and transition semantics inside that
architecture; it does not add a control level or runtime engine.

## 2. Core control law

> Lower levels may execute decisions delegated from higher levels, but they may
> not silently redefine commitments owned by the higher level.

Therefore:

```text
Level 1 cannot silently redefine the selected responsibility.
Level 2 cannot silently redefine the strategic frontier.
Level 3 cannot silently redefine the product thesis.
Level 4 cannot manufacture action, merge, release, or publication authority.
```

Evidence and contradictions may flow upward. Authority does not.

## 3. Level 1 — Execution Loop

Level 1 answers:

> How do I perform this selected bounded action correctly?

Typical shape:

```text
inspect
-> edit / execute
-> test
-> diagnose
-> repair when warranted
-> verify
-> finish
```

Sensemaking should not build a replacement coding runtime for this loop.

## 4. Level 2 — Responsibility / Campaign Loop

Level 2 answers:

> What bounded responsibility is warranted to resolve this decision?

Canonical shape:

```text
task / decision
-> consequential uncertainty
-> bounded evidence
-> warranted responsibility
-> authority check
-> capability selection
-> bounded work
-> mechanical validation
-> durable result
-> advance / defer / owner decision / stop
```

Campaign State, Responsibility, Uncertainty, Capability, Authority, evidence,
transitions, artifacts, handoff, semantic companion state, and mechanical
qualification primarily support this level.

Level 2 may return evidence that invalidates the Level-3 rationale. It must
report that upward rather than silently widening the task.

## 5. Level 3 — Strategic Repository Evolution Loop

Level 3 answers:

> Given the product mission and current repository/product capability state,
> what consequential repository-level responsibility is warranted next, if any?

Canonical shape:

```text
PRODUCT MISSION / CURRENT LEVEL-4 STRATEGY
      |
CURRENT PRODUCT / REPOSITORY STATE
      |
CURRENT CAPABILITY STATE + EVIDENCE CEILINGS
      |
material observations / gaps / contradictions / opportunities
      |
CANDIDATE STRATEGIC BOUNDARIES / STRATEGIC FRONTIER
      |
identify the STRATEGIC DECISION TO SUPPORT
      |
qualitatively compare decision-relevant boundaries
      |
select ONE boundary — or explicitly decline selection
      |
identify DECISION-CHANGING STRATEGIC UNCERTAINTY
      |
identify cheapest sufficient evidence when needed
      |
select ONE WARRANTED REPOSITORY-LEVEL RESPONSIBILITY
      |
choose the SMALLEST WARRANTED INTERVENTION
      |
create/select bounded Campaign / work package when useful
      |
LEVEL 2 + LEVEL 1 execution
      |
qualified result + durable evidence
      |
strategic adjudication + state reconciliation
      |
continue / defer / reject / no change / owner decision /
Level-4 escalation / stop
```

The Level-3 loop is recursive. It is not a phase-gated lifecycle, a backlog
processor, or a deterministic priority function.

### 5.1 Strategic decision to support

Before treating a frontier boundary as current work, Level 3 should state:

> **What consequential strategic decision becomes better informed if this
> boundary is resolved?**

This **Strategic Decision to Support** is first-class reasoning context between
a candidate boundary and the uncertainty/responsibility that follows.

A useful record states:

```text
STRATEGIC DECISION TO SUPPORT
OPTIONS OR MATERIAL ALTERNATIVES, WHEN RELEVANT
WHAT CHANGES IF THE DECISION GOES ONE WAY VS ANOTHER
WHY THE DECISION MATTERS TO THE PRODUCT MISSION
```

```text
boundary observed != strategic decision selected
strategic decision stated != implementation authorized
```

### 5.2 Qualitative frontier comparison

When more than one credible boundary could support the current strategic
decision, compare them explicitly enough for a fresh reader to reconstruct the
judgment.

Use qualitative lenses, not scores:

1. mission relevance;
2. decision value;
3. blocking power;
4. evidence sufficiency / resolvability;
5. consequence of error;
6. deferral cost;
7. reversibility;
8. authority availability;
9. dependency;
10. smallest warranted intervention.

```text
qualitative comparison != deterministic ranking
agent judgment != unexplained intuition
high complexity != high strategic priority
high consequentiality != high strategic priority
```

If no candidate has sufficient warrant, decline selection rather than
manufacture a highest-leverage item.

### 5.3 Strategic Frontier

**Strategic Frontier** means the currently material set of unresolved
product/repository boundaries that could meaningfully change progress toward
the product mission.

A frontier entry is not automatically work. Possible dispositions include:

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

```text
strategic frontier != backlog
search hit != frontier entry
frontier entry != authorization to implement
```

Non-authoritative possibilities belong in
[`strategic-candidate-directions.md`](strategic-candidate-directions.md) as idea
memory only.

### 5.4 Repository-level responsibility classes

Conceptual classes include product-definition clarification, product discovery,
product design, strategy/prioritization, architecture reconciliation,
domain-model refinement, capability development, feature change,
implementation, hardening, simplification/removal, qualification,
documentation reconciliation, and migration.

Level 3 chooses the **kind of repository change that is warranted**, not merely
which file or issue to edit next.

### 5.5 Level-3 state authority

`STATUS.md` is the current operational projection of the Strategic Repository
Evolution Loop. Its detailed conceptual contract is defined in
[`strategic-state-contract.md`](strategic-state-contract.md).

It should distinguish:

```text
product mission / strategy reference
current capability state
material limitations and evidence ceilings
strategic frontier
current highest-leverage boundary, if selected
strategic decision to support
strategic decision-changing uncertainty
current warranted repository-level responsibility
active Campaign / work package
expected evidence + invalidation evidence
available / required authority
deferred, rejected, and superseded directions
thesis tension / thesis-review state when material
reassessment / stopping state
```

Mechanization is justified only for stable representation facts, not strategic
meaning.

## 6. Level 4 — Product Thesis / Strategy Revision Loop

Level 4 asks:

> Is the current understanding of the product itself still the right strategic
> commitment?

It reasons over slower-changing commitments such as product purpose, primary
user, problem, JTBD, value proposition, product boundary, strategic principles,
non-goals, success measures, bets/assumptions, and evidence ceilings.

The canonical strategy authority remains
[`product-strategy.md`](product-strategy.md). Revision behavior is defined in
[`product-thesis-revision.md`](product-thesis-revision.md), and the current
product boundary is ADR 0029.

Canonical shape:

```text
CURRENT PRODUCT THESIS
      |
accumulated material evidence / owner direction
      |
material thesis tension or contradiction?
      |
   no ---> preserve consequential recurring tension when useful
      |     -> return to Level 3
      |
     yes
      |
identify affected commitment
      |
formulate bounded alternatives
      |
reaffirm / reinterpret / revise / retire / supersede
      |
owner ratification where reserved
      |
new / reaffirmed canonical strategy
      |
mandatory Level-3 reconciliation
```

Level 4 should activate less frequently than Level 3.

### 6.1 Thesis tension

A **Thesis Tension** is a material but not-yet-decision-changing signal that a
Level-4 commitment may be generating repeated ambiguity or friction.

Preserve it only when recurrence itself could matter to a future strategy
decision. A useful record includes:

```text
AFFECTED STRATEGY COMMITMENT
OBSERVED INCIDENTS / EVIDENCE
CURRENT INTERPRETATION
WHY REVIEW IS NOT YET REQUIRED
WHAT RECURRENCE / EVIDENCE WOULD TRIGGER REVIEW
ATTRIBUTED AUTHOR
```

```text
thesis tension != thesis contradiction
thesis tension exists != thesis review required
repeated weak signals may become material evidence
```

It is semantic documentation state, not a score, runtime object, automatic
counter, or automatic escalation mechanism.

## 7. Level-3 ↔ Level-4 transition contract

Level 3 may identify a thesis-level problem, but it must not silently rewrite
product strategy.

A Level-4 escalation should preserve:

```text
THESIS_REVIEW_REQUIRED
AFFECTED_STRATEGY_COMMITMENT
CURRENT COMMITMENT
EVIDENCE / CONTRADICTION
RELATED THESIS TENSIONS, WHEN MATERIAL
WHY LEVEL 3 CANNOT RESOLVE IT
AVAILABLE ALTERNATIVES
RECOMMENDATION, IF ANY
AUTHORITY REQUIRED
DOWNSTREAM STATE LIKELY AFFECTED
```

### 7.1 Work behavior while review is unresolved

When thesis review is required, Level 3 identifies which active
responsibilities/Campaigns depend materially on the challenged commitment.

```text
THESIS REVIEW REQUIRED
        |
identify dependency on affected commitment
        |
        +-- thesis-dependent strategic advancement
        |      -> HOLD until Level-4 disposition + Level-3 reconciliation
        |
        +-- independently warranted bounded work
               -> may continue if unaffected and authorized
```

This is a dependency-sensitive hold, not a repository-wide freeze. Safe
mechanical maintenance or non-prejudicial evidence gathering may continue when
it does not assume the disputed thesis.

```text
review pending != all work forbidden
review pending != old thesis safe to assume
```

### 7.2 Mandatory post-review reconciliation

After any material Level-4 disposition, Level 3 reassesses before
thesis-dependent strategic work resumes.

For each materially affected responsibility/Campaign/direction, classify it as
appropriate:

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

Examples that normally remain Level 3 include bounded validators, artifact
contracts, architecture reconciliations, and capabilities. Examples that may
require Level 4 include a materially different primary user, invalidated
problem/JTBD, changed value proposition, major product-boundary expansion, or
reversal of a strategic non-goal.

## 8. Downward delegation contract

Level 4 delegates strategic commitments to Level 3. Level 3 delegates one
bounded repository-level responsibility to Level 2. Level 2 delegates bounded
actions to Level 1.

A useful Level-3-to-Level-2 handoff should include:

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

This does not authorize automatic Campaign creation or semantic routing.

## 9. Cross-cutting requirements

Across all four levels preserve provenance, currentness, attribution, authority,
durability, and evidence ceilings.

The four-level control model is orthogonal to the Semantic Architecture layers
and Epistemic / Decision-Control / Authority-Execution planes. Those models
answer different questions.

## 10. Explicit non-goals

This model does not authorize:

- `OuterLoopEngine` or `StrategicPlanner` machinery;
- deterministic frontier ranking or priority scoring;
- automatic product-strategy revision or escalation classification;
- automatic feature/responsibility/capability selection;
- automatic Campaign generation from repository state;
- a universal decision graph;
- central semantic routing;
- autonomous merge, release, or publication authority;
- a new Campaign schema merely to mirror this document.

The active agent owns semantic selection. Deterministic machinery may validate
only mechanically decidable representation contracts.

## 11. Construction sequence and authorization state

The historical construction sequence is **not** a standing roadmap:

```text
1. Canonical four-level control model                  [integrated]
2. Level-3 strategic-state contract                    [integrated]
3. Level-4 product-thesis revision contract            [integrated]
4. Strategic State Contract Validation v0              [integrated / repository-qualified]
5. Read-only strategy inspect/diff                     [integrated / repository-qualified]
6. Explicit Level-3 -> Campaign handoff mechanics      [integrated / repository-qualified]
7. Level-4 semantic reconciliation automation          [not authorized]
```

Product Boundary Reconciliation v1 superseded ADR 0014 with ADR 0029 without
adding strategy automation. Strategic Outer Loop Precision v1 clarifies
selection/review semantics without authorizing Step 7.

## 12. v0 freeze and normal-use policy

The four-level control architecture remains frozen as the default control
baseline. Precision v1 improves reconstructible strategic judgment and Level-4
transition behavior without changing control ownership.

```text
use outer loop
-> inspect current strategy/repository state
-> state the strategic decision to support
-> compare material boundaries qualitatively
-> select or decline one repository-level responsibility
-> perform bounded Level-2/Level-1 work
-> qualify
-> reconcile current Level-3 projection
-> escalate to Level 4 only when a thesis commitment is decision-changing
-> reassess / stop
```

Do not keep the Outer Loop under construction merely because more machinery can
be imagined.
