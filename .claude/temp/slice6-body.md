## Parent

#2 — Validator Ecosystem Standardization

## What to build

Clean up `scripts/test-validators.py` by removing the hardcoded script-name special case on line 35-36. This check was needed because `validate-usage-research-report.py` lacked `--repo-root`. Now that every validator uniformly accepts `--repo-root`, always pass it without special-casing.

## Acceptance criteria

- [ ] Hardcoded `validate-brief`/`validate-plan` filename check removed from test-validators.py
- [ ] All validators get `--repo-root` passed uniformly
- [ ] `python scripts/test-validators.py` passes

## Blocked by

- #4 — validate-usage-research-report standardized (last validator to gain --repo-root)
