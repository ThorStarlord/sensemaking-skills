# Repository Sensemaking Brief

## 1. Repository goal

Auteur is now best understood as an author-authority-centered narrative engineering system for long-form fiction, not merely an LLM prose generator. Its canonical model separates semantic layers (Ontology → Identity → Structure → Realization → Expression) from narrative scope (Universe → Series → Book → Chapter → Scene), while deterministic code owns contracts, diagnostics, provenance, and workflow boundaries around optional generative work.

For the user's strategic question — what major development step should come next — the repository's own architecture makes an important distinction: the foundational architecture is mostly complete, while product completeness remains uneven across scopes. That shifts the next-step problem from “what architecture should we invent?” toward “which author-facing vertical has enough evidence to justify the next investment?”

## 2. Current shape

The Python package under `src/auteur/` contains mature single-story/Book machinery plus explicit `series/` and `universe/` packages. `docs/narrative-architecture.md` defines Universe, Series, Book, Chapter, and Scene as a scope axis. `src/auteur/series/models.py` makes Series first-class through `SeriesIdentity`, book plans, cross-book character/relationship/faction arcs, mysteries, dependency edges, and Universe linkage.

At the same time, the repository's product-completion documents remain evidence-driven. `docs/architecture-roadmap.md` says architecture is mostly complete but product completeness is uneven, and directs the project to choose the next implementation from real author friction. `docs/capability-coverage.md` defines a controlled pilot, a friction log, and the rule that the next implementation slice should be selected from evidence rather than theory.

## 3. Strong signals

- The semantic model is explicit and scalable: Series is a real cross-book scope rather than an overloaded Book concept (`docs/narrative-architecture.md:21-32`).
- The implementation backs that architecture with a concrete canonical Series contract: `SeriesIdentity` requires book plans and carries cross-book arcs/dependencies (`src/auteur/series/models.py:213-230`).
- The repository already knows how to resist architecture-for-architecture's-sake. Its roadmap states that remaining work is vertical author workflow/capability refinement, and that the next implementation should be selected from author friction (`docs/architecture-roadmap.md:201-216`).
- The product evidence doctrine is unusually strong: pilot completion explicitly requires a reproducible high-impact missing capability and evidence-based selection of the next implementation slice (`docs/capability-coverage.md:170-172`).

## 4. Missing pieces

The most consequential missing piece for the user's decision is **validated author-facing evidence at the newly important Series/long-horizon boundary**.

The exact snapshot has a first-class Series model and cross-book continuity machinery, but the repository's explicit pilot/evidence trail is still framed around a bounded short story, novella, five-to-ten-chapter book, or complete arc, and explicitly warns not to begin with a large series (`docs/capability-coverage.md:108-112`). Its evidence-selected path records single-Chapter evidence and a bounded two-Chapter Book fixture before naming Book workflow as the next candidate (`docs/capability-coverage.md:170-203`). That is useful implementation evidence, but it does not yet answer the strategic question created by the broader Series capability: which parts of the Series workflow materially help an author sustain a long project, which parts create friction, and which missing capability actually blocks the next step.

This is not a claim that Series code lacks automated tests. It is a claim about the **decision evidence needed to choose the next major product investment**. Under the authorized connector-native surface, local Probe Engine metrics (`verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn`) are unmeasured and are not inferred.

## 5. Improvement opportunities

1. Run a bounded Series-oriented author workflow that is large enough to exercise cross-book commitments but small enough to inspect closely (for example, 2–3 Book identities with one complete arc and explicit cross-book setup/payoff obligations).
2. Record friction using the repository's existing taxonomy: missing capability, poor author UX, wrong artifact design, unclear terminology, excessive required data, weak critic, unnecessary validation, or transformation gap.
3. Compare the author effort and decision quality of Series-first planning against a simpler Book-first path so the Series layer earns its complexity empirically.
4. Reconcile top-level status/navigation docs after the pilot so “what Auteur is now” points to the same current product boundary as the canonical architecture.
5. Only after the pilot, choose one bounded implementation slice from the highest-impact reproducible friction rather than expanding the framework speculatively.

