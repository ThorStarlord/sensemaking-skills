# Possibility Assessment and Prioritization Ontology v1

**Status:** conceptual and documentary ontology module, 2026-11-04.
**Scope:** source-grounded Coverage Assessment, diminishing-returns judgment, Possibility Consolidation, Comparative Evaluation and Ranked Opportunity Portfolios.
**Authority:** implements the [accepted design basis](../superpowers/specs/2026-11-04-possibility-assessment-prioritization-ontology-design.md) within the existing [Layered Ontology](ontology.md), [Divergent Exploration Ontology](divergent-exploration-ontology.md), [Product Possibility Ontology](product-possibility-ontology.md), [Prospective Reasoning Ontology](prospective-reasoning-ontology.md) and ADRs 0029/0031/0034. Definitions, retained judgments and rankings confer **no new decision or action authority**.

## 1. Purpose and separation of responsibilities

Preserve *what was assessed, for which purpose, against which alternatives and sources, under which criteria, with what uncertainty, and what could reverse the result*. Later readers should be able to distinguish meaningful differences, inspect a comparison's omissions and reconsider a previous preference without inventing a new question or overwriting history.

This module follows a **shared assessment pattern with purpose-relative views**, not a fixed sequence. Coverage, consolidation, comparative evaluation, strategic attractiveness and implementation planning are different reasoning responsibilities. A divergent result may lead to coverage, or it may stop. An assessment can legitimately return no justified preference. Nothing automatically runs a next Skill, selects a Strategic Frontier, generates a backlog, or commits to construction.

The ontology describes **activities, documentary roles and claimed relations**, not eight new executable knowledge kinds. Existing `Claim`, `Hypothesis`, `Artifact`, `Provenance`, `Assumption`, `Decision`, `ProductPossibility`, `ExplorationInquiry`, `ExploratoryJudgment`, `PossibilityLandscape`, `ArchitectureOption` and `ConstructionPath` retain their established meanings.

## 2. Shared concepts and reference roles

| Concept/role | Definition | Nearest existing meaning and non-identity |
| --- | --- | --- |
| **AssessmentActivity** | Bounded intellectual work evaluating a stated target or landscape for a declared purpose; the activity may produce judgments, a consolidated view, a portfolio or an unresolved result. | Work-layer reasoning activity; not a new workflow stage, session, Campaign or automatically warranted responsibility. |
| **AssessmentFrame** | The purpose, question, beneficiary/end, assessed operand type, comparability criteria, temporal horizon, source scope, assumptions, constraints and applicable authority under which a judgment is meaningful. Partial/contested frames remain explicit. | A purpose-relative refinement of ExplorationFrame; not a new product strategy or owner preference. |
| **AssessmentTarget** | A *typed reference role*: a source-qualified explanatory Hypothesis **when the purpose is evidential adequacy**, or a specific CandidateExpression, InquiryQuestion plus ProposedInquiryApproach, ProductPossibility, outcome direction, relation assertion, architecture option, construction path or authorized construction change. Its underlying referent keeps its original identity. | Not a generic entity replacing all prospective types. A Hypothesis remains an unestablished Claim, **not** a product future. Comparing differently typed targets requires a shared comparison basis or explicit noncomparison. |
| **AssessmentJudgment** | An attributed, source/revision-scoped Claim about a target or relation under an AssessmentFrame, with criteria, supporting/counterevidence, uncertainty and reconsideration conditions. | Can refine ExploratoryJudgment. It is not automatically the Prospective Reasoning `ComparativeJudgment` or `ProvisionalPreference`, whose architecture/path endpoints remain unchanged. |
| **ConsolidatedView** | A bounded source-preserving grouping or crosswalk of expressions and possibilities under an explicit organizing question. It records grouping criteria and what differences the view abstracts away. | Purpose-relative view of a PossibilityLandscape, not a new canonical identity, equality claim or curated ProductPossibility. |
| **PortfolioSnapshot** | An identifiable dated Artifact containing member targets, applicable judgments and any supported partial ordering within a stated frame, including incomparable, outside-frame and unassessed members. | Analytical presentation, not a strategic decision, roadmap, implementation queue or automatic task selector. |
| **ProposedInquiryApproach** | A specific proposed method of investigating a question, including source access, observation prerequisites, cost or feasibility limits and expected decision-relevant learning. | May be conceptual depth, source inspection, normal-use inquiry or an experiment *only if independently warranted*. Not a compulsory experiment or construction responsibility. |
| **AssessmentRevisionAccount** | An attributed explanation of a later interpretation's relationship to an earlier judgment or snapshot: changed question, method, source, frame, criterion, alternatives, evidence or authority. | Preserves the older statement as historical; does not retroactively alter its scope or claim an observed improvement. |

