# Semantic Architecture Implementation Plan

**Status:** Active build-first program  
**Completed foundation:** Semantic foundation + Phase 9 first Reasoning Model operationalization  
**Current strategy:** Continue mechanically bounded construction while architecture remains informative; invoke empirical validation when the Construction Diminishing-Returns Gate becomes decision-critical  
**Implementation principle:** Formalize from demonstrated product/contract pressure; do not manufacture runtime machinery merely to make the ontology look complete.

## Objective

Create a shared semantic foundation that lets Sensemaking Skills reason consistently about unfamiliar repositories while preserving evidence lineage, currentness, uncertainty, semantic authority, and the existing agent/deterministic control boundary.

The permanent progression is:

```text
documented vocabulary
-> ontology semantics
-> bounded Skill adoption
-> mechanically decidable representation
-> reusable product capability
-> empirical validation when behavior becomes decision-critical
```

A later phase never retroactively turns documentation into runtime authority.

## Development policy

The active policy is defined in `build-first-policy.md`.

Sensemaking distinguishes:

```text
mechanical verification
!=
empirical product validation
```

Mechanical verification remains continuous through rejection tests, exact-head CI, packaging/install proof, integrity checks, and explicit authority boundaries.

The earlier common-envelope value experiment is **parked**, not discarded. Its hypotheses remain useful when the architecture reaches diminishing returns or when a consequential design choice can no longer be resolved from existing contracts.

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
        | repeated cross-Skill burden
        | stable semantics
        | mechanically expressible subset
        v
