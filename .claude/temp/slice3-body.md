## Parent

#2 — Validator Ecosystem Standardization

## What to build

Standardize `scripts/validate-skill-improvement-plan.py` to conform to the validator contract. Add `--list-codes` flag and `main(argv)` entry point. Replace free-text error messages with named error code constants (IMPROVEMENT_FILE_NOT_FOUND, MISSING_SECTION, INVALID_FAILURE_MODE_CLASS, INVALID_DEFECT_SOURCE, MISSING_SOURCE_REPORT, SOURCE_REPORT_NOT_FOUND, ABSOLUTE_SOURCE_REPORT_PATH, MISSING_EVIDENCE_SNIPPET, INVALID_RECOMMENDED_ACTION, MISSING_EDIT_TYPE, MISSING_RISK_LEVEL, MISSING_ANTI_OVERFITTING, MISSING_RERUN_SCENARIO, MISSING_SUCCESS_CRITERIA, ABSOLUTE_PATH_DETECTED). Change output format to `ERROR {CODE}: {message}`. Normalize positional argument name from `plan_path` to `artifact_path`.

Update its fixture files to reference stable error codes in `expected_error_contains`.

## Acceptance criteria

- [ ] `--list-codes` prints all stable error codes and exits 0
- [ ] `main(argv)` entry point callable programmatically
- [ ] Error output uses `ERROR {CODE}: {message}` format
- [ ] Negative fixture `expected_error_contains` values reference stable codes
- [ ] `python scripts/test-validators.py` passes

## Blocked by

- #3 — shared utility module
