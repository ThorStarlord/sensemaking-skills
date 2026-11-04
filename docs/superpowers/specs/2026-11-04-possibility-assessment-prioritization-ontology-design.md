# Possibility Assessment and Prioritization Ontology v1 — Design Basis

**Date:** 2026-11-04.
**Repository baseline:** ThorStarlord/sensemaking-skills at main@b327ed2e82e125644a1f88b7feba478f1cd583b1.
**Status:** accepted conceptual direction, proposed implementation design; not implementation authorization.
**Companion:** [implementation plan](../plans/2026-11-04-possibility-assessment-prioritization-ontology.md).

## 1. Intent and expected value

Give an active coding agent and later readers a consistent way to interpret **Coverage Assessment and diminishing returns**, **Possibility Consolidation**, **Comparative Evaluation**, and a **Ranked Opportunity Portfolio**, while maintaining three different priority decisions: which inquiry to investigate, which future is strategically attractive, and which already authorized work to implement.

The goal is improved **reuse and contestability of reasoning**. A returning reader should know what was assessed, why ideas were grouped, which uncertainty limits a comparison, what was left out, and which change in evidence, framing or authority would alter the conclusion. It should not inherit a ranking as an executable queue or turn a source-grounded judgment into automatic truth.

The existing [divergent exploration ontology](../../semantic-architecture/divergent-exploration-ontology.md) already defines inquiry, frame, question, candidate expression, landscape and exploratory judgment. The [product possibility ontology](../../semantic-architecture/product-possibility-ontology.md) preserves enduring product possibilities and their separate realization/disposition. The [prospective reasoning ontology](../../semantic-architecture/prospective-reasoning-ontology.md) retains architecture/path comparison semantics, whose endpoints must **not** be silently widened. The [inquiry-process reconciliation](../../explorations/2026-11-03-inquiry-process-reconciliation.md) already distinguishes three priority objects. This addition unifies interpretation and record-keeping, not their decision authority.

A good result is a source-grounded assessment a fresh agent can reconstruct, challenge and revise without recovering its author's private reasoning. A count of classes, graph nodes, rankings, fields or generated ideas is not the success measure.

## 2. Goals, non-goals and anti-goals

### Goals

- G1. Reuse and clarify existing ontology roles before adding specializations.
- G2. Preserve **target, purpose, assessed corpus/revision, criteria, judgment, grounds, uncertainty, author, and reversal conditions** when these details are material.
- G3. Distinguish corpus completeness, conceptual breadth, consequence depth, empirical support and perspective coverage.
- G4. Distinguish retrospective repetition, expected marginal learning under a proposed method, and attention allocation relative to other inquiries.
- G5. Distinguish restatements, variants, navigational groups, complements, competing alternatives and genuine synthesis, while preserving all original expressions and disputed interpretations.
- G6. Permit qualitative preference, partial ordering, ties, incomparability, conditional order and not-assessed status without forcing one total ordinal list.
- G7. Preserve the difference among an **inquiry question plus proposed investigation**, a **product future**, and an **authorized change**.
- G8. Preserve historical snapshots, changes in source evidence and evaluation frames, and historical dispositions.
- G9. Make the resulting definitions and portable guidance accessible to independently operating installed agents; selectively index source-linked definitions and record references where warranted.
- G10. Verify documentary reconstruction and installed delivery with honest evidence ceilings.

### Non-goals

- No new public entrypoint Skill, mandatory pipeline, automatic stage transition, backlog generator, prioritization algorithm, score/weighting framework, creative novelty detector, or implementation authorization.
- No immediate change to existing ComparativeJudgment/ProvisionalPreference architecture/path endpoints, canonical knowledge schema, artifact registry, parser, or query engine.
- No bulk conversion of 59 exploratory labels, seven generative families or 19 curated possibilities into ranked graph instances.
- No retroactive replacement of the 2026-11-02/04 exploration, coverage, convergence or prioritization reports.
- No claim that documentary reconstruction establishes independent reasoning benefit, owner value, automatic host discovery, or graph-specific causal advantage.

### Anti-goals

