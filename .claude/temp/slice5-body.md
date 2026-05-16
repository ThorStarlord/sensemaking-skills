## Parent

#2 — Validator Ecosystem Standardization

## What to build

Standardize `scripts/validate-plan.py` to conform to the validator contract. Refactor to use shared utility module for loading all 3 registries (workflow, skill, artifact-contracts). Add `--list-codes` flag and `main(argv)` entry point. Replace free-text error messages with named error code constants (WORKFLOW_NOT_FOUND, EXECUTION_MODE_DENIED, INPUT_MISMATCH, STEP_COUNT_MISMATCH, STEP_SKILL_MISMATCH, STEP_TYPE_MISMATCH, GATE_MISMATCH, INPUT_ARTIFACT_MISMATCH, OUTPUT_ARTIFACT_MISMATCH, ARTIFACT_NOT_CONTRACTED, GATE_BEHAVIOR_MISSING, SIMULATED_GATE_CLASH, STOP_CONDITIONS_EMPTY, SUBSET_NOT_CONTIGUOUS, SECTION_11_MALFORMED, ABSOLUTE_PATH_DETECTED). Change output format to `ERROR {CODE}: {message}`. Normalize positional argument name from `plan_path` to `artifact_path`.

Update its fixture files in `tests/fixtures/validate-plan/` to reference stable error codes.

## Acceptance criteria

- [ ] Uses shared registry loading from `_validator_utils.py`
- [ ] `--list-codes` prints all stable error codes and exits 0
- [ ] `main(argv)` entry point callable programmatically
- [ ] Error output uses `ERROR {CODE}: {message}` format
- [ ] Negative fixture `expected_error_contains` values reference stable codes
- [ ] `python scripts/test-validators.py` passes

## Blocked by

- #3 — shared utility module
