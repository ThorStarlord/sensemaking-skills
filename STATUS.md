# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** Product Management source-methodology migration complete at repository qualification; Semantic Architecture Phase 10 complete with Outcome A; bounded Phase 15 registry-liveness conformance qualified; post-Phase-10 build-first semantic substrate B1–B6 repository-qualified  
**Primary program:** Sensemaking Campaign productization with agent-agnostic domain capabilities and evidence-governed repository reasoning  
**Current implementation frontier:** use Git `main` HEAD as exact repository identity; this file intentionally does not self-pin a commit that becomes stale when it changes  
**Current semantic frontier:** continue only from a concrete missing product/integrity capability while the Construction Diminishing-Returns Gate remains untriggered; additional empirical experiments are deferred until that gate or an explicit owner decision  
**Current PM frontier:** Waves 1–6 are `REPOSITORY_QUALIFIED`; the pinned 27-command source migration is complete; native-harness/portability qualification remains pending

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. The active coding agent owns semantic judgment. Deterministic machinery owns only mechanically decidable representation, validation, provenance, persistence, integrity, target identity, authority metadata checks, bounded conformance, and reconstructible state.

## Semantic Architecture state

The architecture has four explicit layers:

```text
Semantic Model
  = what entities, relations, and epistemic statuses mean

Reasoning Model
  = how observations become evidence, claims, uncertainty,
    responsibility, capability use, validation, and decisions

Capability / Skill Layer
  = bounded semantic work performed by Skills

Executable Substrate
  = mechanically decidable contracts, probes, validators,
    conformance, Campaign persistence, provenance, observability,
    and portability
```

Formalization remains:

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract / bounded conformance rule
```

Level-1/2 documentation is not runtime authority. Level-3 behavior may enforce only an explicitly documented mechanical subset.

### Phase 9 — complete

PR #318 operationalized the Reasoning Model across `repo-sensemaker`, `architectural-review`, `repair-verifier`, and `output-reconciler`.

The stable shared warrant/provenance core was:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
decision-relevant uncertainty
explicit limits / non-claims
```

Skill-local taxonomies and verdict enums remain local.

Phase 9 introduced `semantic_reasoning_profile` v1. Its validator checks representation and preserves:

```text
semantic_truth_established: false
semantic profile valid != reasoning semantically correct
```

### Phase 10 — complete / Outcome A

PR #323 tested the companion profile in three real-repository reasoning episodes: Chess Mentor Engine, the React incremental game, and ViralFactory PM risk reasoning.

Qualified decision:

