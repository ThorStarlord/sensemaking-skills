# Validator Ecosystem: Implementation Plan

**Date:** 2026-05-16
**Status:** Plan — not yet executed
**Driving decision doc:** `docs/validator-ecosystem/2026-05-16-validator-ecosystem-grill.md`

---

## Phase Order and Rationale

Phases are ordered to minimize risk: shared infrastructure first (so nothing breaks), then mechanical standardization (no behavior change), then new functionality last.

```
Phase 1 ──> Phase 2 ──> Phase 3 ──> Phase 4
(Shared lib)  (Interface std)  (Codes+Output)  (New validator)
```

---

## Phase 1: Shared Utility Module

**Goal:** Eliminate duplicated registry-loading and path-resolution code across 5 validators.

### Step 1.1 — Create `scripts/_validator_utils.py`

A single module. The leading underscore prevents auto-discovery by `test-validators.py` (which scans for `validate-*.py`).

```python
# Interface sketch — exact implementation detail left to execution

def load_yaml(path: str) -> dict | None        # Safe YAML load with error wrapping
def load_workflow_registry(repo_root: str) -> dict
def load_artifact_contracts(repo_root: str) -> dict
def load_skill_registry(repo_root: str) -> dict
def load_weakness_types(repo_root: str) -> list[str]
def resolve_path(given: str, script_dir: str) -> str  # --repo-root resolution
def format_error(code: str, message: str) -> str       # "ERROR CODE: message"
```

**Contains:** Only pure functions. No side effects. No CLI. Importable by any validator.

### Step 1.2 — Refactor each validator to use shared utils

This is mechanical: replace inline YAML loading with `load_*()` calls. Each file's signature and behavior stay identical.

| Validator | What changes |
|-----------|--------------|
| `validate-brief.py` | Replace inline `_load_weakness_types` + YAML loading with shared utils |
| `validate-plan.py` | Replace 3 inline YAML loads with `load_workflow_registry`, `load_artifact_contracts`, `load_skill_registry` |
| `validate-artifact.py` | Replace inline contract loading with `load_artifact_contracts` |
| `validate-repo.py` | Optional — can use shared utils where convenient, but not required |
| `validate-skill-improvement-plan.py` | No registry loading currently — no change needed |
| `validate-usage-research-report.py` | No registry loading currently — no change needed |

**Risk:** Low. Pure function extraction. Test suite should pass without changes.

### Step 1.3 — Verify

```bash
python scripts/test-validators.py
python scripts/validate-repo.py
```

---

## Phase 2: Standardize CLI Interfaces

**Goal:** Every Level 2 and Level 3 validator accepts the same flags. No behavioral changes yet.

### Step 2.1 — Add `--repo-root` to `validate-usage-research-report.py`

Currently it has `report_path` only. Add a `--repo-root` arg that defaults to `"."`. The argument is accepted but not used yet — it's for interface uniformity.

**Changes to:** `scripts/validate-usage-research-report.py`

### Step 2.2 — Add `--list-codes` to all validators that lack it

Validators that currently have no error codes will add the flag early, returning an empty list (codes get added in Phase 3). This makes the flag contractually present across the ecosystem.

**Changes to:** `validate-plan.py`, `validate-skill-improvement-plan.py`, `validate-usage-research-report.py`, `validate-artifact.py`

### Step 2.3 — Add `main(argv=None) -> int` entry point to all validators

