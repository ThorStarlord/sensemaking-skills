# Idea Library v1: Product Possibility Landscape

**Status:** exploratory / non-authoritative possibility landscape; first curated selection (16 possibilities)  
**Assessed:** 2026-10-28 at `main@d0af33beb52e94b375d6a471e9990df11c8c424d`  
**Authority:** none. A possibility, its dimension labels or its relationships here are not Strategic Frontier membership, priority, implementation authorization, owner decisions or ADR ratification.  
**Conceptual model:** [`semantic-architecture/product-possibility-ontology.md`](semantic-architecture/product-possibility-ontology.md)  
**Source reservoir:** [`strategic-candidate-directions.md`](strategic-candidate-directions.md)  
**Governing sources:** [`product-strategy.md`](product-strategy.md), [ADR 0031](adr/0031-persistent-semantic-stewardship.md), [ADR 0029](adr/0029-current-product-boundary.md), [`../STATUS.md`](../STATUS.md)  
**Program plan:** [`superpowers/plans/2026-10-28-product-possibility-idea-library.md`](superpowers/plans/2026-10-28-product-possibility-idea-library.md)

```text
retained possibility
!= Strategic Frontier item
!= selected responsibility
!= implementation commitment
```

## 1. How to read this library

Each entry gives a stable `poss:` identifier, the proposed future, its origin, the five dimensions of the conceptual model (alignment, ambition, realization, disposition; epistemic status is marked on individual claims), the disposition history with reasons and `revisit_when`, and its relationships.

**One record of origin per disposition.** When a possibility comes from a source that already records its disposition (the reservoir, an ADR, a strategic analysis), that source remains the record of origin. This library cites it as of the assessed revision and adds identity, separated dimensions and relationships. If the two disagree, the origin governs and this entry is stale. Possibilities that originate in a conversation, a plan or a synthesis have their record of origin here.

**Coverage.** This is a deliberate selection, not a conversion of the reservoir. Reservoir entries not listed are `NOT_ASSESSED` here, not rejected. Realization claims cite the sources inspected at the assessed revision; a lexical search that found nothing is labelled as such and is not a complete absence proof.

## 2. Landscape at a glance

| ID | Possibility | Alignment | Ambition | Realization | Latest disposition |
| --- | --- | --- | --- | --- | --- |
| `poss:persistent-semantic-stewardship` | Persistent semantic stewardship (ADR 0031 destination) | ALIGNED | TRANSFORMATIVE | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-15 |
| `poss:git-authored-knowledge-index` | Git-reviewed knowledge with a rebuildable index | ALIGNED | SUBSTANTIAL | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:path-scoped-architecture-vocabulary` | Architecture and ontology vocabulary v2 | ALIGNED | INCREMENTAL | IMPLEMENTED_BASELINE | SELECTED for construction; ADR 0033 PROPOSED |
| `poss:strategic-exploration-funnel` | Coverage-before-convergence exploration | ALIGNED | INCREMENTAL | IMPLEMENTED_BASELINE (guidance) | SELECTED (integrated) |
| `poss:strategic-continuity-reassessment` | Assumptions and reassessment triggers for strategic paths | ALIGNED | INCREMENTAL | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:possibility-memory` | Product possibility memory (this library) | ALIGNED | SUBSTANTIAL | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-28, first increment only |
| `poss:cross-episode-possibility-synthesis` | Cross-episode possibility synthesis | ADJACENT | SUBSTANTIAL | NOT_IMPLEMENTED | EXPLORATORY |
| `poss:possibility-reconsideration-from-change` | Reconsideration from indexed change (new synthesis) | ALIGNED | INCREMENTAL | NOT_IMPLEMENTED | EXPLORATORY |
| `poss:product-core-bootstrap` | Bounded product-core BOOTSTRAP first (PATH-2) | ALIGNED | INCREMENTAL | NOT_IMPLEMENTED as a path | DEFERRED; reconsidered 2026-10-28, NO_CHANGE |
| `poss:s5-evidence-first` | Independent-session evidence before more construction | ALIGNED | INCREMENTAL | NOT_IMPLEMENTED | REJECTED_FOR_NOW as a path |
| `poss:capability-learning-analysis` | Cross-episode capability learning Skill | ADJACENT | SUBSTANTIAL | NOT_IMPLEMENTED | DEFERRED (evidence-gated) |
| `poss:cross-product-transfer` | Stewardship across products and repositories (S6) | ALIGNED | LONG_HORIZON | NOT_IMPLEMENTED | DEFERRED (needs S5 evidence) |
| `poss:domain-general-sensemaking` | Domain-general Sensemaking control | COUNTERFACTUAL | LONG_HORIZON | NOT_IMPLEMENTED | EXPLORATORY (research hypothesis) |
| `poss:automatic-strategic-planner` | Deterministic strategic planner and frontier ranking | CONFLICTS_WITH_CURRENT_STRATEGY | TRANSFORMATIVE | NOT_IMPLEMENTED | REJECTED_FOR_NOW |
| `poss:ranked-possibility-backlog` | The Idea Library as a ranked backlog | CONFLICTS_WITH_CURRENT_STRATEGY | SUBSTANTIAL | NOT_IMPLEMENTED | REJECTED_FOR_NOW |
| `poss:cross-repository-transaction-coordinator` | Cross-repository transaction coordination | CONFLICTS_WITH_CURRENT_STRATEGY | LONG_HORIZON | NOT_IMPLEMENTED | DEFERRED |

