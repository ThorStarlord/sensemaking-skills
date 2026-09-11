# Build-First Semantic Substrate Handoff

**Milestone:** Post-Phase-10 build-first Semantic Architecture B1–B7  
**Status:** REPOSITORY_QUALIFIED  
**B1–B6 implementation PR:** #327  
**B7 implementation PR:** #330  
**B1–B6 qualified candidate head:** `1f180cb6a61a060ed9b46b005f0b539b18d21198`  
**B7 qualified candidate head:** `8369d750c893f143830db6ccc69c8fa80d321dd4`  
**B1–B6 merge commit:** `9e1e0356486f16d113ce7e182d2ef00e0110f857`  
**B7 merge commit:** `6203be05636b12e012a87940429041ff24af821d`  
**Date:** 2026-09-11

## Why this milestone exists

Phase 10 had already selected Outcome A: keep `semantic_reasoning_profile` v1 as an optional companion audit/reconstruction artifact. A later owner decision changed the *prospective* development strategy: continue building while concrete mechanically bounded capabilities remain obvious, and defer **additional** empirical experiments until construction hits diminishing returns or a consequential architecture choice becomes evidence-dependent.

B1–B6 implemented the first broad build-first substrate. B7 followed as one separately preflighted integrity package after the repository exposed a mechanically decidable reference-resolution gap in the optional semantic companion. B7 did not reopen or rewrite the historical Phase 10 result.

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

### B7 — Semantic Reference Resolution & Integrity Audit v0

B7 was authorized by `b7-semantic-reference-audit-design-preflight.md` only after the preflight established that Campaign evidence/admission state provides at least one meaningful non-parent reference family that can be resolved without inventing a universal namespace.

Added standalone `sensemaking_skills.semantic_architecture.reference_audit` mechanics and Campaign rendering through:

```text
campaign semantic-state
campaign explain --ref <exact-ref>
```

The audit separates:

```text
resolution       = resolved | dangling | ambiguous | not_addressable
reference class  = campaign_internal | legacy_opaque | unknown
integrity effect = pass | fail | informational
```

`AMBIGUOUS` remains reserved but is not emitted by B7 v0 because existing authoritative resolvers do not produce multiple valid matches.

B7 reuses existing Campaign evidence/admission authority. It does not create a second evidence registry. Current resolution is bounded to identities already represented by the repository, including Campaign evidence/admitted artifacts, existing semantic-entry parent identities, exact current active uncertainty identity where available, and target binding without currentness inference.

Opaque legacy/claim/profile refs remain `not_addressable` when the repository has no authoritative resolver. This preserves:

```text
not_addressable != invalid
resolved != current
reference occurrence != reference resolution
reference resolution != semantic support
```

B7 leaves `SemanticStateStore.validate()` focused on structural/hash-chain integrity and does not change Resume Capsule behavior or Campaign schema v2.

## Negative / rejection evidence

The build-first track includes explicit tests for:

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
- Resume Capsule/replay/graph non-recommendation and non-truth boundaries;
- resolved raw Campaign evidence;
- resolved admitted artifact identity;
- dangling established Campaign-internal evidence/artifact refs;
- opaque legacy and claim refs remaining `not_addressable`/informational;
- exact current uncertainty resolution only where Campaign state establishes it;
- corrupt semantic-state chain refusing trustworthy outbound audit;
- no Campaign resolver context causing no filesystem guessing;
- reference resolution never becoming semantic support, relevance, currentness, or truth.

## Exact-head qualification

### B1–B6 — PR #327

Candidate:

```text
1f180cb6a61a060ed9b46b005f0b539b18d21198
```

Required workflows completed successfully:

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

### B7 — PR #330

Candidate:

```text
8369d750c893f143830db6ccc69c8fa80d321dd4
```

Required workflows completed successfully on that exact head before merge:

```text
Product Validation
run: 34565797654
conclusion: success

Release Candidate Distribution
run: 34565797661
conclusion: success

Lab Validation
run: 34565797689
conclusion: success
```

Relevant Product Validation evidence across the track includes Campaign product suites on the supported Python matrix, installed-wheel smoke, repository structural validation, the Canonical Probe Engine gate, Phase 15 Skill-registry liveness, Skill Manifest / Domain Pack conformance, semantic substrate/audit tests, Campaign integration tests, and filesystem-security lanes.

Release Candidate Distribution passed build/install/package assertions for both qualified candidate states. Lab Validation remained green, preserving the shipped product/lab split.

## Empirical claims deliberately not made

The build-first track did **not** run a new real-agent product-value experiment for B1–B7.

Therefore repository qualification does not establish that:

```text
mechanical probes reduce real-agent inspection cost
Repository Semantic Map improves real-agent decisions
semantic companion state improves fresh-context task quality
Resume Capsule reduces tokens in practice
Domain Packs improve cross-harness portability
Campaign bundles improve real operational workflows
semantic-reference audit improves agent decision quality or operator usefulness
```

Those are empirical questions, not implied by repository qualification. The historical Phase 10 evidence applies only to the optional `semantic_reasoning_profile` decision it actually tested.

Likewise:

```text
semantic observation valid != interpretation true
semantic map relation != architecture judgment
semantic state chain valid != referenced claim warranted
reference audit pass != semantic truth
reference resolved != current
manifest valid != Skill should run
Domain Pack membership != support/promotion qualification
provenance graph edge != semantic support
bundle valid != Campaign semantically correct
```

## Build-first policy after B7

Mechanical verification remains continuous. The B7 preflight explicitly required a fresh reassessment after B7 rather than assuming a B8/B9 queue.

Additional empirical experiments remain deferred by owner direction. Further construction is warranted only when another concrete product/integrity/reconstruction boundary can be specified mechanically from current authoritative state without semantic ranking, automatic routing, speculative universal identities, or unmeasured product-value assumptions.

Trigger the Construction Diminishing-Returns Gate when construction is dominated by persistent competing designs, abstraction without capability, speculative durable fields, formalization outpacing consumption, maintenance dominating capability growth, unresolved placement ambiguity, behavioral-value questions becoming decisive, or pressure to transfer semantic judgment into deterministic machinery.

Completing B1–B7 does **not** itself assert that the gate has been reached.

## What remains intentionally unchanged

- Campaign schema v2 remains the durable Campaign representation baseline.
- `semantic_reasoning_profile` remains optional and outside Campaign artifact admission.
- The Campaign Controller remains non-semantic.
- No central Reasoning Engine exists.
- No universal semantic reference registry exists.
- No automatic uncertainty ranking exists.
- No automatic Skill selection exists.
- No ontology-driven mutation authority exists.
- Reference resolution does not imply currentness or semantic support.
- The existing real-harness qualification verifier remains the authority for frozen external qualification evidence.

## Recommended next-session procedure

1. Read `STATUS.md`, this handoff, `b7-semantic-reference-audit-design-preflight.md`, and `implementation-plan.md`.
2. Inspect current `main`; do not assume this handoff pins future repository state.
3. Reassess from zero after B7: identify a concrete missing product/integrity/reconstruction capability before proposing another abstraction.
4. If a next design is mechanically clear, give it its own bounded preflight, negative cases, exact-head qualification, and stop condition.
5. If choosing the next design requires answering whether agents actually benefit from/use the abstraction, declare the Construction Diminishing-Returns Gate reached rather than inventing another package.
