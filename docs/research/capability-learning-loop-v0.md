# Capability Learning Loop v0

**Status:** evidence-gated research / architecture clarification  
**Date:** 2026-10-03  
**Authority:** non-authoritative cross-episode learning model; existing product strategy, ADR 0029, Policy Hierarchy, Skill contracts, and protected-transition authority remain controlling  
**Runtime status:** no learning runtime, no self-modifying agent, no model training, no new state/schema

## 1. Purpose

Sensemaking already supports durable learning inside and across repository work:

- returned evidence is interpreted through Learning / Reconciliation;
- consequential claims, uncertainties, responsibilities, and strategic state can
  be revised;
- Campaign, handoff/resume, provenance, ADR, STATUS, strategic analysis, and
  reconciliation surfaces preserve selected knowledge across contexts;
- Strategic Continuity preserves lineage between authored strategic states.

This document names the higher-order relationship among those existing surfaces
and distinguishes it from a possible future capability-learning loop across
multiple normal-use episodes.

The important distinction is:

```text
documentation
!= mandatory terminal phase

knowledge externalization
= cross-cutting selection of what should survive for another actor/context

repository learning
!= model-weight training

cross-episode lesson
!= reusable doctrine automatically
```

## 2. Three learning loops

### Loop A — responsibility learning

This is already canonical.

```text
bounded action / inquiry
-> returned result
-> evidence grounding
-> Learning / Reconciliation
-> claim / uncertainty / responsibility update
-> continue / change / stop / escalate
```

The loop improves the current decision and responsibility.

### Loop B — repository learning

This is already canonical when strategically consequential.

```text
repository state
-> strategic repository analysis
-> bounded responsibility / execution
-> changed repository + returned evidence
-> strategic reconciliation
-> reaffirm / revise / reopen / close
-> later strategic state
```

Strategic Continuity makes the relationship between authored states
reconstructible without mutating prior artifacts.

### Loop C — capability learning

This is an evidence-gated candidate extension, not a current autonomous runtime.

```text
multiple normal-use episodes
-> recurring material pattern
-> lesson candidate
-> cross-episode comparison
-> generalization warranted?
   -> no: retain episode/repository-local lesson
   -> yes: nominate bounded reusable guidance change
-> Skill / policy / reference / runbook change
-> independent repository qualification
-> later normal use
-> retain / revise / retire
```

Loop C asks whether experience from several repository episodes warrants a
change to reusable Sensemaking doctrine itself.

## 3. Why this is not a documentation phase

The General Agency Model v0.1 already establishes:

```text
Memory / Provenance
= persistent substrate

Knowledge Externalization / Communication
= cross-cutting capability

cross-cutting capability
!= mandatory final lifecycle node
```

Knowledge may need to be externalized:

- before execution, when an ADR or decision contract must constrain later work;
- during execution, when a handoff/fresh context must continue safely;
- after evidence returns, when reconciliation changes a consequential claim;
- after repeated normal use, when a candidate lesson may deserve reusable
  doctrine.

Trivial, reversible, low-consequence work need not manufacture durable
documentation.

```text
work happened
!= document everything

future reconstruction / transfer value is material
-> externalize the selected decision-relevant subset
```

## 4. Knowledge progression

The repository already supports several levels of explicit knowledge:

```text
OBSERVATION / EXECUTION RESULT
        |
        v
EVIDENCE + PROVENANCE / CURRENTNESS
        |
        v
CLAIM / UNCERTAINTY / RESPONSIBILITY INTERPRETATION
        |
        v
STRATEGIC RECONCILIATION / CONTINUITY WHEN MATERIAL
        |
        v
TRANSFERABLE INSTITUTIONAL KNOWLEDGE
ADRs / STATUS / Skills / references / runbooks / qualification records
```

Promotion upward is semantic and selective. Mechanical validity is never enough
by itself.

```text
artifact valid
!= lesson true

lesson observed once
!= pattern

pattern repeated
!= generalization warranted

generalization warranted
!= protected change authorized
```

## 5. Capability-learning evidence threshold

A cross-episode lesson becomes worth generalizing only when forgetting it would
create meaningful recurring cost or risk beyond one local episode.

Useful signals include:

- materially similar failure or confusion across heterogeneous repositories;
- repeated fresh-context reconstruction failure caused by the same missing
  guidance;
- recurring authority/evidence boundary mistakes;
- repeated premature convergence, over-investigation, or omitted verification
  traceable to the same reusable guidance gap;
- a pattern whose correction has already improved more than one episode without
  introducing a contradictory failure elsewhere.

One episode may produce a lesson candidate. It normally cannot establish a
general doctrine claim by itself.

Prefer heterogeneous corroboration when the claim is intended to generalize
across repository types.

## 6. Lesson candidate shape

No new artifact schema is introduced.

When cross-episode reasoning is warranted, use existing repository evidence,
normal-use records, issues/PRs, reconciliation artifacts, and explicit prose to
make at least these questions reconstructible:

