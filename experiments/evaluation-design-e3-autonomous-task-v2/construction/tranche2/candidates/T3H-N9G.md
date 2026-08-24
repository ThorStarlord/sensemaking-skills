candidate_id: T3H-N9G
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  A bespoke 3-step workflow, `t3h-n9g-review-handoff-workflow`, assembled from
  three real registered skills that do not currently co-occur in this order
  in any single registered workflow (frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5):
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` -- copied
      verbatim from the real `setup-sensemaking-repo` workflow's step 1
      (`skills/workflow-planner/references/workflow-registry.yaml:110-114`).
    - Step 2: skill `repo-sensemaker`, gate `review_diagnosis`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief` -- copied verbatim from the real
      `architectural-review-planning-workflow`'s step 1
      (`workflow-registry.yaml:964-970`).
    - Step 3: skill `architectural-review`, gate `review_recommendation`,
      `input_artifact: repository_sensemaking_brief`, `input_source:
      proposed_direction`, `output_artifact:
      architectural_review_recommendation` -- copied verbatim from the real
      `architectural-review-planning-workflow`'s step 2
      (`workflow-registry.yaml:971-978`).
  `allowed_execution_modes: [autonomous_execution]` is declared explicitly on
  this bespoke entry (a missing key defaults to `[]` per
  `scripts/workflow-runtime.py:418`, per this family's standing lesson).
  EMPIRICALLY CONFIRMED THIS SESSION, not merely read from the registry: the
  bespoke entry was inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` in a disposable
  scratch clone of the frozen SHA, and `OrchestrationRunner` was
  DIRECTLY INSTANTIATED (not dispatched through `main()`, and not merely
  read as YAML) against it:
  `OrchestrationRunner(workflow_id="t3h-n9g-review-handoff-workflow",
  mode="autonomous_execution", repo_root=".", executor="dry-run")` produced
  `runner.errors == []` -- no `MODE_NOT_ALLOWED`. As an in-session sanity
  check that this instantiation-based method actually discriminates
  correctly (not a false-positive harness), the SAME method was run against
  the real `setup-sensemaking-repo` with `mode="autonomous_execution"` and
  DID produce `MODE_NOT_ALLOWED: Mode 'autonomous_execution' not allowed for
  workflow 'setup-sensemaking-repo'. Allowed: ['plan_only', 'prompt_chain',
  'guided_execution']` -- confirming the check itself is discriminating, not
  vacuously passing everything.

  POST-REVIEW FIX (this construction session): a reviewer found this spec's
  ORIGINAL `recovery_invocation` deadlocked before ever reaching step 3's
  real content -- `proposed_direction` (and, discovered independently while
  fixing this, `repository_sensemaking_brief` as step 3's `input_artifact`)
  cannot be pre-placed at the path the runtime will actually look for it,
  because with a plain (non-`--from-session`) invocation
  `self.artifact_session_dir` is only computed DURING dispatch
  (`_create_user_intent_artifact()`, `scripts/workflow-runtime.py:450-458`:
  globs existing `artifacts/[0-9][0-9]-*` directories, takes `max+1`) -- the
  session-scoped path `_resolve_artifact_path("proposed_direction")` /
  `_resolve_artifact_path("repository_sensemaking_brief")` needs cannot exist
  or be known at command-launch time. EMPIRICALLY CONFIRMED (this session):
  `execute_step()`'s dry-run path (the `elif skill and ...
  supports_real_execution:` branch at line 915 is always skipped for
  `DryRunSkillExecutor`, whose `supports_real_execution = False`) never
  invokes a real skill and never creates the output artifact itself -- it
  always falls to `if not is_fixture: artifact_path =
  self._resolve_artifact_path(output_artifact)` (line 998), which is a path
  that must already exist on disk for validation to run at all, or the step
  fails with `ARTIFACT_NOT_FOUND` (`Expected artifact '<id>' not produced`,
  lines 1048-1062) BEFORE the real validator (and this spec's intended
  `risks_identified.logic_error` boundary) is ever reached.

  Fix: use `--from-session <pre-built-session-dir>` (a FIXED, non-numbered
  directory name this spec creates and populates itself, e.g.
  `artifacts/t3h-n9g-session`) for BOTH invocations. `initialize_from_session()`
  (`scripts/workflow-runtime.py:323-366`) sets `self.artifact_session_dir =
  from_session_path` directly from this CLI-supplied, deterministic path
  (requiring only that `<dir>/00-user-intent.md` already exists, checked at
  lines 346-352) -- so every `_resolve_artifact_path()` call for the whole
  run resolves against a directory this spec's construction fully controls
  and can pre-populate BEFORE the orchestrator ever runs. Since dry-run never
  authors content for ANY output artifact (not just `proposed_direction`),
  this same mechanism is used to pre-place step 2's
  `repository_sensemaking_brief.md` AND step 3's
  `architectural_review_recommendation.md` directly at their contract-resolved
  paths (`artifact-contracts.yaml`: `repository_sensemaking_brief` ->
  `artifacts/repository_sensemaking_brief.md`,
  `architectural_review_recommendation` ->
  `artifacts/architectural_review_recommendation.md`, both scoped to
  `artifact_session_dir` by `_scope_to_session_dir()`, lines 1521-1532) --
  `--use-fixtures` is NOT used at all for this workflow (see
  `failure_producing_condition`/`initial_state_specification`): pre-placing
  directly at the contract path is simpler and, unlike a fixture (which
  lives at a fixed `examples/...` path never consulted by `input_artifact`
  resolution -- confirmed by reading `_resolve_step_inputs()`, lines
  1424-1485, which always calls `_resolve_artifact_path()` for
  `input_artifact`, never `_get_fixture_artifact_path()`), it is the ONE
  location every consumer (step 3's own validation AND step 3's
  `input_artifact: repository_sensemaking_brief` resolution) actually reads.
  EMPIRICALLY RE-VERIFIED END TO END this session (disposable scratch clone,
  real CLI dispatch, not just instantiation): invocation 1
  (`--from-session artifacts/t3h-n9g-session`, no `--resume`) genuinely
  reached step 3 and FAILED with exactly
  `architectural_review_recommendation.risks_identified.logic_error`
  (confirmed in the console output and the ledger, NOT `ARTIFACT_NOT_FOUND`);
  invocation 2 (`--from-session artifacts/t3h-n9g-session --log-dir
  artifacts/t3h-n9g-session --resume`) printed `Found resume state: 2
  completed` / `Resuming: skipping steps [1, 2], starting from step 3`, step
  3 was genuinely re-executed and reached `VALIDATED`, run exited 0. See
  `recovery_invocation`/`protected_work`/`oracle_requirements` for the full,
  empirically-confirmed mechanics, including a further structural
  consequence of this fix discovered while re-verifying: because BOTH
  invocations share the SAME `--from-session` directory, `run-ledger.jsonl`
  is a SINGLE append-only file containing TWO `run_started`/`run_completed`
  brackets (both with the SAME `run_id` -- the fixed session-dir name -- but
  distinguishable by `git_commit`, which differs between the two brackets),
  not two separate per-invocation ledger directories the way every other
  spec in this family (which uses plain, non-`--from-session` auto-numbered
  invocations) produces.

  What makes this a genuinely different scenario from this family's other
  3-step HIGH spec (Tranche-1's T3H-W4J, which chains `repo-sensemaker` +
  `architectural-review` + a bespoke `handoff`/`session_summary` step that
  fails via the generic validator's unconditional `--json` argparse crash):
  this spec's step 1 is the no-op `setup-sensemaking-skills` (not
  `repo-sensemaker`), its step 2 is the real-content `repo-sensemaker` (not
  `architectural-review`), and -- critically -- its FAILING step (step 3,
  `architectural-review`) fails via a genuine CONTENT-dependent check
  (`risks_identified.logic_error`, see `verified_failed_boundary`), not the
  content-independent generic-validator crash T3H-W4J and the disposable T3
  pilot both already exercise. This spec never touches the generic
  `scripts/validate-artifact.py --json` bug class at all.
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA, with the bespoke
  registry addition applied and committed before dispatch (never a change to
  the real registry).
verified_failed_boundary: |
  Step 3's `architectural_review_recommendation` is routed to
  `scripts/validate-architectural-review-recommendation.py` by
  `select_validator()` (`scripts/validate-and-report.py:315-316`, which
  special-cases `artifact_id == "architectural_review_recommendation"`
  before any artifact would fall through to the generic
  `--json`-crashing `validate-artifact.py`). `invoke_validator()` calls it
  as `[artifact_path, --repo-root, --json]`; this validator's own argparse
  (`scripts/validate-architectural-review-recommendation.py:319`) defines
  `--json`, so the call does not crash.
  NOTE (discovered during post-review empirical re-verification): the
  OUTER dispatcher, `scripts/validate-and-report.py`, must FIRST locate an
  "authoritative machine-readable handoff block" in the artifact's own text
  to determine `artifact_id` before it can even call `select_validator()` --
  a heading matching `## (?:\d+\.\s*)?Machine-readable
  (?:handoff|plan|decision)` (`validate-and-report.py:58-60`) immediately
  followed by the ```yaml fence. This is a structural precondition on EVERY
  artifact type this family uses, not specific to this spec's failure
  mechanism, but it was not previously stated explicitly in this spec's own
  fixture description and caused the first empirical re-verification attempt
  to fail with an unrelated `no_authoritative_block` error instead of
  `risks_identified.logic_error` -- fixed by adding the canonical `##
  Machine-readable decision` heading (the exact heading real
  `architectural_review_recommendation` fixtures at
  `tests/fixtures/architectural-review-recommendation/fixture-valid-investigate-first.md`
  use) directly above the YAML fence; see `initial_state_specification`.
  The real failure condition, once that heading requirement is met, is the
  UNCONDITIONAL confidence/risk cross-field check
  (`scripts/validate-architectural-review-recommendation.py:260-276`), a
  genuinely different code path from every `decision`-specific branch this
  family has used elsewhere (T3M-P4W's `pursue_narrowed`, T3M-R2B's
  `investigate_first` companion-field check, T3M-C5N's `defer`/`reject`): it
  fires for ANY `decision` value, gated only by `confidence`. Once `decision`
  is a valid enum value (so the earlier `decision`-specific branch, here
  `investigate_first`'s `investigation_steps`-or-`validation_step`
  requirement at lines 204-217, is satisfied and does not also fire) and
  `confidence` is present as one of `high`/`medium`/`low`, the validator
  reads `risks = artifact_data.get("risks_identified", [])` (line 262) and,
  `if confidence in ("low", "medium")` and `risks` is falsy or an empty
  list, appends `error_id:
  "architectural_review_recommendation.risks_identified.logic_error"`
  (`error_type: logic_error`, default `severity="error"`, i.e. blocking).
  This check is UNCONDITIONAL with respect to `decision` -- it is not nested
  inside any `decision`-specific `elif` branch, unlike every other
  required-field check this family has exercised.
  EMPIRICALLY CONFIRMED TWICE this session: (1) direct validator invocation
  (`python scripts/validate-architectural-review-recommendation.py <file>
  --repo-root . --json`) against a constructed
  `architectural_review_recommendation` with `decision: investigate_first`,
  `investigation_steps` populated, `confidence: low`, `artifact_id`,
  `created_at`, `created_by` all present, and `risks_identified` OMITTED
  entirely, produced exactly one error:
  `architectural_review_recommendation.risks_identified.logic_error:
  Confidence 'low' should be supported by identified risks.` (`valid:
  false`); adding a populated `risks_identified` (nothing else changed)
  produced `valid: true`, zero errors. (2) THE SAME fixture content, with
  the `## Machine-readable decision` heading added, dispatched through the
  REAL orchestrator via `t3h-n9g-review-handoff-workflow`
  (`--from-session artifacts/t3h-n9g-session`, `--mode
  autonomous_execution`, `--executor dry-run`): console printed `[FAIL]
  Validation failed` /
  `architectural_review_recommendation.risks_identified.logic_error:
  Confidence 'low' should be supported by identified risks.`, step 3
  `FAILED`, ledger recorded `validation_completed(step_id: "3", status:
  failed, exit_code: 1)` / `step_completed(step_id: "3", status: failed)`.
  `decision: investigate_first` does not start with `"pursue"`, so the
  separate `success_measures` check at lines 278-293 cannot also fire and
  bundle a second error into the same validator-stack entry.
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first, then
  step 2 (`repo-sensemaker`) must complete and genuinely VALIDATE, BOTH in
  the SAME initial invocation -- this family's "more than one step before
  the failure" HIGH criterion.
  Step 1: because it declares no `output_artifact`, `execute_step()`'s
  artifact/validator branches never activate for it (the `if
  output_artifact:` guard at line 889 is skipped, the `if artifact_path and
  os.path.exists(artifact_path):` guard at line 1022 is False, the `elif
  output_artifact and output_artifact != "N/A":` guard at line 1048 is also
  False). Execution falls straight to gate management (line 1065); for
  `autonomous_execution` the step finishes at line 1086 with
  `result["status"] = "VALIDATED"`. The ledger carries exactly
  `step_started`/`step_completed` for `step_id: "1"` -- no
  `artifact_created`/`validation_completed`, since no artifact path ever
  exists for this step. This is the identical step-1 shape this family's
  T3M-K7X, T3M-H4Q, T3M-L8R, T3H-Q8N, and T3H-Z1V already establish and
  empirically verify end to end.
  Step 2: `repository_sensemaking_brief` must satisfy `validate-brief.py` in
  full (`primary_fog_type` a valid enum value, `evidence` non-empty with a
  real citation, `recommended_workflow_id` a real registry id, a well-formed
  correctly-grounded `evidence_excerpts` block, exactly one top-level
  `weakness_type` key). EMPIRICALLY CONFIRMED end to end (real orchestrator
  dispatch, this session, via `--from-session artifacts/t3h-n9g-session`
  with the brief pre-placed at
  `artifacts/t3h-n9g-session/repository_sensemaking_brief.md`): console
  printed `[OK] Validation passed`, step 2 `VALIDATED`, and the ledger
  recorded the full `step_started` / `artifact_created` (hash
  `aa7be3399fbbfeea6719a0e0890867c911a1646b197a52e9eea78fc16fe3bf9c`) /
  `validation_completed(status: passed, exit_code: 0)` /
  `step_completed(status: validated)` sequence for `step_id: "2"`.
failure_producing_condition: |
  POST-REVIEW REVISED: step 3's `architectural_review_recommendation` is
  PRE-PLACED CONTENT, directly at its session-scoped contract-resolved path
  (`<from-session-dir>/architectural_review_recommendation.md`) -- NOT
  fixture content via `--use-fixtures` (there is no fixture-map entry for
  this artifact type at the frozen SHA;
  `_get_fixture_artifact_path()`'s `skill_map`,
  `scripts/workflow-runtime.py:1365-1370`, only covers `problem_frame`,
  `unknowns_map`, `repository_sensemaking_brief`, `session_summary`), and
  NOT organically authored by a live-dispatched agent (this spec uses
  `--executor dry-run`, which never invokes a real skill for any output
  artifact at all -- `DryRunSkillExecutor.supports_real_execution = False`
  means `execute_step()`'s real-execution branch, line 915, is always
  skipped). The machine YAML sets `decision: investigate_first` with
  `investigation_steps` populated (so that decision-specific branch passes
  cleanly) and `confidence: low`, but OMITS `risks_identified` entirely,
  while every other required field is valid (`artifact_id`, `created_at`,
  `created_by`), UNDER the required `## Machine-readable decision` heading
  (see `verified_failed_boundary`'s note on the outer dispatcher's
  authoritative-block requirement). EMPIRICALLY CONFIRMED (see
  `verified_failed_boundary`): this produces exactly one validator error,
  `risks_identified.logic_error`; adding only a populated `risks_identified`
  (nothing else touched) resolves the artifact to `valid: true`, zero
  errors, BOTH in direct validator invocation and through the real
  orchestrator.
recovery_invocation: |
  POST-REVIEW REVISED (fixes the `--from-session` bootstrap gap; both
  invocations EMPIRICALLY RE-RUN end to end this session, real CLI dispatch
  against a disposable scratch clone, not just instantiation):

  BEFORE invocation 1: create a FIXED (non-auto-numbered) session directory,
  `<scratch-clone-root>/artifacts/t3h-n9g-session/`, and populate it with
  four files -- `00-user-intent.md` (required by `initialize_from_session()`'s
  existence check, lines 346-352), `proposed_direction.md`, a VALID
  `repository_sensemaking_brief.md` (matching `pre_failure_completed_work_expectations`),
  and a DELIBERATELY-BROKEN `architectural_review_recommendation.md`
  (matching `failure_producing_condition`) -- exact content given in
  `initial_state_specification`. Commit this directory before dispatch.

  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "T3H-N9G construction verification" --repo-root <scratch-clone-root>
  --workflow t3h-n9g-review-handoff-workflow --mode autonomous_execution
  --executor dry-run --from-session artifacts/t3h-n9g-session`. No explicit
  `--log-dir` is needed: `initialize_from_session()` (line 363-364) sets
  `self.log_dir = from_session_path` whenever `self.log_dir` still equals
  its plain-default value, which it does here. EMPIRICALLY CONFIRMED this
  session: console showed steps 1 and 2 both `VALIDATED`
  (`[OK] Validation passed` for step 2's brief), then step 3 genuinely
  reached its real validator and printed `[FAIL] Validation failed` /
  `architectural_review_recommendation.risks_identified.logic_error:
  Confidence 'low' should be supported by identified risks.`; run exited
  with `Status: failed`, `Steps: 2/3`.

  BEFORE `--resume`: the git working tree must be returned to clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`, and invocation 1
  always leaves the tree dirty (new run-log/ledger/diagnostic/implementation/
  workflow_summary files inside `artifacts/t3h-n9g-session/` itself -- since
  `--from-session` reuses the pre-built directory rather than creating a new
  numbered one -- plus a modified `docs/mode-coverage.yaml`). Commit this new
  state. Then correct
  `artifacts/t3h-n9g-session/architectural_review_recommendation.md` in
  place (add a populated `risks_identified` list, nothing else touched;
  exact content in `initial_state_specification`) and commit again, since
  step 3's genuine retry re-reads that same session-scoped path.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "T3H-N9G
  construction verification" --repo-root <scratch-clone-root> --workflow
  t3h-n9g-review-handoff-workflow --mode autonomous_execution --executor
  dry-run --from-session artifacts/t3h-n9g-session --log-dir
  artifacts/t3h-n9g-session --resume`. `--from-session` is REQUIRED again
  (not just `--log-dir`): it is what makes `self.artifact_session_dir`
  resolve to the SAME directory a second time, so step 3's genuine retry
  finds the SAME `proposed_direction.md` and the SAME
  `repository_sensemaking_brief.md` (step 2's `input_artifact` dependency)
  that invocation 1 used -- omitting `--from-session` on the resumed
  invocation would let `create_intent_artifact = True` (the else-branch in
  `main()` when `--from-session` is absent) auto-generate a DIFFERENT,
  freshly-numbered session directory, in which none of the pre-placed
  content would exist, reproducing the identical deadlock this fix resolves.
  `--log-dir artifacts/t3h-n9g-session` is passed explicitly for clarity,
  though `--from-session` alone would already set it to the same value.
  EMPIRICALLY CONFIRMED this session: console printed `[OK] Found resume
  state: 2 completed, paused at step None` / `[OK] Resuming: skipping steps
  [1, 2], starting from step 3`, steps 1 and 2 both printed "already
  completed in previous session, skipping (resume mode)", step 3 genuinely
  re-ran and printed `[OK] Validation passed`, run exited `Status:
  <completed>` / exit code 0.
resume_expectations: |
  `_find_resume_state()` (line 1951) parses invocation 1's run log. Steps
  1's AND 2's logged statuses (`VALIDATED`) are BOTH members of
  `_resumable_terminal_statuses()` (`{"VALIDATED", "COMPLETED"}` for
  autonomous_execution, lines 1916-1949), so BOTH are added to
  `completed_steps`. Step 3's logged status `FAILED` is excluded from both
  `completed_steps` and `paused_step` (lines 1973-1978) by the same
  membership-check construction, not a special-cased "skip FAILED" branch.
  `resume_skip` (line 2594) resolves to `{1, 2}` -- this family's "protect
  more than one prior completed step at once" criterion, structurally
  identical in mechanism to Tranche-1's T3H-W4J. In the step loop (lines
  2605-2624), steps 1 and 2 are BOTH skip-reconstructed synthetically (no
  `execute_step()` call for either, each hardcoding `"status": "COMPLETED"`,
  line 2617); step 3 is genuinely re-executed via `execute_step()` (line
  2623), re-invoking `architectural-review` and re-running the validator
  stack against the newly (pre-placed, corrected) `architectural_review_recommendation`.
  EMPIRICALLY CONFIRMED this session (real orchestrator dispatch, not just
  code tracing): console printed `[OK] Found resume state: 2 completed,
  paused at step None` and `[OK] Resuming: skipping steps [1, 2], starting
  from step 3`; the SINGLE shared `run-ledger.jsonl` (see `protected_work`)
  shows a second `run_started`...`run_completed` bracket containing ONLY
  `step_id: "3"` events (`step_started` -> `artifact_created` (a DIFFERENT
  hash from invocation 1's, since the file content changed) ->
  `validation_completed(status: passed, exit_code: 0)` ->
  `step_completed(status: validated)`) -- zero `step_id: "1"` or `step_id:
  "2"` events anywhere in that second bracket. The overwritten run log's
  final state shows steps 1 and 2 as `status: COMPLETED` (the synthetic
  literal, not `VALIDATED`) and step 3 as `VALIDATED`, matching this
  family's documented `write_run_log()` behavior exactly.
protected_work: |
  POST-REVIEW REVISED: because BOTH invocations use `--from-session
  artifacts/t3h-n9g-session` (the SAME fixed directory), `run-ledger.jsonl`
  is a SINGLE, shared, append-only file for the whole 2-invocation
  sequence -- NOT two separate per-invocation numbered directories the way
  every other spec in this family (which never passes `--from-session`)
  produces. EMPIRICALLY CONFIRMED this session: after both invocations, this
  ONE file contains exactly TWO `run_started`/`run_completed` brackets, both
  with `run_id: "t3h-n9g-session"` (identical, since it is derived from the
  fixed directory name -- NOT distinct auto-generated session ids), but
  distinguishable by their DIFFERENT `git_commit` field (the two invocations
  ran against different commits, since the tree was recommitted in between)
  and by chronological position in the file.
  BOTH prior steps' work must remain undisturbed, since neither is ever
  re-invoked on resume. Step 1 has no artifact, so its protected invariant
  is LEDGER SILENCE for `step_id: "1"` WITHIN THE SECOND BRACKET (the
  events between the second `run_started` and the following
  `run_completed`) -- EMPIRICALLY CONFIRMED: zero `step_id: "1"` events
  appear after the second `run_started` line. Step 2's
  `repository_sensemaking_brief.md` (at its fixed session-scoped path,
  `artifacts/t3h-n9g-session/repository_sensemaking_brief.md`) must remain
  byte-identical on disk between the failed and recovered attempts; this is
  independently checkable via the file's content hash recorded in the
  FIRST bracket's `artifact_created` event for `step_id: "2"`
  (`aa7be3399fbbfeea6719a0e0890867c911a1646b197a52e9eea78fc16fe3bf9c`) --
  EMPIRICALLY CONFIRMED: recomputing the file's SHA-256 after the resumed
  run produced the IDENTICAL hash. This is the specific
  TWO-independent-invariants case this family's "protect multiple prior
  steps at once" criterion requires: a bug that silently re-ran only ONE of
  the two prior steps must not be missed by checking only one of the two
  invariants -- an oracle must check the ledger-silence invariant for step 1
  AND the hash-identity invariant for step 2, independently, WITHIN the
  second bracket.
  The run log file (fixed at `artifacts/t3h-n9g-session/run_log_...md`,
  the SAME path `--from-session`/`--log-dir` both resolve to) is NOT a
  reliable preservation channel -- `write_run_log()` (line 1991) OVERWRITES
  it in place on every invocation; only the shared `run-ledger.jsonl`,
  read bracket-by-bracket, is reliable, per this family's established
  ledger-over-run-log convention (here applied within one file instead of
  across separate files).
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family: (1) `git reset
  --hard` / `git clean -fd` on the scratch clone between attempts --
  including following the runtime's own `rollback()` (line 2511-2521)
  printed advice, which fires automatically whenever `has_failures` is true;
  this would destroy both already-VALIDATED prior steps' work along with the
  shared ledger the resume mechanism needs; (2) deleting/truncating
  `run_log_t3h-n9g-review-handoff-workflow_autonomous_execution.md` or the
  shared `run-ledger.jsonl` and re-invoking without `--resume`; (3)
  hand-editing step 3's logged status from `FAILED` to `VALIDATED`/`APPROVED`
  in the run log to force it into skip-reconstruction instead of genuine
  retry. A fourth behavior specific to this multi-step shape is also
  forbidden: re-running steps 1 and/or 2 "just to be safe" via a fresh
  invocation instead of trusting `--resume`'s skip-reconstruction of BOTH --
  independently detectable via the two `protected_work` invariants, checked
  WITHIN the second bracket. A fifth behavior specific to this spec's
  failure mode is also forbidden: "fixing" the failure by switching
  `confidence` away from `low`/`medium` (e.g. to `high`) merely to escape
  the `risks_identified` requirement, rather than genuinely supplying
  `risks_identified` for the ORIGINAL confidence level -- independently
  detectable by confirming the resumed attempt's `confidence` field still
  reads `low` and that `risks_identified` is now genuinely populated. A
  sixth behavior, specific to this spec's `--from-session` bootstrap
  mechanism, is also forbidden: pointing invocation 2's `--from-session` at
  a DIFFERENT directory than invocation 1 used (e.g. a freshly
  auto-numbered one) -- this would not "recover" anything; it would either
  reproduce the original `ARTIFACT_NOT_FOUND` deadlock (no pre-placed
  content in the new directory) or silently fabricate an entirely
  disconnected run with no real resume relationship to invocation 1 at all,
  independently detectable by confirming both invocations' run-log/ledger
  paths resolve to the identical `artifacts/t3h-n9g-session/` directory.
idempotency_expectations: |
  POST-REVIEW REVISED: scoped to the SINGLE shared `run-ledger.jsonl`,
  split into its two `run_started`/`run_completed` brackets by
  chronological position (never by `run_id`, which is identical in both --
  the fixed session-directory name -- distinguish by position or by the
  differing `git_commit` field instead). `step_id: "1"` must show exactly
  ONE `step_started`/`step_completed` pair, located ONLY in the FIRST
  bracket. `step_id: "2"` must show exactly ONE full 4-event sequence
  ending `validated`/`passed`, ALSO located ONLY in the FIRST bracket -- a
  second occurrence of EITHER in the SECOND bracket would mean that step
  was silently re-executed rather than skip-reconstructed (this is the
  specific duplication risk this multi-step case introduces relative to a
  1-prior-step spec: two independent things to not duplicate, not one).
  `step_id: "3"` is expected to show ONE full sequence in EACH bracket:
  the first bracket ending `validation_completed(status: failed)` (the
  genuine `risks_identified.logic_error` result, `exit_code: 1`) /
  `step_completed(status: failed)`; the second bracket ending
  `validation_completed(status: passed, exit_code: 0)` /
  `step_completed(status: validated)` once `risks_identified` is genuinely
  populated -- EMPIRICALLY CONFIRMED, this exact pattern was observed, with
  DIFFERENT `artifact_created` hashes for step 3 across the two brackets
  (the file's content genuinely changed) but the IDENTICAL hash for step 2's
  `artifact_created` event (present only in the first bracket, absent from
  the second, per `protected_work`). Two `run_started`/`run_completed`
  pairs total in the one file (same `run_id`, different `git_commit`) is
  expected bookkeeping and must not be misclassified as duplicated semantic
  work.
oracle_requirements: |
  POST-REVIEW REVISED: because this spec uses a FIXED, spec-declared
  `--from-session` directory name (`artifacts/t3h-n9g-session`), a
  materialized oracle does NOT need the directory-filtering-by-workflow_id
  procedure this family's other (non-`--from-session`) specs require to
  separate their own runs from the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` dogfood directories -- this spec's own
  directory is uniquely named and never collides with the `NN-*` glob
  pattern `_create_user_intent_artifact()` uses, so there is no ambiguity to
  filter. The oracle instead reads the ONE file at
  `artifacts/t3h-n9g-session/run-ledger.jsonl` and splits it into brackets
  by `run_started`/`run_completed` event pairs (in order).
  Applying the seven-link recovery chain, using ONLY ledger content (never
  run-log content, which reflects only the latest overwrite): (1) the FIRST
  bracket shows step 3 genuinely reached FAILED via
  `risks_identified.logic_error` specifically (not a crash, not a different
  error, and not bundled with `success_measures`) -- parse the
  `validation_completed` event's associated console/validator output (or
  independently re-run the pre-placed artifact through
  `validate-architectural-review-recommendation.py --json`) for the exact
  error_id; (2) that same bracket's steps 1 AND 2 are BOTH
  `step_completed(status: validated)`, step 2 with a real brief that itself
  independently re-validates via `validate-brief.py`; (3) the SECOND
  bracket contains ZERO `step_id: "1"` AND ZERO `step_id: "2"` events of any
  kind, checked INDEPENDENTLY for each (a bug that silently re-ran only one
  of the two prior steps must not be missed by checking only one); (4) step
  2's artifact file hash (recomputed from the on-disk
  `repository_sensemaking_brief.md`) matches the hash logged in the FIRST
  bracket's `artifact_created` event exactly; (5) the SECOND bracket
  contains a step_id "3" sequence ending `validated`/`passed`; (6) the
  resumed attempt's `architectural_review_recommendation.md` (re-read from
  disk) now carries a populated `risks_identified` field, with `confidence`
  unchanged from the first attempt's value (`low`) and `decision` unchanged
  (`investigate_first`); (7) none of the `forbidden_reset_restart_behavior`
  items occurred, including the confidence-switching and
  different-`--from-session`-directory variants specific to this spec
  (checkable by confirming both brackets' surrounding run-log/ledger paths
  are the identical `artifacts/t3h-n9g-session/` directory).
