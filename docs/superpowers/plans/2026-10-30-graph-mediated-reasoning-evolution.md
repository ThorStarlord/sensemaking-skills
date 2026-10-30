# Sensemaking-skills — Knowledge Graph Reasoning Evolution Plan

**Status:** Owner-supplied implementation plan — approved strategic direction; recorded for construction
**Date:** October 30, 2026
**Target:** `ThorStarlord/sensemaking-skills`
**Inspected baseline:** `main@f73ed7b`
**Strategic scope:** Level 3 — Strategic Repository Evolution
**Governing decisions:** ADR 0029, ADR 0031, ADR 0034

---

## 1. Executive decision

### 1.1 Strategic objective

Evolve Sensemaking-skills from a system capable of storing and retrieving structured repository knowledge into a system that helps coding agents **reliably use accumulated knowledge to understand software, evaluate possibilities, reason about consequences, make warranted decisions, and preserve useful learning across sessions**.

Three development objectives remain distinct:

| Objective | Current state | Program treatment |
|---|---|---|
| O1. Build the knowledge graph | Implemented; partial coverage | Preserve and maintain |
| O2. Improve completeness and expressiveness | Ongoing | Develop selectively in response to reasoning needs |
| O3. Improve agent reasoning using the graph | Main unresolved product opportunity | Primary development priority |

These objectives are mutually reinforcing rather than three sequential completion gates.

### 1.2 Selected construction direction

**Select: Skill-native graph-mediated reasoning.**

Retain the existing agent-native controller and persistent Git-authored knowledge infrastructure.

The system should improve through the recurring relationship:

**Real question → relevant knowledge → source verification → reasoning → warranted conclusion → consequential knowledge reconciliation.**

This describes the product's learning relationship, not a mandatory execution pipeline.

### 1.3 Decisions established for this plan

1. `using-sensemaking` remains the sole public semantic controller.
2. `repository-semantic-steward` continues to own graph retrieval, RELATE, BOOTSTRAP, AUDIT and RECONCILE responsibilities.
3. No second graph database, inference engine, semantic controller or automatic workflow router is introduced.
4. Existing source-grounded query operations are reused before new retrieval infrastructure is considered.
5. Ontology expansion requires a demonstrated inability to represent decision-relevant knowledge, not simply an opportunity to add new types.
6. Continuous Construction remains the development approach. Normal engineering work produces both useful capabilities and learning.
7. Independent qualification is not a prerequisite for every construction increment. Claims of independent effectiveness nevertheless require independent evidence.
8. ADR 0032 and ADR 0033 remain in their existing proposed states; this plan does not silently ratify them.
9. Implementation work stays in Sensemaking-skills unless a separate target repository is explicitly authorized.

### 1.4 Explicit non-goals

The program will not attempt complete extraction of all repository knowledge, universal automated dependency inference, vector-search infrastructure without an observed retrieval need, numerical confidence scoring of semantic truth, mandatory ontology rebuilding before each task, or automatic strategic selection by deterministic software.

It will also avoid creating a new artifact type when existing analysis outputs, authored knowledge records and receipts already carry the needed information.

---

## 2. Baseline and architecture

The inspected repository currently contains seven authored knowledge files with 143 claims and 176 relations. These numbers describe the authored graph, not every mechanically indexed record.

Implemented capabilities include:

- Git-revision-bound source ingestion and SQLite snapshots.
- Typed claims, relations, epistemic status and source references.
- Search, explain, why, impact, contradictions, history and changes queries.
- File-oriented `context-for`, `rules-for` and workspace-aware retrieval.
- Ontology-first repository entry and possibility exploration.
- Prospective architectural synthesis and consequence modeling.
- Session and query receipts.
- RELATE, including declared/implemented/exercised/graph reconciliation.

Important limitations remain:

- Literal retrieval can miss relevant terms or differently named identifiers.
- File-level context depends on actual knowledge anchors and authored relationships.
- Declared graph links do not establish complete software dependencies or causal consequences.
- The latest RELATE refinements have not yet demonstrated fresh-host native behavior.
- Cross-session knowledge benefit has a positive but narrow, non-replicated signal.
- Skill installation, source-file parity and the version a host actually loads are distinct observations.

### Target architecture

The existing components retain their responsibilities:

