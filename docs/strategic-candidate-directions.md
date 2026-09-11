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

The purpose is memory, not prioritization. A candidate enters current Level-3 state only when concrete pressure, a mechanically explicit need, or explicit owner direction makes it decision-relevant. Thesis-changing candidates require Level-4 review.

This file does not replace `STATUS.md`, `product-strategy.md`, `strategic-outer-loop.md`, ADRs, executable validators/CI, empirical evidence records, or historical root `roadmap.md`.

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

Repository-qualified baselines include:

- Campaign Preflight, Doctor, observability, replay, provenance, bundles, semantic-reference audit, and completion receipts;
- Resume Capsule v1/v2, capability context, uncertainty lifecycle/relationships, bundle inspection, inventory, and nondestructive archive markers;
- read-only Level-3 strategy inspect/diff and explicit strategy handoff;
- explicit multi-repository target identity, drift verification, refresh, portable rebinding, and caller-authored cross-repository relationships;
- four static agent-facing Campaign golden paths that describe composition without routing or execution;
- bounded shared companion IO for recent locator/relation/completion records;
- Skill Contract Manifests, Domain Packs, semantic conformance, and `semantic catalog`.

The owner-ratified Persona & Adaptive Guidance Model v0 clarifies the primary design persona and five contextual reasoning factors: user supervision capability, desired delegation, decision complexity, consequentiality, and continuation complexity. Adaptive Guidance Existing Product Reconciliation v0 subsequently aligned the shipped `using-sensemaking` Skill, public onboarding, Campaign product framing, and Golden Path references with that model without changing runtime semantics.

Campaign schema remains v2. None of these baselines establishes native-harness usefulness, empirical portability, comparative superiority, semantic correctness, or automatic planning authority.

## 4. Agent ergonomics candidates

### 4.1 Resume and workflow navigation

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

`campaign resume-profile --profile minimal|working|audit` provides deterministic progressive disclosure. `campaign workflow list/show` exposes static single-repository, fresh-context, transferred-Campaign, and multi-repository composition paths with explicit decision gates.

```text
progressive disclosure != semantic summarization
golden path != workflow engine
flow shown != flow recommended
```

**Possible extensions:** only additional deterministic projections/static paths required by a concrete consumer.

**Non-goal:** adaptive semantic routing, workflow execution, responsibility selection, or recommendation.

### 4.2 Campaign inspect / explain / Doctor / preflight

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

Current mechanical observability includes `inspect`, `explain`, `diff`, semantic-state, graph, graph-integrity, Doctor, preflight, completion receipt verification, and target/dependency checks.

**Possible extensions:** only concrete missing mechanically decidable diagnostics.

### 4.3 Progressive Campaign rigor tiers

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

The Persona & Adaptive Guidance Model v0 supplies the conceptual reason that process ceremony may vary without creating multiple truth systems:

```text
user supervision capability
-> scaffolding / explanation

desired delegation
-> agent decision ownership within granted authority

decision complexity + consequentiality
-> process rigor

continuation complexity
-> durability / Campaign value
```

Adaptive Guidance Existing Product Reconciliation v0 then tested this interpretation against the shipped product. Its audit found **presentation mismatches but no behavior-level mismatch**. The shipped guidance now explicitly supports:

```text
clear/local/one-context work
-> bounded work without Campaign ceremony

uncertain repository responsibility
-> repository sensemaking when useful

consequential claim / repair
-> stronger reconciliation or finding-specific verification when warranted

continuation-heavy work
-> durable Campaign state
```

This currently weakens rather than strengthens the case for formal runtime tiers: existing mechanics already allow proportional use, and the observed burden was resolved through agent/user guidance rather than alternate Campaign semantics.

Potential `LIGHT` / `STANDARD` / `QUALIFIED` presentation remains illustrative only. The risk is creating multiple truth systems, weakening evidence because of a label, or turning contextual semantic judgment into a routing threshold.

**Reopen trigger:** repeated normal-use evidence that aligned guidance is insufficient because the existing one-model Campaign semantics themselves (a) mechanically impose avoidable ceremony on otherwise appropriate work, or (b) cannot express a recurring mechanically bounded continuation/qualification profile without manual reconstruction.

