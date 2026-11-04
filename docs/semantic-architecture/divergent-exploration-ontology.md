# Divergent Exploration Ontology v1

**Status:** implemented conceptual module and documentary semantics, 2026-11-04.
**Scope:** opening and preserving materially different questions, frames and candidate meanings.
**Authority:** implements the owner-authorized [design basis](../superpowers/specs/2026-11-04-divergent-exploration-ontology-design.md) within ADR 0034; definitions do not establish product facts, creative benefit or permission to act.

## 1. Purpose and foundation

An exploration should let a later reader recover what was asked, how an
expression made sense, what appeared different, and which evidence and
judgments support that interpretation. A useful expression can be a question,
tension, analogy or incomplete fragment before a coherent future is available.

This module extends the [layered ontology](ontology.md) and
[prospective reasoning model](prospective-reasoning-ontology.md).
It separates four things: the inquiry activity, the artifact retaining it,
an expression authored at a particular point, and any enduring possibility
that expression refers to. An inquiry can span sessions; a session can contain
several inquiries. A session receipt records execution facts and pointers.

The active agent uses these meanings when they help the requested inquiry.
The model supplies no automatic sequence, closed set of lenses, candidate
quota, creativity score, ranking or construction authority.

## 2. Concepts and neighboring meanings

### ExplorationInquiry

A bounded reasoning activity opening possibilities around one or more related
questions. Its scope includes the target, source boundary and permitted
outcome. It is a Work-layer activity descriptor performed under a
Responsibility, not a new executable responsibility type or Campaign.
Completion can be a useful landscape, a justified no-new-expression result,
or an explicit unresolved boundary.

### InquiryQuestion

A concern whose meaning and revision history matter to exploration. A
generative question need not already block a decision. It can concern an
existing Uncertainty without becoming an executable Campaign Uncertainty.
A question has no truth value merely because its wording is retained;
answers and premises can be Claims or Hypotheses.

### ExplorationFrame

The beneficiary, desired end, situation, scope, temporal horizon, premises
and constraints under which a question or expression is interpreted.
Frames compose Intent-layer goals/constraints and Knowledge-layer
assumptions with context. Partial frames are valid. Unknown dimensions stay
unknown. Distinguish governing constraints from revisable interpretations
and observed implementation facts; the last category is not automatically
a permanent product limit.

### ExplorationLens

An explicitly used perspective that makes certain distinctions salient.
It describes an activity, not a mandatory pass. A lens may foreground a
different beneficiary, timescale, observation condition or desired end.
Naming a lens does not prove it generated a materially different expression.

### CandidateExpression

A source-addressable articulation worth considering at that point in the
inquiry. It can be a question, fragment, outcome sketch, mechanism proposal,
or combination. It is Artifact content; propositions within it can be Claims
or Hypotheses, but every expression need not assert a proposition.

An expression can refer to an existing ProductPossibility or ArchitectureOption.
It can also remain unclassified. Candidate is a role, not a replacement
universal entity. Recording an expression does not curate it into reviewed
knowledge or establish a durable product identity.

### TransformationAccount

An attributed account connecting identified inputs, an asserted conceptual
change and resulting expressions. It is a Claim with Provenance, such as
an author's explanation of reframing a constraint as a possible experience.
It preserves a consequential explanation rather than private scratch
reasoning. An authored account is not an observed internal cognitive trace,
a deterministic derivation, or evidence of causal creative improvement.

### PossibilityLandscape

A bounded, revision-scoped view of expressions and asserted relationships
under an identified inquiry and frame. It is Artifact content. Membership
and grouping can overlap; the view is not an inventory of all possible
futures. Its inspected corpus and acknowledged omissions bound later
novelty and coverage judgments.

### ExploratoryJudgment

An attributed Claim about novelty, similarity, difference, grouping or an
inquiry limit. It identifies its subject(s), criterion, comparison basis,
source/revision scope, assessor and material uncertainty. Unknown attribution
or evidence is explicitly unknown. Depending on its basis, the judgment may
be inferred, hypothesized or otherwise grounded under the existing
[epistemic model](relations-and-epistemics.md).

