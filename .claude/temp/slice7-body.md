## Parent

#2 — Validator Ecosystem Standardization

## What to build

Create `scripts/validate-prompt-handoff.py`, a specialized Level 3 validator for `prompt_handoff` artifacts. This is the terminal artifact in 10 of 11 workflows, consumed by `external_agent` -- no human review before execution.

Checks:
- Required sections present (target_skill, context_to_preserve, task, constraints, inputs, expected_output, stop_condition, ready_to_copy_prompt)
- Target skill exists in `skill-registry.yaml` (error code: UNKNOWN_TARGET_SKILL)
- Stop condition has substantive content (EMPTY_STOP_CONDITION)
- Expected output is populated (EMPTY_EXPECTED_OUTPUT)
- Artifact references exist in `artifact-contracts.yaml` (HALLUCINATED_ARTIFACT_REF)
- No absolute file paths (ABSOLUTE_PATH_DETECTED)
- Ready-to-copy prompt block is non-empty (MISSING_READY_PROMPT)

Create fixture directory `tests/fixtures/validate-prompt-handoff/` with 1 valid and 5 invalid fixtures (one per unique error condition). Register the validator in `artifact-contracts.yaml` under the `prompt_handoff` artifact entry. Add a regression entry to `tests/fixtures/REGRESSIONS.yaml`.

## Acceptance criteria

- [ ] `scripts/validate-prompt-handoff.py` exists with standard CLI (`artifact_path`, `--repo-root`, `--list-codes`)
- [ ] Uses shared utility module for registry loading
- [ ] Stable error codes match the 7 checks described above
- [ ] Validator registered in `artifact-contracts.yaml` for `prompt_handoff` artifact
- [ ] Fixture directory exists with 1 valid + 5 invalid fixtures
- [ ] Regression entry added to `REGRESSIONS.yaml`
- [ ] `python scripts/test-validators.py` passes
- [ ] `python scripts/validate-repo.py` passes

## Blocked by

- #3 — shared utility module
