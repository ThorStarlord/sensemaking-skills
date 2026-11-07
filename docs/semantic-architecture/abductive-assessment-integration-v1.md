# Abductive Explanation, Divergent Expression and Assessment — Semantic Integration v1

**Status:** Level-2 conceptual/documentary composition, 2026-11-06. **No executable kinds, graph predicates, schema version, controller, automatic stages or empirical claim of better reasoning.**  
**Inspected source baseline:** `ThorStarlord/sensemaking-skills@7209bac2429aaa6fe6fd703924ece03938bf3823`. This document has its own later Git source revision.  
**Fit:** [integration baseline and INT-CQ-01..12](abductive-assessment-integration-competency-v1.md); [source-linked cases I1..I5](abductive-assessment-integration-cases-v1.md). Sources of meaning: [Layered Ontology](ontology.md), [Evidence-Grounded Abduction](evidence-grounded-abductive-divergent-ontology-v1.md), [Divergence](divergent-exploration-ontology.md), [Assessment](possibility-assessment-ontology.md), [Relations and Epistemics](relations-and-epistemics.md), [Prospective Reasoning](prospective-reasoning-ontology.md).

## 1. Three questions that must not collapse

| Intellectual question | Original referent / output | Warrant and boundary |
| --- | --- | --- |
| **What could explain this?** | Source-qualified `Observation`/Claim is the explandum. Rival `Hypothesis` Claims seek to account for it. A proposed `InquiryQuestion` may discriminate. | Judge explanatory fit, source relevance and counterevidence; an attractive fit is not a proven cause. |
| **What different end, beneficiary, mechanism or question becomes possible?** | An attributed `TransformationAccount` may yield an `InquiryQuestion` or incomplete `CandidateExpression` under an `ExplorationFrame`. | Neither explanatory plausibility nor novel wording proves a valuable new `ProductPossibility`. Divergence is optional. |
| **What is sufficiently supported, worth investigating, comparable or preferable for this purpose?** | An `AssessmentActivity` considers original typed targets under an `AssessmentFrame`; its `AssessmentJudgment`, optional view and `AssessmentRevisionAccount` remain source/revision-scoped. | Evidence adequacy, expected inquiry learning, product attractiveness and construction priority require different criteria and authority. Assessment never implies selection or permission. |

The **operation** follows the actual question, not a document title, available Skill or proposed next stage. A narrow explanatory result may stop without creative transformation or ranking; pure divergence may occur without abduction; an assessment may reopen a premise or decline comparison.

## 2. Identity and assessment-target compatibility

`AssessmentTarget` is a **documentary typed-reference role**, not a new universal machine entity. For a diagnostic assessment of *explanatory adequacy*, an original source-qualified `Hypothesis` (an unestablished `Claim` in the Layered Ontology) **may be the assessed operand**. It retains its original observation, candidate explanation, source and epistemic identity.

This compatibility does **not**:
- reclassify `Hypothesis` as `CandidateExpression`, `ProductPossibility`, `ArchitectureOption` or `ConstructionPath`;
- extend executable relation/predicate endpoints (including prospective `ComparativeJudgment evaluates` or `ProvisionalPreference prefers`, which remain architecture/path-scoped);
- allow a comparison of different target types without an explicit shared criterion, or promote any comparison into a `Decision`.

A source-based diagnostic can use `AssessmentJudgment` as an attributed `Claim` about a `Hypothesis` or the contrast between H1/H2. This is **not** a new Graph `assessesTarget` predicate. Cite the source identity for each hypothesis, who assessed it, the shared explanandum, and the frame under which it was judged.

Original identity persists across transitions:

| Role | Original identity to retain | Do not silently replace with |
| --- | --- | --- |
| `Observation` / Claim | Source, detected statement, target snapshot and observation horizon | Later explanatory framing or expected result |
| `Hypothesis` | Claim/prose ID + explanandum + assumptions + author and source revision | A selected root cause or product option |
| `InquiryQuestion` / discriminator | Its question, possible different observed results and predecessor | An executed probe or a method chosen to obtain evidence |
| `CandidateExpression` | Exact original report and local expression ID; `TransformationAccount` inputs/outputs | A canonical `poss:` identity or duplicate merged away |
| `ProductPossibility` | Already reviewed enduring ID, if one exists | Every fragment or hypothesis that mentions a possible future |
| `AssessmentJudgment` / snapshot | Assessment report-file revision, target IDs, assessor, frame, criterion and **inspected target baseline** | The underlying target's identity or a timeless global rank |

Local IDs such as `I1.H1`, `I2.E1` and `I1.J` are **qualified by their source document**; they are not executable global identifiers.

## 3. Evidence and assumptions are claim-specific

For every consequential explanation, name its shared observed explandum, proposed mechanism, source-relevant supporting and challenging observations, absent or uninspected sources, assumptions, and what would change the hypothesis. One observation can fit several rivals; citation does not itself prove support. No number of citations can rank causes.

