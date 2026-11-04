# Divergent Exploration Ontology v1 — Design Basis

**Date:** 2026-11-04.  
**Status:** design basis for the owner-requested implementation plan. The owner agreed with the preceding conceptual recommendations and requested a detailed plan; the concrete representation and file-level choices below are the planning agent's proposals. No ontology implementation or creative-benefit qualification is claimed.  
**Inspected repository:** `ThorStarlord/sensemaking-skills@8bd41bdf324e00aa75c1b849e333e076d85648ef`.  
**Implementation plan:** [Divergent Exploration Ontology implementation plan](../plans/2026-11-04-divergent-exploration-ontology.md).

## 1. Intent and useful outcome

Give the active coding agent a shared semantic model for opening and preserving materially different possibilities. The model should help it notice a changed question, a changed beneficiary or premise, a new desired end, a different realization of an existing end, a meaningful combination, and an admitted restatement.

The owner-endorsed direction centers on **questions, frames and meaningful differences between candidates**. Creative transformations, source provenance, bounded coverage and continuity across inquiries support that center. An emerging question or fragment must remain expressible before it becomes a complete product or architecture proposal.

The useful result is an agent that can produce a substantive divergent exploration and leave enough source-bound meaning for another reader to reconstruct, challenge and extend it. A count of ontology classes, completed template fields or graph records is not the success measure.

This develops the existing product purpose in [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md) and [product strategy](../../product-strategy.md). It does not select a new product thesis.

## 2. Current foundations and the bounded addition

The [layered ontology](../../semantic-architecture/ontology.md) already supplies Artifact, Claim, Hypothesis, Assumption, Goal, Constraint, EvidenceSource, Provenance and TargetSnapshot. The [prospective ontology](../../semantic-architecture/prospective-reasoning-ontology.md) separates reasoning activities from persistent possibilities and architecture options. [Creative discovery guidance](../../../skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md) already describes optional transformations and bounded novelty discrimination.

Existing CQ-099/100 and CQ-103 through CQ-114 cover reconstruction, novelty, changed premises, alternative outcomes and creative contribution. The [inquiry reconciliation](../../explorations/2026-11-03-inquiry-process-reconciliation.md) already describes distinct inquiry responsibilities and declines a schema or pipeline inferred merely from a new report. The [qualification-readiness record](../../normal-use/2026-11-04-independent-inquiry-operation-readiness.md) records no completed fresh operation trials.

The addition is a coherent semantic vocabulary and usable agent-facing representation for distinctions that are currently distributed across guidance and narrative reports. No existing source establishes that a new executable claim kind or automatic generator is necessary. The plan therefore implements a usable conceptual and documentary v1, connects selected material to existing reviewed knowledge, and leaves new parser/schema work conditional on a concrete consumer gap.

## 3. Approaches considered

| Approach | Useful property | Main cost or limit | Disposition |
| --- | --- | --- | --- |
| Archive and prompt guidance alone | Preserves rich prose with very low representation cost | Question/frame changes and identity judgments remain inconsistently explicit | Retain as the historical source foundation; insufficient by itself for this requested implementation |
| Semantic module, readable record profile and existing-vocabulary projection | Gives agents explicit distinctions, preserves fragments, supports reuse through existing surfaces | Requires careful semantic review; some relations remain documentary or unchecked attributes | **Proposed v1 approach** |
| Dedicated machine artifact, graph types and specialized queries immediately | Could support strict machine handoffs and filtering | No inspected consumer currently requires those fields; risks premature type and validator growth | Conditional follow-up only after a documented need |

The second approach is the planning agent's proposed implementation of the accepted direction. The owner has not independently selected every concept name, file path or optional future mechanism below.

## 4. Global constraints

These requirements are copied into the implementation plan.

