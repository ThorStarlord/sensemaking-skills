# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-26T11:47:55.054649Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is a narrative engineering toolkit for long-form fiction, designed to prevent narrative drift (lore inconsistencies, character teleportation, plot holes) through a unified 9-Layer Structural Engine. The toolkit provides opinionated story identity recommendations, deterministic structural validation, and optional downstream cartographer outlining and chapter drafting. The codebase is transitioning toward a "whole-story structure engine first, chapter drafting second" architecture where structural validation must pass before draft generation.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

- `src/auteur/structure/state.py` implements the unified multi-layer state manager and orchestrates CLI commands (`state check`, `state update`, `state prepare`, `state canon`, `state confirm`).
- `src/auteur/structure/analyzer.py` defines `run_all_diagnostics()` which runs structural analysis across layers 1-7 (TARGET_EXPERIENCE, CONSTRAINTS, SCOPE, STRUCTURAL_FORCES, THREADS, CARRIERS, REPRESENTATION).
- `src/auteur/structure/bible_audit.py` audits lore consistency through character location tracking and event log validation (Layer 6).
- `src/auteur/structure/outline_audit.py` validates scene representations against bible carrier state (Layer 7).
- `src/auteur/blueprint.py` defines the `StoryBlueprint` Pydantic model with cascading layer defaults and cross-field validation.
- `src/auteur/cli.py` exposes the `auteur structure`, `auteur identity`, and `auteur state` command families.
- `tests/` contains 265+ passing tests covering state commands, proposals, diagnostics, and character teleportation detection.
- `docs/` contains PRDs, architecture decision records (ADRs 001-017), and layer-to-command mapping in CONTEXT.md.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

- Layers 1-7 diagnostic infrastructure is complete and well-integrated: `analyze_structure()` covers structural coherence, `audit_bible_locations()` covers carrier state, `audit_outline_carriers()` covers scene representation.
- The Pydantic model discipline is strict: `StoryBlueprint`, `StructureDiagnostic`, `CharacterState`, `StoryBibleModel` all enforce schema validation at the model boundary.
- The state command lifecycle is documented in `CONTEXT.md` with ownership clarity: CLI commands own entry points, `StoryStateManager` owns transaction semantics, the analyzer owns diagnostic rules.
- Test suite is comprehensive and green: 265+ tests validate state commands, repair proposals, and character-location audit logic.
- Layer naming is consistent across docs and code: `DiagnosticLayer` enums (TARGET_EXPERIENCE, CONSTRAINTS, SCOPE, STRUCTURAL_FORCES, THREADS, CARRIERS, REPRESENTATION, MODULATION, THEME) align with CONTEXT.md and the 9-Layer framework.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

- Layers 8 (Modulation) and 9 (Resonance/Theme) have no active diagnostic rules in `run_all_diagnostics()`: the function only calls `analyze_structure()`, `audit_bible_locations()`, and `audit_outline_carriers()`, covering layers 1-7.
- The `_LAYER_ORDER` display list in `state_check()` includes layers 8 and 9 (MODULATION and THEME), but no diagnostics are ever generated for these layers, creating a ghost-feature illusion that these layers are validated.
- No CLI entry point or validator exists for pre-drafting structural gates: the state commands do not prevent chapter drafting from proceeding despite layer validation failures, preventing the "structure-first" goal.
- The proposal resolution system (`proposal_resolution.py`) exists but is not documented as part of the core architecture or reconciliation workflow, creating implicit dependencies.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Implement diagnostic rules for Layer 8 (Modulation): thematic consistency, emotional pacing, tension waveform coherence.
- Implement diagnostic rules for Layer 9 (Resonance): narrative closure, thematic resolution, character arc completion.
- Wire `state check` into the drafting pipeline as a blocking validation gate: require layer errors to be resolved before cartographer/bard execution.
- Extract and document the proposal lifecycle: diagnostics -> proposals -> resolution -> state application.
- Create a "layer status dashboard" in the CLI that shows which layers have errors, warnings, or are skipped.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

Layers 8 (Modulation) and 9 (Resonance) are declared in the code but not implemented in the diagnostic validator pipeline. The `state_check()` function displays these layers in its output header (`_LAYER_ORDER` lines 193-194), and the enum `DiagnosticLayer.MODULATION` and `DiagnosticLayer.THEME` exist in the code, but `run_all_diagnostics()` never generates diagnostics for these layers. The code acknowledges these layers as part of the 9-Layer Engine (visible in display logic, enum definitions, and documentation), but no validation rules consume or enforce them. This is a Ghost Features weakness: the interface declares the layers, but the implementation is absent.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

The evidence for this boundary weakness follows a clear diagnostic chain. The `state_check()` command in `src/auteur/structure/state.py:185-194` defines `_LAYER_ORDER` with all 9 layers including MODULATION (layer 8) and THEME (layer 9). However, when examining `src/auteur/structure/analyzer.py:21-63`, the `run_all_diagnostics()` function only calls `analyze_structure()` (layers 1-5), `audit_bible_locations()` (layer 6), and `audit_outline_carriers()` (layer 7). No calls to modulation or resonance validators exist in the implementation.

