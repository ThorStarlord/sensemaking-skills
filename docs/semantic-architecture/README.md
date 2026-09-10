# Sensemaking Semantic Architecture

**Status:** Canonical semantic foundation + first executable build-first substrate  
**Scope:** Repository reasoning, evidence semantics, work semantics, product-change vocabulary, bounded mechanical observations, cross-Skill provenance, conformance, and Campaign projections  
**Executable status:** Existing Campaign contracts, experimental `semantic_reasoning_profile`, mechanical semantic probes/map/state/conformance, Campaign observability, and portable bundles; semantic judgment remains agent-owned

## Purpose

Sensemaking needs a shared semantic model so different Skills can reason about repositories with the same meanings for repository structure, evidence, claims, uncertainty, responsibility, capability, authority, change, and validation.

The central design problem is not to describe every software concept. It is to define the **minimal-but-sufficient semantic model needed to reason reliably about an unfamiliar repository, preserve the provenance of that reasoning, and state the limits of what has actually been established**.

## Canonical hierarchy

```text
Sensemaking Semantic Architecture
|
+-- Semantic Model
|   +-- foundational concepts
|   +-- repository / software architecture ontology
|   +-- evidence and epistemic ontology
|   +-- engineering-work ontology
|   +-- product ontology / product-change taxonomy
|
+-- Reasoning Model
|   +-- observation -> evidence
|   +-- evidence -> claim
|   +-- claim -> uncertainty
|   +-- uncertainty -> responsibility
|   +-- responsibility -> capability
|   +-- result -> validation -> decision
|
+-- Capability / Skill Layer
|   +-- bounded Skill methodology
|   +-- Skill Contract Manifests
|   +-- Domain Pack reference manifests
|
+-- Executable Substrate
    +-- mechanical probes
    +-- bounded Repository Semantic Map
    +-- cross-Skill semantic companion state
    +-- artifacts / validators / conformance
    +-- Campaign persistence / observability / portability
```

No lower layer automatically receives the semantic authority of an upper-layer concept.

## Document map

| Document | Role |
|---|---|
| [`constitution.md`](constitution.md) | Permanent guardrails for semantic formalization. |
| [`problem-statement.md`](problem-statement.md) | Why a shared semantic architecture is needed. |
| [`competency-questions.md`](competency-questions.md) | Acceptance questions governing ontology scope. |
| [`concept-inventory.md`](concept-inventory.md) | Existing repository vocabulary and sources of authority. |
| [`ontology.md`](ontology.md) | Layered Level-2 ontology. |
| [`product-change-taxonomy.md`](product-change-taxonomy.md) | Descriptive product-change taxonomy. |
| [`relations-and-epistemics.md`](relations-and-epistemics.md) | Relationship/evidence/epistemic semantics and prohibited inference. |
| [`reasoning-model.md`](reasoning-model.md) | Evidence-governed reasoning lifecycle. |
| [`execution-integration.md`](execution-integration.md) | Semantic model integration boundaries. |
| [`reference-scenarios.md`](reference-scenarios.md) | Concrete scenarios for model usefulness. |
| [`implementation-plan.md`](implementation-plan.md) | Current build-first phases and promotion gates. |
| [`build-first-policy.md`](build-first-policy.md) | Verification-vs-validation policy and Construction Diminishing-Returns Gate. |
| [`mechanical-semantic-substrate.md`](mechanical-semantic-substrate.md) | Executable probes, Repository Semantic Map v0, and cross-Skill state. |
| [`skill-contract-manifests-and-domain-packs.md`](skill-contract-manifests-and-domain-packs.md) | Machine-readable Skill/domain shells and conformance boundary. |
| [`pilots/README.md`](pilots/README.md) | Phase 9 Skill semantic-alignment evidence. |
| [`common-semantic-contract.md`](common-semantic-contract.md) | Experimental Level-3 `semantic_reasoning_profile`. |
| [`phase-9-handoff.md`](phase-9-handoff.md) | Qualified Phase 9 handoff. |
| [`milestone-handoff.md`](milestone-handoff.md) | Original semantic-foundation handoff. |

Campaign observability, Resume Capsule, replay/graph, and portable bundles are documented in [`../campaign-observability-and-portability.md`](../campaign-observability-and-portability.md).

## Three levels of formalization

### Level 1 — Vocabulary

Shared definitions for agents and humans.

### Level 2 — Ontology

Explicit entities, relationships, constraints, and epistemic meaning.

### Level 3 — Executable semantic contract

