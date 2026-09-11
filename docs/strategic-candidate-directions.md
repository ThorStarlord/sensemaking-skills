# Strategic Candidate Directions

**Status:** exploratory / non-authoritative idea reservoir  
**Updated:** 2026-09-11  
**Control level:** input to future Level-3 Strategic Repository Evolution or Level-4 Product Thesis reasoning  
**Authority:** none; candidate ideas do not constitute Strategic Frontier membership, implementation authorization, product-thesis ratification, or release commitment  
**Current strategy authority:** [`product-strategy.md`](product-strategy.md)  
**Current Level-3 state:** [`../STATUS.md`](../STATUS.md)  
**Control model:** [`strategic-outer-loop.md`](strategic-outer-loop.md)

## 1. Purpose

This document preserves strategically interesting ways Sensemaking Skills could evolve without turning brainstorming into a roadmap, backlog, or implementation queue.

```text
possible direction
!= Strategic Frontier item
!= warranted repository responsibility
!= authorized Campaign/work package
!= implementation commitment
```

The purpose of this file is memory, not prioritization. A candidate may remain here indefinitely. It enters current Level-3 state only when concrete pressure, a mechanically explicit product/integrity/reconstruction need, or explicit owner direction makes it decision-relevant. Thesis-changing candidates require Level-4 review.

This file does **not** replace `STATUS.md`, `product-strategy.md`, `strategic-outer-loop.md`, ADRs, executable validators/CI, empirical evidence records, or the historical root `roadmap.md`.

## 2. Candidate lifecycle

| Disposition | Meaning |
| --- | --- |
| `IMPLEMENTED_BASELINE` | Core idea exists as repository-qualified product/support machinery. |
| `PARTIALLY_IMPLEMENTED` | A bounded baseline exists but broader scope remains possible. |
| `CANDIDATE_EXTENSION` | Additive extension; not current work by itself. |
| `REQUIRES_EVIDENCE` | Needs concrete pressure/need or owner direction before promotion. |
| `DEFERRED_BY_OWNER_DIRECTION` | Relevant evidence/research work is explicitly not the current path. |
| `LONG_HORIZON` | Too broad or insufficiently grounded for current Level-3 work. |
| `REQUIRES_LEVEL_4_REVIEW` | May materially change the product thesis/category. |
| `SUPERSEDED_BY_IMPLEMENTATION` | Original brainstorm has been overtaken by current implementation. |
| `REJECTED_FOR_NOW` | Current architecture/evidence argues against pursuing it now. |

None grants execution authority.

```text
idea / observation / owner direction
        ↓
Strategic Candidate Directions
        ↓
Level-3 reassessment
        ↓
Strategic Frontier
        ↓
one explicitly warranted responsibility
        ↓
Campaign / work package
        ↓
implementation + qualification
        ↓
STATUS.md reconciliation
```

## 3. Reconciliation snapshot

As of the second 2026-09-11 owner-directed build-first closeout, the repository has moved substantially beyond the original candidate inventory.

Now repository-qualified baselines include:

- Campaign Preflight, Doctor, observability, replay, local provenance, graph integrity, bundles, and semantic-reference audit;
- Resume Capsule v1 plus v2 progressive-disclosure profiles;
- Capability Context after explicit agent-supplied responsibility classification;
- append-only Uncertainty History and explicit Uncertainty Relationships;
- pre-import Bundle Inspection / Resume / Graph projections;
- Campaign workspace Inventory without prioritization;
- Skill Contract Manifests, Domain Packs, semantic conformance, and `semantic catalog`;
- read-only Level-3 `strategy inspect` / `strategy diff`;
- explicit Level-3→Campaign `strategy handoff`;
- explicit multi-repository target-set identity, per-target authority/role/evidence, drift verification, refresh history, and Campaign Preflight integration.

Campaign schema remains v2. These implementations do not establish native-harness usefulness, portability, comparative superiority, semantic correctness, or automatic planning authority.

## 4. Agent ergonomics candidates

### 4.1 Resume Capsule progressive disclosure

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

`campaign resume-profile --profile minimal|working|audit` now supplies deterministic progressive disclosure. `--max-items` uses tail-preserving bounds with explicit omission counts. The original `campaign resume-context` v1 surface remains backward compatible.

```text
progressive disclosure != semantic summarization
bounded list != evidence ranking
```

**Possible extensions:** only new mechanically deterministic projections required by a concrete consumer.

### 4.2 Campaign inspect / diff / explain / doctor

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