- G1. The active agent remains the semantic controller; no new Skill, workflow engine, automatic next-stage transition, candidate ranking or implementation authorization is introduced by v1.
- G2. Preserve existing candidate identifiers, original records and historical judgments. A new expression, a revised interpretation and a new enduring possibility are different events.
- G3. Permit incomplete and unclassified candidate expressions. Do not require a product goal, value mechanism, architecture or canonical graph identity before an idea can be recorded.
- G4. Keep source facts, assumptions, interpretations, hypothetical outcomes, preferences and governing authority distinguishable. Every material judgment identifies its basis and scope.
- G5. Treat novelty, overlap and coverage as attributed, bounded judgments. No global originality claim, exhaustive possibility universe, numerical creativity score or fixed candidate/lens quota follows from the model.
- G6. Retain consequential meaning and provenance; do not persist private scratch reasoning or claim that a transformation account proves the model's internal cognitive cause.
- G7. Standalone Divergent Exploration ends with its landscape and a warranted stop or recommendation. Coverage Assessment, convergence, depth, strategic adoption and construction remain separately warranted responsibilities.
- G8. Use existing reviewed-knowledge kinds and predicates for v1. Do not bulk-promote the 59 archive candidates, change their dispositions, invent unsupported kind names or increment the universal knowledge schema.
- G9. Portable guidance must work from installed Skill references without a checkout of the Sensemaking framework, a SQLite index, a new CLI command or access to another repository's private sources.
- G10. Follow this repository's current CLAUDE.md policy: do not add or manually run local unit or synthetic evidence tests; use source/diff review and proportionate real-artifact checks, preserve hosted CI and release gates, and report NOT_RUN and evidence limits accurately.

G10 is a local construction policy, not part of the portable ontology or target-repository instructions.

## 5. Conceptual model

### 5.1 Concepts and roles

These are proposed conceptual definitions, not executable claim kinds. Existing concepts remain authoritative in their current scope.

| Concept or role | Meaning | Existing foundation and boundary |
| --- | --- | --- |
| **ExplorationInquiry** | A bounded reasoning activity opening possibilities around one or more related questions; may span sessions | Activity descriptors and Responsibility. A session and an inquiry are not required to have one-to-one identity |
| **InquiryQuestion** | A question whose meaning and revision history matter to the exploration | Related to Uncertainty, but a generative question need not already block a decision |
| **ExplorationFrame** | The beneficiary, desired end, scope, horizon, premises and constraints through which a question is interpreted | Composition of existing goals, assumptions, constraints and context; source-backed authority and revisable interpretation remain separate |
| **ExplorationLens** | An explicitly used perspective that makes certain distinctions salient | An activity descriptor; not a required pass or a closed list of viewpoints |
| **CandidateExpression** | A source-addressable expression of something worth considering, including a fragment or reframed question | Artifact/Claim content. It can express an existing ProductPossibility or ArchitectureOption, but does not require either |
| **TransformationAccount** | An attributed account connecting identified inputs, an asserted conceptual change and resulting expressions | Claim plus Provenance. A stated derivation is not verified cognitive causation or automatic graph inference |
| **PossibilityLandscape** | A bounded, revision-scoped view of candidate expressions and asserted relationships under a declared question/frame | Artifact content; not an inventory of all possible futures |
| **ExploratoryJudgment** | An attributed claim about novelty, similarity, difference, grouping or an inquiry limit | Existing Claim/Hypothesis semantics. Value ranking and authoritative selection remain outside a divergence-only result |

**Candidate is a role, not a replacement universal entity.** Keep ProductPossibility, ArchitectureOption, ConsequenceHypothesis and ordinary engineering alternatives distinct. A candidate expression may remain unclassified. A classification later established through review must cite its basis rather than rewrite its earlier expression.

### 5.2 Relationship meanings

The ontology module will define these conceptual relationships with endpoint roles, direction and examples. Their names are documentary vocabulary; they are not new executable predicates.

