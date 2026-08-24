candidate_id: T3M-L8R
family: T3
complexity_level: MEDIUM
source_workflow_or_operation: |
  A bespoke 2-step workflow, `t3m-l8r-diagnostic-setup-workflow`, assembled
  VERBATIM from the real registered `setup-sensemaking-repo`'s steps 1-2
  only (frozen SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5,
  `skills/workflow-planner/references/workflow-registry.yaml:109-126`), with
  one explicit addition: `allowed_execution_modes: [autonomous_execution]`.
  Same disqualifying reason and same fix as this family's T3M-K7X /
  T3M-H4Q: `setup-sensemaking-repo`'s own `allowed_execution_modes` at the
  frozen SHA (registry lines 105-108) is `[plan_only, prompt_chain,
  guided_execution]` -- no `autonomous_execution` -- so
  `_load_registries()` (`scripts/workflow-runtime.py:401-428`, the
  `MODE_NOT_ALLOWED` check at lines 418-426) would abort the run before
  step 1 ever executes if the real workflow entry were used unmodified.
  CONFIRMED by direct re-inspection of the frozen-SHA registry entry (lines
  105-108) as part of this construction task.
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` (copied
      verbatim from registry lines 110-114).
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief` (copied verbatim from registry lines
      115-120).
  Step 3 of the real `setup-sensemaking-repo` (`handoff` -> `session_summary`)
  is dropped by construction, not by convention -- it cannot execute, so it
  cannot contaminate this spec with the generic validator's unrelated
  `--json` argparse crash (the bug class the disposable T3 pilot and this
  family's T3H-W4J already exercise; neither reachable here).
  This is the same bespoke 2-step slice T3M-H4Q also uses (a distinct
  registry id, `t3m-l8r-diagnostic-setup-workflow`, so the two specs'
  ledgers can never be confused with each other by workflow_id filtering
  if both run against the same clone) -- what makes this spec a genuinely
  different scenario is an entirely different validator code branch (see
  `verified_failed_boundary`): a structural field-TYPE check, not a
  file-existence check.
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`), invoked with `--json`
  (accepted by validate-brief.py's own argparse), so this does not crash.
  The real failure condition here is `WEAKNESS_TYPE_MALFORMED`
  (`scripts/validate-brief.py:662-669`): once `artifact_data` is parsed and
  a top-level `weakness_type` key is present and non-None (so the
  `WEAKNESS_TYPE_MISSING` warning-only branch at lines 652-660 does not
  apply), the validator checks `isinstance(weakness_type, str)`; if this is
  False, it appends `_code_error(WEAKNESS_TYPE_MALFORMED, f"'weakness_type'
  must be a string, got {type(weakness_type).__name__}: {weakness_type!r}",
  field="weakness_type", severity="error")` (lines 664-669) -- an explicit,
  BLOCKING error, unlike every other `weakness_type`-related check in this
  same function (`WEAKNESS_TYPE_MISSING`, `WEAKNESS_TYPE_UNKNOWN`,
  `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`, `WEAKNESS_TYPE_PROSE_MISMATCH`,
  `HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT`, all `severity="warning"` per
  the code comment at lines 609-613: "Taxonomy is required metadata but
  non-blocking (D2): missing/unrecognized/prose-mismatched values are
  warnings only ... Only a malformed field (wrong YAML type) is blocking,
  since that is a structural defect rather than a taxonomy-completeness
  gap"). This is a genuinely different underlying cause and code branch
  from every other `repository_sensemaking_brief` failure already used in
  this family (T3M-K7X: `recommended_workflow_id.unknown_value`; T3H-Z1V:
  `primary_fog_type.unknown_value` then `evidence.logic_error`; T3H-Q8N:
  `EVIDENCE_QUOTE_NOT_FOUND`; T3M-H4Q: `HALLUCINATED_FILE`) -- it is a
  YAML-type check on a field that is present and non-empty, not a
  missing-field, unknown-enum-value, empty-list, or citation-grounding
  check. `validation_json["valid"]` becomes False via the same
  `execute_step()` / `_run_validator_stack()` / `_run_validate_and_report()`
  chain cited throughout this family (`scripts/workflow-runtime.py` lines
  1023, 1038-1046), and `result["status"] = "FAILED"` is set for step 2,
  halting the run (`run()` lines 2626-2631).

  EMPIRICALLY CONFIRMED (direct validator invocation, this construction
  session, frozen-SHA archive extracted from `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`): a constructed brief,
  otherwise identical to a fully-valid baseline (valid `primary_fog_type`,
  non-empty `evidence`, a real `recommended_workflow_id`, `created_at`,
  `immutable: true`, a correctly-grounded `evidence_excerpts` entry citing
  an existing file), but with `weakness_type: ["Contract Mismatch"]` (a
  YAML list, not a string) in the `## 13. Machine-readable handoff` block,
  run through `python scripts/validate-brief.py <file> --repo-root .
  --json`, produced exactly one error: `WEAKNESS_TYPE_MALFORMED:
  'weakness_type' must be a string, got list: ['Contract Mismatch']`
  (`valid: false`). The IDENTICAL fixture with only `weakness_type` changed
  back to the plain string `"Contract Mismatch"` produced `valid: true`,
  zero errors -- confirming the isolation: this is the ONLY error the
  fixture produces.
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first.
  Identically to T3M-K7X's and T3M-H4Q's step 1: no `output_artifact` means
  `execute_step()`'s artifact/validator branches (lines 889, 1022, 1048)
  never activate, execution falls straight to gate management (line 1065),
  and for `autonomous_execution` the step finishes with
  `result["status"] = "VALIDATED"` (line 1086). The run log's `### Step 1`
  block logs status `VALIDATED`; the ledger carries only `step_started` and
  `step_completed` events for `step_id: "1"` (no `artifact_created` /
  `validation_completed`, since there is no artifact).
failure_producing_condition: |
  The step-2 `repository_sensemaking_brief` is FIXTURE CONTENT placed as
  part of this spec's initial state (via `--use-fixtures` pointing at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`,
  `--executor dry-run`), not asserted to be organically produced by a
  live-dispatched `repo-sensemaker` invocation. As with T3M-H4Q, this spec
  makes the fixture-content framing explicit rather than relying on any
  specific live agent's behavior. `scripts/brief_skeleton.py`'s
  `reconcile_evidence_excerpt_quotes()` (issue #89) is irrelevant here
  regardless -- it only ever touches `evidence_excerpts[].quote` fields
  (confirmed by reading `scripts/brief_skeleton.py:336-396`), never the
  top-level `weakness_type` field this spec's failure depends on -- but
  `--use-fixtures --executor dry-run` is used anyway for consistency with
  this family's established, safe dispatch pattern for fixture-sourced
  content (T3M-H4Q, T3H-Q8N, T3H-W4J).

  The fixture's `## 13. Machine-readable handoff` block is otherwise fully
  valid: `artifact_id: repository_sensemaking_brief`, `primary_fog_type:
  architecture_fog`, a non-empty `evidence` list, `recommended_workflow_id:
  architecture-implementation-workflow` (a real registry id), `created_at`,
  `immutable: true` -- but `weakness_type` is set to the YAML list
  `["Contract Mismatch"]` instead of the plain string `"Contract
  Mismatch"`. A separately-headed `## 5. Evidence` section contains a
  correctly formed, correctly grounded `evidence_excerpts` YAML block
  citing a real, existing file and a validly-formatted line range with a
  quote genuinely present at that location, so `HALLUCINATED_FILE`,
  `INVALID_LINE_FORMAT`, and `EVIDENCE_QUOTE_NOT_FOUND` cannot fire and be
  confused with this spec's target failure. The prose includes a "logic
  trace" marker and a file-level citation in the Evidence section so those
  separate structural checks also pass cleanly. EMPIRICALLY CONFIRMED (see
  `verified_failed_boundary`): this isolates the brief to exactly one
  blocking error, `WEAKNESS_TYPE_MALFORMED`; changing only `weakness_type`
  back to a plain string (nothing else touched) resolved the fixture to
  `valid: true`, zero errors.
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3m-l8r-diagnostic-setup-workflow --mode autonomous_execution
  --use-fixtures --executor dry-run` (no `--log-dir`; defaults to the
  auto-generated session directory under `artifacts/`). Ends with step 2
  FAILED (`WEAKNESS_TYPE_MALFORMED`).

  BEFORE `--resume`: the git working tree must be returned to clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`, and a
  completed invocation always leaves the tree dirty (the new, untracked
  `artifacts/NN-orchestration-run/` ledger directory, plus a modified
  `docs/mode-coverage.yaml`). Commit this new state before `--resume`.
  Also correct the fixture at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`
  (change `weakness_type` from the list `["Contract Mismatch"]` to the
  plain string `"Contract Mismatch"`, nothing else) before recommitting,
  since step 2's genuine retry re-reads that same fixture path.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  t3m-l8r-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume
  --use-fixtures --executor dry-run`. `--log-dir` must point at the
  directory holding invocation 1's
  `run_log_t3m-l8r-diagnostic-setup-workflow_autonomous_execution.md`
  (`_find_resume_state()`, line 1956, builds the path from
  `self.log_dir`). `--log-dir` only controls where the PRIOR run log is
  read from for resume-state discovery -- the new attempt's own
  `run-ledger.jsonl` goes to a freshly auto-generated session directory
  (`_generate_session_id()`, line 151) unless `--from-session` is also
  passed. `--use-fixtures --executor dry-run` is required again for the
  same reason as invocation 1.
resume_expectations: |
  `_find_resume_state()` (line 1951) parses invocation 1's run log. Step
  1's logged status `VALIDATED` is in `_resumable_terminal_statuses()`
  (`{"VALIDATED", "COMPLETED"}` for autonomous_execution, lines 1916-1949)
  and is added to `completed_steps`; step 2's logged status `FAILED` is
  excluded from both `completed_steps` and `paused_step` (lines 1973-1978)
  by the same membership-check construction, not a special-cased "skip
  FAILED" branch. `resume_skip` (line 2594) resolves to `{1}`. In the step
  loop (lines 2605-2624): step 1 is skip-reconstructed synthetically (lines
  2606-2621, no `execute_step()` call, hardcoded `"status": "COMPLETED"`,
  line 2617); step 2 is genuinely re-executed via `execute_step()` (line
  2623), re-invoking `repo-sensemaker` (via the fixture path again) and
  re-running `_run_validator_stack()` against the corrected fixture.
  Because this bespoke workflow has exactly 2 steps, the step loop ends
  after step 2 succeeds.
protected_work: |
  Step 1 has no output artifact (identical shape to T3M-K7X and T3M-H4Q),
  so the protected invariant is LEDGER SILENCE for `step_id: "1"`: the
  resumed invocation's own fresh `run-ledger.jsonl` (a separate,
  auto-incrementing numbered directory, independent of `--log-dir`) must
  contain no new `step_started`, `artifact_created`, `validation_completed`,
  or `step_completed` events for `step_id: "1"`. The first attempt's run
  log file is NOT a reliable preservation channel: `write_run_log()` (line
  1991, path built at line 1995 from `self.log_dir`) OVERWRITES that same
  fixed file in place on every invocation, since `--resume` must reuse the
  identical `--log-dir`. After the resumed run, that file shows only the
  latest state; invocation 1's `FAILED` record for step 2 is gone from it.
  Only `run-ledger.jsonl`, in each invocation's own separate numbered
  directory, is a reliable, isolated, never-overwritten record.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family: (1)
  `git reset --hard` / `git clean -fd` on the scratch clone between
  attempts -- the runtime's own `rollback()` (line 2511-2521) prints
  exactly this advice after every FAILED run; following it would destroy
  the ledger directories the resume mechanism depends on; (2)
  deleting/truncating
  `run_log_t3m-l8r-diagnostic-setup-workflow_autonomous_execution.md` or
  any `run-ledger.jsonl` and re-invoking without `--resume`; (3)
  hand-editing step 2's logged status from `FAILED` to
  `VALIDATED`/`COMPLETED` to force it into skip-reconstruction instead of
  genuine retry. A fourth behavior specific to this spec's failure mode is
  also forbidden: "fixing" the failure by changing `weakness_type`'s VALUE
  to some other list, dict, or non-string type ("as long as it's not the
  exact same list") rather than genuinely converting the field to a plain
  string -- independently detectable by re-running the real validator
  against the resumed attempt's brief and confirming `isinstance(data.get
  ("weakness_type"), str)` is true, not merely that the reported error
  message text changed. Committing invocation 1's own run artifacts (new
  ledger directory, updated `docs/mode-coverage.yaml`) to restore a clean
  tree before `--resume` is REQUIRED operational hygiene, not reset
  laundering.
idempotency_expectations: |
  Across the combined ledger record (invocation 1's file plus invocation
  2's file, read together), `step_id: "1"` must show exactly ONE
  `step_started`/`step_completed` pair (from invocation 1 only) -- a second
  occurrence in invocation 2's ledger would mean step 1 was silently
  re-executed rather than skip-reconstructed. `step_id: "2"` is expected to
  show TWO full sequences: invocation 1's ending
  `validation_completed(status: failed)` (the genuine
  `WEAKNESS_TYPE_MALFORMED` result) / `step_completed(status: failed)`,
  invocation 2's ending `validation_completed(status: passed)` /
  `step_completed(status: validated)` once `weakness_type` is genuinely a
  string -- that second sequence is the legitimate retry, not duplicate
  work. One `run_started`/`run_completed` pair per invocation is expected
  bookkeeping. Because this workflow has exactly 2 steps, any `step_id:
  "3"` event anywhere would be a structural anomaly, not legitimate work.
oracle_requirements: |
  A materialized oracle must first isolate this spec's own invocations from
  the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories and from any other
  T3-family spec's own bespoke-workflow directories. Filter by reading each
  candidate directory's `run-ledger.jsonl` first line and matching
  `event == "run_started"`.`workflow_id ==
  "t3m-l8r-diagnostic-setup-workflow"` exactly -- never by directory
  position/number.
  Applying the seven-link recovery chain, using ONLY ledger content: (1)
  the chronologically-first matching directory's ledger shows step 2
  genuinely reached FAILED via `WEAKNESS_TYPE_MALFORMED` specifically (not
  a crash, not `WEAKNESS_TYPE_MISSING`/`WEAKNESS_TYPE_UNKNOWN`, which are
  non-blocking warnings and could not have produced a FAILED step at all);
  (2) that same ledger's step 1 status is `step_completed(status:
  validated)`; (3) the chronologically-LAST matching directory's ledger
  contains ZERO `step_id: "1"` events of any kind; (4) that same ledger
  contains a fresh step_id "2" sequence ending `validated`/`passed`; (5)
  the resumed run's step 2 brief has a `weakness_type` field that the
  oracle itself independently confirms `isinstance(..., str)` (re-parsing
  the YAML directly, not merely trusting the validator's own report); (6)
  the fixed `--log-dir` path's run log, read only for its latest state,
  shows step 2 as `VALIDATED`; (7) none of the
  `forbidden_reset_restart_behavior` items occurred, including the
  wrong-type-substitution variant specific to this spec.
complexity_breakdown: |
  MEDIUM: exactly one failing step (step 2) out of two total steps; the fix
  is a single, unambiguous type correction (change a YAML list to a plain
  string) with no branching logic and no interaction with any other field.
  This is a structurally distinct failure class from every other
  `repository_sensemaking_brief` scenario in this family: not a
  missing-field check (T3M-K7X's `recommended_workflow_id`), not an
  unknown-enum-value check (T3H-Z1V's `primary_fog_type`), not an
  empty-collection check (T3H-Z1V's `evidence`), not a
  file-existence/grounding check (T3M-H4Q's `HALLUCINATED_FILE`, T3H-Q8N's
  `EVIDENCE_QUOTE_NOT_FOUND`), but a YAML-type/structural-validity check on
  a field whose VALUE is otherwise present and would-be-acceptable content
  wrapped in the wrong container type. Step 1 contributes no validation
  surface at all, keeping the "earlier completed work" precondition trivial
  to satisfy and verify.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml` (under the
  top-level `workflows:` key):

    id: t3m-l8r-diagnostic-setup-workflow
    display_name: T3M-L8R Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (malformed weakness_type field type).
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
      - file: scripts/workflow-runtime.py
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
    weakness_type: ["Contract Mismatch"]
    ```

  The `evidence_excerpts` YAML block is placed under its own `## 5.
  Evidence` heading, separate from `## 13. Machine-readable handoff`'s own
  fence -- required for the same structural reason T3M-H4Q's
  `initial_state_specification` documents (EMPIRICALLY DISCOVERED this
  construction session): co-locating both YAML fences inside the same
  `##`-delimited section causes
  `weakness_type_safeguard.extract_single_yaml_fence()` to see two
  candidate blocks in one section and report a contaminating, unrelated
  `MALFORMED_FENCE` error before the `weakness_type`-specific checks this
  spec targets are ever reached.
  For the RESUME attempt, this same fixture file must be corrected in
  place (only `weakness_type` changed from `["Contract Mismatch"]` to
  `"Contract Mismatch"`; nothing else touched) before `--resume` is
  invoked -- see `recovery_invocation`. `workflow-registry.yaml`'s
  pre-existing entries must otherwise be left unmodified from the frozen
  SHA.
spec_sha256: a9faaeb428d364974e6a66da44a98afd62fe0b754cf4f818831b9e021cf87c78
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
