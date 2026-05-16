# Validator Ecosystem Standardization — PRD

## Problem Statement

The `sensemaking-skills` repository has 6 validator scripts that enforce artifact integrity across the sensemaking pipeline, but they evolved independently. This has created four problems:

1. **Inconsistent CLI interfaces.** Each validator has a different argument name for the artifact path, different flags, and different help text. `validate-usage-research-report.py` lacks `--repo-root` entirely, forcing the test harness to hardcode which scripts get which flags.

2. **Duplicated registry loading.** Registry YAML files (workflow-registry.yaml, artifact-contracts.yaml, skill-registry.yaml) are loaded and parsed independently in multiple validators. The same parsing logic, error handling, and path resolution appear in 4 different files.

3. **No stable error codes.** Only `validate-brief.py` has named error code constants. The other validators emit free-text error messages. This prevents machine parsing, makes regression testing fragile (tests match on substrings of human text), and blocks downstream tooling from handling errors by type.

4. **One high-value validation gap.** `prompt_handoff` artifacts (the terminal artifact in 10 of 11 workflows, consumed by `external_agent`) have only generic Level 2 validation. No specialized validator checks whether the target skill exists in the registry, whether the stop condition has real content, or whether artifact references are hallucinated.

## Solution

Standardize the 6 existing validators into a coherent ecosystem with a shared utility module, uniform CLI interface, stable error codes, and consistent output format. Add one new specialized validator for `prompt_handoff` artifacts.

The implementation is organized into 4 sequential phases:

1. **Shared utility module** — extract registry loading, error formatting, and path resolution into `scripts/_validator_utils.py`
2. **CLI standardization** — uniform `artifact_path` + `--repo-root` + `--list-codes` across all validators
3. **Stable error codes + output format** — named error code constants, `ERROR {CODE}: {message}` output, fixture updates
4. **New prompt_handoff validator** — specialized Level 3 validator with fixtures

## User Stories

1. As an **agent executing a workflow**, I want every artifact validator to accept the same CLI flags, so that I don't need to special-case which flags to pass to which validator.

2. As a **developer adding a new validator**, I want shared utility functions for registry loading and error formatting, so that I don't duplicate boilerplate across validator scripts.

3. As a **developer debugging a validation failure**, I want stable error codes in the output, so that I can search documentation or code for the exact error type.

4. As a **contributor running regression tests**, I want negative fixtures to assert against stable error codes instead of free-text substrings, so that tests don't break when error wording changes.

5. As an **orchestrator deciding whether to halt a workflow**, I want machine-parseable error output, so that I can categorize and handle failures by error type.

6. As a **developer of the test harness**, I want validators to have a `main(argv)` entry point, so that I can import and call them programmatically instead of subprocessing.

7. As a **developer working on the ecosystem**, I want a shared utility module with a leading underscore in its name, so that it is automatically excluded from the test harness's auto-discovery.

8. As an **agent producing a prompt handoff**, I want a specialized validator that checks my target skill exists in the registry, so that hallucinated skill IDs are caught before handoff reaches the external agent.

9. As a **developer adding a new validator**, I want to follow a documented how-to guide, so that I know the standard steps for script creation, contract registration, and fixture setup.

10. As a **developer maintaining the ecosystem**, I want `validate-repo.py` to remain structurally separate, since it validates the entire repository state and cannot be fixture-tested.

11. As a **developer extending usage research validators**, I want `--repo-root` to be present on all validators including `validate-usage-research-report.py`, so that the test harness does not need hardcoded special-case logic.

## Implementation Decisions

### Architecture: Three-Level Hierarchy

The existing three-level hierarchy (Structural → Generic → Specialized) is preserved and formalized:

- **Level 1** (`validate-repo.py`): Structural, no standard CLI, no fixture coverage. Special exception.
- **Level 2** (`validate-artifact.py`): Generic, passes through all contract checks. Takes `artifact_id` + `artifact_path` as positionals.
- **Level 3** (one per artifact type): Specialized, follows the standard CLI contract.

### Shared Utility Module: Single File