| Relationship | Intended endpoints | Meaning or qualification |
| --- | --- | --- |
| addressesQuestion | inquiry -> question | States the question an inquiry actually addresses |
| producesExpression | inquiry -> expression | Identifies the activity that authored or revised this expression; the record supports attribution, not an internal cognitive trace |
| respondsToQuestion | expression -> question | Preserves which question an individual expression addresses when an inquiry has several questions |
| interpretedUnder | inquiry or expression -> frame | Makes the relevant assumptions and beneficiaries inspectable |
| usesLens | inquiry -> lens | Records a perspective actually used; does not prescribe another pass |
| expressedIn | expression -> artifact | Anchors the exact authored expression |
| refersToCandidate | expression -> existing enduring candidate | Preserves a known identity; disputed identity belongs in a judgment |
| drawsOn | expression or transformation account -> source/claim/prior expression | Attributed source contribution; not an implementation dependency |
| revisesQuestion / revisesFrame | new question/frame -> predecessor | Identifies a material change while preserving the earlier meaning |
| hasInput / hasOutput | transformation account -> source or expression / expression | Identifies the account's operands without claiming an observed cognitive trace |
| includesExpression | landscape -> expression | Membership in this bounded view, with overlapping groupings allowed |
| summarizesInquiry | landscape -> inquiry | States which bounded inquiry this landscape records, including its revision/scope |
| assesses | judgment -> identified subject(s) | Carries criterion, comparison basis, assessor and applicable scope |

Near-duplicate, alternative, complement, revision, combination and changed-frame readings are **assertions made by a judgment**, not destructive identity operations. A relation's establishment and supporting evidence remain distinct from the truth of the relation.

### 5.3 Identity and revision rules

1. Give a retained record a stable repository-relative path and explicit local anchors such as `Q1`, `F1`, `C1`, `T1`, and `J1` only when referenced. No global UUID service is needed.
2. Qualify a local identity by its record. An old table label without an anchor is referenced by source path plus original label; do not fabricate a Markdown anchor.
3. A wording correction can preserve the candidate referent. A materially changed question or frame gets a distinguishable expression/version with its predecessor and stated delta.
4. A CandidateExpression records what was expressed at that point. Several expressions may refer to one enduring possibility; one expression may cite several predecessors without declaring their identities equivalent.
5. A synthesis can receive a new enduring identity only when its distinct meaning and retention value justify one. Mere reuse of the same capability does not establish sameness.
6. Preserve disagreement about identity or grouping as attributed claims. Never collapse source records merely because a later grouping treats them together.
7. Keep novelty relative to an identified comparison corpus, semantic dimension, source revision and assessor. Distinguish new wording, changed realization, changed beneficiary/end and changed question.

## 6. Usable representation and agent behavior

### 6.1 Readable exploration record

The v1 profile is a documentary contract for an agent and later reader. It has no registered `artifact_id`, parser, mandatory YAML sidecar or automatic validator.

Always make recoverable: the inquiry question and target; source scope/revision; the substantive output (including a justified no-new-candidate result); material uncertainty and authority limits; and the completion/continuation judgment.

Use explicit frame, lens, candidate, transformation and relationship entries when they preserve a material distinction. Small inquiries may express the same information in compact prose. Do not populate empty sections or fabricate a transformation to satisfy a template.

The template will offer these headings: **Inquiry and scope; Sources and premises; Frames and lenses; Candidate expressions; Relationships and judgments; Open territory; Completion and possible continuation**. Frame/lens/transformation detail is conditional on relevance. Candidate entries distinguish the source expression, its producing inquiry and question, an optional known referent, proposed meaning, consequential difference, assumptions and open questions. Shared context may be declared once for the record; repeat it per expression only when it differs.

The target's own documented artifact location wins. Otherwise, an authorized retained record may use `docs/explorations/YYYY-MM-DD-<topic>.md`; add an existing index pointer when useful. A read-only result remains in the response until retention is authorized. Session receipts point to legitimately retained records using their existing `artifact_refs`; no receipt schema changes.

### 6.2 How it should affect exploration

The active agent can use the model to notice repeated beneficiaries, unchanged ends, interchangeable mechanisms, hidden assumptions or a question that deserves revision. It chooses a helpful lens or transformation in response to those observations. It can also proceed directly when the distinctions are already clear.

The model does not require the agent to enumerate every lens, consult all prior answers before an intentionally independent first pass, assign every fragment a permanent type, or run Coverage Assessment as a hidden compulsory stage. Exposure to prior answers must remain explicit when independence matters.