Level 3: executable semantic contract
```

### Level 1 -> Level 2 gate

Require:

- at least one competency question;
- repeated semantic use or critical boundary value;
- clear definition;
- no canonical duplicate;
- useful relations to existing concepts.

### Level 2 -> Level 3 gate

Require:

- stable semantic meaning;
- an identified mechanically decidable subset;
- explicit validator/probe scope;
- negative/rejection cases;
- backward-compatibility or explicit versioning when durable state is affected;
- no transfer of semantic authority to deterministic machinery;
- either repeated workflow use or a concrete integrity/product capability that independently warrants the mechanical representation.

Empirical promotion claims remain stronger than repository implementation claims.

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
| 9 | Reasoning Model operationalization / Skill semantic-alignment pilots | FIRST THREE PILOTS COMPLETE |
| 10 | Mechanical Semantic Substrate | IMPLEMENTED; mechanical qualification required |
| 11 | Repository Semantic Map v0 | IMPLEMENTED as bounded supplied-observation map |
| 12 | Cross-Skill Semantic State | IMPLEMENTED as optional companion hash chain |
| 13 | Campaign Semantic Integration & Observability | IMPLEMENTED additively; Campaign schema remains v2 |
| 14 | Semantic Conformance & Skill Contract Manifests | IMPLEMENTED at repository-contract level |
| 15 | Domain Pack reference architecture | IMPLEMENTED for engineering + Product Management references |
| 16 | Portability & Ergonomics | IMPLEMENTED for Resume Capsule, replay/graph and Campaign bundles |
| 17 | Construction Diminishing-Returns Gate | ACTIVE monitoring; not automatically triggered by completing Phase 16 |
| 18 | Common-envelope / native empirical validation | DEFERRED until Phase 17 trigger or explicit owner decision |

“Implemented” in this plan means the capability exists in the source design. Repository-qualified claims require the exact candidate head to pass the repository's existing CI/release gates and merge.

---

# Phases 0–8 — Semantic foundation

The foundation established:

- semantic/evidence/authority constitution;
- problem statement;
- competency questions;
- concept inventory;
- Intent / Repository-System / Evidence / Knowledge / Work / Product ontology;
- `SoftwareCapability`, `SensemakingCapability`, and `ProductCapability` separation;
- relationship/epistemic rules and prohibited inferences;
- staged Reasoning Model;
- execution-integration boundaries;
- reference scenarios.

These remain semantic-design authority except where an existing executable product contract implements a mechanical subset.

---

# Phase 9 — Reasoning Model Operationalization

**Status:** COMPLETE for the first contrasting set.

Pilots covered:

```text
repo-sensemaker
architectural-review
repair-verifier + output-reconciler
```

The common warrant/provenance core was:

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

Domain-local vocabularies remained local. Phase 9 also produced experimental `semantic_reasoning_profile` v1, whose validator checks representation only and reports `semantic_truth_established: false`.

---

# Phase 10 — Mechanical Semantic Substrate

## Goal

Give Skills deterministic repository observations that preserve exact scope, completeness, currentness, and provenance without making semantic conclusions.

## Implemented v0 probes

```text
file containment
Python import syntax
supported manifest dependencies
exact UTF-8 literal search
```

Each observation records:

```text
kind
subject / predicate / object
evidence refs
source
scope
completeness
currentness
target ref
```

The contract is documented in `mechanical-semantic-substrate.md`.

## Boundary

```text
import syntax present != runtime dependency established
import syntax present != architecture violation
dependency declared != dependency used
zero exact matches in complete declared scope != universal absence
```

New probes require a concrete consumer and an explicit mechanical claim.

---

# Phase 11 — Repository Semantic Map v0

## Goal

Share mechanically observed repository relations without forcing every Skill to reconstruct the same structural facts.

## Implemented shape

```text
RepositorySemanticMap
- map_id
- target_ref
- repository-locator entities
- derived mechanical relations
- source observation refs
- evidence refs
- optional external claim refs
- optional external uncertainty refs
- explicit limits
```

The builder accepts supplied observations only, rejects mixed target refs, and never infers architecture Components/Layers/Boundaries from directory shape.

The v0 map is deliberately incomplete:

```text
absence from map != absence from repository
relation in map != semantic importance
repository locator != architectural Component
```

---

# Phase 12 — Cross-Skill Semantic State

## Goal

Preserve lightweight references between bounded Skill reasoning episodes without copying hidden reasoning or expanding Campaign schema.

## Implemented companion state

`SemanticStateStore` writes an append-only JSONL chain containing explicit refs:

```text
entry ID
source Skill
artifact ref
target ref
evidence refs
claim refs
uncertainty refs
parent semantic entries
optional profile ref
notes
timestamp
```

Entries are SHA-256 hash chained. Reconstruction detects tamper, chain mismatch, duplicate IDs, and missing/future/self-parent refs.

This is provenance, not a reasoning engine.

---

# Phase 13 — Campaign Semantic Integration & Observability

## Goal

Make durable Campaign state easier to inspect and allow optional cross-Skill semantic references to travel with a Campaign while preserving Campaign schema v2.

## Implemented commands

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

The companion semantic state uses `semantic-state.jsonl` inside the Campaign workspace. It is **not** a field in `CampaignState` and therefore does not require a schema migration.

Repository-bound Campaigns derive the semantic companion target ref from the current TargetSnapshot digest. Targetless Campaigns require an explicit target ref.

Observability commands expose recorded provenance and explicit limits. They never infer a next responsibility or decide whether a claim is true.

Replay explicitly refuses to invent full historic `CampaignState` snapshots that Campaign v2 did not store.

---

# Phase 14 — Semantic Conformance & Skill Contract Manifests

## Goal

Make the deterministic shell of a Skill machine-readable without turning metadata into a router.

## Skill Contract Manifest v1

```text
skill identity
domain
responsibility declarations
canonical consumed identities
canonical produced identities
shared semantic concepts
repository mutation declaration
```

Conformance checks include:

- schema/field shape;
- canonical Skill file existence;
- duplicate IDs/list values;
- canonical semantic vocabulary membership;
- prohibited semantic-authority fields;
- Domain Pack/manifest domain agreement;
- Domain Pack responsibility/artifact coverage.

Explicitly prohibited manifest concepts include automatic Skill selection, semantic truth claims, and automatic uncertainty ranking.

---

# Phase 15 — Domain Pack Reference Architecture

## Goal

Extract the repeated structural shell now demonstrated by two implemented domains without building a generic plugin/router platform.

## Implemented reference packs

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

A Domain Pack references:

```text
domain identity
capability ledger
Skill manifests
responsibility vocabulary
artifact identities
qualification policy
```

Engineering currently uses the four first semantic-alignment Skills as a bounded reference slice rather than pretending to enumerate every engineering Skill.

The PM pack references the complete repository-qualified PM migration set and its existing maturity policy.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

---

# Phase 16 — Portability & Ergonomics

## Resume Capsule

`campaign resume-context` gives a fresh agent a deterministic projection of durable state plus optional semantic companion summary. It includes an explicit limit instead of a recommended next action.

## Replay / graph

`campaign replay` exposes the transition prefix possible under Campaign v2. `campaign graph` renders recorded Campaign/transition/evidence and semantic-companion provenance relations without inventing causal semantics.

## Portable Campaign bundle

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles are deterministic ZIP archives of exact Campaign workspace bytes plus a SHA-256/size manifest. Verification fails closed on path traversal, symlinks, undeclared/missing files, duplicate members, digest mismatch, size mismatch, and format/version mismatch.

```text
bundle integrity valid != semantic Campaign correctness
```

---

# Phase 17 — Construction Diminishing-Returns Gate

The gate is defined in `build-first-policy.md`.

Construction should continue when the next missing capability is concrete and its mechanical contract is clear.

Empirical validation becomes mandatory when design is dominated by:

```text
competing architectures not resolvable from contracts
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

# Phase 18 — Deferred empirical validation

The previous common-envelope Phase 10 questions are preserved here for later execution.

When triggered, measure:

```text
repeated semantic reconstruction
claims missing currentness/evidence
unsupported inference jumps
fresh-context usefulness
artifact/profile duplication
token/coordination overhead
validator friction/overreach
native-harness behavior where applicable
```

Possible outcome is retention, narrowing, redistribution, or retirement of explicit semantic profile fields. No current code should claim this value study has already happened.

---

# Metrics for continued construction

Track architecture pressure rather than maximum ontology coverage:

```text
new mechanically useful relations requested
cross-Skill reconstruction points removed
integrity failures now rejected
semantic-authority overreach prevented
new product/operator capabilities unlocked
new schemas/metadata with no consumer
migration/synchronization burden
repeated architecture placement disputes
```

The goal remains **more consistent warranted reasoning per unit of coordination overhead**, but that ratio becomes an empirical product claim only after the deferred validation program runs.

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

Do not build a central reasoning engine, universal semantic router, automatic uncertainty ranking, or ontology-driven mutation authority under this roadmap.
