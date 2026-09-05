# Repository Sensemaking Brief

## 1. Repository goal

Auteur appears to be an author-authority-centered narrative engineering system for long-form fiction. Its core direction is not simply prose generation: it represents author-declared narrative intent and canonical state as typed artifacts, compiles and evaluates those artifacts across narrative scopes, and keeps generated analysis or proposals derivative until the author accepts them.

At the frozen target snapshot, the product already spans a scope hierarchy from Universe through Series, Book, Chapter, and Scene. The consequential question is therefore no longer whether Auteur needs another foundational architecture layer, but which author-facing capability should be strengthened next and what evidence should justify that choice.

## 2. Current shape

The repository is organized around a substantial Python package under `src/auteur/`, with domain-specific modules for story identity, blueprints, chapters/scenes, reasoning, reconciliation, publishing, provenance, Series, and Universe behavior. The documentation layer includes architecture descriptions, ADRs, capability coverage, workflow guidance, and explicit pilot/evidence records.

For the long-horizon boundary specifically, `src/auteur/series/` contains a real Series subsystem rather than a placeholder: models, compiler, CLI, graphing, diagnostics, continuity validators, handlers, serializers, bible generation, and related support modules are present. `SeriesIdentity` is canonical and can hold book plans plus cross-book character, relationship, faction, mystery, dependency, and thematic structures. The documented narrative scope model likewise assigns Series responsibility for cross-book continuity and progression.

The product evidence path is more mature at smaller scopes. `docs/capability-coverage.md` records bounded Scene/Chapter and Book workflow evidence and describes choosing subsequent implementation from observed author friction.

## 3. Strong signals

- The repository has an explicit scope model rather than letting long-form hierarchy emerge implicitly. Series is defined as the cross-book continuity/progression scope.
- Series is represented by a first-class canonical model with multiple `BookPlan` entries and cross-book arc/dependency structures.
- The Series ADR deliberately preserves author-declared canonical intent while treating compiled identities, diagnostics, graphs, and bibles as derivative outputs.
- The architecture roadmap explicitly says the remaining work is vertical author workflow/capability refinement rather than another foundational architecture.
- The capability-coverage record uses empirical progression: it names bounded pilots, records what was actually traversed, and says the next implementation slice should be selected from evidence rather than theory.
- Book-level workflow has advanced materially enough that the repository documents a bounded two-Chapter Book Manuscript path as proven, which gives a concrete lower-scope baseline for a next product probe.

## 4. Missing pieces

The explicit evidence trail inspected at this frozen snapshot does not yet establish comparable author-facing decision evidence at the Series/long-horizon boundary. The controlled pilot guidance remains deliberately bounded below a large Series, while the recorded evidence-selected implementation path is Book-level.

That is not evidence that Series code is absent or untested, and it is not a claim that a large-Series pilot should be run next. It is a narrower gap: the repository already has a meaningful Series representation and executable surface, but the inspected product-evidence record does not yet show which parts of that surface create the most consequential author friction when a real cross-book plan is created, reviewed, revised, and carried into Book work.

Local-only probe metrics such as verification gap, context entropy, fixture coverage, and churn were not measured in this connector-only run and are not inferred.

## 5. Improvement opportunities

1. Exercise the existing Series surface with a deliberately small cross-book project before adding another architecture concept.
2. Observe where author friction appears when moving between Series intent and Book-level planning rather than assuming that the next weakness is structural revision propagation or another preselected feature.
3. Compare a Series-first planning path with a Book-first path to learn whether the existing hierarchy helps an author preserve long-horizon intent or merely adds ceremony.
4. Capture one reproducible highest-impact friction point and use it to select exactly one subsequent implementation slice, or record that no Series-specific implementation is yet warranted.

## 6. Weakest boundary

The weakest consequential boundary is the **author-facing evidence boundary between Auteur's first-class Series architecture and the decision about what major capability should be developed next**. The architecture already expresses long-horizon structure; what remains comparatively under-demonstrated in the inspected evidence is how that structure performs as an author workflow on a bounded real cross-book problem.

**Weakness type:** Other

`Other` is used because this is a product-validation/decision-evidence boundary, not a demonstrated repository/code defect. Calling it `Zero Validation` would overstate the evidence and could falsely imply that Series core logic lacks automated validation.

