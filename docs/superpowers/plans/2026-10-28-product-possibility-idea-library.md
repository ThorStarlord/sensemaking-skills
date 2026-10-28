> **Repository record (2026-10-28).** Owner-supplied program plan, preserved verbatim below from the owner's message in the session that built its first increment.
> **Status:** proposed program plan. It grants no authority beyond what its own section 11 states; each later increment is selected against current source and authority.
> **Inspected base:** `ThorStarlord/sensemaking-skills` `main@d0af33beb52e94b375d6a471e9990df11c8c424d`.
> **First increment built:** PR 1 and the smallest useful part of PR 2, in the change that added this file: [`../../semantic-architecture/product-possibility-ontology.md`](../../semantic-architecture/product-possibility-ontology.md), competency questions section M, and [`../../idea-library.md`](../../idea-library.md).
>
> **Reconciliation with the repository at that base.** The plan text below is unchanged; these notes record how it was applied.
>
> - The illustrative PQ-01 to PQ-10 are CQ-079 to CQ-088, in the same order (`docs/semantic-architecture/competency-questions.md`, section M).
> - Relation names: the conceptual dictionary uses camelCase (`potentiallyEnabledBy`, `alternativeTo`, ...), like the existing Level-2 relations. The plan's snake_case names denote the same relations; snake_case stays reserved for predicates `knowledge.py` accepts.
> - Epistemic status: documentary claims use the Level-2 statuses in `relations-and-epistemics.md`; typed records use the executable statuses, as section 3.2.D intends.
> - "Opportunity" exists as an executable claim kind, not as an `ontology.md` concept; the conceptual model says so rather than adding it.
> - The reservoir's lifecycle labels in `docs/strategic-candidate-directions.md` are read into the dimensions (conceptual model, section 4.8), not replaced.
> - Owner reconciliation before merge (2026-10-28): ambition and horizon are separate dimensions (six in total); relation endpoints follow `ontology.md`, so a possibility is distinct from its realized capability and construction paths and evidence prerequisites are not possibilities; observed implementation evidence is kept apart from inferred realization judgments; an originating document governs its own historical record while the latest applicable accepted authority governs current commitments; counterfactual exploration needs no Level-4 review unless a thesis commitment becomes decision-changing; `NOT_IMPLEMENTED` needs a completeness basis.
> - For PR 4, `skills/strategic-repository-analysis/SKILL.md` section 1B already recalls goals, decisions and relationships before path comparison.

# Product Possibility Ontology & Idea Library v1
## Detailed Development Plan — Sensemaking Skills

**Status:** Proposed implementation plan  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Product direction:** Persistent Semantic Stewardship, ADR 0031  
**Development approach:** Value-directed continuous construction  
**Primary objective:** Preserve and develop the product's long-term possibility space across coding-agent sessions without turning speculative ideas into an automatic backlog or strategic authority.

---

## 1. Product objective

### 1.1 Problem

Sensemaking Skills already supports repository understanding, strategic exploration, responsibility selection and cumulative engineering knowledge.

However, several limitations remain in how these capabilities work together:

1. An agent can converge on a locally justified responsibility without adequately considering the product's wider possible futures.
2. Divergent exploration can generate valuable alternatives and relationships that remain primarily in one conversation or analysis artifact.
3. Previously rejected, deferred or superseded possibilities may lose their original rationale or become difficult to rediscover.
4. Existing capabilities are not consistently connected to the new futures they could enable.
5. A future coding agent may reconstruct the current product but fail to reconstruct the intellectual development of its possible future.

The objective is to address these limitations while preserving the established distinction between exploration, strategic decision-making and implementation authority.

### 1.2 Desired capability

A fresh coding agent should be able to answer:

- What is currently implemented?
- What future capabilities and product directions have been considered?
- Which ideas are compatible with the current strategy?
- Which ambitious or counterfactual futures challenge current assumptions?
- Which possibilities depend on, complement, contradict or supersede others?
- Why was an idea previously deferred or rejected?
- Have changes in the product made a previously impractical idea plausible?
- What genuinely new possibilities can be synthesized from the existing landscape?

