# Sensemaking Semantic Architecture

**Status:** Canonical semantic foundation; Phase 9 and Phase 10 complete; first bounded Phase 15 liveness rule qualified; post-Phase-10 build-first substrate implemented as a candidate  
**Scope:** Repository reasoning, evidence semantics, work/product semantics, bounded mechanical observations, cross-Skill provenance, conformance, and Campaign projections  
**Semantic authority:** The active agent/human owns interpretation and warrant; executable semantic machinery implements only documented mechanical subsets

## Purpose

Sensemaking needs a shared semantic model so different Skills can reason about repositories with the same meanings for repository structure, evidence, claims, uncertainty, responsibility, capability, authority, change, and validation.

The goal is not an ontology of every software concept. It is the **minimal-but-sufficient semantic architecture needed to reason reliably about an unfamiliar repository, preserve provenance, and state the limits of what has actually been established**.

## Canonical hierarchy

```text
Sensemaking Semantic Architecture
|
+-- Semantic Model
|   +-- foundational concepts
|   +-- repository / software-architecture ontology
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
    +-- artifacts / validators / conformance checks
    +-- Campaign persistence / observability / portability
```

No lower layer automatically receives semantic authority from an upper-layer concept.

## Document map

| Document | Role |
|---|---|
| [`constitution.md`](constitution.md) | Permanent semantic/evidence/authority guardrails. |
| [`problem-statement.md`](problem-statement.md) | Why a shared semantic architecture is needed. |
| [`competency-questions.md`](competency-questions.md) | Ontology acceptance questions. |
| [`concept-inventory.md`](concept-inventory.md) | Existing canonical vocabulary and authority sources. |
| [`ontology.md`](ontology.md) | Layered Level-2 ontology. |
| [`product-change-taxonomy.md`](product-change-taxonomy.md) | Product-change taxonomy. |
| [`relations-and-epistemics.md`](relations-and-epistemics.md) | Relationship/evidence/epistemic semantics. |
| [`reasoning-model.md`](reasoning-model.md) | Evidence-governed reasoning lifecycle. |
| [`execution-integration.md`](execution-integration.md) | Integration boundaries. |
| [`reference-scenarios.md`](reference-scenarios.md) | Reference competency scenarios. |
| [`implementation-plan.md`](implementation-plan.md) | Historical phases plus active build-first track. |
| [`build-first-policy.md`](build-first-policy.md) | Post-Phase-10 policy and diminishing-returns gate. |
| [`mechanical-semantic-substrate.md`](mechanical-semantic-substrate.md) | Probes, Repository Semantic Map v0, and cross-Skill state. |
| [`skill-contract-manifests-and-domain-packs.md`](skill-contract-manifests-and-domain-packs.md) | Skill/domain manifests and conformance. |
| [`pilots/README.md`](pilots/README.md) | Phase 9 pilot evidence. |
| [`common-semantic-contract.md`](common-semantic-contract.md) | `semantic_reasoning_profile` Level-3 contract. |
| [`phase-10/results.md`](phase-10/results.md) | Qualified Phase 10 evidence and Outcome A. |
| [`phase-10-handoff.md`](phase-10-handoff.md) | Phase 10 qualification handoff. |
| [`phase-15/README.md`](phase-15/README.md) | Qualified bounded Skill-registry liveness pilot. |
| [`phase-15-handoff.md`](phase-15-handoff.md) | Phase 15 liveness qualification evidence. |

Campaign observability, Resume Capsule, replay/graph, semantic companion integration, and portable bundles are documented in [`../campaign-observability-and-portability.md`](../campaign-observability-and-portability.md).

## Three levels of formalization

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract / bounded conformance rule
```

A Level-3 mechanism implements only a mechanically decidable subset.

```text
Level-2 relation documented != Level-3 relation automatically derivable
Level-3 representation valid != semantic conclusion true
```

Phase 9 produced `semantic_reasoning_profile` v1. Phase 10 retained it as an **optional companion** while rejecting mandatory universal embedding. The qualified Phase 15 liveness pilot added a narrow conformance rule over explicit Skill-registry/tree consistency.

The build-first candidate adds further Level-3 mechanics only where the boundary is mechanical: repository observations, target consistency, bounded map derivation, hash-chain integrity, manifest/domain cross-reference conformance, Campaign provenance projections, and bundle integrity.

## Phase 9 — Reasoning Model operationalization

The first contrasting pilots covered `repo-sensemaker`, `architectural-review`, and `repair-verifier` + `output-reconciler`.

Their stable warrant/provenance core was:

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

Skill-local semantics remain local rather than being flattened into a universal schema.

## Phase 10 — qualified Outcome A

Phase 10 tested the companion profile on Chess Mentor Engine, the React incremental game, and ViralFactory PM risk reasoning.

The qualified decision remains:

> Keep `semantic_reasoning_profile` as an optional companion audit/reconstruction artifact.

The strongest positive signal was currentness-sensitive cross-artifact reconstruction; the strongest negative signal was duplication where a domain artifact already carried evidence/currentness/uncertainty/limits. Therefore the profile remains selective and outside Campaign artifact admission.

The later build-first policy does **not** erase Phase 10. It changes the prospective development gate: additional experiments are deferred while mechanically clear construction runway remains.

## Qualified Phase 15 baseline — registry liveness

The existing `validate-skill-registry-liveness.py` rule remains qualified and checks only narrow consistency failures such as a live canonical Skill being described as merely proposed/no-current-implementation, wrong/broken canonical Skill paths, and duplicate registry IDs.

It remains a bounded conformance rule with `semantic_truth_established: false`. The build-first manifest/domain conformance layer runs **beside** it rather than replacing it.

## Build-first policy

The active decision rule is:

```text
Can the next architecture be justified primarily
from existing contracts + a known missing capability?

