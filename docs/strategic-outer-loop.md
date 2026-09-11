# Strategic Outer Loop and Four-Level Control Model

**Status:** canonical conceptual model for repository-development scope  
**Version:** v0  
**Construction state:** frozen operational baseline; reopen only from concrete repository/product pressure or explicit owner direction  
**Authority:** product strategy + ADRs 0013/0014; does not override executable contracts  
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

Outer Loop v0 is now a frozen operational baseline. "Frozen" means the current
architecture should be **used** during normal repository evolution rather than
extended merely because additional machinery can be imagined. It does not mean
the product can never change. Reopen this control architecture only when a new
concrete integrity/reconstruction burden, mechanically explicit product need,
or owner direction makes revision decision-changing.

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

Examples include editing code, adding tests, changing a validator, updating a
CLI, or revising documentation. Sensemaking should not build a replacement
coding runtime for this loop.

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

> Given the product mission and the current repository/product capability state,
> what consequential repository-level responsibility is warranted next?

Canonical shape:

```text
PRODUCT MISSION
      |
CURRENT PRODUCT / REPOSITORY STATE
      |
CURRENT CAPABILITY STATE + EVIDENCE CEILINGS
      |
identify material gaps / contradictions / opportunities
      |
STRATEGIC FRONTIER
      |
identify decision-changing strategic uncertainty
      |
select ONE warranted repository-level responsibility
      |
create or select a bounded Campaign / work package
      |
LEVEL 2 + LEVEL 1 execution
      |
qualified result + durable evidence
      |
update strategic state
      |
reassess mission / frontier
      |
continue / defer / owner decision / Level-4 escalation / stop
```

The Level-3 loop is recursive. It is not a phase-gated lifecycle and is not a
backlog processor.

### 5.1 Strategic Frontier

**Strategic Frontier** means:

> The currently material set of unresolved product/repository boundaries that
> could meaningfully change progress toward the product mission.

A frontier entry is not automatically work. Possible dispositions include:

```text
ACTIVE
DEFERRED
REJECTED
NO_CHANGE_WARRANTED
SUPERSEDED
OWNER_DECISION_REQUIRED
THESIS_REVIEW_REQUIRED
```

The repository may contain many useful defects or ideas that are not part of
the current strategic frontier.

```text
strategic frontier != backlog
search hit != frontier entry
frontier entry != authorization to implement
```

### 5.2 Repository-level responsibility classes

These are conceptual classes, not a new runtime enum:

- product-definition clarification;
- product discovery or research synthesis;
- product design;
- product strategy or prioritization;
- architecture reconciliation;
- domain-model refinement;
- capability development;
- feature change;
- implementation;
- integrity / hardening;
- simplification / removal;
- qualification;
- documentation reconciliation;
- migration.

Level 3 chooses the **kind of repository change that is warranted**, not merely
which file or issue to edit next.

### 5.3 Level-3 state authority

`STATUS.md` is the current operational projection of the Strategic Repository
Evolution Loop. Its detailed conceptual contract is defined in
[`strategic-state-contract.md`](strategic-state-contract.md).

It must distinguish at least:

```text
product mission / strategy reference
current capability state
material limitations and evidence ceilings
strategic frontier
current highest-leverage boundary
strategic decision-changing uncertainty
current warranted repository-level responsibility
active Campaign / work package
expected evidence
available / required authority
deferred, rejected, and superseded directions
reassessment / stopping state
```

This is initially a documentation contract, not a Campaign schema extension.

## 6. Level 4 — Product Thesis / Strategy Revision Loop

Level 4 answers:

> Is the current understanding of the product itself still the right strategic
> commitment?

It reasons over slower-changing commitments such as:

```text
product purpose
primary user
problem
job to be done
value proposition
product boundary
strategic principles
non-goals
success measures
strategic bets / assumptions
evidence ceilings
```

The canonical strategy authority remains
[`product-strategy.md`](product-strategy.md). Revision behavior is defined in
[`product-thesis-revision.md`](product-thesis-revision.md).

Canonical shape:

```text
CURRENT PRODUCT THESIS
      |
accumulated material evidence
      |
thesis-level contradiction or owner direction?
      |
   no ------------------------------> return to Level 3
      |
     yes
      |
identify affected strategic commitment
      |
formulate bounded alternatives
      |
reaffirm / reinterpret / revise / retire / supersede
      |
owner ratification where strategy authority is reserved
      |
new canonical strategy
      |
reconcile Level-3 state and frontier
```

