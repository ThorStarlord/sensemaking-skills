# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-26T13:38:16.274169Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is a narrative engineering system — a "literary compiler" for long-form fiction. It implements a complete 7-layer narrative hierarchy (Universe → Series → Book/Story Identity → Blueprint → Outline → Draft → Editing) to prevent lore drift and character state inconsistencies across chapters. The system provides story identity recommendation from raw premises, deterministic structure diagnostics, genre-specific interactive pipelines, chapter drafting with multi-critic validation, project planning with scenario modeling, and state management across all narrative layers.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

Version 0.35.0 with comprehensive subsystems: portfolio management, counterfactual simulation, impact planning, decision workspace, author review sessions, and structural revision lifecycle. The codebase contains 3634 test functions across 227 test files covering structure, diagnostics, three genre pipelines (netorare, mystery, gentlefemdom), decision/impact/review workflows, and end-to-end semantic layer integration. The 9-layer diagnostic model is implemented across Target Experience, Constraints, Scope, Structural Forces, Threads, Theme, Carriers, Representation, Modulation. CLI provides 50+ commands including state check, structure diagnose, portfolio create, simulate compare, and review accept. Genre pipelines with deterministic templates and validation rules exist for all three production genres. State management via StoryBibleModel (Pydantic) tracks character/location/item/faction/event state. Genre pipeline infrastructure (registry, session management, HTTP server, browser UI) is genre-neutral and proven to work across three distinct genres. Story identity recommendation and blueprint seeding from raw premises are supported.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

Comprehensive test suite with 3634 tests across 227 files providing strong regression safety. Multiple completed subsystems demonstrate mature architecture: v0.10-v0.35 releases show planning, simulation, portfolio, decision workspace, and review features. Pydantic schema discipline applied consistently across blueprint, diagnostics, and state models. Nine-layer diagnostic system reflects documented narrative architecture in CONTEXT.md and CLAUDE.md. Genre-neutral interactive pipeline runtime (session/server/UI) successfully generalizes across three distinct genres (netorare, mystery, gentlefemdom) without special-casing in shared infrastructure — a validated pattern per CLAUDE.md. Revision service implements authority-gated lifecycle with transactional safety. Working genre_pipeline.registry module demonstrates registry-based dispatch pattern is achievable and effective. Existing test infrastructure provides confidence in refactoring.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

Acceptance subsystem integration (review/service.py L426): The ReviewService.accept() method records acceptance success but contains a TODO comment: "Call the actual acceptance subsystem". Acceptance is currently mocked; integration with true acceptance API is deferred. Reconciliation proposal loading (decision/adapters/reconciliation_adapter.py L49): The load_proposals() method is stubbed with TODO: "wire real proposal loading in Task 2". It returns empty list; real proposal hydration from ReconciliationStore is deferred. Genre-specific outline generation defaults: GenreDefaults class in outline_builder.py hard-codes chapter goals, conflicts, themes, and sequence counts for all three genres instead of loading from genre packages via registry. This violates stated "no special cases in infrastructure" principle and creates extension friction for adding genre 4.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

Refactor outline generation to use genre_pipeline.registry: Move NETORARA_GOALS, MYSTERY_GOALS, GENTLEFEMDOM_GOALS from outline_builder.py to respective genre packages and dispatch through registry, eliminating hard-coded if/elif chains and enabling genre 4+ to be added without editing outline_builder or composition_rules. Implement acceptance subsystem integration: Wire ReviewService.accept() to delegate to confirmed acceptance API instead of mocking success, unblocking review→acceptance→impact pipeline. Complete reconciliation proposal loading: Implement ReconciliationAdapter.load_proposals() to hydrate from ReconciliationStore. Add regression test for genre-specialization-free infrastructure to prevent re-introduction of hard-coded genre checks.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Vocabulary Drift: Genre-specific infrastructure leakage in outline_builder.py**

The narrative_orchestration module (particularly outline_builder.py and composition_rules.py) directly special-cases all three genres using hard-coded `if genre == Genre.X: ... elif genre == Genre.Y: ...` conditionals. This violates CLAUDE.md's explicit architecture principle (line 218-223): "No Special Cases in Infrastructure. If you find yourself adding `if genre == 'new_genre'` to shared code, stop. The pattern needs rework."

The GenreDefaults class contains 8+ genre-specific branches across methods like get_chapter_goals(), get_chapter_conflicts(), get_sequence_count(), get_character_arc_themes(), and get_story_arc_category(). Hard-coded chapter goals, conflicts, and themes span 137+ lines of genre-specific data embedded in outline-generation logic instead of in genre-specific packages.

However, genre_pipeline/registry.py (lines 97-166) implements a working registry pattern that successfully abstracts all three genres' templates, validation rules, and identity profiles through factory functions with zero infrastructure modifications. This pattern proves the desired approach is achievable.

The consequence: Adding genre 4 requires editing outline_builder.py and composition_rules.py to add new conditionals, violating DRY. All three current genres run on identical genre_pipeline infrastructure with only a registry entry; outline generation is an exception that breaks the extensibility guarantee.

