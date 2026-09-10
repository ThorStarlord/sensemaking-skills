# Build-First Semantic Substrate Handoff

**Milestone:** Post-Phase-10 build-first Semantic Architecture B1–B6  
**Status:** REPOSITORY_QUALIFIED  
**Implementation PR:** #327  
**Qualified candidate head:** `1f180cb6a61a060ed9b46b005f0b539b18d21198`  
**Merge commit:** `9e1e0356486f16d113ce7e182d2ef00e0110f857`  
**Date:** 2026-09-10

## Why this milestone exists

Phase 10 had already selected Outcome A: keep `semantic_reasoning_profile` v1 as an optional companion audit/reconstruction artifact. A later owner decision changed the *prospective* development strategy: continue building while concrete mechanically bounded capabilities remain obvious, and defer **additional** empirical experiments until construction hits diminishing returns or a consequential architecture choice becomes evidence-dependent.

This milestone implements that strategy without rewriting the historical Phase 10 result.

## Qualified build packages

### B1 — Mechanical Semantic Substrate

Shipped `sensemaking_skills.semantic_architecture` with mechanically bounded probes for:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every observation preserves target identity, source/method, evidence refs, scope, completeness, and currentness. The probes make no architectural or product judgment.

### B2 — Repository Semantic Map v0

Added a bounded map built only from supplied observations. It rejects mixed target refs, uses generic repository locators, marks mechanical relations `DERIVED`, retains source/evidence refs, and states explicit incompleteness limits.

The map does not infer architecture Components, Layers, Boundaries, importance, or recommended work.

### B3 — Cross-Skill Semantic State + Campaign observability

Added `SemanticStateStore`, an optional append-only SHA-256 chained JSONL companion containing artifact/evidence/claim/uncertainty references between Skills.

Integrity checks cover tamper, previous-digest mismatch, duplicate IDs, and missing/future/self-parent references.

Campaign integration uses `semantic-state.jsonl` as a workspace companion rather than a `CampaignState` field. **Campaign schema v2 remains unchanged.**

New Campaign projections:

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

Repository-bound Campaigns bind new semantic companion entries to the current TargetSnapshot digest. `resume-context` is a deterministic Resume Capsule with no recommended next action. Replay does not fabricate historical full-state snapshots absent from Campaign v2.

### B4 — Skill Contract Manifests + bounded conformance

Added repository-owned `skill-manifests/` for the first Engineering semantic-alignment slice and all 27 repository-qualified Product Management Skills.

Manifest/domain conformance checks:

```text
required fields and shapes
duplicate IDs / list values
canonical skills/<id>/SKILL.md existence
canonical semantic vocabulary membership
Domain Pack / manifest domain agreement
responsibility coverage
produced-artifact coverage
referenced pack files
```

It explicitly rejects semantic-authority metadata such as `semantic_truth`, `auto_route`, `automatic_skill_selection`, and `automatic_uncertainty_ranking`.

This checker runs **beside**, not instead of, the previously qualified Phase 15 Skill-registry liveness checker.

### B5 — Domain Pack reference architecture

Added:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

These are reference manifests over existing responsibility/capability/artifact/qualification contracts. They do not implement a plugin runtime, ranking system, or semantic router.

The Engineering reference is deliberately bounded. The Product Management reference covers the completed 27-Skill source-methodology migration and preserves its existing maturity policy.

### B6 — Portability and ergonomics

Added Campaign Resume Capsule, exact-reference explanation, transition diff, bounded replay, JSON/Mermaid provenance graph, and deterministic bundle commands:

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles contain exact workspace bytes plus a SHA-256/size manifest. Verification fails closed on unsafe paths, symlink members, duplicate/undeclared/missing members, digest/size mismatch, unsupported format/version, and export destinations inside the source workspace.

Bundle integrity does not establish semantic Campaign correctness.

## Negative / rejection evidence

The milestone includes explicit tests for:

