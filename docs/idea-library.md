# Idea Library v1: Product Possibility Landscape

**Status:** exploratory / non-authoritative possibility landscape; first curated selection (14 possibilities, plus construction paths and evidence prerequisites kept separate)  
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

Each entry gives a stable `poss:` identifier, the proposed future, its origin, the six dimensions of the conceptual model (alignment, ambition, horizon, realization, epistemic status, disposition), the disposition history with reasons and `revisit_when`, and its relationships.

**Possibility versus what realizes it.** An implemented possibility and the capability that realizes it are different entities. Each realized entry names the realized capability or repository element separately, and gives two claims with their own statuses: the **implementation evidence** (`OBSERVED`) and the **realization judgment** (`INFERRED`).

**Authority.** Two scopes apply:

- The **originating document governs its own historical record**: what was proposed, when, by whom and with what disposition at the time. This library cites that record and must not rewrite it. If this library misstates it, the origin wins and the entry is stale.
- The **latest applicable accepted authority governs current product commitments** (accepted ADRs, product strategy, ratified owner decisions). Where an origin's historical label and a later accepted authority differ about the present, the later authority governs the present.

Possibilities that originate in a conversation, a plan or a synthesis have their record of origin here.

**Coverage.** This is a deliberate selection, not a conversion of the reservoir. Reservoir entries not listed are `NOT_ASSESSED` here, not rejected. `NOT_IMPLEMENTED` is used only with a completeness basis for its stated scope; a search that found nothing is reported as `NOT_ASSESSED` with the bounded observation.

## 2. Landscape at a glance

| ID | Possibility | Alignment | Ambition | Horizon | Realization | Latest disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `poss:persistent-semantic-stewardship` | Persistent semantic stewardship (ADR 0031 destination) | ALIGNED | TRANSFORMATIVE | LONG_HORIZON | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-15 |
| `poss:git-authored-knowledge-index` | Git-reviewed knowledge with a rebuildable index | ALIGNED | SUBSTANTIAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:path-scoped-architecture-vocabulary` | Architecture and ontology vocabulary v2 | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED for construction; ADR 0033 PROPOSED |
| `poss:strategic-exploration-funnel` | Coverage-before-convergence exploration | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE (guidance) | SELECTED (integrated) |
| `poss:strategic-continuity-reassessment` | Assumptions and reassessment triggers for strategic paths | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:possibility-memory` | Product possibility memory (this library) | ALIGNED | SUBSTANTIAL | FORESEEABLE | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-28, first increment only |
| `poss:cross-episode-possibility-synthesis` | Cross-episode possibility synthesis | ADJACENT | SUBSTANTIAL | FORESEEABLE | NOT_ASSESSED | EXPLORATORY |
| `poss:possibility-reconsideration-from-change` | Reconsideration from indexed change (new synthesis) | ALIGNED | INCREMENTAL | FORESEEABLE | NOT_IMPLEMENTED | EXPLORATORY |
| `poss:capability-learning-analysis` | Cross-episode capability learning Skill | ADJACENT | SUBSTANTIAL | NOT_ASSESSED | NOT_IMPLEMENTED (as a Skill) | DEFERRED (evidence-gated) |
| `poss:cross-product-transfer` | Stewardship across products and repositories (S6) | ALIGNED | SUBSTANTIAL | LONG_HORIZON | NOT_ASSESSED | DEFERRED (needs S5 evidence) |
| `poss:domain-general-sensemaking` | Domain-general Sensemaking control | COUNTERFACTUAL | TRANSFORMATIVE | LONG_HORIZON | NOT_ASSESSED | EXPLORATORY (research hypothesis) |
| `poss:automatic-strategic-planner` | Deterministic strategic planner and frontier ranking | CONFLICTS_WITH_CURRENT_STRATEGY | TRANSFORMATIVE | NOT_ASSESSED | NOT_ASSESSED | REJECTED_FOR_NOW |
| `poss:ranked-possibility-backlog` | The Idea Library as a ranked backlog | CONFLICTS_WITH_CURRENT_STRATEGY | SUBSTANTIAL | FORESEEABLE | NOT_IMPLEMENTED (in this library) | REJECTED_FOR_NOW |
| `poss:cross-repository-transaction-coordinator` | Cross-repository transaction coordination | CONFLICTS_WITH_CURRENT_STRATEGY | SUBSTANTIAL | LONG_HORIZON | NOT_ASSESSED | DEFERRED (historical label) |

