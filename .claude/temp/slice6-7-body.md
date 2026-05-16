## Parent

#2 — Validator Ecosystem Standardization

## What to build

Clean up `scripts/test-validators.py` by removing the hardcoded script-name special case on line 35-36. This check was needed because `validate-usage-research-report.py` lacked `--repo-root`. Now that it has the flag, always pass `--repo-root` to every validator uniformly.

Create `scripts/validate-prompt-handoff.py`, a specialized Level 3 validator for `prompt_handoff` artifacts. Checks:
- Required sections present (target_skill, context_to_preserve, task, constraints, inputs, expected_output, stop_condition, ready_to_copy_prompt)
- Target skill exists in `skill-registry.yaml` (error code: UNKNOWN_TARGET_SKILL)
- Stop condition has substantive content (EMPTY_STOP_CONDITION)
- Expected output is populated (EMPTY_EXPECTED_OUTPUT)
- Artifact references exist in `artifact-contracts.yaml` (HALLUCINATED_ARTIFACT_REF)
- No absolute file paths (ABSOLUTE_PATH_DETECTED)
- Ready-to-copy prompt block is non-empty (MISSING_READY_PROMPT)

Create fixture directory `tests/fixtures/validate-prompt-handoff/` with 1 valid and 5 invalid fixtures. Register the validator in `artifact-contracts.yaml` under the `prompt_handoff` artifact entry. Add a regression entry to `tests/fixtures/REGRESSIONS.yaml`.

## Acceptance criteria

- [ ] Hardcoded script-name check removed from `test-validators.py`
- [ ] `scripts/validate-prompt-handoff.py` exists with standard CLI
- [ ] Validator registered in `artifact-contracts.yaml` for `prompt_handoff` artifact
- [ ] Fixture directory exists with valid + 5 invalid fixtures
- [ ] Regression entry added to `REGRESSIONS.yaml`
- [ ] All 7 error codes have corresponding negative fixtures
- [ ] `python scripts/test-validators.py` passes
- [ ] `python scripts/validate-repo.py` passes

## Blocked by

- Slice 1 (shared utility module)
- Slice 2 (test harness cleanup depends on all validators having uniform --repo-root)
