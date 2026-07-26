# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-26T03:17:04.106490Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is an opinionated narrative engineering toolkit for long-form fiction that prevents narrative drift (lore inconsistencies and character location teleportation) by structuring narrative design and execution around a multi-layer validation architecture. The system prioritizes whole-story structure validation first, with optional chapter outlining and prose generation as downstream stages.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

- **Structure Engine Core** (`src/auteur/structure/state.py`): Implements 9-layer validation pipeline with CLI commands (`check`, `update`, `prepare`, `canon`, `confirm`) coordinated via unified state manager.
- **Layer 1-5 Diagnostics** (`src/auteur/structure/analyzer.py`): Validates target experience, constraints, scope, structural forces, and threads within blueprint coherence.
- **Layer 6 Audit** (`src/auteur/structure/bible_audit.py`): Runs deterministic location teleportation detection using StoryBible event log.
- **Layer 7 Audit** (`src/auteur/structure/outline_audit.py`): Validates scene outlines against character carrier state from Bible.
- **Cross-layer Validation** (`src/auteur/structure/cartographer_audit.py`): Validates CartographerOutline against story engine (threads, characters, theme).
- **Pydantic Schemas** (`src/auteur/blueprint.py`, `src/auteur/bible.py`): Strict validation for StoryBlueprint and StoryBibleModel models.
- **Test Suite**: Comprehensive coverage in `tests/` directory with all tests passing.
- **Documentation**: Architecture decisions in `docs/adr/`, PRDs in `docs/`, and system context in `CONTEXT.md`.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

- **Strict Pydantic validation**: StoryBlueprint and StoryBibleModel schemas enforce shape contracts at load time with comprehensive field validation.
- **Complete test suite**: Passes fully with coverage for state commands, proposal lifecycle, and deterministic lore audit logic.
- **Layered architecture**: Nine-layer diagnostic framework is conceptually sound and progressively implemented through Layers 1-7.
- **Deterministic core**: Structure validation and Bible audit run without LLM calls, making results reproducible and auditable.
- **Outline validation implemented**: Layer 7 validation via `outline_audit.py` successfully loads and validates scene cards against Bible carrier state (implemented and integrated into `run_all_diagnostics`).
- **Cross-layer integration**: CartographerOutline audit (`cartographer_audit.py`) bridges story engine promises to chapter-level outlines with detailed diagnostic rules.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

- **Layer 8 (Modulation) validation**: No automated rule set exists for Modulation layer checks. This layer is defined in the `DiagnosticLayer` enum but has zero implementation in `run_all_diagnostics()`.
- **Layer 9 (Theme/Resonance) validation**: Only partial implementation via thesis reinforcement check in `cartographer_audit.py:226-255`. No dedicated validators for story-level thematic consistency, payoff tracking, or thematic echo detection.
- **Cartographer outline integration in state_check**: The `run_all_diagnostics()` function accepts an optional `cartographer_outline` parameter but the primary `state_check` command never passes it, making Layer 9 validation inaccessible via the standard CLI path.
- **Layer 8 repair options**: No `RepairOptions` suggestions exist for Layer 8 (Modulation) findings since no validators exist.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Implement Layer 8 (Modulation) validators to check pacing consistency, tone progression, and emotional rhythm across chapter outlines.
- Complete Layer 9 (Theme/Resonance) validation with story-level thesis tracking, thematic echo detection, and setup/payoff accounting.
- Extend `state_check` CLI command to accept optional `--cartographer-outline <path>` parameter so users can run full 9-layer validation in a single command.
- Relocate `bible_audit.py` from `auteur.structure` to a new `auteur.audit` package (as documented in ADR 003) to eliminate domain boundary blending.
- Add automated repair proposal generation for Layer 8/9 findings with specific remediation guidance.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness Type:** Zero Validation

The weakest boundary in the current codebase falls under **Zero Validation** of architectural layers. While the system defines a 9-layer diagnostic architecture and implements Layers 1-7 with validators, Layer 8 (Modulation/Pacing) has absolutely no implementation, and Layer 9 (Theme/Resonance) is only partially implemented and unreachable via the primary CLI path.

