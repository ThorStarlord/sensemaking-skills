# Problem Statement — Repository Reasoning Semantics

**Status:** Canonical problem definition  
**Initiative:** Sensemaking Semantic Architecture

## Problem

Sensemaking Skills contains increasingly mature machinery for Campaign state, evidence admission, responsibility, uncertainty, capability availability, authority, lineage, target snapshots, validation, reconciliation, and handoff. However, the semantic model used to reason **about the repository itself** remains distributed across Skill prompts, artifact contracts, documentation, validators, and agent interpretation.

As a result, different Skills can observe the same repository while carrying different implicit meanings for concepts such as:

- component;
- boundary;
- contract;
- dependency;
- capability;
- implementation;
- documentation authority;
- evidence;
- claim;
- contradiction;
- architectural drift;
- product change;
- successful repair.

This creates a risk of local semantic coherence but global inconsistency.

## Core failure mode

Without a shared semantic model, a Skill may produce a conclusion that is internally plausible yet incompatible with the assumptions of the next Skill.

Example:

```text
Skill A:
  "auth" is a component because it is a directory.

Skill B:
  "auth" is a capability implemented by three packages.

Skill C:
  "auth" is an API contract.

Workflow:
  treats all three uses as if they referred to the same entity.
```

The problem is not that one interpretation must always be wrong. The problem is that the system lacks explicit types and relations with which to state **which meaning is intended and what evidence supports it**.

## Why Campaign semantics alone are insufficient

The Campaign model already provides durable concepts such as `Responsibility`, `Uncertainty`, `Authority`, `ClaimEvidence`, `TargetSnapshot`, and `TransitionRecord`. These are strong control-plane concepts. They do not, by themselves, describe the semantic structure of an arbitrary target repository.

For example, Campaign state can persist:

```text
responsibility = architectural_review
```

but a repository reasoning model still needs to express questions such as:

```text
Which architectural boundary is under review?
Which components participate in it?
Which dependencies cross it?
Which contract defines the intended relation?
Which evidence establishes the observed relation?
Which part is observed versus inferred versus ratified?
```

Therefore the missing layer is not another workflow engine. It is a **shared repository-reasoning semantic layer**.

## Desired outcome

Sensemaking should have a stable language for constructing evidence-grounded models of unfamiliar repositories while preserving uncertainty and provenance.

The desired chain is:

```text
repository state
    -> observation
    -> evidence
    -> typed entity / relation
    -> claim
    -> epistemic status
    -> uncertainty / contradiction
    -> responsibility
    -> bounded capability
    -> result
    -> agent-authored decision
```

A fresh agent should be able to understand not only *what conclusion was reached*, but also:

- what entity the conclusion refers to;
- what relation is being asserted;
- what source supports it;
- how current that source is;
- whether the relation was observed, deterministically derived, agent-inferred, hypothesized, or human-ratified;
- what would falsify or weaken the conclusion;
- what uncertainty remains decision-changing.

## Scope

This initiative defines:

1. a canonical vocabulary;
2. a layered ontology;
3. relation semantics;
4. an epistemic model;
5. competency questions;
6. a reasoning model;
7. integration boundaries with existing Sensemaking machinery;
8. reference scenarios;
9. promotion rules for future executable contracts.

## Explicit non-goals

The initiative does not attempt to:

- enumerate every programming-language construct;
- parse every repository into a complete graph;
- make architecture decisions mechanically;
- rank Skills automatically;
- infer owner intent from code and treat it as canonical;
- assign numerical truth probabilities to claims;
- replace source evidence with a generated model;
- require every Campaign to instantiate every ontology concept;
- rewrite existing Campaign schema merely to mirror the ontology.

## Success criteria

The semantic architecture is useful when it lets multiple Skills answer the same repository question using compatible concepts and explicit evidence boundaries.

It should enable statements such as:

```text
Observed:
  module A imports module B at target snapshot S.

Agent inference:
  A and B appear to belong to distinct architectural layers.

Ratified intent:
  ADR X states that those layers must not depend in this direction.

Derived contradiction:
  observed dependency conflicts with ratified architectural intent.

Uncertainty:
  whether the import is transitional compatibility code or an unintended boundary violation.
```

That is materially stronger than a single unqualified sentence such as:

```text
The architecture is wrong.
```

## Primary design question

The initiative is governed by one question:

> What minimal-but-sufficient semantic model must an agent possess to reason reliably about an unfamiliar repository, preserve the provenance of that reasoning, and know the limits of what it has established?

Every ontology addition should be justified as part of answering that question.