For the **diagnostic** use of this documentary role, the assessed explanatory `Hypothesis` keeps its original source-qualified Claim identity and shared observed explanandum. An `AssessmentJudgment` can evaluate evidence adequacy or contrast explanatory reach without turning the hypothesis into a `CandidateExpression`, new executable assessment target kind, or a prospective architecture/path comparison. See the [abductive-to-assessment integration](abductive-assessment-integration-v1.md) and its [source-scoped competency assessment](abductive-assessment-integration-competency-v1.md).

A common **assessment envelope** specifies when material: activity identity/author/date; target(s) with original source IDs; purpose and comparison frame; source-file and inspected-target revisions; criterion; cited grounds and counterarguments; substantive judgment; uncertainty and exclusions; reason to stop; historical predecessor; and what would reverse or reopen the judgment. Shared scope may be stated once per record. Unknown fields stay unknown; no mandatory form-filling.

## 3. Assessment specializations

### 3.1 CoverageFinding — several different kinds of "covered"

Coverage is a bounded Claim about a declared landscape/corpus and question. Distinguish:

1. **Corpus coverage:** which declared source documents, candidates or systems were inspected. All items inspected within a declared set does not establish completeness of the underlying world.
2. **Conceptual breadth:** which meaningfully different ends, beneficiaries, premises, mechanisms or contexts are represented. A label count does not prove diversity.
3. **Consequence depth:** which direct, second-order, systemic, adverse or conditional consequences were actually examined. Many ideas can have shallow depth.
4. **Empirical support:** which effects have supporting observations, counterevidence, or only hypotheses. An articulated possibility is not an experienced benefit.
5. **Perspective coverage:** which perspectives, source access conditions and independently formed questions were actually available. Multiple named lenses in one agent do not prove independent perspective formation.

Record what is **represented, shallow, omitted, unexamined, outside scope or unknown**. `NOT_ASSESSED` is a documentary statement of the assessment boundary, not a universal graph status or a proof of absence.

**Typed coverage boundary:** a diagnostic account may consider the evidential adequacy and breadth of competing explanations for **one explanandum**. That is not conceptual breadth of product futures: multiple hypotheses do not count as multiple `ProductPossibility` or `CandidateExpression` units. Keep the declared typed corpus and assessment question explicit; this uses the five dimensions above rather than introducing a new coverage enum.

**Sufficiency-for-purpose** asks whether the bounded landscape is usable for a particular next judgment, such as *provisional Convergent Evaluation*. It is not a saturation assertion, approval to act, or requirement to run the next stage.

### 3.2 MarginalLearningJudgment — three non-identical claims

1. **Retrospective contribution:** what actually appeared in earlier work and how it differs from predecessors. Repetition is supported locally by comparison, not by decreasing item counts.
2. **Prospective contribution:** what a *particular proposed inquiry approach* might still teach, conditional on its source, beneficiary, frame, method and observation access. The same intellectual question may have low value as another generic essay but high value with genuine independent evidence.
3. **Attention allocation:** whether this approach merits attention relative to *identified competing inquiries* under the present purpose and available resources.

Observed repetition does not establish low prospective insight across new lenses. Low prospective insight does not alone establish that some other inquiry is feasible or authorized. Record all conclusions and their uncertainty separately.

### 3.3 ConsolidationJudgment — source-preserving interpretation

Recognize and explain these relationships **within a specified criterion**:

- **Restatement or near-duplicate:** closely overlapping meaning/operation for a declared purpose. Do not equate similarity with global sameness.
- **Variant:** shares a salient end or mechanism but differs in a potentially consequential dimension.
- **Navigational group:** expressions placed together because a particular view needs a common organizing unit; members may appear elsewhere.
- **Complement:** different possibilities could contribute to a combined outcome; this does not establish causal enabling or a user-valued synthesis.
- **Contextual alternative:** alternatives compete or conflict under a specified assumption/constraint; not necessarily incompatible in every context.
- **Synthesis:** a proposed new combination with a distinct meaning; granting a new enduring `poss:` identity still requires independent curation.

Keep **original expression IDs, source document and revision, attribution, criterion, counterexamples and disagreements**. An overlap group is not `sameAs`. Similarity is not automatically transitive, especially when A resembles B in *end* while B resembles C in *method*. A view explains which differences it suppressed; later readers can recover them by following sources.

### 3.4 PurposeRelativeComparison — comparison need not rank

A comparison is warranted only for identifiable operands, a clear purpose and criteria, and sufficiently grounded facts or hypotheses. Valid documentary outcomes include:

- **Preferred under frame F:** A more promising than B for this purpose, with grounds and reversal conditions.
- **Tie:** considered and judged indistinguishable on the decisive dimensions for F.
- **Equivalent for purpose:** treated as interchangeable in F, without erasing distinct source identity.
- **Conditional:** order depends on an unresolved premise that is named.
- **Incomparable:** no legitimate shared basis under F (e.g., different beneficiaries or governing values).
- **Unresolved:** the shared question exists but the evidence or interpretation does not justify an order.
- **NOT_ASSESSED:** no comparison of this pair under F occurred.