**Logic Trace**:
1. The `DiagnosticLayer` enum in `src/auteur/structure/diagnostics.py:14-23` defines nine layers: TARGET_EXPERIENCE, CONSTRAINTS, SCOPE, STRUCTURAL_FORCES, THREADS, CARRIERS, REPRESENTATION, MODULATION, and THEME.
2. The `run_all_diagnostics()` function in `analyzer.py` implements validators for Layers 1-7 through calls to `analyze_structure()`, `audit_bible_locations()`, `audit_outline_carriers()`, and (conditionally) `audit_outline_vs_story_engine()`.
3. **Layer 8 (Modulation) has zero validators**: There is no function call to any modulation validator, no diagnostic rules defined, and no repair options.
4. **Layer 9 (Theme/Resonance) is partially implemented but unreachable**: Only `cartographer.theme.thesis_unreinforced` is checked in `cartographer_audit.py:226-255`, and this requires `cartographer_outline` to be passed to `run_all_diagnostics()`, which never happens in the standard `state_check` command.
5. The `state_check()` function in `state.py:159` calls `run_all_diagnostics(blueprint, bible, outline=outline)` without ever providing `cartographer_outline`, making Layer 9 validation inaccessible.

**Proof Points**:
- In `src/auteur/structure/state.py:185-195`, the `_LAYER_ORDER` display loop lists Layer 8 (Modulation) and Layer 9 (Theme/Resonance) as part of the diagnostic report structure, yet no diagnostics are ever populated for these layers.
- The enum in `diagnostics.py` includes `MODULATION` and `THEME`, but `run_all_diagnostics()` in `analyzer.py:21-63` never instantiates validators for either layer.
- CartographerOutline audit (Layer 9 handler) is conditional on a parameter that never gets passed from the CLI entry point.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

The architecture promises comprehensive 9-layer validation but only implements Layers 1-7. Layer 8 (Modulation) has zero automated checks. Layer 9 (Theme/Resonance) is only partially implemented and unreachable via the standard `state_check` command path. In `src/auteur/structure/state.py:185-195`, the _LAYER_ORDER display loop shows Layer 8 (Modulation) and Layer 9 (Theme/Resonance) as diagnostic categories, yet when `state check` runs, no findings are ever generated for these layers. The DiagnosticLayer enum in `src/auteur/structure/diagnostics.py:14-23` includes MODULATION and THEME values, yet `run_all_diagnostics()` in `src/auteur/structure/analyzer.py:21-63` has no corresponding validator for either layer. The cross-layer validation in `cartographer_audit.py:31-39` provides limited Theme checking (thesis reinforcement only in lines 226-255), but this validator is never invoked from `state_check` because `cartographer_outline` is never passed as a parameter.