Order is grouping (realized, aligned future, deferred, long-horizon, conflicting), not priority.

## 3. Possibilities

### 3.1 Realized and partially realized

#### `poss:persistent-semantic-stewardship`: persistent semantic stewardship

- **Proposed future:** Sensemaking becomes a persistent, typed, queryable, provenance-aware knowledge system operated through Skills, improving how agents understand and evolve software "across tasks, agents, repositories, and time".
- **Origin:** the owner's Path 3 choice, recorded in ADR 0031 decision 1 (`docs/adr/0031-persistent-semantic-stewardship.md:32`).
- **Objective:** `goal:compounding-product-knowledge`, `goal:longterm-stewardship`.
- **Value hypothesis (HYPOTHESIZED):** better decisions in later, genuinely separate engineering episodes (ADR 0031, "Success and failure conditions"). Not demonstrated.
- **Realization (OBSERVED):** S1–S3 foundation integrated and S4 Skill guidance in source; S5 independent-agent learning and S6 cross-product transfer not qualified (`STATUS.md:58`).
- **Disposition history:**
  - Earlier (date not recorded in ADR 0031): treated as "merely an optional later optimization", in effect `DEFERRED`.
  - 2026-10-15, owner, `SELECTED`: the earlier conclusion is superseded "as a strategic choice" and was "not a negative empirical verdict" (ADR 0031:25-27).
- **Why it is here:** an earlier deferral reversed by an owner choice rather than by new evidence. Both assessments stay visible (CQ-083).

#### `poss:git-authored-knowledge-index`: Git-reviewed knowledge with a rebuildable index

- **Proposed future:** reviewed, source-pinned typed claims and relations authored in Git, indexed into a local rebuildable SQLite database, and read through bounded, provenance-preserving queries.
- **Origin:** ADR 0031 decision 7; stewardship plan section 14, packages S1–S3 (`docs/persistent-semantic-stewardship-plan.md:459`).
- **Realization (OBSERVED):** `src/sensemaking_skills/semantic_architecture/knowledge.py` (claims, relations, authored-record parsing); `knowledge_store.py` ("Rebuildable SQLite index ... Git-authored semantic records ... remain authoritative"); `semantic_cli.py` `knowledge-build` and `knowledge-query` with 13 operations, including `search`, `explain`, `history`, `changes` and `context-for`; 88 reviewed claims in `.sensemaking/knowledge/*.json`.
- **Limit:** correctness of this slice does not establish better cross-session reasoning (`docs/semantic-architecture/README.md`, "ADR 0031 evolution").
- **Relations:** realizes part of `poss:persistent-semantic-stewardship`; potentially enables typed records for `poss:possibility-memory`.

#### `poss:path-scoped-architecture-vocabulary`: architecture and ontology vocabulary v2