No automatic numerical score, weights, confidence percentage, total ordinal list or inferred preference from mere adjacency. A conditional pairwise preference does not become a global ranking.

### 3.5 PriorityAssessment — three different targets

| Priority frame | Valid target and grounds | Does not imply |
| --- | --- | --- |
| **Exploration priority** | A specific `InquiryQuestion + ProposedInquiryApproach`, compared by likely consequential learning, examinedness, source access, known/unknown consequences, portfolio complementarity, feasible method and relative attention. | Product superiority, strategy acceptance or implementation authorization. |
| **Strategic attractiveness** | A coherent ProductPossibility, product direction or specified combination, compared *after sufficient depth* by beneficiary value, assumptions, consequences, costs, tradeoffs, current thesis, evidence and counterevidence. | Owner ratification, selected Level-3 construction path, new product thesis or authorization. |
| **Implementation priority** | Concrete authorized ProductChange/responsibility within an applicable planning context; compare current repo state, dependencies, reversible benefit, verification, resources and protected boundaries. | Authority obtained by ranking: permission must be independently sourced. A hypothetical sequence remains hypothetical. |

These are **different orderings**. One direction can be strategically central yet have a low-value next conceptual inquiry, while its evidence-dependent question becomes a top investigation when authentic observations are available.

## 4. Relationships and endpoint constraints

These names are **conceptual/documentary descriptions**, not changes to the knowledge-predicate enum.

| Subject | Relationship | Object | Establishment requirement |
| --- | --- | --- | --- |
| AssessmentActivity | `hasPurpose`, `hasAssessmentFrame` | question/declared purpose; AssessmentFrame | State actor, time, task boundary and actual decision purpose. |
| AssessmentActivity | `considers` | typed AssessmentTarget | Source identifies the inspected operand; no synthesized canonical ID merely for convenience. |
| AssessmentActivity | `producesJudgment` or `producesView` | AssessmentJudgment; ConsolidatedView/PortfolioSnapshot | Cite the published assessment artifact, not private scratch. |
| AssessmentJudgment | `assessesTarget`, `usesCriterion`, `citesEvidence` | typed target(s), stated criterion, source/Claim | Retain operands, provenance, contrary evidence or explicit absence. |
| CoverageFinding | `scopesCorpus`, `qualifiesPurpose` | declared source set; assessment purpose | Record omitted/unexamined dimensions. |
| MarginalLearningJudgment | `assessesProposedInquiry` | InquiryQuestion + ProposedInquiryApproach | State which kind of return claim and the alternative if allocating attention. |
| ConsolidatedView | `retainsExpression`, `groupsByJudgment` | original CandidateExpression; ConsolidationJudgment | Source IDs stay intact; views can overlap. |
| PortfolioSnapshot | `includesMember`, `drawsOnJudgment` | typed target; source-attributed AssessmentJudgment | Membership is independent of ordering; outside-frame entries remain members. |
| PortfolioSnapshot | `recordsComparison` | PurposeRelativeComparison | A partial order is valid; avoid invented ranks for unassessed or incomparable entries. |
| AssessmentRevisionAccount | `reconsiders`, `preservesPredecessor` | prior judgment/snapshot with dated identity | Explicit changed scope/criterion/evidence/method and successor's own date. |

**Restricted existing relation endpoints remain restricted:** Prospective `ComparativeJudgment evaluates` and `ProvisionalPreference prefers` apply to ArchitectureOption or ConstructionPath as documented; this assessment module does not extend them to ProductPossibility or InquiryQuestion. Similarly, `Decision selects` still requires appropriate authority. An `AssessmentJudgment` in prose is not an executable graph record just because these concepts are described.

## 5. Identity, currentness and epistemic boundaries

1. Qualify `A1`, `F1`, `J1`, `V1` or `P1` local IDs by their containing artifact and source-file revision. Existing `DE-`, `NX-`, `RP-`, `GD-`, `poss:` and `arch:` identities stay in their original namespaces.
2. Distinguish the revision **containing** an assessment from the older revision that assessment **inspected**. A historical report is not backdated to its inspected baseline.
3. A grouped label is a view label, not an enduring product possibility or new approval state. Preserve alternative group memberships, opposed judgments, and minority frames when meaningful.
4. A changed question, comparison method or important frame changes the scope of the later assessment; preserve earlier results and describe the delta. New evidence may alter a ranking without changing the enduring option's identity.
5. Separate observed facts (source checked), author interpretation, causal hypothesis, preference and governing decisions. A valid schema or successful retrieval establishes neither source meaning nor real user value.
6. Rank only comparable entries for a stated purpose. Preserve outside-frame or non-comparable entries in the portfolio; do not assign low rank as a substitute for epistemic honesty.
7. Do not use count of documents, candidate labels, graph nodes, linked sources or ordinal numbers as a proof of sufficiency, creative benefit or strategic merit.
8. Explicitly preserve `NOT_ASSESSED`, unresolved, conditional, incomparable and tie as different meanings.
9. A ranked inquiry does not authorize its execution, a ranked future does not ratify a thesis, and a ranked change does not create authority where none exists.