A design fails even if structurally valid when it collapses a question into its product direction; treats grouping as identity; hides a non-comparable direction at the bottom of a list; infers saturation from counts; treats a hypothesis as observed benefit; treats a ranking as consent to build; or invents evidence, complete frames or authority to satisfy a template.

## 3. Approaches compared and selected

| Approach | Advantage | Main limitation | Disposition |
| --- | --- | --- | --- |
| Activity-specific documents only | Smallest format change; closely follows the existing exploration archive | Inconsistent comparison context and difficult cross-session reconstruction | Retain historical reports but not sufficient alone for the requested ontology |
| **Shared assessment semantics + purpose-relative views + focused activity profiles** | Reuses established concepts, preserves distinct evaluative purposes, and supports heterogeneous portfolios | Requires disciplined attribution and source-bound review; some relationships remain documentary | **Selected direction for v1** |
| Machine-first assessment schema and automatic ranked pipeline | Allows rigid producers/consumers and sortable records | No demonstrated parser consumer; biases inquiry toward forms, false completeness and machine authority | Conditional only when a concrete consumer and lost meaning justify it |

The owner accepted the shared-model recommendation in conversation. Exact file paths and selective knowledge projection below are implementation-planning choices, not separate product-thesis ratification.

## 4. Conceptual model and boundaries

Treat the following as **documentary roles**, not a new collection of executable claim kinds.

| Role | Definition and relationship to existing model |
| --- | --- |
| **AssessmentActivity** | A bounded reasoning activity assessing a source-scoped landscape, relationship or alternative for a named purpose. May be coverage, consolidation or evaluation. It is not an automatic next stage. |
| **AssessmentFrame** | A purpose-relative context: governing question, relevant beneficiaries and ends, comparison unit, criteria, horizon, evidence boundary, premises and authority context. Builds on ExplorationFrame but makes evaluative purpose explicit. Incomplete dimensions remain unknown. |
| **AssessmentTarget** | A typed reference role, not a universal entity: expression, question + proposed inquiry, source relationship, possibility, group, option, construction path, or authorized change. The referent keeps its original identity. |
| **AssessmentJudgment** | A source-attributed, revision-scoped Claim about assessed target(s) under a frame; includes grounds, counterevidence or omitted evidence, uncertainty, assessor and reconsideration conditions. Specializes the existing ExploratoryJudgment role where appropriate; does not silently broaden prospective ComparativeJudgment. |
| **ConsolidatedView** | A purpose-relative, source-preserving grouping of expressions/possibilities with attributed relationship judgments. Derives from PossibilityLandscape as a view, not a new canonical identity for grouped material. |
| **PortfolioSnapshot** | A bounded historical presentation of members and their applicable assessments; membership differs from ordering, and ordering can be partial or absent. It is an Artifact, not a construction queue or an authority to act. |
| **ProposedInquiryApproach** | The particular way an unresolved question could be investigated, including source/observation prerequisites and anticipated discriminating learning. It is a description for exploration-priority comparison, not a mandatory Experiment or implementation task. |
| **AssessmentRevisionAccount** | An attributed explanation of changed sources, premises, targets, methods, criteria, portfolio membership, or authority between preserved snapshots. Does not overwrite the older assessment. |

### Semantic refinements within AssessmentJudgment

**CoverageFinding:** distinguish (a) a declared corpus was examined, (b) a dimension is represented, shallow, omitted or NOT_ASSESSED, (c) a consequence was analyzed in depth, (d) an empirical claim has support, and (e) a viewpoint is independently represented. Coverage sufficient for a specified next decision is not global completeness or saturation.

**MarginalLearningJudgment:** preserve three separate claims: observed repetition in prior inquiries; a conditional forecast of additional insight under a **specific proposed inquiry approach**; and an allocation preference relative to alternative uses of attention. Do not calculate a novelty curve from candidate counts.

**ConsolidationJudgment:** identify operands, relationship type and the criterion: restatement/near-duplicate, variant, overlapping navigation group, complement, contextual alternative, or synthesis. Keep disagreement and source identity. Shared wording, shared goal, shared method and graph absence are not identity proofs; similarity is not transitive across different criteria.