<!-- MODEL_SECTION:evidence_prose:END -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
```yaml
evidence_excerpts:
  - file: src/auteur/structure/diagnostics.py
    lines: L14-23
    quote: "class DiagnosticLayer(str, Enum):\n    TARGET_EXPERIENCE = \"target_experience\"\n    CONSTRAINTS = \"constraints\"\n    SCOPE = \"scope\"\n    STRUCTURAL_FORCES = \"structural_forces\"\n    THREADS = \"threads\"\n    THEME = \"theme\"\n    CARRIERS = \"carriers\"\n    REPRESENTATION = \"representation\"\n    MODULATION = \"modulation\""
    supports_claim: "The diagnostic architecture defines 9 layers including MODULATION and THEME, but implementation does not follow."
  - file: src/auteur/structure/analyzer.py
    lines: L21-63
    quote: "def run_all_diagnostics(\n    blueprint: StoryBlueprint,\n    bible: StoryBible,\n    *,\n    outline: dict | None = None,\n    cartographer_outline: object | None = None,\n) -> list[StructureDiagnostic]:\n    diagnostics: list[StructureDiagnostic] = []\n    diagnostics.extend(analyze_structure(blueprint))\n    diagnostics.extend(as_structure_diagnostic(d) for d in audit_bible_locations(bible))\n    diagnostics.extend(as_structure_diagnostic(d) for d in audit_outline_carriers(outline, bible))\n    if cartographer_outline is not None:\n        diagnostics.extend(audit_outline_vs_story_engine(blueprint, cartographer_outline))\n    return diagnostics"
    supports_claim: "Layers 1-7 are implemented, but cartographer_outline (Layer 9) is optional and Layer 8 is completely missing."
  - file: src/auteur/structure/state.py
    lines: L159
    quote: "raw_diagnostics = run_all_diagnostics(blueprint, bible, outline=outline)"
    supports_claim: "The state_check command calls run_all_diagnostics without cartographer_outline, making Layer 9 validation unreachable from the CLI."
  - file: src/auteur/structure/cartographer_audit.py
    lines: L31-39
    quote: "def audit_outline_vs_story_engine(\n    blueprint: StoryBlueprint,\n    outline: CartographerOutline | None,\n) -> list[StructureDiagnostic]:\n    \"\"\"Validate a CartographerOutline against the blueprint's story engine.\n    When ``outline`` is None, emits a single INFO that cross-layer validation\n    was skipped (no outline provided)."
    supports_claim: "Layer 9 validation (cartographer audit) is conditional on a parameter never passed from state_check."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

If Layers 8 and 9 validation do not run, the story engine's modulation (pacing consistency, tone progression) and thematic coherence cannot be validated before drafting. This means a story can pass all Layers 1-7 checks (structure is sound, lore is consistent, outlines are plausible) yet still have pacing anomalies or thematic drift that only emerge during prose generation. This forces expensive LLM-based critic loops at draft time or results in stories that feel tonally incoherent despite structural soundness. The unreachable Layer 9 path means theme validation requires special CLI invocations with additional parameters, making the 9-layer promise incomplete for typical users who run the standard `state check` command.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Implement Layer 8 (Modulation) validators to check chapter-to-chapter pacing consistency, emotional tone progression, and rhythm anomalies across the outline.
2. Complete Layer 9 (Theme/Resonance) validation with story-level thesis tracking, thematic echo detection, and setup/payoff accounting.
3. Extend `state_check` command to accept optional `--cartographer-outline <path>` parameter so users can run full 9-layer validation in a single CLI invocation.
4. Add automated repair proposal generation for Layer 8/9 findings with specific, actionable remediation guidance.
5. Relocate `bible_audit.py` from `auteur.structure` to a new `auteur.audit` package per ADR 003 to clarify architectural boundaries.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Implement Layer 8 (Modulation) validators and integrate them into `run_all_diagnostics()` so that pacing and tone consistency can be validated as part of the standard `state check` command. This implementation will close the zero-validation gap and complete the 9-layer architecture promise. Start by defining modulation diagnostic rules for chapter sequence validation, then add repair options for detected pacing anomalies.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

```
Auteur's 9-layer diagnostic architecture is incomplete. Layers 1-7 (Target Experience through Scene Representation) have validators, but Layer 8 (Modulation/Pacing) has zero implementation and Layer 9 (Theme/Resonance) is only partially implemented via an optional cross-layer audit. The primary `state check` command never invokes Layer 9 validation because it doesn't pass the cartographer_outline parameter.

Implement Layer 8 (Modulation) validators to check pacing consistency, tone progression, and emotional rhythm across chapter outlines. Add the validators to `run_all_diagnostics()` in src/auteur/structure/analyzer.py so they run as part of the standard state_check flow. Include repair options for detected pacing anomalies. Ensure all existing tests continue to pass.
```

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
  - "{'src/auteur/structure/diagnostics.py (L14-23)': 'DiagnosticLayer enum defines 9 layers'}"
  - "{'src/auteur/structure/analyzer.py (L21-63)': 'run_all_diagnostics has no Layer 8 validator'}"
  - "{'src/auteur/structure/state.py (L159)': 'state_check never passes cartographer_outline'}"
  - "{'src/auteur/structure/cartographer_audit.py (L31-39)': 'Layer 9 validator is unreachable'}"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Zero Validation
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-26T03:17:04.106490Z"
immutable: true
```