## 6. Representation and selective retention

| Material | V1 representation | Consumer and boundary |
| --- | --- | --- |
| Substantive coverage/consolidation/comparison | A dated source-linked Markdown report using an [optional record profile](../../skills/strategic-repository-analysis/references/possibility-assessment-record-template.md) | A returning human or agent reads the source; no compulsory parser. |
| Reusable procedural guidance | [Portable assessment reference](../../skills/strategic-repository-analysis/references/possibility-assessment-v1.md) under existing Skills | Only when that responsibility is warranted; target owns sources and authority. |
| Portfolio | Dated, purpose-relative snapshot and links to original IDs | Not a roadmap; any order is provisional and scoped. |
| Source and concept discoverability | Existing source claims, declared domain_concept definitions and checked `references` in v1 authored knowledge | Index returns candidate source links and declared concepts; it does not judge actual candidate equivalence or usefulness. |
| Specific conceptual relation without executable predicate | Attributed prose, optionally `references` with clearly labeled `attributes.conceptual_relation` | Attribute is not an enforced endpoint or truth rule. |
| Session execution facts | Existing session receipt with `artifact_refs` to the reports | Receipt is not a knowledge-index surrogate and does not contain the substantive assessment. |

The v1 model adds no new executable `artifact_id`, required fields, universal type, mandatory sidecar, schema version, command, stage engine or ranked-backlog feature. Do not bulk-promote speculative archive candidates to fill a graph. When a concrete producer/consumer requires parsed fields or a real retrieval question loses a necessary distinction, follow the existing [schema-evolution procedure](../../skills/repository-semantic-steward/references/schema-evolution.md) with an explicit example, compatibility analysis, authority and evidence.

## 7. Competencies, cases and evidence ceiling

The [local competency matrix](possibility-assessment-competency-v1.md) contains twelve questions mapped to existing ontology/competency meanings. The [annotated cases](possibility-assessment-reference-cases-v1.md) reconstruct: bounded coverage without saturation; GD-D/DE-F2 near-duplicate grouping without identity collapse; source-/method-dependent Futures inquiry priority; Exit/Public outside the common ordering; and historical pairwise vs later global inquiry rankings.

The product's value thesis is improved source-grounded agent reasoning. Document reconstruction can establish that a reader found and understood the asserted reasons; it cannot establish that an independent agent performs more creative work, that a new ranking serves the owner, or that a graph rather than the original documents caused the result. An installed reference proves package delivery, not host invocation.

This module is a **Level-2 conceptual ontology and documentary profile**. A small checked projection into the existing Level-3 knowledge system does not elevate the whole module into a new executable assessment contract.

## 9. Conditional transition from assessment to selection

The [Convergent Direction Selection Ontology](convergent-direction-selection-ontology.md)
specifies what additional evidence and real actor/authority would be necessary
to treat a comparative assessment as an **adopted scoped choice**. A
`PortfolioSnapshot`, `AssessmentJudgment`, comparative preference or
recommended inquiry does not itself instantiate a `Decision`. The target must
remain typed, credible unselected alternatives preserved, and the decision's
settled/open distinction stated. `NO_SELECTION` is a valid result.
These meanings add no mandatory next activity or executable predicate.

## 10. Consequence-informed reassessment remains purpose-relative

The [Connected Prospective Inquiry Ontology](connected-prospective-inquiry-ontology.md#5-convergent-reassessment-change-or-reaffirm-attributable-judgment)
uses the **existing `AssessmentRevisionAccount`** to say which new consequence,
evidence, premise or beneficiary frame changes an identifiable earlier
`AssessmentJudgment` or `PortfolioSnapshot`, and why. A later interpretation
preserves the former report's source identity, unchanged members and criteria.
Documentary outcomes include **reasoned no change**, revised grounds with the
same preference, narrowed applicability, local pairwise changes,
incomparability or unresolved evidence.

The [2026-11-03 pairwise reassessment case](connected-prospective-inquiry-reference-cases-v1.md#4-c-real-portfolio-reassessment-is-local-and-purpose-specific)
does not rewrite historical global ranks or convert inquiry priority into
strategy or implementation. The [local CPI competencies](connected-prospective-inquiry-competency-v1.md)
make this boundary explicit. No automatic reranking or mandatory next stage.