Standalone divergence loads portable reference guidance directly under `using-sensemaking`. It must not silently invoke the whole Level-3 `strategic-repository-analysis` responsibility, whose contracted output remains a strategic analysis.

## 7. Existing-vocabulary knowledge projection

Implement a small framework-owned pack at `.sensemaking/knowledge/divergent-exploration.json` using `schema_version: 1`, the existing `claims`/`relations` envelope and the current proposal checker.

Proposed definition identifiers are `domain_concept:exploration-inquiry`, `domain_concept:inquiry-question`, `domain_concept:exploration-frame`, `domain_concept:exploration-lens`, `domain_concept:candidate-expression`, `domain_concept:transformation-account`, `domain_concept:possibility-landscape` and `domain_concept:exploratory-judgment`. Check for existing meanings/IDs and reuse a genuine equivalent. Definitions use `kind: domain_concept`, document authority, `epistemic_status: declared`, and the actual ontology source.

A `source:divergent-exploration-reference-cases` claim can make the worked record discoverable with existing search/explain. Its statement concerns the document and its scope; it does not certify the hypotheses in it. Use a small set of source-backed `references` relations where they improve a real reader's reconstruction. Specific conceptual meanings may live in `attributes.conceptual_relation`; report that these meanings are not mechanically checked.

A complete product future may later use an `opportunity`/`poss:` record, a structural option an `alternative`/`arch:` record, and a conditional effect a `hypothesis`/`conseq:` record under the existing Steward contract. Fragments, questions and tentative grouping do not become opportunities merely to enter the index. The complete narrative remains the record of origin.

This pack lives in the framework repository. Installed guidance must not import its claims or authority into a target. Each target's retention uses its own sources and authorization.

## 8. Representation cases and completion evidence

Use a bounded case set, with source revision and original labels preserved:

- **Atlas belonging hypothesis:** separates source-backed host/guest architecture from the hypothetical experiential outcome and the attributed reframing.
- **DE-A2 and DE-B1:** preserves question collision and role migration as changes in what is being asked or for whom, before requiring a complete future proposal.
- **GD-D and DE-F2:** preserves two historical expressions while recording the existing near-duplicate judgment.
- **DE-G1, NX-N2 and NX-K3:** distinguishes competing interpretations, condition-dependent validity and differing observation conditions despite shared plurality language.
- **NX-M1, RP-Q1 and RP-Q2:** distinguishes recoverable hiding, reduced dependence and non-capture; preserves a changed desired end.
- **One explicitly illustrative incomplete question:** demonstrates that a fragment can be retained without invented value, architecture or empirical provenance.

These are representation cases, not new independent exploration trials. Record each competency as **faithful**, **awkward**, **lost**, or **not established**, with its reason and source. Reuse CQ-099/100 and CQ-103..114; local DEO-CQ identifiers refine this implementation without renumbering or duplicating the global catalogue.

V1 completion requires coherent meanings and identity rules, usable portable guidance, faithful worked cases, a retained record a reader can reconstruct, and a small valid/retrievable existing-vocabulary projection. Report actual source review, artifact/knowledge checks and installed-reference delivery separately. Improved creativity, independent repeatability and graph-specific causal benefit remain distinct, unproven claims unless separately observed.

## 9. Conditional growth and limits

Add a machine artifact only when an identified consumer must parse or transfer specific fields that the current record cannot reliably supply. Add a new graph type or query only when an authentic question loses a necessary distinction or answer under supported representations. Use the [schema-evolution procedure](../../../skills/repository-semantic-steward/references/schema-evolution.md), including alternatives, compatibility and required authority.

The core implementation must not be deferred merely because those optional mechanisms are unwarranted. It should deliver the model, agent use and reusable examples through existing capabilities.

## 10. Review and acceptance

Review the design against five failure conditions: incomplete candidates forced into mature product types; false merging of similar expressions; source facts promoted into creative-value claims; frames that turn revisable implementation facts into permanent constraints; and framework-only links that break in an installed Skill.

No remaining owner answer is required to make this plan concrete. The proposed names, paths and representation choices can be reviewed as one coherent design; a later implementation request supplies execution scope. Saving this design and plan does not mark any future task completed.
