candidate_id: T3M-C5N
family: T3
complexity_level: MEDIUM
source_workflow_or_operation: |
  The real, registered workflow `architectural-review-planning-workflow`,
  used UNMODIFIED (no bespoke restructuring needed), defined at
  `skills/workflow-planner/references/workflow-registry.yaml:942-979` at
  frozen SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5:
    - `allowed_execution_modes` (registry lines 958-962): `[plan_only,
      prompt_chain, guided_execution, autonomous_execution]` -- CONFIRMED
      by direct re-inspection of the frozen-SHA registry entry as part of
      this construction task: `autonomous_execution` IS present, so no
      bespoke workflow entry is required here, unlike this family's
      brief-only bespoke specs (T3M-K7X, T3M-H4Q, T3M-L8R, T3H-Q8N,
      T3H-Z1V), all of which needed a bespoke `allowed_execution_modes`
      addition because `setup-sensemaking-repo` lacks
      `autonomous_execution`.
    - Step 1 (registry lines 964-970): skill `repo-sensemaker`, gate
      `review_diagnosis`, `input_source: repository_state`,
      `output_artifact: repository_sensemaking_brief`.
    - Step 2 (registry lines 971-978): skill `architectural-review`, gate
      `review_recommendation`, `input_artifact:
      repository_sensemaking_brief`, `input_source: proposed_direction`,
      `output_artifact: architectural_review_recommendation`.
  This is the same real, unmodified workflow this family's T3M-P4W already
  uses (T3M-R2B instead uses a bespoke variant of a similar shape). What
  makes this spec a genuinely different scenario from T3M-P4W is an
  entirely different `decision` value
  and an entirely different validator code branch (see
  `verified_failed_boundary`): the `defer`/`reject` required-field check,
  never exercised by T3M-P4W (`pursue_narrowed`) or T3M-R2B
  (`investigate_first`).
  `initial_inputs` (registry lines 948-957) require both `repository_state`
  and `proposed_direction` (an external_context, not an artifact) --
  `proposed_direction` must be bootstrapped via `--from-session <dir>`
  pointing at a directory built ahead of time (see
  `initial_state_specification` and `recovery_invocation`) or step 2
  hard-fails for the WRONG reason before it ever reaches validation
  (`execute_step()`'s hard-fail at lines 923-931).

  REVISED after review (a real defect was found and empirically fixed
  during this construction task): a plain CLI invocation with no
  `--from-session` cannot work at all for this workflow, regardless of how
  `proposed_direction` content is described as "supplied". EMPIRICALLY
  CONFIRMED by direct re-run in a disposable scratch clone at the frozen
  SHA: `_create_user_intent_artifact()`
  (`scripts/workflow-runtime.py:450-457`) computes the session directory
  name by globbing existing `artifacts/[0-9][0-9]-*` directories and taking
  `max + 1` -- a number only knowable AFTER the run has already started
  creating it. `_resolve_artifact_path("proposed_direction")` /
  `_scope_to_session_dir()` (lines 1487-1532) resolve `proposed_direction`'s
  path to `<that same session directory>/proposed_direction.md`. There is
  no way to pre-place content at that path before a fresh invocation
  begins, because the directory does not exist yet and its name cannot be
  predicted. The actual working mechanism, confirmed by running it for
  real: `--from-session <pre-built-dir>`, which reuses a directory the
  operator creates and names themselves (`initialize_from_session()`, lines
  323-366) instead of letting the runtime auto-generate one. This same
  bootstrap mechanism is used for BOTH invocations of this spec's two-step
  recovery sequence, pointing at the identical pre-built directory both
  times (not a fresh one per invocation) -- see `recovery_invocation` for
  why this is required, not merely convenient. Invoked via
  `scripts/workflow-runtime.py` in `--mode autonomous_execution` against a
  disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `architectural_review_recommendation` artifact is validated by
  `scripts/validate-architectural-review-recommendation.py`, routed there
  (not the generic `--json`-crashing `validate-artifact.py`) by
  `select_validator()` (`scripts/validate-and-report.py:315-316`, which
  special-cases `artifact_id == "architectural_review_recommendation"`).
  `invoke_validator()` calls it as `[artifact_path, --repo-root, --json]`;
  this validator's own argparse defines `--json`, so the call does not
  crash.
  The real failure condition is the `decision in ("defer", "reject")`
  branch (`scripts/validate-architectural-review-recommendation.py:219-229`):
  once `decision` is confirmed to be one of the five allowed enum values
  (`pursue`, `pursue_narrowed`, `investigate_first`, `defer`, `reject`;
  lines 168-179), and specifically equals `"defer"` or `"reject"`, the
  validator checks `if "reversal_conditions" not in artifact_data or not
  artifact_data["reversal_conditions"]:` and, if true, appends
  `error_id: "architectural_review_recommendation.reversal_conditions.missing_field"`
  (`error_type: missing_field`). This is a THIRD, distinct decision-branch
  code path in the same `if/elif/elif` chain this family's T3M-P4W
  (`pursue_narrowed` -> lines 182-202, `excluded_scope` AND
  `success_measures`) and T3M-R2B (`investigate_first` -> lines 204-217,
  `investigation_steps` OR `validation_step`) already exercise -- a
  genuinely different `decision` value gated by a genuinely different
  branch, with a different companion-field requirement, and (unlike
  T3M-P4W's `pursue_narrowed`, which ALSO triggers the separate
  `decision.startswith("pursue")` `success_measures` check at lines
  278-293) `defer`/`reject` do NOT start with `"pursue"`, so this branch
  fires ALONE, with no risk of the two-errors-bundled-together pitfall
  T3M-P4W's own post-review correction had to fix. `validation_json["valid"]`
  becomes False via the same `execute_step()` / `_run_validator_stack()` /
  `_run_validate_and_report()` chain cited throughout this family
  (`scripts/workflow-runtime.py` lines 1023, 1038-1046), and
  `result["status"] = "FAILED"` is set for step 2, halting the run (`run()`
  lines 2626-2631).

  EMPIRICALLY CONFIRMED (direct validator invocation, this construction
  session, frozen-SHA archive extracted from `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`): a constructed
  `architectural_review_recommendation` with `decision: reject`,
  `confidence: high` (so the separate `risks_identified.logic_error` check
  at lines 260-276, which only applies when `confidence` is `low`/`medium`,
  cannot fire), `artifact_id`, `created_at`, `created_by` all present, and
  `reversal_conditions` OMITTED entirely, run through `python
  scripts/validate-architectural-review-recommendation.py <file>
  --repo-root . --json`, produced exactly one error:
  `architectural_review_recommendation.reversal_conditions.missing_field:
  Decision 'reject' requires 'reversal_conditions' to define when this
  decision could change.` (`valid: false`). The IDENTICAL artifact with
  `decision: defer` (the other member of this branch) and
  `reversal_conditions` still omitted produced the same single error with
  `defer` substituted for `reject` in the message text -- confirming the
  branch is genuinely shared by both enum values, as the code's `elif
  decision in ("defer", "reject"):` (line 219) states. The IDENTICAL
  `decision: reject` artifact with `reversal_conditions:
  ["New evidence of demand emerges"]` added (nothing else changed) produced
  `valid: true`, zero errors -- confirming the isolation: this is the ONLY
  error the omission produces, not one of several firing together (the
  exact failure mode T3M-P4W's own post-review correction warns must be
  checked for empirically, not assumed).
pre_failure_completed_work_expectations: |
  Step 1 (`repo-sensemaker`) must complete and genuinely VALIDATE first.
  Its `repository_sensemaking_brief` output -- placed at its
  `--from-session`-scoped resolved path
  (`<from-session-dir>/repository_sensemaking_brief.md`) as initial state,
  via the same dry-run-executor pre-placement mechanism
  `failure_producing_condition` documents for step 2 -- must satisfy
  validate-brief.py in full: `primary_fog_type` a valid enum value,
  `evidence` non-empty with a real file-level citation,
  `recommended_workflow_id` a value that DOES exist in the registry (e.g.
  `architecture-implementation-workflow`), and a well-formed,
  correctly-grounded `evidence_excerpts` block (so none of this family's
  brief-side failures -- T3M-K7X's, T3H-Z1V's, T3M-H4Q's, or T3M-L8R's --
  accidentally fire here instead of the target ARR failure). With all
  validators passing, `execute_step()` (line 1038) finds `v_failures`
  empty, proceeds to gate management (line 1065), and for
  `autonomous_execution` sets `result["status"] = "VALIDATED"` (line 1086).
  The run log's `### Step 1` block logs status `VALIDATED`, and the
  first-attempt segment of the ledger carries a full
  `step_started`/`artifact_created`(with the file's content hash, line
  1018)/`validation_completed`(`status: "passed"`, line 1034)/
  `step_completed` sequence for `step_id: "1"`.
  EMPIRICALLY CONFIRMED via a full live `OrchestrationRunner` run against
  this exact setup (frozen-SHA archive extracted from `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`, this spec's actual
  `recovery_invocation`): step 1's ledger entry recorded exactly
  `step_started` / `artifact_created` (content hash
  `aa7f62fe497c94b96d6c66cdecbe063f302f4076c1a061499bfacf6f6e9f89da`) /
  `validation_completed(status: passed)` / `step_completed(status:
  validated, gate_status: automated_approval)` -- before step 2 genuinely
  failed with `reversal_conditions.missing_field`.
failure_producing_condition: |
  REVISED after review: the step-2 `architectural_review_recommendation`
  is placed as INITIAL STATE, directly at its session-scoped resolved path
  inside the pre-built `--from-session` directory
  (`<from-session-dir>/architectural_review_recommendation.md`), not
  asserted to be organically produced by a live-dispatched
  `architectural-review` invocation. This is not merely a cautious framing
  choice (per the standing lesson that a scenario needing specific wrong
  content should say so plainly) -- it is also the ONLY way this spec was
  actually exercised end to end during construction, and it works because
  of a real, empirically-confirmed mechanism: with `--executor dry-run`,
  `DryRunSkillExecutor.supports_real_execution` is `False`
  (`scripts/skill_executor.py:1411`), so `execute_step()`'s real-execution
  branch (line 915) is never taken regardless of `output_artifact`; it
  always falls through to the `if not is_fixture:` branch (line 996),
  which resolves the artifact's session-scoped contract path and then
  simply checks `os.path.exists(artifact_path)` (line 1022) -- if a file
  already exists there (because it was placed there as part of this
  spec's initial state, using the SAME `--from-session` directory that
  makes the path deterministic and known in advance), it is read and
  validated exactly as if a skill had just produced it, with no branch in
  the code that distinguishes the two. This is the identical
  session-scoped-pre-placement technique this family's T3H-W4J already
  documents using for this same artifact type (T3H-W4J: "this spec's own
  verification instead placed it directly at its session-scoped resolved
  path via `--from-session`, EMPIRICALLY confirmed to be read and validated
  identically to a skill-produced file") -- necessary here regardless of
  fixture support, since `architectural_review_recommendation` has none
  (confirmed absent from `_get_fixture_artifact_path()`'s `skill_map`,
  `scripts/workflow-runtime.py:1365-1370`) and `--use-fixtures` therefore
  cannot apply to it at all.
  The machine YAML sets `decision: reject` (or `defer`; either exercises
  the identical branch) and OMITS `reversal_conditions` entirely, while
  every other required field is valid: `artifact_id:
  architectural_review_recommendation`, `created_at`, `created_by`, and
  `confidence: high` (deliberately NOT `low`/`medium`, so the separate
  `risks_identified.logic_error` check does not also fire and contaminate
  this spec's single-error isolation -- unlike T3M-P4W's `pursue_narrowed`
  scenario, which needed an explicit populated `risks_identified` to avoid
  exactly this). EMPIRICALLY CONFIRMED, both via direct validator
  invocation (see `verified_failed_boundary`) AND via a full live
  `OrchestrationRunner` run against this exact fixture content dispatched
  through the real orchestrator with this spec's actual
  `recovery_invocation`: this produces exactly one validator error,
  `reversal_conditions.missing_field`; adding only
  `reversal_conditions: [...]` (nothing else touched) resolves the
  artifact to `valid: true`, zero errors, and the real orchestrator's step
  2 genuinely reaches `VALIDATED` on `--resume`.
recovery_invocation: |
  REVISED after review: a real defect was found in the original draft here
  (plain CLI, no `--from-session`) and fixed. `--from-session <dir>` is
  REQUIRED for BOTH invocations below, pointing at the IDENTICAL,
  pre-built directory both times -- not a fresh one per invocation, and
  not optional. This single directory serves three roles simultaneously:
  the source of `proposed_direction.md` and (for this spec's own
  verification, per `failure_producing_condition`) the step artifacts
  themselves; the `--log-dir` `_find_resume_state()` reads from
  (`initialize_from_session()`, lines 358-364, sets `self.log_dir` to this
  same directory when no different `--log-dir` is explicitly given); and
  the directory `run-ledger.jsonl` is appended to on every invocation
  (`_log_ledger_event()`, lines 383-399, opens the ledger in the
  session directory in APPEND mode) -- see `protected_work` for why this
  produces a single, shared, two-bracket ledger file rather than two
  separate per-invocation files as elsewhere in this family.

  Directory setup (BEFORE invocation 1, committed as part of initial
  state -- see `initial_state_specification` for exact file contents):
  create `<scratch-clone-root>/artifacts/t3m-c5n-session/` containing
  `00-user-intent.md` (REQUIRED -- `initialize_from_session()`,
  `scripts/workflow-runtime.py:346-352`, hard-fails with `MISSING_INTENT`
  if absent) and `proposed_direction.md`.

  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  architectural-review-planning-workflow --mode autonomous_execution
  --executor dry-run --from-session
  <scratch-clone-root>/artifacts/t3m-c5n-session`. Ends with step 2 FAILED
  (`reversal_conditions.missing_field`).

  BEFORE `--resume`: the git working tree must be returned to clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`, and a
  completed invocation always leaves the tree dirty (the run log,
  `run-ledger.jsonl` append, diagnostic/implementation reports, and
  `workflow_summary.json` inside the from-session directory, plus a
  modified `docs/mode-coverage.yaml`). Commit this new state, THEN also
  correct `architectural_review_recommendation.md` in place (add
  `reversal_conditions: [...]`, nothing else touched) and commit that fix
  too, before `--resume` -- this is required operational hygiene for
  chaining any two invocations of this runner in a mutating mode against a
  git-backed repo root.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  architectural-review-planning-workflow --mode autonomous_execution
  --executor dry-run --from-session
  <scratch-clone-root>/artifacts/t3m-c5n-session --resume`. Same
  `--from-session` directory as invocation 1, REQUIRED again (not a
  different, freshly-numbered one): `initialize_from_session()`
  re-validates `00-user-intent.md` is present (line 346-352) and sets
  `self.log_dir` to this same directory again (lines 363-364), which is
  what lets `_find_resume_state()` (line 1956) find invocation 1's run log
  at all. `proposed_direction.md` is read from this same directory again
  during step 2's genuine re-execution (it is not itself a
  tracked/resumable workflow artifact, so it must still be present, not
  merely have been present for invocation 1).

  EMPIRICALLY CONFIRMED end to end: both invocations above were actually
  run in sequence in a disposable scratch clone (frozen-SHA archive
  extracted via `git archive 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`),
  not just predicted from source. Invocation 1 printed `[OK] Reusing
  session: artifacts/t3m-c5n-session`, step 1 `[OK] Validation passed`,
  step 2 `[FAIL] Validation failed` with
  `architectural_review_recommendation.reversal_conditions.missing_field`
  in its output, and `[WARN] Execution completed with failures.`
  Invocation 2 printed `[OK] Found resume state: 1 completed, paused at
  step None`, `[OK] Resuming: skipping steps [1], starting from step 2`,
  `~ Step 1 already completed in previous session, skipping (resume
  mode)`, step 2 `[OK] Validation passed`, and `[OK] Execution completed
  successfully.` (`workflow_summary.json`: `steps_completed: 2,
  steps_failed: 0`; the run log's own `Final State` block reads `Status:
  partial` -- the same `write_run_log()` step1-synthetic-`COMPLETED`-vs-
  step2-`VALIDATED` counting quirk this family's T3H-Z1V already
  documents; it is a cosmetic label mismatch, not a failure, and a
  materialized oracle must not misread it as one -- `steps_failed: 0` and
  exit code 0 are the authoritative signal).
resume_expectations: |
  Same mechanism as T3M-P4W, applied to this same real workflow.
  `_find_resume_state()` (line 1951) reads invocation 1's run log (found
  via `self.log_dir`, which `--from-session` set to the pre-built session
  directory); step 1's logged status `VALIDATED` is in
  `_resumable_terminal_statuses()` (`{"VALIDATED", "COMPLETED"}` for
  autonomous_execution, lines 1916-1949) and is added to `completed_steps`;
  step 2's logged status `FAILED` is in neither `completed_steps` nor
  `paused_step` (lines 1973-1978). `resume_skip` (line 2594) resolves to
  `{1}`. In the step loop (lines 2605-2624): step 1 is skip-reconstructed
  synthetically (lines 2606-2621, no `execute_step()` call); step 2 is
  genuinely re-executed via `execute_step()` (line 2623), re-reading
  `architectural_review_recommendation.md` from the same `--from-session`
  directory and re-running `_run_validator_stack()` against it. For that
  retry to reach `VALIDATED`, the corrected artifact must supply
  `reversal_conditions` (a non-empty value) while `decision` remains
  `defer` or `reject`; empirically, this single addition alone is
  sufficient (unlike T3M-P4W's `pursue_narrowed` scenario, which needs two
  independent additions).
  EMPIRICALLY CONFIRMED end to end (see `recovery_invocation`): the real
  orchestrator's resumed run printed exactly `[OK] Found resume state: 1
  completed, paused at step None`, `[OK] Resuming: skipping steps [1],
  starting from step 2`, no `[FIXTURE]`/skill-invocation line for step 1,
  and step 2 genuinely re-ran and passed.
protected_work: |
  REVISED after review: because BOTH invocations use the SAME
  `--from-session` directory (required, per `recovery_invocation` -- not a
  choice), this spec's ledger persistence shape is structurally DIFFERENT
  from every other spec in this family (T3M-K7X/H4Q/L8R/P4W/R2B/T3H-*), all
  of which get a fresh, separate, auto-incrementing numbered directory (and
  thus a fresh, separate `run-ledger.jsonl`) per invocation. Here,
  `_log_ledger_event()` (`scripts/workflow-runtime.py:383-399`) opens
  `<from-session-dir>/run-ledger.jsonl` in APPEND mode (`open(...,
  "a", ...)`, line 395) on every invocation, and because
  `self.artifact_session_dir` is the SAME fixed directory both times, there
  is exactly ONE `run-ledger.jsonl` file for this spec's entire two-
  invocation sequence, containing invocation 1's events followed by
  invocation 2's events, back to back in one file.
  EMPIRICALLY CONFIRMED: the real ledger file, read after both invocations,
  contains exactly two `run_started`/`run_completed` brackets. `step_id:
  "1"` events (`step_started`, `artifact_created`, `validation_completed`,
  `step_completed`) appear ONLY inside the FIRST bracket -- zero `step_id:
  "1"` events of any kind appear in the second bracket, confirming step 1
  was skip-reconstructed on resume, not silently re-executed into the same
  file. The step-1 `repository_sensemaking_brief.md` file itself (at its
  `--from-session`-scoped resolved path) must remain byte-identical on
  disk between the two invocations: EMPIRICALLY CONFIRMED, its SHA-256
  hash after the resumed run
  (`aa7f62fe497c94b96d6c66cdecbe063f302f4076c1a061499bfacf6f6e9f89da`)
  matched the hash recorded in the FIRST bracket's `artifact_created` event
  exactly, byte for byte.
  The run log file (also written to this same `--from-session` directory,
  since `--from-session` sets `self.log_dir` to it) is NOT a reliable
  preservation channel, exactly as elsewhere in this family:
  `write_run_log()` (line 1991) OVERWRITES it in place on every invocation.
  EMPIRICALLY CONFIRMED: after the resumed run it showed only the final
  state (step 1 `COMPLETED`, step 2 `VALIDATED`); invocation 1's `FAILED`
  record for step 2 is gone from it. The single shared `run-ledger.jsonl`
  -- read in FULL, split into its two `run_started`-delimited brackets in
  chronological order -- is the only reliable channel for any
  `protected_work`/`idempotency_expectations` claim here.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family, applied to
  this scenario: (1) `git reset --hard` / `git clean -fd` on the scratch
  clone between attempts -- including actually following the runtime's own
  `rollback()` (line 2511-2521) printed advice, which fires automatically
  whenever `has_failures` is true; this would destroy step 1's
  already-VALIDATED `repository_sensemaking_brief.md` along with the ledger
  directories the resume mechanism needs; (2) deleting/truncating
  `run_log_architectural-review-planning-workflow_autonomous_execution.md`
  or any `run-ledger.jsonl` and re-invoking without `--resume`; (3)
  hand-editing step 2's logged status from `FAILED` to
  `VALIDATED`/`APPROVED` in the run log to force it into
  skip-reconstruction instead of genuine retry. A fourth behavior specific
  to this spec's failure mode is also forbidden: switching `decision` away
  from `defer`/`reject` (e.g. to `pursue`) merely to escape the
  `reversal_conditions` requirement, rather than genuinely supplying
  `reversal_conditions` for the ORIGINAL decision -- independently
  detectable by confirming the resumed attempt's `decision` field still
  reads `defer` or `reject` (whichever the first attempt used) and that
  `reversal_conditions` is now genuinely populated, not that the artifact
  merely reached `valid: true` by changing which decision-branch applies.
  A fifth behavior specific to this spec's `--from-session` bootstrap is
  also forbidden: pointing invocation 2's `--from-session` at a
  DIFFERENT, freshly-created directory instead of the SAME one used for
  invocation 1 -- unlike `--log-dir` elsewhere in this family, there is no
  alternate valid directory to point at here; `--from-session` is not
  itself something a fresh directory can "resume" from (a fresh directory
  has no prior `00-user-intent.md`-backed session to reuse, no
  `run-ledger.jsonl` for `_find_resume_state()`'s companion run log to
  correspond to, and no pre-placed `proposed_direction.md`) -- independently
  detectable by confirming both invocations' `--from-session` argument
  values are byte-identical strings.
idempotency_expectations: |
  REVISED after review: scoped to the SINGLE shared `run-ledger.jsonl` file
  described in `protected_work` (not "invocation 1's file plus invocation
  2's file" -- there is only one file here, appended to twice). Read in
  full and split into two brackets at its two `run_started` events (in
  chronological order): `step_id: "1"` must show exactly ONE
  `step_started`/`artifact_created`/`validation_completed`(passed)/
  `step_completed` sequence, located ONLY in the FIRST bracket -- a second
  occurrence in the SECOND bracket would mean `repo-sensemaker` was
  silently re-run and `repository_sensemaking_brief.md` potentially
  re-written (violating `protected_work`'s hash-identity check). `step_id:
  "2"` is expected to show TWO sequences, one per bracket: the first
  ending in `validation_completed(status: failed)` (the genuine
  `reversal_conditions.missing_field` result) / `step_completed(status:
  failed)`, the second ending in `validation_completed(status: passed)` /
  `step_completed(status: validated)` once `reversal_conditions` is
  genuinely populated -- that second sequence is the legitimate retry, not
  duplicate work. Exactly TWO `run_started`/`run_completed` pairs in the
  one file (both carrying the SAME `run_id`, since `--from-session` reuses
  the same `session_id` both times -- unlike every other spec in this
  family, `run_id` alone cannot distinguish the two invocations here;
  bracket ORDER, via `git_commit` and timestamp, must be used instead) is
  expected bookkeeping and must not be flagged as duplicated semantic work.
  EMPIRICALLY CONFIRMED: the real ledger file showed exactly this pattern
  -- two `run_started` events (both `run_id: "t3m-c5n-session"`, distinct
  `git_commit` values), `step_id: "1"` events present only before the
  second `run_started`, `step_id: "2"` present in both brackets (first
  ending `status: failed`, second ending `status: passed` /
  `step_completed status: validated`), and the second bracket's
  `run_completed` reading `status: completed, exit_code: 0`.
oracle_requirements: |
  REVISED after review: a materialized oracle for this spec must first
  locate the SINGLE `run-ledger.jsonl` inside the known, fixed
  `--from-session` directory (`artifacts/t3m-c5n-session/` in this spec's
  own construction, or whatever name a materializer chooses -- the point
  is the directory name is a KNOWN, pre-chosen constant for this spec, not
  something to be discovered by scanning `artifacts/NN-orchestration-run/`
  numbered directories the way every other spec in this family does).
  Because this spec uses the real, unmodified
  `architectural-review-planning-workflow` (shared with T3M-P4W, which
  does NOT use `--from-session`), `workflow_id`-based filtering alone is
  NOT sufficient to distinguish this spec's own ledger from another spec's
  if multiple specs' scratch clones were ever conflated -- the fixed
  directory NAME is this spec's actual identifying signal, and a future
  materializer must choose one that cannot collide with any other spec's.
  Read the single ledger file in FULL and split it into brackets at each
  `run_started` event, in chronological order (do NOT rely on `run_id` to
  distinguish brackets -- both carry the same value here, since
  `--from-session` reuses the same `session_id` for both invocations;
  order by timestamp/`git_commit`, or simply by position, instead).
  Applying the seven-link recovery chain, using ONLY this ledger content
  (never run-log content, which reflects only the latest overwrite -- see
  `protected_work`): (1) the FIRST bracket's step 2 genuinely reached
  FAILED via `reversal_conditions.missing_field` and ONLY that error (not
  a crash, not a different error, and not bundled with anything else --
  confirming this is a single, cleanly isolated failure, distinct from
  T3M-P4W's two-errors-bundled scenario); (2) that same bracket's step 1
  is `step_completed(status: validated)`, with a real
  `repository_sensemaking_brief.md` that itself independently passes
  validate-brief.py; (3) the SECOND bracket contains ZERO `step_id: "1"`
  events of any kind (confirming skip-reconstruction, not re-execution);
  (4) step 1's artifact file hash after the resumed run matches the hash
  logged in the FIRST bracket's `artifact_created` event exactly; (5) the
  SECOND bracket contains a fresh `step_id: "2"` sequence ending
  `validated`/`passed`; (6) the resumed run's step 2 now carries a
  populated `reversal_conditions` field, with `decision` unchanged from
  the FIRST bracket's value (`defer` or `reject`), and the fixed
  `--from-session`-scoped run log, read only for its LATEST state, shows
  step 2 as `VALIDATED`; (7) none of the `forbidden_reset_restart_behavior`
  items occurred, including the decision-switching variant (compare the
  `decision` field across both brackets' step-2 artifact content and
  confirm they match) and the different-`--from-session`-directory variant
  specific to this spec (confirm both invocations' `--from-session`
  argument was byte-identical).
  Additionally specific to this revised spec: (8) confirm exactly ONE
  `run-ledger.jsonl` file exists for this spec's entire sequence (not two,
  as elsewhere in the family) -- a materializer that mistakenly gave
  invocation 2 a different `--from-session` directory would produce a
  SECOND ledger file instead of a second bracket in the same file, which
  is itself evidence of the forbidden variant in (7).
complexity_breakdown: |
  MEDIUM: exactly one failing step (step 2) of two total steps; the fix is
  a single, unambiguous field addition (`reversal_conditions: [...]`)
  gated by one `elif decision in ("defer", "reject"):` branch
  (`scripts/validate-architectural-review-recommendation.py:219-229`), with
  no interaction with any other field and no risk of a second,
  independently-firing error bundled into the same validator-stack entry
  (unlike T3M-P4W's `pursue_narrowed` scenario, which required two
  independent additions because `decision.startswith("pursue")` triggers a
  SEPARATE `success_measures` check). This is, if anything, a strictly
  simpler single-field-addition MEDIUM case than T3M-P4W within the same
  validator, and a genuinely different decision-branch/companion-field
  pairing than both T3M-P4W (`pursue_narrowed` / `excluded_scope` +
  `success_measures`) and T3M-R2B (`investigate_first` /
  `investigation_steps` or `validation_step`). Step 1 is a real,
  already-validating artifact type (not a no-op step), matching T3M-P4W's
  shape rather than T3M-R2B's or this family's brief-only bespoke specs.
  The `--from-session` bootstrap this spec requires (see
  `recovery_invocation`) is an operational PRECONDITION, not additional
  workflow complexity in the MEDIUM-vs-HIGH sense used elsewhere in this
  family (step count, number of independently-firing errors, or
  multi-layer validator logic) -- it does not add a step, does not change
  the single-error isolation, and does not require the recovering agent to
  reason about anything beyond "supply this one input at a known path and
  reuse it for both invocations." T3M-P4W and T3M-R2B share this same
  precondition (their own `initial_state_specification`s independently
  need the same fix, per this task's own review).
initial_state_specification: |
  REVISED after review: a disposable scratch clone of the repo at frozen
  SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS a
  pre-built `--from-session` bootstrap directory committed as part of
  initial state (required, not optional -- see `source_workflow_or_operation`
  and `recovery_invocation` for why a plain CLI invocation cannot work at
  all for this workflow). `workflow-registry.yaml` must be left unmodified
  from the frozen SHA -- no scratch-registry addition is needed, since the
  real `architectural-review-planning-workflow` already declares
  `autonomous_execution` in its own `allowed_execution_modes` (registry
  lines 958-962).

  Create `artifacts/t3m-c5n-session/` (any name not colliding with an
  existing `artifacts/[0-9][0-9]-*` numbered directory works; this exact
  name is what this spec's own construction used and was empirically
  verified against) containing exactly these files, committed before
  invocation 1:

    `artifacts/t3m-c5n-session/00-user-intent.md` -- REQUIRED
    (`initialize_from_session()`, `scripts/workflow-runtime.py:346-352`,
    hard-fails with `MISSING_INTENT` if absent). Content must match the
    exact YAML shape `_create_user_intent_artifact()` itself writes
    (lines 435-448), so a real, non-`--from-session` run's own intent
    artifact and this pre-built one are structurally identical:

      # User Intent

      ---
      artifact_id: user_intent
      schema_version: 1
      intent_source: user_problem_statement
      scope_mode: soft
      raw_problem_statement: <the same problem statement passed on the
        command line for both invocations>
      immutable: true
      created_at: '<timestamp>'
      created_by: orchestration-runner
      repo_state_used: true
      constraints: []
      non_goals: []
      clarifications: []
      ---

    `artifacts/t3m-c5n-session/proposed_direction.md` -- a short, scoped
    architectural proposal for the `architectural-review` step to
    evaluate (e.g. "add response caching to the validator dispatcher"),
    non-empty content (`_resolve_step_inputs()`'s `proposed_direction`
    check at lines 1466-1480 only requires `bool(f.read().strip())`, not
    that it pass any validator -- it is never itself run through
    `_run_validator_stack()`, only step 1's/step 2's OWN output artifacts
    are). Without this file present and non-empty, `execute_step()`'s
    hard-fail at lines 923-931 (`"proposed_direction" in resolved_inputs
    and not resolved_inputs["proposed_direction"].get("present")`) would
    produce a FAILED step 2 for the WRONG reason (`ARTIFACT_NOT_FOUND`,
    not a validator content failure), contaminating the scenario.

    `artifacts/t3m-c5n-session/repository_sensemaking_brief.md` --
    step 1's output, placed directly at its session-scoped resolved path
    (per `pre_failure_completed_work_expectations`), a fully valid brief
    satisfying validate-brief.py in full.

    `artifacts/t3m-c5n-session/architectural_review_recommendation.md` --
    step 2's output for invocation 1 (per `failure_producing_condition`),
    placed directly at its session-scoped resolved path: `decision: reject`
    (or `defer`), `confidence: high`, `artifact_id`, `created_at`,
    `created_by` all present, `reversal_conditions` OMITTED. Before
    `--resume`, this SAME file is corrected in place (only
    `reversal_conditions: [...]` added, nothing else touched) and
    recommitted -- see `recovery_invocation`.

  EMPIRICALLY CONFIRMED: this exact directory, with this exact content
  (frozen-SHA archive extracted via `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`, `--executor dry-run` for both
  invocations), was actually built and dispatched through the real
  `OrchestrationRunner` end to end during this construction task -- not
  just predicted from source -- and produced exactly the sequence
  `recovery_invocation` describes.
spec_sha256: 3325403e7b68f1c0ac22752d40a03b85b72aee35f4e086d39851ec175b90bdcb
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # RECOMPUTED after the --from-session bootstrap fix (review round 2):
  # the recovery_invocation/initial_state_specification "supplied up
  # front" defect was corrected and the full two-invocation recovery
  # sequence was re-verified end to end via a real live OrchestrationRunner
  # run in a disposable scratch clone. Computed with PyYAML safe_load +
  # hashlib.sha256("".join(str(v) for v in fields)) over this file's final
  # content.
qualification: |
  ADMISSIBLE