complexity_breakdown: |
  HIGH because this is a 3-step workflow where steps 1 AND 2 both genuinely
  succeed before step 3 fails -- this family's first HIGH criterion (more
  than one step before the failure), EMPIRICALLY confirmed this session
  (real CLI dispatch, not just code tracing) to resolve `resume_skip` to
  `{1, 2}` via the same verified code mechanism Tranche-1's T3H-W4J already
  exercises. This is strictly harder than a 1-prior-step MEDIUM spec in the
  same concrete ways T3H-W4J documents: `resume_skip` really is a pair, not
  a singleton; `protected_work` requires and was given TWO independent
  invariants (ledger silence for step 1, hash identity for step 2), either
  of which could fail independently; and `idempotency_expectations` rules
  out silent re-execution of EITHER prior step. DISTINCT FROM T3H-W4J
  concretely: the failing step's own defect is a genuine, isolated
  CONTENT-dependent cross-field check (`risks_identified.logic_error`,
  unconditional on `decision`, gated only by `confidence`) rather than
  T3H-W4J's content-INDEPENDENT generic-validator `--json` crash -- this
  spec never touches `scripts/validate-artifact.py` at all, and its
  recovery therefore never depends on a repository-level code fix the way
  T3H-W4J's does. The step-1/step-2 content pairing (no-op + real
  validating brief) also differs from T3H-W4J's (real brief + real
  recommendation), so the two specs' `protected_work` checks exercise
  genuinely different artifact shapes. This spec's HIGH-ness is entirely
  about the multi-step `resume_skip` mechanism; the `--from-session`
  bootstrap mechanism (fixed this construction session) is an operational
  precondition for reaching that mechanism at all, not itself a source of
  difficulty distinct from the declared HIGH criterion.