## 6. Weakest boundary

**Weakness type:** Other

The weakest boundary is **strategic product evidence for the Series/long-horizon author workflow**. The repository has crossed the architectural threshold into first-class Series modeling, but its own evidence-selection discipline has not yet produced an equally strong Series-level author-use result that can justify the next major investment. This is a product-validation/decision-evidence weakness, which does not fit the seven code/repository weakness labels cleanly; forcing it into `Zero Validation` would incorrectly imply the Series core lacks automated checks.

## 6.5. Problem classification (fog type)

`product_fog`. The uncertainty is not primarily “how should the modules be structured?” The canonical architecture and Series model already answer that well enough. The unresolved question is which author problem should drive the next major development step and what evidence would justify that choice.

## 7. Evidence

<!-- mode: investigative -->

State-currency backend: `github_connector_exact_sha_v1 @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90`. The exact target commit was resolved through GitHub before synthesis. Every repository-content claim below was read with that exact ref; no mutable default-branch content is used as snapshot evidence.

- `docs/narrative-architecture.md:21-32` — blob `4674fa7383d1870eea5bbf888cf349f7d2051a3d` — establishes Series as a cross-book scope alongside Universe/Book/Chapter/Scene.
- `src/auteur/series/models.py:213-230` — blob `753241598602fa7cb68d42144da3f990ae55b5c1` — shows that Series is implemented as a first-class contract with required Book plans and cross-book state.
- `docs/architecture-roadmap.md:201-216` — blob `6b680d765b0b30c1a5dd54891c37a5f9f07a32b2` — documents that foundational architecture is stable, product completeness is uneven, and author friction should select the next implementation.
- `docs/capability-coverage.md:108-112` and `docs/capability-coverage.md:170-203` — blob `d2e7978d825ce93c1545441efd3349d73820d02d` — defines the bounded pilot, says not to begin with a large series, requires evidence-based next-slice selection, and records the explicit evidence path through Chapter/Book rather than a demonstrated Series-level author workflow.

Local-only Probe Engine metrics are unmeasured on this connector-only surface. No values are approximated from prose or repository shape.

Logic trace: the canonical architecture proves that Series is now part of Auteur's intended product model; the code proves that this is not a ghost feature; the roadmap says another foundational architecture is not the priority and that the next implementation should come from author friction; the capability plan says next-slice selection must come from evidence while its explicit pilot boundary remains below a large Series. Therefore the highest-leverage uncertainty for the user's “next major development step” question is not another speculative feature or architecture layer. It is the missing empirical bridge between the first-class Series machinery and a reproducible author-facing Series/long-horizon friction signal.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: docs/narrative-architecture.md
    lines: L26
    quote: "| Series | Cross-book continuity and progression | Optional | Book arcs, recurring relationships, setup/payoff |"
    supports_claim: "The canonical architecture treats Series as an explicit cross-book scope."
  - file: src/auteur/series/models.py
    lines: L222
    quote: "    book_plans: list[BookPlan] = Field(min_length=1)"
    supports_claim: "SeriesIdentity has a concrete required Book-plan contract rather than being documentation-only."
  - file: docs/architecture-roadmap.md
    lines: L211
    quote: "The architecture suite is mostly complete for V1, but product completeness is"
    supports_claim: "The repository itself distinguishes architectural maturity from uneven product completeness."
  - file: docs/capability-coverage.md
    lines: L111
    quote: "book, or one complete arc. Do not begin with a large series."
    supports_claim: "The explicit controlled pilot boundary deliberately stops short of a large Series."
  - file: docs/capability-coverage.md
    lines: L172
    quote: "5. The next implementation slice is selected from evidence rather than theory."
    supports_claim: "The repository requires evidence, not architectural speculation, to select the next implementation."
