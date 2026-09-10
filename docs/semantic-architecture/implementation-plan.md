# Semantic Architecture Implementation Plan

**Status:** Active architecture program; Phase 10 complete; bounded Phase 15 liveness qualified; post-Phase-10 build-first track B1–B6 repository-qualified  
**Completed empirical milestone:** Phase 10 common-envelope experiment — Outcome A  
**Qualified incremental conformance:** Phase 15 Skill-registry liveness + post-Phase-10 Skill Manifest / Domain Pack conformance  
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
| 11 | Mechanical semantic probes | STRICT EMPIRICAL PRE-GATE SUPERSEDED by build-first policy; bounded v0 now repository-qualified |
| 12 | Repository Semantic Map experiment | STRICT EMPIRICAL PRE-GATE SUPERSEDED by build-first policy; bounded supplied-observation v0 now repository-qualified |
| 13 | Campaign/control-plane promotion | PROFILE PROMOTION STILL DEFERRED; additive companion + observability repository-qualified without Campaign schema migration |
| 14 | Domain-pack extraction | MINIMAL REFERENCE SHAPE repository-qualified; generic plugin/router runtime not authorized |
| 15 | Ontology conformance/drift checks | INCREMENTAL — registry-liveness and manifest/domain bounded rules repository-qualified |

The word **superseded** applies only to the former requirement for new empirical evidence before every construction step. It does not claim historical evidence warranted broader semantics.

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

Phase 9 produced `semantic_reasoning_profile` v1 as a Level-3 representation contract whose validator checks representation, not semantic truth.

---

# Phase 10 — qualified Outcome A

Phase 10 ran three contrasting real-repository episodes:

1. Chess Mentor Engine — `repo-sensemaker` direct diagnosis/currentness.
2. React incremental game — `output-reconciler` across immutable exact-SHA evidence and mutable live PR metadata.
3. ViralFactory — PM `pre-mortem` / canonical `risk_analysis` compared with the companion profile.

Qualified decision:

> Keep `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**.

The experiment found useful domain-neutral reconstruction/currentness value but also strong duplication pressure where domain artifacts already represented decision-changing evidence, currentness, uncertainty, and limits.

Accordingly, Phase 10 did **not** authorize a mandatory universal envelope, Campaign admission/promotion of the profile, a central reasoning engine, semantic routing, or semantic truth scoring. See `phase-10/results.md` and `phase-10-handoff.md`.

---

# Phase 15 qualified baseline — Skill-registry liveness

The previously qualified `validate-skill-registry-liveness.py` rule checks a narrow mechanically decidable drift class: duplicate registry IDs, `status: proposed` despite a live canonical Skill, explicit “no current implementation” notes despite a live Skill, and wrong/broken canonical Skill paths.

It preserves `semantic_truth_established: false` and does not judge Skill quality or selection.

The build-first conformance work below runs beside this rule rather than replacing it.

---

# Post-Phase-10 Build-First Track — repository-qualified

PR #327 repository-qualified B1–B6 on exact candidate `1f180cb6a61a060ed9b46b005f0b539b18d21198` before merge as `9e1e0356486f16d113ce7e182d2ef00e0110f857`.

Exact-head workflow evidence:

```text
Product Validation             34471983343  success
Release Candidate Distribution 34471983250  success
Lab Validation                 34471983249  success
```

See `build-first-handoff.md` for the full package and rejection evidence.

## B1 — Mechanical Semantic Substrate

**Status:** REPOSITORY_QUALIFIED.

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

**Status:** REPOSITORY_QUALIFIED as a bounded supplied-observation map.

`RepositorySemanticMap` combines supplied observations into generic repository-locator entities and `DERIVED` mechanical relations. It rejects mixed target refs and preserves source observation/evidence refs plus explicit non-completeness limits.

It does not infer `Component`, `Layer`, `Boundary`, architecture quality, importance, or recommended work.

```text
absence from map != absence from repository
relation in map != semantic importance
repository locator != architectural Component
```

## B3 — Cross-Skill Semantic State + Campaign Observability

**Status:** REPOSITORY_QUALIFIED additively; Campaign schema remains v2.

`SemanticStateStore` provides an optional append-only SHA-256-chained JSONL companion containing explicit artifact/evidence/claim/uncertainty references. Reconstruction detects tamper, previous-digest mismatch, duplicate IDs, and missing/future/self-parent refs.

Campaigns may carry it as `semantic-state.jsonl` without adding fields to `CampaignState`. Repository-bound Campaigns derive the companion target identity from the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

Repository-qualified commands:

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

`resume-context` is the Resume Capsule. `replay` exposes only historical information Campaign v2 actually stores; `graph` renders recorded provenance, not semantic causality.

This does **not** implement the old proposal to promote the Phase 10 profile into Campaign schema/admission.

## B4 — Skill Contract Manifests + broader bounded conformance

**Status:** REPOSITORY_QUALIFIED.

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

Conformance checks required fields, duplicate values/IDs, canonical Skill-file existence, semantic vocabulary membership, Domain Pack domain agreement, responsibility/artifact coverage, and referenced pack files.

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

**Status:** REPOSITORY_QUALIFIED as a reference-manifest shape.

Current repository-owned references:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

A Domain Pack references domain identity, capability ledger, Skill manifests, responsibility vocabulary, artifact identities, and qualification policy.

Engineering is deliberately bounded to the first semantic-alignment slice. Product Management references the complete 27-Skill repository-qualified migration.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

A generic plugin/router runtime remains unwarranted.

## B6 — Portability and ergonomics

**Status:** REPOSITORY_QUALIFIED.

Campaign product capabilities now include Resume Capsule, exact-ref explanation, transition diff, bounded replay, provenance graph, and:

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles are deterministic ZIP archives of exact Campaign workspace bytes plus a SHA-256/size manifest. Verification fails closed on unsafe paths, symlinks, duplicate members, undeclared/missing members, digest mismatch, size mismatch, unsupported format/version, and export destinations inside the source workspace.

```text
bundle integrity valid != semantic Campaign correctness
```

The installed-wheel smoke proves the semantic substrate and Campaign bundle implementation are present in the core distribution while source-only lab packages remain excluded.

---

# Construction Diminishing-Returns Gate

The active policy is defined in `build-first-policy.md`.

Construction may continue without additional empirical episodes while the next missing capability is concrete and its mechanical contract is clear.

Additional empirical validation becomes mandatory when design is dominated by:

```text
competing architectures not resolvable from existing contracts
abstraction without new capability
speculative durable fields
formalization faster than consumption
maintenance/synchronization burden
behavioral-value questions
persistent placement ambiguity
semantic-authority pressure
```

Completing B1–B6 does **not** itself prove diminishing returns.

---

# Deferred additional empirical validation

Phase 10 is not repeated by default. When the diminishing-returns gate eventually triggers, new studies may evaluate B1–B6 in real agent work:

```text
repeated repository reconstruction avoided
mechanical probe usefulness
semantic-map reuse
fresh-context continuation via semantic companion / Resume Capsule
bundle portability
manifest/domain-pack drift reduction
token/coordination overhead
native-harness behavior where applicable
```

No repository-qualified implementation claim should be described as if this later product-value study has already occurred.

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
