# Adaptive Semantic Control Architecture v0

**Status:** canonical descriptive crosswalk over already-integrated control surfaces  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, the Four-Level Control Model, Policy Hierarchy v0, and existing authority contracts  
**Construction authority:** Issue #426  
**Runtime status:** descriptive composition model; not a control level, runtime, router, planner, scheduler, state store, or authority surface

## 1. Purpose

Sensemaking now has several mature but intentionally distinct control surfaces: the
Four-Level Control Model, Policy Hierarchy v0, Strategic Repository Sensemaking v1,
Campaign/responsibility/authority semantics, execution/evidence interfaces, Strategic
Continuity v1, and Learning / Reconciliation.

This document explains how those surfaces compose without renaming, replacing, or
promoting any of them.

```text
Adaptive Semantic Control Architecture
= descriptive composition model

Policy Hierarchy v0
= canonical semantic-policy architecture inside that model

Adaptive Semantic Control Architecture
!= Policy Hierarchy v1
!= new control level
!= runtime
!= authority
```

## 2. Integrated control shape

```text
VALUE / PURPOSE
      |
      v
LEVEL 4 — PRODUCT THESIS / STRATEGY REVISION
      |
      v
LEVEL 3 — STRATEGIC REPOSITORY SENSEMAKING
      |
      +---------------- POLICY HIERARCHY ----------------+
      |                                                 |
      |  Inquiry                                        |
      |  Metareasoning                                  |
      |  Exploration                                    |
      |  Warrant / Choice                               |
      |                                                 |
      +-------------------------------------------------+
      |
      v
RESPONSIBILITY
      |
      v
AUTHORITY
      |
      v
CAMPAIGN / EXECUTION HANDOFF WHEN USEFUL
      |
      v
ACTION / EXECUTION
      |
      v
REALITY / EVIDENCE
      |
      v
LEARNING / RECONCILIATION
      |
      +--------------------+----------------------+
      |                    |                      |
      v                    v                      v
continue locally    change responsibility    reopen Level 3
                                                   |
                                                   v
                                          thesis review when
                                          Level-4 commitment
                                          is decision-changing
```

This diagram is a semantic ownership map, not a required call stack.

## 3. Cross-cutting envelopes and substrates

The following concerns constrain or support several nodes rather than becoming mandatory
vertical phases:

- Adaptive Policy Coordinator v0 — exposes only policy questions that can change the decision;
- Adaptive Guidance v0 — scales scaffolding, rigor, verification, and durability;
- authority — constrains knowing/deciding/acting/publishing transitions;
- consequence and reversibility — influence warrant and control effort;
- resources and opportunity cost — constrain reasoning/search effort;
- evidence, provenance, and currentness — preserve reconstructible support;
- Strategic Continuity v1 — preserves authored strategic lineage, assumptions, and reassessment triggers;
- durability / continuation complexity — determines whether state must survive contexts;
- Knowledge Externalization / Communication — persists useful decision-relevant knowledge when warranted.

```text
cross-cutting concern
!= mandatory workflow phase
```

## 4. Policy responsibility summary

The canonical responsibility matrix lives in `docs/policy-hierarchy-v0.md`. Its
governing distinctions are:

```text
Inquiry
-> what evidence would change the decision?

Metareasoning
-> what kind of effort deserves the next unit of resources?

Exploration
-> where should an already-iterative search go next?

Warrant / Choice
-> what target is sufficiently justified now?

Authority
-> may this actor perform the contemplated transition?

Action / Execution
-> how is the already-selected authorized work performed correctly?

Learning / Reconciliation
-> what explicit decision state changes after evidence returns?

Adaptive Policy Coordinator
-> which of those questions need to be explicit now?
```

Action / Execution is a control boundary in the canonical architecture. It is
deliberately **not** promoted into an `Action Policy v0`; responsibility selection,
warrant, authority, capability choice, and execution already have distinct owners.

## 5. Strategic reassessment bridge

Strategic Continuity v1 records decision assumptions and reassessment triggers.
Mechanical strategy projections can report currentness/drift. Neither one changes
strategy automatically.

