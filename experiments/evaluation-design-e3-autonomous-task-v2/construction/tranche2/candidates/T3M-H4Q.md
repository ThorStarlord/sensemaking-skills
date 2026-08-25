candidate_id: T3M-H4Q
family: T3
complexity_level: MEDIUM
source_workflow_or_operation: |
  A bespoke 2-step workflow, `t3m-h4q-diagnostic-setup-workflow`, assembled
  VERBATIM from the real registered `setup-sensemaking-repo`'s steps 1-2
  only (frozen SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5,
  `skills/workflow-planner/references/workflow-registry.yaml:109-126`), with
  one explicit addition: `allowed_execution_modes: [autonomous_execution]`.
  This is REQUIRED, not optional: `setup-sensemaking-repo`'s own
  `allowed_execution_modes` at the frozen SHA (registry lines 105-108) is
  `[plan_only, prompt_chain, guided_execution]` -- `autonomous_execution` is
  absent, so `_load_registries()` (`scripts/workflow-runtime.py:401-428`,
  the `MODE_NOT_ALLOWED` check at lines 418-426) would append an error and
  the run would abort in `main()` before `run()` is ever called, before step
  1 executes, before any run log or ledger exists. CONFIRMED by direct
  re-inspection of the frozen-SHA registry entry (lines 105-108) as part of
  this construction task, per the standing instruction to check
  `allowed_execution_modes` on any named real workflow before writing a
  spec around it.
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` (copied
      verbatim from registry lines 110-114).
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief` (copied verbatim from registry lines
      115-120).
  Step 3 of the real `setup-sensemaking-repo` (`handoff` -> `session_summary`,
  registry lines 121-126) is dropped by construction, not by convention --
  it is not part of this bespoke entry at all, so it can never execute and
  can never contaminate this spec with the generic validator's unrelated
  `--json` argparse crash (the same bug class the disposable T3 pilot's own
  scenario exercises for `unknowns_map`, and this family's T3H-W4J exercises
  for `session_summary` -- neither is reachable here by construction, so
  this spec cannot be mistaken for a reskin of either).
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`, which special-cases
  `artifact_id == "repository_sensemaking_brief"` before any artifact would
  fall through to the generic `--json`-crashing `validate-artifact.py`).
  `invoke_validator()` calls it with `[artifact_path, --repo-root, --json]`;
  validate-brief.py's own argparse defines `--json`, so this does not crash.
  The real failure condition here is the `HALLUCINATED_FILE` check inside
  the per-excerpt loop over the brief's `evidence_excerpts` YAML block
  (`scripts/validate-brief.py:751-763`): for each excerpt, if its `file`
  field does not start with `file:///`, the validator joins it onto
  `citation_root` (`repo_root` here, no `--target-repo` supplied) and checks
  `os.path.exists(full_path)`; if the resulting path does not exist, it
  appends `_code_error(HALLUCINATED_FILE, f"Excerpt[{i}] references
  non-existent file: {file_path}")` (line 763), a blocking error (default
  severity, confirmed via `_is_blocking()` and `_code_error`'s default
  `severity="error"`). This check runs and fires BEFORE the deterministic
  quote-grounding search (`_quote_found_near()`, lines 780-798) is ever
  reached -- structurally distinct from T3H-Q8N's `EVIDENCE_QUOTE_NOT_FOUND`
  scenario in this same family, which requires the cited file to EXIST and
  the `lines` syntax to be valid so the grounding search can even run;
  `HALLUCINATED_FILE` is a much simpler, single-condition existence check
  that pre-empts that entire downstream code path. `validation_json["valid"]`
  becomes False via the same `execute_step()` / `_run_validator_stack()` /
  `_run_validate_and_report()` chain cited throughout this family
  (`scripts/workflow-runtime.py` lines 1023, 1038-1046), and
  `result["status"] = "FAILED"` is set for step 2, halting the run (`run()`
  lines 2626-2631).

  EMPIRICALLY CONFIRMED (direct validator invocation, this construction
  session, frozen-SHA archive extracted from `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`): a constructed brief with a
  well-formed `## 13. Machine-readable handoff` block (valid
  `primary_fog_type`, non-empty `evidence`, a real `recommended_workflow_id`,
  `created_at`, `immutable: true`, a valid string `weakness_type`), a
  `## 5. Evidence` section containing a separately-headed `evidence_excerpts`
  YAML block citing a real, existing file/line range with a correctly
  grounded quote, EXCEPT the excerpt's `file` field set to
  `scripts/this_file_does_not_exist_anywhere.py` (a path that does not exist
  anywhere in the frozen-SHA tree), run through `python
  scripts/validate-brief.py <file> --repo-root . --json`, produced exactly
  one error: `HALLUCINATED_FILE: Excerpt[0] references non-existent file:
  scripts/this_file_does_not_exist_anywhere.py` (`valid: false`). The
  IDENTICAL fixture with only the `file` field changed to the real,
  existing `scripts/workflow-runtime.py` (quote and line range otherwise
  unchanged, still correctly grounded) produced `valid: true`, zero errors,
  confirming the isolation: this is the ONLY error the fixture produces, not
  one of several firing together (the exact failure mode T3M-P4W's own
  post-review correction warns about and requires checking for).
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first.
  Because it declares no `output_artifact`, `execute_step()`'s
  artifact/validator branches never activate for it: `output_artifact` is
  falsy, so the `if output_artifact:` guard at line 889 is skipped
  (`artifact_path` stays `""`), the `if artifact_path and
  os.path.exists(artifact_path):` guard at line 1022 is False, and the
  `elif output_artifact and output_artifact != "N/A":` guard at line 1048 is
  also False. Execution falls straight to gate management (line 1065);
  assuming the gate auto-approves (mode: autonomous_execution, an
  automated-gate mode), the step finishes at line 1086 with
  `result["status"] = "VALIDATED"` (`MODE_CEILINGS["autonomous_execution"]
  == "VALIDATED"`). The run log's `### Step 1` block logs status
  `VALIDATED`. Ledger-wise, step 1 gets exactly `step_started` (lines
  864-869) and `step_completed` (line 1091 region) events for `step_id:
  "1"` -- no `artifact_created` or `validation_completed` events, since no
  artifact path ever exists for this step. This is the same step-1 shape
  already established and empirically verified end-to-end (real orchestrator
  runs) by this family's T3M-K7X, T3H-Q8N, and T3H-Z1V, all of which use
  the identical `setup-sensemaking-skills`-as-step-1 slice.