- **Proposed future:** reviewed knowledge expresses layers, bounded contexts, lifecycle states, path-scoped architecture rules, data flow and confusable terms, so an agent can ask what applies to a file before editing it.
- **Origin:** ADR 0033 (PROPOSED 2026-10-23) and its competency check, which found 8 of 15 questions not expressible (`docs/semantic-architecture/architecture-ontology-competency-v1.md`).
- **Realization (OBSERVED):** `V2_CLAIM_KINDS` and `V2_PREDICATES` in `knowledge.py:40-46`; `architecture.json` and `domain.json` declare `schema_version: 2`; `rules-for`, `term` and `context-for` queries. Built in PR #565 (`STATUS.md` frontier item 41).
- **Disposition:** `SELECTED` for construction under the owner's standing request; ADR 0033 owner acceptance pending.
- **Why it is here:** implemented but not ratified. Realization and authority are separate dimensions (CQ-081, CQ-087). It is also the precedent for the competency-check gate before schema extension (plan PR 6).

#### `poss:strategic-exploration-funnel`: coverage-before-convergence exploration

- **Proposed future:** a genuine Level-3 analysis maps systems and explores breadth, grounded and counterfactual, before converging; an exploration-only request ends with an opportunity landscape.
- **Origin:** Issue #468 (`STATUS.md` frontier item 35). Not in the reservoir, which it postdates.
- **Realization (OBSERVED):** `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`, sections 2 to 4. This is guidance; whether agents follow it is normal-use evidence, not established here.
- **Gap (OBSERVED):** the breadth landscape receives no stable identity or durable home (section 4, "Breadth output"), and "prior exploratory ideas remain hypotheses" (line 92). `poss:possibility-memory` addresses this.

#### `poss:strategic-continuity-reassessment`: assumptions and reassessment triggers for strategic paths

- **Proposed future:** strategic analyses carry decision and path assumptions with reassessment triggers, plus read-only projections, so a later session sees what would reopen a decision without the tool reopening it.
- **Origin:** Issues #416 and #430; reservoir section 9.5.
- **Realization (OBSERVED):** `src/sensemaking_skills/strategy_cli.py` commands `assumptions` (projects `assumptions` and `reassessment_triggers`) and `drift` ("Detect mechanically observable typed currentness drift; do not invalidate strategy"). The 2026-10-23 analysis uses them (section 7A).
- **Relations:** its assumption-and-trigger shape is the precedent for a possibility's `revisit_when` (ontology section 7.3); potentially enables `poss:possibility-reconsideration-from-change`.

#### `poss:possibility-memory`: product possibility memory (this library)

- **Proposed future:** retained possibilities with stable identity, separated dimensions, explicit relationships and preserved rationale, recoverable by a fresh agent and used during exploration.
- **Origin:** the owner's 2026-10-28 plan.
- **Objective:** `goal:compounding-product-knowledge`. ADR 0031 decision 2 puts alternatives, decisions and temporal history in the knowledge plane.
- **Value hypothesis (HYPOTHESIZED):** a later agent recovers an earlier possibility and its reasoning, connects it to current implementation evidence, and makes a better-grounded assessment (plan section 1.3). Not demonstrated.
- **Assumption:** ASSUMPTION-1 of the 2026-10-23 analysis: later sessions consult retained knowledge when it is relevant (status NOT TESTED).
- **Realization (OBSERVED, introduced in the same change as this file):** the conceptual model and this documentary library. Absent: typed records (plan PR 3), exploration integration (PR 4), retrieval (PR 5).
- **Disposition:** 2026-10-28, owner message, `SELECTED` for the first increment (plan PR 1 and part of PR 2). Later increments are not individually authorized by that selection, and no ADR records it.
- **Risk (INFERRED):** for this repository most retained possibilities describe the knowledge plane itself, the self-referential pattern FRONTIER-1 of the 2026-10-23 analysis warned about. The library shows value only when it informs a decision beyond its own construction.
- **Relations:** extends `poss:persistent-semantic-stewardship`; potentially enabled by `poss:git-authored-knowledge-index` and `poss:strategic-exploration-funnel`; alternative to `poss:ranked-possibility-backlog`.

### 3.2 Aligned and adjacent futures

#### `poss:cross-episode-possibility-synthesis`: cross-episode possibility synthesis

