# Sensemaking Semantic Architecture

**Status:** Canonical semantic foundation; Phase 9 and Phase 10 complete; bounded Phase 15 liveness qualified; post-Phase-10 build-first substrate B1–B7 repository-qualified  
**Scope:** Repository reasoning, evidence semantics, work/product semantics, bounded mechanical observations, cross-Skill provenance, conformance, Campaign observability, reference audit, and portability  
**Semantic authority:** The active agent/human owns interpretation and warrant; executable semantic machinery implements only documented mechanical subsets

## Purpose

Sensemaking needs a shared semantic model so different Skills can reason about repositories with consistent meanings for repository structure, evidence, claims, uncertainty, responsibility, capability, authority, change, and validation.

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
    +-- semantic-reference audit
    +-- artifacts / validators / conformance checks
    +-- Campaign persistence / observability / portability
```

No lower layer automatically receives semantic authority from an upper-layer concept.

## Relationship to the four control levels

The semantic hierarchy above answers **where semantic responsibility and implementation live**. The repository's four control levels answer **at what decision scope the active agent is operating**.

The control model is defined in [`../strategic-outer-loop.md`](../strategic-outer-loop.md):

```text
Level 4 — Product Thesis / Strategy Revision
Level 3 — Strategic Repository Evolution
Level 2 — Responsibility / Campaign
Level 1 — Execution
```

These views are orthogonal, not competing architectures. For example, the Reasoning Model can inform Level-2 Campaign work and Level-3 strategic reassessment, while executable Campaign persistence remains substrate machinery even when the Campaign sits inside a higher-scope strategic decision.

```text
semantic layer != control level
four semantic layers != four control-loop stages
Level-3 strategic state != Level-3 executable semantic contract
```

The duplicated word `Level` comes from two different taxonomies: semantic formalization levels are defined below as Vocabulary / Ontology / Executable Contract, while control levels are decision scopes. Do not infer equivalence from the numbering.

The Strategic Outer Loop is not a semantic router or deterministic planner. It uses semantic/evidence concepts while leaving frontier selection, strategy interpretation, and warrant to the active agent/human under authority.

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
| [`b7-semantic-reference-audit-design-preflight.md`](b7-semantic-reference-audit-design-preflight.md) | B7 reference-audit construction authority, resolver matrix, boundaries, and abort gate. |
| [`skill-contract-manifests-and-domain-packs.md`](skill-contract-manifests-and-domain-packs.md) | Skill/domain manifests and conformance. |
| [`pilots/README.md`](pilots/README.md) | Phase 9 pilot evidence. |
| [`common-semantic-contract.md`](common-semantic-contract.md) | `semantic_reasoning_profile` Level-3 contract. |
| [`phase-10/results.md`](phase-10/results.md) | Qualified Phase 10 evidence and Outcome A. |
| [`phase-10-handoff.md`](phase-10-handoff.md) | Phase 10 qualification handoff. |
| [`phase-15/README.md`](phase-15/README.md) | Qualified bounded Skill-registry liveness pilot. |
| [`phase-15-handoff.md`](phase-15-handoff.md) | Phase 15 liveness qualification evidence. |
| [`build-first-handoff.md`](build-first-handoff.md) | B1–B7 exact-head qualification and continuation handoff. |

Campaign observability, Resume Capsule, replay/graph, semantic companion integration, B7 reference-audit rendering, and portable bundles are documented in [`../campaign-observability-and-portability.md`](../campaign-observability-and-portability.md).

Higher-scope product/repository control is documented in [`../strategic-outer-loop.md`](../strategic-outer-loop.md), [`../strategic-state-contract.md`](../strategic-state-contract.md), [`../product-thesis-revision.md`](../product-thesis-revision.md), and [`../product-strategy.md`](../product-strategy.md).

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

These formalization levels are separate from the four control levels described above.

Phase 9 produced `semantic_reasoning_profile` v1. Phase 10 retained it as an **optional companion** while rejecting mandatory universal embedding. The qualified Phase 15 liveness pilot added a narrow conformance rule over explicit Skill-registry/tree consistency.

PR #327 repository-qualified B1–B6 mechanics where the boundary was directly mechanical. PR #330 then repository-qualified B7 reference resolution/audit from existing Campaign evidence/admission authorities without adding universal semantic identity or routing authority.

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

Qualified decision:

> Keep `semantic_reasoning_profile` as an optional companion audit/reconstruction artifact.

The strongest positive signal was currentness-sensitive cross-artifact reconstruction; the strongest negative signal was duplication where a domain artifact already carried evidence/currentness/uncertainty/limits. The profile therefore remains selective and outside Campaign artifact admission.

The later build-first policy does **not** erase Phase 10. It changes the prospective development gate: additional experiments are deferred while mechanically clear construction runway remains.

## Qualified Phase 15 baseline — registry liveness

The existing `validate-skill-registry-liveness.py` rule remains qualified. It checks only narrow consistency failures such as a live canonical Skill being described as merely proposed/no-current-implementation, wrong/broken canonical Skill paths, and duplicate registry IDs.

It remains a bounded conformance rule with `semantic_truth_established: false`.

## Post-Phase-10 build-first substrate — B1–B7 repository-qualified

### B1–B6

PR #327 qualified the B1–B6 build-first track on exact candidate `1f180cb6a61a060ed9b46b005f0b539b18d21198` with Product Validation `34471983343`, Release Candidate Distribution `34471983250`, and Lab Validation `34471983249`, then merged as `9e1e0356486f16d113ce7e182d2ef00e0110f857`.

See `build-first-handoff.md` for exact scope, rejection evidence, and non-claims.

### Mechanical observations

Repository-qualified v0 probes cover:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every observation preserves target ref, evidence refs, source/method, scope, completeness, and currentness. A probe establishes only its declared mechanical fact.

```text
import syntax present != runtime dependency established
import syntax present != architecture violation
zero exact matches in bounded scope != universal absence
```

### Repository Semantic Map v0

A repository-qualified bounded map combines **supplied** observations into `repository_locator` entities and `DERIVED` mechanical relations. It rejects mixed target refs and remains explicitly incomplete.

It does not infer `Component`, `Layer`, `Boundary`, architecture quality, importance, or recommended work.

### Cross-Skill semantic companion

`SemanticStateStore` provides an optional append-only SHA-256 chain preserving explicit artifact/evidence/claim/uncertainty references between Skills. It stores provenance references, not hidden chain of thought.

Campaigns can carry this as `semantic-state.jsonl` without changing **Campaign schema v2**. Repository-bound Campaign entries bind to the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

### Skill/domain conformance

`skill-manifests/` describes deterministic Skill interfaces. `domain-packs/` provides repository-qualified reference manifests for a bounded Engineering slice and the completed Product Management migration.

The manifest/domain checker runs beside the qualified registry-liveness checker. It validates shape, canonical Skill existence, semantic vocabulary, pack/manifest domain agreement, responsibility/artifact coverage, and references while rejecting fields that imply deterministic semantic truth, auto-routing, automatic Skill selection, or automatic uncertainty ranking.

```text
manifest valid != Skill should run
```

### Campaign observability and portability

Repository-qualified commands include:

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

`resume-context` is a deterministic Resume Capsule. Replay refuses to invent historical full-state snapshots not stored by Campaign v2. Graph output records provenance relations, not semantic support or causality.

Portable Campaign bundles preserve exact workspace bytes plus SHA-256/size bindings and fail closed on unsafe paths, symlinks, duplicate/undeclared/missing members, digest/size mismatch, unsupported format/version, and output destinations inside the source workspace.

```text
bundle valid != Campaign semantically correct
```

### B7 — Semantic Reference Resolution & Integrity Audit v0

PR #330 qualified B7 on exact candidate `8369d750c893f143830db6ccc69c8fa80d321dd4` with Product Validation `34565797654`, Release Candidate Distribution `34565797661`, and Lab Validation `34565797689`, then merged as `6203be05636b12e012a87940429041ff24af821d`.

The standalone `semantic_architecture.reference_audit` primitive mechanically audits outbound `SemanticStateEntry` references using only existing authoritative identities. Campaign rendering is exposed through `campaign semantic-state` and `campaign explain --ref`.

The result keeps resolution, address-space class, and integrity effect separate:

```text
resolved | dangling | ambiguous | not_addressable
```

Current v0 authorities resolve Campaign evidence/admitted artifacts, parent semantic entries, exact current Campaign uncertainty where represented, and target binding without currentness inference. Unsupported claim/profile references remain `not_addressable` rather than becoming invalid data.

```text
not_addressable != invalid
resolved != current
reference occurrence != reference resolution
reference audit pass != semantic truth
```

B7 does not modify Campaign schema v2, Resume Capsule, `SemanticStateStore.validate()`, currentness semantics, semantic routing, or semantic truth authority.

## Domain Pack status

Current repository-qualified reference manifests:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

Engineering is deliberately represented by the first bounded semantic-alignment slice rather than a claim that every engineering Skill has been normalized. Product Management references the completed 27-Skill repository-qualified migration and existing qualification policy.

A Domain Pack is a reference contract shape, not a plugin runtime or semantic router.

## Build-first policy

The active decision rule is:

```text
Can the next architecture be justified primarily
from existing contracts + a known missing capability?