> Keep `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**.

Phase 10 found useful cross-artifact/currentness reconstruction value and also meaningful duplication where strong domain artifacts already represented evidence, uncertainty, limits, and currentness. Therefore the profile remains optional and outside Campaign artifact admission.

Phase 10 did **not** authorize mandatory universal embedding, Campaign schema promotion, a central reasoning engine, semantic routing, or semantic truth scoring.

Exact Phase 10 candidate `89258bd77bc2d234f54e03264c68d3c6de7f6de5` passed Product Validation run `34469270069` and Release Candidate Distribution run `34469270281` before PR #323 merged. PR #324 reconciled its handoff.

### Qualified bounded Phase 15 baseline — Skill-registry liveness

PR #325/#326 qualified `scripts/validate-skill-registry-liveness.py` for a narrow mechanically decidable maintenance defect class.

It rejects contradictions such as:

```text
duplicate registry Skill IDs
status: proposed while skills/<id>/SKILL.md exists
explicit no-current-implementation note while that SKILL.md exists
wrong or broken current-canonical skills/<id>/ path
```

The checker preserves `semantic_truth_established: false` and does not establish Skill quality, selection, native-harness support, or promotion.

### Post-Phase-10 build-first substrate — B1–B6 repository-qualified

PR #327 implemented the owner-authorized build-first continuation strategy on top of the qualified Phase 10 and Phase 15 baseline.

Exact candidate head:

```text
1f180cb6a61a060ed9b46b005f0b539b18d21198
```

Exact-head qualification:

```text
Product Validation            run 34471983343  PASS
Release Candidate Distribution run 34471983250  PASS
Lab Validation                run 34471983249  PASS
```

PR #327 merged as `9e1e0356486f16d113ce7e182d2ef00e0110f857`.

The build-first packages are:

#### B1 — Mechanical Semantic Substrate

Shipped package `sensemaking_skills.semantic_architecture` now provides mechanically bounded observations for:

```text
regular-file containment
Python import syntax
supported manifest dependency declarations
exact UTF-8 literal search
```

Every `SemanticObservation` preserves method/source, target ref, evidence refs, scope, completeness, and currentness.

Boundaries remain:

```text
import syntax present != runtime dependency established
import syntax present != architecture violation
dependency declared != dependency used
zero exact matches in bounded UTF-8 scope != universal absence
```

#### B2 — Repository Semantic Map v0

`RepositorySemanticMap` builds only from supplied observations, rejects mixed target refs, records generic `repository_locator` entities and `DERIVED` mechanical relations, and carries explicit incompleteness limits.

It does not infer `Component`, `Layer`, `Boundary`, architecture correctness, importance, or a recommended change.

```text
absence from map != absence from repository
semantic map relation != architecture judgment
```

#### B3 — Cross-Skill Semantic State + Campaign observability

`SemanticStateStore` provides an optional append-only SHA-256 chained companion log containing explicit artifact/evidence/claim/uncertainty references. Reconstruction detects tamper, previous-digest mismatch, duplicate IDs, and missing/future/self-parent references.

Campaigns may carry the companion as `semantic-state.jsonl`. **Campaign schema v2 remains unchanged.** Repository-bound Campaign entries derive their target identity from the current TargetSnapshot digest; targetless Campaigns require an explicit target ref.

New Campaign commands:

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

`resume-context` is a deterministic Resume Capsule. It does not emit a recommended next action. `replay` explicitly refuses to invent historical full-state snapshots not stored by Campaign v2. `graph` renders provenance edges, not semantic causality.

#### B4 — Skill Contract Manifests + bounded conformance

Repository-owned `skill-manifests/` now describe deterministic Skill interfaces: Skill identity, domain, declared responsibilities, canonical input/output identities, shared semantic concepts, and repository-mutation declaration.

The conformance checker runs beside the already-qualified Phase 15 registry-liveness rule and checks:

```text
required fields / shape
duplicate IDs and list values
canonical skills/<id>/SKILL.md existence
canonical semantic vocabulary membership
Domain Pack ↔ manifest domain agreement
responsibility and produced-artifact coverage
referenced pack files
```

Fields that would imply semantic authority are rejected, including `semantic_truth`, `auto_route`, `automatic_skill_selection`, and `automatic_uncertainty_ranking`.

```text
manifest valid != Skill should run
```

#### B5 — Domain Pack reference architecture

Two repository-level reference manifests now exist:

```text
domain-packs/engineering.yaml
domain-packs/product-management.yaml
```

The Engineering pack is deliberately bounded to the first semantic-alignment slice. The Product Management pack references the completed 27-Skill repository-qualified migration and its existing qualification policy.

A Domain Pack groups existing responsibility/capability/artifact/qualification contracts. It is **not** a generic plugin runtime or semantic router.

```text
Domain Pack membership != support/promotion qualification
Domain Pack membership != automatic routing authority
```

#### B6 — Portability and ergonomics

Campaign observability now includes Resume Capsule, exact-reference explanation, transition diff, bounded replay, and JSON/Mermaid provenance graph.

Portable Campaign commands:

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

Bundles preserve exact workspace bytes plus a deterministic SHA-256/size manifest and fail closed on unsafe paths, symlinks, duplicate/undeclared/missing members, digest/size mismatch, unsupported format/version, and export destinations inside the source workspace.

```text
bundle valid != Campaign semantically correct
```

The installed-wheel smoke test proves the semantic substrate and Campaign bundle implementation ship in the core wheel while retained source-only lab packages remain excluded.

### Build-first policy / Construction Diminishing-Returns Gate

The post-Phase-10 owner decision is now canonical in `docs/semantic-architecture/build-first-policy.md`:

> **Build while architecture remains informative. Validate empirically when architecture stops being informative.**

Mechanical verification remains continuous. Additional empirical experiments may be deferred while the next missing capability has a clear mechanical contract.

The diminishing-returns gate becomes decision-critical when construction is dominated by one or more of:

```text
competing architectures not resolvable from existing contracts
abstraction without new capability
speculative durable fields
formalization faster than consumption
maintenance/synchronization burden dominating capability growth
behavioral-value questions becoming decisive
persistent placement ambiguity
pressure to transfer semantic judgment into deterministic machinery
```

Completing B1–B6 does **not** itself mean the gate has been reached.

No new empirical product-value experiment was required to repository-qualify B1–B6. This is a repository implementation/verification claim only; it does not assert that the new layers have already demonstrated real-world agent-work value.

## Product Management source migration — repository complete

All six planned PM waves are `REPOSITORY_QUALIFIED` against pinned upstream `lucasgaravelli/pm-skills-claude-code` commit `21cbb2903d740d10fc65c667aea97d3ee8657349`.

The 27 canonical PM Skills span Customer Discovery, Feature Definition, Strategy/Prioritization, Experimentation/PMF/Pricing, Customer Modeling, and Launch/GTM/Enablement/Communication.

For this migration:

```text
source inventory reconciled: COMPLETE
agent-agnostic canonical adaptation: COMPLETE
artifact/validator integration: COMPLETE where mechanically warranted
Campaign capability registration: COMPLETE
repository qualification: COMPLETE
native-harness qualification: PENDING
portability qualification: PENDING
promotion: PENDING
```

There is no implied Wave 7.

## Empirical qualification gates remain open

### Engineering v0.3 external golden path

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real PASS requires an actual supported external coding-agent harness attempt frozen under the canonical protocol. The **real-harness qualification verifier** can mechanically check a frozen attempt package; it cannot manufacture real-harness origin evidence.

### Product Management native-harness / portability

```text
Checked-in non-qualifying PM preflights: 1
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, connector-side reasoning, Domain Pack membership, and adapter parity do not substitute for real native-harness discovery/invocation when stronger support claims require it.