- **Proposed future:** across sessions, agents combine retained possibilities, implemented capabilities and strategic history into new, distinct product directions instead of exploring from a blank slate each time.
- **Origin:** the owner's 2026-10-28 plan, section 4.4 (recombination example).
- **Alignment basis:** ADR 0031 names exploration and architectural synthesis in the reasoning plane, but not synthesis of product futures from retained possibilities. `ADJACENT` until that scope is clarified.
- **Realization:** `NOT_IMPLEMENTED` as a supported capability. Precursors exist: `strategic-repository-analysis` section 1B recalls goals, decision history and relationships before comparing paths (`skills/strategic-repository-analysis/SKILL.md:74`), and cross-episode synthesis "is currently agent-owned reasoning" (`skills/using-sensemaking/references/learning-reconciliation-policy-v0.md:355`). There are no possibility records for it to recall.
- **Relations (HYPOTHESIZED):** derived from `poss:git-authored-knowledge-index`, `poss:strategic-exploration-funnel` and `poss:strategic-continuity-reassessment`; potentially enabled by `poss:possibility-memory`; shares an assumption with `poss:capability-learning-analysis`.

#### `poss:possibility-reconsideration-from-change`: reconsideration from indexed change

- **Proposed future:** a possibility's `revisit_when` names the claims or sources whose change would matter, in the same shape as strategic `reassessment_triggers`. When an indexed revision changes one of them (`knowledge-query --operation changes`), the agent sees the possibility as a reconsideration question.
- **Origin:** synthesized by the agent in this session (2026-10-28) from `poss:strategic-continuity-reassessment`, `poss:git-authored-knowledge-index` and `poss:possibility-memory`, while writing ontology section 7.3. HYPOTHESIZED.
- **Alignment basis:** ADR 0031 success conditions: "contradictions and invalidated assumptions are recognized rather than canonized".
- **Value hypothesis (HYPOTHESIZED):** reconsideration (CQ-084) could reuse two existing surfaces instead of the dedicated `reconsideration_candidates` query proposed in plan PR 5.
- **Assumptions:** the claims a `revisit_when` cites exist as typed records (needs plan PR 3). `changes` reports set differences, not semantic consequences (`docs/semantic-architecture/persistent-knowledge-cli.md`), so the agent still judges whether a condition is met.
- **Relations:** alternative to plan PR 5's dedicated query; potentially enabled by its three origins.

### 3.3 Deferred and declined paths

#### `poss:product-core-bootstrap`: bounded product-core BOOTSTRAP before accretion (PATH-2)

- **Proposed future:** one bounded BOOTSTRAP models the product's core contracts up front; accretion through genuine work follows.
- **Origin:** 2026-10-23 strategic analysis, PATH-2 (`artifacts/history/2026-10-23-strategic-repository-analysis.md:136`).
- **Realization:** `NOT_IMPLEMENTED` as a path. The Steward's BOOTSTRAP mode exists.
- **Disposition history:**
  - 2026-10-23, Level-3 analysis, `DEFERRED`: PATH-1 (accrete through genuine responsibilities) was selected as "ADR 0031's own construction rule, more reversible" (line 218); reason `better_alternative`, with the Auteur lesson against broadening the ontology before a real task benefits. Reaffirmed by the 2026-10-24 reconciliation.
  - `revisit_when`: "PATH-1 shows no product ADD after several genuine responsibilities outside the plane" (line 159).
  - 2026-10-28, this library, reconsideration: **NO_CHANGE**. At `d0af33b`, reviewed knowledge holds product records outside the knowledge plane added through PATH-1 work, for example `component:workflow-runtime`, `component:legacy-brief-producer` and `decision:legacy-brief-producer-fails-closed` (`.sensemaking/knowledge/architecture.json`) and the product goal, constraint and non-goals in `.sensemaking/knowledge/product.json`. The trigger has not fired. Whether later sessions reuse those records is not assessed.
- **Relations:** alternative to PATH-1, the selected construction path of `poss:persistent-semantic-stewardship` (not a separate entry in v1).

#### `poss:s5-evidence-first`: independent-session evidence before more construction

