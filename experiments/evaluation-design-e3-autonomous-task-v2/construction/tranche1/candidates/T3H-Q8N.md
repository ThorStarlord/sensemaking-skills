candidate_id: T3H-Q8N
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  REVISED after review: the real registered workflow `setup-sensemaking-repo`
  cannot be used as originally specified, for the same empirically-confirmed
  reason T3M-K7X was revised for: its `allowed_execution_modes` at frozen SHA
  (`skills/workflow-planner/references/workflow-registry.yaml:105-108`) is
  `[plan_only, prompt_chain, guided_execution]` -- `autonomous_execution` is
  NOT in that list, so `_load_registries()`
  (`scripts/workflow-runtime.py:401-428`, the `MODE_NOT_ALLOWED` check at
  lines 417-426) appends an error during `OrchestrationRunner.__init__` and
  the run aborts before step 1 executes. CONFIRMED by direct empirical
  re-run in a disposable scratch clone at the frozen SHA: invoking
  `setup-sensemaking-repo` with `--mode autonomous_execution` produces
  `MODE_NOT_ALLOWED` and exit code 1 with no run log or ledger ever created.

  Fix chosen (mirroring T3M-K7X's own post-review fix, and its own
  `initial_state_specification`): restructure to a bespoke 2-step workflow,
  `t3h-q8n-diagnostic-setup-workflow`, assembled VERBATIM from the real
  `setup-sensemaking-repo`'s steps 1-2 only, with one explicit addition:
  `allowed_execution_modes: [autonomous_execution]`. This keeps `--mode
  autonomous_execution` and every VALIDATED-status claim elsewhere in this
  spec correct:
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` (copied
      verbatim from workflow-registry.yaml:110-114).
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief` (copied verbatim from
      workflow-registry.yaml:115-120).
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, with the scratch-only registry
  addition described in `initial_state_specification` applied and committed
  before dispatch (never a change to the real registry). EMPIRICALLY
  CONFIRMED end to end: this exact workflow, invoked this way, ran past
  preflight, executed step 1 to `VALIDATED`, and reached step 2's real
  validator.

  This is the same real 2-step slice T3M-K7X (MEDIUM tier) also scopes to,
  but the failure this spec exercises lives in an entirely different
  validator code path (see `verified_failed_boundary`) -- a deterministic
  quote-grounding search algorithm, not a single required-field/
  registry-lookup check -- which is what makes this spec HIGH rather than
  MEDIUM.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`) and invoked with `--json`
  (`invoke_validator()`, lines 378-386) -- accepted by validate-brief.py's
  own argparse (`scripts/validate-brief.py:902-916`), so this does not
  crash.
  The genuine failure here is the deterministic "evidence quote grounding"
  check (issue #80), which requires tracing through THREE layers of real
  logic, not a single field-presence `if`:
  (1) `validate_brief()` locates a fenced `evidence_excerpts` YAML block in
  the brief's prose (`validate-brief.py:729-736`) and, for each excerpt
  with a present `file`, `lines`, and `quote`, first confirms the cited
  FILE exists (`os.path.exists(full_path)`, lines 761-763,
  `HALLUCINATED_FILE` if not) and the `lines` value parses as a valid
  `Lx`/`Lx-Ly`/bare-number form (lines 765-773, `INVALID_LINE_FORMAT` if
  not) -- both of which this spec's fixture satisfies, so neither of those
  two errors fires.
  (2) Only once both of those pass does `_quote_found_near()`
  (`validate-brief.py:340-430`) actually run (lines 786-789): it opens the
  cited file, computes a window `QUOTE_GROUNDING_WINDOW=3` lines on each
  side of the cited `lines` range (lines 366-385), normalizes both the
  quote and every candidate line in the window via `_normalize_for_grounding()`
  (lines 278-306: line-ending normalization, horizontal-whitespace
  collapse, per-line strip), and does an exact (post-normalization)
  substring search within that window only (lines 391-404) -- never a
  whole-file or semantic search.
  (3) When the cited quote is real text but copied from a location in the
  file MORE than 3 lines outside the cited range, the window search finds
  no match (`matched_lines` stays empty, lines 396-410), `_quote_found_near`
  returns `found=False`, and `validate_brief()` appends a BLOCKING error
  (`_code_error(EVIDENCE_QUOTE_NOT_FOUND, ...)` at line 791-798;
  `_code_error`'s `severity` parameter defaults to `"error"`, confirmed at
  `validate-brief.py:196` / `_is_blocking()` at lines 221-227). This is NOT
  one of the non-blocking `severity="warning"` checks elsewhere in the same
  function. `validation_json["valid"]` becomes False via the same
  `execute_step()` / `_run_validator_stack()` / `_run_validate_and_report()`
  path cited throughout this family (workflow-runtime.py lines 1023,
  1038-1046, 1587-1716, 1679), and `result["status"] = "FAILED"` is set for
  step 2.

  EMPIRICALLY CONFIRMED (both in isolation and through the real
  orchestrator): a constructed fixture with a valid, existing-file,
  well-formed-line-range `evidence_excerpts` entry citing
  `scripts/workflow-runtime.py`, `lines: L100-L102` (which at the frozen
  SHA holds the `"guided_execution": "APPROVED",` /
  `"autonomous_execution": "VALIDATED",` / `"yolo_execution": "VALIDATED",`
  MODE_CEILINGS entries), but whose `quote` is the real, verbatim text
  `def _generate_session_id() -> str:` (the actual line 151 of the same
  file), run directly through `python scripts/validate-brief.py <file>
  --repo-root . --json` produced exactly one error:
  `EVIDENCE_QUOTE_NOT_FOUND: Excerpt[0] quote not found in
  scripts/workflow-runtime.py (searched lines 97-105, no match). The quote
  must exist verbatim ... within 3 lines of the cited range 'L100-L102'.`
  (`valid: false`, exit code 1). The SAME fixture, dispatched through the
  real orchestrator (`t3h-q8n-diagnostic-setup-workflow`, `--mode
  autonomous_execution`, `--use-fixtures`), produced the identical error
  inside step 2's validator_stack and step 2 status `FAILED`.
  This is genuinely multi-layer: the root cause is not "a field is
  missing" but "a field IS present, references a REAL file, with a VALID
  line-range syntax, and still fails validation because a downstream text-
  search algorithm, applied to that upstream file's actual on-disk content
  at the cited location, does not find the claimed text there."
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first.
  Identically to T3M-K7X's step 1: no `output_artifact` means
  `execute_step()`'s artifact/validator branches (lines 889, 1022, 1048)
  never activate, execution falls straight to gate management (line 1065),
  and for `autonomous_execution` the step finishes with
  `result["status"] = "VALIDATED"` (line 1086). The run log's `### Step 1`
  block logs status `VALIDATED`; the ledger carries only `step_started` and
  `step_completed` events for `step_id: "1"` (no `artifact_created` /
  `validation_completed`, since there is no artifact).
  EMPIRICALLY CONFIRMED: the real orchestrator run's ledger for step 1 was
  exactly `step_started` then `step_completed(status: validated,
  gate_status: automated_approval)` -- no other event types for
  `step_id: "1"`.