| Component | Responsibility |
|---|---|
| `using-sensemaking` | Understand the goal, judge whether knowledge matters, compose reasoning, decide and stop |
| Semantic knowledge query layer | Return bounded, revision-aware, explicitly supported graph information |
| Repository Semantic Steward | Bootstrap, retrieve, verify, reconcile and maintain consequential knowledge |
| Strategic Repository Analysis | Explore repository futures, compare paths and select justified strategic dispositions |
| Architecture exploration | Analyze structural options, assumptions, constraints and conditional consequences |
| Strategic reconciliation | Reassess earlier claims and directions against new evidence |
| Receipts and durable artifacts | Preserve attributable continuation evidence without becoming semantic authority |

**Invariant:** A retrieved relationship is evidence for interpretation, never automatic authority to act.

---

## 3. Implementation work packages

### WP-0 — Strategic continuity and plan integration

**Priority:** P0
**Purpose:** Place the new reasoning emphasis within the existing authoritative strategy without incorrectly declaring a product pivot.

**Tasks**

1. Re-read the October 23 Strategic Repository Analysis, October 24 reconciliation, ADR 0031, ADR 0034 and current STATUS.
2. Determine whether the new evidence warrants a revised Level-3 Strategic Frontier or a narrower continuation update.
3. Preserve the existing PATH-1 knowledge-accretion mechanism while making effective agent reasoning its immediate value criterion.
4. If materially warranted, create a successor Strategic Repository Analysis using the current version-2 contract and explicit continuity with the previous analysis.
5. Otherwise, record a bounded strategic reconciliation that captures the revised emphasis without pretending the whole strategy was reopened.
6. Add this implementation plan to the repository's planning documents and update STATUS only where its current projection changes.

**Proposed files**

- `docs/superpowers/plans/2026-10-30-graph-mediated-reasoning-evolution.md`
- `artifacts/history/` — a successor strategic analysis or reconciliation, when warranted
- `STATUS.md`
- Relevant planning references, only where needed

**Acceptance**

The next agent can determine the governing direction, why reasoning is the development priority, which existing capabilities it reuses, what remains unproven and which first responsibility is warranted.

Historical analysis is not overwritten.

**Boundary:** No new Level-4 ADR is required unless the work actually proposes changing the accepted product thesis.

---

### WP-1 — Decision-relevant graph activation

**Priority:** P0
**Purpose:** Improve when and why agents consult existing knowledge.

**Current problem**

A graph can contain the right information while an agent still reconstructs the decision from scratch or makes an unsupported inference without consulting it.

**Tasks**

1. Review the current RECALL, ontology-first entry and adaptive-composition guidance.
2. Identify the smallest missing instruction, if any, that prevents graph retrieval when it could alter a consequential decision.
3. Clarify the distinction between a task that benefits from retained knowledge and a routine local edit that should proceed directly.
4. Make the supported retrieval choice explicit:
   - known claim ID → `explain` or `why` where applicable;
   - source file or file set → `context-for`;
   - architecture constraints → `rules-for`;
   - uncertain terminology → bounded `search`, followed by source inspection;
   - proposed impact → `impact`, treated only as declared-edge candidates.
5. Require the agent to examine the governing original sources before relying on a material claim.
6. Make knowledge unavailability and source-only fallback legitimate outcomes.
7. Ensure a recorded prior next step is re-warranted rather than followed merely because it appears in a receipt.

**Proposed files**

- `skills/using-sensemaking/SKILL.md` — only if a short core trigger is necessary
- `skills/using-sensemaking/references/adaptive-skill-composition-v1.md`
- `skills/using-sensemaking/references/ontology-first-entry-v1.md`
- `skills/repository-semantic-steward/references/recall.md`

**Acceptance**

An agent can explain why relevant knowledge was retrieved, how it applies to the decision, what source checks remain necessary and when further retrieval is unnecessary.

Routine edits remain lightweight.

**Guardrail:** Do not create a mandatory graph consultation stage or another query-planning Skill.

---

### WP-2 — Relational reasoning reliability

**Priority:** P0
**Purpose:** Build upon the RELATE capability already integrated in PRs #668 and #669.

**Current problem**

The agent may mistake a missing graph relationship for a missing product relationship, or overstate a recorded relationship beyond the evidence supporting it.

**Tasks**