The system should preserve useful answers and relationships between sessions.

### 1.3 Definition of success

The first meaningful success is not a populated database.

It is a later agent recovering an earlier possibility and its reasoning, connecting it to current implementation evidence, and using that understanding to discover or assess a consequential future product direction.

This demonstrates usefulness at the observed scope, not general superiority or autonomous strategic intelligence.

---

## 2. Architectural decisions

The following design decisions are recommended for the initial program.

| Decision | Selected approach |
|---|---|
| Ontological home | Extend the existing Product and Knowledge ontology |
| User-facing capability | Idea Library |
| Canonical semantic concept | ProductPossibility, provisionally |
| Knowledge storage | Reuse Git-authored semantic knowledge |
| Search and retrieval | Reuse the existing SQLite index and query interfaces first |
| Idea generation | Extend the use of existing divergent exploration |
| Historical memory | Preserve consequential decisions, alternatives and reconsideration conditions |
| Selection authority | Remains with the active agent and applicable owner decisions |
| Strategic relationship | Input to Level 3, not a replacement for the Strategic Frontier |
| Initial scope | `sensemaking-skills` itself |
| New Skill | Not initially required |
| New database/runtime | Not initially required |
| Product-thesis revision | Not part of this program |

The proposed extension fits the selected ADR 0031 direction. That strategic fit does not itself authorize every implementation detail or any future Level-4 thesis revision.

### 2.1 Source-of-truth rule

Preserve the existing hierarchy:

- `docs/product-strategy.md` and accepted ADRs govern product intent.
- `STATUS.md` projects current Level-3 strategic state.
- `docs/strategic-candidate-directions.md` preserves existing exploratory history.
- Git-authored knowledge records preserve reviewed semantic claims and relationships.
- The SQLite index is rebuildable retrieval infrastructure, not normative authority.

**Do not create two independently maintained authoritative idea catalogs.**

Existing candidate documentation should remain source material. New idea records should have stable origins, and typed representations should reference rather than silently replace those origins.

---

## 3. Ontology design

### 3.1 Introduce ProductPossibility at the conceptual level

Define:

**ProductPossibility:** A retained representation of a potential future product state, capability, product change or strategic direction, together with its value hypothesis, assumptions, relevant relationships and historical disposition.

It does not imply feasibility, endorsement, implementation or authorization.

Place it in Layer 6, the Product Ontology, and connect its claims to Layer 4, the Knowledge and Epistemic Ontology.

Reuse existing concepts rather than redefining them:

| Existing concept | Relationship to ProductPossibility |
|---|---|
| ProductCapability | A possible future capability or a currently realized prerequisite |
| ProductChange | A proposed or implemented modification that may realize a possibility |
| Initiative | A coordinated effort that may advance a selected possibility |
| Opportunity | A product or engineering need motivating the possibility |
| Hypothesis | A defeasible claim about the possibility's value, feasibility or consequences |
| Alternative | A competing means or future direction |
| Decision | Records selection, deferral, rejection or another authorized disposition |
| Evidence | Grounds claims about the existing state or observations |
| Constraint | Limits what may be implemented under current authority |

Avoid equating a possibility with a feature, backlog item or implementation task.

### 3.2 Use independent descriptive dimensions

Each retained possibility should support these conceptual dimensions.

**A. Strategic alignment**

- `ALIGNED`: compatible with currently accepted intent.
- `ADJACENT`: plausible extension requiring additional scope clarification.
- `COUNTERFACTUAL`: explores an explicitly altered premise.
- `CONFLICTS_WITH_CURRENT_STRATEGY`: incompatible with an accepted commitment.
- `NOT_ASSESSED`: no adequate alignment judgment exists.

**B. Ambition and horizon**

- `INCREMENTAL`
- `SUBSTANTIAL`
- `TRANSFORMATIVE`
- `LONG_HORIZON`

These categories describe scope or aspiration, not priority or quality.

**C. Realization state**

- `NOT_IMPLEMENTED`
- `PARTIALLY_IMPLEMENTED`
- `IMPLEMENTED_BASELINE`
- `SUPERSEDED_BY_IMPLEMENTATION`
- `NOT_ASSESSED`

