# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-26T10:50:52.689746Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

Auteur is an opinionated narrative-engine toolkit for long-form fiction authoring. It provides writers with a deterministic, layered approach to story composition: taking raw creative input (a premise) through seven semantic layers (Universe → Series → Identity → Structure → Realization → Expression → Editing), validating each layer against genre contracts and narrative coherence rules, and optionally generating outlines and prose drafts through multi-LLM providers (Anthropic Claude, OpenAI GPT). The toolkit emphasizes deterministic validation over pure generative AI, treating LLM outputs as one part of a larger structured compilation pipeline.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

The repository is a mature Python package (v0.35.0) with:

- **Core library** (`src/auteur/`): ~50 modules across 12 domains (universe, series, identity, structure, realization, expression, character, convergence, commitment, decision, planning, simulation, workflow, UI)
- **CLI** (`auteur` command): ~30 subcommands organized by domain (identity, blueprint, structure, draft, plan, simulate, state, charmap, etc.)
- **Genre pipelines**: Three fully implemented browser-based interactive authoring workflows (netorare, mystery, gentlefemdom) with 3 emotional cores each and 9-phase decision trees
- **Validation infrastructure**: 20+ deterministic rules across Identity, Structure, and Realization layers; Pydantic models for all major artifacts
- **LLM integration**: Dual-provider support with per-agent model routing, exponential-backoff retry, and dry-run mode
- **Scripts** (`scripts/`): ~20 utility scripts for orchestration, validation, skill execution, and testing
- **Tests**: pytest suite with comprehensive coverage across modules
- **Documentation**: 7 ADRs, architecture.md, narrative-architecture.md, structure-engine-v1.md, genre-overrides.md, plus archived planning notes
- **Project artifacts**: YAML-based story identity, blueprint, and outline schemas; JSON bible.json for state tracking

All major semantic layers are production-ready with working CLI commands, validation rules, and documented contracts.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

1. **Complete 7-layer hierarchy implementation**: All semantic layers (Universe → Series → Identity → Structure → Realization → Expression → Editing) are implemented with working CLI commands, validation, and examples. The docs/adr/ directory confirms each layer was shipped through design-acceptance cycles.

2. **Proven extensible architecture**: Genre pipelines follow an identical pattern across three distinct genres (netorare, mystery, gentlefemdom), each with 3 emotional cores, 9-phase templates, and 10+ validation rules. CLAUDE.md explicitly validates this pattern as "production-ready for additional genres."

3. **Sophisticated deterministic validation**: 20+ named rules enforce coherence across Identity (want-change, genre tone), Structure (subplot budgets, subgenre modifiers), and Realization (state consistency). Rules are testable independently and compose into multi-rule diagnostics.

4. **Dual LLM provider maturity**: RetryingClient (exponential backoff + jitter) handles transient errors; per-agent model routing allows blueprint-level control; adapters for both Anthropic and OpenAI with feature parity.

5. **Full proposal lifecycle**: Diagnose → Generate Repair Proposals → Select → Apply cycle implemented for structure problems and genre violations; users can review recommendations before mutation.

6. **Production CLI maturity**: ~30 subcommands with consistent option handling, help text, and error reporting. `auteur state` commands coordinate multi-layer operations; `auteur plan` provides project-level narrative coordination.

7. **Browser-based interactive authoring**: Genre pipelines use versioned session state, atomic writes, deterministic choice validation, and explicit ratification before identity compilation — no silent mutations.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

1. **Genre UI/UX documentation**: The README mentions "interactive browser-based sessions" but provides no visual examples, user flow descriptions, or accessibility considerations. Users cannot predict the UI layout from documentation alone.

2. **End-to-end workflow examples**: While individual CLI commands are documented, there is no step-by-step walkthrough of a complete project from raw premise → validated identity → generated blueprint → drafted chapter → accepted final.md. The Quick Start jumps between commands without showing real output.

3. **Orchestration framework integration**: The `scripts/` directory contains production-grade orchestration (orchestration-runner.py, skill-execution-dispatcher.py) that assumes external `workflow-registry.yaml`, `artifact-contracts.yaml`, and `skill-registry.yaml` files. These files are not in this repository, making the scripts non-functional without external infrastructure.

4. **Architecture documentation lag**: The CLAUDE.md claims "Universe layer (implemented 2026-07-11) completes the hierarchy" as a recent change, yet there is no corresponding doc/architecture/v0.36.0 acceptance or design document. The narrative-architecture.md does not show the Universe layer's role in the 7-layer model.

5. **Glossary or domain-language reference**: Terms like "realization layer", "convergence service", "commitment execution", and "simulation projection" are not centrally defined. New contributors must infer meanings from class names and docstrings.

6. **Test coverage gaps for genre validation**: While netorare/mystery/gentlefemdom have 75–154 unit tests each, there is no integration test showing a complete genre pipeline (session → browser validation → identity compilation) end-to-end.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