```text
STRATEGIC ASSUMPTION
        |
        v
REASSESSMENT TRIGGER
        |
        v
NEW OBSERVATION / RESULT / DRIFT EVIDENCE
        |
        v
Is the evidence decision-changing?
        |
     +--+--+
     |     |
    no    yes
     |     |
     v     v
NO_MODEL_ STRATEGIC RECONCILIATION
CHANGE            |
                  v
        Learning / Reconciliation
                  |
       +----------+-----------+----------------+
       |                      |                |
       v                      v                v
    CONFIRM              REVISE / OPEN     REOPEN_STRATEGY
                          UNCERTAINTY             |
                                                v
                                  Strategic Repository Sensemaking
                                                |
                                                v
                                         Warrant / Choice
```

The following non-identities are mandatory:

```text
drift detected
!= strategy invalid

drift detected
!= semantic reassessment automatically required

reassessment trigger observed
!= strategic assumption falsified

assumption falsified
!= strategy automatically invalid

reconciliation produced
!= strategy automatically changed

REOPEN_STRATEGY
!= BUILD

THESIS_REVIEW_REQUIRED
!= thesis ratified
```

If returned evidence makes a Level-4 commitment decision-changing,
`THESIS_REVIEW_REQUIRED` carries the question through a `thesis_review_packet`; only
the separately authorized Level-4 process may ratify a thesis transition.

## 6. Semantic disposition versus durable artifact

Policy outcomes answer semantic questions. Companion artifacts preserve consequential
results across actors or contexts. They must not be confused.

| Semantic ownership | Durable companion when warranted | Boundary |
| --- | --- | --- |
| Learning / Reconciliation Policy | `strategic_reconciliation` | policy judgment != automatic state mutation |
| `OWNER_DECISION_REQUIRED` | `owner_decision_capsule` | packet != owner decision |
| `THESIS_REVIEW_REQUIRED` | `thesis_review_packet` | packet != Level-4 ratification |
| `EXTERNAL_EVIDENCE_REQUIRED` | `external_evidence_packet` | packet != timeless truth |
| Strategic Repository Sensemaking | `strategic_repository_analysis` | valid artifact != strategy correct |
| Strategic Continuity | continuity metadata on a later strategic analysis | lineage != semantic endorsement |

```text
policy disposition
!= durable companion artifact

durable artifact
!= authority transfer
```

## 7. Entry and re-entry

There is no universal start node. Work may enter from:

- a goal or owner direction;
- an observation, failure, or anomaly;
- a pre-existing decision;
- a returned execution result;
- a currentness/reconstruction concern;
- a reserved owner/Level-4/external evidence boundary.

Re-enter an earlier semantic layer only when new evidence actually reopens its question.

```text
repository changed
!= run the whole hierarchy

drift detected
!= run Strategic Repository Sensemaking

new evidence
!= reopen strategy
```

## 8. Normal-use evidence posture

This architecture should be exercised during ordinary consequential repository work.
Do not create a synthetic control episode merely to test whether another semantic layer
could exist.

When real work exposes recurring friction, preserve enough evidence to reconstruct:

- the decision being supported;
- which policy question became explicit and why;
- whether a zero-work outcome was valid;
- whether adjacent policy ownership was ambiguous;
- whether strategic continuity/reconciliation was reconstructible;
- whether authority stayed separate from warrant/selection;
- whether a fresh context could resume from durable evidence;
- the smallest concrete deficiency, if any.

One awkward episode is not sufficient to establish an architectural defect.

## 9. Explicit non-goals

This crosswalk does not authorize or introduce:

- Policy Hierarchy v1;
- `Action Policy v0`;
- a new control level;
- a policy router, planner, scheduler, state machine, or generic agent runtime;
- deterministic semantic policy activation;
- numeric inquiry, exploration, warrant, strategy, or intelligence scores;
- `AgentState`, `SearchState`, `BeliefState`, or a generic memory database;
- Campaign schema v3;
- automatic strategic reopening or construction-path selection;
- automatic repository discovery or scope expansion;
- automatic owner decisions or product-thesis revision;
- autonomous merge, release, deploy, publication, or other protected external authority;
- a synthetic StrategicPlanner experiment gate.

## 10. Governing rule

> **Use the smallest semantic composition that can materially improve the current
> decision, preserve its evidence and authority boundaries, and collapse the visible
> control structure when its decision value disappears.**