1. Treat the October 30 RELATE implementation as the baseline, not as a feature that needs to be rebuilt.
2. Select a genuine unresolved relationship question outside the already-corrected receipt/Campaign case.
3. Inspect the relevant graph claims and their original source references.
4. Reconcile four evidence dimensions: declared contract, implemented behavior, exercised behavior and reviewed graph.
5. Distinguish `OVERSTATED`, `ABSENT_IN_SCOPE`, `IMPLEMENTATION_GAP`, `BOUNDARY`, `HOLDS` and `UNRESOLVED` according to the current procedure.
6. Confirm that the remaining uncertainty is routed correctly: source inspection, knowledge correction, ratification, owner intent or authority boundary.
7. Review both positive and negative product claims.
8. Make only corrections revealed by the use case.

**Proposed files**

- `skills/repository-semantic-steward/references/relational-reconciliation.md`
- `skills/using-sensemaking/SKILL.md`, only if a real controller defect remains
- `.sensemaking/knowledge/architecture.json`, if actual source-grounded corrections are warranted
- A normal-use receipt or report for the investigated case

**Acceptance**

The agent neither turns an unmodeled relationship into a false architectural absence nor treats a recorded positive edge as stronger than its source.

The RELATE verdict returns to the controller; it never becomes an autonomous recommendation or authorization.

**No-change condition:** If the current RELATE implementation already handles the new case correctly, preserve the observation and do not manufacture another code or Skill change.

---

### WP-3 — Decision-context retrieval and reachability

**Priority:** P1
**Purpose:** Ensure agents can recover the knowledge necessary to reason about a particular engineering question.

**Current problem**

File ownership can be well represented while a decision's alternatives, governing contracts, verification relationships or history remain unreachable from the files involved.

The Atlas application demonstrated this failure before targeted anchoring repaired it.

**Tasks**

1. Choose an authentic engineering responsibility involving more than one relevant source file or architectural boundary.
2. Query the existing graph from those file paths and from any known decision identifiers.
3. Record which relevant knowledge is returned and which categories are `NOT_ASSESSED`.
4. Compare the retrieved context with source documents and the relevant code.
5. Classify observed gaps:
   - a missing authored record;
   - a missing source-grounded relation;
   - a missing path anchor;
   - a query-selection problem;
   - a retrieval-consumer limitation;
   - or knowledge that is appropriately outside the bounded query.
6. Correct authored knowledge before changing the query implementation when the problem is genuinely missing knowledge.
7. Modify retrieval code only when a real consumer needs a mechanically expressible capability that the current interface cannot supply.
8. Retain explicit limits, truncation information, currentness and provenance.

**Potential implementation locations**

- `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py`
- `src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py`
- `src/sensemaking_skills/semantic_architecture/knowledge_store.py`
- `src/sensemaking_skills/semantic_cli.py`
- `.sensemaking/knowledge/*.json`

**Acceptance**

For the selected real responsibility, the agent can retrieve relevant governing context, distinguish genuinely represented relationships from missing coverage, and identify the source documents that settle the consequential question.

Multi-file queries preserve each file's independent coverage limits.

**Non-goals:** No new semantic similarity backend, automatic relevance scoring, arbitrary-depth inference or claim of graph completeness.

---

### WP-4 — Prospective reasoning with accumulated knowledge

**Priority:** P1
**Purpose:** Make retained repository knowledge useful for reasoning about possible futures, not only explaining existing architecture.

**Tasks**

1. Select an actual repository-level product or architecture question with materially different plausible outcomes.
2. Recover existing product goals, non-goals, constraints, decisions, alternatives and possibilities.
3. Examine relevant existing system relationships before generating proposals.
4. Explore options sufficiently broadly to avoid selecting the easiest implementation by default.
5. Use existing `ArchitectureOption`, `ConsequenceHypothesis` and strategic-path representations where their distinctions matter.
6. Distinguish present architecture, proposed architecture, conditional consequences and actual implementation.
7. Explore meaningful second-order effects across system boundaries.
8. Identify assumptions that would materially change the preference.
9. Use the existing architecture-synthesis and strategic-analysis artifacts instead of producing a new reasoning artifact.
10. Return the comparison to the active controller for a recommendation, further inquiry, justified no-change or separately authorized construction.

**Proposed files**