failure_producing_condition: |
  REVISED after review: the step-2 `repository_sensemaking_brief` with the
  wrong-quote `evidence_excerpts` entry is FIXTURE CONTENT placed as part
  of this spec's initial state (via `--use-fixtures` pointing at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`,
  `--executor dry-run`) -- it is NOT something a live, real-skill-dispatched
  `repo-sensemaker` invocation would organically produce. REVIEWER-CONFIRMED
  reason: `scripts/brief_skeleton.py`'s `reconcile_evidence_excerpt_quotes()`
  (issue #89) is invoked unconditionally inside the SDK-backed `claude-code`
  executor's `invoke_skill()` path for `repository_sensemaking_brief`, and
  it deterministically OVERWRITES every `evidence_excerpts[].quote` with
  the actual verbatim text extracted from the cited file/lines at
  reconciliation time, discarding whatever an agent/model wrote there. The
  reviewer ran this function directly against this spec's own excerpt
  (`file: scripts/workflow-runtime.py`, `lines: L100-L102`, the wrong
  quote below) and confirmed it silently rewrites the quote to the CORRECT
  text -- so a genuinely-dispatched live agent producing this brief via
  real skill execution can never actually trigger
  `EVIDENCE_QUOTE_NOT_FOUND` for "right file, valid line syntax, wrong-but-
  real quote": only `HALLUCINATED_FILE` (wrong/nonexistent file) or
  `INVALID_LINE_FORMAT` (malformed `lines` syntax) survive reconciliation,
  since `reconcile_evidence_excerpt_quotes()` only has a real quote to
  extract and substitute when the file exists and the line range is
  parseable in the first place. This is exactly the same honesty pattern
  the disposable T3 pilot's own `T3-PILOT-TASK.md` already follows: its
  broken content is pre-placed fixture state, not agent-produced, and it
  says so up front. A future materializer must dispatch this scenario the
  same way this spec was itself empirically verified (fixture content
  placed at initial state, `--use-fixtures` + `--executor dry-run`, never
  real skill dispatch for step 2) -- attempting it via real skill
  execution will not reproduce `EVIDENCE_QUOTE_NOT_FOUND`, by construction
  of `reconcile_evidence_excerpt_quotes()`, not by any flaw in the
  dispatch.

  The fixture is authored so every OTHER check in `validate_brief()`
  passes cleanly: `primary_fog_type` a valid enum value, `evidence` (the
  top-level machine-YAML list, distinct from the prose `evidence_excerpts`
  block) non-empty with a real citation, `recommended_workflow_id` a real
  registry id, "logic trace" present in the prose, a structured
  `weakness_type` set to a real taxonomy term (e.g. "Contract Mismatch",
  per `skills/repo-sensemaker/references/weakness-types.md`) that also
  appears in the Section 6 "Weakest boundary" prose.
  The `evidence_excerpts` YAML block contains exactly one excerpt whose
  `file` is a REAL path at the frozen SHA (`scripts/workflow-runtime.py`),
  whose `lines` is a validly-formatted, REAL range within that file
  (`L100-L102`, the `MODE_CEILINGS` entries), and whose `quote` field is
  instead copied VERBATIM from a genuinely different, non-adjacent
  location in the SAME file -- the real line 151,
  `def _generate_session_id() -> str:`. Line 151 is well outside the +/-3
  line grounding window around `L100-L102` (window = lines 97-105), so
  `_quote_found_near` finds zero matches and `EVIDENCE_QUOTE_NOT_FOUND`
  fires. This isolates the brief to exactly one error -- EMPIRICALLY
  CONFIRMED both via direct `validate-brief.py --json` invocation and via
  the real orchestrator run (see `verified_failed_boundary`), in both
  cases using the fixture-content dispatch path described above.
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-q8n-diagnostic-setup-workflow --mode autonomous_execution
  --use-fixtures --executor dry-run` -- `--use-fixtures --executor dry-run`
  is REQUIRED here, not optional flourish: per `failure_producing_condition`
  /`initial_state_specification`, the wrong-quote step-2 brief is fixture
  content, not something a live-dispatched `repo-sensemaker` would
  organically produce (`--executor` defaults to `"claude-code"`, i.e. real
  dispatch, if unspecified -- omitting these flags would route step 2
  through real skill execution, where `reconcile_evidence_excerpt_quotes()`
  would silently correct the quote and `EVIDENCE_QUOTE_NOT_FOUND` would
  never fire). (no `--log-dir`, so it defaults to the auto-generated
  session directory, e.g.
  `artifacts/08-orchestration-run` -- EMPIRICALLY the exact directory name
  depends on how many `artifacts/NN-orchestration-run/` directories already
  exist in the clone; the frozen-SHA repo ships with several PRE-EXISTING
  ones for unrelated dogfood workflows, see `oracle_requirements`). Ends
  with step 2 FAILED.

  BEFORE invoking `--resume`: the git working tree must be returned to
  clean. EMPIRICALLY DISCOVERED (not previously documented in this spec):
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution` -- and a
  completed invocation ALWAYS leaves the tree dirty (the new, untracked
  `artifacts/NN-orchestration-run/` directory, plus a modified
  `docs/mode-coverage.yaml` from Phase 5's `update_mode_coverage()`). A
  second invocation (whether `--resume` or a fresh one) will hit
  `[FAIL] GIT: Git working tree is not clean` and abort at preflight,
  before any resume logic runs, unless this new state is committed first.
  This is a genuine operational precondition for chaining any two
  invocations of this runner in `autonomous_execution`/`guided_execution`/
  `yolo_execution` mode against a git-backed repo root, confirmed by
  directly hitting this failure and resolving it with a commit.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-q8n-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume
  --use-fixtures --executor dry-run`. `--use-fixtures --executor dry-run`
  is REQUIRED again here for the same reason as invocation 1 -- step 2 is
  genuinely re-executed on resume, and without these flags it would fall
  back to the `"claude-code"` default (real dispatch), which would route
  the corrected fixture content through real skill execution instead of
  the fixture path this spec's verification actually used.
  `--log-dir` must point at the directory that holds INVOCATION 1's
  `run_log_t3h-q8n-diagnostic-setup-workflow_autonomous_execution.md`,
  since `_find_resume_state()` (line 1956) builds the path to read as
  `os.path.join(self.log_dir, f"run_log_{self.workflow_id}_{self.mode}.md")`.
resume_expectations: |
  `_find_resume_state()` (line 1951) reads invocation 1's run log; step 1's
  logged status `VALIDATED` is in `_resumable_terminal_statuses()`
  (`{"VALIDATED", "COMPLETED"}` for autonomous_execution, lines 1916-1949)
  and is added to `completed_steps`; step 2's logged status `FAILED` is
  excluded from both `completed_steps` and `paused_step` (lines 1973-1978)
  by the same membership-check construction, not a special-cased "skip
  FAILED" branch. `resume_skip` (line 2594) resolves to `{1}`. In the step
  loop (lines 2605-2624): step 1 is skip-reconstructed synthetically (lines
  2606-2621, no `execute_step()` call, and its result dict hardcodes
  `"status": "COMPLETED"`, line 2617); step 2 is genuinely re-executed via
  `execute_step()` (line 2623), re-invoking `repo-sensemaker` and
  re-running the full `_quote_found_near()` grounding search again against
  the newly produced brief.
  EMPIRICALLY CONFIRMED end to end: the resumed run printed `[OK] Found
  resume state: 1 completed, paused at step None` and `[OK] Resuming:
  skipping steps [1], starting from step 2`, then genuinely re-ran
  `repo-sensemaker`'s validator against a corrected fixture (grounded quote
  this time) and step 2 passed (`[OK] Validation passed`), ending with
  `Execution completed successfully.` / exit code 0.
protected_work: |
  REVISED after review: run-log content is NOT a reliable preservation
  channel and must not be claimed as one. EMPIRICALLY CONFIRMED:
  `_find_resume_state()` and `write_run_log()` both resolve the run-log
  path from the SAME `self.log_dir` (lines 1956 and 1995) -- and because
  `--resume` MUST reuse the identical `--log-dir` value to find prior
  state at all, `write_run_log()` OVERWRITES that same file in place on
  every invocation. After the resumed run, the run log at that fixed path
  shows ONLY the latest state (step 1 `COMPLETED`, step 2 `VALIDATED`);
  invocation 1's `FAILED` record for step 2 is gone from it. A
  materialized oracle must never rely on run-log content surviving past a
  later invocation.
  The reliable, isolated preservation channel is instead
  `run-ledger.jsonl`, which lives in a SEPARATE, auto-incrementing numbered
  directory (`artifacts/NN-orchestration-run/`), independent of
  `--log-dir`, freshly created on EVERY invocation (via
  `_create_user_intent_artifact`, which always computes
  `next_num = max(existing NNs) + 1`) and never overwritten. EMPIRICALLY
  CONFIRMED: invocation 1's ledger (its own numbered directory) and
  invocation 2's ledger (a DIFFERENT, later-numbered directory) coexist on
  disk unchanged after both runs complete.
  Step 1 has no output artifact, so the protected invariant is LEDGER
  SILENCE for `step_id: "1"`: invocation 2's own fresh `run-ledger.jsonl`
  must contain no `step_started`, `artifact_created`, `validation_completed`,
  or `step_completed` events for `step_id: "1"` -- EMPIRICALLY CONFIRMED
  (invocation 2's ledger contained exactly one `step_started`/
  `artifact_created`/`validation_completed`/`step_completed` sequence, all
  for `step_id: "2"`, and nothing for `step_id: "1"`). The cited SOURCE
  file (`scripts/workflow-runtime.py` in the scratch clone) is itself also
  implicitly protected -- it must not be modified between attempts, since
  the fix for this failure is entirely within the BRIEF's own
  `evidence_excerpts` block.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family: (1)
  `git reset --hard` / `git clean -fd` on the scratch clone between
  attempts -- EMPIRICALLY CONFIRMED the runtime's own `rollback()` (line
  2511-2521) prints exactly this advice after every FAILED run
  (`has_failures` true, lines 2661-2663); following it would destroy the
  ledger directories the resume mechanism depends on; (2)
  deleting/truncating `run_log_t3h-q8n-diagnostic-setup-workflow_autonomous_execution.md`
  or any `run-ledger.jsonl` and re-invoking without `--resume`; (3)
  hand-editing step 2's logged status from `FAILED` to `VALIDATED` in the
  run log to force it into skip-reconstruction instead of genuine retry.
  A fourth behavior specific to this spec's failure mode is also
  forbidden: "fixing" the failure by editing the CITED SOURCE FILE
  (`scripts/workflow-runtime.py`) so the fabricated quote happens to appear
  near the cited lines, instead of correcting the brief's own citation --
  independently detectable via a diff/hash of the cited source file across
  attempts. Committing invocation 1's own run artifacts (the new numbered
  ledger directory, the run log, `docs/mode-coverage.yaml`) to restore a
  clean tree BEFORE `--resume` (see `recovery_invocation`) is REQUIRED
  operational hygiene, not reset laundering -- it commits forward, changes
  no prior recorded state, and does not touch `git reset`/`git clean`.
idempotency_expectations: |
  REVISED after review: scoped entirely to ledger content, per
  `protected_work`. Across invocation 1's ledger and invocation 2's ledger
  (two separate files in two separate numbered directories, read
  together), `step_id: "1"` must show exactly ONE `step_started`/
  `step_completed` pair (from invocation 1's ledger only) -- a second
  occurrence in invocation 2's ledger would mean step 1 was silently
  re-executed rather than skip-reconstructed (there is no artifact file
  hash to fall back on for step 1, so this ledger-pair check is the only
  detector). `step_id: "2"` is expected to show TWO full sequences across
  the two ledgers: invocation 1's ending in
  `validation_completed(status: failed)` / `step_completed(status: failed)`,
  invocation 2's ending in `validation_completed(status: passed)` /
  `step_completed(status: validated)` -- EMPIRICALLY CONFIRMED, this exact
  pattern was observed. One `run_started` / `run_completed` pair per
  invocation's own ledger (two pairs total, distinct `session_id`/`run_id`
  values) is expected bookkeeping and must not be misclassified as
  duplicated semantic work.
oracle_requirements: |
  A materialized oracle must first isolate THIS spec's own invocations from
  the frozen-SHA repo's pre-existing, committed `artifacts/NN-orchestration-run/`
  directories (real dogfood examples for unrelated workflows --
  EMPIRICALLY CONFIRMED the scratch clone ships with several, e.g. for
  `fast-local-diagnostic` and `full-local-sensemaking`, before this spec's
  own runs ever execute). Filter by reading each candidate directory's
  `run-ledger.jsonl` first line and matching
  `event=="run_started"`.`workflow_id == "t3h-q8n-diagnostic-setup-workflow"`
  -- never by directory position/number alone, since pre-existing and
  newly-created directories interleave in the numbering.
  Applying the seven-link recovery chain to this scenario, using ONLY
  ledger content (never run-log content, per `protected_work`): (1) the
  chronologically-first matching directory's ledger shows step 2 genuinely
  reached FAILED via `EVIDENCE_QUOTE_NOT_FOUND` specifically (parse the
  validator output / `validation_run_log.md` for the error_id/message, not
  a crash); (2) that same ledger shows step 1's `step_completed` at status
  `validated`; (3) the chronologically-LAST matching directory's ledger
  contains ZERO `step_id: "1"` events of any kind; (4) that same ledger
  contains a fresh step_id "2" sequence ending `validated`/`passed`; (5)
  the resumed run's step 2 brief has an `evidence_excerpts` entry whose
  quote is independently re-verifiable (by the oracle itself) as present
  within +/-3 lines of its cited range in the named file; (6) the fixed
  `--log-dir` path's run log, read ONLY for its LATEST state (never for
  history), shows step 2 as `VALIDATED`; (7) none of the
  `forbidden_reset_restart_behavior` items occurred, INCLUDING the
  source-file-tampering variant specific to this spec (diff/hash of
  `scripts/workflow-runtime.py` in the scratch clone across attempts must
  show no change).
complexity_breakdown: |
  HIGH because the failure's root cause requires tracing through more than
  one layer of real validator logic -- this family's second HIGH criterion.
  Unlike a MEDIUM spec's single `if field not in artifact_data` check, this
  failure only reaches the deciding logic (`_quote_found_near`'s windowed,
  normalized substring search) after passing TWO prior gating checks
  (`HALLUCINATED_FILE`, `INVALID_LINE_FORMAT`) that this spec's fixture
  deliberately satisfies so they cannot mask or be confused with the real
  failure. The failure additionally depends on the actual on-disk content
  of a file OUTSIDE the artifact under validation, at a location OUTSIDE
  the artifact author's claimed citation. This is a single failing step
  (step 2 of 2), so it does NOT also claim the multi-step HIGH criterion --
  the multi-layer root cause is this spec's sole, sufficient basis for
  HIGH, and this was independently, empirically confirmed to actually
  behave this way in a real orchestrator run, not just inferred from
  reading the validator's source.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` (under the
  top-level `workflows:` key):

    id: t3h-q8n-diagnostic-setup-workflow
    display_name: T3H-Q8N Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (multi-layer evidence-quote grounding).
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
  and committed, let `--mode autonomous_execution` pass preflight and both
  steps execute for real.

  REVISED after review: step 1 needs no fixture (`setup-sensemaking-skills`
  requires no pre-existing fixture). Step 2's `repository_sensemaking_brief`
  -- INCLUDING its deliberately-mis-grounded `evidence_excerpts` entry --
  is NOT authored fresh by a real, live-dispatched `repo-sensemaker`
  invocation for this spec. It MUST instead be placed as fixture content
  at `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md` as
  part of initial state, and the dispatched run invoked with
  `--use-fixtures --executor dry-run` for step 2 (exactly how this spec
  was itself empirically verified). Reason (reviewer-confirmed, see
  `failure_producing_condition`): `scripts/brief_skeleton.py`'s
  `reconcile_evidence_excerpt_quotes()` (issue #89), which runs
  unconditionally inside the real `claude-code` executor's `invoke_skill()`
  path for this artifact type, deterministically overwrites any
  `evidence_excerpts[].quote` with the actual verbatim text at the cited
  location -- so a live-dispatched agent can never organically produce the
  "right file, valid lines, wrong-but-real quote" condition this spec's
  `EVIDENCE_QUOTE_NOT_FOUND` failure depends on; reconciliation would
  silently correct it before validation ever runs. This mirrors the
  disposable T3 pilot's own `T3-PILOT-TASK.md`, which is likewise upfront
  that its broken content is pre-placed fixture state, not agent-produced.
  A future materializer must not attempt this scenario via real skill
  dispatch for step 2 and should not treat a failure to reproduce it that
  way as a bug in the materializer -- it is expected, by construction of
  `reconcile_evidence_excerpt_quotes()`.

  `workflow-registry.yaml` and
  `skills/repo-sensemaker/references/weakness-types.md` must otherwise be
  left unmodified from the frozen SHA. The scratch clone must be an
  unmodified checkout of the frozen SHA so that
  `scripts/workflow-runtime.py` lines 100-102 and 151 are exactly the real,
  cited text this spec's fixture quote depends on. Per `recovery_invocation`,
  the tree must be recommitted clean (new ledger directory + updated
  `docs/mode-coverage.yaml`) after invocation 1, before `--resume` is
  invoked -- this is required for any second invocation of this runner in
  a mutating mode against a git-backed root, not specific to the content
  fix.
spec_sha256: 93c27aa0301941d255219d09e294dd48c01ae448cc0c8509a9713cb8d1a47100
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Recomputed after the third post-review fix (recovery_invocation's two
  # example commands now include --use-fixtures --executor dry-run, so the
  # reproduction recipe is consistent with failure_producing_condition /
  # initial_state_specification's fixture-content requirement) with PyYAML
  # safe_load + hashlib.sha256("".join(str(v) for v in fields)) over this
  # file's revised content.
qualification: |
  ADMISSIBLE
