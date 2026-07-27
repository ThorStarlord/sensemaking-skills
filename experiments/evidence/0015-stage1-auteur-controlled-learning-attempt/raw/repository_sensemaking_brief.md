# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-27T19:42:50.875356Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is a narrative engineering system for long-form fiction: a layered pipeline (Universe -> Series -> Book -> Story Identity -> chapter drafting) that turns authored intent into structurally-validated story artifacts. It combines Pydantic-modeled domain contracts (`StoryBlueprint`, `StoryIdentity`, `SeriesIdentity`, `UniverseIdentity`), deterministic diagnostic validators for each layer, three built-in interactive "genre pipelines" (netorare, mystery, gentlefemdom), and an orchestration/CLI layer that compiles, audits, and drafts narrative content while trying to prevent lore drift and continuity breaks across a multi-book series.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

- `src/auteur/` is organized by domain package: `genre_pipeline/` (interactive browser-based genre setup), `universe/`, `series/`, `book/`, `character/`, `structure/`, `cartographer*.py` (outline compilation), `commitment/`, `convergence/`, `decision/`, `editing/`, `critic/`, `reasoning/`.
- `CONTEXT.md` (last updated 2026-07-11) is the canonical architecture doc and documents "ADR 013" Universe-to-Series constraint propagation as an operational feature, including six named continuity validators and a three-tier constraint classification (structured / natural-language / LLM-assisted).
- `docs/adr/` holds 18 ADR files (001-017 plus a separately-named `ADR-013-Universe-to-Series-Propagation.md`) tracking major decisions including bible_audit placement (003), the Series engine (012), and Universe-to-Series propagation (013).
- `tests/` is large (100+ files across `auteur/`, `gentlefemdom/`, `mystery/`, `netorare/`, `impact/`, `convergence/`, `qualification/`, `phase1`-`phase6`) and CI (`.github/workflows/validation.yml`) runs the full pytest suite across Python 3.11/3.12/3.13 plus a separate wheel-build-and-smoke-test job.
- `src/auteur/series/` implements six "Group 3" continuity validators (Thematic, Character, Relationship, Lore, Chronology, Setup/Payoff) in `continuity_validators.py`, plus a separate Universe-to-Series validator (`universe_integration.py`) covering four `StructuredConstraint` types (`genre_rule`, `thematic_invariant`, `character_state`, `relationship_rule`).

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

- All six ADR-013 "Group 3" continuity validators (Thematic/Character/Relationship/Lore/Chronology/Setup-Payoff) described in `CONTEXT.md` are genuinely implemented in `src/auteur/series/continuity_validators.py` and wired into `handle_series_diagnose` (`src/auteur/series/handlers.py:107-132`) -- exactly the kind of doc-vs-code gap that usually shows up in architecture_fog repos, and here it does not.
- The four `StructuredConstraint` types defined in ADR-013 decision #5 (`genre_rule`, `thematic_invariant`, `character_state`, `relationship_rule`) are all implemented with real per-book/per-character diagnostic logic in `universe_integration.py`, not stubs.
- CI is a real gate: `.github/workflows/validation.yml` runs pytest across Python 3.11/3.12/3.13 plus a separate job that builds the wheel, installs it into a fresh venv, and smoke-tests `auteur --help` and `auteur ontology list`.
- Pydantic modeling discipline is consistent across layers -- `UniverseIdentity`, `SeriesIdentity`, `StructuredConstraint`, and `CrossStoryConstraint` all use `pydantic.BaseModel` with explicit `Field` constraints rather than plain dataclasses or dicts.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

