# Phase 6 validation summary — run 0002

- `python scripts/validate-brief.py artifacts/05-orchestration-run/repository_sensemaking_brief.md`
  -> **FAIL**, 7 errors (HALLUCINATED_WORKFLOW_ID for `docs-aligner`; 6x
  INVALID_LINE_FORMAT on excerpt citations). Matches the runtime's own
  validator rejection recorded in the positive-path run log.
- `python scripts/validate-architectural-review-recommendation.py <path>`
  -> not run: no recommendation artifact was ever produced (Step 2 never
  executed in either the positive or negative attempt, since Step 1 failed
  validation both times).
- `python scripts/test-validators.py` -> **PASS**, 66/66 (Validator Ecosystem
  baseline held; unaffected by this run's live-executor output failures).
- `python scripts/validate-repo.py` -> **PASS** ("Repo is aligned...").
- `git diff --check` -> **PASS** (exit 0, no whitespace errors).

## Target immutability

- `target-0002` (positive-path disposable checkout): `git status --short`
  empty after the run.
- `target-0002-negative` (negative-path disposable checkout): `git status
  --short` empty after the run.
Both disposable target worktrees, created via `git worktree add --detach`
outside the framework tree, were read-only for the duration of both runs.

## Framework pollution

`git status --short` in the framework worktree after both runs showed only:
- the new session directories under `artifacts/05-orchestration-run/` and
  `artifacts/06-orchestration-run/` (intentional, preserved as evidence
  under `experiments/evidence/0002/{positive,negative}/session/`);
- `docs/mode-coverage.yaml` (updated by the runtime itself, by design, as
  part of PHASE 5: UPDATE MODE COVERAGE).
No other files were touched.
