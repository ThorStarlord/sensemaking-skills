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
| `REQUIRES_EVIDENCE` | Do not promote without a concrete natural-use burden/failure, mechanically explicit need, or owner direction. |
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

The candidate inventory below was reconciled against `main` on 2026-09-11 after the owner-directed Campaign Productization/Operability/Extensibility sequence.

The repository now contains repository-qualified:

- Campaign observability/portability, Resume Capsule v1, replay, provenance graph, portable bundles, and bounded semantic-reference audit;
- Campaign Preflight v0;
- append-only Uncertainty History v0;
- mechanical Campaign Doctor diagnostics;
- local Campaign provenance rendering and graph-integrity checks;
- Skill Contract Manifests, Domain Packs, semantic conformance, and read-only `semantic catalog` discovery;
- a bounded validator preserving this candidate reservoir's explicit non-authority markers.

The Product Management source migration remains complete across all six planned waves and all 27 pinned upstream source capabilities. Native-harness and portability qualification remain pending and explicitly unestablished.

The 2026-09-11 owner direction changed the **construction gate**, not the evidence ceiling: repository-only/hermetic capabilities may be built from explicit owner direction without a new experiment, while empirical/native-harness claims still require their own evidence.

This document preserves the difference between an **implemented baseline** and a **possible next extension** so future agents do not rebuild existing machinery under a new name.

## 4. Agent ergonomics candidates

### 4.1 Resume Capsule extensions

**Original idea:** make durable Campaign state easy for a fresh agent to consume, optionally under bounded context projections.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign resume-context` is now Resume Capsule v1. The full deterministic projection remains the default; `--compact` provides a smaller stable projection and `--include-preflight` can include bounded Campaign Preflight v0 status. `--recent-transitions` remains the deterministic history bound.

Current v1 still does **not** recommend a next action or use LLM summarization.

**Possible extensions:**

- additional deterministic projection profiles only for a concrete consumer need;
- selectively richer reference-audit details when mechanically available and useful;
- other bounded output-shape controls that do not create a second truth source.

**Reopen trigger:** a concrete reconstruction/consumer need or explicit owner direction that cannot be met cleanly by full/compact v1 projections.

**Non-goal:** semantic summarization, next-action recommendation, hidden chain-of-thought reconstruction, or a new Campaign schema merely for presentation.

### 4.2 Campaign inspect / diff / explain ergonomics

**Original idea:** provide read-only observability commands so agents/operators can understand current Campaign state and provenance without manually reading every workspace file.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Repository-qualified commands already include:

```text
campaign inspect
campaign explain --ref
campaign diff
campaign semantic-state
campaign doctor
```

**Possible extensions:** only when a concrete mechanically decidable projection/diagnostic need is missing.

**Reopen trigger:** repeated or owner-identified inability to reconstruct a mechanically available fact using the existing observability/doctor surfaces.

**Non-goal:** semantic ranking, recommendation, correctness judgment, automatic repair, or inferred causal explanation.

### 4.3 One-command Campaign preflight

**Original idea:** expose a bounded preflight that aggregates existing mechanical checks before consequential Campaign work.

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

`campaign preflight` now composes existing Campaign reconstruction, target binding, evidence/admission, handoff, semantic-reference, authority-metadata, and optional agent-supplied capability-catalog checks.

It deliberately preserves:

```text
preflight PASS != responsibility warranted
preflight PASS != capability semantically appropriate
preflight PASS != native-harness availability
preflight PASS != agent should proceed
```

The responsibility type is never inferred from responsibility prose. When supplied, capability candidates are enumerated without ranking or selection.

**Possible extensions:** additional checks only when an existing authoritative invariant is mechanically decidable and a concrete consumer/owner need justifies adding it.

**Non-goal:** semantic proceed/stop decision, responsibility inference, capability ranking, or automatic repair.

### 4.4 Progressive Campaign rigor

**Idea:** allow the same underlying Campaign semantics to support lighter or denser evidence requirements for differently consequential tasks.

Illustrative presentation only:

```text
LIGHT      snapshot + responsibility + transition
STANDARD   + evidence + authority + handoff
QUALIFIED  + exact provenance + qualification receipts
```

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

The repository already has policy/authority concepts and different qualification ceilings, but no current owner direction or concrete mechanical requirement has authorized user-facing rigor tiers.

**Risk:** tiers could accidentally create multiple truth systems or encourage weak evidence merely because a task was labeled "light."

**Reopen trigger:** explicit owner direction or concrete evidence that the current contract density blocks legitimate use while core semantic invariants can remain unchanged.

**Non-goal:** separate incompatible Campaign truth models.

## 5. Campaign observability and portability candidates

### 5.1 Replay / time-travel extensions

**Original idea:** reconstruct historical Campaign evolution for debugging and decision review.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign replay --at-transition` already reconstructs the trace prefix, state label at the cursor, and cumulative evidence refs. Campaign schema v2 does not store a full historical state snapshot for every transition, so the implementation correctly reports that historic full state was not reconstructed.