Order is grouping (realized, aligned future, deferred, long-horizon, conflicting), not priority. `ranked-possibility-backlog` is `FORESEEABLE` because it would be easy to build: horizon is not desirability.

Construction paths and evidence prerequisites that earlier drafts listed as possibilities are in section 4.

## 3. Possibilities

### 3.1 Realized and partially realized

#### `poss:persistent-semantic-stewardship`: persistent semantic stewardship

- **Proposed future:** Sensemaking becomes a persistent, typed, queryable, provenance-aware knowledge system operated through Skills, improving how agents understand and evolve software "across tasks, agents, repositories, and time".
- **Origin:** the owner's Path 3 choice, recorded in ADR 0031 decision 1 (`docs/adr/0031-persistent-semantic-stewardship.md:32`).
- **Objective:** `goal:compounding-product-knowledge`, `goal:longterm-stewardship`.
- **Value hypothesis (HYPOTHESIZED):** better decisions in later, genuinely separate engineering episodes (ADR 0031, "Success and failure conditions"). Not demonstrated.
- **Horizon basis:** the full destination needs S5 and S6 evidence, which `STATUS.md:58` declares not qualified.
- **Realized in part by:** `cap:semantic-queries` (reviewed capability claim in `.sensemaking/knowledge/stewardship.json`).
  - Implementation evidence (OBSERVED): the code cited under `poss:git-authored-knowledge-index`; `STATUS.md:58` declares S1–S3 integrated and S4 guidance in source.
  - Realization judgment (INFERRED): `PARTIALLY_IMPLEMENTED`.
- **Advanced by:** construction path PATH-1 (section 4).
- **Disposition history:**
  - Earlier (date not recorded in ADR 0031): treated as "merely an optional later optimization", in effect `DEFERRED`.
  - 2026-10-15, owner, `SELECTED`: the earlier conclusion is superseded "as a strategic choice" and was "not a negative empirical verdict" (ADR 0031:25-27).
- **Why it is here:** an earlier deferral reversed by an owner choice rather than by new evidence. Both assessments stay visible (CQ-083).

#### `poss:git-authored-knowledge-index`: Git-reviewed knowledge with a rebuildable index

- **Proposed future:** reviewed, source-pinned typed claims and relations authored in Git, indexed into a local rebuildable SQLite database, and read through bounded, provenance-preserving queries.
- **Origin:** ADR 0031 decision 7; stewardship plan section 14, packages S1–S3 (`docs/persistent-semantic-stewardship-plan.md:459`).
- **Realized by:** `cap:semantic-queries`, implemented by `component:knowledge-store` (existing reviewed relation `rel:query-implemented`).
  - Implementation evidence (OBSERVED): `src/sensemaking_skills/semantic_architecture/knowledge.py` (claims, relations, authored-record parsing); `knowledge_store.py` ("Rebuildable SQLite index ... Git-authored semantic records ... remain authoritative"); `semantic_cli.py` `knowledge-build` and `knowledge-query`, whose closed operation list has 13 entries including `search`, `explain`, `history`, `changes` and `context-for`; 88 reviewed claims in `.sensemaking/knowledge/*.json`.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`.
- **Limit:** correctness of this slice does not establish better cross-session reasoning (`docs/semantic-architecture/README.md`, "ADR 0031 evolution").

#### `poss:path-scoped-architecture-vocabulary`: architecture and ontology vocabulary v2

- **Proposed future:** reviewed knowledge expresses layers, bounded contexts, lifecycle states, path-scoped architecture rules, data flow and confusable terms, so an agent can ask what applies to a file before editing it.
- **Origin:** ADR 0033 (PROPOSED 2026-10-23) and its competency check, which found 8 of 15 questions not expressible (`docs/semantic-architecture/architecture-ontology-competency-v1.md`).
- **Realized by:** the path-scoped architecture context queries (`rules-for`, `term`, `context-for`) over v2 records; components `component:semantic-knowledge-plane` and `component:semantic-cli`.
  - Implementation evidence (OBSERVED): `V2_CLAIM_KINDS` and `V2_PREDICATES` in `knowledge.py:40-46`; `architecture.json` and `domain.json` declare `schema_version: 2`; the three query operations are in `semantic_cli.py`. Built in PR #565 (`STATUS.md` frontier item 41).
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`.
- **Disposition:** `SELECTED` for construction under the owner's standing request; ADR 0033 owner acceptance pending.
- **Why it is here:** implemented but not ratified. Realization and authority are separate (CQ-081, CQ-087). It is also the precedent for a competency check before schema extension (plan PR 6).