## 6.5. Problem classification (fog type)

**Primary fog type:** `product_fog`

The uncertainty concerns which author problem deserves the next implementation slice and what workflow evidence should determine that choice. The repository architecture is comparatively explicit; the unresolved issue is product priority under real author use.

## 7. Evidence

<!-- mode: investigative -->

At the frozen snapshot, `docs/narrative-architecture.md:26` assigns Series responsibility for cross-book continuity and progression, while `src/auteur/series/models.py:213-230` shows a first-class `SeriesIdentity` with one-or-more book plans and several cross-book arc/dependency collections. `docs/adr/012-series-engine-v1.md:16-38` documents Series as a canonical layer above StoryIdentity and distinguishes canonical author-declared series intent from derivative compiled/diagnostic artifacts.

The repository's own roadmap points away from another architecture layer: `docs/architecture-roadmap.md:201-216` says the foundational architecture is stable enough that the remaining work is vertical author workflow/capability refinement and that the next implementation should be selected from author friction. The controlled pilot in `docs/capability-coverage.md:108-112` is deliberately bounded and explicitly says not to begin with a large series. Its completion criteria at `docs/capability-coverage.md:170-172` require a reproducible missing capability and evidence-selected next slice; later, `docs/capability-coverage.md:194-214` records Book-level workflow as the evidence-selected slice and a bounded two-Chapter Book Manuscript path as proven.

Logic trace: the exact frozen snapshot demonstrates that Series is already a substantive architectural and executable product surface; the same snapshot's planning documents say foundational architecture is largely complete and that new implementation should follow observed author friction; the explicit pilot/evidence record remains bounded at lower scopes and cautions against starting with a large Series. Therefore the highest-leverage uncertainty is not "what Series architecture should be invented?" but "what, if anything, breaks or creates meaningful friction when the existing Series layer is used in a bounded cross-book author workflow?" A small empirical product probe can answer that question without presupposing an implementation.

State currency and provenance: all target claims above were verified by GitHub connector reads against the experiment's exact frozen target commit `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`; the Git commit and tree were resolved before the cited file reads. This establishes the state of the frozen experiment snapshot, not the current default branch outside that snapshot. Statements about what the documentation says are documented claims; the recommendation that Series-oriented author evidence is the next consequential probe is an inference from those verified documents, not a repository fact or owner-ratified product decision.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: docs/narrative-architecture.md
    lines: L26
    quote: "| Series | Cross-book continuity and progression | Optional | Book arcs, recurring relationships, setup/payoff |"
    supports_claim: "Series is explicitly the cross-book continuity and progression scope."
  - file: src/auteur/series/models.py
    lines: L222
    quote: "    book_plans: list[BookPlan] = Field(min_length=1)"
    supports_claim: "SeriesIdentity is a first-class model that contains one or more book plans."
  - file: docs/adr/012-series-engine-v1.md
    lines: L16
    quote: "Series Engine V1 adds `SeriesIdentity` as a canonical Narrative Engine artifact"
    supports_claim: "The Series layer is canonical architecture, not merely a proposed feature."
  - file: docs/architecture-roadmap.md
    lines: L211
    quote: "The architecture suite is mostly complete for V1, but product completeness is"
    supports_claim: "The roadmap frames the remaining uncertainty as product completeness rather than missing foundational architecture."
  - file: docs/capability-coverage.md
    lines: L111
    quote: "book, or one complete arc. Do not begin with a large series."
    supports_claim: "The repository's controlled-pilot policy intentionally keeps the next empirical step bounded."
  - file: docs/capability-coverage.md
    lines: L172
    quote: "5. The next implementation slice is selected from evidence rather than theory."
    supports_claim: "The repository explicitly requires evidence, not theory, to choose the next implementation slice."
  - file: docs/capability-coverage.md
    lines: L203
    quote: "This bounded Book Manuscript slice is now proven on the canonical two-Chapter"
    supports_claim: "The explicit product-evidence path has already reached a bounded Book workflow."