This is the most critical architectural gap because it directly contradicts stated design principles and creates maintenance burden for future genre additions.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
```yaml
evidence_excerpts:
  - file: src/auteur/narrative_orchestration/orchestrator/outline_builder.py
    lines: L137-L175
    quote: "@staticmethod\ndef get_chapter_goals(genre: Genre) -> List[str]:\n    \"\"\"Get genre-specific chapter goals.\"\"\"\n    if genre == Genre.NETORARE:\n        return GenreDefaults.NETORARA_GOALS\n    elif genre == Genre.MYSTERY:\n        return GenreDefaults.MYSTERY_GOALS\n    elif genre == Genre.GENTLEFEMDOM:\n        return GenreDefaults.GENTLEFEMDOM_GOALS\n    else:\n        return [f\"Advance plot objective {i}\" for i in range(1, 13)]\n\n@staticmethod\ndef get_sequence_count(genre: Genre) -> int:\n    \"\"\"Get recommended sequence count for genre.\"\"\"\n    if genre == Genre.NETORARE:\n        return 3\n    elif genre == Genre.MYSTERY:\n        return 4\n    elif genre == Genre.GENTLEFEMDOM:\n        return 3\n    else:\n        return 3"
    supports_claim: "GenreDefaults class implements genre dispatch with hard-coded if/elif chains instead of using genre_pipeline registry pattern, directly violating CLAUDE.md architecture principle."
  - file: src/auteur/genre_pipeline/registry.py
    lines: L183-L189
    quote: "def get_genre_pipeline(genre: Genre | str) -> GenrePipelineSpec:\n    try:\n        genre_enum = genre if isinstance(genre, Genre) else Genre(genre)\n        return _specs()[genre_enum]\n    except (KeyError, ValueError) as exc:\n        raise ValueError(f\"No built-in interactive pipeline for genre: {genre}\") from exc"
    supports_claim: "Working registry pattern exists for genre dispatch but is not used by outline_builder, showing infrastructure for extensibility exists but is underutilized."
  - file: src/auteur/CLAUDE.md
    lines: L218-223
    quote: "No Special Cases in Infrastructure\n\nIf you find yourself adding `if genre == \"new_genre\"` to shared code, stop. The pattern needs rework:\n- Either the infrastructure should handle it generically\n- Or the new genre needs its own implementation of that component"
    supports_claim: "Architecture specification explicitly forbids genre-specific conditionals in infrastructure, and genre_pipeline registry proves the pattern can be implemented generically."
  - file: src/auteur/narrative_orchestration/orchestrator/outline_builder.py
    lines: L435-436
    quote: "# Get genre-specific goals and conflicts\ngoals = GenreDefaults.get_chapter_goals(self.genre)"
    supports_claim: "Outline generation method calls hard-coded genre dispatch instead of registry lookup."
  - file: src/auteur/decision/adapters/reconciliation_adapter.py
    lines: L49
    quote: "return []  # TODO: wire real proposal loading in Task 2"
    supports_claim: "Incomplete feature: reconciliation adapter does not load proposals, indicating workflow integration gaps."
  - file: src/auteur/review/service.py
    lines: L426
    quote: "# TODO: Call the actual acceptance subsystem"
    supports_claim: "Incomplete feature: review service does not call acceptance subsystem, indicating workflow gaps."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

The genre-specialization leakage directly impacts code maintainability and extensibility. The stated architecture principle is clear: genres should be added by registering them, not by editing shared infrastructure. When a fourth genre is added, developers unfamiliar with the outline_builder will waste time searching for where to add new conditionals instead of following the proven registry pattern. Each new genre adds complexity to outline_builder instead of being self-contained in its package. This violates the stated goal (from CLAUDE.md line 60): "If you can implement the same architecture for three different genres (netorare, mystery, gentle femdom) with zero infrastructure changes, the pattern is production-ready for additional genres." The pattern IS production-ready in genre_pipeline; outline_builder is an exception that breaks this guarantee. The secondary issues (acceptance subsystem, reconciliation proposals) are incomplete feature integrations; this is an architectural principle violation.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. **Refactor outline generation to use registry (Phase 1):** Create GenreOutlineDefaults interface in genre_pipeline; move NETORARA_GOALS, MYSTERY_GOALS, GENTLEFEMDOM_GOALS to respective genre packages; update GenreDefaults to dispatch through registry instead of hard-coded if/elif.

2. **Unify remaining genre-dispatch patterns (Phase 2):** Audit and centralize composition_rules.py genre handling through registry; add regression tests to prevent hard-coded genre checks.

3. **Complete TODO-marked features (Phase 3):** Implement acceptance subsystem integration in ReviewService.accept(); complete ReconciliationAdapter.load_proposals().

4. **Validate with genre 4 addition (Phase 4):** Attempt to add a fourth genre (e.g., horror) using only registry pattern + genre package, no edits to outline_builder or composition_rules, confirming extensibility.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Execute architecture-implementation-workflow Phase 1: Refactor outline_builder.py to load genre defaults from genre packages via registry. This is the highest-leverage fix because it removes the architectural exception and proves the extensibility guarantee for genre 4+. The fix is localized to outline_builder.py's GenreDefaults class and requires moving genre-specific data to genre packages (netorare/, mystery/, gentlefemdom/). Secondary priority: complete acceptance subsystem integration (ReviewService.accept()) to unblock the review→acceptance→impact pipeline.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: False
escalation_recommended: True
evidence: []  # model fills: list of "path/to/file (lines Lx-Ly): citation"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: phased
weakest_boundary: {'type': 'Vocabulary Drift', 'affected_modules': ['narrative_orchestration.orchestrator.outline_builder', 'narrative_orchestration.schema.composition_rules'], 'severity': 'HIGH', 'impact': 'Adding new genres requires edits to multiple hard-coded conditionals instead of following proven registry pattern'}
required_inputs:
  - repository_state
  - analysis_depth
created_at: "2026-07-26T13:38:16.274169Z"
immutable: true
```