**Non-goals:** incompatible Campaign models, weaker truth/evidence standards, user-expertise scoring, complexity/consequentiality scoring, automatic Campaign thresholds, or deterministic flow selection.

```text
adaptive guidance model
!= formal Campaign tier system
presentation burden repaired
!= runtime tier warranted
```

## 5. Campaign portability and lifecycle candidates

### 5.1 Portable target rebinding

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Primary and multi-target paths can now be rebound only from caller-supplied locations whose recorded repository identity and exact Git/worktree state match. Primary rebinding preserves canonical Campaign snapshot provenance through a locator companion; multi-target rebinding records an explicit rebind history.

```text
rebind valid != repository selected
rebind != target refresh
```

**Remaining candidates:** remote storage/transport, synchronization, or stronger explicit target-rebinding workflows only if separately warranted.

**Non-goal:** repository discovery or silently accepting drift.

### 5.2 Bundle transport extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Export/verify/import plus pre-import inspection/resume/graph and target rebinding provide a coherent deterministic transferred-Campaign path.

**Remaining candidates:** network transport/remote storage/synchronization if a concrete need or owner direction warrants them.

### 5.3 Campaign completion and archival

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Terminal Campaigns can produce a recalculable `completion-receipt.json` bound to durable workspace bytes and an optional nondestructive `archive-receipt.json`. Inventory hides valid archived Campaigns by default and can include them explicitly.

```text
completion receipt != semantic success
archive != success
archive != delete/move
```

**Possible extensions:** deterministic archival/export indexing or retention metadata only when a concrete consumer needs them.

**Non-goal:** automatic terminal decisions, success inference, or destructive archival.

### 5.4 Replay / richer historical-state reconstruction

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Current replay reconstructs only information schema v2 actually stores. Richer historical state remains a candidate only if future durable persistence explicitly contains the needed data.

**Non-goal:** fabricate past state from present state.

## 6. Multi-repository candidates

### 6.1 Target sets and explicit cross-repository relationships

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Current machinery supports explicit target aliases/roles/authority/evidence, exact target-set identity, live drift verification, refresh/rebind history, and caller-authored relations:

```text
depends_on
provides_interface_to
consumes_interface_from
must_change_with
release_after
```

Only explicit ordering relations participate in cycle rejection. Sensemaking does not infer relationships or work order.

```text
relationship recorded != architectural truth
dependency graph valid != execution plan correct
```

**Possible extensions:** additional explicit relation classes or deterministic filters only from a concrete need.

### 6.2 Cross-repository transaction / activation coordination

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Multi-Repository Campaigns intentionally do not promise atomic commit/deploy/rollback behavior. A transaction coordinator would substantially expand failure-recovery, external-system, and authority scope.

**Reopen trigger:** explicit owner direction plus a concrete responsibility whose correctness genuinely depends on atomic cross-repository activation.

**Non-goal:** infer deployment topology from repository membership or relation records.

### 6.3 Automatic repository discovery/scope expansion

**Current reconciliation:** `REJECTED_FOR_NOW`.

Current target/rebind workflows deliberately require caller-selected repositories and aliases.

**Non-goal:** search a machine/organization and silently decide which repositories belong to a Campaign.

## 7. Domain extensibility candidates

### 7.1 Skill Contract Manifests / Domain Packs / catalog

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Machine-readable contracts, aggregate conformance, and read-only discovery are repository-qualified.

**Possible extensions:** new mechanically decidable fields or developer tooling only from a concrete domain/maintenance need or owner direction.

### 7.2 Additional domains

**Current reconciliation:** `CANDIDATE_EXTENSION`.

New Domain Packs beyond Engineering/Product Management should arise from explicit owner direction or a concrete domain with stable responsibilities/artifact contracts.

**Non-goal:** grow Skill/Domain counts for their own sake.

### 7.3 Product Management migration

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

All six planned waves and all 27 capabilities from the pinned source are repository-qualified. There is no implied Wave 7.

## 8. Measurement, research, and evaluation candidates

### 8.1 Coordination-overhead measurement

**Current reconciliation:** `DEFERRED_BY_OWNER_DIRECTION`.

Retained research/accounting machinery exists, but ordinary repository construction is not to be silently converted into an experiment program.