This role does not broaden the architecture/path endpoints of
ComparativeJudgment or ProvisionalPreference. Value ranking, strategic
selection and action authority belong to their separately warranted
responsibilities. A later coverage judgment can use this role without making
Coverage Assessment a compulsory part of divergence.

## 3. Relationship meanings

These are documentary relationships with semantic endpoint constraints.
They are not additions to the executable predicate enum. An artifact can
establish that an author asserted a relationship; establishing the
relationship itself may require further evidence or interpretation.

| Relationship | Direction and endpoints | Establishment and example |
| --- | --- | --- |
| `addressesQuestion` | ExplorationInquiry -> InquiryQuestion | Explicit inquiry scope or an attributed reconstruction. Example: an inquiry asks which player experience a host/guest distinction could support. |
| `producesExpression` | ExplorationInquiry -> CandidateExpression | Source identifies authorship or revision. Example: a retained divergent report contains DE-B1; this attributes the expression, not an observed mental process. |
| `respondsToQuestion` | CandidateExpression -> InquiryQuestion | Explicit answer connection or labeled interpretation. Example: one expression answers a beneficiary question while another answers an observation question in the same inquiry. |
| `interpretedUnder` | ExplorationInquiry or CandidateExpression -> ExplorationFrame | Declare shared context or a justified expression-specific difference. Example: reduced software dependence is the desired end for a successful-exit expression. |
| `usesLens` | ExplorationInquiry -> ExplorationLens | Record a perspective actually stated or used; label retrospective attribution. Example: a source explicitly considers another beneficiary. |
| `expressedIn` | CandidateExpression -> Artifact | Resolve an actual source location and revision. Example: source path plus table-local DE-F2 label; a fabricated URL anchor is invalid provenance. |
| `refersToCandidate` | CandidateExpression -> existing enduring prospective entity | Cite the identity basis. Example: a later expression explicitly develops a known `poss:` record; disputed identity stays a judgment. |
| `drawsOn` | CandidateExpression or TransformationAccount -> EvidenceSource, Claim or prior CandidateExpression | Attribute the contribution and its uncertainty. Example: a reframing account cites a documented ownership boundary. |
| `revisesQuestion` / `revisesFrame` | new InquiryQuestion/ExplorationFrame -> its predecessor of the same role | Retain predecessor, material delta and reason. Example: shifting from recoverable hiding to principled non-collection changes the desired end. |
| `hasInput` / `hasOutput` | TransformationAccount -> source/claim/expression input; TransformationAccount -> expression output | Identify the account's operands. Example: a report connects non-ownership to a hypothetical belonging experience; the effect remains hypothetical. |
| `includesExpression` | PossibilityLandscape -> CandidateExpression | Explicit membership in the bounded view. Example: a comparison retains both GD-D and DE-F2 despite a near-duplicate judgment. |
| `summarizesInquiry` | PossibilityLandscape -> ExplorationInquiry | State which inquiry and revision/scope the view records. Example: an accumulated landscape draws from named archive passes, with known omissions. |
| `assesses` | ExploratoryJudgment -> identifiable expression(s), frame, question, landscape or relation assertion | Criterion, operands, corpus, assessor and basis travel together. Example: a dated convergence judges two expressions near duplicates within its inspected corpus. |

The input endpoint of `hasInput` and the output endpoint of `hasOutput`
have different roles; the slash notation does not create one ambiguous
relation. Likewise, question and frame revision preserve their own kinds.

## 4. Identity, revision and historical integrity

1. Qualify a local identity by its artifact. Use explicit local headings
   such as `Q1`, `F1`, `C1`, `T1`, `J1` when cross-reference helps.
   Existing table labels retain their source path plus original label.
2. Preserve the authored expression and its source-file revision. Distinguish
   that revision from an earlier target baseline reported inside the artifact.
   A report's inspected baseline may predate the report itself.