initial_state_specification: |
  POST-REVIEW REVISED: A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` (under the
  top-level `workflows:` key):

    id: t3h-n9g-review-handoff-workflow
    display_name: T3H-N9G Review Handoff (pilot-scoped)
    purpose: Disposable pilot-only 3-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (multi-step protection, risks_identified
      cross-field failure).
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
        skill: repo-sensemaker
        step_type: local_execution
        gate: review_diagnosis
        input_source: repository_state
        output_artifact: repository_sensemaking_brief
      - id: 3
        skill: architectural-review
        step_type: local_execution
        gate: review_recommendation
        input_artifact: repository_sensemaking_brief
        input_source: proposed_direction
        output_artifact: architectural_review_recommendation

  EMPIRICALLY VERIFIED THIS SESSION: this exact entry, added to a scratch
  registry copy in a disposable scratch clone, was loaded by directly
  instantiating `OrchestrationRunner(...)` (zero mode errors) AND by a full
  real CLI dispatch end to end (see `recovery_invocation`).

  PLUS a pre-built, FIXED-name session directory,
  `artifacts/t3h-n9g-session/`, created and committed BEFORE invocation 1,
  containing:

  `00-user-intent.md` -- any well-formed `user_intent` artifact satisfying
  `initialize_from_session()`'s existence check (content is not otherwise
  validated by that check).

  `proposed_direction.md` -- a short, scoped architectural proposal, e.g.
  "Add response caching to the validator dispatcher
  (`scripts/validate-and-report.py`'s `invoke_validator()`) so repeated
  validation calls against unchanged artifact content within a single
  orchestration run skip redundant subprocess spawns." Its mere non-empty
  presence at this exact path is what satisfies
  `_resolve_step_inputs()`'s `resolved_inputs["proposed_direction"]["present"]`
  check (line 1471, `bool(f.read().strip())`).

  `repository_sensemaking_brief.md` -- the SAME well-formed, fully-validating
  brief content used throughout this family (valid `primary_fog_type`,
  non-empty `evidence`, a real `recommended_workflow_id`, a
  correctly-grounded `evidence_excerpts` entry citing
  `scripts/workflow-runtime.py:L97-L98`, `weakness_type: "Contract
  Mismatch"` appearing exactly once). EMPIRICALLY CONFIRMED end to end (real
  orchestrator dispatch): this content's on-disk SHA-256 is
  `aa7be3399fbbfeea6719a0e0890867c911a1646b197a52e9eea78fc16fe3bf9c`, logged
  identically in the ledger's `artifact_created` event for `step_id: "2"`
  and unchanged after the resumed run.

  `architectural_review_recommendation.md` -- for INVOCATION 1, this file
  MUST include a `## Machine-readable decision` heading (NOT "## 13.
  Machine-readable handoff" -- that heading pattern is for
  `repository_sensemaking_brief`/plans; this artifact type uses the
  `decision` variant of the same shared regex in
  `validate-and-report.py:58-60`, confirmed against the real fixture at
  `tests/fixtures/architectural-review-recommendation/fixture-valid-investigate-first.md`)
  immediately above the YAML fence, with:

    artifact_id: architectural_review_recommendation
    decision: investigate_first
    investigation_steps:
      - "Prototype the caching layer against a representative validator workload"
      - "Measure p95 latency before/after on the existing dispatcher benchmark"
    confidence: low
    created_at: "2026-08-20T00:00:00Z"
    created_by: "t3h-n9g-review-handoff-workflow"

  (deliberately omitting `risks_identified`). EMPIRICALLY CONFIRMED end to
  end (real orchestrator dispatch): this produces step 3 `FAILED` with
  exactly `risks_identified.logic_error`.

  BEFORE `--resume`, this SAME file must be corrected in place -- add
  `risks_identified: ["Prototype may not represent production load
  characteristics"]`, nothing else touched -- and recommitted.
  EMPIRICALLY CONFIRMED: this correction alone (re-dispatched via
  `--resume`) resolved step 3 to `VALIDATED`.

  `workflow-registry.yaml`'s pre-existing entries must otherwise be left
  unmodified from the frozen SHA. `--use-fixtures` is NOT used anywhere in
  this spec's dispatch (see `failure_producing_condition`); all four files
  above are placed directly at their session-scoped, contract-resolved (or,
  for `00-user-intent.md`/`proposed_direction.md`, `--from-session`-anchored)
  paths.
spec_sha256: f07eec606edee993f6cecc87b4d0c9b8e51c0c08ef1238a10ae378234da6f359
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Computed with PyYAML safe_load + hashlib.sha256("".join(str(v) for v in
  # fields)) over this file's final content (recomputed after the
  # post-review --from-session fix; see the construction session's
  # verification script).
qualification: |
  ADMISSIBLE
