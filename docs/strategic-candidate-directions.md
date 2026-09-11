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

The repository already distinguishes:

```text
possible direction
!= Strategic Frontier item
!= warranted repository responsibility
!= authorized Campaign/work package
!= implementation commitment
```

The purpose of this file is therefore memory, not prioritization.

A candidate may remain here indefinitely. It should move into current Level-3 state only when natural-use evidence, a mechanically explicit product/integrity/reconstruction need, or explicit owner direction makes it decision-relevant. A candidate that would materially change product purpose, primary user, external product boundary, major non-goals, or public claim ceilings requires Level-4 review under `product-thesis-revision.md`.

This file deliberately does **not** replace:

- `STATUS.md`, which is the current Level-3 operational projection;
- `product-strategy.md`, which is the current Level-4 strategy authority;
- `strategic-outer-loop.md`, which defines the frozen four-level control model;
- ADRs, executable validators, or CI workflows;
- research protocols or empirical evidence records;
- the historical root `roadmap.md`, which remains superseded and unmaintained.

## 2. Candidate lifecycle

Use these dispositions when reconciling an idea against current repository state:

| Disposition | Meaning |
| --- | --- |
| `IMPLEMENTED_BASELINE` | The core idea already exists as current repository-qualified product/support machinery. |
| `PARTIALLY_IMPLEMENTED` | Material pieces exist, but the broader idea still contains unimplemented scope. |
| `CANDIDATE_EXTENSION` | A possible additive extension to an existing capability; not current work. |
| `REQUIRES_EVIDENCE` | Do not promote without a concrete natural-use burden/failure or resumed empirical evidence. |
| `DEFERRED_BY_OWNER_DIRECTION` | Relevant evidence work exists but is currently deferred by explicit owner direction. |
| `LONG_HORIZON` | Strategically interesting, but too broad or insufficiently grounded for current Level-3 work. |
| `REQUIRES_LEVEL_4_REVIEW` | Pursuing the idea may materially change ratified product-thesis commitments. |
| `SUPERSEDED_BY_IMPLEMENTATION` | The original brainstorm has already been overtaken by a broader/current implementation. |
| `REJECTED_FOR_NOW` | Current evidence or architecture argues against pursuing it now. |

None of these dispositions grants execution authority.

Canonical promotion path:

```text
brainstorm / external idea / natural-use observation
        |
        v
Strategic Candidate Directions
        |
        | concrete pressure, repeated burden,
        | mechanically explicit need, or owner direction
        v
Level-3 reassessment
        |
        v
Strategic Frontier
        |
        | one warranted repository-level responsibility
        v
bounded Campaign / work package
        |
        v
implementation + qualification
        |
        v
STATUS.md reconciliation and reassessment
```

For thesis-changing candidates, Level 3 escalates to Level 4 rather than silently promoting the idea.

## 3. Reconciliation snapshot

The candidate inventory below was reconciled against `main` on 2026-09-11 after the first frozen Outer Loop v0 normal-use cycle.

Several ideas that originally appeared as future possibilities are already implemented in the B1-B7 semantic/build-first substrate. In particular, the repository now contains repository-qualified Campaign observability/portability, Resume Capsule, replay, provenance graph, portable bundles, Skill Contract Manifests, Domain Packs, and bounded semantic-reference audit.

The Product Management source migration also progressed beyond the original Wave-2 proposal: all six planned waves and all 27 pinned upstream source capabilities are repository-qualified, while native-harness and portability qualification remain pending.

This document preserves the difference between an **implemented baseline** and a **possible next extension** so future agents do not rebuild existing machinery under a new name.

## 4. Agent ergonomics candidates

### 4.1 Resume Capsule extensions