**PurposeRelativeComparison:** represent assessed alternatives, governing frame and relevant dimensions; an outcome may be preferred, tied, incomparable, conditional, unresolved, or NOT_ASSESSED. A missing comparison is not a tie. Do not borrow a normative priority from an unrelated assessment frame.

**PriorityAssessment:** retain the target's type and question:
- **Exploration priority:** compare InquiryQuestion + ProposedInquiryApproach using expected decision-relevant learning, remaining uncertainty, repetition, evidence access, dependencies, and attention opportunity cost.
- **Strategic attractiveness:** compare ProductPossibility or explicitly scoped future directions/combinations using potential beneficiary value, consequences, assumptions, costs, strategic fit and counterevidence; depth and authorized strategy interpretation remain prerequisites to authoritative conclusions.
- **Implementation priority:** compare concrete **authorized** ProductChanges/responsibilities under current state, dependencies, reversibility, verification, resources and permission. Ranking cannot create authorization; hypothetical sequences must be labeled hypothetical.

### Suggested documentary relations (no executable predicate changes)

- AssessmentActivity **considers** AssessmentTarget under AssessmentFrame, and **produces** AssessmentJudgment or a view.
- AssessmentJudgment **assesses** typed operand(s), **usesCriterion**, **citesEvidence**, **statesUncertainty**, and **reconsiderIf** specified conditions change.
- ConsolidatedView **includesOriginalExpression**, **groupsForPurpose** and **recordsRelationJudgment**; it never silently asserts sameAs.
- PortfolioSnapshot **includesEntry**, **drawsOnAssessment** and **recordsOrdering** or **recordsNoncomparability** under its frame.
- AssessmentRevisionAccount **reassessesEarlierSnapshot**, names the changed premise/source/criterion and cites both identities.

Read these as semantic relationship descriptions; a documented link is not a validated v1 graph predicate. If a proposed endpoint is unavailable in the executable schema, keep the relationship in prose or an existing checked reference without asserting machine semantics.

## 5. Identity, provenance and history

1. Preserve each target's original file path, local ID and source **file revision**. Distinguish that from an earlier **inspected target revision** reported in the source itself.
2. A grouping never changes the identity or original disposition of the grouped expressions; disagreement and multiple legitimate groupings can coexist.
3. Use document-qualified local IDs (e.g. A1, F1, J1, V1, P1) when they improve cross-reference. Their spelling does not confer global canonical identity.
4. Record purpose and criterion with each comparison. A changed question or inquiry method requires a distinguishable assessment target; a changed judgment requires dated attribution rather than rewriting the old statement.
5. Do not force transitive equivalence or one-to-one mapping from 59 exploratory labels to 19 curated possibilities. Retained source concepts and new synthesis identities require separate evidence.
6. A new assessment may supersede a prior recommendation for current use while preserving the historically correct earlier assessment and its actual scope.
7. A portfolio can preserve an outside-frame member without assigning it a last place. Preserve incomparable, conditional and non-assessed distinctions.

## 6. Record profile and activity-specific use

Use readable Markdown as the authoritative explanatory surface. The common **assessment envelope** contains the assessment purpose, target type/identities, sources and revisions, governing frame, criteria, substantive judgment, confidence/uncertainty in words, counterarguments/omissions, revision triggers, historical connections, and stopping rationale. Shared context may be stated once. Do not require empty template fields merely to appear complete.

- **Coverage profile:** corpus, dimensions and inspected perspectives, representation vs depth vs evidence, material gaps, specific sufficiency claim, rationale for another lens, and three distinct diminishing-return judgments.
- **Consolidation profile:** original expression IDs, source-to-group crosswalk, relationship grounds and overlap, preserved distinctions, unresolved identity disputes, and what a convenient group view abstracts away.
- **Evaluation profile:** specified targets and comparison unit, qualitative criteria, evidence/counterevidence, direct comparison, conditional implications, incomparability and reversal conditions.
- **Portfolio profile:** membership and per-entry target identity, frame, ranked or partially ordered subsets, non-comparable/outside-frame entries, shared uncertainties, complement/substitution/dependency where material, and dated reconsideration links.

