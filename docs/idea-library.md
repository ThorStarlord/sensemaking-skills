# Idea Library v1: Product Possibility Landscape

**Status:** exploratory / non-authoritative possibility landscape; curated selection (18 possibilities, plus construction paths and evidence prerequisites kept separate)  
**Typed records:** [`../.sensemaking/knowledge/possibilities.json`](../.sensemaking/knowledge/possibilities.json) (plan PR 3)  
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

**Typed records.** Every possibility here is also a reviewed `opportunity` claim with the same `poss:` identifier in `.sensemaking/knowledge/possibilities.json`. Realized capabilities are `capability` claims, mechanically observed implementation evidence is in `observation` claims, and shared premises are `hypothesis` claims. Recover them with existing queries, for example `knowledge-query --operation search --term poss:`, `explain --subject poss:<slug>`, `impact --subject cap:<slug>` and `contradictions` (section 6).

**Coverage.** This is a deliberate selection, not a conversion of the reservoir. Reservoir entries not listed are `NOT_ASSESSED` here, not rejected. `NOT_IMPLEMENTED` is used only with a completeness basis for its stated scope; a search that found nothing is reported as `NOT_ASSESSED` with the bounded observation.

## 2. Landscape at a glance

| ID | Possibility | Alignment | Ambition | Horizon | Realization | Latest disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `poss:persistent-semantic-stewardship` | Persistent semantic stewardship (ADR 0031 destination) | ALIGNED | TRANSFORMATIVE | LONG_HORIZON | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-15 |
| `poss:git-authored-knowledge-index` | Git-reviewed knowledge with a rebuildable index | ALIGNED | SUBSTANTIAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:path-scoped-architecture-vocabulary` | Architecture and ontology vocabulary v2 | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED for construction; ADR 0033 PROPOSED |
| `poss:strategic-exploration-funnel` | Coverage-before-convergence exploration | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE (guidance) | SELECTED (integrated) |
| `poss:strategic-continuity-reassessment` | Assumptions and reassessment triggers for strategic paths | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED (integrated) |
| `poss:possibility-memory` | Product possibility memory (this library) | ALIGNED | SUBSTANTIAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED 2026-10-28 (plan PR 1 to PR 4) |
| `poss:cross-episode-possibility-synthesis` | Cross-episode possibility synthesis | ALIGNED (was ADJACENT) | SUBSTANTIAL | FORESEEABLE | PARTIALLY_IMPLEMENTED | SELECTED 2026-10-28 (guidance) |
| `poss:possibility-reconsideration-from-change` | Reconsideration from indexed change (new synthesis) | ALIGNED | INCREMENTAL | FORESEEABLE | NOT_IMPLEMENTED | EXPLORATORY |
| `poss:capability-learning-analysis` | Cross-episode capability learning Skill | ADJACENT | SUBSTANTIAL | NOT_ASSESSED | NOT_IMPLEMENTED (as a Skill) | DEFERRED (evidence-gated) |
| `poss:cross-product-transfer` | Stewardship across products and repositories (S6) | ALIGNED | SUBSTANTIAL | LONG_HORIZON | NOT_ASSESSED | DEFERRED (needs S5 evidence) |
| `poss:domain-general-sensemaking` | Domain-general Sensemaking control | COUNTERFACTUAL | TRANSFORMATIVE | LONG_HORIZON | NOT_ASSESSED | EXPLORATORY (research hypothesis) |
| `poss:automatic-strategic-planner` | Deterministic strategic planner and frontier ranking | CONFLICTS_WITH_CURRENT_STRATEGY | TRANSFORMATIVE | NOT_ASSESSED | NOT_ASSESSED | REJECTED_FOR_NOW |
| `poss:ranked-possibility-backlog` | The Idea Library as a ranked backlog | CONFLICTS_WITH_CURRENT_STRATEGY | SUBSTANTIAL | FORESEEABLE | NOT_IMPLEMENTED (in this library) | REJECTED_FOR_NOW |
| `poss:cross-repository-transaction-coordinator` | Cross-repository transaction coordination | CONFLICTS_WITH_CURRENT_STRATEGY | SUBSTANTIAL | LONG_HORIZON | NOT_ASSESSED | DEFERRED (historical label) |
| `poss:construction-time-possibility-reconciliation` | Reconcile possibilities from construction changes (new) | ALIGNED | INCREMENTAL | FORESEEABLE | IMPLEMENTED_BASELINE | SELECTED 2026-10-28 (plan PR 7 guidance) |
| `poss:target-repository-discovery-memory` | Discovery memory for target repositories (new) | ALIGNED | SUBSTANTIAL | FORESEEABLE | NOT_ASSESSED | EXPLORATORY |
| `poss:possibilities-projected-from-analyses` | Derive possibilities from strategic analyses (new counterfactual) | COUNTERFACTUAL | INCREMENTAL | FORESEEABLE | NOT_ASSESSED | REJECTED_FOR_NOW |
| `poss:repository-local-prospective-decision-memory` | Prospective decision memory in target repositories (from a consequence) | ALIGNED | SUBSTANTIAL | FORESEEABLE | NOT_ASSESSED | EXPLORATORY |

Order is grouping (realized, aligned future, deferred, long-horizon, conflicting, then the three recorded from the 2026-10-28 exploration), not priority. `ranked-possibility-backlog` is `FORESEEABLE` because it would be easy to build: horizon is not desirability.

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
- **Realized by:** `cap:path-scoped-architecture-context` (the `rules-for`, `term` and `context-for` queries over v2 records), implemented by `component:semantic-knowledge-plane`.
  - Implementation evidence (OBSERVED): `V2_CLAIM_KINDS` and `V2_PREDICATES` in `knowledge.py:40-46`; `architecture.json` and `domain.json` declare `schema_version: 2`; the three query operations are in `semantic_cli.py`. Built in PR #565 (`STATUS.md` frontier item 41).
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`.
- **Disposition:** `SELECTED` for construction under the owner's standing request; ADR 0033 owner acceptance pending.
- **Why it is here:** implemented but not ratified. Realization and authority are separate (CQ-081, CQ-087). It is also the precedent for a competency check before schema extension (plan PR 6).