**Original idea:** make durable Campaign state easy for a fresh agent to consume, optionally under token/context budgets.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign resume-context` is already the deterministic Resume Capsule. It projects mission, current state, target snapshot, responsibility, uncertainty, authority/terminal state, established facts, deferred work, evidence refs, recent transitions, handoff, and semantic companion summary without recommending a next action.

**Possible extensions:**

- deterministic progressive-disclosure / size-budget modes;
- selectively include reference-audit status when natural use shows it materially improves reconstruction;
- explicit machine-readable profile for different consumption contexts, if one repeated consumer need emerges.

**Current missing warrant:** no repeated natural-use evidence shows that Resume Capsule v0 is too large, too small, or missing reference-resolution data in a decision-changing way.

**Reopen trigger:** repeated fresh-context reconstruction burden attributable specifically to the current capsule shape.

**Non-goal:** do not turn the capsule into semantic summarization, next-action recommendation, hidden chain-of-thought reconstruction, or a new Campaign schema merely for presentation.

### 4.2 Campaign inspect / diff / explain ergonomics

**Original idea:** provide read-only observability commands so agents/operators can understand current Campaign state and provenance without manually reading every workspace file.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Repository-qualified commands already include:

```text
campaign inspect
campaign explain --ref
campaign diff
campaign semantic-state
```

**Possible extensions:** only if natural use exposes a missing mechanically decidable projection or a recurring navigation failure.

**Reopen trigger:** repeated inability to reconstruct a mechanically available fact using the existing observability surface.

**Non-goal:** no semantic ranking, recommendation, correctness judgment, or inferred causal explanation.

### 4.3 One-command Campaign preflight

**Idea:** expose a bounded preflight that aggregates existing mechanical checks before consequential Campaign work.

Potential checks might include:

- Campaign/schema integrity;
- target identity/snapshot consistency;
- declared responsibility presence;
- declared capability availability;
- authority metadata sufficiency where mechanically decidable;
- referenced evidence/admission integrity;
- broken lineage/reference diagnostics;
- duplicate transition identifiers or other existing fail-closed conditions.

**Current reconciliation:** `CANDIDATE_EXTENSION` + `REQUIRES_EVIDENCE`.

The repository already has many individual validators, target checks, semantic-reference audit, Campaign validation, and operational qualification commands. It does not currently establish that another aggregator is needed.

**Current missing warrant:** no repeated operator/agent failure shows that manually composing existing checks causes wrong decisions, false closure, or material reconstruction burden.

**Reopen trigger:** repeated natural-use evidence that the same mechanical pre-action checks are assembled incorrectly or omitted across Campaigns.

**Non-goal:** a preflight may say declared mechanical prerequisites pass or fail; it must not conclude that the agent **should proceed**.

### 4.4 Progressive Campaign rigor

**Idea:** allow the same underlying Campaign semantics to support lighter or denser evidence requirements for differently consequential tasks.

Illustrative presentation only:

```text
LIGHT      snapshot + responsibility + transition
STANDARD   + evidence + authority + handoff
QUALIFIED  + exact provenance + qualification receipts
```

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

The repository already has policy/authority concepts and different qualification ceilings, but no current evidence warrants formalizing user-facing rigor tiers.

**Risk:** tiers could accidentally create multiple truth systems or encourage weak evidence merely because a task was labeled "light."

**Reopen trigger:** repeated evidence that the full current ceremony discourages use for otherwise appropriate consequential work, while the same semantic invariants could be preserved with fewer required surfaces.

**Non-goal:** separate incompatible Campaign models.

## 5. Campaign observability and portability candidates

### 5.1 Replay / time-travel extensions

**Original idea:** reconstruct historical Campaign evolution for debugging and decision review.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign replay --at-transition` already reconstructs the trace prefix, state label at the cursor, and cumulative evidence refs. Campaign schema v2 does not store a full historical state snapshot for every transition, so the implementation correctly reports that historic full state was not reconstructed.

**Possible extension:** richer historical reconstruction only if future durable state explicitly stores the necessary information and a concrete consumer need justifies the added persistence cost.

**Reopen trigger:** repeated debugging/review failures caused by information that current v2 transition history genuinely does not preserve.

**Non-goal:** fabricate historical full state from present state.

### 5.2 Provenance graph extensions

