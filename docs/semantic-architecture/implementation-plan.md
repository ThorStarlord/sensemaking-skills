# Semantic Architecture Implementation Plan

**Status:** Active architecture program; Phase 10 complete; first bounded Phase 15 liveness rule qualified; post-Phase-10 build-first track implemented as a candidate  
**Completed empirical milestone:** Phase 10 common-envelope experiment — Outcome A  
**Qualified incremental check:** Phase 15 Skill-registry liveness conformance  
**Current strategy:** Preserve those results while continuing mechanically bounded construction until the Construction Diminishing-Returns Gate becomes decision-critical  
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

## Development policy after Phase 10

The active owner-authorized policy is defined in `build-first-policy.md`.

Sensemaking distinguishes:

```text
mechanical verification
!=
empirical product validation
```

Mechanical verification remains continuous through rejection tests, exact-head CI, packaging/install proof, integrity checks, and explicit authority boundaries. Phase 10's Outcome A remains preserved; only **additional** empirical episodes are deferred while a concrete build runway remains.

This policy is prospective. It does not erase the three Phase 10 episodes or the later bounded Phase 15 liveness pilot.

## Permanent promotion ladder

```text
observed vocabulary / maintenance need
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
Level 3: executable semantic contract / bounded conformance rule
```

Level-3 behavior requires stable meaning, an identified mechanically decidable subset, explicit validator/probe scope, negative/rejection cases, compatible versioning when durable state is affected, and preservation of agent/human semantic authority. Empirical promotion claims remain separately evidence-gated.

---

# Historical phase status

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
| 11 | Mechanical semantic probes | SUPERSEDED AS A STRICT EMPIRICAL GATE by build-first policy; bounded v0 candidate now exists |
| 12 | Repository Semantic Map experiment | SUPERSEDED AS A STRICT EMPIRICAL GATE by build-first policy; bounded supplied-observation v0 candidate now exists |
| 13 | Campaign/control-plane promotion | STILL DEFERRED; companion integration exists without Campaign schema promotion |
| 14 | Domain-pack extraction | REFERENCE-SHAPE CANDIDATE only; no generic plugin/router runtime |
| 15 | Ontology conformance/drift checks | INCREMENTAL — registry-liveness rule qualified; manifest/domain-pack conformance candidate added |

The word **superseded** here applies only to the old requirement that a new empirical episode had to occur before construction. It does not claim the historical evidence suddenly warranted broader semantics.

---

# Phase 9 — Reasoning Model operationalization

The first contrasting pilots covered `repo-sensemaker`, `architectural-review`, and `repair-verifier` + `output-reconciler`.

They found a recurring warrant/provenance core:

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

Phase 9 produced `semantic_reasoning_profile` v1 as an experimental Level-3 representation contract whose validator checks representation, not semantic truth.

---

# Phase 10 — qualified Outcome A

Phase 10 ran three contrasting real-repository episodes:

1. Chess Mentor Engine — `repo-sensemaker` direct diagnosis/currentness.
2. React incremental game — `output-reconciler` across immutable exact-SHA evidence and mutable live PR metadata.
3. ViralFactory — PM `pre-mortem` / canonical `risk_analysis` compared with the companion profile.

The qualified decision remains:

