## Parent

#2 — Validator Ecosystem Standardization

## What to build

Standardize `scripts/validate-usage-research-report.py` to conform to the validator contract. Add `--repo-root` flag (defaults to `.`), `--list-codes` flag, and `main(argv)` entry point. Replace free-text error messages with named error code constants. Change output format to `ERROR {CODE}: {message}`. Normalize positional argument name from `report_path` to `artifact_path`.

Update its fixture files in `tests/fixtures/validate-usage-research-report/` to reference stable error codes in `expected_error_contains` instead of free-text substrings.

## Acceptance criteria

- [ ] `--repo-root` flag accepted (may not be used yet -- interface uniformity)
- [ ] `--list-codes` prints all error codes and exits 0
- [ ] `main(argv)` entry point callable programmatically
- [ ] Error output uses `ERROR {CODE}: {message}` format
- [ ] Negative fixture `expected_error_contains` values reference stable codes
- [ ] `python scripts/test-validators.py` passes

## Blocked by

- #3 — shared utility module