Implementation claims require source-inspected code, contracts or suitable observed behavior. Documentation alone does not establish operational completeness.

**D. Epistemic status**

Continue using the existing typed knowledge statuses where represented: `declared`, `observed`, `hypothetical`, `contested`, `superseded` and `invalidated`.

Do not create a conflicting epistemic enum merely for the library. Owner ratification and action authorization remain independently recorded.

**E. Strategic disposition**

- `EXPLORATORY`
- `FRONTIER_CANDIDATE`
- `SELECTED`
- `DEFERRED`
- `REJECTED_FOR_NOW`
- `SUPERSEDED`

These reflect historical decisions or assessments. They do not automatically change when another field changes.

### 3.3 Identity and provenance

Each possibility needs:

- A stable identifier that survives title changes.
- A clear statement of the proposed future.
- Its origin and original author or source.
- Relevant product objective.
- Value hypothesis.
- Material assumptions.
- Referenced capabilities and evidence.
- Assessment scope and relevant revision.
- Historical dispositions and their rationale.
- Conditions for reconsideration.

Use stable identifiers such as `poss:cross-episode-synthesis`, subject to the repository's existing ID contract.

Do not generate identity solely from the current wording of a proposal.

---

## 4. Relationship ontology

Relationships are the distinctive product capability.

### 4.1 Initial conceptual vocabulary

| Relationship | Intended meaning |
|---|---|
| `potentially_enabled_by` | Another capability may supply a necessary prerequisite |
| `complements` | Two possibilities could produce greater value together |
| `alternative_to` | Different possibilities offer competing approaches to a related outcome |
| `conflicts_with` | Two directions or their assumptions may be incompatible |
| `extends` | One possibility broadens an existing capability or earlier possibility |
| `derived_from` | A possibility originated from another idea or source |
| `realized_by` | Implementation evidence identifies a capability realizing some or all of the proposed future |
| `supersedes` | A later proposal or decision replaces an earlier one for current reasoning |
| `shares_assumption_with` | Multiple possibilities depend on a common unresolved premise |
| `motivates_reconsideration_of` | New evidence makes an earlier disposition worth reviewing |

These are **proposed ontology relationships**, not currently accepted executable predicate names.

### 4.2 Representation policy

First use the existing claim types and supported relations where their meanings genuinely match.

For example, existing `derived_from`, `depends_on`, `implemented_by`, `supersedes`, `contradicts` and `references` may be sufficient for some relationships.

Do not misuse a strong causal `depends_on` relation merely to represent an interesting speculative association.

When the current vocabulary cannot preserve a consequential distinction, document the failed query and consider a small typed extension.

Do not use the existing generic `relates_to` predicate as an unqualified replacement for every relationship; its current schema has specific cardinality requirements.

### 4.3 Relationship evidence

Every material relationship should preserve:

1. Its semantic meaning.
2. The claims or ideas it connects.
3. Whether the relationship is observed, inferred or hypothetical.
4. Its original source or reasoning artifact.
5. Relevant assumptions and currentness.
6. The conditions under which it might no longer apply.

A relationship must not become an established dependency merely because two ideas are frequently mentioned together.

### 4.4 Recombination

Support the synthesis of new possibilities from multiple existing ones.

For example:

- Persistent knowledge enables historical retrieval.
- Divergent exploration produces alternatives.
- Strategic continuity preserves previous reasoning.
- Their combination suggests cross-episode possibility synthesis.

The resulting possibility must receive its own identity, hypothesis and provenance.

Recombination is not automatic acceptance.

---

## 5. Historical lifecycle and reconsideration

### 5.1 Preserve consequential history

An idea should not disappear merely because it was rejected, implemented or superseded.

Preserve the earlier assessment and link it to the new one.

This must be event- or revision-aware: do not overwrite the original conclusion with today's interpretation and make the outcome appear inevitable.

### 5.2 Distinguish rejection reasons

Examples include:

- Insufficient feasibility under current capabilities.
- Disproportionate implementation cost.
- Lower present opportunity value.
- Strategic incompatibility.
- Contradictory evidence.
- Better alternative available.
- Missing authorization.

A rejection reason is not necessarily a permanent property of the idea.

### 5.3 Reconsideration conditions

A consequential deferral or rejection may have a `revisit_when` description:

- A particular prerequisite is implemented.
- An earlier architectural constraint is removed.
- New consumer evidence appears.
- A historical assumption is contradicted.
- An accepted product strategy changes.
- Another possibility makes a previously expensive approach practical.

These are semantic conditions, not automatically scheduled jobs or implementation triggers.

### 5.4 Reconsideration process

When a relevant condition changes:

1. Retrieve the previous possibility and disposition.
2. Inspect the original evidence and reasoning.
3. Identify which premise may have changed.
4. Verify current source and authority.
5. Reassess the idea qualitatively.
6. Preserve the new assessment and its relationship to the old one.
7. Escalate to Level 3 or Level 4 only if the result warrants it.

The outcome may legitimately be `NO_CHANGE`.

---

## 6. Competency questions

Extend `docs/semantic-architecture/competency-questions.md` with a bounded new section, using the next available canonical identifiers.

Suggested questions:

**PQ-01 — Possibility recovery:** Which future directions have been considered for a product goal, including speculative and counterfactual directions?

**PQ-02 — Strategic alignment:** Which possibilities align with accepted intent, and which require changing an assumption or product boundary?

**PQ-03 — Realization:** Which parts of a possibility are actually implemented, partially implemented or absent from the inspected evidence?

**PQ-04 — Relationship retrieval:** What dependencies, alternatives, complementary capabilities and contradictions have been explicitly represented?

**PQ-05 — Historical rationale:** Why was a possibility previously selected, deferred, rejected or superseded?

**PQ-06 — Reconsideration:** Which previous assumptions or obstacles may have changed following recent construction?

**PQ-07 — Synthesis:** Which existing capabilities and possibilities could combine into a distinct future capability, and which relationships remain hypothetical?

**PQ-08 — Cross-session continuity:** Can a fresh agent reconstruct important possibilities and their relationships without the original conversation?

**PQ-09 — Governance:** Can an agent explore a thesis-conflicting possibility without mistaking its existence for authorization to pursue it?

**PQ-10 — Opportunity cost:** Does the current local construction responsibility advance the selected long-term direction, or is a materially different strategic option being overlooked?

The identifiers are illustrative until reconciled with the repository's current numbering.

Each ontology concept or new predicate should identify which competency question it helps answer.

---

# 7. Implementation roadmap

## PR 1 — Conceptual ontology and competency questions

**Purpose:** Establish unambiguous semantics before building storage or query features.

**Files to inspect or update:**

- `docs/semantic-architecture/ontology.md`
- `docs/semantic-architecture/competency-questions.md`
- `docs/semantic-architecture/relations-and-epistemics.md`
- `docs/semantic-architecture/product-change-taxonomy.md`

**Tasks:**

1. Define the proposed `ProductPossibility` concept and its boundary.
2. Map it to existing Product and Knowledge ontology concepts.
3. Define the independent descriptive dimensions.
4. Specify proposed relationship meanings and their epistemic boundaries.
5. Add the competency questions.
6. Explain how conceptual possibilities differ from the current Strategic Frontier.
7. Document why no new runtime or planner is required for this increment.

**Acceptance:**

- The model distinguishes speculative ideas, current capabilities and implementation evidence.
- Ambition, alignment, realization and authority cannot be confused.
- All introduced concepts have meaningful competency questions.
- Existing ontology concepts remain compatible.
- No executable schema migration is required.

**Deliverable:** Reviewed ontology extension and competency-question specification.

---

## PR 2 — Curated possibility landscape

**Purpose:** Produce the first genuinely useful idea library using existing repository evidence.

**Primary sources:**

- `docs/strategic-candidate-directions.md`
- `docs/product-strategy.md`
- `STATUS.md`
- Accepted ADRs
- Existing strategic analyses and historical decisions

