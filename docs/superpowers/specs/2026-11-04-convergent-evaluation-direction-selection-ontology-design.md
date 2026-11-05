# Convergent Evaluation and Direction Selection Ontology v1 — Design Basis

**Date:** 2026-11-04
**Target:** ThorStarlord/sensemaking-skills; planning source baseline \`main@4ef254cd6251e515910e2187de22195d0e49401d\`
**Status:** design accepted in conversation; implementation is **not** part of this planning change.
**Companion plan:** [implementation plan](../plans/2026-11-04-convergent-evaluation-direction-selection-ontology.md)

## 1. Intent

**Question:** Given source-grounded alternatives, an explicit purpose, current premises and the decision authority actually available, which direction—if any—should guide subsequent work, what does that choice settle, and what would warrant reconsidering it?

Develop **focused conceptual semantics for convergence to a scoped selection**, not another generic evaluation model. Preserve the useful result of a real choice for future agents: the chosen target, why it was worth choosing *at all*, why it was preferred to credible alternatives, accepted tradeoffs, scope, decision authority, nonselected alternatives, and reconsideration conditions. A returning agent must be able to continue **within** a decision without replaying all option analysis, while also recognizing when new evidence defeats a decision-critical premise.

Convergent Evaluation answers "what should we do?" **at a named level**. It may select (1) an \`InquiryQuestion + ProposedInquiryApproach\` for further intellectual inquiry, (2) a product future/direction for further strategic development, (3) an \`ArchitectureOption\` or \`ConstructionPath\` when the appropriate Level-3 process selects one, or (4) independently authorized bounded implementation work. These are different target types and different authority/commitment levels. A selection may be conditional or unavailable; it is not always a single winner.

## 2. Existing foundations and gap

Reuse, rather than reimplement:

- [Possibility Assessment and Prioritization Ontology](../../semantic-architecture/possibility-assessment-ontology.md): AssessmentFrame, typed AssessmentTarget, AssessmentJudgment, PurposeRelativeComparison, PortfolioSnapshot, method-sensitive inquiry priority, revision; **evaluation != decision**.
- [Divergent Exploration Ontology](../../semantic-architecture/divergent-exploration-ontology.md) and [Product Possibility Ontology](../../semantic-architecture/product-possibility-ontology.md): original expression, question, frame, retained \`poss:\` identity, source provenance, no automatic promotion.
- [Prospective Reasoning Ontology](../../semantic-architecture/prospective-reasoning-ontology.md): \`EVALUATE\` versus \`SELECT\`, \`ProvisionalPreference\` versus \`Decision\`, narrow existing \`evaluates\`/\`prefers\`/\`selects\` endpoints for architecture options and construction paths.
- [Warrant / Choice Policy v0](../../../skills/using-sensemaking/references/warrant-choice-policy-v0.md): target-specific warrant, \`NO_SELECTION\`, smallest sufficient intervention, premise currency, action authority orthogonal to semantic warrant.
- [Adaptive Skill Composition](../../../skills/using-sensemaking/references/adaptive-skill-composition-v1.md) and [Strategic Exploration Funnel](../../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md): conditional activities, specialist evidence return to the active controller; no fixed stage engine.
- Accepted [ADR 0029](../../adr/0029-current-product-boundary.md) and [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md): no automatic strategic ranking/selection, no decision authority from an artifact, breadth before consequential convergence, optional implementation.

**Gap:** These already define comparison, warrant and decision separately, but a later reader often has to reconstruct the *transition*: Which specific assessment and warrant claims justified an actual **selection**, what exactly was adopted (vs merely recommended), which rejected/deferred alternatives remain viable, and what continuation can legitimately inherit? This design makes that transition explicitly interpretable without inventing a new control layer.

## 3. Approaches examined

| Approach | Strength | Cost / problem | Disposition |
| --- | --- | --- | --- |
| **Cross-link only**: refer readers to assessment and warrant policy | Minimal maintenance | Leaves selection scope, nonselected alternative dispositions, and inherited work limits scattered across documents | Reuse all underlying meaning, but insufficient as the primary result |
| **Focused conceptual specialization + portable selection profile** | Makes a real selection, conditional/no-selection outcomes and continuation reconstructible with minimal novelty | Requires semantic discipline and source-cited examples; remains documentary rather than machine-interpretable | **Recommended / accepted design direction** |
| **Selection runtime/state machine and executable schema** | Easily parsed outcomes and automated downstream routing | Confuses semantic authority with workflow execution; not warranted by an identified consumer, risks contradicting ADR 0029 | Explicitly excluded from v1; conditional separate proposal only |

The design does not add a universal ontology class for every row below. It defines **documentary roles**, most of which specialize existing \`AssessmentJudgment\`, \`Decision\`, \`Artifact\` or reference relationships.

## 4. Conceptual roles

| Role | Meaning and boundary |
| --- | --- |
| **ChoiceQuestion** | The exact question the selecting actor intends to settle, including the decision level, beneficiary, scope and permitted kind of commitment. Can reuse InquiryQuestion/AssessmentFrame; do not reduce "what next?" to an undifferentiated ranking. |
| **ConsideredChoiceSet** | Source-qualified, type-consistent credible alternatives, including status quo/no change where it materially affects the choice. Records coverage adequacy and exclusions; no fixed minimum count and no invented alternative. |
| **CandidateWarrant** | A defeasible account for a *specific target*, including prerequisites, evidence/counterevidence, authority requirements, meaningful consequences and uncertainty. Derived from existing Warrant / Choice Policy; not a confidence scalar or new universal status object. |
| **ConvergenceRationale** | Why one warranted target is preferable **for this choice purpose**, including marginal contribution, accepted costs, plausible contrary perspectives, comparator distinctions and the reason that another option is not preferred now. Reuse AssessmentJudgment/qualitative comparison. |
| **ScopedDirectionSelection** | An actual agent-/owner-authored \`Decision\` selecting an existing typed target in a named scope with actor/authority, date, evidence and what downstream work may treat as settled. A *recommendation* is not this role. Do not create another canonical target identity. |
| **AlternativeDispositionAccount** | For material nonselected alternatives, distinguish declined under this frame, deferred, retained as complementary, outside scope/incomparable, defeated by evidence, not assessed or superseded. Nonselection does not equal universal rejection. |
| **SelectionReconsiderationBoundary** | The decision-critical premise/source/currentness/owner-goal or condition that would trigger reassessment; the choice remains historical even if later superseded. Triggers reconsideration, not automatic reversal or routing. |
| **SelectionHandoff** | A concise bounded interpretation for subsequent work: inherited question, selected target, accepted tradeoffs, what remains open, prerequisites, forbidden inferences and stop conditions. Use existing PR/ADR/strategic artifact/receipt/handoff surfaces before inventing another artifact. |

A **DirectionSelectionRecord** is a *documentary profile for these meanings*, not a new executable artifact kind. Do not interpret all \`ConvergenceRationale\` as enacted selections: cases with insufficient warrant, reserved authority, incomplete choice sets, or insufficient decision need can validly end without \`ScopedDirectionSelection\`.

## 5. Semantic relationships, stages and invariants

This is an **interpretive relationship model**, not a machine predicate list:

\`\`\`text
ChoiceQuestion isAddressedBy AssessmentActivity
ConsideredChoiceSet contains existing typed AssessmentTargets
CandidateWarrant evaluatesPrerequisitesFor one target
ConvergenceRationale compares supported targets under AssessmentFrame
ScopedDirectionSelection selects existing target within SelectionScope
ScopedDirectionSelection cites CandidateWarrant and ConvergenceRationale
AlternativeDispositionAccount concerns nonselected source-qualified alternatives
SelectionHandoff inherits scoped choice, not downstream work authorization
SelectionReconsiderationBoundary qualifies ScopedDirectionSelection
Later reconciliation reconsiders, never rewrites, earlier decision
\`\`\`

**Hard distinctions:**

1. *Comparative preference* may exist without a selection; *selected for further inquiry* does not mean *adopted product strategy*, *selected architecture* or *authorized implementation*.
2. \`Decision\` with an established actor/authority and scope differs from \`Recommendation\`, a report's "top-ranked" entry and \`ProvisionalPreference\`. Selection can be agent-decided within explicitly delegated bounds; owner-reserved thesis revisions still require owner ratification.
3. A candidate can be **preferable to peers but unwarranted to select**. CandidateWarrant and ConvergenceRationale therefore cannot collapse into a ranking.
4. No choice is forced: valid results include genuine **NO_SELECTION**, owner decision required, more evidence needed, option-set incomplete/reopen alternatives, bounded provisional preference, or an actual scoped selection. Reuse existing policy dispositions and strategic artifact terminology; do not create conflicting executable enums.
5. A **new synthesis** can be the target of a choice only when the synthesized option's distinct meaning, assumptions and consequences have been assessed. Merely aggregating benefits is not a synthesis warrant. Source candidates remain traceable.
6. The selected direction may guide a later agent within its **scope** without authorizing a Skill call, code, external mutation, protected merge or release. "Selection is inherited" means check decision-critical prerequisites before operating on it; it is not a pipeline.
7. Alternatives retain provenance and local identity. No selected \`poss:\` identity is silently created from grouped expressions or an outcome-family label; no failed comparison implies \`sameAs\` or universal rejection.
8. A stale source baseline may justify a currentness check but does not automatically invalidate historical selection or reopen Level-3/Level-4 strategy.
9. A source-grounded selection can still be wrong or based on an owner's preference; structural validity is not correctness.
10. Level-4 thesis commitments (e.g., ADR 0034) are different from Level-3 strategic direction choices and ordinary bounded selections; a recommendation does not imitate owner ratification.

## 6. Reference cases and critical counterexamples

Use *real existing records*, pinning their **file-containing revision** separately from any inspected source baseline. Distinguish historical claims from conceptual annotations.

- **S1: Provisional convergence without selection.** [2026-11-03 accumulated Convergent Evaluation](../../explorations/2026-11-03-convergent-accumulated-creative-possibilities.md) explicitly produces alternatives for potential depth inquiries, *not* a selected strategic direction, architecture or construction task. Assess if a reader can reconstruct why a candidate remains open.
- **S2: A preferred inquiry versus an adopted decision.** [2026-11-04 coverage/portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md), §§6–8, recommends owner-agency depth inquiry. It does not establish that the owner adopted it, started the inquiry or changed thesis. The Future/Continuity synthesis is an interpretation, not selected new architecture or ratified goal.
- **S3: Actual owner-ratified product selection.** [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md) identifies owner selection, authority and explicit commitments, including the single public entrypoint and breadth-before-convergence. It expressly differs from merely proposed/implemented/qualified capability.
- **S4: Provisional architecture and feedback.** [Prospective ontology](../../semantic-architecture/prospective-reasoning-ontology.md) records a preferred \`ArchitectureOption\`/ConstructionPath and how consequence depth can reaffirm, revise, reopen or defer. An architecture preference by itself is not a selected strategic path or implementation authority.
- **S5: No justified selection / incomplete options.** [Warrant / Choice Policy](../../../skills/using-sensemaking/references/warrant-choice-policy-v0.md) defines \`NO_SELECTION\`; [owner-decision-capsule](../../../skills/owner-decision-capsule/SKILL.md) defines \`OPTION_SET_INCOMPLETE\`. These are **policy cases**, not fabricated historical trial results. A separately labeled illustration may show what a record would look like.

**Negative checks:** (a) no selection from a ranking; (b) no automatic execution after direction selection; (c) no owner decision from agent recommendation; (d) nonselected alternatives not globally rejected; (e) no selecting a composite direction whose effects were never examined; (f) when option coverage fails, no forced binary or total order.

## 7. Proposed v1 representation and intended consumers

- Canonical **Level-2 ontology module** and local competency questions linked to existing ontology/semantic navigation.
- A **portable, self-contained guide** in the current strategic-repository-analysis references, plus optional Markdown decision record template. Agent needs only the installed Skill tree and the target's sources/authority.
- **Conditional reference cue** through existing \`using-sensemaking\` and strategic-funnel/choice guidance, only when selecting a direction is *actually* the warranted responsibility. No new public Skill.
- **Source-pinned case annotations** of the examples above, including actor and authority distinctions; no bulk rewrite of historical exploration docs or backfilled decisions.
- **Selective reviewed-knowledge projection** of durable *concept definitions and source references* under existing v1 \`domain_concept\`/\`source\`/\`references\` only when it improves discoverability. It must pass the existing checker; do not turn policy dispositions into graph kinds or automatically record every selected choice as a graph Decision.
- **Existing continuation surfaces** (ADR, Level-3 strategic artifact, ordinary PR note, receipt, handoff) remain authoritative for actual choices. The ontology documents their meaning but does not replace them.
- **Mechanical and documentary verification:** source/diff, links and identity; existing JSON proposal checker and exact-commit retrieval if used; real wheel/install reference parity; fresh reader reconstruction when available. The current repository's local construction exception limits manually authored unit/synthetic tests; apply its current \`CLAUDE.md\` at execution.

**When to formalize more:** only when a real producer/consumer demonstrates a parsed-field requirement that source-linked prose cannot satisfy, or when a specific query loses a necessary selection-scope distinction under existing \`Decision\`, \`Claim\`, \`source\`, \`references\` and authority surfaces. Follow the repository's existing [schema evolution](../../../skills/repository-semantic-steward/references/schema-evolution.md) and owner boundaries.

## 8. Success, failure and stop criteria

**Successful documentary v1:** a later reader can reconstruct whether a selection happened, the authority and target, selection scope, warrant, why not the alternatives, remaining unknowns, and whether any currentness change requires reconsideration; the installed guide makes those distinctions available with no new runtime dependency. It can also faithfully report **NO_SELECTION** or a reserved-owner handoff.

**Failure even when mechanically valid:** provisional ranking presented as adoption; wrong target granularity; disappearing alternatives; selection interpreted as authorization; unsupported synthesis; made-up ratification; fixed-stage mandatory funnel; or overstatement of an independent benefit claim.

**Evidence ceiling:** structural validation and source-document reconstruction are not proof of better choices, effective autonomous continuation, owner satisfaction or incremental creative merit. Independent benefit and causal graph advantage remain separate empirical inquiries. Nothing in this design asks the implementer to automatically conduct them.