**Possible extension:** richer historical reconstruction only if future durable state explicitly stores the necessary information and a concrete need or owner direction justifies the added persistence cost.

**Non-goal:** fabricate historical full state from present state.

### 5.2 Provenance graph extensions

**Original idea:** visualize durable Campaign relations as a DAG.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign graph` emits JSON/Mermaid mechanically established provenance relations. `campaign graph-integrity` now validates the same graph construction for node-ID collisions, duplicate edges, missing endpoints, invalid semantic-reference state, and invalid uncertainty-history state. Both commands consume one `CampaignProvenanceGraphService`, eliminating the earlier duplicate construction path.

**Possible extensions:** additional edge classes only when existing authoritative identities make them mechanically decidable and a concrete consumer requires them.

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

The implementation preserves exact workspace bytes, verifies manifest hashes/sizes, rejects unsafe archive members, and keeps transport integrity separate from semantic correctness. Current additive companion files, including uncertainty history, travel with workspace bytes without changing Campaign schema.

**Possible extensions:** network transport, remote storage, target re-binding, or synchronization only if explicitly warranted.

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

The repository already has setup adapters, structural canonical-byte parity tests, an engineering external golden-path verifier, PM qualification protocols, and frozen-attempt evidence contracts. What remains unproven is native discovery/invocation and product-value/portability behavior in genuine supported harness runs.

The owner explicitly does not want additional experiments as the current construction path, so this remains deferred unless they later choose to pursue stronger native-harness claims.

**Non-goal:** Sensemaking launching or semantically controlling an external coding agent merely to create evidence.

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

Repository tests establish installation/representation parity, while native-harness discovery/invocation and second-harness evidence remain open. No new matrix is needed for the current no-experiment construction program.

**Non-goal:** collapse semantic usefulness, native invocation, artifact validity, and portability into one numeric compatibility score.

## 7. Domain extensibility candidates

### 7.1 Skill Contract Manifests and developer ergonomics

**Original idea:** separate a Skill's machine-readable deterministic interface from its semantic methodology and make that interface easy to inspect.

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Repository-owned `skill-manifests/` and semantic conformance provide the deterministic shell for Skill identity/domain/responsibility/artifact relationships. `semantic catalog` now adds read-only developer discovery/filtering and canonical Skill-path visibility while reusing aggregate conformance rather than creating another validator.

**Possible extensions:** only from a concrete conformance/discovery defect or another mechanically decidable field required by a real consumer/owner direction.

**Non-goal:** encode semantic routing, ranking, confidence thresholds, planner logic, or automatic Skill scaffolding merely for inventory growth.

### 7.2 Domain Packs

**Original idea:** organize reusable domain-specific responsibility/capability/artifact semantics above the Campaign core.

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Domain Pack manifests and conformance are repository-qualified. Product Management supplies a substantial agent-agnostic domain capability set, and `semantic catalog` can inspect/filter Domain Pack metadata without treating pack membership as selection authority.

**Possible extensions:** new domains or stronger pack contracts only when a concrete domain need, mechanically expressible maintenance problem, or explicit owner direction warrants them.

**Non-goal:** treat Domain Pack membership as native-harness qualification, portability qualification, promotion, routing authority, or semantic appropriateness.

### 7.3 Product Management Wave 2 / additional PM migration

**Original idea:** after Customer Discovery, reconcile and migrate `prd`, `user-stories`, `acceptance-criteria`, and `pre-mortem` as a coherent next wave.

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

The repository has already progressed through PM Waves 1-6. All 27 capabilities from the pinned upstream methodology source are repository-qualified. There is no implied Wave 7.

**Future PM expansion candidate:** additional PM capability work should arise from a new explicitly pinned methodological source, concrete maintenance/product need, or owner direction rather than from completing an obsolete migration checklist.

**Non-goal:** bulk-migrate more commands merely to grow capability count.

## 8. Measurement and research candidates

### 8.1 Sensemaking coordination-overhead observations

**Idea:** understand how much ceremony/reconstruction cost Sensemaking introduces relative to the trust/reliability benefit it provides.

Possible observations include transitions per consequential task, artifact rejection/repair loops, operator interventions, fresh-context reconstruction failures, durable-state size, reconstruction cost, time to first warranted responsibility/action, and time from implementation to justified closure.

**Current reconciliation:** `DEFERRED_BY_OWNER_DIRECTION`.

The repository contains retained research/accounting machinery, but the owner explicitly does not want more experiments as the current development path. Existing repository tests are qualification of mechanical contracts, not new product-value experiments.

**Reopen trigger:** explicit owner direction to resume measurement/research or a concrete operational need for already-available accounting data.

**Non-goal:** silently turn ordinary repository development into an experiment program.

### 8.2 Uncertainty Register / history

**Original idea:** preserve multiple consequential uncertainties and their durable lifecycle without automatically ranking them.

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Uncertainty History v0 now persists agent-authored lifecycle events in append-only `uncertainty-history.jsonl`, with stable event/uncertainty IDs, transition/evidence reference validation, supersession shape, and hash-chain integrity. Resume Capsule v1 exposes a bounded summary.

Critically:

```text
CampaignState.active_uncertainty = current authority
uncertainty history = lifecycle companion
history valid != lifecycle judgment semantically correct
history != uncertainty ranking/selection
```

**Possible extension:** richer dependency/relationship fields only if a concrete need or owner direction justifies them without creating a universal ranking engine.

**Non-goal:** deterministic uncertainty ranking or automatic selection of which uncertainty the agent should resolve next.

### 8.3 Agent-evaluation substrate

**Idea:** use durable Campaign evidence to evaluate engineering judgment, not only final code outcomes.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW` for a general evaluation product.

