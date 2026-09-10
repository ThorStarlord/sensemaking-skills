# Sensemaking Semantic Architecture

**Status:** Canonical semantic foundation + Phase 10 Outcome A + build-first executable substrate candidate  
**Scope:** Repository reasoning, evidence semantics, work semantics, product-change vocabulary, bounded mechanical observations, cross-Skill provenance, conformance, and Campaign projections  
**Semantic authority:** The active agent/human owns interpretation and warrant; executable semantic machinery implements only documented mechanical subsets

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
| [`execution-integration.md`](execution-integration.md) | Semantic integration boundaries. |
| [`reference-scenarios.md`](reference-scenarios.md) | Concrete scenarios for model usefulness. |
| [`implementation-plan.md`](implementation-plan.md) | Current build-first phases and promotion gates. |
| [`build-first-policy.md`](build-first-policy.md) | Post-Phase-10 development strategy and Construction Diminishing-Returns Gate. |
| [`mechanical-semantic-substrate.md`](mechanical-semantic-substrate.md) | Executable probes, Repository Semantic Map v0, and cross-Skill state. |
| [`skill-contract-manifests-and-domain-packs.md`](skill-contract-manifests-and-domain-packs.md) | Machine-readable Skill/domain shells and conformance boundary. |
| [`pilots/README.md`](pilots/README.md) | Phase 9 Skill semantic-alignment evidence. |
| [`common-semantic-contract.md`](common-semantic-contract.md) | Level-3 `semantic_reasoning_profile` representation contract. |
| [`phase-9-handoff.md`](phase-9-handoff.md) | Qualified Phase 9 handoff. |
| [`phase-10/README.md`](phase-10/README.md) | Preregistered Phase 10 real-repository experiment. |
| [`phase-10/results.md`](phase-10/results.md) | Phase 10 evidence synthesis and Outcome A decision. |
| [`phase-10-handoff.md`](phase-10-handoff.md) | Qualified Phase 10 handoff and deferred-phase dispositions at that time. |
| [`milestone-handoff.md`](milestone-handoff.md) | Original semantic-foundation handoff. |

Campaign observability, Resume Capsule, replay/graph, semantic companion integration, and portable bundles are documented in [`../campaign-observability-and-portability.md`](../campaign-observability-and-portability.md).

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

Phase 9 produced the first new bounded example, `semantic_reasoning_profile` v1. Phase 10 retained that contract as an optional companion but rejected mandatory universal embedding. The post-Phase-10 build-first milestone adds additional Level-3 mechanics only where the boundary is directly mechanical: repository observations, target consistency, hash-chain integrity, manifest/domain conformance, Campaign provenance projections, and bundle integrity.

## Phase 9 — first Reasoning Model operationalization

The first contrasting pilots covered:

```text
repo-sensemaker
architectural-review
repair-verifier + output-reconciler
```

Across them, the stable common warrant/provenance core was:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
uncertainty
explicit limits / non-claims
```

Skill-local semantics such as fog/weakness taxonomies, `Component`/`Layer`/`Boundary`, architectural verdicts, repair `closed/remaining`, and reconciliation `verified/disputed/omitted` remain local rather than being flattened into one universal schema.

## Phase 10 — qualified Outcome A remains authoritative

Phase 10 tested the companion profile in three real-repository reasoning episodes:

```text
Chess Mentor Engine
    repo-sensemaker / direct diagnosis

React incremental game
    output-reconciler / immutable snapshot + live PR currentness

ViralFactory
    PM pre-mortem / canonical risk_analysis + companion profile
```

The qualified result is **Outcome A**:

> Keep `semantic_reasoning_profile` as an optional companion audit/reconstruction artifact.

The experiment found useful domain-neutral reconstruction value, especially where immutable snapshot evidence and mutable live metadata had to remain distinct, while also finding strong duplication pressure when domain artifacts already carried the relevant evidence/currentness/uncertainty/limits.

Accordingly, the profile remains selective and outside Campaign artifact admission. Phase 10 did not authorize a mandatory universal artifact envelope, Campaign schema promotion, a central reasoning engine, or automatic semantic routing.

The later owner decision to continue building does **not** erase this result. It changes the prospective development gate: additional experiments are deferred while mechanically clear construction runway remains.

## Build-first policy after Phase 10

The active decision rule is:

```text
Can the next architecture be justified primarily
from existing contracts + a known missing capability?

YES -> build and mechanically qualify
NO  -> invoke additional empirical validation
```

This is not a relaxation of verification. New executable behavior still requires negative cases, integrity boundaries, exact-head CI, and installed-product proof where relevant.

See `build-first-policy.md` for the Construction Diminishing-Returns Gate.

## Current executable semantic substrate candidate

### Mechanical observations

Current v0 probes cover:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every observation preserves target ref, evidence refs, method, scope, completeness, and currentness.

The probes establish only their declared mechanical facts. For example, an import statement does not establish an architecture violation, and zero exact matches in a bounded UTF-8 scope do not establish universal absence.

### Repository Semantic Map v0

A bounded map combines supplied mechanical observations into `repository_locator` entities and `DERIVED` relations. It rejects mixed target refs and states explicitly that absence from the map does not establish repository absence.

It does not infer `Component`, `Layer`, `Boundary`, architectural correctness, importance, or a recommended change.

### Cross-Skill semantic companion

An optional append-only SHA-256 hash chain preserves explicit artifact/evidence/claim/uncertainty references between Skills. It stores provenance references rather than hidden chain of thought.

Campaigns can carry this companion as `semantic-state.jsonl` without changing Campaign schema v2. Repository-bound Campaigns bind new companion entries to the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

### Skill/domain conformance

`skill-manifests/` describes deterministic Skill interfaces. `domain-packs/` groups existing Engineering and Product Management contracts. Conformance validates shape and cross-reference consistency while explicitly rejecting fields that imply deterministic semantic routing or truth authority.

### Campaign observability and portability

Campaign CLI projections now include:

```text
inspect
explain
diff
semantic-state-append
semantic-state
resume-context
replay
graph
bundle-export
bundle-verify
bundle-import
```

These commands inspect, connect, project, or transport durable state. They do not determine a warranted next action.

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
- explicitly documented Level-3 mechanical invariants.

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

## Domain Pack status

The build-first milestone extracts two **reference manifests**, not a plugin runtime:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

Engineering is deliberately represented by the first bounded semantic-alignment slice, not by a claim that every engineering Skill has been normalized. Product Management references the completed 27-Skill repository-qualified migration and its existing qualification policy.

Domain Pack membership does not change native-harness, portability, or promotion maturity.

## Construction Diminishing-Returns Gate

Additional empirical validation becomes required when construction can no longer resolve its own architecture questions. Signals include competing designs with no contract-based discriminator, abstraction without new capability, speculative durable fields, formalization outpacing consumption, maintenance dominating capability growth, persistent placement ambiguity, or pressure to transfer semantic judgment into deterministic machinery.

Completing the current build milestone does not automatically mean that gate has been reached.

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
- mandatory use of `semantic_reasoning_profile` in every domain artifact;
- claiming that Phases 11–16 were empirically validated by the historical Phase 10 episodes.

## Current frontier

The current candidate advances the Semantic Architecture through bounded mechanical substrate, map/state sharing, Campaign observability, conformance, reference Domain Packs, and portability ergonomics while preserving Campaign schema v2 and Phase 10 Outcome A.

After exact-head qualification, choose further construction only from a concrete remaining capability or integrity gap. If the next architecture instead depends on a behavioral value question, stop building and invoke the additional empirical-validation program defined by the diminishing-returns policy.