The repository now exposes `campaign inspect`, `explain`, transition `diff`, semantic-state inspection, Doctor, graph, graph-integrity, and provenance rendering.

**Possible extensions:** only mechanically available projections/diagnostics whose absence becomes a concrete problem.

### 4.3 Campaign Preflight

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Preflight composes existing Campaign integrity authorities and now conditionally includes multi-target verification when `multi-targets.json` is present.

```text
preflight PASS != should proceed
```

### 4.4 Progressive Campaign rigor tiers

**Idea:** allow lighter/denser presentation or evidence ceremony while preserving one Campaign truth model.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Potential labels such as LIGHT/STANDARD/QUALIFIED remain illustrative only. The risk is creating multiple truth systems or weakening evidence based on a label.

**Reopen trigger:** explicit owner direction or concrete use showing current ceremony is disproportionate while invariant semantics can stay identical.

**Non-goal:** incompatible Campaign models or weaker truth standards.

## 5. Campaign observability and portability candidates

### 5.1 Replay / historical-state extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Current replay reconstructs only information Campaign v2 actually stores. Richer historical full-state reconstruction would require additional durable information.

**Reopen trigger:** a concrete debugging/review need for history not currently persisted.

**Non-goal:** fabricate old state from current state.

### 5.2 Provenance graph extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Graph rendering/integrity share one `CampaignProvenanceGraphService`. Additional edge classes remain candidates only when mechanically authoritative identities already exist.

**Non-goal:** semantic causality, architectural truth, or universal decision graph.

### 5.3 Bundle inspection and transport extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

In addition to export/verify/import, current commands can inspect a verified bundle and render Resume Capsule/provenance through an ephemeral workspace before durable import.

**Remaining candidates:** network transport, remote storage, synchronization, or explicit target rebinding if separately warranted.

**Non-goal:** automatically authorize import or action on discovered repositories.

### 5.4 Campaign fleet/inventory extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign inventory` enumerates direct child Campaign workspaces and mechanical health without ranking them.

**Possible extension:** deterministic filtering/grouping only if a concrete operator need arises.

**Non-goal:** choose which Campaign should be worked on next.

## 6. Harness interoperability candidates

### 6.1 Harness Conformance / Qualification Kit

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `DEFERRED_BY_OWNER_DIRECTION`.

Setup adapters, canonical-byte parity, frozen-attempt verifiers, and qualification protocols exist. Genuine native discovery/invocation/product-value evidence remains unestablished.

The owner explicitly does not want additional experiments as the current development path.

**Reopen trigger:** owner chooses to pursue stronger native-harness claims or a genuine attempt exposes repeated deterministic packaging/freeze errors.

### 6.2 Harness conformance matrix

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `DEFERRED_BY_OWNER_DIRECTION`.

Layered evidence distinctions already exist conceptually; no new reporting matrix is current work.

**Non-goal:** one numeric compatibility score collapsing installation, invocation, semantic usefulness, and portability.

## 7. Domain extensibility candidates

### 7.1 Skill Contract Manifests / Domain Packs / catalog

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Machine-readable Skill/Domain Pack contracts, aggregate conformance, and read-only catalog inspection are repository-qualified.

**Possible extensions:** new mechanically decidable fields or developer tooling only from a concrete domain/maintenance need or owner direction.

**Non-goal:** semantic routing/ranking encoded in manifests.

### 7.2 Additional domains

**Idea:** add Domain Packs beyond current Engineering/Product Management when a stable domain responsibility set warrants it.

**Current reconciliation:** `CANDIDATE_EXTENSION`.

**Reopen trigger:** explicit owner direction or a concrete domain with stable responsibilities/artifact contracts.

**Non-goal:** grow domain/Skill count for its own sake.

### 7.3 Product Management migration

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

All six planned waves and all 27 capabilities from the pinned source are repository-qualified. There is no implied Wave 7.

## 8. Uncertainty, measurement, and evaluation candidates

### 8.1 Uncertainty lifecycle and relationships

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Current companions preserve lifecycle events and explicit `depends_on`, `blocks_decision`, `introduced_by_transition`, `resolved_by_transition`, and `supersedes` relations.

```text
CampaignState.active_uncertainty = current authority
history / relationship companions = durable authored context
relationship graph != ranking
```

**Possible extensions:** new explicit relation classes only when mechanically bounded and useful.

### 8.2 Coordination-overhead measurement

**Current reconciliation:** `DEFERRED_BY_OWNER_DIRECTION`.

The repository has retained accounting/research machinery, but ordinary development is not to be silently converted into an experiment program.