#### `poss:strategic-exploration-funnel`: coverage-before-convergence exploration

- **Proposed future:** a genuine Level-3 analysis maps systems and explores breadth, grounded and counterfactual, before converging; an exploration-only request ends with an opportunity landscape.
- **Origin:** Issue #468 (`STATUS.md` frontier item 35). Not in the reservoir, which it postdates.
- **Realized by:** `cap:breadth-exploration-guidance`, whose implementation is the repository element `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` (Skill guidance).
  - Implementation evidence (OBSERVED): that reference, sections 2 to 4.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE` as guidance. Whether agents follow it is normal-use evidence, not established here.
- **Gap observed at `d0af33b`:** the breadth landscape received no stable identity or durable home, and "prior exploratory ideas remain hypotheses" (line 92). Since plan PR 4, section 4 recalls retained possibility records before breadth and retains consequential new or revised ones (`observation:funnel-recalls-retained-possibilities` supersedes `observation:funnel-breadth-guidance`).

#### `poss:strategic-continuity-reassessment`: assumptions and reassessment triggers for strategic paths

- **Proposed future:** strategic analyses carry decision and path assumptions with reassessment triggers, plus read-only projections, so a later session sees what would reopen a decision without the tool reopening it.
- **Origin:** Issues #416 and #430; reservoir section 9.5.
- **Realized by:** `cap:strategic-reassessment-projection`, implemented by the `strategy assumptions` and `strategy drift` commands.
  - Implementation evidence (OBSERVED): `src/sensemaking_skills/strategy_cli.py`, command `assumptions` (projects `assumptions` and `reassessment_triggers`) and command `drift` ("Detect mechanically observable typed currentness drift; do not invalidate strategy"). The 2026-10-23 analysis records assumptions and triggers in section 7A.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`.
- **Note:** its assumption-and-trigger shape is the precedent for a possibility's `revisit_when` (conceptual model, section 7.3).

#### `poss:possibility-memory`: product possibility memory (this library)