Campaigns provide structured evidence that could support analysis, but a general agent-evaluation platform is not current product scope. The owner has also deferred new experiments.

**Potential Level-4 boundary:** turning Sensemaking into a general agent-evaluation platform materially broadens the product category.

**Non-goal:** semantic truth oracle or hidden reasoning capture.

## 9. Integration candidates

### 9.1 GitHub-native Campaign provenance

**Original idea:** surface selected Campaign provenance at engineering boundaries such as pull requests or checks.

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `LONG_HORIZON` for external publication.

`campaign provenance --format markdown|json` now renders local deterministic Campaign provenance including identity, responsibility metadata, target digests, transitions, evidence refs, preflight state, and uncertainty-history integrity.

The implementation deliberately stops before external mutation:

```text
generate provenance != publish provenance
```

**Remaining candidate:** optional GitHub publication/check integration if separately authorized and concretely useful.

**Authority boundary:** posting comments, editing PR descriptions, creating checks, or merging remain distinct GitHub mutations and are not implied by local rendering.

**Non-goal:** imply that a green provenance representation semantically proves the change is correct.

### 9.2 Multi-repository Campaigns

**Idea:** allow one Campaign to bind and reason across multiple repository targets for changes that genuinely span repositories.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Current Campaign target identity is intentionally simpler and strongly bound. Multi-target state would multiply identity, atomicity, authority, handoff, and verification complexity.

**Reopen trigger:** concrete repeated cross-repository work or explicit owner direction showing that bounded single-target Campaigns cannot represent the responsibility safely.

**Non-goal:** introduce multi-repo complexity solely because cross-repo work is theoretically possible.

### 9.3 Campaign mechanical diagnostics

**Original idea:** expose bounded diagnostics rather than forcing operators to manually map a failed mechanical check to the right inspection surface.

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

`campaign doctor` now consumes Campaign Preflight v0 and maps mechanical failures to deterministic diagnostic classes/inspection commands. It does not mutate the Campaign or select a semantic repair.

```text
doctor finding != repair decision
doctor clean != responsibility warranted
```

**Possible extensions:** additional diagnostic classes only when backed by an existing mechanically authoritative failure mode.

**Non-goal:** automatic semantic repair selection or autonomous execution.

## 10. Product-category candidate

### 10.1 Sensemaking as a protocol with multiple implementations

**Idea:** treat Campaign/Capability/Evidence/Authority/Handoff contracts as an implementation-independent protocol, with the Python package as one reference implementation.

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW`.

The current product is a Python package plus agent-native Skills and repository contracts. Harness independence is already a strong architectural principle, but implementation independence is not a current product requirement.

**Potential value:** stronger portability, ecosystem interoperability, and separation between semantic contracts and one runtime implementation.

**Current missing warrant:** no concrete independent implementation/consumer requires a non-Python implementation, and no owner direction currently changes the product category.

**Level-4 boundary:** making "Sensemaking Protocol" the product category would materially alter positioning/external product boundary.

**Non-goal:** prematurely freeze unstable implementation details into a public standard.

## 11. Ideas deliberately not promoted by this document

The following may appear elsewhere as possible future directions but remain non-authorized unless current evidence/need or owner direction changes:

```text
strategy inspect/diff
Level-3 -> Campaign automation
Level-4 reconciliation automation
StrategicPlanner / OuterLoopEngine
automatic Strategic Frontier ranking
automatic responsibility selection
automatic uncertainty ranking
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
2. Identify the exact current consumer/problem or explicit owner direction.
3. Ask what consequential decision or concrete product capability would improve.
4. Record direct/derived evidence separately from interpretation and hypothesis where evidence is being used.
5. Prefer the smallest intervention that addresses the selected boundary.
6. Check whether the candidate is actually Level 3 or requires Level-4 thesis review.
7. Do not promote a candidate simply because it is attractive, old, frequently mentioned, or easy to implement.
8. Preserve empirical claim ceilings when construction proceeds from owner direction rather than behavioral evidence.
9. After implementation, update this file so the original candidate does not remain falsely presented as future work.

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

Current operational priority remains whatever `STATUS.md` identifies under the Strategic Frontier and current warranted repository-level responsibility. The owner-directed Campaign Productization/Operability/Extensibility sequence is now complete; this reservoir does not automatically promote another candidate merely because the previous sequence finished.

Therefore:

```text
candidate inventory exists
!= repository has pending work
!= candidate ordering is priority
!= absence of current work means product is finished
```

Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.