3. A wording correction may preserve meaning and referent. A changed question,
   beneficiary, desired end, premise or truth condition needs a distinguishable
   version/expression and stated delta. Stable local IDs never justify silently
   rewriting an older interpretation.
4. Several expressions may articulate one enduring candidate. An expression
   may refer to several known entities or cite several predecessors. Neither
   shared wording nor a shared mechanism establishes identity.
5. Near duplication, variant, complement, alternative, combination and
   changed-frame readings are attributed judgments. Preserve both operands,
   including disagreement. Group membership is not `sameAs`.
6. A synthesis earns a new enduring identity only when its distinct meaning
   and retention value warrant one. Existing ProductPossibility,
   ArchitectureOption and ConsequenceHypothesis meanings continue to govern.
7. Preserve historical dispositions. Reopening a rejected candidate needs the
   changed premise and the earlier assessment; it does not erase rejection.

## 5. Difference, novelty and inquiry limits

Explain the consequential difference in ordinary language: desired end,
beneficiary, mechanism, assumption, scope or truth conditions can matter.
These are useful dimensions rather than a mandatory taxonomy. For example,
competing interpretations, condition-dependent validity and alternative
observation conditions all involve plurality but make different claims.

A novelty judgment names the comparison corpus and its revision. It may
concern wording, realization, beneficiary/end or question. A missing graph
record means absence from that graph, not global originality. An unexamined
dimension remains NOT_ASSESSED rather than proven absent.

A standalone divergent result reports its landscape, uncertainty and reason
to stop or continue. Another lens is useful when it could change a material
question or candidate meaning; repeating differently worded versions of the
same end is a reason to reconsider the inquiry. This is a bounded judgment,
not a saturation score or universal stopping threshold. Coverage Assessment,
consolidation, comparison, depth and implementation keep their own purposes
and authority.

## 6. Representation and selective retention

| Semantic content | V1 representation | Boundary |
| --- | --- | --- |
| Inquiry, question, frame, lens | Source-addressable prose/entries in a readable exploration record | No new executable kind, Campaign object or fixed form |
| Expression and landscape | Artifact content with local identity and context | Record retention does not create an enduring possibility |
| Transformation and exploratory judgment | Attributed passages; existing Claim/Hypothesis semantics when selectively retained | Account, evidence, interpretation and authority remain distinct |
| Definitions of the eight roles | Existing `domain_concept` claims, document authority, `declared` epistemic status | A definition claim is not an instance of that role |
| Discoverable retained record | Existing `source` claim with legitimate source references | Describes a document and scope; does not certify its hypotheses |
| Coherent product future, structural option, conditional effect | Existing `opportunity`/`poss:`, `alternative`/`arch:`, `hypothesis`/`conseq:` conventions when warranted | Fragments are not promoted to satisfy indexing |
| Specific relation without a supported predicate | Source prose or `references` with `attributes.conceptual_relation` | Attribute meaning is not mechanically checked |

Use the current [knowledge contract](../../skills/repository-semantic-steward/references/knowledge-contract.md)
and [schema-evolution procedure](../../skills/repository-semantic-steward/references/schema-evolution.md).
The readable profile adds no registered `artifact_id`, parser, mandatory
sidecar, new predicate or schema version. Existing session receipts can point
to authorized retained documents through repository-relative `artifact_refs`.

The framework's definitions and examples are not automatically a target
repository's facts or authority. Portable guidance must contain its required
meanings and use the target's own sources and retention conventions.

## 7. Competency and growth boundary

The [local competency matrix](divergent-exploration-competency-v1.md) maps
these meanings to existing CQ-099/100 and CQ-103..114. Source fidelity,
documentary reconstruction, structural validity, retrieval, installed delivery,
observed use and independent creative benefit are separate evidence categories.

A machine artifact needs an identified producer/consumer and exact fields that
the readable record cannot reliably supply. A graph/query extension needs an
authentic lost distinction or answer and comparison with existing references,
attributes and prose. Either follows the existing evolution process.
An unchecked attribute alone does not establish a schema gap.