Standardize the callable entry point so validators can be imported and called programmatically (test-validators.py currently shells out, but shouldn't have to).

**Pattern:**

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args(argv)
    if args.list_codes:
        ...  # print codes, return 0
    errors = validate_thing(args.artifact_path, args.repo_root)
    for e in errors:
        print(f"ERROR {e}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 2.4 — Normalize positional arg names

All artifact validators use `artifact_path` as the positional name. Currently: `plan_path`, `report_path`, `artifact_path`, `artifact_id + artifact_path`. The `validate-artifact.py` takes two positionals — keep that as the exception (it's Level 2, always takes `artifact_id` first).

**Changes to:** `validate-plan.py` (`plan_path` → `artifact_path`), `validate-skill-improvement-plan.py` (`plan_path` → `artifact_path`), `validate-usage-research-report.py` (`report_path` → `artifact_path`)

### Step 2.5 — Update `test-validators.py`

Remove the hardcoded script-name check on line 35-36 that special-cases which validators get `--repo-root`. Now every validator accepts it uniformly.

### Step 2.6 — Verify

```bash
python scripts/test-validators.py
# Test --list-codes on each validator
python scripts/validate-brief.py --list-codes
python scripts/validate-plan.py --list-codes
python scripts/validate-skill-improvement-plan.py --list-codes
python scripts/validate-usage-research-report.py --list-codes
python scripts/validate-artifact.py --list-codes
```

---

## Phase 3: Stable Error Codes + Output Format

**Goal:** Every Level 3 validator has stable error codes and machine-parseable output.

### Step 3.1 — Define error codes for `validate-plan.py`

Current errors are free-text strings. Extract them into named constants. Categorize:

```
WORKFLOW_NOT_FOUND      — chosen_workflow_id missing from registry
EXECUTION_MODE_DENIED   — mode not in allowed_execution_modes
INPUT_MISMATCH          — initial_inputs don't match registry
STEP_COUNT_MISMATCH     — step count differs from registry
STEP_SKILL_MISMATCH     — step skill doesn't match registry
STEP_TYPE_MISMATCH      — step_type doesn't match registry
GATE_MISMATCH           — gate doesn't match registry
INPUT_ARTIFACT_MISMATCH — input_artifact doesn't match registry
OUTPUT_ARTIFACT_MISMATCH— output_artifact doesn't match registry
ARTIFACT_NOT_CONTRACTED — output_artifact not produced_by this skill
GATE_BEHAVIOR_MISSING   — missing gate_behavior for a declared gate
SIMULATED_GATE_CLASH    — approved_by_user=true but gate is simulated
STOP_CONDITIONS_EMPTY   — stop_conditions is missing or empty
SUBSET_NOT_CONTIGUOUS   — included_steps not a contiguous subsequence
SECTION_11_MALFORMED    — Section 11 YAML block not found or unparseable
ABSOLUTE_PATH_DETECTED   — absolute path in YAML block
```

**Changes to:** `scripts/validate-plan.py`

### Step 3.2 — Define error codes for `validate-skill-improvement-plan.py`

```
IMPROVEMENT_FILE_NOT_FOUND
MISSING_SECTION
INVALID_FAILURE_MODE_CLASS
INVALID_DEFECT_SOURCE
MISSING_SOURCE_REPORT
SOURCE_REPORT_NOT_FOUND
ABSOLUTE_SOURCE_REPORT_PATH
MISSING_EVIDENCE_SNIPPET
INVALID_RECOMMENDED_ACTION
MISSING_EDIT_TYPE
MISSING_RISK_LEVEL
MISSING_ANTI_OVERFITTING
MISSING_RERUN_SCENARIO
MISSING_SUCCESS_CRITERIA
ABSOLUTE_PATH_DETECTED
```

**Changes to:** `scripts/validate-skill-improvement-plan.py`

### Step 3.3 — Define error codes for `validate-usage-research-report.py`

```
REPORT_FILE_NOT_FOUND
MISSING_SECTION
INVALID_SEMANTIC_SCORE
INVALID_FAILURE_CLASSIFICATION
PLACEHOLDER_DETECTED
ABSOLUTE_PATH_DETECTED
ROLE_BOUNDARY_VIOLATION
```

**Changes to:** `scripts/validate-usage-research-report.py`

### Step 3.4 — Define error codes for `validate-artifact.py`

```
ARTIFACT_FILE_NOT_FOUND
CONTRACTS_FILE_NOT_FOUND
CONTRACT_NOT_FOUND
ABSOLUTE_FILE_LINK
MISSING_REQUIRED_SECTION
MISSING_YAML_BLOCK
MISSING_MACHINE_FIELDS
MISSING_EVIDENCE_EXCERPTS
MISSING_EXCERPT_FIELD
ABSOLUTE_EXCERPT_PATH
```

**Changes to:** `scripts/validate-artifact.py`

### Step 3.5 — Standardize output format

All validators output `ERROR {CODE}: {message}`. The `format_error()` from the shared utils module is the canonical way to produce this.

**Changes to:** All 5 validators that use errors (not validate-repo, which stays free-text).

### Step 3.6 — Update negative fixtures

Each negative fixture's `expected_error_contains` frontmatter field must reference the stable error code, not a free-text fragment. This is the regression guarantee.

**Example:**
```yaml
---
expected_error_contains: HALLUCINATED_WORKFLOW_ID
---
```

**Changes to:** All existing negative fixtures across all validator fixture directories.

### Step 3.7 — Verify

```bash
python scripts/test-validators.py
# Spot-check: each --list-codes output matches module constants
```

---

## Phase 4: New `prompt_handoff` Specialized Validator

**Goal:** Add `scripts/validate-prompt-handoff.py` for `prompt_handoff` artifacts.

### Step 4.1 — Create `scripts/validate-prompt-handoff.py`

Checks:

| Check | Error Code | What It Validates |
|-------|------------|-------------------|
| Section presence | `MISSING_SECTION` | target_skill, context_to_preserve, task, constraints, inputs, expected_output, stop_condition, ready_to_copy_prompt |
| Target skill exists | `UNKNOWN_TARGET_SKILL` | The `Target Skill` value exists in `skill-registry.yaml` |
| Stop condition has content | `EMPTY_STOP_CONDITION` | The stop condition is more than just a heading with whitespace |
| Expected output non-empty | `EMPTY_EXPECTED_OUTPUT` | The expected output is populated |
| No hallucinated artifact refs | `HALLUCINATED_ARTIFACT_REF` | Any artifact IDs mentioned exist in `artifact-contracts.yaml` |
| Absolute path ban | `ABSOLUTE_PATH_DETECTED` | No `file:///` or path with drive letter |
| Ready-to-copy prompt present | `MISSING_READY_PROMPT` | The ready-to-copy prompt block exists and is non-empty |

### Step 4.2 — Register in `artifact-contracts.yaml`

Add to the `prompt_handoff` contract entry:

```yaml
specialized_validators:
  - "python scripts/validate-prompt-handoff.py {artifact_path}"
```

### Step 4.3 — Create fixture directories

```
tests/fixtures/validate-prompt-handoff/
├── valid/
│   └── valid-prompt-handoff.md          # Fully correct handoff
└── invalid/
    ├── unknown-target-skill.md           # Target skill not in registry
    ├── empty-stop-condition.md           # Stop condition is blank
    ├── hallucinated-artifact-ref.md      # References fake artifact ID
    ├── missing-ready-prompt.md           # No ready-to-copy-prompt block
    └── absolute-path-detected.md         # Contains file:/// reference
```

### Step 4.4 — Update `test-validators.py` registration

No code change needed — it auto-discovers new `validate-*.py` scripts. Verify the fixture directory is picked up.

### Step 4.5 — Add required regression

Add to `tests/fixtures/REGRESSIONS.yaml`:

```yaml
- id: prompt-handoff-unknown-target-skill
  validator: validate-prompt-handoff
  fixture: tests/fixtures/validate-prompt-handoff/invalid/unknown-target-skill.md
  reason: Prevent regression of hallucinated target skills in handoff artifacts.
```

### Step 4.6 — Verify

```bash
python scripts/test-validators.py
```

---

## File Change Summary

| File | Phase | Action |
|------|-------|--------|
| `scripts/_validator_utils.py` | 1 | Create |
| `scripts/validate-brief.py` | 1 | Refactor to shared utils |
| `scripts/validate-plan.py` | 1, 2, 3 | Refactor to shared utils, add `--list-codes`, add error codes |
| `scripts/validate-artifact.py` | 1, 2, 3 | Refactor to shared utils, normalize CLI, add error codes |
| `scripts/validate-repo.py` | 1 | Optional shared utils usage |
| `scripts/validate-skill-improvement-plan.py` | 2, 3 | Add `--list-codes`, add error codes, normalize `--repo-root` |
| `scripts/validate-usage-research-report.py` | 2, 3 | Add `--repo-root`, add `--list-codes`, add error codes |
| `scripts/validate-prompt-handoff.py` | 4 | Create |
| `scripts/test-validators.py` | 2 | Remove hardcoded `--repo-root` special case |
| `skills/workflow-orchestrator/references/artifact-contracts.yaml` | 4 | Register prompt_handoff specialized validator |
| `tests/fixtures/REGRESSIONS.yaml` | 4 | Add prompt-handoff regression entry |
| `tests/fixtures/validate-*/invalid/*.md` | 3 | Update `expected_error_contains` to stable codes |
| `tests/fixtures/validate-prompt-handoff/` | 4 | Create fixture directory (valid + 5 invalid) |

**Total new files:** 2 (`_validator_utils.py`, `validate-prompt-handoff.py` + fixture directory)
**Total modified files:** 8-9

---

## Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Shared utils change breaks a validator | Low | Run full test suite after each refactor step |
| Stable error codes make negative fixtures too strict | Medium | Keep a mapping of old free-text → new code during migration; verify each fixture actually fails for the expected code |
| `validate-repo.py` has no fixture coverage | N/A (accepted) | Already excluded from test suite. Structural validators inherently can't be fixture-tested |
| `validate-prompt-handoff` duplicates logic from `validate-artifact.py` (section checks) | Low | The generic validator still runs first (Level 2 before Level 3). The specialized validator adds cross-registry checks the generic one can't do |
| New artifact type added later but no fixture for it | Low | Covered by the contract mapping in `artifact-contracts.yaml`, not by fixture coverage |