```text
PATTERN
-> what recurring behavior/failure/success is claimed?

EPISODES
-> which concrete episodes support the claim?

INVARIANT
-> what appears common across those episodes?

CONTEXT LIMITS
-> where might the lesson not transfer?

COUNTEREVIDENCE
-> what episodes or evidence weaken the generalization?

PROPOSED DOCTRINE CHANGE
-> what smallest reusable guidance change would address it?

CLAIM CEILING
-> what would the available evidence actually establish?

QUALIFICATION
-> what independent checks must pass before integration?

REVISIT / RETIRE TRIGGER
-> what future evidence would revise or remove the doctrine?
```

This is a reasoning checklist, not a mandatory persisted object.

## 7. Allowed reusable targets

A warranted generalized lesson may nominate changes to existing surfaces such as:

- a Skill instruction;
- an existing semantic-policy reference;
- an architecture/reference document;
- operator guidance or runbook;
- a validation contract when the lesson is mechanically decidable;
- examples/anti-patterns that improve transferability.

The smallest intervention should win.

```text
guidance defect
-> guidance repair

mechanical invariant repeatedly violated
-> bounded deterministic assurance may be warranted

observed semantic pattern
!= new schema/runtime automatically
```

## 8. Qualification and promotion

Capability learning must preserve the repository's existing independent
verification discipline.

```text
normal-use observation
-> lesson candidate
-> bounded generalization
-> proposed reusable change
-> repository qualification on exact candidate
-> independent review/verification when consequential
-> integration under existing authority
-> later normal-use observation
-> reconciliation / revision / retirement
```

Qualification can establish that the reusable change is coherent and preserves
contracts. It does not prove universal semantic correctness or universal product
value.

## 9. Relationship to Learning / Reconciliation

Learning / Reconciliation remains the canonical semantic policy for interpreting
returned evidence in the current decision model.

Capability Learning Loop v0 does not add another policy layer.

```text
Learning / Reconciliation
= what changes in this explicit decision/repository model?

Capability Learning Loop v0
= when do repeated explicit lessons warrant a reusable doctrine candidate?
```

Loop C consumes already-explicit evidence and lessons. It must not reconstruct or
persist private chain-of-thought.

## 10. Relationship to Strategic Continuity

Strategic Continuity preserves authored repository-strategy lineage.

Capability learning may use several such histories as evidence, but it does not
collapse them into one universal repository strategy.

```text
multiple strategic histories
-> possible cross-episode evidence

possible cross-episode evidence
!= common causal explanation established
```

## 11. Relationship to normal-use observation

Normal use is the preferred source for capability-learning evidence because the
question is whether reusable guidance improves real repository decision work.

Synthetic examples may clarify a candidate rule, but stronger claims require
appropriate normal-use or external evidence.

The current autonomy evidence ceiling remains intact:

```text
one successful episode
!= general full-autonomy reliability

one repaired failure
!= universal doctrine

owner acceptance
!= empirical generalization
```

## 12. Explicit non-goals

Capability Learning Loop v0 does not authorize or introduce:

- model-weight training or fine-tuning;
- a universal `LearningEngine`;
- a generic belief/memory/vector database;
- automatic aggregation of all repository activity;
- automatic lesson extraction;
- automatic cross-repository causal inference;
- automatic Skill/policy/reference editing;
- automatic self-modification or self-deployment;
- automatic promotion of observed patterns into doctrine;
- a new Campaign or strategic artifact schema;
- a second Policy Hierarchy;
- a second strategic controller;
- merge/release/deploy/publication authority.

## 13. Current disposition

```text
CROSS_CONTEXT_LEARNING
= IMPLEMENTED / CANONICAL

REPOSITORY_STRATEGIC_LEARNING
= IMPLEMENTED / CANONICAL

KNOWLEDGE_EXTERNALIZATION
= IMPLEMENTED AS CROSS_CUTTING GUIDANCE

CROSS_EPISODE_CAPABILITY_LEARNING
= CONCEPTUALLY_SUPPORTED / CANDIDATE_EXTENSION

AUTOMATIC_SKILL_SELF_MODIFICATION
= NOT_AUTHORIZED

NEW_LEARNING_RUNTIME
= NOT_WARRANTED
```

This document does not reopen the current Level-3 construction frontier.

## 14. Reopen trigger

Promote capability learning from an explanatory/candidate model only when
normal-use evidence identifies a concrete recurring cross-episode deficiency
that cannot be absorbed by ordinary local reconciliation.

Examples:

1. the same guidance defect materially harms several independent repository
   episodes;
2. fresh agents repeatedly rediscover a lesson that existing durable surfaces
   fail to make transferable;
3. a recurring pattern justifies a bounded Skill/reference repair whose
   generality can be independently reviewed and qualified;
4. current evidence shows that an existing reusable doctrine should be revised or
   retired.

Until then, use existing durable artifacts and normal-use observation rather than
building a generic continual-learning runtime.

## 15. Governing rule

> **Externalize consequential learning when future actors need it; generalize
> across episodes only when evidence warrants the transfer; change reusable
> doctrine only through the repository's ordinary review, qualification, and
> authority boundaries.**