**Original idea:** visualize durable Campaign relations as a DAG.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign graph` already emits JSON/Mermaid mechanically established provenance relations among Campaigns, transitions, evidence refs, semantic companion entries, artifacts, and parent relations.

**Possible extensions:** additional edge classes only when existing authoritative identities make them mechanically decidable and a real consumer requires them.

**Reopen trigger:** repeated reconstruction burden around an already-authoritative relation that the graph does not expose.

**Non-goal:** semantic causal graph, architectural truth graph, evidence-support inference, or universal decision graph.

### 5.3 Portable Campaign bundle extensions

**Original idea:** export/import a self-verifying Campaign package across machines and contexts.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Current commands already provide deterministic integrity bundles:

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

The implementation preserves exact workspace bytes, verifies manifest hashes/sizes, rejects unsafe archive members, and keeps transport integrity separate from semantic correctness.

**Possible extensions:** network transport, remote storage, target re-binding, or synchronization only if concrete use demonstrates a need.

**Reopen trigger:** repeated portability failure after bundle verification/import caused by a missing mechanically expressible transport/reconstruction contract.

**Non-goal:** automatically locate or authorize action on a target repository after import.

## 6. Harness interoperability candidates

### 6.1 Harness Conformance / Qualification Kit

**Idea:** reduce operator ceremony around preparing, freezing, and verifying genuine native-harness qualification attempts while leaving semantic execution with the external harness.

Potential shape:

```text
qualification prepare
-> native harness run remains external
-> qualification freeze
-> qualification verify
```

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `DEFERRED_BY_OWNER_DIRECTION`.

The repository already has:

- setup adapters for supported harness discovery roots;
- structural canonical-byte parity tests;
- the engineering external golden-path verifier;
- PM functional/fresh-context/second-harness protocols;
- exact frozen-attempt qualification receipts and claim ceilings.

What remains unproven is native discovery/invocation and product-value/portability behavior in genuine supported harness runs. Additional empirical/native-harness experiments are currently deferred by owner direction.

**Potential value:** make empirical qualification easier to conduct without weakening native-harness independence or turning Sensemaking into the agent runtime.

**Reopen trigger:** owner resumes empirical qualification, or an authorized genuine attempt exposes repeated packaging/freeze/operator errors that a deterministic helper could remove.

**Non-goal:** Sensemaking launching or semantically controlling the external coding agent merely to make qualification easier.

### 6.2 Harness conformance matrix

**Idea:** represent portability evidence by layer rather than a single harness PASS/FAIL label.

Candidate dimensions:

```text
installation
canonical-byte exposure
discovery
invocation
artifact contract
Campaign admission
transition/reconstruction
fresh-context continuation
second-harness portability
```

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `DEFERRED_BY_OWNER_DIRECTION`.

Repository tests already establish installation/representation parity, while native-harness discovery/invocation and second-harness evidence remain open. Existing qualification protocols already preserve many of these distinctions.

**Current missing warrant:** no qualifying corpus exists that demonstrates a recurring reporting/reconstruction problem requiring a new matrix schema.

**Reopen trigger:** multiple authorized native-harness attempts whose results cannot be compared clearly using existing evidence records.

**Non-goal:** collapse semantic usefulness, native invocation, artifact validity, and portability into one numeric compatibility score.

## 7. Domain extensibility candidates

### 7.1 Skill Contract Manifests

**Original idea:** separate a Skill's machine-readable deterministic interface from its semantic methodology.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Repository-owned `skill-manifests/` and semantic conformance already provide the deterministic shell for Skill identity/domain/responsibility/artifact relationships while leaving methodology in the Skill tree.

**Possible extensions:** only from a repeated conformance defect or another mechanically decidable field required by a real consumer.

**Reopen trigger:** repeated mismatch that current manifest/conformance contracts cannot mechanically represent.

**Non-goal:** encode semantic routing, ranking, confidence thresholds, or planner logic in manifests.

### 7.2 Domain Packs

**Original idea:** organize reusable domain-specific responsibility/capability/artifact semantics above the Campaign core.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Domain Pack manifests and conformance are already part of the repository-qualified semantic substrate. Product Management provides a substantial agent-agnostic domain capability set.

**Possible extensions:** new domains or stronger pack contracts only when a concrete domain migration/use case demonstrates stable repeated semantics.

**Reopen trigger:** a second concrete domain or maintenance problem exposes a missing mechanically expressible Domain Pack invariant.

**Non-goal:** treat Domain Pack membership as native-harness qualification, portability qualification, promotion, or semantic appropriateness.

### 7.3 Product Management Wave 2 / additional PM migration

**Original idea:** after Customer Discovery, reconcile and migrate `prd`, `user-stories`, `acceptance-criteria`, and `pre-mortem` as a coherent next wave.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

The repository has already progressed through PM Waves 1-6. All 27 capabilities from the pinned upstream methodology source are repository-qualified. There is no implied Wave 7.

**Future PM expansion candidate:** additional PM capability work should arise from native use, a new explicitly pinned methodological source, maintenance pressure, or owner direction rather than from completing an obsolete migration checklist.

**Reopen trigger:** concrete user/domain evidence that a missing PM responsibility changes a repository/product decision and cannot be addressed by current capabilities.

**Non-goal:** bulk-migrate more commands merely to grow capability count.

## 8. Measurement and research candidates

### 8.1 Sensemaking coordination-overhead observations

**Idea:** understand how much ceremony/reconstruction cost Sensemaking introduces relative to the trust/reliability benefit it provides.

Possible observations include:

- transitions per consequential task;
- artifact rejection/repair loops;
- operator interventions;
- fresh-context reconstruction failures;
- durable-state size;
- time/tokens spent reconstructing state;
- time to first warranted responsibility/action;
- time from implementation to justified closure.

**Current reconciliation:** `REQUIRES_EVIDENCE`.

The repository contains retained research/accounting machinery, but historical/lab mechanisms are not automatically current product instrumentation. Existing owner direction also defers manufacturing new experiments merely to keep the research loop active.

**Reopen trigger:** recurring natural-use complaints or observed burden where coordination cost itself becomes decision-changing.

**Non-goal:** optimize a proxy metric at the expense of evidence quality, or instrument every task by default.

### 8.2 Uncertainty Register

**Idea:** preserve multiple consequential uncertainties and their durable relations without automatically ranking them.

Potential mechanically bounded fields:

```text
uncertainty ID
description
introduced_at
status
dependencies
referenced evidence
resolution record
```

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `REQUIRES_EVIDENCE`.

Campaign state already has active uncertainty semantics, semantic companion entries may reference uncertainties, and normal-use research tracks uncertainty-selection episodes. There is no current warrant for a separate universal uncertainty registry or ranking engine.

**Reopen trigger:** repeated Campaign reconstruction or decision-review failures caused specifically by losing non-active uncertainty identity/history that existing state cannot preserve cleanly.

**Non-goal:** deterministic uncertainty ranking or automatic selection of which uncertainty the agent should resolve next.

### 8.3 Agent-evaluation substrate

**Idea:** use durable Campaign evidence to evaluate engineering judgment, not only final code outcomes.

Possible evaluation questions:

- Was the selected uncertainty decision-changing?
- Was sufficient evidence gathered before action?
- Did the agent exceed authority?
- Were completion claims stronger than evidence?
- Did a fresh agent reconstruct state correctly?
- Did the agent stop appropriately?

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Campaigns already provide useful structured evidence for such analysis, and the research program studies aspects of responsibility/evidence/authority behavior. A general agent-evaluation product is not current product scope.

**Reopen trigger:** a concrete internal/research consumer repeatedly uses Campaign records for evaluation and exposes a stable, mechanically bounded missing interface.

**Potential Level-4 boundary:** turning Sensemaking into a general agent-evaluation platform may materially broaden the product category and should be reviewed before commitment.

**Non-goal:** semantic truth oracle or hidden reasoning capture.

## 9. Integration candidates

### 9.1 GitHub-native Campaign provenance

**Idea:** surface selected Campaign provenance at ordinary engineering boundaries such as pull requests or checks.

Possible generated metadata:

```text
Campaign ID
responsibility
before/after target identity
evidence refs
verification refs
transition ID
```

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

The repository already tracks target identity, evidence, transitions, and exact-head qualification internally. There is no current evidence that publishing those projections to GitHub is required for product value.

**Reopen trigger:** repeated reviewer/operator reconstruction burden at the PR boundary that existing Campaign inspection cannot address efficiently.

**Authority boundary:** generating provenance is distinct from posting comments, creating checks, merging, or otherwise mutating GitHub; external mutation remains separately authorized.

**Non-goal:** imply that a green provenance check semantically proves the change is correct.

### 9.2 Multi-repository Campaigns

**Idea:** allow one Campaign to bind and reason across multiple repository targets for changes that genuinely span repositories.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Current Campaign target identity is intentionally simpler and strongly bound. Multi-target state would multiply identity, atomicity, authority, handoff, and verification complexity.

**Reopen trigger:** repeated real work in which splitting a cross-repository responsibility into bounded single-target Campaigns causes material lost context, false closure, or reconstruction failure.

**Non-goal:** introduce multi-repo complexity solely because cross-repo work is theoretically possible.

## 10. Product-category candidate

### 10.1 Sensemaking as a protocol with multiple implementations

**Idea:** treat Campaign/Capability/Evidence/Authority/Handoff contracts as an implementation-independent protocol, with the Python package as one reference implementation.

Possible long-horizon implementations could include other languages or environments while preserving the same mechanically defined contracts.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW`.