These profiles are optional guides for the appropriate existing responsibilities, not compulsory stages or different new executable artifact types. Session receipts point to reports; reports carry the substantive analysis; reviewed knowledge contains only selected claims.

## 7. Worked-case source set and competency questions

Use current originals instead of inventing an assessment dataset:

| Case | Source | Critical distinction |
| --- | --- | --- |
| **Coverage without saturation** | [Divergent coverage assessment](../../explorations/2026-11-02-divergent-coverage-assessment.md) and [2026-11-04 portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md) | Broad enough for provisional convergence; unresolved dimensions and no general diminishing-return rate |
| **Near duplication without identity collapse** | [Accumulated convergence](../../explorations/2026-11-03-convergent-accumulated-creative-possibilities.md) | GD-D / DE-F2 related, both original labels preserved; a group is not sameAs |
| **Method-dependent inquiry priority** | [Current portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md) and [evidence inquiry](../../explorations/2026-11-03-evidence-inquiry-creative-goal-discovery.md) | Futures remains strategically central; its specific causal-benefit question is low value as more conceptual prose but may be high value with authentic independent observations |
| **Outside-frame membership** | [Current portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md) | Exit and Public stay in a parallel frontier rather than being ranked last |
| **Priority revision** | [Initial depth prioritization](../../explorations/2026-11-03-depth-exploration-prioritization.md), [architectural reappraisal](../../explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md), [current portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md) | Different remaining questions and inspected evidence change rank without changing enduring opportunity identity |

Local competency questions to assess in a new fit document (do not invent global CQ IDs):
1. What exactly was assessed, by whom, and at which source/target revisions?
2. Was a finding about corpus inspection, breadth, depth, independent perspective or empirical support?
3. Sufficient for which follow-on purpose, and what remains NOT_ASSESSED?
4. Is a diminishing-return claim retrospective, prospective under a method, or relative to competing attention?
5. Which original expressions are grouped, under what criterion, and which distinctions were abstracted away?
6. Can an alleged duplicate remain separately identifiable, disputed, and revisable?
7. What is the exact target of a comparison: question+inquiry approach, future, or authorized change?
8. Which comparisons are preferred, tied, conditional, incomparable, unresolved or NOT_ASSESSED?
9. Does a portfolio distinguish membership from ordering and preserve outside-frame directions?
10. What evidence, changed premise or new method would alter a ranking, and which older assessment remains historical?
11. Can shared uncertainty or complementarity be reported without implying a causal relationship?
12. Does any priority or grouping improperly promote a hypothesis into a decision, accepted product identity, or action permission?

Use qualitative fit: faithful, awkward, lost, not established. The cases test documentary meaning, not creative efficacy.

## 8. Implementation and growth boundary

Proposed v1: one new conceptual module; a local competency/fit document; source-pinned annotated cases; a portable self-contained guide and optional record profile in existing Skill references; bounded conditional guidance cues; a small reviewed-knowledge pack with existing accepted types and predicates; installed-reference and fresh-reader reconstruction; navigation and completion record.

No dedicated parser, contract or schema mutation in v1. Propose one only when a named producer/consumer needs stable parsed fields not recoverable by the readable profile, or when a real retrieval question loses a necessary distinction under existing claims, references, attributes and prose. Follow the [schema-evolution procedure](../../../skills/repository-semantic-steward/references/schema-evolution.md). Verify authority and scope independently.

## 9. Evidence and authorization ceiling

- Source-grounded cases and a ten-plus-question reader reconstruction can establish document fidelity and use by the tested reader, not improved originality, independent agent repeatability, causal graph advantage or owner value.
- A knowledge proposal check establishes admissible structure, not semantic truth.
- A successful wheel/profile installation establishes distributed files, not automatic host loading.
- A portfolio is a provisional intellectual view, never a merged roadmap, selected strategic destination or authorized construction task.
- Current repository-local instructions govern the future implementation's verification and PR discipline. They must be rechecked at execution time.