> Keep `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**.

The experiment found useful domain-neutral reconstruction value and currentness discipline, but also strong duplication pressure where domain artifacts already represented the decision-changing evidence/currentness/uncertainty/limits.

Accordingly, Phase 10 did **not** authorize a mandatory universal envelope, Campaign admission/promotion of the profile, a central reasoning engine, semantic routing, or semantic truth scoring. See `phase-10/results.md` and `phase-10-handoff.md`.

---

# Phase 15 qualified baseline — Skill-registry liveness

A post-Phase-10 maintenance audit found a narrow mechanically decidable drift class: compatibility Skill-registry liveness prose could contradict the canonical `skills/<id>/SKILL.md` tree.

The already-qualified `validate-skill-registry-liveness.py` rule checks duplicate registry IDs, `status: proposed` despite a live canonical Skill, explicit “no current implementation” notes despite a live Skill, and wrong/broken canonical Skill paths. It preserves `semantic_truth_established: false` and does not judge Skill quality or selection.

That bounded rule remains intact. The build-first work below extends conformance beside it rather than replacing it.

---

# Post-Phase-10 Build-First Track

The following packages are construction candidates. Their source exists on the current build branch; repository-qualified status requires exact-head Product Validation / release qualification and merge.

## B1 — Mechanical Semantic Substrate

Current v0 probes:

```text
file containment
Python import syntax
supported manifest dependencies
exact UTF-8 literal search
```

Each `SemanticObservation` preserves kind, subject/predicate/object, evidence refs, mechanical source, declared scope, completeness, currentness, target ref, and optional metadata.

Boundaries:

```text
import syntax present != runtime dependency established
import syntax present != architecture violation
dependency declared != dependency used
zero exact matches in declared UTF-8 scope != universal absence
```

The executable contract is documented in `mechanical-semantic-substrate.md`.

## B2 — Repository Semantic Map v0

`RepositorySemanticMap` combines **supplied** observations into generic repository-locator entities and `DERIVED` mechanical relations. It rejects mixed target refs and preserves source observation/evidence references plus explicit non-completeness limits.

It does not infer `Component`, `Layer`, `Boundary`, architecture quality, importance, or a recommended change.

```text
absence from map != absence from repository
relation in map != semantic importance
repository locator != architectural Component
```

## B3 — Cross-Skill Semantic State + Campaign Observability

`SemanticStateStore` provides an optional append-only SHA-256-chained JSONL companion containing explicit artifact/evidence/claim/uncertainty references between Skills. Reconstruction detects tamper, previous-digest mismatch, duplicate IDs, and missing/future/self-parent refs.

Campaigns may carry the companion as `semantic-state.jsonl` while **Campaign schema remains v2**. Repository-bound Campaigns derive the companion target identity from the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

New deterministic Campaign projections:

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

`resume-context` is the Resume Capsule. `replay` exposes only historical information Campaign v2 actually stores and explicitly refuses to fabricate full state snapshots after every transition. `graph` renders recorded provenance edges, not semantic causality.

This package does **not** implement the old Phase 13 proposal to promote the Phase 10 profile into Campaign schema/admission.

## B4 — Skill Contract Manifests + broader bounded conformance

Skill Contract Manifest v1 makes the deterministic Skill shell machine-readable:

```text
skill identity
domain
responsibility declarations
canonical consumed identities
canonical produced identities
shared semantic concepts
repository mutation declaration
```

The new conformance layer runs beside the already-qualified registry-liveness checker and validates required fields, duplicate values/IDs, canonical Skill-file existence, semantic vocabulary membership, Domain Pack domain agreement, responsibility/artifact coverage, and referenced pack files.

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

## B5 — Domain Pack reference architecture

Two repository-owned **reference manifests** exist:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

A Domain Pack references domain identity, capability ledger, Skill manifests, responsibility vocabulary, artifact identities, and qualification policy.

The engineering reference is deliberately bounded to the first semantic-alignment slice; it does not pretend every engineering capability has been normalized. Product Management references the completed 27-Skill repository-qualified migration and its existing qualification policy.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

This is a reference contract shape, not a generic runtime plugin system.

## B6 — Portability and ergonomics

The Campaign product gains:

```text
campaign resume-context
campaign replay
campaign graph
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles are deterministic ZIP archives of exact Campaign workspace bytes plus a SHA-256/size manifest. Verification fails closed on unsafe paths, symlinks, duplicate members, undeclared/missing members, digest mismatch, size mismatch, and unsupported format/version. Export destinations inside the source workspace are rejected so bundle creation cannot mutate the bytes it claims to package.

```text
bundle integrity valid != semantic Campaign correctness
```

See `../campaign-observability-and-portability.md`.

---

# Construction Diminishing-Returns Gate

The gate is defined in `build-first-policy.md`.

Construction may continue without new empirical episodes while the next missing capability is concrete and its mechanical contract is clear.

Additional empirical validation becomes mandatory when design is dominated by:

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

Completing B1–B6 does not itself prove diminishing returns.

---

# Deferred additional empirical validation

Phase 10 is not repeated by default. When the diminishing-returns gate eventually triggers, new studies may evaluate the capabilities added by B1–B6, including:

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

The goal remains **more consistent warranted reasoning per unit of coordination overhead**, but that ratio is an empirical product claim only when measured.

# Current development loop

```text
known missing capability
-> bounded mechanical contract
-> negative cases
-> implementation
-> exact-head qualification
-> next known gap
-> Construction Diminishing-Returns Gate
-> additional empirical validation when triggered
```

Do not build a central reasoning engine, universal semantic router, automatic uncertainty ranking, automatic Skill selection, confidence-as-truth scoring, or ontology-driven mutation authority under this roadmap.
