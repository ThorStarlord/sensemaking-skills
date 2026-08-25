candidate_id: T3H-X7M
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  A bespoke 2-step workflow, `t3h-x7m-diagnostic-setup-workflow`, assembled
  VERBATIM from the real registered `setup-sensemaking-repo`'s steps 1-2
  only (frozen SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5,
  `skills/workflow-planner/references/workflow-registry.yaml:110-120`), with
  one explicit addition: `allowed_execution_modes: [autonomous_execution]`.
  Same disqualifying reason as this family's other bespoke-from-`setup-sensemaking-repo`
  specs: `setup-sensemaking-repo`'s own `allowed_execution_modes` at the
  frozen SHA is `[plan_only, prompt_chain, guided_execution]` -- no
  `autonomous_execution`. EMPIRICALLY CONFIRMED THIS SESSION, not merely
  read from the registry: the bespoke entry (a fresh, distinct registry id
  from every other spec in this family, so ledger-based filtering can never
  conflate this spec's THREE invocations with anyone else's) was inserted
  into a scratch copy of `workflow-registry.yaml` in a disposable scratch
  clone of the frozen SHA, and `OrchestrationRunner` was DIRECTLY
  INSTANTIATED (not dispatched through `main()`, and not merely read as
  YAML) against it:
  `OrchestrationRunner(workflow_id="t3h-x7m-diagnostic-setup-workflow",
  mode="autonomous_execution", repo_root=".", executor="dry-run")` produced
  `runner.errors == []` -- no `MODE_NOT_ALLOWED`. In the SAME script, the
  identical instantiation method run against the real
  `setup-sensemaking-repo` with `mode="autonomous_execution"` DID correctly
  produce `MODE_NOT_ALLOWED`, confirming the check discriminates rather than
  vacuously passing everything -- directly answering this construction
  task's standing instruction to verify `allowed_execution_modes` claims by
  actually instantiating `OrchestrationRunner`, the exact category of bug
  that broke two earlier specs in this family.
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact`.
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief`.
  Step 3 of the real `setup-sensemaking-repo` is dropped by construction, so
  it can never contaminate this spec with the generic validator's unrelated
  `--json` argparse crash.
  What makes this a genuinely different scenario from this family's other
  double-resume HIGH spec (Tranche-1's T3H-Z1V, which chains
  `primary_fog_type.unknown_value` then `evidence.logic_error`, both
  top-level required-field/enum checks): this spec's two successive
  failures both live inside the SAME `evidence_excerpts[]` per-excerpt
  validation block (`scripts/validate-brief.py:751-773`) but are two
  STRUCTURALLY DISTINCT checks within it -- attempt 1 fails a line-range
  SYNTAX check (`INVALID_LINE_FORMAT`), attempt 2 (produced during the FIRST
  `--resume`) fails a per-excerpt REQUIRED-FIELD-PRESENCE check
  (`EVIDENCE_EXCERPT_FIELD`) -- neither of which T3H-Z1V, nor any other
  spec in this family, uses as its PRIMARY failure. This family's "recovery
  verified under a second resume" HIGH criterion is exercised here through a
  different pair of underlying defects than Z1V's, testing that the SAME
  `_resumable_terminal_statuses()` `"COMPLETED"`-literal mechanism (see
  `resume_expectations`) correctly recognizes a synthetically-reconstructed
  step 1 a second time, independent of which specific validator checks are
  driving step 2's two successive failures.
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`), invoked with `--json`
  (accepted by validate-brief.py's own argparse), so this does not crash --
  the same non-crashing routing path used throughout this family.
  Attempt 1's failure: `INVALID_LINE_FORMAT`
  (`scripts/validate-brief.py:765-773`). For the one `evidence_excerpts[]`
  entry, `lines = exc.get("lines")` is checked against
  `re.match(r"^L?\d+(?:-L?\d+)?$", str(lines).strip())`; a value using a
  colon instead of a dash (`L100:L102`) does not match, so
  `_code_error(INVALID_LINE_FORMAT, ...)` is appended (default
  `severity="error"`, blocking). Critically, this check runs BEFORE the
  downstream quote-grounding search (`_quote_found_near()`, only reached
  `if ... and lines_valid and quote`, line 781-789) -- an invalid `lines`
  syntax pre-empts that entire code path, so `EVIDENCE_QUOTE_NOT_FOUND`
  cannot also fire here.
  EMPIRICALLY CONFIRMED: a fixture with `file: scripts/workflow-runtime.py`
  (a real, existing file, so `HALLUCINATED_FILE` does not fire), `lines:
  L100:L102`, and a real, verbatim quote from that file's actual line 101
  (`"autonomous_execution": "VALIDATED",`), run through `python
  scripts/validate-brief.py <file> --repo-root . --json`, produced exactly
  one error: `INVALID_LINE_FORMAT: Excerpt[0] has invalid lines format:
  L100:L102 (expected a line number or range, e.g. L18, 18, L25-L30, or
  25-30)` (`valid: false`).
  Attempt 2's failure (produced during `--resume` #1, after `lines` is
  corrected to the valid `L100-L102`): `EVIDENCE_EXCERPT_FIELD`
  (`scripts/validate-brief.py:751-754`). The per-excerpt required-field loop
  (`for field in ["file", "lines", "quote", "supports_claim"]: if field not
  in exc:`) fires when `supports_claim` is entirely absent from the excerpt
  dict, appending `_code_error(EVIDENCE_EXCERPT_FIELD, f"Excerpt[{i}]
  missing required field: supports_claim")` (default severity, blocking).
  This check is a simple dict-membership test, structurally distinct from
  `INVALID_LINE_FORMAT`'s regex check and from the downstream quote-grounding
  search -- with `lines` now valid and the same real, correctly-grounded
  quote present, the quote-grounding search at lines 786-798 DOES run and
  DOES succeed (confirmed below), so `EVIDENCE_QUOTE_NOT_FOUND` cannot also
  fire and bundle a second error into this attempt.
  EMPIRICALLY CONFIRMED: the IDENTICAL fixture with `lines` corrected to
  `L100-L102` but `supports_claim` removed entirely (file and quote
  unchanged) produced exactly one error: `EVIDENCE_EXCERPT_FIELD:
  Excerpt[0] missing required field: supports_claim` (`valid: false`).
  Attempt 3's success: the IDENTICAL fixture with `supports_claim` restored
  (nothing else changed from attempt 2's corrected `lines`) produced `valid:
  true`, zero errors -- confirming both defects are genuinely independent,
  single-cause, and cleanly isolated in sequence. All three fixtures'
  validator invocations were run directly against a frozen-SHA archive
  extracted via `git archive 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5` this
  construction session.
  Both attempt-1 and attempt-2 failures flip `validation_json["valid"]` to
  False via the identical `execute_step()` / `_run_validator_stack()` /
  `_run_validate_and_report()` chain cited throughout this family
  (`scripts/workflow-runtime.py` lines 1023, 1038-1046), and
  `result["status"] = "FAILED"` is set for step 2 each time, halting the run.
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully ONLY ONCE,
  in the FIRST (non-resumed) invocation -- and must NEVER be genuinely
  re-executed on EITHER subsequent `--resume`, matching this family's
  established double-resume shape (Tranche-1's T3H-Z1V). No `output_artifact`
  means `execute_step()`'s artifact/validator branches (lines 889, 1022,
  1048) never activate; for `autonomous_execution` the step finishes with
  `result["status"] = "VALIDATED"` (line 1086). Invocation 1's own numbered
  ledger directory must record exactly `step_started` then
  `step_completed(status: validated, gate_status: automated_approval)` for
  `step_id: "1"` -- nothing else. Neither `--resume` #1's nor `--resume`
  #2's own fresh ledger may contain any `step_id: "1"` event of any kind --
  this is the specific "double opportunity for the bug to occur" this
  family's third HIGH criterion introduces: a single-resume spec can only
  ever check step-1 non-duplication once, this spec checks it twice,
  independently.
failure_producing_condition: |
  Attempt 1: the step-2 brief's one `evidence_excerpts[]` entry cites a
  real, existing file (`scripts/workflow-runtime.py`) with a genuinely
  verbatim quote from its real line 101, but with `lines: L100:L102` (a
  colon in place of the required dash), while every other Phase-1 field
  (`primary_fog_type`, `evidence`, `recommended_workflow_id`, logic trace,
  file-level citation, `weakness_type`) is populated validly -- isolating
  attempt 1 to exactly one error, `INVALID_LINE_FORMAT`.
  Attempt 2 (produced during `--resume` #1): `lines` corrected to the
  syntactically valid `L100-L102`, but the excerpt's `supports_claim` field
  is omitted entirely, with every other field (including `file` and the
  same real, correctly-grounded `quote`) still valid -- isolating attempt 2
  to exactly one, DIFFERENT error, `EVIDENCE_EXCERPT_FIELD`. This is the
  realistic failure mode this family's T3H-Z1V also models: an agent that
  fixes the reported defect (the line-format syntax) while introducing or
  leaving a second, previously-masked one (the quote-grounding search never
  even ran on attempt 1, since `INVALID_LINE_FORMAT` pre-empted it, so
  `EVIDENCE_EXCERPT_FIELD`'s absence on attempt 1 was never itself confirmed
  as a pass -- it was simply unreached).
  Attempt 3 (produced during `--resume` #2): `supports_claim` restored,
  `lines` still valid from attempt 2 -- all checks pass.
  EMPIRICALLY CONFIRMED at every step (see `verified_failed_boundary`):
  three separate fixture files, each validated in isolation via
  `validate-brief.py --json` before being described here, each producing
  exactly the predicted single error (or zero errors, for attempt 3).
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-x7m-diagnostic-setup-workflow --mode autonomous_execution
  --use-fixtures --executor dry-run` (no `--log-dir`; defaults to the
  auto-generated session directory). Ends with step 2 FAILED
  (`INVALID_LINE_FORMAT`).

  BEFORE `--resume` #1: the git tree must be recommitted clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`, and every
  completed invocation leaves the tree dirty (new untracked ledger
  directory, plus a modified `docs/mode-coverage.yaml`). This spec's THREE
  invocations therefore require commits after invocation 1 AND after
  `--resume` #1 -- twice as many required commits as a single-resume spec.
  Also correct the fixture's `lines` field from `L100:L102` to `L100-L102`
  (nothing else touched) before recommitting.

  `--resume` #1: `python scripts/workflow-runtime.py "<same problem
  statement>" --repo-root <scratch-clone-root> --workflow
  t3h-x7m-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume
  --use-fixtures --executor dry-run`. `--log-dir` points
  `_find_resume_state()` (line 1956) at invocation 1's run log. Ends with
  step 2 FAILED again (`EVIDENCE_EXCERPT_FIELD`); the run log at the SAME
  fixed path is OVERWRITTEN in place (see `protected_work`) -- critical for
  what `--resume` #2 reads next.

  BEFORE `--resume` #2: recommit the tree clean again (new ledger directory
  from `--resume` #1, updated `docs/mode-coverage.yaml`, overwritten run
  log). Also add back the fixture's `supports_claim` field (nothing else
  touched) before recommitting.

  `--resume` #2 (the "resume of an already-resumed run"): `python
  scripts/workflow-runtime.py "<same problem statement>" --repo-root
  <scratch-clone-root> --workflow t3h-x7m-diagnostic-setup-workflow --mode
  autonomous_execution --log-dir <scratch-clone-root>/artifacts/<SAME
  invocation-1-session-dir -- NOT a different directory> --resume
  --use-fixtures --executor dry-run`. `--log-dir` is the SAME path used for
  `--resume` #1 -- there is only ever ONE run-log location for this whole
  3-invocation sequence, fixed at whatever `--log-dir` resolved to on
  invocation 1, reused verbatim every time (`--resume` always writes back to
  `self.log_dir`, which never changes once explicitly set on the CLI, per
  this family's T3H-Z1V, already empirically confirmed end to end for the
  identical mechanism). Ends with step 2 VALIDATED.
resume_expectations: |
  `--resume` #1: `_find_resume_state()` (line 1951) parses invocation 1's
  run log. Step 1's logged status `VALIDATED` is in
  `_resumable_terminal_statuses()` (lines 1916-1949) and is added to
  `completed_steps`. `resume_skip` (line 2594) resolves to `{1}`. Step 1 is
  skip-reconstructed (lines 2606-2621): the synthetic result dict hardcodes
  `"status": "COMPLETED"` (line 2617, a LITERAL string, not
  `MODE_CEILINGS[self.mode]`). `write_run_log()` then writes THIS
  invocation's own new run log content (to the SAME fixed path) with step
  1's block showing `- **status**: COMPLETED`, not `VALIDATED`. Step 2 is
  genuinely re-executed via `execute_step()` (line 2623) and fails again,
  this time `EVIDENCE_EXCERPT_FIELD`.

  `--resume` #2: `_find_resume_state()` parses the SAME fixed-path run log,
  which by now holds `--resume` #1's OVERWRITTEN content -- step 1 status
  `COMPLETED` (not `VALIDATED`). This is exactly why
  `_resumable_terminal_statuses()` explicitly includes the `"COMPLETED"`
  literal alongside the mode's own ceiling status (its own docstring, lines
  1928-1932, states this is written for exactly this "chained resume"
  case -- the identical mechanism this family's T3H-Z1V already empirically
  confirms end to end). Because `"COMPLETED"` is a member of the set, step 1
  is STILL correctly recognized as resumable -- `resume_skip` again resolves
  to `{1}`. Step 1 is skip-reconstructed a SECOND time (never genuinely
  executed a second or third time, across all three invocations). Step 2's
  logged status `FAILED` (from `--resume` #1's genuine re-execution) is
  again excluded from `completed_steps`, so step 2 is genuinely re-executed
  a THIRD time, and this time passes (`supports_claim` restored, `lines`
  still valid, the same real quote still grounded).
protected_work: |
  There is no "two separate run-log locations" to diff, and run-log content
  is not a preservation channel at all: `_find_resume_state()` and
  `write_run_log()` both resolve the run-log path from the SAME
  `self.log_dir` (lines 1956, 1995); because `--resume` MUST reuse the
  identical `--log-dir` to find prior state, EVERY invocation after the
  first OVERWRITES that ONE fixed file in place. After `--resume` #1, it
  holds attempt-2's state (step 1 `COMPLETED`, step 2 `FAILED` with the
  `EVIDENCE_EXCERPT_FIELD` error); after `--resume` #2, it holds attempt-3's
  state (step 1 `COMPLETED`, step 2 `VALIDATED`). Attempt 1's original
  `FAILED`-for-`INVALID_LINE_FORMAT` record is NOT preserved anywhere in
  run-log form after `--resume` #1 overwrites it.
  The reliable, isolated preservation channel is `run-ledger.jsonl`: EACH of
  the three invocations gets its OWN fresh, auto-incrementing numbered
  directory (`artifacts/NN-orchestration-run/`), independent of
  `--log-dir`, created on every invocation including resumes, and never
  overwritten.
  The protected invariant, across ALL THREE ledgers: `step_id: "1"` must
  appear in EXACTLY ONE of the three ledgers (invocation 1's), never in
  `--resume` #1's or `--resume` #2's own ledger.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family, explicitly at
  BOTH transition points (attempt1->2 AND attempt2->3), not just once: (1)
  `git reset --hard` / `git clean -fd` between any two attempts -- the
  runtime's own `rollback()` prints this advice after every FAILED run
  (both attempt 1 and attempt 2 trigger it); (2) deleting/truncating the run
  log or any `run-ledger.jsonl` and re-invoking without `--resume`; (3)
  hand-editing either run-log overwrite's step 2 status from `FAILED` to
  `VALIDATED`/`COMPLETED`. A fourth behavior specific to this spec: pointing
  `--resume` #2's `--log-dir` at anything other than the ONE fixed path used
  since invocation 1 -- there is no alternate valid directory to point at.
  A fifth behavior specific to this spec's two-defect content shape is also
  forbidden: "fixing" attempt 1's `INVALID_LINE_FORMAT` by deleting the
  entire `evidence_excerpts[]` entry and adding a NEW, differently-shaped
  one (rather than correcting the existing entry's `lines` field in place),
  and likewise "fixing" attempt 2's `EVIDENCE_EXCERPT_FIELD` by fabricating
  a new excerpt from scratch rather than adding the missing
  `supports_claim` field to the SAME excerpt -- independently detectable by
  confirming the `file` and `quote` values remain identical across all
  three attempts' fixtures (only `lines` changes between attempt 1 and 2;
  only `supports_claim`'s presence changes between attempt 2 and 3).
  Committing each invocation's own run artifacts to restore a clean tree
  between invocations is REQUIRED operational hygiene, not reset laundering.
idempotency_expectations: |
  Scoped entirely to ledger content, across the THREE separate ledger files
  (one per invocation, read together): `step_id: "1"` must show exactly ONE
  `step_started`/`step_completed` pair, located ONLY in invocation 1's
  ledger -- ZERO occurrences in `--resume` #1's ledger and ZERO in
  `--resume` #2's ledger. A single occurrence in either resumed ledger would
  mean step 1 was silently, genuinely re-executed rather than
  skip-reconstructed -- and because this spec has TWO resumes, there are TWO
  independent opportunities for that bug to occur, both of which a
  single-resume spec cannot exercise. `step_id: "2"` is expected to show
  exactly THREE full sequences, one per invocation's own ledger: invocation
  1 ending `validation_completed(status: failed)` (`INVALID_LINE_FORMAT`);
  `--resume` #1's ledger ending the same way but for
  `EVIDENCE_EXCERPT_FIELD`; `--resume` #2's ledger ending
  `validation_completed(status: passed)` / `step_completed(status:
  validated)`. All three are legitimate retries, not duplicates. Three
  `run_started`/`run_completed` pairs total (distinct `run_id` values) are
  expected bookkeeping.
oracle_requirements: |
  A materialized oracle must first isolate THIS spec's own three
  invocations from the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories AND from any other
  T3-family spec's own bespoke-workflow directories, if multiple specs' runs
  happen to run against the same clone. Filter by reading each candidate
  directory's `run-ledger.jsonl` first line and matching `event ==
  "run_started"`.`workflow_id == "t3h-x7m-diagnostic-setup-workflow"`
  exactly -- never by directory position/number. Order the matched
  directories chronologically (by ledger timestamp, not directory number) to
  identify invocation 1, `--resume` #1, and `--resume` #2 as
  first/middle/last.
  Applying the seven-link recovery chain across three attempts, using ONLY
  ledger content: (1) the first matching ledger's step 2 reached FAILED via
  `INVALID_LINE_FORMAT` specifically; (1b, this spec's extension) the SECOND
  matching ledger's step 2 ALSO reached FAILED, but via the DIFFERENT
  `EVIDENCE_EXCERPT_FIELD` -- confirming these are different defects, not
  the same one re-reported (which would indicate the agent's `--resume` #1
  fix did nothing); (2) the first ledger's step 1 status is `validated`;
  (2b) the SECOND matching ledger contains ZERO `step_id: "1"` events
  (confirming skip-reconstruction during `--resume` #1); (3) the THIRD
  matching ledger ALSO contains ZERO `step_id: "1"` events (confirming
  skip-reconstruction held on the SECOND resume too -- the check a
  single-resume spec structurally cannot perform); (4) the third ledger
  contains a fresh step_id "2" sequence ending `validated`/`passed`; (5) the
  third attempt's brief has a `lines` value the oracle independently
  confirms matches `^L?\d+(?:-L?\d+)?$` AND a `supports_claim` field
  present in the same excerpt, AND that `file`/`quote` are unchanged across
  all three attempts (per the fabricated-new-excerpt pitfall in
  `forbidden_reset_restart_behavior`); (6) none of the
  `forbidden_reset_restart_behavior` items occurred at EITHER transition
  (git reflog spanning all three invocations; confirm no alternate
  `--log-dir` was ever used for `--resume` #2).
complexity_breakdown: |
  HIGH because recovery is verified not just for the immediate retry but
  for idempotency under a SECOND resume of an already-resumed run -- this
  family's third HIGH criterion, structurally identical in MECHANISM to
  Tranche-1's T3H-Z1V (the same `_resumable_terminal_statuses()`
  `"COMPLETED"`-literal design decision, `workflow-runtime.py:1928-1932`)
  but exercised over a DIFFERENT pair of underlying content defects: both
  of this spec's two failures live inside the SAME
  `evidence_excerpts[]`-entry validation block
  (`scripts/validate-brief.py:751-773`) rather than T3H-Z1V's two
  TOP-LEVEL field checks (`primary_fog_type`, `evidence`), and are
  themselves two structurally distinct sub-checks within that block (a
  regex syntax check vs. a dict-membership presence check) rather than two
  independent enum/emptiness checks. A `--resume` #2 reads a run log whose
  step 1 entry was ITSELF synthetically written by `--resume` #1, never
  genuinely re-validated -- a single-resume spec can never exercise this
  code path at all, since its one resumed run's step 1 entry is always read
  from an ORIGINAL (non-synthetic) `VALIDATED` log line. The two content
  failures (attempt 1, attempt 2) are each individually simple in
  isolation, deliberately so, keeping the double-resume mechanism itself,
  not failure-content novelty, the primary source of this spec's HIGH
  rating -- though the specific pairing of two different `evidence_excerpts[]`
  sub-checks (never used as a PRIMARY failure by any other spec in this
  family) is itself a genuinely new concrete scenario, per this construction
  task's distinctness requirement.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS a
  bespoke workflow entry committed before dispatch:

    id: t3h-x7m-diagnostic-setup-workflow
    display_name: T3H-X7M Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (double-resume idempotency, two distinct
      evidence-excerpt defects).
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

  EMPIRICALLY VERIFIED THIS SESSION: this exact entry, added to a scratch
  registry copy in a disposable scratch clone, was loaded by directly
  instantiating `OrchestrationRunner(workflow_id="t3h-x7m-diagnostic-setup-workflow",
  mode="autonomous_execution", ...)` and produced zero errors.
  PLUS `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`
  (overwriting whatever is there at the frozen SHA) set, for the FIRST
  invocation, to:

    # Repository Sensemaking Brief

    ## 1. Summary
    <fixture summary prose>. This brief includes a logic trace: the
    diagnosis below walks from evidence to conclusion step by step.

    ## 5. Evidence
    See `scripts/workflow-runtime.py:100` for the cited mode-ceiling entry.

    ```yaml
    evidence_excerpts:
      - file: scripts/workflow-runtime.py
        lines: L100:L102
        quote: "\"autonomous_execution\": \"VALIDATED\","
        supports_claim: "Autonomous execution's mode ceiling is VALIDATED."
    ```

    ## 6. Weakest boundary
    <prose mentioning "Contract Mismatch">

    ## 13. Machine-readable handoff
    ```yaml
    artifact_id: repository_sensemaking_brief
    primary_fog_type: architecture_fog
    evidence:
      - "scripts/workflow-runtime.py:100 (mode-ceiling entry)"
    recommended_workflow_id: architecture-implementation-workflow
    created_at: "<timestamp>"
    immutable: true
    weakness_type: "Contract Mismatch"
    ```

  EMPIRICALLY CONFIRMED (direct `validate-brief.py --json` invocation this
  session): this exact fixture produces exactly one error,
  `INVALID_LINE_FORMAT` (`Excerpt[0] has invalid lines format: L100:L102`).
  For `--resume` #1, `lines` is corrected in place to `L100-L102`, nothing
  else touched -- EMPIRICALLY CONFIRMED this alone still leaves the fixture
  invalid, now with exactly one DIFFERENT error,
  `EVIDENCE_EXCERPT_FIELD: Excerpt[0] missing required field:
  supports_claim`, because this corrected version additionally has
  `supports_claim` removed from the excerpt (the deliberate second defect;
  see `failure_producing_condition`). For `--resume` #2, `supports_claim`
  is added back (`"Autonomous execution's mode ceiling is VALIDATED."`,
  nothing else touched) -- EMPIRICALLY CONFIRMED this resolves the fixture
  to `valid: true`, zero errors. `workflow-registry.yaml`'s pre-existing
  entries must otherwise be left unmodified from the frozen SHA.
spec_sha256: c85ed6f8bdf41856a5101debd16b624e09720c1cd744b40c4829cad23c4d8a1c
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Computed with PyYAML safe_load + hashlib.sha256("".join(str(v) for v in
  # fields)) over this file's final content (recomputed after all edits;
  # see the construction session's verification script).
qualification: |
  ADMISSIBLE
