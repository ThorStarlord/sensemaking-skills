# Strategic Candidate Directions

**Status:** exploratory / non-authoritative idea reservoir  
**Updated:** 2026-09-11  
**Control level:** input to future Level-3 Strategic Repository Evolution or Level-4 Product Thesis reasoning  
**Authority:** none; candidate ideas do not constitute Strategic Frontier membership, implementation authorization, product-thesis ratification, or release commitment  
**Current strategy authority:** [`product-strategy.md`](product-strategy.md)  
**Current product-boundary authority:** [`adr/0029-current-product-boundary.md`](adr/0029-current-product-boundary.md)  
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

This file does not replace `STATUS.md`, `product-strategy.md`, ADR 0029, `strategic-outer-loop.md`, ADRs, executable validators/CI, empirical evidence records, or historical root `roadmap.md`.

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
Strategic Decision to Support
        ↓
one explicitly warranted responsibility
        ↓
Campaign / work package when useful
        ↓
implementation + qualification
        ↓
STATUS.md reconciliation
```

## 3. Reconciliation snapshot

Repository-qualified/current baselines include:

- Campaign Preflight, Doctor, observability, replay, provenance, bundles, semantic-reference audit, completion receipts, portable rebinding, and explicit multi-repository target/dependency mechanics;
- Resume Capsule v1/v2, capability context, uncertainty lifecycle/relationships, bundle inspection, inventory, and nondestructive archive markers;
- read-only Level-3 strategy inspect/diff and explicit strategy handoff;
- four static agent-facing Campaign golden paths that describe composition without routing or execution;
- bounded shared companion IO for recent locator/relation/completion records;
- Skill Contract Manifests, Domain Packs, semantic conformance, and `semantic catalog`;
- Persona & Adaptive Guidance Model v0 plus shipped-guidance reconciliation;
- **Product Boundary Reconciliation v1**: ADR 0029 supersedes ADR 0014 for current product-scope decisions while ADR 0014 remains historical evidence;
- **Strategic Outer Loop Precision v1**: Strategic Decision to Support, qualitative frontier comparison, smallest-warranted-intervention reasoning, concise current Level-3 state, Thesis Tension, dependency-sensitive Level-4 review hold, mandatory post-review reconciliation, and Level-3/Level-4 Semantic Reasoning Model integration;
- bounded strategic-state mechanics that require/project the Strategic Decision anchor and ADR 0029 pointer without validating strategic quality.

Campaign schema remains v2. None of these baselines establishes native-harness usefulness, empirical portability, comparative superiority, semantic correctness, objective strategic priority, or automatic planning authority.

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
user supervision capability -> scaffolding / explanation
desired delegation -> agent decision ownership within granted authority
decision complexity + consequentiality -> process rigor
continuation complexity -> durability / Campaign value
```

Adaptive Guidance Existing Product Reconciliation v0 found presentation mismatches but no behavior-level mismatch. The shipped guidance now supports direct bounded work, repository sensemaking when responsibility is uncertain, stronger reconciliation/repair verification when consequential, and Campaign state when continuation complexity warrants it.

This weakens rather than strengthens the case for formal runtime tiers: existing mechanics already allow proportional use.

**Reopen trigger:** repeated normal-use evidence that aligned guidance is insufficient because one-model Campaign semantics themselves impose a mechanically bounded recurring burden.

**Non-goals:** incompatible Campaign models, weaker evidence standards, user-expertise scoring, complexity/consequentiality scoring, automatic Campaign thresholds, or deterministic flow selection.

```text
adaptive guidance model != formal Campaign tier system
presentation burden repaired != runtime tier warranted
```

## 5. Campaign portability and lifecycle candidates

### 5.1 Portable target rebinding

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Primary and multi-target paths can be rebound only from caller-supplied locations whose recorded repository identity and exact Git/worktree state match. Primary rebinding preserves canonical Campaign snapshot provenance through a locator companion; multi-target rebinding records explicit history.

```text
rebind valid != repository selected
rebind != target refresh
```

**Remaining candidates:** remote storage/transport, synchronization, or stronger explicit rebinding workflows only if separately warranted.

### 5.2 Bundle transport extensions

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Export/verify/import plus pre-import inspection/resume/graph and target rebinding provide a coherent deterministic transferred-Campaign path.

**Remaining candidates:** network transport/remote storage/synchronization if a concrete need or owner direction warrants them.

### 5.3 Campaign completion and archival

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Terminal Campaigns can produce a recalculable completion receipt bound to durable workspace bytes and an optional nondestructive archive receipt. Inventory can include archived Campaigns explicitly.

```text
completion receipt != semantic success
archive != success
archive != delete/move
```

**Possible extensions:** deterministic retention/index metadata only when a concrete consumer needs it.

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

### 6.2 Cross-repository transaction / activation coordination

**Current reconciliation:** `LONG_HORIZON` + `REQUIRES_EVIDENCE`.

Multi-Repository Campaigns intentionally do not promise atomic commit/deploy/rollback behavior. A transaction coordinator would substantially expand failure-recovery, external-system, and authority scope.

**Reopen trigger:** explicit owner direction plus a concrete responsibility whose correctness genuinely depends on atomic cross-repository activation.

### 6.3 Automatic repository discovery/scope expansion

**Current reconciliation:** `REJECTED_FOR_NOW`.

Current target/rebind workflows deliberately require caller-selected repositories and aliases.

## 7. Domain extensibility candidates

### 7.1 Skill Contract Manifests / Domain Packs / catalog

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

