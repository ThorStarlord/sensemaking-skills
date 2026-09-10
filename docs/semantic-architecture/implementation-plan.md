# Semantic Architecture Implementation Plan

**Status:** Active build-first architecture program  
**Completed empirical milestone:** Phase 10 common-envelope experiment — Outcome A  
**Current strategy:** Continue mechanically bounded construction while architecture remains informative; defer additional empirical experiments until the Construction Diminishing-Returns Gate becomes decision-critical  
**Implementation principle:** Formalize from concrete product/integrity pressure; do not manufacture runtime machinery merely to make the ontology look complete.

## Objective

Create a shared semantic foundation that lets Sensemaking Skills reason consistently about unfamiliar repositories while preserving evidence lineage, currentness, uncertainty, semantic authority, and the existing agent/deterministic control boundary.

The long-run progression is:

```text
documented vocabulary
-> ontology semantics
-> bounded Skill adoption
-> mechanically decidable representation
-> reusable product capability
-> empirical validation when behavior becomes decision-critical
```

A later phase never retroactively turns documentation into runtime authority, and repository implementation never retroactively strengthens an empirical claim.

## Development policy

The active post-Phase-10 policy is defined in `build-first-policy.md`.

Sensemaking distinguishes:

```text
mechanical verification
!=
empirical product validation
```

Mechanical verification remains continuous through rejection tests, exact-head CI, packaging/install proof, integrity checks, and explicit authority boundaries. Phase 10's Outcome A remains preserved; only **additional** empirical episodes are deferred.

## Permanent promotion ladder

```text
observed vocabulary need
        |
        v
Level 1: shared term
        |
        | repeated useful distinction
        v
Level 2: ontology entity/relation
        |
        | stable meaning + concrete mechanical/product pressure
        v
Level 3: executable semantic contract
```

### Level 1 -> Level 2 gate

Require a competency question, reusable meaning, clear definition, no canonical duplicate, and useful relations to existing concepts.

### Level 2 -> Level 3 gate

Require stable meaning, an identified mechanically decidable subset, explicit validator/probe scope, negative/rejection cases, compatible versioning when durable state is affected, and preservation of agent/human semantic authority. Empirical promotion claims remain separately evidence-gated.

---

# Phase status map

| Phase | Name | Status |
|---:|---|---|
| 0 | Preserve architecture boundary | COMPLETE |
| 1 | Problem definition | COMPLETE |
| 2 | Competency questions | COMPLETE |
| 3 | Existing concept inventory/reconciliation | BASELINE COMPLETE; incremental |
| 4 | Layered ontology | COMPLETE at Level 2 |
| 5 | Relationship and epistemic model | COMPLETE at Level 2 |
| 6 | Reasoning architecture | COMPLETE at design level |
| 7 | Integration architecture | COMPLETE at design level |
| 8 | Reference scenarios | COMPLETE |
| 9 | Reasoning Model operationalization / Skill semantic-alignment pilots | COMPLETE for first contrasting set |
| 10 | Common artifact-semantic envelope experiment | COMPLETE — Outcome A: optional companion profile |
| 11 | Mechanical Semantic Substrate | IMPLEMENTED CANDIDATE; exact-head qualification required |
| 12 | Repository Semantic Map v0 | IMPLEMENTED CANDIDATE; bounded supplied-observation map |
| 13 | Cross-Skill Semantic State + Campaign observability | IMPLEMENTED CANDIDATE; additive companion, Campaign schema remains v2 |
| 14 | Semantic conformance + Skill Contract Manifests | IMPLEMENTED CANDIDATE |
| 15 | Domain Pack reference architecture | IMPLEMENTED CANDIDATE for engineering + Product Management |
| 16 | Portability & ergonomics | IMPLEMENTED CANDIDATE: Resume Capsule, replay/graph, Campaign bundles |
| 17 | Construction Diminishing-Returns Gate | ACTIVE policy monitor; not automatically triggered by Phase 16 |
| 18 | Additional empirical/native validation | DEFERRED until Phase 17 trigger or explicit owner decision |

“Implemented candidate” means source behavior exists. Repository-qualified claims require the exact candidate head to pass the repository's existing CI/release gates and merge.

---

# Phases 0–9 — Foundation and first operationalization