failure_producing_condition: |
  The step-2 `repository_sensemaking_brief` is FIXTURE CONTENT placed as
  part of this spec's initial state (via `--use-fixtures` pointing at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`,
  `--executor dry-run`), not something asserted to be organically produced
  by a live-dispatched `repo-sensemaker` invocation. This is a deliberate,
  explicit choice (per the standing lesson that a scenario needing specific
  wrong content must say so plainly): while `scripts/brief_skeleton.py`'s
  `reconcile_evidence_excerpt_quotes()` (issue #89) only overwrites each
  excerpt's `quote` field from real on-disk content (confirmed by reading
  `scripts/brief_skeleton.py:336-396`: it reads `item.get("file")` and
  `item.get("lines")` to extract a quote, but never reassigns `file` or
  `lines` themselves) -- so a hallucinated `file` field would in principle
  survive even real dispatch -- this spec does not rely on that survival
  being guaranteed for any specific live agent's behavior. Using
  `--use-fixtures --executor dry-run` sidesteps the question entirely
  (`reconcile_evidence_excerpt_quotes()` only runs inside the real
  `claude-code` executor's `invoke_skill()` path, never for fixture-sourced
  artifacts), matching the same safe, explicit dispatch pattern this
  family's T3H-Q8N and T3H-W4J already establish.

  The fixture's `## 13. Machine-readable handoff` block is otherwise fully
  valid: `artifact_id: repository_sensemaking_brief`, `primary_fog_type:
  architecture_fog`, a non-empty `evidence` list, `recommended_workflow_id:
  architecture-implementation-workflow` (a real registry id),
  `created_at`, `immutable: true`, and `weakness_type: "Contract Mismatch"`
  (a valid string, a real taxonomy term). A separately-headed `## 5.
  Evidence` section contains a correctly formed `evidence_excerpts` YAML
  block: `lines: L97-L98` (a validly-formatted, real range in
  `scripts/workflow-runtime.py`, the two `MODE_CEILINGS` dict-entry lines
  at that location at the frozen SHA), a `quote` field that IS grounded
  within the +/-3-line window of that range, and `supports_claim` present
  -- but the excerpt's `file` field is set to
  `scripts/this_file_does_not_exist_anywhere.py`, a path that does not
  exist anywhere in the frozen-SHA tree. The prose includes a "logic trace"
  marker and a file-level citation in the Evidence section (both required
  by separate, non-`HALLUCINATED_FILE` structural checks) so those checks
  also pass cleanly and cannot be confused with this spec's target failure.
  EMPIRICALLY CONFIRMED (see `verified_failed_boundary`): this isolates the
  brief to exactly one blocking error, `HALLUCINATED_FILE`; changing only
  the `file` field to the real, existing `scripts/workflow-runtime.py`
  (nothing else touched) resolved the fixture to `valid: true`, zero
  errors.
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3m-h4q-diagnostic-setup-workflow --mode autonomous_execution
  --use-fixtures --executor dry-run` (no `--log-dir`; defaults to the
  auto-generated session directory under `artifacts/`). Ends with step 2
  FAILED (`HALLUCINATED_FILE`).

  BEFORE `--resume`: the git working tree must be returned to clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`
  (lines 550-556), and a completed invocation always leaves the tree dirty
  (the new, untracked `artifacts/NN-orchestration-run/` ledger directory,
  plus a modified `docs/mode-coverage.yaml` from Phase 5). Commit this new
  state (the ledger directory and the mode-coverage update) before
  `--resume` -- this is required operational hygiene for chaining any two
  invocations of this runner in a mutating mode against a git-backed repo
  root, not specific to this spec's content fix. Also correct the fixture
  at `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`
  (change the excerpt's `file` field to the real
  `scripts/workflow-runtime.py`, nothing else) before recommitting, since
  step 2's genuine retry re-reads that same fixture path.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  t3m-h4q-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume
  --use-fixtures --executor dry-run`. `--log-dir` must point at the
  directory holding invocation 1's
  `run_log_t3m-h4q-diagnostic-setup-workflow_autonomous_execution.md`, since
  `_find_resume_state()` (line 1956) builds the path to read as
  `os.path.join(self.log_dir, f"run_log_{self.workflow_id}_{self.mode}.md")`.
  `--log-dir` only controls where the PRIOR run log is read from for
  resume-state discovery -- it does NOT control where the new attempt's own
  ledger goes; absent `--from-session`, a fresh `artifact_session_dir` (and
  thus a fresh `run-ledger.jsonl`) is auto-generated via
  `_generate_session_id()` (line 151) for this second invocation.
  `--use-fixtures --executor dry-run` is required again for the same reason
  as invocation 1.
resume_expectations: |
  `_find_resume_state()` (line 1951) parses invocation 1's run log with the
  regex at lines 1969-1972. Step 1's logged status `VALIDATED` is a member
  of `_resumable_terminal_statuses()` (line 1916-1949, which returns
  `{MODE_CEILINGS["autonomous_execution"], "COMPLETED"}` ==
  `{"VALIDATED", "COMPLETED"}`), so step 1 goes into `completed_steps`.
  Step 2's logged status `FAILED` is in neither `resumable_statuses` nor
  equal to `"PAUSED"`, so it is excluded from both `completed_steps` and
  `paused_step` (lines 1973-1978) -- by construction of the membership
  check, not a special-cased "skip FAILED" branch.
  In `run()`, `resume_skip` (line 2594) resolves to `{1}`, not `{1, 2}`.
  The step loop (lines 2605-2624): for i=1 (in `resume_skip`), a synthetic
  result is appended without calling `execute_step()` (lines 2606-2621,
  hardcoding `"status": "COMPLETED"`, line 2617); for i=2 (not in
  `resume_skip`), `execute_step()` is called again for real (line 2623),
  genuinely re-invoking `repo-sensemaker` (via the fixture path again, per
  `--use-fixtures`) and re-running `_run_validator_stack()` against the
  corrected fixture. Because this bespoke workflow has exactly 2 steps, the
  step loop ends after step 2 succeeds -- no step 3 of any kind exists to
  genuinely execute or fail for an unrelated reason.
protected_work: |
  Step 1 has no output artifact, so there is no artifact file to compare
  byte-for-byte. The protected invariant is LEDGER SILENCE for `step_id:
  "1"`: the new invocation's `run-ledger.jsonl` (its own fresh, separate,
  auto-incrementing numbered directory, independent of `--log-dir`, per the
  substrate note) must contain no new `step_started`, `artifact_created`,
  `validation_completed`, or `step_completed` events carrying `"step_id":
  "1"`. The first attempt's run log file itself (the one `--log-dir` points
  at) is NOT a reliable preservation channel: `write_run_log()` (line 1991,
  path built at line 1995 from the same `self.log_dir`) OVERWRITES that
  same fixed file in place on every invocation, since `--resume` must reuse
  the identical `--log-dir` to find prior state at all. After the resumed
  run, that file shows only the latest state (step 1 `COMPLETED`, step 2
  `VALIDATED`) -- invocation 1's `FAILED` record for step 2 is gone from
  it. Only `run-ledger.jsonl`, in each invocation's own separate numbered
  directory, is a reliable, isolated, never-overwritten record; any
  `protected_work`/`idempotency_expectations` claim must be checked against
  ledger content, never run-log content.
forbidden_reset_restart_behavior: |
  Explicitly out of bounds: (1) `git reset --hard` / `git clean -fd` on the
  scratch clone between the failed and resumed attempts -- the runtime's
  own `rollback()` (line 2511-2521) prints exactly this advice after every
  FAILED run; following it would destroy the ledger directories the resume
  mechanism depends on; (2) deleting or truncating
  `run_log_t3m-h4q-diagnostic-setup-workflow_autonomous_execution.md` or any
  `run-ledger.jsonl` and re-invoking without `--resume` (a fresh,
  non-resumed run from scratch); (3) hand-editing the first attempt's run
  log to change step 2's logged status from `FAILED` to
  `VALIDATED`/`COMPLETED` so it gets synthetically skipped instead of
  genuinely retried. A fourth behavior specific to this spec's failure mode
  is also forbidden: "fixing" the failure by creating a dummy/placeholder
  file at the hallucinated path (`scripts/this_file_does_not_exist_anywhere.py`)
  so the citation technically resolves, instead of correcting the brief's
  own citation to point at a real, pre-existing repository file --
  independently detectable by confirming no new file was added to the
  scratch clone's tree between attempts (a git status/diff check) and that
  the corrected `file` field names a file that existed BEFORE this spec's
  first invocation, not one created during recovery. Committing invocation
  1's own run artifacts (new ledger directory, updated
  `docs/mode-coverage.yaml`) to restore a clean tree before `--resume` is
  REQUIRED operational hygiene, not reset laundering.
idempotency_expectations: |
  "No duplicate semantic work" means: after the resumed run completes,
  `run-ledger.jsonl` (invocation 1's file plus invocation 2's file, read
  together) must show exactly ONE `step_started`/`step_completed` pair for
  `step_id: "1"` (from invocation 1 only) -- a second occurrence for
  step_id "1" in invocation 2's ledger would indicate step 1 was silently
  re-executed rather than skip-reconstructed. For `step_id: "2"`, TWO
  occurrences of `step_started`/`artifact_created`/`validation_completed`/
  `step_completed` are expected and correct: invocation 1's sequence ending
  `validation_completed(status: failed)` (the genuine `HALLUCINATED_FILE`
  result) / `step_completed(status: failed)`, invocation 2's sequence ending
  `validation_completed(status: passed)` / `step_completed(status:
  validated)` once the `file` field is corrected -- that is the genuine
  retry, not a duplicate. One `run_started`/`run_completed` pair per
  invocation (two total, distinct session/run ids) is expected bookkeeping,
  not evidence of duplicate work. Because this workflow has exactly 2 steps,
  any `step_id: "3"` event appearing anywhere in either ledger would be a
  structural anomaly (wrong workflow definition loaded), not legitimate new
  work.
oracle_requirements: |
  A materialized oracle must first isolate this spec's own invocations from
  the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories (real, committed dogfood
  examples for unrelated workflows, e.g. `fast-local-diagnostic`,
  `full-local-sensemaking`) and from any other T3-family spec's own
  bespoke-workflow directories, if multiple specs' recovery attempts run
  against the same clone. Filter by reading each candidate directory's
  `run-ledger.jsonl` first line and matching `event == "run_started"`
  `.workflow_id == "t3m-h4q-diagnostic-setup-workflow"` exactly -- never by
  directory position/number, which interleaves pre-existing and other
  specs' directories unpredictably.
  Applying the seven-link recovery chain, using ONLY ledger content (never
  run-log content, which reflects only the latest overwrite): (1) the
  chronologically-first matching directory's ledger shows step 2 genuinely
  reached FAILED via `HALLUCINATED_FILE` specifically (parse the validator
  output for that error_id/message, not a crash and not a different error);
  (2) that same ledger's step 1 status is `step_completed(status:
  validated)`; (3) the chronologically-LAST matching directory's ledger
  contains ZERO `step_id: "1"` events of any kind; (4) that same ledger
  contains a fresh step_id "2" sequence ending `validated`/`passed`; (5) the
  resumed run's step 2 brief has an `evidence_excerpts[0].file` field that
  the oracle itself independently confirms exists on disk in the scratch
  clone (re-running `os.path.exists` against the same `citation_root` logic
  the real validator uses); (6) the fixed `--log-dir` path's run log, read
  ONLY for its latest state, shows step 2 as `VALIDATED`; (7) none of the
  `forbidden_reset_restart_behavior` items occurred, including the
  placeholder-file variant specific to this spec (git status/diff of the
  scratch clone across attempts must show no NEW file added at the
  previously-hallucinated path).
complexity_breakdown: |
  MEDIUM: exactly one failing step (step 2) out of two total steps; the fix
  is a single, unambiguous field-value change (replace the hallucinated
  `file` path with a real, pre-existing repository file) with no branching
  logic and no interaction with any other field. `HALLUCINATED_FILE` is
  structurally simpler than this family's HIGH-tier T3H-Q8N
  (`EVIDENCE_QUOTE_NOT_FOUND`): the file-existence check
  (`validate-brief.py:761-763`) is a single `os.path.exists()` call with no
  downstream windowed-search algorithm and no dependency on the exact
  on-disk content of a location outside the artifact's own claimed
  citation -- it fires or does not fire based on one boolean fact about the
  path itself. Step 1 contributes no validation surface at all (no
  `output_artifact`), keeping the "earlier completed work" precondition
  trivial to satisfy and verify, identically to T3M-K7X's step 1.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` (under the
  top-level `workflows:` key):

    id: t3m-h4q-diagnostic-setup-workflow
    display_name: T3M-H4Q Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (hallucinated evidence-file citation).
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

  PLUS the following content placed at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`
  (overwriting whatever is there at the frozen SHA) as this spec's own
  fixture, before dispatch:

    # Repository Sensemaking Brief

    ## 1. Summary
    <fixture summary prose>. This brief includes a logic trace: the
    diagnosis below walks from evidence to conclusion step by step.

    ## 5. Evidence
    See `scripts/workflow-runtime.py:97` for the cited MODE_CEILINGS block.

    ```yaml
    evidence_excerpts:
      - file: scripts/this_file_does_not_exist_anywhere.py
        lines: L97-L98
        quote: "MODE_CEILINGS = {"
        supports_claim: "Mode ceilings are defined as a dict."
    ```

    ## 6. Weakest boundary
    <prose mentioning "Contract Mismatch">

    ## 13. Machine-readable handoff
    ```yaml
    artifact_id: repository_sensemaking_brief
    primary_fog_type: architecture_fog
    evidence:
      - "scripts/workflow-runtime.py:97 (MODE_CEILINGS block)"
    recommended_workflow_id: architecture-implementation-workflow
    created_at: "<timestamp>"
    immutable: true
    weakness_type: "Contract Mismatch"
    ```

  The `evidence_excerpts` YAML block is placed under its own `## 5.
  Evidence` heading, separate from `## 13. Machine-readable handoff`'s own
  fence -- EMPIRICALLY DISCOVERED during this construction session:
  co-locating both YAML fences inside the SAME `##`-delimited section
  (e.g. both under Section 13) causes
  `weakness_type_safeguard.extract_single_yaml_fence()` to see two
  candidate blocks in one section and report `MALFORMED_FENCE`
  (`architectural_review_recommendation.weakness_type` -> blocking
  `MALFORMED_HANDOFF_FENCE`), an unrelated contaminating error that would
  make the fixture fail for the WRONG reason. Keeping the two fences under
  separate `##` headings (as in real, correctly-structured briefs) avoids
  this entirely and was confirmed empirically to produce a clean, isolated
  `valid: true` baseline before the `file` field is corrupted.
  For the RESUME attempt, this same fixture file must be corrected in place
  (only the `file` field changed to `scripts/workflow-runtime.py`; nothing
  else touched) before `--resume` is invoked -- see `recovery_invocation`.
  `workflow-registry.yaml`'s pre-existing entries (used for the
  `recommended_workflow_id` cross-reference check) must otherwise be left
  unmodified from the frozen SHA.
spec_sha256: 2690f9e9d60a02dc503fb056d65ea2a49da029efb58e97d4bec78a9a07f74990
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Computed with PyYAML safe_load + hashlib.sha256("".join(str(v) for v in
  # fields)) over this file's final content (verified by re-running the
  # same computation against the file on disk after all edits).
qualification: |
  ADMISSIBLE