**Tasks:**

1. Review the existing candidate reservoir.
2. Identify a representative set of consequential possibilities.
3. Include implemented baselines, partial capabilities, compatible future extensions, long-horizon proposals and thesis-challenging ideas.
4. Preserve the source and history of each selected possibility.
5. Record material dependencies, alternatives, combinations and contradictions.
6. Distinguish capabilities already present from proposals whose implementation remains hypothetical.
7. Avoid converting the entire historical catalog indiscriminately.
8. Produce a readable landscape and stable identifiers using the existing documents as source material.

**Suggested initial examples:**

- Persistent semantic knowledge as an accepted long-term direction.
- Git-authored knowledge and SQLite retrieval as implemented infrastructure.
- Cross-episode opportunity synthesis as a speculative extension.
- More ambitious strategic-memory capabilities as long-horizon possibilities.
- Automatic strategic planning as a counterfactual direction conflicting with current non-goals.

These examples must be reconciled against actual current sources before their statuses are recorded.

**Acceptance:**

- Every retained possibility has a meaningful description and provenance.
- The landscape includes more than only future backlog items.
- Implemented and unimplemented concepts are distinguishable.
- Important rejected or deferred directions retain their rationale.
- At least one consequential cross-idea relationship or synthesis is documented.
- No new source of normative strategy authority is created.

**Deliverable:** First source-grounded Idea Library, readable by another agent.

---

## PR 3 — Integrate selected possibilities into reviewed semantic knowledge

**Purpose:** Make the landscape recoverable through the existing semantic knowledge infrastructure.

**Relevant code and storage:**

- `src/sensemaking_skills/semantic_architecture/knowledge.py`
- `src/sensemaking_skills/semantic_architecture/knowledge_sources.py`
- `.sensemaking/knowledge/*.json`
- Existing semantic knowledge CLI and SQLite index

**Tasks:**

1. Inspect the current supported authored schema and relationship types.
2. Encode a useful subset of the curated possibilities using existing `opportunity`, `hypothesis`, `alternative` and `capability` claim kinds.
3. Add only relationships whose current predicate meanings are appropriate.
4. Preserve source references, epistemic status and authority separation.
5. Use stable identifiers that can survive future revisions.
6. Keep source-grounded proposal records distinct from implementation observations.
7. Confirm that the existing index can recover these claims without modifying the SQLite database schema.
8. Document representation gaps that genuinely prevent important competency questions from being answered.

**Important boundary:**

Do not introduce `kind: possibility` into the executable schema merely because the conceptual ontology uses `ProductPossibility`.

A new kind is justified only if existing representations repeatedly lose consequential information.

**Acceptance:**

- Reviewed records remain compatible with the supported authored-document versions.
- The index remains rebuildable.
- Existing records are not forced through a migration.
- Source and authority references are valid.
- A speculative possibility cannot masquerade as observed implementation.
- The current query tools retrieve the selected examples.

**Deliverable:** A useful initial typed possibility collection without a new database.

---

## PR 4 — Connect divergent exploration with possibility memory

**Purpose:** Make the library an active part of creative strategic reasoning rather than a passive archive.

**Likely integration points:**

- `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`
- `skills/repository-semantic-steward/references/architecture-exploration.md`
- `skills/repository-semantic-steward/SKILL.md`
- Relevant concise guidance in `skills/using-sensemaking/`

**Tasks:**

1. Add guidance for recovering relevant prior possibilities before open-ended strategic exploration.
2. Preserve both grounded and counterfactual divergent exploration.
3. Encourage discovery of missing relationships, capability combinations and alternative architectures.
4. Teach the agent to distinguish new possibilities from restatements of stored ones.
5. Reconcile consequential new ideas into durable knowledge where their reuse is worth the maintenance.
6. Preserve proposed relationships as hypotheses unless the appropriate evidence or authority establishes more.
7. End exploration-only requests with an opportunity landscape, not an automatically selected construction task.
8. Keep ordinary bounded engineering tasks free from mandatory full-landscape exploration.

**Recommended operating pattern:**

