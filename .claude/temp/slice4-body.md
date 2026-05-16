## Parent

#2 — Validator Ecosystem Standardization

## What to build

Standardize `scripts/validate-artifact.py` to conform to the validator contract. Refactor to use shared utility module (`load_artifact_contracts`). Add `--list-codes` flag and `main(argv)` entry point. Replace free-text error messages with named error code constants (ARTIFACT_FILE_NOT_FOUND, CONTRACTS_FILE_NOT_FOUND, CONTRACT_NOT_FOUND, ABSOLUTE_FILE_LINK, MISSING_REQUIRED_SECTION, MISSING_YAML_BLOCK, MISSING_MACHINE_FIELDS, MISSING_EVIDENCE_EXCERPTS, MISSING_EXCERPT_FIELD, ABSOLUTE_EXCERPT_PATH). Change output format to `ERROR {CODE}: {message}`.

Update its fixture files in `tests/fixtures/validate-artifact/` to reference stable error codes.

Note: `validate-artifact.py` keeps its two-positional signature (`artifact_id` + `artifact_path`) -- it is the exception documented in the architecture.

## Acceptance criteria

- [ ] Uses shared `load_artifact_contracts` from `_validator_utils.py`
- [ ] `--list-codes` prints all stable error codes and exits 0
- [ ] `main(argv)` entry point callable programmatically
- [ ] Error output uses `ERROR {CODE}: {message}` format
- [ ] Negative fixture `expected_error_contains` values reference stable codes
- [ ] `python scripts/test-validators.py` passes

## Blocked by

- #3 — shared utility module