YES -> build and mechanically qualify
NO  -> invoke additional empirical validation when policy/owner direction requires it
```

Mechanical verification remains continuous. Additional empirical experiments are currently deferred by owner direction while a concrete missing capability has a clear mechanical contract.

See `build-first-policy.md` for the Construction Diminishing-Returns Gate.

## Construction Diminishing-Returns Gate

Additional empirical validation becomes required when construction can no longer resolve its own architecture questions. Signals include competing designs with no contract-based discriminator, abstraction without new capability, speculative durable fields, formalization outpacing consumption, maintenance dominating capability growth, persistent placement ambiguity, behavioral-value questions becoming decisive, or pressure to transfer semantic judgment into deterministic machinery.

Completing B1–B7 does not automatically mean the gate has been reached. The B7 preflight nevertheless requires a fresh post-B7 reassessment rather than a presumptive B8 queue.

## Authority boundary

The active agent/human owns semantic interpretation, consequential uncertainty selection, warranted responsibility selection, semantic capability selection, Strategic Frontier selection, and judgment about whether evidence warrants a conclusion, repair success, or higher-scope strategy review.

Deterministic machinery may own repository identity/mechanical observation, declared probe scope/completeness, structural validation, persistence/integrity, exact-byte provenance, bounded conformance checks, reference-resolution integrity under existing namespaces, authority metadata checks, reconstructible history, and bundle integrity.

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
Domain Pack membership != routing authority
bundle valid != Campaign semantically correct
provenance edge != semantic support
reference resolved != current
reference audit pass != semantic truth
```