```text
RECALL relevant possibilities and actual capabilities
    |
    v
EXPLORE current, adjacent and counterfactual futures
    |
    v
RELATE alternatives, dependencies and combinations
    |
    v
SYNTHESIZE materially distinct new possibilities
    |
    v
RECONCILE consequential knowledge
    |
    v
STOP, or move to authorized strategic selection
```

**Acceptance:**

- Exploration can produce new ideas rather than only retrieve existing ones.
- Existing historical ideas are considered when relevant.
- The output distinguishes original ideas, newly generated combinations and established facts.
- Exploration does not force Level-3 reopening or implementation.
- No fifth Steward mode or new mandatory Skill is required.

**Deliverable:** Reusable Skill behavior connecting creative exploration with durable knowledge.

---

## PR 5 — Build useful idea-library queries, conditionally

**Purpose:** Make the library easy for fresh agents to navigate.

First inspect what can already be answered through:

- `knowledge-query --operation search`
- `knowledge-query --operation explain`
- `knowledge-query --operation history`
- `knowledge-query --operation changes`

Do not implement another query surface if these already meet the relevant needs at acceptable cost.

**Candidate read-only queries:**

| Query | Intended result |
|---|---|
| `possibilities_for_goal` | Possibilities linked to a product objective |
| `possibility_context` | Description, origin, history, relationships and evidence |
| `related_possibilities` | Explicitly represented complementary, alternative and competing ideas |
| `realization_context` | Related implemented capabilities and limits of supporting evidence |
| `reconsideration_candidates` | Historical deferrals whose stated assumptions may warrant reinspection |
| `possibility_changes` | Authored and source-linked differences across indexed revisions |

These are proposed contracts, not existing CLI operations.

If a dedicated query becomes warranted, it should:

- Remain read-only.
- Require explicit repository/revision identity.
- Return bounded and truncation-aware results.
- Preserve epistemic status and evidence links.
- Distinguish unassessed data from confirmed absence.
- Never infer strategic priority from graph position, connectivity or counts.
- Never turn a reconsideration candidate into automatic work.

**Acceptance:**

A fresh agent can recover a specific previously recorded possibility, its relationships and relevant history without reading an entire collection of strategic documents.

**Deliverable:** Minimal useful retrieval interface, implemented only where the existing commands prove insufficient.

---

## PR 6 — Typed schema specialization, conditionally

**Purpose:** Introduce additional executable structure only where actual use establishes that it is necessary.

This increment is conditional.

Before modifying shared schema types, produce a short compatibility and competency assessment.

The assessment must establish:

1. Which important competency question current claim kinds cannot answer faithfully.
2. Why descriptive attributes or existing relations are inadequate.
3. Which new claim kind or predicate resolves that limitation.
4. What the new semantics require of source evidence and authority.
5. Whether query consumers need a distinct mechanically enforceable type.
6. Whether historical records remain readable.
7. What migration, versioning or reindexing consequences follow.

**Potential future additions:**

- A dedicated executable `possibility` claim kind.
- Explicit `complements` or `alternative_to` relations.
- Typed relationship hypotheses with rationale.
- Bounded realization-link semantics.
- Historical assessment identity or reconsideration metadata.

Do not introduce all of these automatically.

If the accepted schema must change, use the repository's documented additive schema-evolution procedure. Preserve older authored versions, existing query behavior and historical replay compatibility.

The existing ADR 0033 architecture-vocabulary proposal is not automatically ratified by this plan. New shared contracts must follow their applicable authority process.

**Acceptance:**

The extension resolves an observed representational limitation without creating an unrelated generic knowledge database or automatic planning system.

**Deliverable:** Only the typed extensions earned by concrete use.

---

## PR 7 — Construction-to-possibility reconciliation

**Purpose:** Connect normal product development back to the long-term creative horizon.

**Tasks:**

1. During a consequential engineering increment, identify which existing capabilities changed.
2. Inspect related retained possibilities when the changes could materially affect their feasibility or value.
3. Reassess specific previously documented blockers or dependencies.
4. Preserve newly realized capability links.
5. Record genuinely new combinations or extensions when useful.
6. Preserve earlier assessments as historical context.
7. Avoid editing unrelated idea records.
8. Update the Level-3 strategic state only when the new evidence actually changes a strategic decision or continuation condition.