The foundation established the semantic constitution, problem statement, competency questions, concept inventory, layered ontology, relationship/epistemic rules, Reasoning Model, integration boundaries, reference scenarios, and the first contrasting engineering Skill pilots.

Phase 9 found a recurring warrant/provenance core:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence refs
bounded scope / claim limits
uncertainty
explicit limits / non-claims
```

It also produced `semantic_reasoning_profile` v1 as an experimental Level-3 representation contract whose validator checks representation, not semantic truth.

---

# Phase 10 — Common Artifact-Semantic Envelope Experiment

**Status:** COMPLETE — repository-qualified Outcome A.

Phase 10 ran three contrasting real-repository episodes:

1. Chess Mentor Engine — `repo-sensemaker` direct diagnosis/currentness.
2. React incremental game — `output-reconciler` across immutable exact-SHA evidence and mutable live PR metadata.
3. ViralFactory — PM `pre-mortem` / canonical `risk_analysis` compared with the companion profile.

The qualified decision remains **Outcome A**:

> Keep `semantic_reasoning_profile` v1 as an optional companion audit/reconstruction artifact.

Use it selectively when reasoning crosses artifacts/surfaces/domains, a fresh context needs a compact warrant/provenance index, or cross-domain audit would otherwise require learning local taxonomies first.

Do not require it when strong domain artifacts already represent the decision-changing evidence/currentness/uncertainty/limits.

Phase 10 did **not** authorize a mandatory universal envelope, Campaign admission of the profile, a central reasoning engine, semantic routing, or semantic truth scoring. See `phase-10/results.md` and `phase-10-handoff.md` for the qualified evidence.

The owner subsequently authorized a **build-first continuation policy**: preserve Outcome A, but do not require new experiments before every mechanically clear construction package. That policy is prospective; it does not rewrite Phase 10's historical evidence.

---

# Phase 11 — Mechanical Semantic Substrate

## Goal

Give Skills deterministic repository observations that preserve exact scope, completeness, currentness, and provenance without making semantic conclusions.

## Implemented candidate

Current v0 probes:

```text
file containment
Python import syntax
supported manifest dependencies
exact UTF-8 literal search
```

Each `SemanticObservation` records kind, subject/predicate/object, evidence refs, mechanical source, declared scope, completeness, currentness, target ref, and optional mechanical metadata.

Boundaries include:

```text
import syntax present != runtime dependency established
import syntax present != architecture violation
dependency declared != dependency used
zero exact matches in declared UTF-8 scope != universal absence
```

The executable contract is documented in `mechanical-semantic-substrate.md`.

---

# Phase 12 — Repository Semantic Map v0

## Goal

Share mechanically observed repository relations without forcing every Skill to reconstruct the same structural facts.

## Implemented candidate

`RepositorySemanticMap` contains:

```text
map_id
target_ref
repository-locator entities
DERIVED mechanical relations
source observation IDs
evidence refs
optional external claim refs
optional external uncertainty refs
explicit limits
```

The builder accepts supplied observations only, rejects mixed target refs, and never infers architectural Components/Layers/Boundaries from directory/file shape.

```text
absence from map != absence from repository
relation in map != semantic importance
repository locator != architectural Component
```

This is a bounded shared representation, not a complete repository source of truth.

---

# Phase 13 — Cross-Skill Semantic State and Campaign Observability

## Goal

Preserve lightweight semantic provenance between bounded Skill episodes and make Campaign state easier to inspect without migrating Campaign schema v2.

## Cross-Skill companion state

`SemanticStateStore` provides an optional append-only SHA-256 chained JSONL log containing explicit references:

```text
entry ID
source Skill
artifact ref
target ref
evidence refs
claim refs
uncertainty refs
parent semantic entries
optional semantic profile ref
notes
timestamp
```

Reconstruction detects tamper, previous-digest mismatch, duplicate IDs, and missing/future/self-parent references.

Campaigns may store this companion as `semantic-state.jsonl` in the workspace. It remains outside `CampaignState`; no schema v3 is introduced.

Repository-bound Campaigns derive the companion target ref from the current TargetSnapshot digest. Targetless Campaigns require an explicit target ref.

## Observability commands

```text
campaign inspect
campaign explain
campaign diff
campaign semantic-state-append
campaign semantic-state
campaign resume-context
campaign replay
campaign graph
```

`resume-context` is the deterministic Resume Capsule. `replay` exposes only historical information Campaign v2 actually stores and explicitly refuses to fabricate full state snapshots after every transition. `graph` renders recorded provenance edges, not semantic causality.

---

# Phase 14 — Semantic Conformance and Skill Contract Manifests

## Goal

Make the deterministic shell of a Skill machine-readable without turning metadata into a semantic router.

## Skill Contract Manifest v1

Manifests declare:

```text
skill identity
domain
responsibility declarations
canonical consumed identities
canonical produced identities
shared semantic concepts
repository mutation declaration
```

Conformance checks required fields, shape, duplicate values/IDs, canonical Skill-file existence, semantic vocabulary membership, Domain Pack domain agreement, responsibility/artifact coverage, and referenced pack files.

Fields implying semantic control are rejected, including:

```text
semantic_truth
auto_route
automatic_skill_selection
automatic_uncertainty_ranking
```

```text
manifest valid != Skill semantically good
manifest responsibility declared != responsibility warranted now
Skill available != Skill should run
```

---

# Phase 15 — Domain Pack Reference Architecture

## Goal

Extract the repeated deterministic shell now visible across two materially different implemented domains without building a generic plugin/router runtime.

## Implemented reference manifests

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

A Domain Pack references domain identity, capability ledger, Skill manifests, responsibility vocabulary, artifact identities, and qualification policy.

The engineering reference pack is deliberately bounded to the first four semantic-alignment Skills. The Product Management pack references the completed 27-Skill repository-qualified migration and its existing maturity policy.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

This is a reference contract shape, not yet a generic runtime plugin system.

---

# Phase 16 — Portability and Ergonomics

## Resume Capsule

`campaign resume-context` emits a fresh-context projection of durable Campaign state plus optional semantic companion summary, but no recommended next action.

## Replay and provenance graph

`campaign replay` exposes the trace prefix possible under Campaign v2. `campaign graph` emits JSON or Mermaid for recorded Campaign/transition/evidence and semantic-companion provenance relations.

## Portable Campaign bundles

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles are deterministic ZIP archives of exact Campaign workspace bytes plus a SHA-256/size manifest. Verification fails closed on unsafe paths, symlinks, duplicate members, undeclared/missing members, digest mismatch, size mismatch, and unsupported format/version. Export destinations inside the source workspace are rejected so exporting a bundle cannot mutate the bytes it claims to package.

```text
bundle integrity valid != semantic Campaign correctness
```

---

# Phase 17 — Construction Diminishing-Returns Gate

The gate is defined in `build-first-policy.md`.

Construction may continue without new empirical episodes while the next missing capability is concrete and its mechanical contract is clear.

Empirical validation becomes mandatory when design is dominated by:

```text
competing architectures not resolvable from existing contracts
abstraction without new capability
speculative durable fields
formalization faster than consumption
maintenance/synchronization burden
behavioral value questions
persistent placement ambiguity
semantic-authority pressure
```

Completing a planned build package does not itself prove diminishing returns.

---

# Phase 18 — Deferred additional empirical validation

Phase 10 is not repeated by default. When Phase 17 eventually triggers, new studies may evaluate the capabilities added in Phases 11–16, including:

```text
repeated repository reconstruction avoided
mechanical probe usefulness
semantic-map reuse
fresh-context continuation via companion state/Resume Capsule
bundle portability
manifest/domain-pack drift reduction
token/coordination overhead
native-harness behavior where applicable
```

No current code should claim this later product-value study has already happened.

---

# Construction metrics

Track architecture pressure rather than ontology coverage:

```text
new mechanically useful relations requested
cross-Skill reconstruction points removed
integrity failures now rejected
semantic-authority overreach prevented
new product/operator capabilities unlocked
new schemas/metadata with no consumer
migration/synchronization burden
repeated architecture-placement disputes
```

The goal remains **more consistent warranted reasoning per unit of coordination overhead**, but the ratio is an empirical product claim only when measured.

# Current development loop

```text
known missing capability
-> bounded mechanical contract
-> negative cases
-> implementation
-> exact-head qualification
-> next known gap
-> Construction Diminishing-Returns Gate
-> empirical validation when triggered
```

Do not build a central reasoning engine, universal semantic router, automatic uncertainty ranking, automatic Skill selection, confidence-as-truth scoring, or ontology-driven mutation authority under this roadmap.