## Empirical status of B1–B7

B1–B7 are repository-qualified implementation capabilities. Their CI qualification does **not** establish that they reduce coordination cost or improve real native-agent task quality. That later product-value question remains intentionally deferred until the Construction Diminishing-Returns Gate or an explicit owner decision.

This distinction preserves:

```text
repository implementation qualified
!=
real-agent product value empirically established
```

## Non-goals

This architecture does **not** authorize:

- a universal ontology of all software engineering;
- a complete repository knowledge graph;
- a universal semantic-reference namespace or registry;
- automatic semantic routing;
- automatic architecture judgment;
- automatic uncertainty ranking;
- automatic Skill selection;
- confidence scores treated as truth probabilities;
- ontology-driven mutation authority;
- replacing source evidence with a generated semantic map;
- a central Reasoning Engine;
- mandatory use of `semantic_reasoning_profile` in every artifact;
- inferring currentness, support, or truth from reference resolution;
- claiming that B1–B7 were empirically validated by the historical Phase 10 episodes;
- treating the four control levels as semantic-layer implementations;
- using semantic formalization levels to infer strategic authority.

## Current frontier

The repository now has a broad mechanically bounded semantic substrate, map/state sharing, Campaign observability, reference-resolution audit, conformance, Domain Pack references, and portability ergonomics while preserving Campaign schema v2 and Phase 10 Outcome A.

The separate Strategic Outer Loop foundation defines Level-3/Level-4 repository control and product-thesis authority using existing documentation surfaces; it does not add a semantic router or autonomous strategic runtime.

Further semantic construction must start from a fresh post-B7 Level-3 reassessment and a concrete missing product/integrity/reconstruction capability. When the next architecture instead depends on a behavioral-value question, stop building at that boundary and invoke empirical validation only when required by policy or explicit owner direction.
