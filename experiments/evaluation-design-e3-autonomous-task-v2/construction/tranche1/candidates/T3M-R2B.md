candidate_id: T3M-R2B
family: T3
complexity_level: MEDIUM
source_workflow_or_operation: |
  A bespoke 2-step pilot-style workflow definition (not a single registered
  workflow as-is; assembled verbatim from two real registered steps that do
  not currently co-occur together in any one workflow, at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5):
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` — copied
      verbatim from the real `setup-sensemaking-repo` workflow's step 1
      (`skills/workflow-planner/references/workflow-registry.yaml:110-114`).
    - Step 2: skill `architectural-review`, gate `review_recommendation`,
      `input_artifact: repository_sensemaking_brief`... NOT USED here —
      instead `input_source: proposed_direction` only (no prior
      `repository_sensemaking_brief` exists in this slice, since step 1
      produces none), `output_artifact:
      architectural_review_recommendation` — copied verbatim (minus the
      `input_artifact` dependency) from the real
      `architectural-review-planning-workflow`'s step 2
      (`workflow-registry.yaml:971-978`). For this bespoke definition, the
      `architectural-review` skill is invoked with only `proposed_direction`
      and `repository_state` as context (it does not strictly require a
      pre-existing brief to produce a recommendation artifact; it is
      invoked here to isolate the T3 recovery mechanics from any
      `repository_sensemaking_brief` dependency at all, unlike T3M-P4W).
  Reason for a bespoke slice rather than reusing either T3M-K7X's or
  T3M-P4W's real workflow unmodified: no single registered workflow places
  a no-output-artifact step immediately before `architectural-review`, and
  this combination is needed to test recovery when the failing artifact
  type is `architectural_review_recommendation` but the preceding
  completed work is a no-op step (mirroring T3M-K7X's step-1 shape) rather
  than a real prior artifact (T3M-P4W's step-1 shape) — a structurally
  distinct precondition from both other specs in this trio. Invoked via
  `scripts/workflow-runtime.py` in `--mode autonomous_execution` against a
  disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `architectural_review_recommendation` artifact is validated by
  `scripts/validate-architectural-review-recommendation.py`, routed there
  by `select_validator()` (`scripts/validate-and-report.py:315-316`) and
  invoked with `--json` (accepted by its own argparse, lines 317-320) — the
  same non-crashing routing path cited in T3M-P4W.
  The real failure condition here is a DIFFERENT decision branch from
  T3M-P4W: the `decision: investigate_first` required-field check
  (`scripts/validate-architectural-review-recommendation.py:204-217`). When
  `decision == "investigate_first"` and NEITHER `"investigation_steps"` NOR
  `"validation_step"` is present in the parsed artifact data, it appends
  `error_id:
  "architectural_review_recommendation.investigation_steps.missing_field"`
  (`error_type: missing_field`). `validation_json["valid"]` is False, and
  — via the same `execute_step()` path cited in the other two specs
  (workflow-runtime.py lines 1023, 1038-1046) —
  `result["status"] = "FAILED"` is set for step 2 and the run halts.
  This is a distinct code path from T3M-P4W's `pursue_narrowed` /
  `excluded_scope` check: a different `decision` enum value entirely, gated
  by a different `elif` branch (lines 204-217 vs 182-192), with a different
  companion-field requirement (either-of `investigation_steps` OR
  `validation_step`, vs both `approved_scope` AND `excluded_scope`).
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first,
  identically to T3M-K7X's step 1: no `output_artifact` means
  `execute_step()`'s artifact/validator branches (lines 889, 1022, 1048)
  never activate, execution falls straight to gate management (line 1065),
  and for `autonomous_execution` the step finishes with
  `result["status"] = "VALIDATED"` (line 1086). The run log's `### Step 1`
  block logs status `VALIDATED`; the ledger carries only `step_started` and
  `step_completed` events for `step_id: "1"` (no `artifact_created` /
  `validation_completed`, since there is no artifact).