- **Proposed future:** establish whether separate later sessions use reviewed knowledge (S5) before building more.
- **Origin:** 2026-10-23 analysis, "Orthogonality challenge" (lines 162-167).
- **Disposition history:** 2026-10-23, Level-3 analysis, `REJECTED_FOR_NOW` as a construction path: "an evidence state, not a construction trajectory"; the owner had ruled that S5 does not gate construction, and an independent executor was reported unavailable. Reasons `owner_direction` and `feasibility`. Preserved as ASSUMPTION-1 (line 201).
- **`revisit_when`:** ASSUMPTION-1's trigger, an independent-session record showing reviewed knowledge was skipped or decisive, or owner direction to measure. Not reassessed here.
- **Relations:** its premise is shared with `poss:possibility-memory` and `poss:cross-episode-possibility-synthesis`; the S5 evidence it would gather is the declared prerequisite of `poss:cross-product-transfer`.

#### `poss:capability-learning-analysis`: cross-episode capability learning Skill

- **Proposed future:** a specialized Skill takes an explicitly selected set of normal-use and reconciliation artifacts and produces a bounded lesson candidate.
- **Origin:** reservoir section 10.6; `docs/research/capability-learning-loop-v0.md`.
- **Realization:** `NOT_IMPLEMENTED`; no `skills/capability-learning-analysis/` at `d0af33b`.
- **Disposition:** reservoir `CANDIDATE_ONLY` and evidence-gated, read as `DEFERRED`, reason `opportunity_value`: existing reconciliation already produces episode learning. `revisit_when`: repeated normal use establishes a stable cross-episode synthesis responsibility with recurring comparison structure and material failure modes (reservoir section 10.6).
- **Relations:** shares with `poss:cross-episode-possibility-synthesis` the assumption that cross-episode synthesis is a stable, recurring responsibility worth retained structure. Not yet recorded as a hypothesis claim.

### 3.4 Long-horizon and counterfactual futures

#### `poss:cross-product-transfer`: stewardship across products and repositories (S6)

- **Proposed future:** stewardship across multiple subsystems or repositories, with scoped adapters and retrieval as warranted.
- **Origin:** stewardship plan section 11 (Wave 6) and section 14, S6 (`docs/persistent-semantic-stewardship-plan.md:462`).
- **Realization:** `NOT_IMPLEMENTED`; not qualified (`STATUS.md:58`).
- **Disposition:** `DEFERRED`, reason `feasibility`: the plan declares S5 evidence as its dependency. `revisit_when`: S5 evidence of reuse, correction and architectural decision value.
- **Relations:** potentially enabled by S5 evidence (declared in the plan, not hypothesized); extended by `poss:domain-general-sensemaking`.

#### `poss:domain-general-sensemaking`: domain-general Sensemaking control

- **Proposed future:** the control model (goal, decision-changing uncertainty, warranted responsibility, evidence-bounded claims, authority separation) applied outside software engineering, with the domain semantics replaced.
- **Origin:** research agenda, Research path 4 (`docs/research/control-model-research-agenda.md:177`).
- **Alignment basis:** alters the product's software-engineering domain premise; `CONTEXT.md` lists "domain-general research-agent control semantics" as not ratified. No accepted non-goal forbids it, so `COUNTERFACTUAL`.
- **Realization:** `NOT_IMPLEMENTED`; one bounded synthetic conceptual-transfer exercise only.
- **Disposition:** research hypothesis, `EXPLORATORY`. The transfer result "does not warrant a generic framework" (line 219). `revisit_when`: materially new uncertainty or real use.
- **Relations (HYPOTHESIZED):** extends `poss:cross-product-transfer`, from other software products to other domains.

### 3.5 Directions that conflict with current strategy

#### `poss:automatic-strategic-planner`: deterministic strategic planner and frontier ranking

- **Proposed future:** a `StrategicPlanner` or `OuterLoopEngine` ranks the Strategic Frontier and selects the next responsibility.
- **Origin:** a recurring proposal, recorded as not promoted in reservoir section 11.
- **Alignment basis:** ADR 0029 puts it outside product scope (`docs/adr/0029-current-product-boundary.md:45-47`); `ng:deterministic-planner`, `ng:automatic-selection`.
- **Realization:** `NOT_IMPLEMENTED` (a lexical search of `src/` for those class names found none at `d0af33b`; not a complete absence proof).
- **Disposition:** `REJECTED_FOR_NOW`, reason `strategic_incompatibility`. `revisit_when`: only an owner Level-4 revision of ADR 0029 ([`product-thesis-revision.md`](product-thesis-revision.md)). Library evidence alone never reopens it.
- **Relations:** conflicts with `con:agent-owns-semantic-control`.