The current product is a Python package plus agent-native Skills and repository contracts. Harness independence is already a strong architectural principle, but implementation independence is not a current product requirement.

**Potential value:** stronger portability, ecosystem interoperability, and separation between semantic contracts and one runtime implementation.

**Current missing warrant:** no repeated consumer requires a non-Python implementation, and no evidence shows that standardizing the protocol is more valuable than continuing to improve the reference product.

**Reopen trigger:** at least one concrete independent implementation/consumer need, or explicit owner strategy direction.

**Level-4 boundary:** making "Sensemaking Protocol" the product category would materially alter positioning/external product boundary and therefore requires thesis review rather than ordinary Level-3 implementation.

**Non-goal:** prematurely freeze unstable implementation details into a public standard.

## 11. Ideas deliberately not promoted by this document

The following may appear elsewhere as possible future directions but remain non-authorized unless current evidence changes:

```text
strategy inspect/diff
Level-3 -> Campaign automation
Level-4 reconciliation automation
StrategicPlanner / OuterLoopEngine
automatic Strategic Frontier ranking
automatic product-thesis revision
universal semantic-reference registry
universal causal/decision graph
new Campaign schema merely for convenience
bulk historical-document deletion
new empirical experiment without owner direction
```

Their presence in this document or another design/history document is not a reason to implement them.

