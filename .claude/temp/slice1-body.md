## Parent

#2 — Validator Ecosystem Standardization

## What to build

Create `scripts/_validator_utils.py` with shared functions for registry loading (workflow, skill, artifact-contracts, weakness-types), error formatting (`format_error` returning `ERROR {CODE}: {message}`), and repo-root path resolution. Pure functions only, no CLI, no side effects.

Refactor `scripts/validate-brief.py` to use this module instead of its inline `_load_weakness_types` function and inline YAML loading. No behavioral change -- same validation logic, same error codes, same CLI interface. Just the implementation shifts from inline to shared.

## Acceptance criteria

- [ ] `scripts/_validator_utils.py` exists with load functions, `format_error`, and `resolve_repo_root`
- [ ] `scripts/validate-brief.py` no longer has inline `_load_weakness_types` function
- [ ] Both validators run `--list-codes` and `--help` without errors
- [ ] `python scripts/test-validators.py` passes (all 34 tests)
- [ ] `python scripts/validate-repo.py` passes

## Blocked by

None -- can start immediately.
