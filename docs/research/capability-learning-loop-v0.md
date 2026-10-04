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

## 6A. Artifact production and ownership

Capability learning does not require every Skill to emit a second, generic
"learning artifact." Existing Skills and execution surfaces already produce the
episode evidence from which learning can be reconstructed.

| Responsibility | Existing producer/surface | Durable result when warranted |
| --- | --- | --- |
| repository diagnosis | `repo-sensemaker` | repository sensemaking brief |
| Level-3 strategic model | `strategic-repository-analysis` | `strategic_repository_analysis` |
| bounded execution | Campaign / executor / repository work | evidence, transitions, receipts, code/tests/PR history |
| current decision-model learning | Learning / Reconciliation in `using-sensemaking` | revised explicit claim/uncertainty/responsibility in the appropriate existing durable surface |
| Level-3 evidence return | `strategic-repository-reconciliation` | `strategic_reconciliation` |
| cross-context continuation | Campaign / handoff / resume surfaces | reconstruction context and provenance |
| promoted institutional doctrine | ordinary repository development | Skill/reference/ADR/runbook/validator change |

The active semantic controller decides whether a consequential lesson needs to
survive another context and places it in the narrowest existing durable surface
that owns that information.

```text
learning occurred
!= create a learning artifact automatically

episode result is trivial / locally reconstructible
-> no additional durable learning record

forgetting the lesson would cause rediscovery, contradiction, unsafe
continuation, repeated failed search, or lost rationale
-> preserve the lesson in the appropriate existing artifact
```

Do not add a universal `artifacts/capability_learning.md`,
`LEARNINGS.md`, or equivalent append-only knowledge dump.

## 6B. Artifact lifecycle

The learning architecture distinguishes three representations:

```text
EPISODE ARTIFACT
= what happened and what the current decision model learned

CAPABILITY-LEARNING CANDIDATE
= what several comparable episodes may jointly teach

PROMOTED DOCTRINE
= what future agents should actually use
```

The normal lifecycle is:

```text
episode evidence / Campaign / reconciliation / PR / qualification
        |
        | several episodes become materially comparable
        v
cross-episode synthesis
        |
        v
capability-learning candidate
        |
        v
generalization warranted?
     /        \
   no          yes
   |            |
   v            v
retain local/   identify smallest reusable target
historical      |
knowledge       v
            Skill / reference / runbook / validator change
                 |
                 v
            exact-candidate qualification
                 |
                 v
             later normal use
                 |
                 v
           retain / revise / retire
```

A candidate may be represented initially as a bounded research/normal-use
document, issue, PR rationale, or reconciliation note. No canonical candidate
artifact schema is required until repeated use demonstrates that a stable
machine-checked representation would create value.

```text
what happened
!= what several episodes jointly imply

cross-episode synthesis
!= doctrine

doctrine candidate
!= integrated capability

integrated capability
!= permanently correct
```

## 6C. Skill boundary

No new capability-learning Skill is warranted by this clarification alone.

Current ownership is:

```text
existing Skills / execution surfaces
-> produce episode evidence

Learning / Reconciliation
-> decide what consequential episode learning becomes durable

active semantic agent
-> perform cross-episode synthesis when explicitly warranted

future specialized Skill
-> candidate only
```

A future Skill, tentatively describable as
`capability-learning-analysis`, would own only this bounded responsibility:

> Given an explicitly selected set of normal-use/reconciliation artifacts,
> determine whether they support a reusable capability lesson and produce a
> bounded lesson candidate with context limits, counterevidence, claim ceiling,
> proposed reusable target, and qualification requirements.

It would not discover all repositories automatically, rewrite existing Skills,
promote doctrine, merge changes, or create protected authority.

Consider creating that Skill only when normal use shows all of the following:

1. cross-episode synthesis is repeatedly needed;
2. agents repeatedly perform substantially the same comparison structure;
3. omission of explicit guidance causes material generalization errors, missed
   counterevidence, or inflated claim ceilings;
4. the input/output responsibility is stable enough to describe independently
   of one repository;
5. a dedicated Skill would reduce repeated work without creating a second
   learning state system.

Until those conditions are established, cross-episode synthesis remains an
agent-owned reasoning responsibility using existing artifacts.

```text
possible reusable responsibility
!= Skill warranted now

repeated stable responsibility + demonstrated guidance value
-> reconsider dedicated Skill
```

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