## 12. Candidate review discipline

When reviewing this file during future Level-3 work:

1. Reconcile the candidate against current `main` before assuming it is still missing.
2. Identify the exact current consumer/problem.
3. Ask what consequential decision would improve.
4. Record direct/derived evidence separately from interpretation and hypothesis.
5. Prefer the smallest intervention that addresses the observed boundary.
6. Check whether the candidate is actually Level 3 or requires Level-4 thesis review.
7. Do not promote a candidate simply because it is attractive, old, frequently mentioned, or easy to implement.
8. After implementation, update this file so the original candidate does not remain falsely presented as future work.

Useful promotion test:

```text
repeated useful responsibility or concrete product need
+ stable enough semantics
+ repeated burden/error or explicit owner direction
+ mechanically expressible implementation boundary where applicable
        -> candidate for Level-3 reassessment
```

Even after that test, Level 3 may still choose `NO_CHANGE_WARRANTED`, `DEFERRED`, `OWNER_DECISION_REQUIRED`, or `THESIS_REVIEW_REQUIRED`.

## 13. Current priority statement

This document intentionally declares **no current implementation priority**.

Current operational priority remains whatever `STATUS.md` identifies under the Strategic Frontier and current warranted repository-level responsibility. At the time of this reconciliation, the frozen Outer Loop v0 normal-use closeout found no additional repository-level construction package warranted from a concrete mechanical/reconstruction boundary.

Therefore:

```text
candidate inventory exists
!= repository has pending work
!= candidate ordering is priority
!= absence of current work means product is finished
```

Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.