### Build-first semantic empirical limit

B1–B6 are repository-qualified mechanical/product capabilities. Their Product Validation/Release/Lab PASS does **not** establish that mechanical probes, maps, semantic companion state, Resume Capsules, Domain Packs, or bundles reduce coordination cost in repeated native agent work. Further empirical validation is intentionally deferred until the diminishing-returns gate or explicit owner direction.

## Release architecture continuity

- **Campaign schema v2** remains the durable representation baseline.
- The shipped **product/lab split** remains intact.
- Product Validation owns shipped/installed-product claims.
- Lab Validation owns retained source-only research/lab claims.
- Release Candidate Distribution proves exact candidate build/install/package identities.
- `semantic_reasoning_profile` remains optional and outside Campaign artifact admission.
- Skill-registry liveness and manifest/domain conformance remain bounded repository checks, not semantic routers.
- tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

```text
observation != interpretation
evidence != truth
support != proof
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
semantic profile valid != reasoning semantically correct
registry liveness valid != Skill semantically correct
semantic map relation != architecture judgment
manifest valid != Skill should run
Domain Pack membership != routing authority
provenance edge != semantic support
bundle valid != Campaign semantically correct
repository changed != repair succeeded
document says X != X is current
immutable snapshot evidence != live mutable metadata
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router. The Reasoning Model is not a central semantic controller.

## Current next step

The repository now has a broad mechanically bounded build-first substrate. **Do not interpret the completion of this batch as evidence that construction must stop.**

Choose the next package only from a concrete missing product/integrity capability. If the next meaningful architecture choice cannot be resolved from existing contracts without answering “would agents actually benefit from/use this?”, treat that as the Construction Diminishing-Returns Gate and switch to empirical validation instead of inventing another abstraction.

## Canonical sources

- `STATUS.md` — current cross-program state.
- `docs/semantic-architecture/README.md` — Semantic Architecture index.
- `docs/semantic-architecture/implementation-plan.md` — historical phases + active build-first track.
- `docs/semantic-architecture/build-first-policy.md` — construction authorization and diminishing-returns gate.
- `docs/semantic-architecture/mechanical-semantic-substrate.md` — probes/map/state contracts.
- `docs/semantic-architecture/skill-contract-manifests-and-domain-packs.md` — manifest/domain conformance.
- `docs/semantic-architecture/common-semantic-contract.md` — optional companion semantic profile contract.
- `docs/semantic-architecture/phase-10/results.md` — qualified Phase 10 evidence/Outcome A.
- `docs/semantic-architecture/phase-10-handoff.md` — Phase 10 qualification handoff.
- `docs/semantic-architecture/phase-15/README.md` — bounded registry-liveness pilot.
- `docs/semantic-architecture/phase-15-handoff.md` — Phase 15 liveness qualification evidence.
- `docs/semantic-architecture/build-first-handoff.md` — B1–B6 exact-head qualification handoff.
- `docs/campaign-observability-and-portability.md` — observability/semantic companion/portability commands.
- `docs/product-management/capability-migration-matrix.md` — PM capability maturity ledger.
- `docs/product-management/milestone-handoff.md` — complete six-wave PM source migration handoff.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `qualification-evidence/STATUS.md` — engineering empirical qualification status.
- `docs/sensemaking-campaign.md` — canonical Campaign model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — Lab Validation authority.
- `.github/workflows/release-candidate.yml` — Release Candidate Distribution authority.

When prose and checked-in executable validation disagree, executable behavior is authority for what the software currently enforces; semantic documentation remains authority for intended concept meaning unless superseded by a later ratified decision. Documentation should then be reconciled rather than used to hide the mismatch.