#### `poss:strategic-exploration-funnel`: coverage-before-convergence exploration

- **Proposed future:** a genuine Level-3 analysis maps systems and explores breadth, grounded and counterfactual, before converging; an exploration-only request ends with an opportunity landscape.
- **Origin:** Issue #468 (`STATUS.md` frontier item 35). Not in the reservoir, which it postdates.
- **Realized by:** the repository element `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` (Skill guidance).
  - Implementation evidence (OBSERVED): that reference, sections 2 to 4.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE` as guidance. Whether agents follow it is normal-use evidence, not established here.
- **Gap (OBSERVED):** the breadth landscape receives no stable identity or durable home (section 4, "Breadth output"), and "prior exploratory ideas remain hypotheses" (line 92). `poss:possibility-memory` addresses this.

#### `poss:strategic-continuity-reassessment`: assumptions and reassessment triggers for strategic paths

- **Proposed future:** strategic analyses carry decision and path assumptions with reassessment triggers, plus read-only projections, so a later session sees what would reopen a decision without the tool reopening it.
- **Origin:** Issues #416 and #430; reservoir section 9.5.
- **Realized by:** the `strategy assumptions` and `strategy drift` commands.
  - Implementation evidence (OBSERVED): `src/sensemaking_skills/strategy_cli.py`, command `assumptions` (projects `assumptions` and `reassessment_triggers`) and command `drift` ("Detect mechanically observable typed currentness drift; do not invalidate strategy"). The 2026-10-23 analysis records assumptions and triggers in section 7A.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`.
- **Note:** its assumption-and-trigger shape is the precedent for a possibility's `revisit_when` (conceptual model, section 7.3).

#### `poss:possibility-memory`: product possibility memory (this library)

- **Proposed future:** retained possibilities with stable identity, separated dimensions, explicit relationships and preserved rationale, recoverable by a fresh agent and used during exploration.
- **Origin:** the owner's 2026-10-28 plan.
- **Objective:** `goal:compounding-product-knowledge`. ADR 0031 decision 2 puts alternatives, decisions and temporal history in the knowledge plane.
- **Value hypothesis (HYPOTHESIZED):** a later agent recovers an earlier possibility and its reasoning, connects it to current implementation evidence, and makes a better-grounded assessment (plan section 1.3). Not demonstrated.
- **Assumption:** ASSUMPTION-1 (section 4).
- **Realized in part by:** this file and the conceptual model.
  - Implementation evidence (OBSERVED): both documents exist in the change that introduced this entry; no `poss:` records exist in `.sensemaking/knowledge/` at `d0af33b` (exhaustive check of that directory).
  - Realization judgment (INFERRED): `PARTIALLY_IMPLEMENTED`, documentary only. Typed records (plan PR 3), exploration integration (PR 4) and any retrieval support (PR 5) are absent.