1. **Create visual genre pipeline guide**: Document the 9-phase decision tree and browser UI with wireframes or screenshots. Show decision constraints and how author choices map to StoryIdentity fields.

2. **Add canonical project workflow walkthrough**: Create a complete worked example using a simple 5-chapter story: premise → identity recommendation → blueprint seed → structure diagnosis → outline compilation → draft → critique → accept. Show all inputs and outputs.

3. **Extract the genre pattern as a reusable SDK**: The 9-layer genre pipeline pattern is proven but currently embedded in genre-specific code. Package it as `auteur.genre_pipeline_runtime` for simpler third-party genre additions.

4. **Document architecture decisions as decision records**: Create architecture/ decision records for: (1) why 7 semantic layers, (2) why deterministic validation first, (3) why LLM calls are optional, (4) why Pydantic models own schema truth.

5. **Add a glossary section to CONTEXT.md**: Define key terms: realization, convergence, commitment, simulation, proposal lifecycle, semantic layer, genre override, subgenre modifier, emotional core.

6. **Annotate orchestration scripts with external dependencies**: Add comments to orchestration-runner.py, skill-execution-dispatcher.py, etc. documenting the required external registry files and their expected schema. Consider a `--validate-registries` subcommand.

7. **Create genre UI/UX testing framework**: Build a headless browser test harness that exercises all 9 phases for each genre, verifies choice validation errors, and confirms identity compilation.

8. **Verify RetryingClient behavior under network failures**: Add integration tests simulating transient failures (rate limits, timeouts) to prove exponential backoff + jitter work in practice.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

The weakest boundary is between the Auteur core library (fully self-contained, well-validated) and the production orchestration infrastructure (scripts/ directory). The scripts assume an external orchestration framework and registry files that are not part of this repository.

**Evidence**: The scripts `orchestration-runner.py` (L24-31) and `skill-execution-dispatcher.py` directly call `load_workflow_registry()`, `load_artifact_contracts()`, and `load_skill_registry()` from `_validator_utils.py`. These files are expected to exist at `docs/mode-coverage.yaml`, workflow registry paths defined in environment, but the paths are not documented and the registry YAML files are not included in this repository. The scripts will fail at runtime with "file not found" errors if deployed without the external sensemaking-external-exp2-framework infrastructure.

This is a textbook **Implicit Dependencies** weakness: the scripts are production-grade and assume a complete external orchestration framework (workflow IDs, artifact contracts, skill definitions, approval gates) exists, but this dependency is neither documented in the README nor validated by any "check" or "validate" command.

**Type**: Implicit Dependencies

**Consequence**: Users or downstream orchestrators deploying these scripts standalone will encounter silent failures when registry files are missing. CI/CD pipelines that run `python scripts/check.py` may pass locally (if registry files happen to exist) but fail in clean environments.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

**Implicit Dependencies** are evident in the orchestration scripts. The `scripts/orchestration-runner.py` file (lines 24-31) imports directly from `_validator_utils` which defines functions like `load_workflow_registry()`, `load_artifact_contracts()`, and `load_skill_registry()`. These functions attempt to load YAML files from paths that are not part of the auteur repository.

Running `orchestration-runner.py` without the external framework will fail at module load time with missing registry data. The README (lines 1–23) does not mention these external dependencies; it positions Auteur as a self-contained toolkit for "opinionated interpretation" of story premises, yet the scripts directory contains production orchestration code that requires external infrastructure.

Additionally, the scripts/check.py and docs/mode-coverage.yaml refer to workflow execution modes (plan_only, guided_execution, autonomous_execution) that are defined in the external sensemaking framework, not in Auteur itself. The integration is undocumented.