**Example:**

```text
New capability implemented
    |
    v
Existing semantic relationships inspected
    |
    v
Previously deferred possibility found
    |
    v
Original deferral reason inspected
    |
    v
Relevant assumption may have changed
    |
    v
Possibility reassessed
    |
    +--> Still deferred
    |
    +--> Revised hypothesis
    |
    +--> Candidate for Level-3 consideration
    |
    +--> No meaningful change
```

**Acceptance:**

A meaningful construction episode can update the applicable possibility history without requiring an exhaustive global analysis or altering the product thesis.

**Deliverable:** A continuous, proportional knowledge-development loop.

---

## 8. Product-value acceptance criteria

Evaluate the program using useful behavior rather than artifact counts.

### Minimum useful capability

A later coding agent should be able to:

1. Recover an ambitious proposal not currently authorized for implementation.
2. Recover an implemented capability linked to a previous product intention.
3. Explain the difference between an original possibility and its partial realization.
4. Find a documented historical rejection or deferral and its rationale.
5. Recover at least one materially interesting relationship between distinct ideas.
6. Generate a new possible combination, clearly marking it hypothetical.
7. Reconsider an idea when real new evidence changes one of its original assumptions.
8. Continue ordinary coding work without mandatory full-graph exploration.

### Evidence levels

Keep these claims separate:

**Representation established:** Records exist, validate mechanically and preserve the expected distinctions.

**Retrieval demonstrated:** The existing or new query surfaces return the right authored records and their caveats.

**Local reasoning usefulness observed:** An agent uses a recovered possibility or relationship to make a better-grounded engineering or strategic assessment.

**Cross-session usefulness observed:** A fresh-context agent correctly recovers and applies consequential prior information.

**Longitudinal product benefit established:** Multiple real episodes support a cumulative decision-quality benefit relative to practical alternatives.

The first two are appropriate construction acceptance conditions. Later evidence should arise from genuine use; it is not a standing synthetic-experiment gate.

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Idea accumulation without useful synthesis | Retain material ideas and relationships, not every passing thought |
| Duplicate source of truth | Reuse existing reviewed records and source documents |
| Premature ontology expansion | Require failed competency questions before executable type changes |
| Speculation presented as fact | Preserve hypothesis and evidence status explicitly |
| Implemented claims based on documentation alone | Inspect actual implementation evidence |
| Historical rationale erased | Preserve revisions and supersession links |
| Idea graph limits creativity to known nodes | Retain open-ended counterfactual exploration |
| Every task becomes a brainstorm | Keep exploration proportional and conditional |
| Idea library becomes automatic backlog | Preserve explicit Level-3 decision and authority boundaries |
| Rejected ideas silently reactivated | Reconsideration produces a question, not an authorized action |
| Repository-level priorities overfit short-term work | Keep long-term product capability relationships visible during consequential selection |
| High maintenance from frequent changes | Update only meaningfully affected records and use existing drift/reconciliation tools |

---

## 10. Development and integration policy

The repository is operating under its owner-selected construction-first policy.

For this program:

- Prefer useful, reversible increments over building an elaborate experimental harness.
- Reuse existing semantic-knowledge validators, source checks, schema checks and hosted CI.
- Do not introduce new local unit or synthetic evidence tests merely as a prerequisite to construction under the current repository-specific exception.
- Report unrun checks honestly.
- Preserve existing security and GitHub protection boundaries.
- Keep each PR reviewable and include a short decision note.
- Merge construction PRs only under the applicable current integration authority and repository protections.
- Do not assert product-value improvement solely from successful implementation.
- Update `STATUS.md` when a consequential capability or strategic continuation actually changes, rather than after every minor documentation edit.

### Dependencies