- `skills/repository-semantic-steward/references/architecture-exploration.md`
- `skills/repository-semantic-steward/references/architectural-synthesis-template.md`
- `skills/using-sensemaking/references/adaptive-skill-composition-v1.md`
- `skills/strategic-repository-analysis/SKILL.md`
- Applicable prospective knowledge records, when durable retention is justified

**Acceptance**

A real reasoning episode produces a source-grounded comparison in which recovered knowledge affects the interpretation of at least one materially relevant assumption, option, consequence or decision boundary.

A justified confirmation of an existing direction counts when the evidence genuinely strengthens or corrects the rationale; an artificial change of direction is not required.

**Guardrail:** A hypothetical consequence chain does not establish causal certainty. The controller must preserve conditionality at every consequential link.

---

### WP-5 — Knowledge enrichment through reasoning and construction

**Priority:** P1
**Purpose:** Connect Objective 2 directly to Objective 3.

**Tasks**

1. Inspect the knowledge gaps encountered in WP-2 through WP-4.
2. Distinguish missing information from missing ontology expressiveness.
3. Add or revise reviewed knowledge only when the record improves future reconstruction or reasoning.
4. Prefer existing claim kinds and predicates before proposing a schema change.
5. Connect consequential records to actual source owners, governing decisions, contracts and verification evidence.
6. Preserve rejected alternatives when their rationale could affect a later decision.
7. Preserve superseded and invalidated knowledge as history rather than silently rewriting the past.
8. Reconcile source changes with the applicable knowledge records.
9. Validate proposals and build an updated index at the appropriate clean committed revision.
10. Use a later query to confirm the new knowledge is reachable through an actual consumer path.

**Likely target files**

- `.sensemaking/knowledge/architecture.json`
- `.sensemaking/knowledge/domain.json`
- `.sensemaking/knowledge/possibilities.json`
- `.sensemaking/knowledge/prospective-reasoning.json`
- `.sensemaking/knowledge/stewardship.json`

**Acceptance**

The new or revised knowledge supports a real question better than the previous graph and remains attributable to the appropriate source authority.

No minimum claim count, edge count or graph-density threshold applies.

**Schema-evolution condition:** Add a new ontology construct only when an explicit competency question cannot be answered with the existing vocabulary, and when an actual consumer needs the distinction.

---

### WP-6 — Cross-session continuity and reliable Skill consumption

**Priority:** P1
**Purpose:** Ensure the reasoning capabilities and knowledge can be recovered by later coding agents.

**Current problem**

Source files, installed Skill copies, loaded host instructions, durable receipts and retained knowledge can represent different revisions or different levels of persistence.

**Tasks**

1. Preserve source revision and worktree identity for consequential retrieval.
2. Check whether the active host actually loaded the expected Skill, rather than assuming that matching installed files establish native invocation.
3. Use the existing manual-load fallback when native Skill invocation is unavailable, reporting it accurately.
4. Confirm that a returning agent can locate previous knowledge, source references and relevant decision artifacts.
5. Make the existing query and session receipts useful for reconstruction, without turning them into a new knowledge database.
6. Keep the distinction between write-time persistence declarations and current Git durability.
7. Report stale, missing or unreachable knowledge and loaded-instruction uncertainty.
8. Avoid changing external user-level Skill installations without applicable authorization.
9. Review whether a material prior decision can be reconstructed without the previous conversation.

**Proposed files**

- Existing `using-sensemaking` continuation references
- Existing Steward RECALL and query-receipt guidance
- Existing session receipt documentation and consumers, only if a demonstrated defect exists
- `CLAUDE.md` or `AGENTS.md` only for relevant repository-local discovery guidance

**Acceptance**

A fresh session can recover the selected repository context and known limitations through its actual available tools, without assuming that a prior agent's conversation memory survives.

The system reports native loading, manual loading and unavailable invocation as different observations.

---

### WP-7 — Normal-use evidence and independent qualification

**Priority:** P2 — after useful construction increments
**Purpose:** Establish what improvement in agent reasoning has actually been demonstrated.

This package is divided into two evidence levels.

**Level A — Ordinary construction evidence**

Use the real engineering responsibilities undertaken during WP-1 through WP-6.

For each consequential case, record:

- the engineering question;
- relevant source and graph knowledge;
- what the agent concluded;
- any knowledge correction or decision change;
- what additional reasoning was necessary;
- remaining uncertainty and cost;
- whether the result was retained and reachable.