YES -> build and mechanically qualify
NO  -> invoke additional empirical validation
```

Mechanical verification remains continuous. See `build-first-policy.md` for the Construction Diminishing-Returns Gate.

## Build-first executable substrate candidate

### Mechanical observations

Current v0 probes cover:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every observation preserves target ref, evidence refs, source/method, scope, completeness, and currentness. A probe establishes only its declared mechanical fact.

### Repository Semantic Map v0

A bounded map combines **supplied** observations into `repository_locator` entities and `DERIVED` mechanical relations. It rejects mixed target refs and explicitly remains incomplete.

It does not infer `Component`, `Layer`, `Boundary`, architecture quality, importance, or a recommended change.

### Cross-Skill semantic companion

An optional append-only SHA-256 hash chain preserves explicit artifact/evidence/claim/uncertainty references between Skills. It stores provenance references, not hidden chain of thought.

Campaigns can carry this as `semantic-state.jsonl` without changing Campaign schema v2. Repository-bound Campaigns bind new entries to the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

### Skill/domain conformance

`skill-manifests/` describes deterministic Skill interfaces. `domain-packs/` provides reference manifests for a bounded Engineering slice and the completed Product Management migration.

The new checker validates manifest/domain shape and cross-reference consistency while explicitly rejecting fields that imply deterministic semantic truth, auto-routing, automatic Skill selection, or automatic uncertainty ranking.

### Campaign observability and portability

New projections/transport commands include:

```text
campaign inspect
campaign explain
campaign diff
campaign semantic-state-append
campaign semantic-state
campaign resume-context
campaign replay
campaign graph
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

These inspect, connect, project, or transport durable state; they do not determine a warranted next action. Replay refuses to invent historic full-state snapshots not stored by Campaign v2. Bundles verify byte/path integrity, not semantic correctness.

## Domain Pack status

The build-first candidate extracts **reference manifests**, not a plugin runtime:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

Engineering is deliberately represented by the first bounded semantic-alignment slice, not by a claim that every engineering Skill has been normalized. Product Management references the completed 27-Skill repository-qualified migration and its existing qualification policy.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

## Authority boundary

The active agent/human owns semantic interpretation, consequential uncertainty selection, warranted responsibility selection, semantic capability selection, and judgment about whether evidence warrants a conclusion or repair success.

Deterministic machinery may own repository identity/mechanical observation, declared probe scope/completeness, structural validation, persistence/integrity, exact-byte provenance, bounded conformance checks, authority metadata checks, reconstructible history, and bundle integrity.

Therefore:

```text
observation != interpretation
artifact valid != claim true
relation detected != architectural intent established
capability available != capability warranted
repository changed != repair succeeded
semantic profile valid != reasoning semantically correct
registry liveness valid != Skill semantically correct
semantic map relation != architecture judgment
manifest valid != Skill should run
bundle valid != Campaign semantically correct
provenance edge != semantic support
```

## Construction Diminishing-Returns Gate

Additional empirical validation becomes required when construction can no longer resolve its own architecture questions. Signals include competing designs with no contract-based discriminator, abstraction without new capability, speculative durable fields, formalization outpacing consumption, maintenance dominating capability growth, persistent placement ambiguity, behavioral-value questions becoming decisive, or pressure to transfer semantic judgment into deterministic machinery.

Completing the current build package does not automatically mean the gate has been reached.

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
- mandatory use of `semantic_reasoning_profile` in every artifact;
- claiming that this build-first substrate was empirically validated by the historical Phase 10 episodes.

## Current frontier

The build-first candidate extends the already-qualified Phase 10/Phase 15 baseline with bounded mechanical substrate, map/state sharing, Campaign observability, broader conformance, reference Domain Packs, and portability ergonomics while preserving Campaign schema v2.

After exact-head qualification, further construction should come from a concrete remaining product/integrity gap. When the next architecture instead depends on a behavioral value question, stop building and invoke the additional empirical-validation program defined by the diminishing-returns policy.