```text
PR 1: Ontology and competency questions
    |
    v
PR 2: Source-grounded possibility landscape
    |
    v
PR 3: Reviewed semantic knowledge integration
    |
    +--------------------+
    |                    |
    v                    v
PR 4: Exploration     PR 5: Retrieval,
integration           if needed
    |                    |
    +---------+----------+
              |
              v
PR 6: Schema specialization,
      only if necessary
              |
              v
PR 7: Real construction and
      possibility reconciliation
```

PR 6 is deliberately conditional, not a mandatory prerequisite for PR 7. A successful implementation may never need a new executable `possibility` kind.

Each merged increment should leave a usable capability or durable, decision-relevant improvement.

---

## 11. Owner decisions and authority boundaries

### Decisions recommended for this program

1. Pursue Product Possibility Stewardship as an extension of ADR 0031.
2. Include implemented, speculative, compatible, adjacent, counterfactual, deferred and rejected ideas.
3. Make relationships and historical rationale central to the model.
4. Use the existing Semantic Architecture as the conceptual foundation.
5. Reuse existing Git-authored knowledge and its rebuildable index.
6. Avoid automatically ranking possibilities or selecting construction work.
7. Preserve rejected ideas and their original reconsideration conditions when consequential.
8. Introduce new executable schema types only when required by meaningful use.
9. Keep divergence and convergence as distinct responsibilities.
10. Use construction results to update the possible-futures model proportionally.

### Not authorized by the plan alone

- Changing the accepted Level-4 product thesis.
- Ratifying proposed ADRs without their required process.
- Adding a deterministic planner or automatic responsibility selector.
- Treating speculative ideas as accepted strategy.
- Automatically executing ideas found in the library.
- Creating an unrelated cross-repository runtime or knowledge service.
- Publishing or deploying outside existing authority.

---

## 12. Recommended first development increment

Begin with **PR 1 and the smallest useful part of PR 2**.

This creates a concrete ontology and a source-grounded possibility landscape in one early, reviewable vertical slice.

Do not begin with a database migration, generic graph API, UI dashboard or new Skill.

The first increment should prove a simpler claim:

> The existing repository can preserve a meaningful selection of possible futures, their status and their relationships in a form that a later coding agent can understand and extend.

Once that capability exists, integrate it into the reviewed knowledge substrate and exploration workflow.

The target outcome is not an impressive schema in isolation. It is a meaningful improvement in how coding agents explore and develop software products over time.

---

## 13. Long-term development direction

The intended evolutionary relationship is:

```text
PERSISTENT PRODUCT KNOWLEDGE
    What exists and what has happened
                |
                v
PERSISTENT POSSIBILITY KNOWLEDGE
    What could exist and why
                |
                v
RELATIONAL POSSIBILITY SYNTHESIS
    What new futures could emerge
                |
                v
VALUE-DIRECTED CONSTRUCTION
    What is warranted to build now
                |
                v
RECONCILIATION AND LEARNING
    What changed in reality and possibility
                |
                +----------> Repeat
```

The loop must preserve an asymmetry:

**Creative exploration can consider possibilities beyond accepted strategy. Construction remains governed by current product intent, evidence and authority.**

That asymmetry allows the system to become intellectually ambitious without becoming operationally reckless.

### Guiding principles

1. **It is not a repository of suggestions; it is a repository of possible product futures and their relationships.**
2. **It is not a fixed roadmap, and it is not an automatic backlog; it is a persistent space for exploration, reconsideration and strategic judgment.**
3. **Implementation changes what becomes possible.**
4. **Historical rejection is knowledge, not automatic permanent prohibition.**
5. **Cross-session conceptual synthesis is a product capability, not merely a convenience of long conversations.**

### Proposed program completion condition

The initial Product Possibility Ontology & Idea Library v1 program is complete when the ontology, curated records, retrieval path and exploration integration are usable in real repository work; one consequential possibility can be recovered and reinterpreted using current evidence; implementation status and authority remain accurate; and no known essential relationship or provenance distinction is lost by the chosen representation.

Long-term cumulative intelligence remains an aspiration to be supported or revised through subsequent genuine engineering episodes.

**Final product objective:** An agent that can continuously develop software while maintaining a growing, revisable understanding of what that software could become.
