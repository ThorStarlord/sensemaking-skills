# Sensemaking Semantic Architecture

**Status:** Canonical semantic-design foundation, v0  
**Scope:** Repository reasoning, evidence semantics, work semantics, and product-change vocabulary  
**Executable status:** Documentation only unless a concept is explicitly mapped to an existing executable contract

## Purpose

Sensemaking needs a shared semantic model so different Skills can reason about repositories with the same meanings for repository structure, evidence, claims, uncertainty, responsibility, capability, authority, change, and validation.

This directory defines that shared model without moving semantic control out of the active agent.

The central design problem is not to describe every software concept. It is to define the **minimal-but-sufficient semantic model needed to reason reliably about an unfamiliar repository, preserve the provenance of that reasoning, and state the limits of what has actually been established**.

## Canonical hierarchy

```text
Sensemaking Semantic Architecture
|
+-- Semantic Model
|   +-- Foundational concepts
|   +-- Repository ontology
|   +-- Software-architecture ontology
|   +-- Evidence and epistemic ontology
|   +-- Engineering-work ontology
|   +-- Product ontology
|       +-- Product-change taxonomy
|
+-- Reasoning Model
|   +-- observation -> evidence
|   +-- evidence -> claim
|   +-- claim -> uncertainty
|   +-- uncertainty -> responsibility
|   +-- responsibility -> capability
|   +-- result -> decision
|
+-- Execution Integration
    +-- probes
    +-- Skills
    +-- artifacts
    +-- validators
    +-- Campaigns
    +-- handoff
```

## Document map

| Document | Role |
|---|---|
| [`constitution.md`](constitution.md) | Permanent guardrails for semantic formalization. |
| [`problem-statement.md`](problem-statement.md) | Why a shared semantic architecture is needed and what failure modes it addresses. |
| [`competency-questions.md`](competency-questions.md) | Questions the semantic model must eventually support. These are the primary acceptance tests for ontology scope. |
| [`concept-inventory.md`](concept-inventory.md) | Existing repository vocabulary and its current sources of authority. |
| [`ontology.md`](ontology.md) | Layered ontology of intent, software systems, evidence, knowledge, work, and product concepts. |
| [`product-change-taxonomy.md`](product-change-taxonomy.md) | Descriptive taxonomy for how product changes differ and create value. |
| [`relations-and-epistemics.md`](relations-and-epistemics.md) | Relationship semantics, evidence requirements, epistemic status, and prohibited inference. |
| [`reasoning-model.md`](reasoning-model.md) | Evidence-governed reasoning lifecycle. |
| [`execution-integration.md`](execution-integration.md) | How the semantic model maps to probes, Skills, artifacts, validators, Campaigns, and harnesses. |
| [`reference-scenarios.md`](reference-scenarios.md) | Concrete scenarios used to test whether the model is useful. |
| [`implementation-plan.md`](implementation-plan.md) | Phased plan and promotion gates from vocabulary to ontology to executable contracts. |
| [`milestone-handoff.md`](milestone-handoff.md) | What this milestone establishes and what remains intentionally deferred. |

## Three levels of formalization

Sensemaking distinguishes three different levels. A concept MUST NOT silently cross levels.

### Level 1 — Vocabulary

Shared definitions for agents and humans.

Example: `reinforcing product change` is a useful phrase even if no runtime field represents it.

### Level 2 — Ontology

Explicit entities, relationships, constraints, and epistemic meaning.

Example: `ProductChange reinforces ProductCapability` is an ontology relation once repeated reasoning needs that distinction.

### Level 3 — Executable semantic contract

Schema fields, validators, deterministic probes, registries, or runtime invariants.

Example: a relation becomes executable only when machinery needs to store or mechanically verify it and the boundary is deterministic enough to encode safely.

Promotion is one-way only in the sense of authority: a Level 1 or Level 2 concept MUST NOT be treated as if Level 3 machinery enforces it.

## Authority boundary

The semantic architecture preserves the Campaign control boundary:

```text
Agent owns:
- semantic interpretation;
- consequential uncertainty selection;
- warranted responsibility selection;
- semantic capability selection;
- judgment about whether evidence justifies a conclusion.

Deterministic machinery owns:
- repository identity and mechanically observable state;
- structural validation;
- persistence and integrity;
- exact-byte provenance;
- declared capability metadata;
- authority metadata checks;
- reconstructible transition history.
```

Therefore:

```text
observation != interpretation
artifact valid != claim true
relation detected != architectural intent established
capability available != capability warranted
repository changed != repair succeeded
ontology term documented != runtime-enforced concept
```

## Ontology admission rule

A candidate concept should enter the shared ontology only when all of the following are true:

1. it answers at least one demonstrated competency question;
2. at least two meaningful reasoning situations need the distinction, unless the distinction protects a critical safety/authority boundary;
3. its meaning can be stated independently of one Skill implementation;
4. its relationship to evidence and authority is clear;
5. it does not duplicate an existing canonical concept under another name.

Executable promotion requires additional evidence described in [`implementation-plan.md`](implementation-plan.md).

## Non-goals

This initiative does **not** authorize:

- a universal ontology of all software engineering;
- a mandatory knowledge graph for every Campaign;
- automatic semantic routing;
- automatic architecture judgment;
- confidence scores treated as truth probabilities;
- ontology-driven autonomous mutation authority;
- replacing source evidence with a generated semantic map;
- encoding the entire ontology in YAML/JSON before real Skills demonstrate the need.

## Relationship to the Campaign

The Campaign remains the durable decision process. The semantic architecture supplies a shared language for what Campaign participants mean.

The intended relationship is:

```text
repository / external source
        |
        v
observations and evidence
        |
        v
shared semantic vocabulary
        |
        v
agent-authored claims and uncertainty
        |
        v
responsibility / capability / authority
        |
        v
Campaign decision and durable transition
```

The ontology does not replace Campaign evidence. It makes evidence-linked reasoning more consistent.