Schemas, validators, deterministic probes, manifests, persistence invariants, and other code that implement **only the mechanically decidable subset** of a semantic distinction.

Therefore:

```text
Level-2 relation documented
!=
Level-3 relation automatically derivable

Level-3 representation valid
!=
semantic conclusion true
```

Phase 9 produced `semantic_reasoning_profile` v1. The build-first milestone adds further Level-3 mechanics where the boundary is directly mechanical: repository observations, target consistency, hash-chain integrity, manifest/domain conformance, Campaign provenance projections, and bundle integrity.

## Build-first policy

The earlier common-envelope empirical study is deliberately parked while concrete construction runway remains.

This is **not** a relaxation of verification. Every executable addition still requires mechanical contracts, negative cases, exact-head CI, and packaging proof where relevant.

The decision rule is:

```text
Can the next architecture be justified primarily
from existing contracts + a known missing capability?

YES -> build and mechanically qualify
NO  -> invoke empirical validation
```

See `build-first-policy.md` for the full diminishing-returns gate.

## Current executable semantic substrate

### Mechanical observations

Current v0 probes cover:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every observation preserves target ref, evidence ref, method, scope, completeness, and currentness.

### Repository Semantic Map v0

A bounded map can combine supplied mechanical observations into `repository_locator` entities and `DERIVED` relations. It rejects mixed target refs and explicitly states that absence from the map does not establish repository absence.

It does not infer `Component`, `Layer`, `Boundary`, architecture correctness, or importance.

### Cross-Skill semantic companion

An optional append-only hash chain preserves explicit artifact/evidence/claim/uncertainty refs between Skills. It is provenance, not hidden reasoning.

Campaigns may keep this companion as `semantic-state.jsonl` in the workspace without changing Campaign schema v2.

### Skill/domain conformance

`skill-manifests/` describes deterministic Skill interfaces. `domain-packs/` groups existing engineering and Product Management contracts. Conformance validates shape and cross-reference consistency while prohibiting automatic semantic authority fields.

### Campaign observability / portability

Campaign commands can inspect/explain/diff/replay/graph durable provenance, emit a Resume Capsule, integrate the optional semantic companion, and export/verify/import exact-byte bundles.

These are projections and transport operations, not semantic recommendations.

## Authority boundary

The active agent/human continues to own:

- semantic interpretation;
- consequential uncertainty selection;
- warranted responsibility selection;
- semantic capability selection;
- judgment about whether evidence justifies a conclusion;
- judgment that a repair or architectural response succeeds semantically.

Deterministic machinery may own:

- repository identity and mechanically observable state;
- declared probe scope/completeness;
- structural representation validation;
- persistence and integrity;
- exact-byte provenance;
- manifest/domain cross-reference consistency;
- authority metadata checks;
- reconstructible transition history;
- bundle integrity and safe extraction;
- explicit Level-3 mechanical invariants.

Therefore:

```text
observation != interpretation
artifact valid != claim true
relation detected != architectural intent established
capability available != capability warranted
repository changed != repair succeeded
ontology term documented != runtime-enforced concept
semantic profile valid != reasoning semantically correct
semantic map relation != architecture judgment
manifest valid != Skill should run
bundle valid != Campaign semantically correct
provenance edge != semantic support
```

## Ontology / executable admission rule

A candidate concept enters shared ontology only when it answers demonstrated competency questions, has stable reusable meaning, has clear evidence/authority semantics, and does not duplicate canonical vocabulary.

Executable promotion additionally requires a mechanically expressible boundary, rejection coverage, compatible versioning, and a concrete product/integrity consumer. Empirical support claims remain separately evidence-gated.

## Non-goals

This initiative does **not** authorize:

- a universal ontology of all software engineering;
- a complete repository knowledge graph;
- automatic semantic routing;
- automatic architecture judgment;
- automatic uncertainty ranking;
- automatic Skill selection;
- confidence scores treated as truth probabilities;
- ontology-driven mutation authority;
- replacing source evidence with a generated semantic map;
- a central Reasoning Engine;
- claiming the parked common-envelope value experiment already passed.

## Current frontier

The build-first phases through Campaign observability/portability and reference Domain Packs now have an executable implementation candidate. The next construction step should be selected from a **concrete remaining product or integrity gap**, not from pressure to add ontology coverage.

The Construction Diminishing-Returns Gate remains active as a policy check. When the next architecture cannot be justified without answering behavioral value questions, execute the parked empirical program rather than continuing speculative formalization.