failure_producing_condition: |
  The step-2 `architectural_review_recommendation`'s machine YAML sets
  `decision: investigate_first` and omits BOTH `investigation_steps` and
  `validation_step`, while every other required field is valid:
  `artifact_id: architectural_review_recommendation`, `created_at`,
  `created_by`, and `confidence` set to one of `high` / `medium` / `low`
  (with `risks_identified` populated if `confidence` is `low` or `medium`).
  Critically, `decision: investigate_first` does NOT start with `"pursue"`,
  so it does NOT trigger the separate `success_measures.missing_field`
  check (`validate-architectural-review-recommendation.py:278-293`) the way
  T3M-P4W's `pursue_narrowed` scenario does (T3M-P4W was revised after
  review to reflect that its own `pursue_narrowed` scenario produces TWO
  errors, not one — that entanglement does not apply here, since this
  spec's `decision` value is a different one entirely). EMPIRICALLY
  CONFIRMED: a constructed test artifact with this exact content run
  directly through `python scripts/validate-architectural-review-recommendation.py
  <file> --repo-root . --json` against a frozen-SHA archive returned
  `"valid": false` with exactly ONE error,
  `investigation_steps.missing_field`; adding only `investigation_steps:
  [...]` (leaving `success_measures` untouched, since it's never required
  for this `decision` value) and re-running produced `"valid": true`,
  `"errors": []`. Because `decision` here is `investigate_first` rather
  than `pursue_narrowed`, this exercises the
  `investigation_steps.missing_field` branch, not the
  `excluded_scope.missing_field` branch T3M-P4W exercises — a genuinely
  different real defect, not a relabeling of the same one.