**Reopen trigger:** explicit owner direction to resume measurement/research.

### 8.3 Agent-evaluation substrate

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW` for a general evaluation product.

Campaign records could support evaluation, but making agent evaluation a first-class product category would broaden current scope.

**Non-goal:** semantic truth oracle or hidden reasoning capture.

## 9. Strategic Outer Loop candidates

### 9.1 Read-only strategy inspect / diff

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

`campaign strategy inspect` projects required Level-3 `STATUS.md` sections/frontier identities and exact source SHA-256. `campaign strategy diff` reports representation changes between explicit status files.

```text
strategy inspect != correct frontier
strategy diff != better strategy
```

### 9.2 Explicit Level-3 → Campaign handoff

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

`campaign strategy handoff` requires an exact caller-selected current frontier item and explicit responsibility/type/authority/scope/success conditions before initializing Campaign v2 state and recording source-status identity.

```text
frontier membership != warranted responsibility
handoff != responsibility selection
```

### 9.3 Level-4 reconciliation automation

**Idea:** mechanically assist reconciliation when product-thesis commitments change.

**Current reconciliation:** `REJECTED_FOR_NOW` + `REQUIRES_LEVEL_4_REVIEW` for any semantic automation.

Read-only/representation tooling may be considered later, but automatic strategy revision, thesis adjudication, or owner-ratification substitution remains outside current authority.

## 10. Integration and scale candidates

### 10.1 GitHub-native Campaign provenance publication

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `LONG_HORIZON` for external mutation.

Local Markdown/JSON provenance rendering exists. Posting comments, checks, PR-description edits, or merges remains separately authorized GitHub mutation.

```text
generate provenance != publish provenance
```

### 10.2 Multi-repository Campaigns

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Multi-Repository Campaigns v1 now supplies explicit target-set companions, per-target identity/role/authority/evidence, live drift verification, explicit refresh history, tamper detection, and preflight integration without changing Campaign schema v2.

**Remaining candidates:** only deeper mechanics justified by concrete cross-repository needs, such as deterministic dependency declarations between already-explicit targets.

```text
multi-target verified != semantic correctness
same Campaign != atomic deployment unit
```

### 10.3 Cross-repository transaction / activation coordination

**Idea:** coordinate atomic commit/deploy/rollback semantics across multiple targets.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Multi-Repository Campaigns v1 intentionally does not promise transaction atomicity. Building a transaction coordinator would substantially increase authority, failure-recovery, deployment, and external-system scope.

**Reopen trigger:** explicit owner direction plus a concrete responsibility whose correctness genuinely depends on atomic cross-repository activation.

**Non-goal:** infer deployment topology from repository membership.

## 11. Ideas deliberately not promoted

These remain non-authorized unless a later Level-3/Level-4 decision explicitly changes their disposition:

```text
Level-4 reconciliation automation
StrategicPlanner / OuterLoopEngine
automatic Strategic Frontier ranking
automatic responsibility selection
automatic capability selection
automatic uncertainty ranking
automatic repository discovery/scope expansion
cross-repository transaction/deployment coordinator
universal semantic-reference registry
universal causal/decision graph
new Campaign schema merely for convenience
bulk historical-document deletion
new empirical experiment without owner direction
```

Completed surfaces such as strategy inspect/diff/handoff and multi-target identity/drift are no longer listed here as missing work.

## 12. Candidate review discipline

When reviewing this file:

1. Reconcile each candidate against current `main` before assuming it is missing.
2. Identify the exact consumer/problem or explicit owner direction.
3. Separate mechanical implementation warrant from stronger empirical claims.
4. Prefer the smallest intervention that preserves existing authority boundaries.
5. Escalate thesis-changing directions to Level 4.
6. Never promote a candidate merely because it is attractive, old, frequently mentioned, or easy to implement.
7. After implementation, reconcile this file so completed work is not rediscovered as future work.

Useful promotion test:

```text
stable enough semantics
+ concrete product/integrity need or explicit owner direction
+ mechanically expressible bounded implementation
+ no silent thesis/authority expansion
        -> candidate for Level-3 reassessment
```

## 13. Current priority statement

This document intentionally declares **no current implementation priority**.

`STATUS.md` is authoritative for the current Level-3 frontier and warranted responsibility. The owner-directed Campaign Usability & Composition, Strategic Outer Loop Ergonomics, and Multi-Repository Campaigns v1 sequence is complete; finishing it does not automatically promote another candidate.

```text
candidate inventory exists
!= repository has pending work
!= candidate ordering is priority
!= absence of current work means product is finished
```

Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.