Logic trace: When `state_check()` is invoked (state.py:159), it calls `run_all_diagnostics()`, which returns diagnostics only for layers 1-7. The function then groups these by layer (line 198) and displays them using `_LAYER_ORDER` (line 204). If no layer 8 or 9 diagnostics exist, the loop simply skips them (line 206: `if not items: continue`). Therefore, users see a complete layer listing in the command output but receive no validation for the two highest layers, creating the illusion that structural validation is complete when it is demonstrably not. This means the "whole-story structure engine first" transition goal cannot be achieved because the validator is incomplete. The docstring of `run_all_diagnostics()` at lines 29-35 explicitly states "Currently runs: Layers 1-5... Layer 6... Layer 7..." with no mention of layers 8 and 9, confirming this is not an accidental omission but a known gap in the current implementation.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
<!-- REQUIRED: every item below must include all four fields file, lines, quote, supports_claim (exact key names -- `citation` or similar does NOT satisfy this). validate-brief.py raises EVIDENCE_EXCERPT_FIELD per missing/misnamed key, per excerpt. -->

```yaml
evidence_excerpts:
  - file: src/auteur/structure/state.py
    lines: L185-195
    quote: "_LAYER_ORDER = [(1, DiagnosticLayer.TARGET_EXPERIENCE, 'Target Experience'), (2, DiagnosticLayer.CONSTRAINTS, 'Promise / Constraints'), (3, DiagnosticLayer.SCOPE, 'Scope / Container'), (4, DiagnosticLayer.STRUCTURAL_FORCES, 'Structural Forces'), (5, DiagnosticLayer.THREADS, 'Threads / Modules'), (6, DiagnosticLayer.CARRIERS, 'Carriers'), (7, DiagnosticLayer.REPRESENTATION, 'Representation (Scene Outline)'), (8, DiagnosticLayer.MODULATION, 'Modulation'), (9, DiagnosticLayer.THEME, 'Theme / Resonance')]"
    supports_claim: "The state_check function displays all 9 layers including MODULATION and THEME in its output, suggesting they are validated."
  - file: src/auteur/structure/analyzer.py
    lines: L21-63
    quote: "def run_all_diagnostics(blueprint: StoryBlueprint, bible: StoryBible, *, outline: dict | None = None, cartographer_outline: object | None = None) -> list[StructureDiagnostic]: ... diagnostics.extend(analyze_structure(blueprint)); diagnostics.extend(as_structure_diagnostic(d) for d in audit_bible_locations(bible)); diagnostics.extend(as_structure_diagnostic(d) for d in audit_outline_carriers(outline, bible)); if cartographer_outline is not None: diagnostics.extend(audit_outline_vs_story_engine(blueprint, cartographer_outline))"
    supports_claim: "The run_all_diagnostics function only invokes validators for layers 1-7; no validators for MODULATION (layer 8) or THEME (layer 9) are called."
  - file: src/auteur/structure/analyzer.py
    lines: L29-35
    quote: "Currently runs: - Layers 1-5: analyze_structure() for within-blueprint coherence (Structure Diagnostic) - Layer 6: audit_bible_locations() for Bible Audit carrier state consistency - Layer 7: audit_outline_carriers() for Scene Representation validation (requires outline)"
    supports_claim: "The docstring of run_all_diagnostics explicitly documents only layers 1-7 as implemented, confirming layers 8 and 9 are not currently validated."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

If layers 8 and 9 remain unimplemented, the structural validation system is incomplete and authors cannot achieve the goal of "whole-story structure engine first" validation before drafting. The architecture declares these layers as part of the design (visible in enums, CLI lists, and docs), but they are not enforced, creating a false sense of validation completeness. When authors see `state check` pass with no errors, they have only validated 7 of 9 layers. This means the system cannot detect thematic incoherence, modulation problems, or narrative closure gaps before chapter generation begins, directly contradicting the transition goal. Additionally, if new validation rules are added to layers 1-7, modulation and resonance concerns remain unmeasured, and the gap between documentation and implementation will widen over time as more features reference these layers without proper validation backing.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Audit existing layer 8 and 9 concepts in the codebase (search for "modulation", "resonance", "theme", "coherence" in docs and code) to identify any partial implementations or design patterns already in place.
2. Design layer 8 (Modulation) diagnostic rules: thematic consistency rules, emotional trajectory validation, pacing coherence checks based on the story engine.
3. Design layer 9 (Resonance) diagnostic rules: narrative closure validation, character arc completion checks, thematic resolution assessment.
4. Implement the validator functions and integrate them into `run_all_diagnostics()` so they run alongside existing layer validators.
5. Add end-to-end tests covering layer 8 and 9 failures, repairs, and successful validation paths.
6. Document the new validators in the layer-to-command matrix and update CONTEXT.md Layer 8/9 rows.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Implement layers 8 and 9 diagnostic validators and integrate them into `run_all_diagnostics()`. This completes the 9-Layer Engine validation system and unblocks the transition to whole-story structure-first architecture. This is the highest-priority structural gap preventing full validation readiness and contradicts the stated architectural goal.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

The repo-sensemaker identified that layers 8 (Modulation) and 9 (Resonance) of the 9-Layer Structural Engine are declared in the code and displayed in the state_check command output, but no diagnostic validators implement them. This prevents complete structural validation and blocks the transition to "whole-story structure engine first" architecture. Discovery findings indicate the validator infrastructure for layers 1-7 is complete. Implement modulation and resonance validators following the same pattern, integrate them into run_all_diagnostics(), and add tests to verify all 9 layers are validated end-to-end before any chapter drafting occurs.

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: architecture_fog
primary_fog_type: architecture_fog
diagnosis_conflict: False
escalation_recommended: False
evidence:
  - "src/auteur/structure/state.py (L185-195): Layer 8 and 9 declared in _LAYER_ORDER but not validated"
  - "src/auteur/structure/analyzer.py (L21-63): run_all_diagnostics only implements layers 1-7"
  - "src/auteur/structure/analyzer.py (L29-35): Docstring confirms layers 8 and 9 are not implemented"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: ghost_features_missing_layer_8_9_validators
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-26T11:47:55.054649Z"
immutable: true
```