The adaptive-guidance reinterpretation makes coordination overhead more interpretable: visible ceremony should not scale merely because the user is less expert, while durable machinery should earn its cost from decision/consequentiality/continuation pressure. That is a product hypothesis, not measured evidence.

**Reopen trigger:** explicit owner direction to resume measurement/research.

### 8.2 Harness Conformance / portability evidence

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `DEFERRED_BY_OWNER_DIRECTION`.

Setup adapters, canonical-byte parity, qualification protocols, and real-harness verifier machinery exist. Genuine native discovery/invocation and second-harness product evidence remain unestablished.

Portable target rebinding is repository-qualified transport mechanics; it is **not** empirical proof of native-harness portability.

### 8.3 Agent-evaluation substrate

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW` for a general evaluation product.

Campaign records could support evaluation, but making agent evaluation a first-class product category would broaden current scope.

**Non-goal:** semantic truth oracle or hidden reasoning capture.

## 9. Strategic Outer Loop candidates

### 9.1 Strategy inspect / diff / explicit handoff

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Representation inspection/diff and explicit Level-3→Campaign handoff exist without ranking or responsibility selection.

### 9.2 Level-4 reconciliation automation

**Current reconciliation:** `REJECTED_FOR_NOW` + `REQUIRES_LEVEL_4_REVIEW` for semantic automation.

Automatic strategy revision, thesis adjudication, or owner-ratification substitution remains outside current authority.

## 10. Integration and implementation-shape candidates

### 10.1 GitHub-native Campaign provenance publication

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `LONG_HORIZON` for external mutation.

Local Markdown/JSON provenance exists. Posting comments, checks, PR-description edits, or merges remains separately authorized GitHub mutation.

```text
generate provenance != publish provenance
```

### 10.2 Companion persistence consolidation

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Recent target-rebind, multi-target-rebind, target-relation, and completion/archive modules share a bounded `companion_io.py` for canonical JSON hashing, atomic JSON replacement, and fsync'd JSONL append.

The schemas and semantics remain independently owned.

```text
shared IO != shared semantic model
```

**Possible extensions:** migrate another persistence consumer only when duplication creates a concrete maintenance/integrity problem. Do not bulk-consolidate Semantic Architecture merely for stylistic consistency.

### 10.3 Sensemaking as an implementation-independent protocol

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_LEVEL_4_REVIEW`.

Harness independence remains an architectural principle, but implementation independence is not a current product requirement.

**Reopen trigger:** a concrete independent implementation/consumer need or explicit owner strategy direction.

**Non-goal:** prematurely freeze current Python implementation details into a public standard.

## 11. Ideas deliberately not promoted

These remain non-authorized unless a later Level-3/Level-4 decision explicitly changes their disposition:

```text
StrategicPlanner / OuterLoopEngine
automatic Strategic Frontier ranking
automatic responsibility selection
automatic capability selection
automatic uncertainty ranking
automatic workflow routing/execution
automatic repository discovery/scope expansion
cross-repository transaction/deployment/rollback coordinator
Level-4 reconciliation automation
universal semantic-reference registry
universal causal/decision graph
Sensemaking Protocol product-category pivot
Campaign schema v3 merely for convenience
user expertise / task complexity / consequentiality scoring
automatic persona inference or beginner/expert runtime modes
automatic Campaign rigor thresholds
bulk historical-document deletion
new empirical experiment without owner direction
```

Completed surfaces such as target rebinding, dependency declarations, completion/archive, static golden paths, and adaptive-guidance presentation alignment are no longer listed as missing work.

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

`STATUS.md` is authoritative for the current Level-3 frontier and warranted responsibility. The owner-directed Portable Target Rebinding, Cross-Repository Dependency Declarations, Campaign Completion & Archival, Agent Workflow / Golden Path, Surface Simplification & Contract Consolidation, Persona & Adaptive Guidance Model v0, and Adaptive Guidance Existing Product Reconciliation v0 work do not automatically promote another candidate.

The latest reconciliation specifically found no behavior-level defect requiring formal Campaign tiers: the observed proportionality mismatch was in shipped guidance and was repaired there.

```text
candidate inventory exists
!= repository has pending work
!= candidate ordering is priority
!= adaptive product model requires adaptive runtime
!= aligned guidance requires a rigor-mode system
!= absence of current work means product is finished
```

Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.