#### `poss:ranked-possibility-backlog`: the Idea Library as a ranked backlog

- **Proposed future:** the library scores possibilities by graph position, connectivity or labels and emits the next construction task. A narrower form of `poss:automatic-strategic-planner`.
- **Origin:** the owner's 2026-10-28 plan, sections 9 and 11 ("avoid automatically ranking possibilities or selecting construction work"); reservoir section 13.
- **Alignment basis:** `ng:deterministic-planner`, `ng:automatic-selection`.
- **Disposition:** 2026-10-28, owner plan, `REJECTED_FOR_NOW`, reason `strategic_incompatibility`.
- **Why it is here:** it is the most likely way this program could drift. Naming it makes CQ-087 checkable.
- **Relations:** alternative to `poss:possibility-memory`; conflicts with `con:agent-owns-semantic-control`.

#### `poss:cross-repository-transaction-coordinator`: cross-repository transaction coordination

- **Proposed future:** atomic commit, deploy and rollback coordination across repositories.
- **Origin:** reservoir section 6.2.
- **Alignment basis:** ADR 0029 lists "general-purpose multi-repository commit/deploy/rollback transaction coordination" outside current product scope (`docs/adr/0029-current-product-boundary.md:48`).
- **Realization:** `NOT_IMPLEMENTED`; Multi-Repository Campaigns "intentionally do not promise atomic commit/deploy/rollback behavior" (reservoir section 6.2).
- **Disposition:** reservoir `LONG_HORIZON + REQUIRES_EVIDENCE`, read as `DEFERRED`. `revisit_when`: "explicit owner direction plus a concrete responsibility whose correctness genuinely depends on atomic cross-repository activation".
- **Why it is here:** the reservoir's horizon label alone reads as if evidence could reopen it. Separating alignment from horizon shows that the owner direction its trigger requires would also have to revise ADR 0029's scope.

## 4. Relationship map

| Subject | Relation | Object | Status | Basis |
| --- | --- | --- | --- | --- |
| `poss:persistent-semantic-stewardship` | `realizedBy` (in part) | `poss:git-authored-knowledge-index` | OBSERVED | Code cited in 3.1; S5 and S6 remain unrealized |
| `poss:path-scoped-architecture-vocabulary` | `extends` | `poss:git-authored-knowledge-index` | OBSERVED | `V2_*` sets extend the v1 model (`knowledge.py:40-46`) |
| `poss:possibility-memory` | `extends` | `poss:persistent-semantic-stewardship` | INFERRED | ADR 0031 decision 2 (alternatives, decisions, history) |
| `poss:possibility-memory` | `potentiallyEnabledBy` | `poss:git-authored-knowledge-index` | INFERRED | Plan PR 3 reuses existing claim kinds |
| `poss:possibility-memory` | `potentiallyEnabledBy` | `poss:strategic-exploration-funnel` | INFERRED | Funnel produces the landscape that currently has no home |
| `poss:ranked-possibility-backlog` | `alternativeTo` | `poss:possibility-memory` | RATIFIED rejection, INFERRED relation | Owner plan section 11 |
| `poss:cross-episode-possibility-synthesis` | `derivedFrom` | `poss:git-authored-knowledge-index`, `poss:strategic-exploration-funnel`, `poss:strategic-continuity-reassessment` | HYPOTHESIZED | Owner plan section 4.4 |
| `poss:cross-episode-possibility-synthesis` | `potentiallyEnabledBy` | `poss:possibility-memory` | HYPOTHESIZED | No possibility records exist to recall |
| `poss:cross-episode-possibility-synthesis` | `sharesAssumptionWith` | `poss:capability-learning-analysis` | HYPOTHESIZED | Both assume cross-episode synthesis is a stable recurring responsibility |
| `poss:possibility-reconsideration-from-change` | `derivedFrom` | `poss:strategic-continuity-reassessment`, `poss:git-authored-knowledge-index`, `poss:possibility-memory` | HYPOTHESIZED | Synthesis in this session |
| `poss:product-core-bootstrap` | `alternativeTo` | PATH-1 of `poss:persistent-semantic-stewardship` | OBSERVED | 2026-10-23 analysis, section 5 |
| `poss:s5-evidence-first` | `sharesAssumptionWith` | `poss:possibility-memory`, `poss:cross-episode-possibility-synthesis` | INFERRED | ASSUMPTION-1, NOT TESTED |
| `poss:cross-product-transfer` | `potentiallyEnabledBy` | S5 evidence | declared in plan | Stewardship plan section 14 |
| `poss:domain-general-sensemaking` | `extends` | `poss:cross-product-transfer` | HYPOTHESIZED | Research path 4 |
| `poss:automatic-strategic-planner` | `conflictsWith` | `con:agent-owns-semantic-control` | RATIFIED | ADR 0029:45-47 |
| `poss:ranked-possibility-backlog` | `conflictsWith` | `con:agent-owns-semantic-control` | RATIFIED | ADR 0029:45-47; owner plan section 11 |
| `poss:cross-repository-transaction-coordinator` | `conflictsWith` | ADR 0029 product scope | RATIFIED | ADR 0029:48 |

