candidate_id: T3H-Z1V
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  REVISED after review: same disqualifying reason and same fix as T3H-Q8N
  and T3M-K7X -- the real `setup-sensemaking-repo`'s `allowed_execution_modes`
  at frozen SHA (`workflow-registry.yaml:105-108`) is `[plan_only,
  prompt_chain, guided_execution]`, no `autonomous_execution`. CONFIRMED by
  direct empirical re-run: `MODE_NOT_ALLOWED`, no run log or ledger ever
  created.

  Fix: a SEPARATE bespoke 2-step workflow, `t3h-z1v-diagnostic-setup-workflow`
  (distinct id from T3H-Q8N's own bespoke workflow, so the two specs'
  ledgers can never be confused with each other by workflow_id filtering),
  assembled VERBATIM from `setup-sensemaking-repo`'s steps 1-2, with
  `allowed_execution_modes: [autonomous_execution]` added:
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact`.
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief`.
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5.

  What makes this spec a DIFFERENT scenario from T3H-Q8N and T3M-K7X
  despite the same underlying 2-step shape is that this spec requires
  THREE total invocations, not one or two: an initial attempt, a first
  `--resume` that ALSO fails (for a different, equally real reason), and a
  second `--resume` -- resuming a run that is itself already a resumed
  run. All three of this spec's content-validation failures/pass are
  distinct from T3H-Q8N's `EVIDENCE_QUOTE_NOT_FOUND` and from T3M-K7X's
  `recommended_workflow_id.unknown_value`. EMPIRICALLY VERIFIED end to end
  in a disposable scratch clone: all three invocations were actually run
  in sequence (not just read from source) and produced exactly the
  outcomes this spec describes throughout.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`) and invoked with `--json`,
  accepted by its own argparse (`scripts/validate-brief.py:902-916`) -- the
  same non-crashing routing path used throughout this family.
  Attempt 1's failure: `primary_fog_type` is present but its value is not
  one of the four allowed enum values (`scripts/validate-brief.py:509-520`),
  producing `error_id:
  "repository_sensemaking_brief.primary_fog_type.unknown_value"`
  (`error_type: unknown_value`). EMPIRICALLY CONFIRMED: a fixture with
  `primary_fog_type: backend_fog` and every other field valid, run directly
  through `validate-brief.py --json`, produced exactly this one error;
  dispatched through the real orchestrator, step 2 FAILED with exactly this
  error in its validator_stack.
  Attempt 2's failure (after the agent fixes `primary_fog_type` on
  `--resume` #1, but introduces or leaves a SEPARATE defect): `evidence` is
  present as a list but is EMPTY (`scripts/validate-brief.py:548-560`),
  producing `error_id: "repository_sensemaking_brief.evidence.logic_error"`
  (`error_type: logic_error`). EMPIRICALLY CONFIRMED the same way: exactly
  one error, and the real orchestrator's `--resume` genuinely re-ran
  `repo-sensemaker`'s validator and failed again with THIS DIFFERENT error
  (not a repeat of attempt 1's).
  Attempt 3's success: `evidence` restored to non-empty with
  `primary_fog_type` still valid -- EMPIRICALLY CONFIRMED `valid: true`,
  zero errors, and the real orchestrator's second `--resume` genuinely
  re-ran the validator a third time and step 2 reached `VALIDATED`.
  Both failures flip `validation_json["valid"]` to False via the identical
  `execute_step()` / `_run_validator_stack()` / `_run_validate_and_report()`
  chain cited throughout this family (workflow-runtime.py lines 1023,
  1038-1046, 1587-1716, 1679).
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully ONLY ONCE,
  in the FIRST (non-resumed) invocation. No `output_artifact` means
  `execute_step()`'s artifact/validator branches (lines 889, 1022, 1048)
  never activate; for `autonomous_execution` the step finishes with
  `result["status"] = "VALIDATED"` (line 1086). EMPIRICALLY CONFIRMED:
  invocation 1's ledger (its own numbered `artifacts/NN-orchestration-run/`
  directory) recorded exactly `step_started` then
  `step_completed(status: validated, gate_status: automated_approval)` for
  `step_id: "1"` -- nothing else.
  Step 1 must NEVER be genuinely re-executed on EITHER subsequent
  `--resume`. EMPIRICALLY CONFIRMED for BOTH resumes: neither `--resume`
  #1's nor `--resume` #2's own fresh ledger contained any `step_id: "1"`
  event of any kind.
failure_producing_condition: |
  Attempt 1: the step-2 brief sets `primary_fog_type: backend_fog` (not
  among the four allowed values), while every other Phase-1 field
  (`evidence` non-empty, `recommended_workflow_id` a real registry id,
  logic trace present, file-level evidence citation present, a valid
  `weakness_type`, a well-formed and correctly-grounded `evidence_excerpts`
  block) is populated validly -- isolating attempt 1 to exactly one error.
  Attempt 2 (produced during `--resume` #1): `primary_fog_type` corrected
  to a valid value (`architecture_fog`), but `evidence` re-authored as an
  empty list, with every other field still valid -- isolating attempt 2 to
  exactly one, DIFFERENT error. (A realistic failure mode: an agent fixing
  the reported defect while introducing or leaving a second, previously-
  masked one; attempt 1's brief has valid non-empty evidence by
  construction, so this is attempt 2's genuine rewrite, not a
  pre-existing latent defect surfacing coincidentally.)
  Attempt 3 (produced during `--resume` #2): `evidence` restored to
  non-empty, `primary_fog_type` still valid from attempt 2 -- all checks
  pass.
  EMPIRICALLY CONFIRMED at every step: three separate fixture files, each
  validated in isolation via `validate-brief.py --json` before being
  dispatched through the real orchestrator, each producing exactly the
  predicted single error (or zero errors, for attempt 3).
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-z1v-diagnostic-setup-workflow --mode autonomous_execution` (no
  `--log-dir`; defaults to the auto-generated session directory --
  EMPIRICALLY this was `artifacts/05-orchestration-run` in the verification
  clone, but the exact number depends on how many
  `artifacts/NN-orchestration-run/` directories already exist; the
  frozen-SHA repo ships with several pre-existing ones for unrelated
  dogfood workflows, see `oracle_requirements`). Ends with step 2 FAILED
  (`primary_fog_type.unknown_value`).

  BEFORE `--resume` #1: the git tree must be recommitted clean.
  EMPIRICALLY DISCOVERED: `preflight_check()`
  (`scripts/workflow-runtime.py:537-560`) requires a clean
  `git status --porcelain` for `autonomous_execution`, and every completed
  invocation leaves the tree dirty (new untracked ledger directory, plus a
  modified `docs/mode-coverage.yaml`). This spec's THREE invocations
  therefore require commits after invocation 1 AND after invocation 2 --
  twice as many required commits as a single-resume spec, since there are
  two "in-between" points, not one.

  `--resume` #1: `python scripts/workflow-runtime.py "<same problem
  statement>" --repo-root <scratch-clone-root> --workflow
  t3h-z1v-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume`.
  `--log-dir` points `_find_resume_state()` (line 1956) at invocation 1's
  run log. Ends with step 2 FAILED again (`evidence.logic_error`); the run
  log at the SAME fixed path is OVERWRITTEN in place (see `protected_work`)
  -- this is critical for what `--resume` #2 reads next.

  BEFORE `--resume` #2: recommit the tree clean again (new ledger
  directory from `--resume` #1, updated `docs/mode-coverage.yaml`,
  overwritten run log).

  `--resume` #2 (the "resume of an already-resumed run"): `python
  scripts/workflow-runtime.py "<same problem statement>" --repo-root
  <scratch-clone-root> --workflow t3h-z1v-diagnostic-setup-workflow --mode
  autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<SAME invocation-1-session-dir --
  NOT a different directory> --resume`. Critically, `--log-dir` is the SAME
  path used for `--resume` #1 -- there is only ever ONE run-log location
  for this whole 3-invocation sequence, fixed at whatever `--log-dir`
  resolved to on invocation 1, reused verbatim every time (see
  `protected_work` for why: `--resume` always writes back to `self.log_dir`,
  and `self.log_dir` never changes once explicitly set on the CLI). Ends
  with step 2 VALIDATED.
resume_expectations: |
  `--resume` #1: `_find_resume_state()` (line 1951) parses invocation 1's
  run log. Step 1's logged status `VALIDATED` is in
  `_resumable_terminal_statuses()` (`{"VALIDATED", "COMPLETED"}` for
  autonomous_execution, lines 1916-1949) and is added to `completed_steps`.
  `resume_skip` (line 2594) resolves to `{1}`. Step 1 is skip-reconstructed
  (lines 2606-2621): the synthetic result dict hardcodes
  `"status": "COMPLETED"` (line 2617, a LITERAL string, not
  `MODE_CEILINGS[self.mode]`). `write_run_log()` then writes THIS
  invocation's own new run log content (to the SAME fixed path) with step
  1's `### Step 1` block showing `- **status**: COMPLETED` (line 2092,
  directly from the synthetic dict, not `VALIDATED`). Step 2 is genuinely
  re-executed via `execute_step()` (line 2623) and fails again (this time
  `evidence.logic_error`). EMPIRICALLY CONFIRMED: the overwritten run log,
  read after `--resume` #1, showed `- **status**: COMPLETED` for step 1
  and `- **status**: FAILED` for step 2 -- verbatim, byte-for-byte matching
  this prediction.

  `--resume` #2: `_find_resume_state()` parses the SAME fixed-path run log
  (per `--log-dir` above) -- which by now holds `--resume` #1's
  OVERWRITTEN content, i.e. step 1 status `COMPLETED` (not `VALIDATED`).
  This is EXACTLY why `_resumable_terminal_statuses()` explicitly includes
  the `"COMPLETED"` literal alongside the mode's own ceiling status --
  its own docstring (`workflow-runtime.py:1928-1932`) states this in so
  many words: "'COMPLETED' is additionally accepted across all modes for
  backward compatibility ... and with the synthetic step reconstructions
  this runner itself writes for already-resumed steps." Because
  `"COMPLETED"` is a member of the set, step 1 is STILL correctly
  recognized as resumable -- `resume_skip` again resolves to `{1}`. Step 1
  is skip-reconstructed a SECOND time (never genuinely executed a second
  or third time, across all three invocations). Step 2's logged status
  `FAILED` (from `--resume` #1's genuine re-execution) is again excluded
  from `completed_steps`, so step 2 is genuinely re-executed a THIRD time,
  and this time passes.
  EMPIRICALLY CONFIRMED end to end: `--resume` #2's console output printed
  `[OK] Found resume state: 1 completed, paused at step None` and
  `[OK] Resuming: skipping steps [1], starting from step 2`, step 1 was
  skip-reconstructed (no `[FIXTURE] Using fixture artifact` line for step
  1), step 2 genuinely re-ran and printed `[OK] Validation passed`, and the
  run finished `Execution completed successfully.` / exit code 0. The run
  log's `## Final State` block read `Status: partial` / `Note: 2/2 steps
  completed` / `Steps completed: 1/2` -- a real, confirmed quirk of
  `write_run_log()`'s final-state computation (it separately counts
  `status=="COMPLETED"` and `status=="VALIDATED"` steps, lines 2002-2030,
  and neither count alone equals the total step count when the two
  completed steps have DIFFERENT status literals) that a materialized
  oracle must not misread as a failure -- the run's actual exit code (0)
  and per-step statuses are the authoritative signal, not this summary
  label.
protected_work: |
  REVISED after review: there is no "two separate run-log locations" to
  diff, and run-log content is not a preservation channel at all.
  EMPIRICALLY CONFIRMED: `_find_resume_state()` and `write_run_log()` both
  resolve the run-log path from the SAME `self.log_dir` (lines 1956,
  1995); because `--resume` MUST reuse the identical `--log-dir` to find
  prior state, EVERY invocation after the first OVERWRITES that ONE fixed
  file in place. After `--resume` #1, it holds attempt-2's state
  (step 1 `COMPLETED`, step 2 `FAILED` with the evidence error); after
  `--resume` #2, it holds attempt-3's state (step 1 `COMPLETED`, step 2
  `VALIDATED`). Attempt 1's original `FAILED`-for-`primary_fog_type` record
  is NOT preserved anywhere in run-log form after `--resume` #1 overwrites
  it.
  The reliable, isolated preservation channel is `run-ledger.jsonl`: EACH
  of the three invocations gets its OWN fresh, auto-incrementing numbered
  directory (`artifacts/NN-orchestration-run/`), independent of
  `--log-dir`, created via `_create_user_intent_artifact`
  (`next_num = max(existing NNs) + 1`) on every invocation including
  resumes, and never overwritten. EMPIRICALLY CONFIRMED: all three
  invocations' ledger directories (in the verification clone,
  05/06/07-orchestration-run) coexisted unchanged on disk after all three
  runs completed.
  The protected invariant, across ALL THREE ledgers: `step_id: "1"` must
  appear in EXACTLY ONE of the three ledgers (invocation 1's), never in
  `--resume` #1's or `--resume` #2's own ledger. EMPIRICALLY CONFIRMED:
  grep across all three ledger files for `"step_id": "1"` matched only
  invocation 1's file.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family, explicitly at
  BOTH transition points (attempt1->2 AND attempt2->3), not just once: (1)
  `git reset --hard` / `git clean -fd` between any two attempts --
  EMPIRICALLY CONFIRMED the runtime's own `rollback()` prints this advice
  after every FAILED run (both attempt 1 and attempt 2 trigger it); (2)
  deleting/truncating the run log or any `run-ledger.jsonl` and
  re-invoking without `--resume`; (3) hand-editing either run-log
  overwrite's step 2 status from `FAILED` to `VALIDATED`/`COMPLETED`. A
  fifth behavior specific to this spec is also forbidden: pointing
  `--resume` #2's `--log-dir` at anything other than the ONE fixed path
  used since invocation 1 -- there is no alternate valid directory to
  point at (unlike an earlier, incorrect draft of this spec, there is no
  "session dir B" holding its own separate run log; `--log-dir` is a
  single, reused, overwritten-in-place location for this entire 3-
  invocation sequence). Committing each invocation's own run artifacts
  (new ledger directory, overwritten run log, `docs/mode-coverage.yaml`)
  to restore a clean tree between invocations (see `recovery_invocation`)
  is REQUIRED operational hygiene, not reset laundering.
idempotency_expectations: |
  REVISED after review: scoped entirely to ledger content. Across the
  THREE separate ledger files (one per invocation, read together),
  `step_id: "1"` must show exactly ONE `step_started`/`step_completed`
  pair, located ONLY in invocation 1's ledger -- ZERO occurrences in
  `--resume` #1's ledger and ZERO in `--resume` #2's ledger. A single
  occurrence in either resumed ledger would mean step 1 was silently,
  genuinely re-executed rather than skip-reconstructed -- and because this
  spec has TWO resumes, there are TWO independent opportunities for that
  bug to occur, both of which a single-resume spec cannot exercise.
  `step_id: "2"` is expected to show exactly THREE full sequences, one per
  invocation's own ledger: invocation 1 ending
  `validation_completed(status: failed)` (`primary_fog_type.unknown_value`);
  `--resume` #1's ledger ending the same way but for
  `evidence.logic_error`; `--resume` #2's ledger ending
  `validation_completed(status: passed)` /
  `step_completed(status: validated)`. All three are legitimate retries,
  not duplicates -- EMPIRICALLY CONFIRMED, this exact 1/3 pattern was
  observed across the three ledger files. Three `run_started` /
  `run_completed` pairs total (distinct `run_id` values) are expected
  bookkeeping.
oracle_requirements: |
  A materialized oracle must first isolate THIS spec's own three
  invocations from the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories (EMPIRICALLY CONFIRMED
  present for unrelated dogfood workflows, e.g. `fast-local-diagnostic`,
  `full-local-sensemaking`) AND from T3H-Q8N's own bespoke-workflow
  directories, if both specs' recovery attempts happen to run against the
  same clone. Filter by reading each candidate directory's
  `run-ledger.jsonl` first line and matching
  `event=="run_started"`.`workflow_id == "t3h-z1v-diagnostic-setup-workflow"`
  exactly -- never by directory position/number, which interleaves
  pre-existing, other-spec, and this-spec directories unpredictably. Order
  the matched directories chronologically (by ledger timestamp, not
  directory number, for robustness) to identify invocation 1, `--resume`
  #1, and `--resume` #2 as first/middle/last.
  Applying the seven-link recovery chain across three attempts, using ONLY
  ledger content (never run-log content, which reflects only the latest
  overwrite): (1) the first matching ledger's step 2 reached FAILED via
  `primary_fog_type.unknown_value`; (1b, this spec's extension) the SECOND
  matching ledger's step 2 ALSO reached FAILED, but via the DIFFERENT
  `evidence.logic_error` -- confirming these are different defects, not
  the same one re-reported (which would indicate the agent's `--resume` #1
  fix did nothing); (2) the first ledger's step 1 status is `validated`;
  (2b) the SECOND ledger contains ZERO `step_id: "1"` events (confirming
  skip-reconstruction, not re-validation, during `--resume` #1 -- the run
  log's own `COMPLETED` literal is a SUPPORTING signal, not required, since
  ledger silence alone is sufficient and more robust); (3) the THIRD
  matching ledger ALSO contains ZERO `step_id: "1"` events (confirming
  skip-reconstruction held on the SECOND resume too -- this is the check a
  single-resume spec structurally cannot perform); (4) the third ledger
  contains a fresh step_id "2" sequence ending `validated`/`passed`; (6)
  the third attempt's brief has valid `primary_fog_type` AND non-empty
  `evidence`; (7) none of the `forbidden_reset_restart_behavior` items
  occurred at EITHER transition (git reflog spanning all three invocations;
  confirm no alternate `--log-dir` was ever used).
complexity_breakdown: |
  HIGH because recovery is verified not just for the immediate retry but
  for idempotency under a SECOND resume of an already-resumed run -- this
  family's third HIGH criterion, explicitly, and now empirically (not just
  theoretically) confirmed. `--resume` #2 reads a run log whose step 1
  entry was ITSELF synthetically written by `--resume` #1, never genuinely
  re-validated -- this spec verifies a real, specific, DOCUMENTED runtime
  design decision (the `"COMPLETED"` literal in
  `_resumable_terminal_statuses()`, per its own docstring at
  `workflow-runtime.py:1928-1932`, explicitly written for this "chained
  resume" case) actually works end to end. A single-resume spec can never
  exercise this code path at all, since its one resumed run's step 1 entry
  is always read from an ORIGINAL (non-synthetic) `VALIDATED` log line. The
  two content failures (attempt 1, attempt 2) are each individually
  MEDIUM-simple in isolation -- deliberately so, keeping the double-resume
  mechanism itself, not failure-content novelty, the sole source of this
  spec's HIGH rating.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS a
  bespoke workflow entry committed before dispatch (distinct id from
  T3H-Q8N's own, `t3h-z1v-diagnostic-setup-workflow` vs.
  `t3h-q8n-diagnostic-setup-workflow`, so ledger-based filtering can never
  conflate the two specs' runs):

    id: t3h-z1v-diagnostic-setup-workflow
    display_name: T3H-Z1V Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (double-resume idempotency).
    initial_inputs:
      - id: repository_state
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
        skill: repo-sensemaker
        step_type: local_execution
        gate: review_repo_brief
        input_source: repository_state
        output_artifact: repository_sensemaking_brief

  EMPIRICALLY VERIFIED: this exact entry, added to a scratch registry copy
  and committed, let all three invocations pass preflight in
  `--mode autonomous_execution` (once the tree was recommitted clean
  between each pair of invocations, per `recovery_invocation`). No fixture
  repair needed: all three successive versions of the step-2 brief are
  authored fresh during each respective invocation. `workflow-registry.yaml`
  and `skills/repo-sensemaker/references/weakness-types.md` must be left
  unmodified from the frozen SHA. The dispatch protocol for this spec must
  explicitly instruct the agent to run all THREE invocations in the exact
  sequence given in `recovery_invocation`, committing between each pair --
  the entire point of this spec is unreachable with only two invocations,
  and unreachable at all if the tree is never recommitted clean between
  them (preflight would abort every invocation after the first).
spec_sha256: 9abe8992632a26b1fc0b4770d9e9ad24bf5547909f83d29c36b8c2d159e1e84a
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Recomputed after the post-review fix (mode fix + ledger-based protected
  # work, both empirically verified across all 3 invocations) with PyYAML
  # safe_load + hashlib.sha256("".join(str(v) for v in fields)) over this
  # file's revised content.
qualification: |
  ADMISSIBLE