- Series-level enforcement of a Universe's `cross_story_constraints` (ADR-013's "Natural-Language Principles" tier) and of `forbidden_elements`/`required_elements` is absent from the actual diagnose path -- see the weakest boundary below.
- Book-level Universe/Series constraint inheritance ("Book 1 inherits Series + Universe constraints", per ADR-013's own hierarchy diagram) has no code at all in `src/auteur/book/` referencing universe or series constraints.
- ADR-013 decision #3's "strengthen but not weaken" corollary (worked example: Universe says "Magic is possible", Series may not say "Magic is impossible") has no corresponding contradiction-detection code or test anywhere in `src/` or `tests/`.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Route `universe.cross_story_constraints` (and `forbidden_elements`/`required_elements`) through `compile_universe_constraints()` into `UniverseToSeriesValidator.validate()` as new ADVISORY-severity checks, matching the ADR-013 "Natural-Language Principles -> WARNING diagnostics" contract.
- Extend `src/auteur/book/builder.py` (or a new book-level validator) to accept a Series' resolved Universe constraints so Book compilation actually inherits constraints per the ADR-013 hierarchy diagram.
- Add a "strengthen not weaken" contradiction check (e.g. an explicit `contradicts` relationship on `CrossStoryConstraint`, or a simple heuristic) with a regression test built from the ADR's own magic-possible/impossible example.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness type:** Ghost Features

The weakest boundary is the gap between what `CONTEXT.md` and `docs/adr/ADR-013-Universe-to-Series-Propagation.md` document as the Universe-to-Series constraint-propagation contract, and what the Series diagnostic pipeline actually executes. ADR-013 (`docs/adr/ADR-013-Universe-to-Series-Propagation.md:31-51`) classifies Universe constraints into three tiers: (1) Structured Constraints -> `ERROR` diagnostics, (2) Natural-Language Principles (the free-text `cross_story_constraints` field, plus `forbidden_elements`/`required_elements`) -> `WARNING` diagnostics, (3) LLM-assisted interpretation -> `INFO`. `CONTEXT.md`'s "Series Continuity & Universe Propagation (ADR 013)" section repeats the same three-tier contract almost verbatim. Only tier 1 is real: `UniverseToSeriesValidator.validate()` (`src/auteur/series/universe_integration.py:19-35`) dispatches on exactly the four `ConstraintType` values that back `structured_constraints`, and the single production call site, `_collect_universe_diagnostics()` in `src/auteur/series/handlers.py:159`, passes `universe.structured_constraints` and nothing else. `cross_story_constraints`, `forbidden_elements`, and `required_elements` are read by `compile_universe_constraints()` (`src/auteur/universe/compiler.py:15-29`), whose own docstring says the output is a form "Series/Book validators can quickly check against" -- but `compile_universe_constraints` has exactly one caller in the entire repository, and that caller is its own unit test (`tests/test_universe.py:203-229`), not any Series or Book handler. The "strengthen but not weaken" corollary in ADR-013 decision #3 likewise has no implementing code or test. Series-level advisory enforcement is therefore a ghost feature: modeled, documented, unit-tested in isolation, and never invoked from the path a real author would exercise (`auteur series diagnose`).

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

`CONTEXT.md`'s "Series Continuity & Universe Propagation (ADR 013)" section and `docs/adr/ADR-013-Universe-to-Series-Propagation.md:31-51` both describe three constraint tiers, the second of which ("Natural-Language Principles") is documented to be advisory and non-blocking, generating `WARNING` diagnostics when a Series violates an advisory Universe principle. `src/auteur/universe/models.py:65-67` defines `forbidden_elements`, `required_elements`, and `cross_story_constraints` as first-class, populated `UniverseIdentity` fields -- not aspirational placeholders. `src/auteur/universe/compiler.py:15-29`'s `compile_universe_constraints()` flattens exactly those three fields into a `CompiledUniverseConstraints` object whose docstring (`compiler.py:18-19`) states it exists so "Series/Book validators can quickly check against" it. The only place a Series is actually checked against a Universe in production code is `_collect_universe_diagnostics()` in `src/auteur/series/handlers.py:135-160`, whose call at line 159 is `validate_series_against_universe(series, universe, universe.structured_constraints)` -- it forwards `structured_constraints` alone. `UniverseToSeriesValidator.validate()` (`src/auteur/series/universe_integration.py:19-35`) confirms this: its dispatch loop only branches on `ConstraintType.GENRE_RULE`, `THEMATIC_INVARIANT`, `CHARACTER_STATE`, and `RELATIONSHIP_RULE` -- there is no branch, helper method, or fallback that reads `cross_story_constraints`, `forbidden_elements`, or `required_elements`. A repo-wide search for `compile_universe_constraints` and `CompiledUniverseConstraints` turns up exactly one caller outside their own definition file: `tests/test_universe.py:203-229`, which calls the compiler directly and asserts on its output in isolation -- no handler, CLI command, or `book/` module calls it. `src/auteur/book/` was also searched directly for `forbidden_elements`, `required_elements`, `cross_story_constraints`, and `universe`; none of those terms appear anywhere in that package, confirming Book-level inheritance (promised by ADR-013's own hierarchy diagram) has no implementation either.

Logic trace: CONTEXT.md and ADR-013 both promise that "Natural-Language Principles" (the free-text `cross_story_constraints`, plus `forbidden_elements`/`required_elements`) produce `WARNING` diagnostics when a Series is checked against its Universe. Reading the one real call site (`handlers.py:159`) shows only `structured_constraints` is forwarded into validation. Reading the validator itself (`universe_integration.py:27-35`) shows its dispatch table has no case for the natural-language fields at all, so even if they were forwarded, nothing downstream would consume them. Reading the one function that does transform those fields into a check-ready shape (`compiler.py:15-29`) and then searching the repository for its callers shows its only caller is its own unit test. Chaining these three reads together shows the documented advisory-tier enforcement is unreachable from any real author-facing command (`auteur series diagnose`), which is the definition of a ghost feature rather than, say, a bug confined to one branch. I deliberately searched for the rebuttal case too -- a second call site, a book-level validator, or a test exercising `handle_series_diagnose` end-to-end with a violated `cross_story_constraints` rule -- and found none of the three; the one existing test that does pass a real Universe with `cross_story_constraints` into `validate_series_against_universe` (`tests/test_series_universe_integration.py::test_validate_series_against_universe_constraints`) calls it as `validate_series_against_universe(series, universe)` with the `constraints` argument omitted, which defaults to `None` and short-circuits the function to `return []` before any real check runs (`src/auteur/series/universe_integration.py:217-218`), so even that test provides no evidence of enforcement -- if anything it is further evidence of the gap, since it is the closest thing to a positive test and still does not exercise the advisory path. Per the evidence-authority ordering, this conclusion rests on executable code (the dispatch table, the single call site, and the caller search) rather than on CONTEXT.md's or the ADR's own claims, which are the documentation being checked, not the evidence checking it.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
evidence_excerpts:
- file: docs/adr/ADR-013-Universe-to-Series-Propagation.md
  lines: L40-L43
  quote: "2. **Natural-Language Principles** (advisory, non-blocking)\n   - Free-text guidance (e.g., \"stories should explore intimacy within power dynamics\")\n   - Thematic directions without computational enforcement\n   - Narrative values that inform but do not mechanically block"
  supports_claim: ADR-013 documents an advisory 'Natural-Language Principles' tier that CONTEXT.md says must generate WARNING diagnostics during Universe-to-Series validation.
- file: src/auteur/universe/models.py
  lines: L65-L67
  quote: "    forbidden_elements: list[str] = Field(default_factory=list)\n    required_elements: list[str] = Field(default_factory=list)\n    cross_story_constraints: list[CrossStoryConstraint] = Field(default_factory=list)"
  supports_claim: Confirms forbidden_elements, required_elements, and cross_story_constraints are real, populated UniverseIdentity fields, not merely planned, making their absence from Series validation a genuine wiring gap rather than a missing data model.
- file: src/auteur/universe/compiler.py
  lines: L18-L19
  quote: "    This creates a flat list of constraints that Series/Book validators can\n    quickly check against without needing the full UniverseIdentity structure."
  supports_claim: compile_universe_constraints()'s own docstring claims its output is meant to be consumed by Series/Book validators, establishing intended, documented behavior.
- file: src/auteur/series/handlers.py
  lines: L159
  quote: "        diagnostics = validate_series_against_universe(series, universe, universe.structured_constraints)"
  supports_claim: The only production call site forwards structured_constraints alone, never cross_story_constraints, forbidden_elements, or required_elements, and never calls compile_universe_constraints.
- file: src/auteur/series/universe_integration.py
  lines: L27-L35
  quote: "        for constraint in constraints:\n            if constraint.type == ConstraintType.GENRE_RULE:\n                diagnostics.extend(self._validate_genre_constraint(series, constraint))\n            elif constraint.type == ConstraintType.THEMATIC_INVARIANT:\n                diagnostics.extend(self._validate_thematic_constraint(series, constraint))\n            elif constraint.type == ConstraintType.CHARACTER_STATE:\n                diagnostics.extend(self._validate_character_constraint(series, constraint))\n            elif constraint.type == ConstraintType.RELATIONSHIP_RULE:\n                diagnostics.extend(self._validate_relationship_constraint(series, constraint))"
  supports_claim: The validator's entire dispatch table only recognizes the four StructuredConstraint types; there is no branch for advisory/natural-language constraints despite the method's own docstring promising 'Natural-language principles (ADVISORY) produce WARNING diagnostics.'
- file: tests/test_universe.py
  lines: L227
  quote: "    compiled = compile_universe_constraints(universe)"
  supports_claim: This line, inside test_compile_universe_constraints, is the only invocation of compile_universe_constraints found anywhere in the repository outside its own definition, confirming no Series/Book handler calls it.
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

If advisory Universe principles and forbidden/required elements are silently unenforced, an author who defines a Universe rule like "no modern technology" or a `forbidden_elements` list can write a Series (or eventually a Book) that violates it and receive zero diagnostic feedback -- the exact "silent drift" failure mode the layered Universe -> Series -> Book architecture exists to prevent. Because `compile_universe_constraints` already exists and is unit-tested, a future contributor skimming the codebase (or `CONTEXT.md`) will reasonably believe advisory enforcement is live, and may build new features on top of that false assumption (e.g. a Book-level validator that expects `CompiledUniverseConstraints` to already be flowing through diagnostics), discovering the gap only when an author reports lore that should have been flagged but wasn't. This is the same failure shape `CONTEXT.md`'s own architecture document is meant to prevent for characters and locations (see the sibling `bible_audit.py` teleportation checks), just recurring one layer higher in the Universe/Series hierarchy.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Wire `compile_universe_constraints()`'s output (or the raw `cross_story_constraints`/`forbidden_elements`/`required_elements` fields) into `_collect_universe_diagnostics()` in `handlers.py`, generating `WARNING`-severity `ValidationDiagnostic`s per ADR-013 tier 2.
2. Add a regression test that constructs a Series violating a `forbidden_elements` entry or a `cross_story_constraints` rule and asserts `handle_series_diagnose` returns a corresponding `WARNING` diagnostic, closing the gap the current isolated compiler test leaves open.
3. Implement the ADR-013 decision #3 "strengthen but not weaken" contradiction check, using the ADR's own magic-possible/impossible example as the first regression test.
4. Extend `src/auteur/book/` to accept and check resolved Series+Universe constraints at Book compilation time, per the ADR-013 inheritance diagram.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Implement candidate next step 1 first: route the three advisory Universe fields (`cross_story_constraints`, `forbidden_elements`, `required_elements`) through `compile_universe_constraints()` into `_collect_universe_diagnostics()` so `auteur series diagnose` actually emits the `WARNING` diagnostics `CONTEXT.md` and ADR-013 already document. This is the smallest change that closes the ghost-feature gap (the compiler function and data model already exist), and it directly unblocks next step 2 -- a real enforcement regression test, which cannot be written honestly until the wiring exists.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

```
We need to address the weakest boundary identified in the repository sensemaking brief: advisory Universe constraints are unenforced. ADR-013 (docs/adr/ADR-013-Universe-to-Series-Propagation.md) and CONTEXT.md document that a Series's `cross_story_constraints`, `forbidden_elements`, and `required_elements` should produce WARNING diagnostics during Universe-to-Series validation, but `_collect_universe_diagnostics` (src/auteur/series/handlers.py:159) only forwards `structured_constraints` into `UniverseToSeriesValidator`, and the existing `compile_universe_constraints()` (src/auteur/universe/compiler.py) that flattens the advisory fields has no caller besides its own unit test (tests/test_universe.py). Wire the advisory fields into the Series diagnose path as WARNING diagnostics, add a regression test proving a real violation is now flagged by `handle_series_diagnose`, and treat ADR-013's "strengthen not weaken" contradiction check as a stretch goal. Ensure all existing tests remain green.
```

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: False
escalation_recommended: False
evidence:
- "docs/adr/ADR-013-Universe-to-Series-Propagation.md (lines L40-L43): documents the advisory 'Natural-Language Principles' tier that should generate WARNING diagnostics."
- "src/auteur/universe/models.py (lines L65-L67): forbidden_elements, required_elements, and cross_story_constraints are real, populated UniverseIdentity fields."
- "src/auteur/universe/compiler.py (lines L15-L29): compile_universe_constraints() flattens those fields for 'Series/Book validators' per its own docstring."
- "src/auteur/series/handlers.py (line L159): the only production call to validate_series_against_universe passes structured_constraints alone."
- "src/auteur/series/universe_integration.py (lines L27-L35): the validator's dispatch loop has no case for cross_story_constraints, forbidden_elements, or required_elements."
- "tests/test_universe.py (lines L203-L227): the sole caller of compile_universe_constraints in the repository is this isolated unit test of the compiler."
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: cross_story_constraint_enforcement_gap
weakness_type: Ghost Features
weakness_type_explanation: None
required_inputs:
- "user_intent"
- "repository_state"
created_at: "2026-07-27T19:42:50.875356Z"
immutable: true
```