- **Proposed future:** retained possibilities with stable identity, separated dimensions, explicit relationships and preserved rationale, recoverable by a fresh agent and used during exploration.
- **Origin:** the owner's 2026-10-28 plan.
- **Objective:** `goal:compounding-product-knowledge`. ADR 0031 decision 2 puts alternatives, decisions and temporal history in the knowledge plane.
- **Value hypothesis (HYPOTHESIZED):** a later agent recovers an earlier possibility and its reasoning, connects it to current implementation evidence, and makes a better-grounded assessment (plan section 1.3). Not demonstrated.
- **Assumption:** ASSUMPTION-1 (section 4).
- **Realized in part by:** `cap:possibility-records`.
  - Implementation evidence (OBSERVED): this file, the conceptual model, the typed records in `.sensemaking/knowledge/possibilities.json` (retrieved with existing operations, section 6), and since plan PR 4 the exploration guidance in funnel section 4 and the steward knowledge contract ("Product possibility records").
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE`, revised from `PARTIALLY_IMPLEMENTED` at `d1dee16`. Agent adherence and cross-session use are not established.
- **Disposition history:** 2026-10-28, owner message, `SELECTED` for the first increment (plan PR 1 and part of PR 2); then plan PR 3 and PR 4 under the owner's follow-up message. No ADR records it.
- **Risk (INFERRED):** for this repository most retained possibilities describe the knowledge plane itself, the self-referential pattern FRONTIER-1 of the 2026-10-23 analysis warned about. The library shows value only when it informs a decision beyond its own construction.

### 3.2 Aligned and adjacent futures

#### `poss:cross-episode-possibility-synthesis`: cross-episode possibility synthesis

- **Proposed future:** across sessions, agents combine retained possibilities, implemented capabilities and strategic history into new, distinct product directions instead of exploring from a blank slate each time.
- **Origin:** the owner's 2026-10-28 plan, section 4.4 (recombination example).
- **Alignment:** `ALIGNED` since 2026-10-28: the owner's plan PR 4 and follow-up message direct exploration to recall retained possibilities and record consequential new synthesis. Earlier assessment at `d0af33b`: `ADJACENT`, because ADR 0031 names exploration and synthesis in the reasoning plane but not synthesis of product futures from retained possibilities.
- **Realization:** `PARTIALLY_IMPLEMENTED` since plan PR 4: funnel section 4 and `strategic-repository-analysis` section 1B tell agents to recall retained possibilities and retain new syntheses, and one same-session exploration is recorded (section 6). Cross-session use is not established. Earlier assessment at `d0af33b`: `NOT_ASSESSED`; a lexical search of `skills/` found no guidance for synthesizing retained possibilities, and the learning policy says cross-episode synthesis "is currently agent-owned reasoning" (`skills/using-sensemaking/references/learning-reconciliation-policy-v0.md:355`).
- **Disposition history:** `EXPLORATORY` (owner plan example, 2026-10-28); `SELECTED` for its guidance under plan PR 4 (2026-10-28).
- **Assumptions:** ASSUMPTION-1; and that cross-episode synthesis is a stable, recurring responsibility worth retained structure (not yet recorded as a hypothesis claim).

#### `poss:possibility-reconsideration-from-change`: reconsideration from indexed change

- **Proposed future:** a possibility's `revisit_when` names the claims or sources whose change would matter, in the same shape as strategic `reassessment_triggers`. When an indexed revision changes one of them (`knowledge-query --operation changes`), the agent sees the possibility as a reconsideration question.
- **Origin:** synthesized by the agent on 2026-10-28 while writing the conceptual model, section 7.3. HYPOTHESIZED.
- **Alignment basis:** ADR 0031 success conditions: "contradictions and invalidated assumptions are recognized rather than canonized".
- **Value hypothesis (HYPOTHESIZED):** reconsideration (CQ-084) could reuse two existing surfaces instead of the dedicated `reconsideration_candidates` query proposed in plan PR 5.
- **Realization:** `NOT_IMPLEMENTED`. Completeness basis: at `d0af33b` no `poss:` records existed in `.sensemaking/knowledge/`. Since plan PR 3, records exist and `changes` lists changed `poss:` records (section 6), but every `revisit_when` is free text that names no claim identifier (exhaustive check of `possibilities.json`), so no change can yet be matched to a condition.
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

### 3.5 Recorded from the 2026-10-28 retrieval-grounded exploration

These grew from the typed records and queries described in section 6. Each is a hypothesis or an agent design judgment, not a selection or an authorization.

#### `poss:construction-time-possibility-reconciliation`: reconcile possibilities from construction changes

- **Proposed future:** during a construction increment, the existing `workspace-impact` query lists the possibility records whose cited sources the change touched. The agent re-inspects only those, as plan PR 7 intends, with no new machinery.
- **Origin:** agent synthesis, 2026-10-28. `impact` on `cap:semantic-queries` reached every possibility that capability realizes or enables, and the `workspace-impact` contract (`docs/semantic-architecture/persistent-knowledge-cli.md`) maps changed paths to records that cite them.
- **Alignment basis:** ADR 0031 success conditions: invalidated assumptions are recognized rather than canonized. `ALIGNED`, `INCREMENTAL`, `FORESEEABLE`.
- **Realization:**
  - Implementation evidence (OBSERVED, query QY-11 in the section 6 receipt): with this change's library edits uncommitted, `workspace-impact` against the indexed records listed 13 records citing the edited file, 5 of them possibilities.
  - Realization judgment (INFERRED): `IMPLEMENTED_BASELINE` since plan PR 4 added the guidance to the steward reconciliation reference (`PARTIALLY_IMPLEMENTED` before).
- **Limits observed:** matching is by file path, not meaning. In QY-11, re-inspection found 3 of the 5 listed possibilities changed by the edit; 2 were listed only because their records cited the library file. On plan PR 4 itself, 6 records were flagged by path, and inspecting the 4 changed files no record cited found 3 more affected possibilities. Read `uncited_changed_paths`, not only the flagged records.
- **Disposition history:** `EXPLORATORY` (agent, 2026-10-28); `SELECTED` for its guidance under plan PR 7, first used on plan PR 4 (2026-10-28).
- **Relations:** complements `poss:possibility-reconsideration-from-change` (during construction, versus across indexed revisions); enabled by `cap:semantic-queries`.

#### `poss:target-repository-discovery-memory`: discovery memory for target repositories

- **Proposed future:** when the portable `using-sensemaking` Skill performs repository-only discovery in a target repository and has authority to write knowledge there, it retains the candidate responsibilities it compared (selected and declined, with reasons and `revisit_when`) as possibility records. A later discovery starts from them instead of re-deriving them or anchoring on the last receipt's `next`.
- **Origin:** agent synthesis, 2026-10-28, combining `poss:possibility-memory` with the realized `cap:repository-only-discovery` and the observed 2026-10-27 discovery miss (`docs/agents/build-loop.md`, "Observed repository-only discovery miss").
- **Alignment basis:** ADR 0031 decision 1 names repositories, and repository-only discovery is the product's front door, so `ALIGNED`. Writing records in a target repository needs that repository's knowledge authority; discovery alone stays read-only. `SUBSTANTIAL`; `FORESEEABLE`, because the records are plain JSON a target can read without an index or CLI.
- **Realization:** `NOT_ASSESSED` as a whole. Bounded observation (OBSERVED; the documented schema lists every receipt field, which gives a completeness basis for this part): the session receipt records one `next.warranted_responsibility` and has no field for the compared candidate set (`skills/using-sensemaking/references/session-receipt-v1.md`, section 5). The receipt validator does not reject unknown fields, so an added field would be neither enforced nor read. A lexical search of `skills/using-sensemaking/` found no guidance for retaining that set.
- **Value hypothesis (HYPOTHESIZED):** fewer repeated discoveries and less recency anchoring in target repositories. It would also give possibility memory value outside this repository's own knowledge plane, which is the self-reference risk noted under `poss:possibility-memory`.
- **Assumptions:** ASSUMPTION-1 also holds in target repositories; their owners grant knowledge-edit authority.
- **Relations:** extends `poss:possibility-memory`; enabled by `cap:possibility-records` and `cap:repository-only-discovery`. Unlike `poss:cross-product-transfer`, it moves no knowledge between products, so it does not depend on S5 evidence.
- **Disposition:** `EXPLORATORY` (agent, 2026-10-28). A consequential candidate for a later Level-3 or plan PR 4 decision; not selected or authorized.
- **Assessed 2026-10-28** in the prospective reasoning reference case (`artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md`; records in `.sensemaking/knowledge/prospective-reasoning.json`). Four architecture options were compared. The provisional preference, `arch:git-reviewed-local-memory`, was narrowed by `REVISE_PREFERENCE` to sessions that hold knowledge-edit and commit authority in the target, because discovery is read-only by default and uncommitted receipts are lost. That yields a candidate responsibility for plan PR H; it is not authorized and the disposition is unchanged.

#### `poss:repository-local-prospective-decision-memory`: prospective decision memory in target repositories

- **Proposed future:** a target repository's authorized knowledge surface retains architecture options, consequence hypotheses and preferences from its own reasoning, not only discovery candidates, so later sessions there reconstruct why one structure or path was preferred.
- **Origin:** derived on 2026-10-28 from `conseq:prospective-decision-memory-reuse` in the prospective reasoning reference case.
- **Alignment basis:** ADR 0031 decision 1 names repositories, and the owner's prospective reasoning plan (PR J) intends this outcome. `ALIGNED`, `SUBSTANTIAL`, `FORESEEABLE` (existing kinds suffice; it needs one explicitly authorized target repository).
- **Realization:** `NOT_ASSESSED`; no target repository was inspected. This repository's `.sensemaking/knowledge/prospective-reasoning.json` is the in-repository precedent.
- **Disposition:** `EXPLORATORY` (agent, 2026-10-28). It coincides with plan PR J's intended outcome, so it is recorded as the possibility PR J would advance, not as an independent proposal.
- **Relations:** derived from `conseq:prospective-decision-memory-reuse`; extends `poss:target-repository-discovery-memory`.

#### `poss:possibilities-projected-from-analyses`: derive possibilities from strategic analyses (counterfactual)

- **Proposed future:** instead of authoring possibility records, project them from strategic analyses' frontier candidates, paths and dispositions with the existing `strategy history` and `strategy graph` commands.
- **Origin:** agent counterfactual, 2026-10-28, challenging this program's premise that possibilities need authored records.
- **Alignment basis:** `COUNTERFACTUAL`: it alters a design premise of this program, not a product commitment, and exploring it needed no review. `INCREMENTAL`; `FORESEEABLE`.
- **Realization:** `NOT_ASSESSED`. The commands exist (`src/sensemaking_skills/strategy_cli.py`); whether they could carry possibilities was not assessed.
- **Disposition:** 2026-10-28, agent (design choice within plan PR 3), `REJECTED_FOR_NOW`, reason `better_alternative`. Analyses cover Level-3 episodes and their paths, and none of the 17 possibilities recorded with it originates in one: they come from ADRs, plans, the reservoir, the research agenda and syntheses, which a projection would drop. Citing analyses as records of origin keeps their value. `revisit_when`: authored records drift from or duplicate analyses in real use, or their maintenance cost becomes material.
- **Relations:** alternative to `poss:possibility-memory`; derived from `poss:strategic-continuity-reassessment`.

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
| `poss:path-scoped-architecture-vocabulary` | `realizedBy` | `cap:path-scoped-architecture-context` (ProductCapability) | INFERRED | `knowledge.py:40-46`; `semantic_cli.py` |
| `poss:path-scoped-architecture-vocabulary` | `extends` | `poss:git-authored-knowledge-index` (possibility) | INFERRED | v2 sets are additive to the v1 model (OBSERVED in `knowledge.py`) |
| `poss:strategic-exploration-funnel` | `realizedBy` | `cap:breadth-exploration-guidance` (ProductCapability) | INFERRED | The funnel reference |
| `poss:strategic-continuity-reassessment` | `realizedBy` | `cap:strategic-reassessment-projection` (ProductCapability) | INFERRED | `strategy_cli.py` |
| `poss:possibility-memory` | `realizedBy` (in part) | `cap:possibility-records` (ProductCapability) | INFERRED | Section 6 |
| `poss:possibility-memory` | `extends` | `poss:persistent-semantic-stewardship` (possibility) | INFERRED | ADR 0031 decision 2 |
| `poss:possibility-memory` | `potentiallyEnabledBy` | `cap:semantic-queries` (ProductCapability) | INFERRED | Plan PR 3 reuses existing claim kinds and queries |
| `poss:possibility-memory` | `potentiallyEnabledBy` | `cap:breadth-exploration-guidance` (ProductCapability) | INFERRED | It produces the landscape memory retains; not a prerequisite |
| `poss:ranked-possibility-backlog` | `alternativeTo` | `poss:possibility-memory` (possibility) | INFERRED relation; rejection RATIFIED | Owner plan section 11 |
| `poss:cross-episode-possibility-synthesis` | `derivedFrom` | `poss:git-authored-knowledge-index`, `poss:strategic-exploration-funnel`, `poss:strategic-continuity-reassessment` (possibilities) | HYPOTHESIZED | Owner plan section 4.4 |
| `poss:cross-episode-possibility-synthesis` | `potentiallyEnabledBy` | `cap:possibility-records` (ProductCapability) | HYPOTHESIZED | It needs retained records to recall |
| `poss:cross-episode-possibility-synthesis` | `sharesAssumptionWith` | `poss:capability-learning-analysis` (possibility) | HYPOTHESIZED | Both assume cross-episode synthesis is a stable recurring responsibility |
| `poss:possibility-reconsideration-from-change` | `derivedFrom` | `poss:strategic-continuity-reassessment`, `poss:git-authored-knowledge-index`, `poss:possibility-memory` (possibilities) | HYPOTHESIZED | Synthesis on 2026-10-28 |
| `poss:possibility-reconsideration-from-change` | `potentiallyEnabledBy` | `cap:semantic-queries` (`changes`) and `cap:strategic-reassessment-projection` (ProductCapabilities) | HYPOTHESIZED | Conceptual model, section 7.3 |
| `poss:domain-general-sensemaking` | `extends` | `poss:cross-product-transfer` (possibility) | HYPOTHESIZED | Research path 4 |
| `poss:automatic-strategic-planner` | `conflictsWith` | `ng:deterministic-planner` (RatifiedIntent) | RATIFIED | ADR 0029:45 names it explicitly |
| `poss:ranked-possibility-backlog` | `conflictsWith` | `ng:automatic-selection` (RatifiedIntent) | INFERRED | ADR 0029:47 names automatic responsibility selection, not possibility ranking |
| `poss:cross-repository-transaction-coordinator` | `conflictsWith` | ADR 0029 product scope (RatifiedIntent) | RATIFIED | ADR 0029:48 names it explicitly |
| `poss:construction-time-possibility-reconciliation` | `complements` | `poss:possibility-reconsideration-from-change` (possibility) | HYPOTHESIZED | During construction versus across indexed revisions |
| `poss:construction-time-possibility-reconciliation` | `potentiallyEnabledBy` | `cap:semantic-queries` (`workspace-impact`) (ProductCapability) | INFERRED | Section 6, demonstrated on possibility records |
| `poss:target-repository-discovery-memory` | `extends` | `poss:possibility-memory` (possibility) | HYPOTHESIZED | From this repository to target repositories |
| `poss:target-repository-discovery-memory` | `potentiallyEnabledBy` | `cap:possibility-records`, `cap:repository-only-discovery` (ProductCapabilities) | HYPOTHESIZED | Section 3.5 |
| `poss:possibilities-projected-from-analyses` | `alternativeTo` | `poss:possibility-memory` (possibility) | INFERRED relation; rejection by agent design choice | Section 3.5 |
| `poss:possibilities-projected-from-analyses` | `derivedFrom` | `poss:strategic-continuity-reassessment` (possibility) | HYPOTHESIZED | Counterfactual on 2026-10-28 |
| `poss:repository-local-prospective-decision-memory` | `derivedFrom` | `conseq:prospective-decision-memory-reuse` (ConsequenceHypothesis) | HYPOTHESIZED | Prospective reasoning reference case |
| `poss:repository-local-prospective-decision-memory` | `extends` | `poss:target-repository-discovery-memory` (possibility) | HYPOTHESIZED | Prospective reasoning reference case |

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

## 6. Typed records and a retrieval-grounded exploration (2026-10-28)

**Records.** `.sensemaking/knowledge/possibilities.json` encodes every possibility as an `opportunity` claim with its `poss:` identifier, realized capabilities as `capability` claims, mechanically observed implementation evidence as `observation` claims (status `observed`, authority `code` or `document`), and shared premises as `hypothesis` claims. Each relation keeps the executable `epistemic_status` (`declared` or `hypothetical`) plus `attributes.establishment` (`inferred`, `ratified`, `hypothesized`) and, where the predicate is only an approximation, `attributes.conceptual_relation`. Dimensions and disposition history are claim attributes. Encoding findings are in the conceptual model, section 6.2.

**Retrieval.** The queries are recorded in `.sensemaking/receipts/2026-10-28-possibility-reconciliation-and-knowledge.query.yaml`.

- Before the records existed, a search for `poss:`, "possibility" or "opportunity" at `main@d1dee16` returned 0 claims.
- After indexing, `search --term poss:` returned every possibility; `explain` on `poss:possibility-memory` returned its goal, capabilities, assumption, extension and the possibilities derived from or alternative to it; `explain` on `hyp:cross-episode-synthesis-recurs` returned both possibilities sharing that premise; `contradictions` returned the three strategy-conflicting possibilities with their establishment; `impact` on `cap:semantic-queries` returned every possibility that capability realizes or enables.
- After the exploration's records were indexed, `changes` from the first indexed revision listed the 5 added claims and separated the 4 possibility records whose authored fields changed from 16 records changed only in provenance. That is the mechanism `poss:possibility-reconsideration-from-change` needs, minus claim-identified `revisit_when` conditions.
- Gaps: construction paths are not in knowledge (by design; they live in their analyses and in section 4 here). A possibility's implementation evidence is two hops away (possibility, capability, observation), so `explain` on a possibility reports observations as not assessed; use `explain` on the capability. Dimensions are attributes, so no query can filter by alignment or horizon; at 17 records, reading them is acceptable.

**Exploration.** Starting only from those results, the agent explored grounded and counterfactual futures:

- The `impact` result and the `workspace-impact` contract suggested `poss:construction-time-possibility-reconciliation`, which was then exercised on this change (section 3.5).
- `poss:possibility-memory` combined with the Skill's repository-only discovery and the observed 2026-10-27 discovery miss suggested `poss:target-repository-discovery-memory`.
- Challenging the program's own premise gave `poss:possibilities-projected-from-analyses`, retained as a declined alternative with its rationale.
- The `impact` result also suggested treating the most-connected possibilities as the most leveraged. Retrieval showed that is a restatement of the rejected `poss:ranked-possibility-backlog`, so it was not recorded as new.

**Plan PR 4 (exploration guidance and first construction-time reconciliation).** Funnel section 4 now recalls retained possibilities before breadth, marks observations restated, revised or new, and retains only consequential ones; `strategic-repository-analysis` section 1B, the steward's architecture-exploration reference, knowledge contract ("Product possibility records") and reconciliation reference carry matching hooks. Building it was itself the first use of construction-time reconciliation: `workspace-impact` against `main@274e585` flagged 6 records citing the funnel, its uncited-path list led to 3 more affected possibilities, and the records were revised with their earlier assessments kept in `history` and a superseded observation.

**Lesson applied (from QY-11).** Evidence matches by file, so a record that cites this library while its origin lies elsewhere is flagged by every library edit. Records now cite the library only where it is their record of origin or the subject of their realization.

None of these syntheses is selected, prioritized or authorized.

**Prospective reasoning (2026-10-28).** The reference case on `poss:target-repository-discovery-memory` is encoded in `.sensemaking/knowledge/prospective-reasoning.json`: four `arch:` options, six `conseq:` consequences, two observed premises and three assumptions. `explain` on the possibility returns its options; on an option, its consequences, reused capabilities and alternatives. The derived `poss:repository-local-prospective-decision-memory` is linked back to its consequence. Vocabulary findings are in `docs/semantic-architecture/prospective-reasoning-competency-v1.md`.

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

Plan PR 1, the smallest useful part of PR 2, PR 3, PR 4 and the guidance part of PR 7 are built. The [plan](superpowers/plans/2026-10-28-product-possibility-idea-library.md) remains the reference for their intent; any further increment still needs selection against current source and authority. Observations so far:

- **PR 2 remainder:** most reservoir entries are `NOT_ASSESSED` here. Extend only where a decision needs them.
- **PR 5:** the questions tried so far were answered by `search`, `explain`, `impact`, `contradictions`, `workspace-impact` and `changes`. Filtering by dimension is the first gap that would justify new retrieval, and only once the set is too large to read.
- **PR 6:** no schema change is warranted yet. The awkward encodings (`extends`, `complements`, `alternativeTo`, relation establishment, dimensions) lose no answer at the current scale.
- **PR 7:** reconciliation now runs through the existing `workspace-impact` query plus the uncited-path list; its value depends on records citing the files that realize them.
- **Beyond the plan:** `poss:target-repository-discovery-memory` is the largest recorded opportunity to give possibility memory value outside this repository. It is `EXPLORATORY`; adopting it would change the portable Skill and needs its own selection.