A single `scripts/_validator_utils.py` module, not a package. Provides pure functions for:
- Registry loading (`load_workflow_registry`, `load_artifact_contracts`, `load_skill_registry`, `load_weakness_types`)
- Error formatting (`format_error` returning `"ERROR {CODE}: {message}"`)
- Path resolution (`resolve_repo_root`)

The leading underscore prevents auto-discovery by the test harness (which scans for `validate-*.py`).

### Standard CLI Contract

```
python scripts/validate-{name}.py <artifact_path> [--repo-root PATH] [--list-codes]
```

- `artifact_path`: positional with `nargs="?"` (omittable with `--list-codes`)
- `--repo-root`: defaults to `"."`
- `--list-codes`: prints stable error codes and exits 0
- Exit code 0 = pass, 1 = any error

Exceptions: `validate-artifact.py` takes `artifact_id` first. `validate-repo.py` takes no positionals.

### Standard Output Format

```
ERROR {CODE}: {descriptive message}
```

One error per line. Multiple errors for the same artifact are all reported.

### Stable Error Codes

Every Level 3 validator defines module-level constants. Exposed via `--list-codes`. Used in `expected_error_contains` in negative fixture frontmatter. Guaranteed stable across versions.

### prompt_handoff Validator Scope

New `scripts/validate-prompt-handoff.py` checks:
- Required sections exist
- Target skill exists in `skill-registry.yaml`
- Stop condition has substantive content
- Expected output is populated
- Artifact references exist in `artifact-contracts.yaml`
- No absolute paths
- Ready-to-copy prompt block is non-empty

Registered in `artifact-contracts.yaml` as a specialized validator for the `prompt_handoff` artifact type.

### Scope Boundary

Only `prompt_handoff` gets a new specialized validator. The other 17 artifact types (persona_definition, okr_list, roadmap, etc.) are adequately served by the generic Level 2 validator. Adding validators for `problem_frame` or `unknowns_map` was explicitly rejected — they have no cross-registry references to validate and only 6-7 sections each.

## Testing Decisions

A good test for this ecosystem validates external behavior only: given an artifact file, the validator produces the expected exit code and expected error output. Tests should not depend on internal implementation details like which functions are called or how registries are cached.

### What Gets Tested

- **All existing validators** continue to have fixture coverage via the Validator Verification Suite
- **Negative fixtures** are updated to assert against stable error codes instead of free-text substrings
- **New prompt_handoff validator** gets 1 valid + 5 invalid fixtures at minimum
- **REGRESSIONS.yaml** gets one new entry for prompt_handoff unknown-target-skill

### Prior Art

The existing test infrastructure in `scripts/test-validators.py` provides the pattern: fixture files with YAML frontmatter (`validator_case`, `expected_error_contains`, `validator_args`) that the test harness runs as subprocesses and checks exit codes and output substrings.

### What Is NOT Tested

- `validate-repo.py` remains excluded from the fixture-based test suite (structural validator, not fixture-testable)
- Shared utility module functions are tested implicitly through the validators that use them (no separate unit tests)

## Out of Scope

- **No new validators for the other 17 artifact types.** Only `prompt_handoff` is added. The design decision document explicitly rejects `problem_frame` and `unknowns_map` validators as unnecessary.

- **No CI/CD pipeline changes.** The test harness is already runnable; no GitHub Actions or other CI changes are part of this work.

- **No schema format changes.** Validation remains regex-based against Markdown+YAML documents. No migration to JSON Schema, Pydantic, or other formal schema systems.

- **No `validate-repo.py` refactor.** It keeps its own CLI and remains excluded from fixture coverage.

- **No behavioral changes to existing validators** beyond error code extraction and output format. The validation logic itself stays identical.

## Further Notes

- The implementation plan is ordered to minimize risk: shared infrastructure first (no behavior change), then mechanical CLI standardization (no behavior change), then error codes and output format, then new functionality last.
- At each phase, `python scripts/test-validators.py` must pass. The 4-phase sequence means the test suite is green at every intermediate state.
- The documents `docs/validator-ecosystem/ARCHITECTURE.md` and `docs/validator-ecosystem/2026-05-16-validator-ecosystem-grill.md` contain the full design rationale and should be consulted before deviating from this plan.