```

## 9. Why this boundary matters

If Auteur chooses another major implementation from architectural intuition alone, it risks deepening a system whose foundational structure is already ahead of its demonstrated author workflow. That can create sophisticated machinery around a problem that real authors do not experience as the limiting factor.

Conversely, jumping directly to a large-Series dogfood would violate the repository's own bounded-pilot discipline and make attribution difficult. A small cross-book probe creates a cleaner decision boundary: either a reproducible Series-level friction point appears and warrants a focused implementation, or the evidence says the existing Series layer is adequate enough that another product boundary deserves attention.

## 10. Candidate next steps

1. **Bounded Series pilot:** create a two-Book mini-series or similarly small complete cross-book arc using the existing Series and Book surfaces; include at least one recurring character/relationship arc, one setup/payoff or dependency edge, and one revision after review.
2. **Series-first vs Book-first comparison:** perform the same bounded planning problem once from SeriesIdentity downward and once by starting from Book intent, then compare author effort, duplication, ambiguity, and continuity handling.
3. **Existing-surface walkthrough:** exercise Series compile, graph, validate/review, and bible outputs on the bounded pilot and record where the author must leave the intended workflow, inspect raw structures, or manually reconcile information.
4. **Evidence-selected decision:** after the probe, write one reproducible highest-impact friction example and choose at most one implementation slice from it; if no material Series-specific friction emerges, record that result instead of forcing a change.

## 11. Recommended next step

Run a **bounded two-Book Series-oriented product-validation pass using the existing implementation, with no repository changes during the probe**. Start from one canonical SeriesIdentity, derive the two Book plans, carry at least one cross-book dependency/setup-payoff through review, and perform one revision. Record author-facing friction and whether the workflow preserves long-horizon intent without unnecessary duplication.

This recommendation depends on current-state claims that were verified only for the frozen experiment snapshot `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`: `src/auteur/series/models.py:213-230` verifies the relevant Series representation exists there, and `docs/architecture-roadmap.md:201-216` plus `docs/capability-coverage.md:108-112` verify that this snapshot directs subsequent work toward bounded author-friction evidence rather than another foundational architecture.

## 12. Recommended workflow

**Workflow:** `product-discovery-sprint`

**Execution mode:** `plan_only`

Use the workflow to plan the bounded empirical author-use probe and its decision criteria. Do not implement a Series change before the probe identifies a reproducible product problem.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: experiments/campaigns/EXP-0006-empirical-skill-qualification-diagnostic/scientific-questions.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "docs/narrative-architecture.md (line L26): Series owns cross-book continuity and progression"
  - "src/auteur/series/models.py (lines L213-L230): SeriesIdentity contains book plans and cross-book arc/dependency structures"
  - "docs/adr/012-series-engine-v1.md (lines L16-L38): SeriesIdentity is canonical while compiled analysis artifacts are derivative"
  - "docs/architecture-roadmap.md (lines L201-L216): remaining work is author workflow/capability refinement selected from friction"
  - "docs/capability-coverage.md (lines L108-L112): controlled pilot must remain bounded and not begin with a large series"
  - "docs/capability-coverage.md (lines L170-L172): next implementation slice must be selected from evidence rather than theory"
  - "docs/capability-coverage.md (lines L194-L214): bounded Book Manuscript workflow is documented as proven"
recommended_workflow_id: product-discovery-sprint
recommended_execution_mode: plan_only
weakest_boundary: "The first-class Series/long-horizon product surface lacks equally strong author-facing decision evidence for selecting the next major implementation."
weakness_type: Other
weakness_type_explanation: "This is a product-validation and decision-evidence boundary; the registered weakness taxonomy is repository/code-centric, and labeling it Zero Validation would falsely imply missing automated checks in Series core logic."
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-09-05T23:34:00Z"
immutable: true
representation_sufficiency:
  status: sufficient
  rationale: >-
    The frozen repository evidence is sufficient to select the next investigative probe: validate the existing Series workflow with bounded cross-book author use before selecting another major implementation.
  needed_representation: null
```

## 14. Ready-to-copy prompt

Plan a `product-discovery-sprint` for the frozen Auteur snapshot `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`. Do not implement changes. Design a bounded two-Book Series-oriented author-use probe that exercises the existing SeriesIdentity and Book workflow, includes at least one cross-book arc or recurring relationship, one setup/payoff or dependency edge, and one revision after review. Include a Series-first versus Book-first comparison if it can be done without expanding the probe excessively. Define what author friction to record, what would count as a reproducible missing capability, and how the evidence will select at most one next implementation slice or support a no-change result. Respect the repository's instruction not to begin with a large series.