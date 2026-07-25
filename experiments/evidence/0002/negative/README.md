# Negative-path attempt — run 0002

## What was intended

Phase 5 of the remediation protocol asked for a fresh, isolated session
against a disposable target, deliberately never creating `proposed_direction.md`,
to prove that: architectural-review is never invoked; the failure occurs at
input resolution (the `ARTIFACT_NOT_FOUND` / "requires 'proposed_direction'"
check at `scripts/workflow-runtime.py` lines 856-864); the error is explicit;
the run log records it; no recommendation is produced; the target is
unchanged.

## What actually happened

The live `repo-sensemaker` skill executed (Step 1) exactly as in the positive
attempt, but its output again failed the unified validator
(`validate-and-report.py`) -- this time with a different error
(`unknown.artifact_id.missing_field: Cannot determine artifact_id from
file.`), and execution halted at Step 1 before Step 2
(architectural-review) was ever reached. See
`session/run_log_architectural-review-planning-workflow_guided_execution.md`
and `negative_stdout.txt`.

## Honest assessment

This run does NOT demonstrate the intended negative-path proof (failure at
`proposed_direction` input resolution), because Step 1 itself failed
validation before Step 2's input-resolution logic ever ran. What it DOES
demonstrate, consistently with the positive-path attempt:
- the live `claude-code` executor genuinely invokes the `repo-sensemaker`
  skill (not a stub);
- the unified validator genuinely inspects the live output and genuinely
  rejects it when it does not conform to the brief contract;
- the target repository remains unmodified in both attempts (confirmed via
  `git status --short` in the target worktree, empty in both cases);
- framework pollution is confined to the new session directory under
  `artifacts/` and the `docs/mode-coverage.yaml` run-tracking file.

The intended `proposed_direction` negative-path proof therefore remains
UNTESTED by this run and is called out explicitly, rather than claimed, in
the Phase 8 verdict.