```text
persistent-semantic-stewardship (SELECTED)
 |-- realized in part by: git-authored-knowledge-index
 |     `-- extended by: path-scoped-architecture-vocabulary (ADR 0033 PROPOSED)
 |-- alternative path declined: product-core-bootstrap (DEFERRED, NO_CHANGE 2026-10-28)
 `-- extended by: possibility-memory (first increment)
       |-- enabled? by: git-authored-knowledge-index, strategic-exploration-funnel
       |-- alternative: ranked-possibility-backlog (REJECTED_FOR_NOW; conflicts with agent-owned control)
       `-- enables?: cross-episode-possibility-synthesis
                       `-- shares assumption with: capability-learning-analysis

strategic-continuity-reassessment + git-authored-knowledge-index + possibility-memory
 `-- derived: possibility-reconsideration-from-change (new, HYPOTHESIZED)

cross-product-transfer (needs S5 evidence) <-- extended by: domain-general-sensemaking
```

## 5. Syntheses recorded in this version

- **`poss:cross-episode-possibility-synthesis`** comes from the owner's plan: persistent knowledge, divergent exploration and strategic continuity combine into synthesis across sessions. It stays `EXPLORATORY` and every connecting relationship is hypothesized.
- **`poss:possibility-reconsideration-from-change`** emerged while building the conceptual model: strategic analyses already pair assumptions with reassessment triggers, and indexed revisions already report changed claims. Pairing a possibility's `revisit_when` with that shape might make a dedicated reconsideration query (plan PR 5) unnecessary. Plan PR 5 should test this before building a new query.

## 6. Extending and maintaining the library

- Add a possibility only when it is consequential enough that losing it, its rationale or its relationships would cost a later decision. Do not convert every passing thought.
- Give it a new `poss:` identifier, its origin, the five dimensions with bases, and any material relationships with their status. Cite where a record of origin exists; do not copy its narrative.
- Append disposition entries; do not edit earlier ones. Use `supersedes` instead of rewriting a possibility.
- When an origin source changes (for example a reservoir disposition), update the pointer here or mark the entry stale. The origin governs.
- Before a consequential reconsideration, follow the procedure in the conceptual model, section 7.4. `NO_CHANGE` is a valid result, as recorded for `poss:product-core-bootstrap`.
- Nothing here selects work. Level 3 decides whether a possibility has become consequential enough to act on.

## 7. Program continuation (non-authoritative pointer)

This version completes the plan's first increment: PR 1 and the smallest useful part of PR 2. The [plan](superpowers/plans/2026-10-28-product-possibility-idea-library.md) describes PR 2 to PR 7; each still needs selection against current source and authority. Observations made while building this version:

- **PR 2 remainder:** most reservoir entries are `NOT_ASSESSED` here. Extend only where a decision needs them.
- **PR 3:** the provisional fit table (conceptual model, section 6.2) predicts that `complements` and `extends` will not be expressible and that `sharesAssumptionWith` fits best as a shared `hypothesis` claim. Encoding records will test this. Reuse `poss:` identifiers as claim IDs.
- **PR 4:** `strategic-repository-analysis` section 1B already recalls goals, decisions and relationships before path comparison. Extending it is likely smaller than a new integration point.
- **PR 5:** test `poss:possibility-reconsideration-from-change` against the existing `changes`, `history` and `strategy assumptions` surfaces first.