No synthetic benchmark is required to continue normal construction.

**Level B — Independent comparative qualification**

When an appropriate executor and isolation environment are available:

1. Select a genuine decision question before running a comparison.
2. Pin the target repository revision, Skill revision and host configuration.
3. Compare a returning agent with access to retained reviewed knowledge against an appropriately matched source-only condition.
4. Ensure the conditions do not leak treatment-specific knowledge.
5. Record actual loading, queries, source inspections, relevant actions, final outputs and interruptions.
6. Use independent assessment when making comparative claims.
7. Compare substantive reasoning, unsupported claims, missed evidence, time and context cost.
8. Distinguish a better answer from merely making more Skill invocations.
9. Retain the evidence and explicitly state the level of confidence warranted by it.

**Dependencies**

The October 29 decision-observability qualification was stopped during preflight because the available environment did not establish the required credential isolation. Do not bypass that protection to produce experimental evidence.

If a suitable executor remains unavailable, preserve the dependency as open. Continue authorized construction rather than treating incomplete independent qualification as product failure.

**Acceptance**

A later agent demonstrates defensible reuse or correction of consequential prior knowledge in a fresh context. Comparative superiority is claimed only if the evidence supports it.

---

## 4. Incremental PR plan

The work packages should be implemented in reviewable slices, without requiring one PR per conceptual section when overlap makes a smaller combined change more coherent.

| PR | Proposed scope | Dependency | Expected output |
|---|---|---|---|
| PR-A | Strategic continuity and approved development plan | Current source and owner direction | Durable Level-3 direction and implementation plan |
| PR-B | Decision-relevant RECALL activation | PR-A | Controller/Steward guidance for selective use of knowledge |
| PR-C | RELATE application to an independent real relationship question | PR-B | Source-grounded verdict, knowledge correction if needed |
| PR-D | Decision-context reachability and bounded retrieval repair | PR-B; findings from PR-C where relevant | Better real task context or a justified no-change conclusion |
| PR-E | Prospective reasoning and adaptive composition during a real architecture question | PR-B–D as relevant | Architecture synthesis with decision-relevant graph use |
| PR-F | Reviewed knowledge reconciliation and source anchoring | Results of PR-C–E | Corrected, queryable retained knowledge and provenance |
| PR-G | Cross-session discovery and continuity corrections | PR-B–F; actual host evidence | Reliable, accurately reported continuation behavior |
| PR-H | Independent qualification when safe and available | Stable relevant construction; isolated executor | Evidence-backed qualification report and limits |

**PR-C, PR-D and PR-G are conditional implementation slices.** If a genuine use case reveals no defect or missing capability, record the finding and do not manufacture a patch.

PR-H is a separate qualification milestone, not a condition that prevents continued construction of the earlier work packages.

### Recommended implementation order

Start with PR-A and PR-B. Then undertake a genuine engineering responsibility that can exercise relational verification and decision-context retrieval together.

From that use, prioritize PR-C and PR-D according to the actual weakness discovered. Continue to PR-E without waiting for complete graph coverage. PR-F should reconcile consequential knowledge as the work produces it, not as one large delayed cleanup.

Improve continuity and host integration through PR-G where evidence warrants it. Conduct PR-H once the necessary conditions exist.

This order gives the coding agent a clear default while preserving the freedom to skip, combine or revisit increments when new evidence changes the correct responsibility.

---

## 5. Verification and evidence policy

Follow the repository's current `CLAUDE.md` construction policy.

For current Sensemaking-skills construction PRs, do not add or manually run local unit tests or synthetic evidence tests. Use source/diff inspection and applicable mechanical validators; report `NOT_RUN` accurately. Preserve hosted CI, required checks, branch protections and release gates.

Examples of existing checks to reuse when relevant:

- Skill hygiene and documentation-currentness validation for changed Skill guidance.
- `semantic knowledge-proposal-check` for modified authored graph records.
- Receipt validation for created or updated session/query receipts.
- Artifact validation for new architectural syntheses or strategic analyses.
- `git diff --check` and reviewed source differences.
- Exact-revision index rebuilding and retrieval when knowledge changes are integrated.

A mechanically valid artifact does not establish correct semantic reasoning. A successful query does not prove the agent used the retrieved result. A merged PR does not establish release qualification or comparative benefit.