```

## 9. Why this boundary matters

Auteur's architecture is already broad enough to support substantial continued implementation. That is exactly why this boundary matters: without author-facing evidence, almost any additional Series feature can be made to look locally reasonable. The project risks returning to architecture-first development and accumulating sophisticated contracts whose marginal author value is unknown.

A bounded Series pilot turns that open-ended option space into a falsifiable decision. It can show whether the actual bottleneck is cross-book direction capture, continuity review, setup/payoff visibility, progressive disclosure, Series-to-Book propagation, revision impact, or simply too much required structure. That evidence is more decision-changing than implementing the next plausible subsystem by inspection alone.

## 10. Candidate next steps

1. Define a bounded Series pilot fixture/use case: 2–3 Book identities, one cross-book arc, at least one setup/payoff dependency, and one revision that should propagate or trigger review.
2. Run the existing author-facing Series/Book workflow against it without adding features first; capture friction and decision points.
3. Compare Series-first and Book-first planning paths for author effort, clarity, and continuity leverage.
4. Rank observed friction by author impact and authority risk using the existing `docs/capability-coverage.md` friction taxonomy.
5. Select exactly one next implementation slice only after a reproducible high-impact gap emerges.

## 11. Recommended next step

Do **not** begin with another major implementation. First run one bounded Series/long-horizon product-validation pass that exercises the already-implemented Series contract and records author friction. The decision criterion should be: “Which reproducible obstacle most prevents an author from confidently planning or revising across Book boundaries?”

That recommendation is grounded in exact-SHA repository evidence: the architecture is already Series-aware, the Series contract is real, and the repository's own roadmap says remaining work should be chosen from author friction rather than another foundational design pass.

## 12. Recommended workflow

`product-discovery-sprint` — verified in the frozen `workflow-registry.yaml`. Use `plan_only`: the purpose here is to turn the product-fog question into a bounded opportunity/hypothesis and evidence plan, not to implement changes during this diagnostic run.

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
  - "docs/narrative-architecture.md (lines L21-L32, blob 4674fa7383d1870eea5bbf888cf349f7d2051a3d): Series is a canonical cross-book scope in the semantic model"
  - "src/auteur/series/models.py (lines L213-L230, blob 753241598602fa7cb68d42144da3f990ae55b5c1): SeriesIdentity is implemented with required Book plans and cross-book state"
  - "docs/architecture-roadmap.md (lines L201-L216, blob 6b680d765b0b30c1a5dd54891c37a5f9f07a32b2): foundations are stable and next implementation should come from author friction"
  - "docs/capability-coverage.md (lines L108-L112, L170-L203, blob d2e7978d825ce93c1545441efd3349d73820d02d): pilot/evidence doctrine is bounded below a large Series and requires evidence-based next-slice selection"
recommended_workflow_id: product-discovery-sprint
recommended_execution_mode: plan_only
weakest_boundary: "The first-class Series/long-horizon product surface lacks equally strong author-facing decision evidence for selecting the next major implementation."
weakness_type: Other
weakness_type_explanation: "This is a product-validation/decision-evidence boundary; the registered weakness taxonomy is repository/code-centric, and labeling it Zero Validation would falsely imply missing automated checks in Series core logic."
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-09-05T22:38:00Z"
immutable: true
representation_sufficiency:
  status: sufficient
  rationale: "Exact-SHA architecture, Series-contract, roadmap, and pilot evidence are sufficient to choose the next probe: validate the existing Series workflow with bounded author use before selecting another major implementation."
  needed_representation: null
```

## 14. Ready-to-copy prompt

Use the current Auteur Series/Universe and Book capabilities without implementing new features. Design one bounded 2–3 Book author workflow that exercises cross-book direction, one setup/payoff dependency, continuity review, and one revision. Record friction using the existing capability-coverage taxonomy, compare Series-first with Book-first planning where practical, and identify the single highest-impact reproducible obstacle to confident cross-Book planning or revision. Return the evidence and a recommendation for exactly one next implementation slice; do not implement it yet.