- **Disposition:** 2026-10-28, owner message, `SELECTED` for the first increment (plan PR 1 and part of PR 2). Later increments are not individually authorized by that selection, and no ADR records it.
- **Risk (INFERRED):** for this repository most retained possibilities describe the knowledge plane itself, the self-referential pattern FRONTIER-1 of the 2026-10-23 analysis warned about. The library shows value only when it informs a decision beyond its own construction.

### 3.2 Aligned and adjacent futures

#### `poss:cross-episode-possibility-synthesis`: cross-episode possibility synthesis

- **Proposed future:** across sessions, agents combine retained possibilities, implemented capabilities and strategic history into new, distinct product directions instead of exploring from a blank slate each time.
- **Origin:** the owner's 2026-10-28 plan, section 4.4 (recombination example).
- **Alignment basis:** ADR 0031 names exploration and architectural synthesis in the reasoning plane, but not synthesis of product futures from retained possibilities. `ADJACENT` until that scope is clarified.
- **Realization:** `NOT_ASSESSED`. Bounded observations: a lexical search of `skills/` found no guidance for synthesizing retained possibilities; `strategic-repository-analysis` section 1B recalls goals, decision history and relationships before comparing paths (`skills/strategic-repository-analysis/SKILL.md:74`); the learning policy says cross-episode synthesis "is currently agent-owned reasoning" (`skills/using-sensemaking/references/learning-reconciliation-policy-v0.md:355`).
- **Assumptions:** ASSUMPTION-1; and that cross-episode synthesis is a stable, recurring responsibility worth retained structure (not yet recorded as a hypothesis claim).

#### `poss:possibility-reconsideration-from-change`: reconsideration from indexed change

- **Proposed future:** a possibility's `revisit_when` names the claims or sources whose change would matter, in the same shape as strategic `reassessment_triggers`. When an indexed revision changes one of them (`knowledge-query --operation changes`), the agent sees the possibility as a reconsideration question.
- **Origin:** synthesized by the agent on 2026-10-28 while writing the conceptual model, section 7.3. HYPOTHESIZED.
- **Alignment basis:** ADR 0031 success conditions: "contradictions and invalidated assumptions are recognized rather than canonized".
- **Value hypothesis (HYPOTHESIZED):** reconsideration (CQ-084) could reuse two existing surfaces instead of the dedicated `reconsideration_candidates` query proposed in plan PR 5.
- **Realization:** `NOT_IMPLEMENTED`. Completeness basis: no `poss:` records exist in `.sensemaking/knowledge/` at `d0af33b` (exhaustive check of that directory), so there is nothing for `changes` to surface.
- **Assumptions:** the claims a `revisit_when` cites exist as typed records (needs plan PR 3). `changes` reports set differences, not semantic consequences (`docs/semantic-architecture/persistent-knowledge-cli.md`), so the agent still judges whether a condition is met.

#### `poss:capability-learning-analysis`: cross-episode capability learning Skill

- **Proposed future:** a specialized Skill takes an explicitly selected set of normal-use and reconciliation artifacts and produces a bounded lesson candidate.
- **Origin:** reservoir section 10.6; `docs/research/capability-learning-loop-v0.md`.
- **Realization:** `NOT_IMPLEMENTED` as a packaged or registered Skill. Completeness basis: no `skills/capability-learning-analysis/` directory and no entry in `skills/workflow-planner/references/skill-registry.yaml` at `d0af33b`. Agent-owned cross-episode synthesis without a Skill is not assessed.
- **Horizon:** `NOT_ASSESSED`; it is gated on repeated normal-use evidence whose timing is unknown.
- **Disposition (historical record, reservoir section 10.6):** `CANDIDATE_ONLY` and evidence-gated, read as `DEFERRED`, reason `opportunity_value`: existing reconciliation already produces episode learning. `revisit_when`: repeated normal use establishes a stable cross-episode synthesis responsibility with recurring comparison structure and material failure modes.

### 3.3 Long-horizon and counterfactual futures

#### `poss:cross-product-transfer`: stewardship across products and repositories (S6)