<!-- MODEL_SECTION:evidence_prose:END -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
```yaml
evidence_excerpts:
  - file: "scripts/orchestration-runner.py"
    lines: "24-31"
    citation: "Import statements reference _validator_utils functions (load_workflow_registry, load_artifact_contracts, load_skill_registry) which load YAML files not included in the repository."
  - file: "scripts/_validator_utils.py"
    lines: "1-50"
    citation: "Utility module defines registry-loading functions that expect external YAML files (workflow-registry.yaml, artifact-contracts.yaml, skill-registry.yaml) at paths not documented in README."
  - file: "pyproject.toml"
    lines: "1-47"
    citation: "Project declares no dependencies on external orchestration framework; entry point is 'auteur.cli:main' which does not reference orchestration-runner.py."
  - file: "README.md"
    lines: "1-347"
    citation: "README focuses on Auteur CLI commands and narrative engine features; does not mention scripts/ directory or external orchestration framework dependency."
  - file: "docs/mode-coverage.yaml"
    lines: "1-50"
    citation: "Refers to execution modes (plan_only, guided_execution, autonomous_execution, yolo_execution) and approval gates that are managed by external orchestration framework."
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

The implicit dependencies create a **deployment risk**: an operator deploying these scripts in isolation (e.g., in CI/CD, in a local automation layer, or in a customer environment) will encounter cryptic "file not found" errors at runtime. The scripts will not fail fast with a clear error message like "Orchestration framework not detected" — instead, they will fail during module import, making debugging difficult.

The boundary also creates a **documentation debt**: the README positions Auteur as a complete self-contained toolkit, yet the scripts directory contradicts this by assuming external infrastructure. New contributors cloning the repository might assume the orchestration workflows are functional out-of-the-box, leading to wasted troubleshooting time.

From an **architecture perspective**, the boundary violates the principle of "explicit dependencies": the orchestration scripts should either (1) be removed from the repository if they are external-framework-specific, or (2) be rewritten to fail fast with a clear error message and documented dependency list.

This is a **medium-severity** issue because:
- The core Auteur library (src/auteur/) is self-contained and functional.
- The CLI (auteur identity, auteur draft, auteur plan) does not depend on the orchestration scripts.
- Most users will not interact with the scripts/ directory directly.
- However, advanced users or operators trying to automate Auteur workflows will hit this wall.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. **Audit and document the orchestration framework contract**: Review scripts/orchestration-runner.py, scripts/skill-execution-dispatcher.py, and scripts/_validator_utils.py. Document the exact schema for workflow-registry.yaml, artifact-contracts.yaml, and skill-registry.yaml. Add a README.md to the scripts/ directory explaining these dependencies.

2. **Add a pre-flight check to the scripts**: Modify _validator_utils.py to export a `validate_orchestration_environment()` function that checks for required registry files and reports missing dependencies clearly before any execution begins.

3. **Reconcile README and scripts/ documentation**: Either (a) remove scripts/ if they are not part of the core Auteur product, or (b) add a "Production Orchestration" section to the README explaining when and how to use the orchestration scripts and what external infrastructure is required.

4. **Create an integration test for orchestration**: Write a test that mocks the external registries and verifies that orchestration-runner.py can execute a workflow end-to-end. This proves the implicit dependencies are satisfied.

5. **Add schema examples to docs/**: Create example workflow-registry.yaml, artifact-contracts.yaml, and skill-registry.yaml files in docs/examples/ so users understand the expected structure.

6. **Extract orchestration as optional feature**: If the scripts are truly optional, move them to scripts-optional/ or a separate repository, and add a note in the README explaining where to find them.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

**Recommended Action**: Audit the orchestration scripts and document their external dependencies. This is a **discovery + documentation task**, not a code fix. The goal is to prevent deployment failures and clarify the Auteur architecture.

**Rationale**: The core Auteur library is solid and well-documented. The implicit dependencies are contained to a small set of scripts that advanced users might deploy. Documenting these dependencies is a low-risk, high-value fix that clarifies the repository boundary and prevents future confusion.

**Expected outcome**: 
- README updated with a "Production Orchestration" section explaining scripts/ and external framework requirements.
- scripts/README.md created documenting the registry contracts and dependencies.
- _validator_utils.py updated with a pre-flight check function.
- No code changes required to core Auteur functionality.

This work should be routed to a **full-local-diagnostic** or **docs-implementation-workflow** to clarify repository boundaries and update documentation.

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

You are auditing the Auteur narrative-engine toolkit repository to clarify its architectural boundaries. The core library (src/auteur/) is a complete, self-contained Python toolkit for story structure validation and generation. However, the scripts/ directory contains orchestration code (orchestration-runner.py, skill-execution-dispatcher.py) that assumes external YAML registry files (workflow-registry.yaml, artifact-contracts.yaml, skill-registry.yaml) that are not included in the repository.

**Your task**: 
1. Review scripts/orchestration-runner.py and scripts/_validator_utils.py to understand what external registries are required and how they are used.
2. Check whether these registry files are documented anywhere (README, docs/, CI config).
3. Document the findings in a brief (< 500 words) explaining: (a) what external files/registries are required, (b) where they should be located, (c) what happens when they are missing, (d) whether the scripts are core Auteur features or optional.
4. Recommend whether to (a) document the dependencies in README, (b) move scripts/ to a separate repository, or (c) refactor scripts to fail fast with clear error messages.

**Context**: This is part of repository sensemaking work to clarify Auteur's architectural boundaries and improve deployment safety.

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
  - "scripts/orchestration-runner.py (L24-31): Import statements reference registry-loading functions"
  - "scripts/_validator_utils.py: Defines registry-loading functions for external YAML files"
  - "README.md (L1-347): Does not document orchestration framework or scripts/ dependencies"
  - "pyproject.toml (L22-23): Entry point is auteur.cli:main, not orchestration-runner"
  - "docs/mode-coverage.yaml: References execution modes managed by external framework"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: Implicit Dependencies
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-26T10:50:52.689746Z"
immutable: true
```