An assessment of the explanation asks **which hypothesis the evidence supports within a declared scope**. A separate assessment of its derived expression asks **whether a beneficiary would value the proposed difference, whether it is distinct from nearby sources, and what evidence could change that judgment**. The evidence supporting H1 cannot silently migrate as evidence for E1's desirability, novelty, feasibility or owner adoption.

A **discriminating `InquiryQuestion`** specifies potential observations that would differently affect named explanations. A **`ProposedInquiryApproach`** adds a concrete method/source-access plan, feasibility, cost and expected learning *if* a separate decision about doing the inquiry is warranted. Specifying either does not execute an experiment, validate an explanation or select an implementation task.

## 4. Coverage and comparability retain their denominator

Use the five existing [assessment coverage dimensions](possibility-assessment-ontology.md#31-coveragefinding--several-different-kinds-of-covered): corpus, conceptual breadth, consequence depth, empirical support and perspective coverage. They apply only after declaring the **typed corpus** and **purpose**.

- **Explanatory adequacy/coverage:** have the materially plausible explanations of a specific observed question been considered with grounds/counterevidence and a potentially discriminating observation? This is a purpose-specific judgment about explanations, not a new universal `CoverageFinding` enum.
- **Possibility-space coverage:** have materially different ends, beneficiaries, mechanisms, contexts and source-linked expressions been considered for a declared product question? Several explanations of one incident are **not** several futures.
- **Mixed presentation:** a crosswalk may show hypotheses, questions and expressions together, but coverage and comparison judgments preserve their own target-type denominators. An `Incomparable`, `UNRESOLVED`, `Conditional`, `NOT_ASSESSED` or outside-frame result is not a missing score or implicit last place.

A `ConsolidatedView` can group original expressions for one criterion; it must preserve their original source IDs, what was abstracted away and any disputed similarity. Counting names, graph records or source citations does not establish conceptual coverage or user value.

## 5. Two distinct revision histories

**Explanation/creative revision:** a changed source, premise or observation may narrow, preserve or challenge an earlier `Hypothesis`; a `TransformationAccount` records the attributed conceptual change to a revised explanation, question or expression, including predecessors. The observation retains its own original source state.

**Assessment revision:** a later `AssessmentRevisionAccount` refers to an identifiable earlier `AssessmentJudgment` or `PortfolioSnapshot` and explains changed evidence, questions, criteria, comparative alternatives, target baselines or authority. It does **not** retroactively modify the earlier assessment.

A hypothesis revision may warrant a *new* assessment of a dependent expression, or no change: ask whether the changed premise was actually necessary for that expression or judgment. Preserve both records and explain the actual delta. An assessment revision may in turn expose a new explanatory question. Neither automatically triggers the other.

## 6. Conditional moves and stop rules

`Explanation → evidence inquiry`; `explanation → divergent question`; `divergence → coverage`; `assessment → more divergence`; `assessment → comparison`; and **any step → justified stop** are possible author-selected intellectual moves, **not** registered stages or mandatory Abduct → Diverge → Rank → Build choreography.

Select the smallest operation that could change the actual decision or understanding. Do not manufacture extra hypotheses when only one is warranted, product futures where there is only wordplay, a ranked winner from incomparability, or a new graph relation because prose requires interpretation.

**Compact source-grounded account, when consequential:** name the source-revision-scoped explandum → H1/H2 and relevant grounds/assumptions → unrun discriminator and expected alternative outcomes → any attributed, genuinely different question/expression → purpose/typed targets of subsequent assessment → historical predecessor and delta → explicit uncertainty, authority and stop. No mandatory template, hidden cognition trace, machine parsing or extra receipt field.

## 7. Representation, portability, authority and qualification

Use existing `Observation`, `Claim`, `Hypothesis`, `Assumption`, `EvidenceSource`, `Provenance`, `InquiryQuestion`, `TransformationAccount`, `CandidateExpression` and assessment role meanings in source-addressable prose. If reviewed knowledge is warranted, use supported predicates/references; `attributes.conceptual_relation` records a claim, **not** enforced semantic truth. An authentic failed producer/consumer query with a necessary lost distinction is required before the [schema-evolution gate](../../skills/repository-semantic-steward/references/schema-evolution.md) can be reconsidered.

The portable agent methods [abductive inquiry](../../skills/strategic-repository-analysis/references/evidence-grounded-abductive-inquiry-v1.md), [divergence](../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md) and [possibility assessment](../../skills/strategic-repository-analysis/references/possibility-assessment-v1.md) must contain the actionable distinctions without requiring this framework checkout, index, CLI, new Skill or runtime. The `using-sensemaking` agent chooses their conditional use under ADR 0034; ADRs 0029/0031 preserve owner authority, original sources and evidence ceilings.

**Evidence ceiling:** source review and authored case reconstruction can show that semantic relations are *documentable*, not that a fresh host loaded the guide, that another agent applies it independently, or that any product future is valuable. Fresh read-only agent application is a separately warranted observation and remains `NOT_RUN` here.