- **Proposed future:** stewardship across multiple subsystems or repositories, with scoped adapters and retrieval as warranted.
- **Origin:** stewardship plan section 11 (Wave 6) and section 14, S6 (`docs/persistent-semantic-stewardship-plan.md:462`).
- **Realization:** `NOT_ASSESSED`. `STATUS.md:58` declares S6 "not qualified", which is a statement about evidence, not implementation. Explicit multi-repository Campaign and strategic-analysis mechanics exist (reservoir sections 6.1 and 6.4); whether they realize part of this possibility is not assessed.
- **Evidence prerequisite:** S5 evidence (section 4), declared as S6's dependency in plan section 14.
- **Disposition:** `DEFERRED`, reason `feasibility`. `revisit_when`: S5 evidence of reuse, correction and architectural decision value.

#### `poss:domain-general-sensemaking`: domain-general Sensemaking control

- **Proposed future:** the control model (goal, decision-changing uncertainty, warranted responsibility, evidence-bounded claims, authority separation) applied outside software engineering, with the domain semantics replaced.
- **Origin:** research agenda, Research path 4 (`docs/research/control-model-research-agenda.md:177`).
- **Alignment basis:** alters the product's software-engineering domain premise; `CONTEXT.md` lists "domain-general research-agent control semantics" as not ratified. No accepted non-goal forbids it, so `COUNTERFACTUAL`. Exploring it needs no review.
- **Realization:** `NOT_ASSESSED`. The research agenda reports one bounded synthetic conceptual-transfer exercise. Engineering and Product Management Domain Packs exist (reservoir section 7.1); their relation to this possibility is not assessed.
- **Disposition:** research hypothesis, `EXPLORATORY`. The transfer result "does not warrant a generic framework" (line 219). `revisit_when`: materially new uncertainty or real use.

### 3.4 Directions that conflict with current strategy

#### `poss:automatic-strategic-planner`: deterministic strategic planner and frontier ranking

- **Proposed future:** a `StrategicPlanner` or `OuterLoopEngine` ranks the Strategic Frontier and selects the next responsibility.
- **Origin:** a recurring proposal, recorded as not promoted in reservoir section 11.
- **Alignment basis:** ADR 0029 names it outside product scope (`docs/adr/0029-current-product-boundary.md:45-47`); `ng:deterministic-planner`, `ng:automatic-selection`.
- **Realization:** `NOT_ASSESSED`. Bounded observation: a lexical search of `src/` for class definitions with those names found none at `d0af33b`.
- **Disposition:** `REJECTED_FOR_NOW`, reason `strategic_incompatibility`. `revisit_when`: changing it would require revising ADR 0029's scope through the Level-4 process, which applies only if that commitment becomes decision-changing. Library evidence alone does not do that.

#### `poss:ranked-possibility-backlog`: the Idea Library as a ranked backlog

- **Proposed future:** the library scores possibilities by graph position, connectivity or labels and emits the next construction task. A narrower form of `poss:automatic-strategic-planner`.
- **Origin:** the owner's 2026-10-28 plan, sections 9 and 11 ("avoid automatically ranking possibilities or selecting construction work"); reservoir section 13.
- **Realization:** `NOT_IMPLEMENTED` in this library. Completeness basis: this file and the conceptual model contain no ranking, and no `poss:` records exist to rank.
- **Disposition:** 2026-10-28, owner plan, `REJECTED_FOR_NOW`, reason `strategic_incompatibility`.
- **Why it is here:** it is the most likely way this program could drift. Naming it makes CQ-087 checkable.

#### `poss:cross-repository-transaction-coordinator`: cross-repository transaction coordination