Machine-readable contracts, aggregate conformance, and read-only discovery are repository-qualified.

**Possible extensions:** new mechanically decidable fields or developer tooling only from a concrete domain/maintenance need or owner direction.

### 7.2 Additional domains

**Current reconciliation:** `CANDIDATE_EXTENSION`.

New Domain Packs beyond Engineering/Product Management should arise from explicit owner direction or a concrete domain with stable responsibilities/artifact contracts.

### 7.3 Product Management migration

**Current reconciliation:** `SUPERSEDED_BY_IMPLEMENTATION`.

All six planned waves and all 27 capabilities from the pinned source are repository-qualified. There is no implied Wave 7.

## 8. Measurement, research, and evaluation candidates

### 8.1 Coordination-overhead measurement

**Current reconciliation:** `DEFERRED_BY_OWNER_DIRECTION`.

Retained research/accounting machinery exists, but ordinary repository construction is not to be silently converted into an experiment program.

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

Representation inspection/diff and explicit Level-3→Campaign handoff exist without ranking or responsibility selection. Strategic Outer Loop Precision v1 additionally projects/transports the already-authored **Strategic Decision to Support** while explicitly reporting that the tool did not select it.

### 9.2 Level-4 reconciliation automation

**Current reconciliation:** `REJECTED_FOR_NOW` + `REQUIRES_LEVEL_4_REVIEW` for semantic automation.

Automatic strategy revision, Thesis Tension scoring/aggregation, escalation adjudication, affected-work dependency inference, reconciliation planning, or owner-ratification substitution remains outside current authority.

The current semantic contracts already support dependency-sensitive review holds and mandatory Level-3 reconciliation without requiring an engine.

### 9.3 Strategic Outer Loop Precision v1

**Current reconciliation:** `IMPLEMENTED_BASELINE`.

The milestone established:

- ADR 0029 as current product-boundary authority through an owner-ratified `SUPERSEDE` disposition;
- first-class Strategic Decision to Support;
- qualitative frontier-comparison lenses without scoring;
- smallest-warranted-intervention reasoning;
- concise current `STATUS.md` projection;
- Thesis Tension and Level-3↔Level-4 transition semantics;
- Level-3 and Level-4 instantiations of the Semantic Reasoning Model;
- bounded mechanical enforcement of only the Strategic Decision heading and ADR 0029 pointer.

**Possible extensions:** none are current work. Reopen only from concrete normal-use/integrity/reconstruction pressure or explicit owner direction.

```text
reasoning precision != strategic automation
explicit comparison != priority scoring
```

## 10. Integration and implementation-shape candidates

### 10.1 GitHub-native Campaign provenance publication

**Current reconciliation:** `PARTIALLY_IMPLEMENTED` + `LONG_HORIZON` for external mutation.

Local Markdown/JSON provenance exists. Posting comments, checks, PR-description edits, or merges remains separately authorized GitHub mutation.

```text
generate provenance != publish provenance
```

### 10.2 Companion persistence consolidation

**Current reconciliation:** `IMPLEMENTED_BASELINE` + `CANDIDATE_EXTENSION`.

Recent target-rebind, multi-target-rebind, target-relation, and completion/archive modules share bounded canonical JSON hashing, atomic JSON replacement, and fsync'd JSONL append primitives. Schemas and semantics remain independently owned.

```text
shared IO != shared semantic model
```

**Possible extensions:** migrate another consumer only when duplication creates a concrete maintenance/integrity problem.

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
automatic Strategic Decision selection/scoring
automatic responsibility selection
automatic capability selection
automatic uncertainty ranking
automatic workflow routing/execution
automatic repository discovery/scope expansion
cross-repository transaction/deployment/rollback coordinator
Level-4 reconciliation automation / Thesis Tension scoring
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

Completed surfaces and Strategic Outer Loop Precision v1 are no longer missing work.

## 12. Candidate review discipline

When reviewing this file:

1. Reconcile each candidate against current `main` before assuming it is missing.
2. State the **Strategic Decision to Support** before promoting a boundary.
3. Compare credible boundaries qualitatively; do not infer a numeric priority function.
4. Identify the exact consumer/problem or explicit owner direction.
5. Separate mechanical implementation warrant from stronger empirical claims.
6. Prefer the smallest intervention that preserves existing authority boundaries.
7. Escalate thesis-changing directions to Level 4.
8. Never promote a candidate merely because it is attractive, old, frequently mentioned, or easy to implement.
9. After implementation, reconcile this file so completed work is not rediscovered as future work.

Useful promotion test:

```text
stable enough semantics
+ consequential Strategic Decision to Support
+ concrete product/integrity need or explicit owner direction
+ sufficient current evidence
+ mechanically expressible bounded implementation where mechanics are needed
+ no silent thesis/authority expansion
        -> candidate for Level-3 reassessment
```

## 13. Current priority statement

This document intentionally declares **no current implementation priority**.

`STATUS.md` is authoritative for the current Level-3 frontier, Strategic Decision to Support, and warranted responsibility. Strategic Outer Loop Precision v1 closes with `NO_FURTHER_REPOSITORY_WORK_WARRANTED`; its completion does not automatically promote another candidate.

The remaining directions are either extensions without current consumer pressure, owner-deferred empirical questions, long-horizon scope expansions, or ideas whose automation would violate current semantic/authority boundaries.

```text
candidate inventory exists
!= repository has pending work
!= candidate ordering is priority
!= qualitative lenses are a scoring system
!= future uncertainty is current work
!= absence of current work means product is finished
```

Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.