- Python parse incompleteness;
- mixed-target Repository Semantic Map input;
- bounded zero-match exact search;
- semantic-state digest tamper;
- future/missing/self-parent semantic references;
- unknown semantic manifest vocabulary;
- missing canonical Skill file;
- prohibited semantic-authority fields;
- Domain Pack domain/responsibility/artifact mismatch;
- targetless Campaign semantic-state append without explicit target;
- bundle path traversal;
- in-workspace bundle export;
- bundle integrity and safe import boundaries;
- Resume Capsule/replay/graph non-recommendation and non-truth boundaries.

## Exact-head qualification

PR #327 candidate:

```text
1f180cb6a61a060ed9b46b005f0b539b18d21198
```

Required workflows all completed successfully on that exact head:

```text
Product Validation
run: 34471983343
conclusion: success

Release Candidate Distribution
run: 34471983250
conclusion: success

Lab Validation
run: 34471983249
conclusion: success
```

Relevant Product Validation evidence includes:

- Campaign product suites on the supported Python matrix;
- updated installed-wheel smoke proving `semantic_architecture` and Campaign bundle code ship in the core wheel;
- Repository structural validation;
- Canonical Probe Engine gate;
- existing Phase 15 Skill-registry liveness test;
- new Skill Manifest / Domain Pack conformance;
- new semantic substrate / CLI / conformance tests;
- filesystem-security lanes.

Release Candidate Distribution passed build/install/package assertions for the candidate distribution. Lab Validation remained green, preserving the shipped product/lab split.

## Empirical claims deliberately not made

This milestone did **not** run a new real-agent product-value experiment for B1–B6.

Therefore repository qualification does not establish that:

```text
mechanical probes reduce real-agent inspection cost
Repository Semantic Map improves real-agent decisions
semantic companion state improves fresh-context task quality
Resume Capsule reduces tokens in practice
Domain Packs improve cross-harness portability
Campaign bundles improve real operational workflows
```

Those are future empirical questions. The historical Phase 10 evidence applies only to the optional `semantic_reasoning_profile` decision it actually tested.

Likewise:

```text
semantic observation valid != interpretation true
semantic map relation != architecture judgment
semantic state chain valid != referenced claim warranted
manifest valid != Skill should run
Domain Pack membership != support/promotion qualification
provenance graph edge != semantic support
bundle valid != Campaign semantically correct
```

## Build-first policy after this milestone

Mechanical verification remains continuous. Additional empirical experiments are deferred while the next meaningful missing capability can still be justified from existing product/integrity contracts.

Trigger empirical validation when the Construction Diminishing-Returns Gate becomes decision-critical, including persistent competing designs, abstraction without capability, speculative durable fields, formalization outpacing consumption, maintenance dominating capability growth, unresolved placement ambiguity, behavioral-value questions becoming decisive, or semantic-authority pressure.

Completing B1–B6 does **not** itself assert that the gate has been reached.

## What remains intentionally unchanged

- Campaign schema v2 remains the durable Campaign representation baseline.
- `semantic_reasoning_profile` remains optional and outside Campaign artifact admission.
- The Campaign Controller remains non-semantic.
- No central Reasoning Engine exists.
- No automatic uncertainty ranking exists.
- No automatic Skill selection exists.
- No ontology-driven mutation authority exists.
- The existing real-harness qualification verifier remains the authority for frozen external qualification evidence.

## Recommended next-session procedure

1. Read `STATUS.md`, this handoff, and `implementation-plan.md`.
2. Inspect current `main`; do not assume this handoff pins future repository state.
3. Identify a concrete missing product/integrity capability before proposing another semantic abstraction.
4. If the next design is mechanically clear, implement it with negative cases and exact-head qualification.
5. If choosing the next design requires answering whether agents actually benefit from/use the abstraction, declare the Construction Diminishing-Returns Gate reached and switch to empirical validation.