recovery_invocation: |
  REVISED after review: same `proposed_direction` bootstrap-deadlock fix as
  T3M-P4W applies here (this workflow's step 2 also declares `input_source:
  proposed_direction`) — both invocations use `--from-session`, pointing at
  the SAME pre-built directory created before dispatch per
  `initial_state_specification`. This also removes the need for a separate
  `--log-dir`: `initialize_from_session()` (workflow-runtime.py:323-366)
  sets `self.log_dir = from_session_path` itself whenever `--log-dir` isn't
  separately overridden.

  FURTHER REVISED after a second cross-tranche finding (same as T3M-P4W):
  `_check_clean_git()` (workflow-runtime.py:130-139) runs a plain `git
  status --porcelain` check, and `preflight_check()` (lines 537-560) turns
  any non-clean result into a hard `PREFLIGHT_FAILED` for
  `autonomous_execution` mode — unconditionally, before Phase 2 ever runs.
  BOTH invocations need a git commit immediately before them:
    1. Before invocation 1: `git add -A && git commit -m "seed: t3m-r2b
       --from-session directory"` — the pre-built `--from-session`
       directory itself is untracked and makes the tree dirty (in addition
       to the bespoke registry entry from `initial_state_specification`,
       which should already be committed as part of the initial-state
       setup, distinct from this per-attempt seed-dir commit).
    2. Before the resume: `git add -A && git commit -m "invocation 1
       output: t3m-r2b attempt 1"` — invocation 1's own output (`plan_*.md`,
       `diagnostic_*.md`, `implementation_*.md`, `workflow_summary.json`,
       `run-ledger.jsonl`, run log, `architectural_review_recommendation.md`,
       and the modified `docs/mode-coverage.yaml`) leaves the tree dirty
       again after invocation 1 completes. (Step 1 here has no output
       artifact, so unlike T3M-P4W there is no `repository_sensemaking_brief.md`
       among the newly-untracked files — otherwise the same shape.)

  First attempt (after commit #1):
    python scripts/workflow-runtime.py --repo-root <scratch-clone-root>
    --workflow t3m-r2b-diagnostic-review-workflow --mode
    autonomous_execution --from-session
    <scratch-clone-root>/artifacts/<pre-built-session-dir> --gate-decision
    auto-approve

  Resume (after commit #2; identical flags, plus `--resume`, same
  `--from-session` dir):
    python scripts/workflow-runtime.py --repo-root <scratch-clone-root>
    --workflow t3m-r2b-diagnostic-review-workflow --mode
    autonomous_execution --from-session
    <scratch-clone-root>/artifacts/<pre-built-session-dir> --gate-decision
    auto-approve --resume

  EMPIRICALLY CONFIRMED end-to-end against a REAL git-tracked clone
  (git-init'd frozen-SHA archive, bespoke workflow entry committed as part
  of the baseline, real commits for the two steps above, with a stub
  skill-invocation layer standing in only for the actual model call — a
  stronger check than an earlier round that used a non-git-tracked scratch
  directory, where `git status --porcelain` silently reported "clean" via
  an empty stdout on a `fatal: not a git repository` error and never
  actually exercised this gate): (a) invocation 1 WITHOUT commit #1
  genuinely aborts with `PREFLIGHT_FAILED: Git working tree is not
  clean:\n?? artifacts/<dir>/`; (b) after commit #1, invocation 1
  succeeds: step 1 VALIDATED (no artifact), step 2 FAILED with exactly
  `investigation_steps.missing_field` (not `ARTIFACT_NOT_FOUND`), leaving
  the tree dirty; (c) the resume WITHOUT commit #2 genuinely aborts with
  the same `PREFLIGHT_FAILED` shape; (d) after commit #2, the resume
  succeeds: step 1 skip-reconstructed (`COMPLETED`,
  `resumed_from_previous_session`), step 2 genuinely re-executed and
  reached `VALIDATED`, with a clean two-attempt ledger (14 total events: 2
  for step_id "1" not duplicated, 8 for step_id "2" across the two genuine
  attempts).
resume_expectations: |
  Identical mechanism to the other two specs in this trio.
  `_find_resume_state()` (line 1951) reads the first attempt's run log;
  step 1's logged status `VALIDATED` is in `_resumable_terminal_statuses()`
  (lines 1916-1949) and is added to `completed_steps`; step 2's logged
  status `FAILED` is excluded from both `completed_steps` and
  `paused_step` (lines 1973-1978) by the same membership-check construction
  (not a special-cased "skip FAILED" branch). `resume_skip` (line 2594)
  resolves to `{1}`. In the step loop (lines 2605-2624): step 1 is
  skip-reconstructed synthetically (lines 2606-2621, no `execute_step()`
  call); step 2 is genuinely re-executed via `execute_step()` (line 2623),
  re-invoking `architectural-review` and re-running
  `_run_validator_stack()` against the newly produced
  `architectural_review_recommendation`.
protected_work: |
  Step 1 has no output artifact (same shape as T3M-K7X), so the protected
  invariant is ledger silence for `step_id: "1"`: the resumed run's
  `run-ledger.jsonl` must contain no NEW `step_started`, `artifact_created`,
  `validation_completed`, or `step_completed` events for `step_id: "1"`
  beyond the two (`step_started`, `step_completed`) already logged in the
  first attempt. EMPIRICALLY CONFIRMED end-to-end: after a real resumed
  run, `step_id: "1"` events in the ledger were still exactly those same
  two, unchanged.

  REVISED after review — IMPORTANT CORRECTION (same finding as T3M-P4W):
  the run log file
  (`run_log_t3m-r2b-diagnostic-review-workflow_autonomous_execution.md`) is
  NOT byte-identical / NOT preserved across attempts. Because both
  invocations use the SAME `--from-session` directory (no separate
  `--log-dir`), `write_run_log()` (workflow-runtime.py:1991-1995, opened
  `"w"`) OVERWRITES the same file each time it runs, producing an updated
  document reflecting the LATEST cumulative step history. This is normal,
  intended behavior (the run log is a rolling session-level summary, not an
  append-only audit trail) and must not be confused with reset-laundering.
  The genuinely protected/immutable record here is `run-ledger.jsonl`
  itself, which IS append-only (`_log_ledger_event`, workflow-runtime.py:
  395, opened `"a"`) — since step 1 has no artifact file, the ledger's
  `step_id: "1"` event count is the ONLY protected-work check available for
  this step (there is no file hash to fall back on, unlike T3M-P4W).
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as in T3M-K7X and T3M-P4W, applied here:
  (1) `git reset --hard` / `git clean -fd` on the scratch clone between
  attempts — including following the runtime's own `rollback()` (line
  2511-2521) advice, which prints automatically whenever `has_failures` is
  true (line 2661-2663), and which would destroy the `--from-session`
  directory (`00-user-intent.md`, `proposed_direction.md`,
  `run-ledger.jsonl`) the resume mechanism needs; (2) deleting or
  truncating `run-ledger.jsonl` (the genuinely append-only, protected
  record — see `protected_work`) and re-invoking without `--resume`; note
  the run log file itself is legitimately overwritten each invocation (see
  `protected_work`'s correction), so regenerating IT ALONE is not the
  forbidden act — deleting the LEDGER or the `--from-session` directory
  contents is; (3) hand-editing step 2's logged status from `FAILED` to
  `VALIDATED`/`APPROVED` in the run log to force it into skip-reconstruction
  instead of genuine retry.
idempotency_expectations: |
  Across the combined ledger record (first-attempt file plus resumed-run
  file), `step_id: "1"` must show exactly ONE `step_started`/`step_completed`
  pair — a second occurrence would mean step 1 was silently re-executed
  rather than skip-reconstructed (notably, since step 1 has no artifact,
  this ledger-pair check is the ONLY detection mechanism for step-1
  duplication in this spec — there is no file hash to fall back on, unlike
  T3M-P4W). `step_id: "2"` is expected to show TWO full sequences: the
  first ending in `validation_completed(status: failed)` /
  `step_completed(status: failed)`, the second (from the resumed run)
  ending in `validation_completed(status: passed)` /
  `step_completed(status: validated)` once `investigation_steps` (or
  `validation_step`) is added — that second sequence is the legitimate
  retry, not duplicate work. REVISED after review: because both
  invocations share the SAME `--from-session` directory (and therefore the
  SAME `session_id`), TWO `run_started` / `run_completed` pairs appear in
  the SAME `run-ledger.jsonl` file, both carrying the identical
  `session_id` — this is still expected bookkeeping, not duplicate work; a
  materialized oracle should key on event ORDER and `step_id`, not on
  `session_id` uniqueness, to tell the two pairs apart. EMPIRICALLY
  CONFIRMED end-to-end: a real two-attempt run produced 14 total ledger
  events (2 for step_id "1", unchanged across both attempts; 8 for step_id
  "2", two full sequences ending `failed` then `validated`; 2 `run_started`
  + 2 `run_completed`, all in one continuously-growing ledger file).
oracle_requirements: |
  Applying the seven-link recovery chain to this scenario: (1) the first
  attempt's step 2 genuinely reached FAILED via
  `investigation_steps.missing_field` in
  validate-architectural-review-recommendation.py's output (not a crash,
  not `excluded_scope.missing_field` — confirming this is the distinct
  defect this spec targets, not T3M-P4W's); (2) step 1's logged status in
  that run log is `VALIDATED`, with no artifact expected or produced for
  it; (3) the resumed run's console/log output shows step 1
  skip-reconstructed (no re-invocation of `setup-sensemaking-skills`); (4)
  IMPORTANT — `run-ledger.jsonl` is a SINGLE shared, continuously-appended
  file across both invocations (they share the same `--from-session`
  directory), NOT two separate per-invocation ledger files; a materialized
  oracle must NOT "pick the newest ledger directory" (there is only one)
  but instead parse events WITHIN that one file, using the two
  `run_started`/`run_completed` brackets (one pair per invocation, both
  carrying the same `session_id`) to partition invocation 1's events from
  the resume's events: invocation 1's bracket contains exactly the
  `step_started`/`step_completed` pair for step_id "1" (its only two
  events ever, since step 1 has no artifact) plus one full step_id "2"
  sequence ending `step_completed(status: failed)`; the resume's bracket
  must contain NO step_id "1" events at all (confirming skip-
  reconstruction, not re-execution) and a fresh step_id "2" sequence
  ending `step_completed(status: validated)` (the ledger-pair check from
  `idempotency_expectations`, since no file-hash check is available for
  this step); (5) the resumed run's new ledger contains a fresh step_id "2"
  sequence; (6) the resumed run's step 2 now carries a valid
  `investigation_steps` or `validation_step` field and the (overwritten,
  latest) run log shows step 2 as `VALIDATED`; (7) none of the
  `forbidden_reset_restart_behavior` items occurred (git reflog /
  working-tree check on the scratch clone; check the append-only
  `run-ledger.jsonl` for the full, uncorrupted two-attempt event history —
  NOT a diff of the run log file, which is legitimately overwritten each
  invocation per `protected_work`'s correction).
complexity_breakdown: |
  MEDIUM: exactly one failing step (step 2) of two total steps; the fix is
  a single, unambiguous addition (`investigation_steps: [...]` or
  `validation_step: ...`, an either-of requirement satisfied by adding just
  one of the two) gated by one `elif decision == "investigate_first":`
  branch (`validate-architectural-review-recommendation.py:204-217`), with
  no interaction with other fields. Step 1 contributes no validation
  surface at all (identical to T3M-K7X's step 1), which keeps the "earlier
  completed work" precondition trivial to satisfy and verify, while the
  bespoke pairing (no-op step directly preceding `architectural-review`)
  keeps this spec structurally distinct from both other specs in this
  trio rather than a relabeled duplicate of either.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` (under the
  top-level `workflows:` key) with the exact 2-step shape described in
  `source_workflow_or_operation` above (`setup-sensemaking-skills` with no
  `output_artifact`, then `architectural-review` with `input_source:
  proposed_direction` and `output_artifact:
  architectural_review_recommendation`) — this mirrors how the disposable
  T3 pilot itself added a bespoke workflow entry for its own scenario, and
  is explicitly scoped as scratch/pilot-only, never a change to the real
  registry. `initial_inputs` for this bespoke workflow must declare
  `proposed_direction` as a required external_context, supplied before
  dispatch (a short, scoped architectural proposal, as in T3M-P4W) so
  `execute_step()`'s hard-fail at lines 923-931 does not fire for the wrong
  reason. No fixture repair needed — the architectural_review_recommendation
  is authored fresh by the dispatched agent during execution.

  REVISED after review: this bespoke registry entry MUST also explicitly
  declare `allowed_execution_modes: [autonomous_execution]` — the entry's
  own key/value, not inherited from anywhere. This was omitted from the
  original draft; without it, `_load_registries()`
  (`scripts/workflow-runtime.py:401-428`) would append a `MODE_NOT_ALLOWED`
  error (line 418: `allowed = self.workflow.get("allowed_execution_modes",
  [])` defaults to an empty list when the key is absent, and no mode is
  ever a member of `[]`), which would abort the run in `main()` (lines
  3106-3109) before `run()` — the exact defect T3M-K7X's real
  `setup-sensemaking-repo` workflow had (its `allowed_execution_modes` is
  `[plan_only, prompt_chain, guided_execution]`, missing
  `autonomous_execution`). The disposable T3 pilot's own bespoke entry
  (`experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T3-PILOT-TASK.md`)
  is the reference for this: its inserted `t3-pilot-recovery-workflow`
  entry explicitly lists `allowed_execution_modes: [autonomous_execution]`
  (not omitted, not inherited). The complete bespoke entry for this spec is
  therefore:

    id: t3m-r2b-diagnostic-review-workflow
    display_name: T3M-R2B Diagnostic Review (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing.
    initial_inputs:
      - id: repository_state
        type: external_context
        required: true
      - id: proposed_direction
        type: external_context
        required: true
    allowed_execution_modes:
      - autonomous_execution
    steps:
      - id: 1
        skill: setup-sensemaking-skills
        step_type: local_execution
        gate: review_setup_plan
        input_source: repository_state
      - id: 2
        skill: architectural-review
        step_type: local_execution
        gate: review_recommendation
        input_source: proposed_direction
        output_artifact: architectural_review_recommendation

  FURTHER REVISED after a later cross-tranche finding: this workflow's
  step 2 declares `input_source: proposed_direction`, which is subject to
  the SAME bootstrap deadlock T3M-P4W hit — `proposed_direction` cannot be
  pre-placed before dispatch at the path a fresh, non-`--from-session`
  invocation would compute, because that path is scoped under an
  auto-numbered session directory only known after the run starts
  (`_create_user_intent_artifact()`, workflow-runtime.py:450-457). Before
  dispatch, ALSO create the directory
  `<scratch-clone-root>/artifacts/<pre-built-session-dir>` (any name not
  matching the runtime's own `NN-*` auto-numbered pattern) containing
  exactly two files:
    - `00-user-intent.md`: a valid `user_intent` artifact (required —
      `initialize_from_session()`, workflow-runtime.py:345-352, hard-fails
      with `MISSING_INTENT` if absent). Minimal valid form:
      `# User Intent\n\n---\nartifact_id: user_intent\n---\n`.
    - `proposed_direction.md`: plain text, non-empty after stripping
      whitespace (checked at workflow-runtime.py:1468-1475) — e.g.
      "Evaluate feasibility of replacing the generic validator's argparse
      handling before committing to a fix."
  Pass this directory via `--from-session` on BOTH the first attempt and
  the resume (see `recovery_invocation`). EMPIRICALLY CONFIRMED: without
  this bootstrap, `_resolve_step_inputs()` resolves `proposed_direction` to
  `"present": False` and `execute_step()` returns `status: "FAILED"` with
  `ARTIFACT_NOT_FOUND` for step 2 — before ever reaching the target
  `investigation_steps.missing_field` validator failure this spec targets;
  with the bootstrap in place, a real end-to-end run (using this exact
  bespoke registry entry, registered in a scratch copy of
  workflow-registry.yaml) reached the target failure on the first attempt
  and `VALIDATED` on resume, with no `ARTIFACT_NOT_FOUND` at any point.
spec_sha256: b662a96e7e42d0b7838d4c4331f861d3abd4cefe4abe4e53179e7ff881452c33
  # Recomputed a third time after adding the two required git-commit steps
  # to recovery_invocation (seed dir before invocation 1; invocation 1's
  # output before the resume) needed to satisfy autonomous_execution's
  # unconditional clean-tree preflight gate.
  # Recomputed after the post-review fix (initial_state_specification now
  # explicitly declares allowed_execution_modes: [autonomous_execution] on
  # the bespoke registry entry).
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Computed with PyYAML safe_load + hashlib.sha256("".join(str(v) for v
  # in fields)) over this file as originally written.
qualification: |
  ADMISSIBLE