Level 4 should activate less frequently than Level 3.

## 7. Level-3 to Level-4 escalation

Level 3 may identify a thesis-level problem, but it must not silently rewrite
product strategy.

A Level-4 escalation should preserve:

```text
THESIS_REVIEW_REQUIRED
AFFECTED_STRATEGY_COMMITMENT
EVIDENCE / CONTRADICTION
WHY LEVEL 3 CANNOT RESOLVE IT
AVAILABLE ALTERNATIVES
AUTHORITY REQUIRED
```

Examples that normally remain Level 3:

- add a JS/TS probe;
- repair a validator;
- change an artifact contract;
- improve architecture boundaries;
- add or remove a bounded capability.

Examples that may require Level 4:

- primary user is materially different from the ratified strategy;
- the problem/JTBD is invalidated;
- the value proposition no longer matches use;
- the external product boundary should materially expand or contract;
- a strategic non-goal should be reversed;
- the product should move to a materially different category.

## 8. Downward delegation contract

Level 4 delegates strategic commitments to Level 3.

Level 3 delegates one bounded repository-level responsibility to Level 2.

Level 2 delegates bounded actions to Level 1.

A useful Level-3-to-Level-2 handoff should include:

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

This structure does not authorize automatic Campaign creation or semantic
routing.

## 9. Cross-cutting requirements

Across all four levels preserve:

- provenance;
- currentness;
- attribution;
- authority;
- durability;
- evidence ceilings.

The four-level control model is also orthogonal to the existing four Semantic
Architecture implementation layers and to the Epistemic / Decision-Control /
Authority-Execution planes. Those models answer different questions.

## 10. Explicit non-goals

This model does not authorize:

- `OuterLoopEngine` or `StrategicPlanner` machinery;
- deterministic frontier ranking;
- automatic product-strategy revision;
- automatic feature prioritization;
- automatic Campaign generation from repository state;
- automatic Level-4 escalation classification where semantic judgment is
  required;
- a universal decision graph;
- central semantic routing;
- autonomous merge, release, or publication authority;
- a new Campaign schema merely to mirror this document.

The active agent owns semantic selection. Deterministic machinery may validate
only explicitly ratified, mechanically decidable representation contracts.

## 11. Construction sequence and authorization state

The construction sequence is intentionally **not** a standing roadmap:

```text
1. Canonical four-level control model                  [integrated]
2. Level-3 strategic-state contract                    [integrated]
3. Level-4 product-thesis revision contract            [integrated]
4. Strategic State Contract Validation v0              [integrated / repository-qualified]
5. Read-only strategy inspect/diff                     [not authorized]
6. Level-3 -> Campaign handoff mechanics               [not authorized]
7. Level-4 escalation/reconciliation mechanics         [not authorized]
```

Step 4 was authorized only after the fresh post-B7 reassessment found a concrete
mechanically decidable representation-integrity boundary and recorded it in
[`strategic-state-validation-design-preflight.md`](strategic-state-validation-design-preflight.md).
It was implemented as the repository-local `scripts/validate-strategic-state.py`
validator and integrated into Product Validation.

The post-step-4 Level-3 reassessment found no comparably concrete current
mechanical failure/reconstruction boundary for steps 5–7. They therefore remain
ideas, not pending work. Existing Markdown authority and agent-owned reasoning
remain sufficient at the current evidence boundary.

Reopen a later step only from new concrete product/integrity/reconstruction
pressure or explicit owner direction. Do not infer authorization from sequence
numbering or from the existence of this conceptual model.

## 12. v0 freeze and normal-use policy

Outer Loop v0 is complete as an architecture/operating contract and is now
**frozen as the default control baseline**.

Normal development should use the model to choose repository responsibilities;
it should not treat development of the model itself as the default frontier.

```text
use outer loop
-> inspect current strategy/repository state
-> select or decline one repository-level responsibility
-> perform bounded Level-2/Level-1 work
-> qualify
-> reconcile STATUS.md
-> reassess
```

The first repository-wide normal-use audit under this freeze is recorded in
[`strategic-repository-evolution-audit-2026-09-11.md`](strategic-repository-evolution-audit-2026-09-11.md).

Natural-use evidence may reopen outer-loop construction when repeated concrete
friction appears. Do not create a separate experimental evidence program merely
to keep the outer loop under construction.