The current repository-specific prompt-merge and no-local-unit-tests policy should remain local to Sensemaking-skills; do not export it to external target repositories.

---

## 6. Milestones and exit criteria

### M1 — Strategic alignment

The repository accurately represents the approved priority: improving agent reasoning with existing knowledge while selectively enriching the ontology.

**Evidence:** durable strategic continuity record and current plan.

### M2 — Relational reliability

The agent appropriately distinguishes missing graph representation, contract definition, implemented behavior, actual use and genuine unresolved architecture questions.

**Evidence:** real source-grounded RELATE application beyond the original corrected case.

### M3 — Decision-context usefulness

Existing graph queries provide materially useful context for an authentic engineering decision, or expose a specific correctable reachability problem.

**Evidence:** query/source correspondence and an attributable decision outcome.

### M4 — Prospective reasoning usefulness

The agent uses repository knowledge to examine alternatives, assumptions or cross-system consequences in a way that improves the defensibility of a recommendation.

**Evidence:** architecture synthesis, referenced prior knowledge and a clear explanation of its actual contribution.

### M5 — Knowledge compounding readiness

The consequential lesson is retained, currentness-aware, and recoverable through the ordinary knowledge access path.

**Evidence:** reviewed authored records and subsequent retrieval against the correct revision.

### M6 — Independent qualification

A genuinely separate session demonstrates a source-grounded benefit from retained knowledge or corrects it, with evidence limits and total cost reported.

**Evidence:** admissible independent-session record; stronger comparative conclusions require corresponding comparative evidence.

---

## 7. Strategic risks and responses

| Risk | Response |
|---|---|
| Graph volume grows faster than practical usefulness | Select enrichment from observed decision needs |
| Agent treats absence from graph as absence from product | Apply RELATE and verify original sources |
| Agent treats recorded claims as certain or authoritative | Preserve epistemic status, source scope, currentness and authority |
| Agent performs unnecessary specialist calls | Keep activation decision-relevant and adaptive |
| Prospective graph traversal becomes false causal inference | Retain conditional assumptions and require source-supported links |
| Reconciliation creates excessive documentation | Preserve only knowledge consequential to future reasoning |
| New query machinery duplicates existing facilities | Require a demonstrated consumer and missing capability |
| Host loads stale Skill text | Distinguish repository, installed and observed loaded revisions |
| Qualification delays construction | Separate normal-use learning from independent comparative claims |
| The agent returns repeatedly to receipt maintenance | Reassess product value and avoid treating historical receipts as an automatic backlog |

---

## 8. Program-wide definition of done

The construction program is sufficiently mature when a coding agent can, through ordinary Sensemaking use:

1. Understand the actual repository goal and the consequential decision being supported.
2. Discover and retrieve relevant prior knowledge when warranted.
3. Verify important knowledge against authoritative and current original sources.
4. Recognize missing coverage, contradictions and overstated relations.
5. Explore material alternatives and relevant conditional consequences.
6. Reach a qualified recommendation, selection, justified no-change or appropriate escalation.
7. Explain which existing knowledge materially contributed.
8. Retain useful corrections and lessons through the established knowledge and receipt surfaces.
9. Enable later agents to recover that information without depending on conversation memory.
10. Preserve the boundary between evidence, semantic judgment, execution authority and publication.

This does not require complete ontology coverage, guaranteed superiority on every task or mandatory implementation.

Independent, longitudinal effectiveness remains a distinct qualification objective.

---

## 9. First execution responsibility

**Recommended starting responsibility:** Integrate the approved strategic emphasis into the current Level-3 state, then improve the agent's selective use of graph knowledge during an authentic consequential engineering question.

The first technical intervention should not be another ontology extension or another query operation by default.

It should begin by checking whether the existing controller, RECALL, RELATE and context-retrieval procedures are sufficient for a genuine decision. Build the smallest missing capability or correct the smallest consequential knowledge defect revealed by that work.

Proceed through subsequent warranted, authorized increments using the existing source review, integration and continuation rules.

### Final construction principles

**It is not about accumulating more graph records; it is about making accumulated knowledge useful for consequential reasoning.**

**It is not automatic inference and it is not mandatory process choreography; it is agent-owned judgment grounded in retrievable, verifiable knowledge.**

**Knowledge that changes and improves future decisions is the actual product capability.**