- **Proposed future:** atomic commit, deploy and rollback coordination across repositories.
- **Origin:** reservoir section 6.2.
- **Realization:** `NOT_ASSESSED`. The reservoir records that Multi-Repository Campaigns "intentionally do not promise atomic commit/deploy/rollback behavior"; no implementation search was made.
- **Disposition (historical record, reservoir section 6.2):** `LONG_HORIZON + REQUIRES_EVIDENCE`, read as `DEFERRED`. `revisit_when`: "explicit owner direction plus a concrete responsibility whose correctness genuinely depends on atomic cross-repository activation".
- **Current commitment:** ADR 0029 lists "general-purpose multi-repository commit/deploy/rollback transaction coordination" outside current product scope (`docs/adr/0029-current-product-boundary.md:48`). The reservoir governs its historical label; ADR 0029 governs the current scope. Acting on this possibility would therefore also need ADR 0029's scope revised.

## 4. Construction paths and evidence prerequisites (not possibilities)

These advance or condition possibilities but are not product futures. They keep their identities from the analysis that defined them. Earlier drafts of this page (PR #625 before merge) listed PATH-2 and the "S5 evidence first" option as possibilities; they are corrected here.

#### PATH-1 and PATH-2 of the 2026-10-23 strategic analysis

- **PATH-1** (accrete product knowledge through genuine responsibilities) and **PATH-2** (bounded product-core BOOTSTRAP, then accrete) are alternative construction paths toward `poss:persistent-semantic-stewardship` (`artifacts/history/2026-10-23-strategic-repository-analysis.md`, section 5; PATH-2 at line 136).
- **Historical record (governed by that analysis):** 2026-10-23, PATH-1 selected as "ADR 0031's own construction rule, more reversible" (line 218); PATH-2 not selected, reason `better_alternative`, with the Auteur lesson against broadening the ontology before a real task benefits. Reaffirmed by the 2026-10-24 reconciliation. PATH-2's reassessment trigger: "PATH-1 shows no product ADD after several genuine responsibilities outside the plane" (line 159).
- **Reconsideration of PATH-2, 2026-10-28: NO_CHANGE.**
  - Inspected evidence (OBSERVED): the 2026-10-25 PATH-1/T1 session receipt (`.sensemaking/receipts/2026-10-25-legacy-brief-producer-fail-closed.session.yaml`, R-4) records a knowledge reconciliation that revised product records outside the knowledge plane and added typed code, test and decision links. `STATUS.md` describes the same result for the legacy producer and the runtime-owned path rule. Those records, including `component:legacy-brief-producer`, are present in `.sensemaking/knowledge/architecture.json` at `d0af33b`.
  - Judgment (INFERRED): that is at least one product ADD through a PATH-1 responsibility, so the inspected evidence does not show the trigger's "no product ADD" condition.
  - Not established: how many PATH-1 responsibilities ran, whether others added product knowledge, which records were newly created rather than revised, whether later sessions reuse them, or whether PATH-2's intended benefit (less per-session reconstruction) is being achieved. NO_CHANGE means no inspected evidence gives a reason to reopen; it is not a finding that PATH-1 has succeeded.

#### ASSUMPTION-1 and the "S5 evidence first" option

- **ASSUMPTION-1** (evidence prerequisite): separately started later sessions will query reviewed knowledge when it is relevant; status NOT TESTED (analysis line 201). Its trigger: an independent-session record showing reviewed knowledge was skipped or decisive.
- **"Obtain S5 evidence first"** was considered and not admitted as a construction path on 2026-10-23: "an evidence state, not a construction trajectory"; the owner had ruled that S5 does not gate construction, and an independent executor was reported unavailable (lines 162-167). Reasons `owner_direction` and `feasibility`. It was preserved as ASSUMPTION-1. Not reassessed here.
- **Depends on ASSUMPTION-1:** PATH-1 (recorded by the analysis), `poss:possibility-memory` and `poss:cross-episode-possibility-synthesis` (INFERRED).

#### S5 evidence

- **Evidence prerequisite** for `poss:cross-product-transfer`, declared in stewardship plan section 14, whose S6 row lists "S5 evidence" as its dependency. It is evidence of reuse, correction and architectural decision value in independent sessions, not a capability.

## 5. Relationship map

Implementation evidence is listed with each realized entry in section 3. The table below lists only semantic relationships between possibilities and their endpoints, each with its own status. Endpoint types follow `ontology.md` (Layer 6, "Product relations").

| Subject (possibility) | Relation | Object (type) | Status | Basis |
| --- | --- | --- | --- | --- |
| `poss:persistent-semantic-stewardship` | `realizedBy` (in part) | `cap:semantic-queries` (ProductCapability) | INFERRED | Evidence under `poss:git-authored-knowledge-index`; S5 and S6 unrealized |
| `poss:git-authored-knowledge-index` | `realizedBy` | `cap:semantic-queries` (ProductCapability) | INFERRED | Code cited in 3.1 |
| `poss:path-scoped-architecture-vocabulary` | `realizedBy` | path-scoped architecture context queries (ProductCapability) | INFERRED | `knowledge.py:40-46`; `semantic_cli.py` |
| `poss:path-scoped-architecture-vocabulary` | `extends` | `poss:git-authored-knowledge-index` (possibility) | INFERRED | v2 sets are additive to the v1 model (OBSERVED in `knowledge.py`) |
| `poss:strategic-exploration-funnel` | `realizedBy` | funnel reference (RepositoryElement) | INFERRED | The reference file |
| `poss:strategic-continuity-reassessment` | `realizedBy` | `strategy assumptions` and `strategy drift` (RepositoryElement) | INFERRED | `strategy_cli.py` |
| `poss:possibility-memory` | `extends` | `poss:persistent-semantic-stewardship` (possibility) | INFERRED | ADR 0031 decision 2 |
| `poss:possibility-memory` | `potentiallyEnabledBy` | `cap:semantic-queries` (ProductCapability) | INFERRED | Plan PR 3 reuses existing claim kinds and queries |
| `poss:possibility-memory` | `potentiallyEnabledBy` | Level-3 breadth exploration guidance (ProductCapability) | INFERRED | It produces the landscape that currently has no home |
| `poss:ranked-possibility-backlog` | `alternativeTo` | `poss:possibility-memory` (possibility) | INFERRED relation; rejection RATIFIED | Owner plan section 11 |
| `poss:cross-episode-possibility-synthesis` | `derivedFrom` | `poss:git-authored-knowledge-index`, `poss:strategic-exploration-funnel`, `poss:strategic-continuity-reassessment` (possibilities) | HYPOTHESIZED | Owner plan section 4.4 |
| `poss:cross-episode-possibility-synthesis` | `potentiallyEnabledBy` | `poss:possibility-memory` (possibility) | HYPOTHESIZED | No possibility records yet exist to recall |
| `poss:cross-episode-possibility-synthesis` | `sharesAssumptionWith` | `poss:capability-learning-analysis` (possibility) | HYPOTHESIZED | Both assume cross-episode synthesis is a stable recurring responsibility |
| `poss:possibility-reconsideration-from-change` | `derivedFrom` | `poss:strategic-continuity-reassessment`, `poss:git-authored-knowledge-index`, `poss:possibility-memory` (possibilities) | HYPOTHESIZED | Synthesis on 2026-10-28 |
| `poss:possibility-reconsideration-from-change` | `potentiallyEnabledBy` | `cap:semantic-queries` (`changes`) and the `strategy assumptions` projection (ProductCapabilities) | HYPOTHESIZED | Conceptual model, section 7.3 |
| `poss:domain-general-sensemaking` | `extends` | `poss:cross-product-transfer` (possibility) | HYPOTHESIZED | Research path 4 |
| `poss:automatic-strategic-planner` | `conflictsWith` | `ng:deterministic-planner` (RatifiedIntent) | RATIFIED | ADR 0029:45 names it explicitly |
| `poss:ranked-possibility-backlog` | `conflictsWith` | `ng:automatic-selection` (RatifiedIntent) | INFERRED | ADR 0029:47 names automatic responsibility selection, not possibility ranking |
| `poss:cross-repository-transaction-coordinator` | `conflictsWith` | ADR 0029 product scope (RatifiedIntent) | RATIFIED | ADR 0029:48 names it explicitly |

Links to construction paths and evidence prerequisites are in section 4; they are not possibility relations.

```text
persistent-semantic-stewardship (possibility, SELECTED)
 |-- realized in part by: cap:semantic-queries (capability)
 |-- advanced by: PATH-1 (construction path; PATH-2 declined, NO_CHANGE 2026-10-28)
 `-- extended by: possibility-memory (possibility, first increment)
       |-- enabled? by: cap:semantic-queries, breadth exploration guidance (capabilities)
       |-- alternative: ranked-possibility-backlog (REJECTED_FOR_NOW)
       |-- depends on: ASSUMPTION-1 (evidence prerequisite)
       `-- enables?: cross-episode-possibility-synthesis
                       `-- shares assumption with: capability-learning-analysis

git-authored-knowledge-index (possibility) -- realized by --> cap:semantic-queries
 `-- extended by: path-scoped-architecture-vocabulary (ADR 0033 PROPOSED)

strategic-continuity-reassessment + git-authored-knowledge-index + possibility-memory
 `-- derived: possibility-reconsideration-from-change (new, HYPOTHESIZED)

cross-product-transfer (needs S5 evidence) <-- extended by: domain-general-sensemaking
```

## 6. Syntheses recorded in this version

- **`poss:cross-episode-possibility-synthesis`** comes from the owner's plan: persistent knowledge, divergent exploration and strategic continuity combine into synthesis across sessions. It stays `EXPLORATORY` and every connecting relationship is hypothesized.
- **`poss:possibility-reconsideration-from-change`** emerged while building the conceptual model: strategic analyses already pair assumptions with reassessment triggers, and indexed revisions already report changed claims. Pairing a possibility's `revisit_when` with that shape might make a dedicated reconsideration query (plan PR 5) unnecessary. Plan PR 5 should test this before building a new query.

## 7. Extending and maintaining the library

- Add a possibility only when it is consequential enough that losing it, its rationale or its relationships would cost a later decision. Do not convert every passing thought.
- Give it a new `poss:` identifier, its origin, the six dimensions with bases, and any material relationships with their status and correctly typed endpoints. Cite where a record of origin exists; do not copy its narrative.
- Name a realized capability separately from the possibility it realizes, and keep implementation evidence (`OBSERVED`) apart from realization judgments (`INFERRED`).
- Keep construction paths and evidence prerequisites in section 4, not among possibilities.
- Append disposition entries; do not edit earlier ones. Use `supersedes` instead of rewriting a possibility.
- When an origin source changes its historical record, update the pointer here or mark the entry stale. When a later accepted authority changes a current commitment, record the new commitment beside the historical label.
- Before a consequential reconsideration, follow the procedure in the conceptual model, section 7.4. `NO_CHANGE` is a valid result, as recorded for PATH-2.
- Nothing here selects work. Level 3 decides whether a possibility has become consequential enough to act on.

## 8. Program continuation (non-authoritative pointer)

This version completes the plan's first increment: PR 1 and the smallest useful part of PR 2. The [plan](superpowers/plans/2026-10-28-product-possibility-idea-library.md) describes PR 2 to PR 7; each still needs selection against current source and authority. Observations made while building this version:

- **PR 2 remainder:** most reservoir entries are `NOT_ASSESSED` here. Extend only where a decision needs them.
- **PR 3:** the provisional fit table (conceptual model, section 6.2) predicts that `complements` and `extends` will not be expressible and that `sharesAssumptionWith` fits best as a shared `hypothesis` claim. Encoding records will test this. Reuse `poss:` identifiers as claim IDs.
- **PR 4:** `strategic-repository-analysis` section 1B already recalls goals, decisions and relationships before path comparison. Extending it is likely smaller than a new integration point.
- **PR 5:** test `poss:possibility-reconsideration-from-change` against the existing `changes`, `history` and `strategy assumptions` surfaces first.
