candidate_id: T3H-W4J
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  A bespoke 3-step workflow definition assembled by taking the real
  registered `architectural-review-planning-workflow` (frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5,
  `skills/workflow-planner/references/workflow-registry.yaml:942-979`) for
  its two steps, then appending one additional bespoke step 3:
    - Step 1: skill `repo-sensemaker`, gate `review_diagnosis`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief`.
    - Step 2: skill `architectural-review`, gate `review_recommendation`,
      `input_artifact: repository_sensemaking_brief`, `input_source:
      proposed_direction`, `output_artifact:
      architectural_review_recommendation`.
    - Step 3 (bespoke addition, shape copied from the real `handoff` step
      used to close out `setup-sensemaking-repo`,
      `workflow-registry.yaml:121-126`): skill `handoff`, gate
      `review_handoff_prompt`, `input_artifact:
      architectural_review_recommendation`, `output_artifact:
      session_summary`.

  REVISED after review: the bespoke workflow entry, as originally drafted,
  never declared `allowed_execution_modes` at all. This is FATAL, not
  cosmetic: `_load_registries()` (`scripts/workflow-runtime.py:401-428`)
  reads `allowed = self.workflow.get("allowed_execution_modes", [])` (line
  418) -- a MISSING key defaults to an EMPTY list, so `self.mode not in []`
  is unconditionally True and `MODE_NOT_ALLOWED` fires regardless of what
  mode is requested. CONFIRMED by direct empirical re-run: the original
  entry aborted before step 1 with no run log or ledger ever created.
  Fix: add `allowed_execution_modes: [autonomous_execution]` explicitly to
  the bespoke entry (see `initial_state_specification`), mirroring T3M-K7X's
  own post-review fix for the identical class of defect.

  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA, with
  `workflow-registry.yaml` amended in the scratch clone only. EMPIRICALLY
  VERIFIED end to end after the fix: both invocations of this exact
  sequence were actually run in a disposable scratch clone (not just read
  from source), and every claim below reflects what was observed, not
  merely predicted.
verified_failed_boundary: |
  Step 3's `session_summary` artifact is NOT one of the 3 artifact_ids
  `select_validator()` special-cases
  (`scripts/validate-and-report.py:311-319`: only
  `repository_sensemaking_brief`, `workflow_orchestration_plan`,
  `architectural_review_recommendation`), so it falls to the generic
  fallback, `scripts/validate-artifact.py`.
  `_run_validate_and_report()` (workflow-runtime.py lines 1612-1716) invokes
  the OUTER dispatcher with NO `--json` flag (lines 1635-1636);
  `validate-and-report.py`'s own `main()` (lines 536-552) takes no `--json`
  argument at all and unconditionally emits JSON -- this outer call always
  succeeds.
  The genuine defect is one layer down: `invoke_validator()`'s generic-
  fallback branch (lines 370-377) always appends `--json` when shelling out
  to `scripts/validate-artifact.py`. At the frozen SHA that script's own
  argparse (lines 320-325) does NOT define `--json`; `parser.parse_args()`
  rejects it as unrecognized, printing a usage error to stderr and exiting
  nonzero with EMPTY stdout. `invoke_validator()`'s
  `json.loads(result.stdout)` then raises `JSONDecodeError`, caught (lines
  405-427) and turned into a well-formed `{"valid": false, "errors":
  [{"error_id": "session_summary.validator.execution_error", ...}]}`
  result -- which is what the OUTER process prints as its own valid JSON.
  EMPIRICALLY CONFIRMED: `python scripts/validate-and-report.py
  <session_summary-file> --repo-root .` (no `--json`, matching exactly how
  the runtime invokes it) returned exit code 2 and
  `{"valid": false, "artifact_id": "session_summary", ...,
  "errors": [{"error_id": "session_summary.validator.execution_error",
  "message": "Validator returned invalid JSON: Expecting value: line 1
  column 1 (char 0)", ...}]}` -- both in isolation and, identically, inside
  the real orchestrator's step 3 validator_stack.
  Back in `workflow-runtime.py`, `passed = validation_json.get("valid",
  False)` is False (line 1675), appended as `FAILED` (lines 1676-1682);
  `v_failures` (line 1038) non-empty sets `result["status"] = "FAILED"`
  for step 3 (line 1046) and the run halts (lines 2626-2631). This failure
  is CONTENT-INDEPENDENT: it fires for ANY `session_summary` content, since
  the crash happens before content is ever parsed.
  CRITICAL, EMPIRICALLY DISCOVERED FINDING NOT IN THE ORIGINAL DRAFT: because
  this failure is content-independent, NO amount of re-authoring
  `session_summary`'s content on `--resume` can ever make step 3 pass --
  EMPIRICALLY CONFIRMED by attempting exactly that: a well-formed,
  fully-contract-compliant `session_summary` fixture (including the
  required `source_intent_ref` field) STILL failed with the identical
  `validator.execution_error`, because the crash happens at the argparse
  layer, before any content is read. Genuine recovery to a `VALIDATED`
  step 3 REQUIRES the SAME underlying repository-level code fix the
  disposable T3 pilot's own oracle documents and verifies as correct:
  adding `--json` support to `scripts/validate-artifact.py`'s `main()`.
  This spec's `recovery_invocation` makes that fix an explicit, required
  part of the recovery, not an optional nicety -- see
  `initial_state_specification` and the qualification note below.
pre_failure_completed_work_expectations: |
  Steps 1 AND 2 must both complete successfully first, in the SAME initial
  invocation. Step 1 (`repo-sensemaker`): `repository_sensemaking_brief`
  satisfying `validate-brief.py` in full. Step 2 (`architectural-review`):
  `architectural_review_recommendation` satisfying
  `validate-architectural-review-recommendation.py` in full (`decision:
  pursue` with a populated `success_measures` dict, since
  `decision.startswith("pursue")` triggers that check at
  `validate-architectural-review-recommendation.py:278-293`); this step
  also requires `proposed_direction` supplied up front (see
  `initial_state_specification`) or it hard-fails at
  `workflow-runtime.py:923-931` for the wrong reason. Both steps finish
  `VALIDATED` (`MODE_CEILINGS["autonomous_execution"] == "VALIDATED"`,
  line 1086).
  EMPIRICALLY CONFIRMED end to end: the real orchestrator's ledger for
  invocation 1 recorded a full `step_started`/`artifact_created`/
  `validation_completed(status: passed)`/`step_completed(status: validated)`
  sequence for BOTH `step_id: "1"` and `step_id: "2"`, with content
  hashes `ae06de7e...` (brief) and `b6c760c9...` (recommendation) recorded
  in each step's `artifact_created` event -- before step 3 genuinely failed.
failure_producing_condition: |
  Step 3's `session_summary` artifact is authored with well-formed,
  contract-compliant content (a normal handoff summary, including the
  required `source_intent_ref` machine field per
  `skills/workflow-planner/references/artifact-contracts.yaml`'s
  `session_summary` entry) -- content is irrelevant to the FIRST attempt's
  outcome, since the crash fires unconditionally. EMPIRICALLY CONFIRMED:
  this exact content produced `session_summary.validator.execution_error`
  and nothing else, both via direct `validate-and-report.py` invocation and
  through the real orchestrator's step 3.
recovery_invocation: |
  Invocation 1 (initial): `python scripts/workflow-runtime.py "<problem
  statement>" --repo-root <scratch-clone-root> --workflow
  t3h-w4j-review-handoff-workflow --mode autonomous_execution` (against a
  scratch clone with the bespoke workflow entry from
  `initial_state_specification` already committed; `proposed_direction`
  supplied up front). Ends with step 3 FAILED.

  BEFORE the fix + `--resume`: the git tree must be recommitted clean.
  EMPIRICALLY DISCOVERED: `preflight_check()`
  (`scripts/workflow-runtime.py:537-560`) requires a clean
  `git status --porcelain` for `autonomous_execution`, and every completed
  invocation leaves the tree dirty (new untracked ledger directory, plus a
  modified `docs/mode-coverage.yaml`).

  REQUIRED PART OF THE RECOVERY (not optional, per `verified_failed_boundary`):
  patch `scripts/validate-artifact.py`'s `main()` to add `--json` support
  (an `action="store_true"` argument plus a JSON-emitting branch mirroring
  the pattern already used by `scripts/validate-brief.py` and
  `scripts/validate-plan.py`, both of which already support `--json`
  correctly). EMPIRICALLY VERIFIED: applying exactly this patch made
  `validate-and-report.py <session_summary-file> --repo-root .` return
  `valid: true` for well-formed content and (independently re-confirmed
  by the disposable T3 pilot's own oracle, not re-derived here) `valid:
  false` for genuinely invalid content -- i.e. a real fix, not a bypass.
  Commit this patch alongside the tree-cleanup commit above.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-w4j-review-handoff-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume`.
  `--log-dir` must point at the directory holding invocation 1's run log,
  since `_find_resume_state()` (line 1956) reads from
  `os.path.join(self.log_dir, ...)`.
resume_expectations: |
  `_find_resume_state()` (line 1951) parses invocation 1's run log. Steps
  1's AND 2's logged status `VALIDATED` are BOTH members of
  `_resumable_terminal_statuses()` (`{"VALIDATED", "COMPLETED"}`, lines
  1916-1949), so BOTH are added to `completed_steps`. Step 3's logged
  status `FAILED` is excluded (lines 1973-1978). `resume_skip` (line 2594)
  resolves to `{1, 2}` -- the specific, strictly-harder case this spec
  exercises: TWO prior steps protected at once. Steps 1 and 2 are BOTH
  skip-reconstructed (lines 2606-2621, called twice, no `execute_step()`
  either time; each synthetic result hardcodes `"status": "COMPLETED"`,
  line 2617). Step 3 is genuinely re-executed via `execute_step()` (line
  2623), re-invoking `handoff` and re-running the validator stack -- this
  time against the now-patched `validate-artifact.py`.
  EMPIRICALLY CONFIRMED end to end: the resumed run printed `[OK] Found
  resume state: 2 completed, paused at step None` and `[OK] Resuming:
  skipping steps [1, 2], starting from step 3`; step 3 genuinely re-ran and
  printed `[OK] Validation passed`; the run finished `Execution completed
  successfully.` / exit code 0. The overwritten run log's status lines read
  `COMPLETED` / `COMPLETED` / `VALIDATED` for steps 1/2/3 respectively --
  verbatim, byte-for-byte matching this prediction.
protected_work: |
  REVISED after review: run-log content is NOT a preservation channel.
  EMPIRICALLY CONFIRMED: because `--resume` MUST reuse the identical
  `--log-dir` to find prior state, `write_run_log()` OVERWRITES that one
  fixed file in place on every invocation -- after the resumed run, it
  shows only the LATEST state (steps 1/2 `COMPLETED`, step 3 `VALIDATED`);
  invocation 1's `FAILED` record for step 3 is gone from it.
  BOTH prior artifacts must remain byte-identical on disk, since neither
  step 1 nor step 2 is ever re-invoked on resume -- both are
  skip-reconstructed. This is independently checkable via TWO separate
  file-hash comparisons against the hashes logged in invocation 1's own
  ledger (a SEPARATE, auto-incrementing numbered directory, independent of
  `--log-dir`, never overwritten). EMPIRICALLY CONFIRMED: after the
  resumed run, `repository_sensemaking_brief-fixture.md`'s hash
  (`ae06de7e679cf56d43926fde6f8bd3815a39c680614d361b42678aefec99cd08`) and
  `architectural_review_recommendation.md`'s hash
  (`b6c760c9c1343f44bd6e24b0dfdb183abe2b2418ac4ba87c002f0c508b2db4d9`)
  BOTH matched invocation 1's `artifact_created` ledger events exactly, and
  the resumed run's own fresh ledger contained ZERO `step_id: "1"` and
  ZERO `step_id: "2"` events of any kind (only a fresh `step_id: "3"`
  sequence).
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family: (1)
  `git reset --hard` / `git clean -fd` on the scratch clone between
  attempts -- EMPIRICALLY CONFIRMED `rollback()` prints exactly this advice
  after the FAILED first invocation; following it would destroy BOTH
  already-VALIDATED artifacts and the ledger directories the resume
  mechanism depends on; (2) deleting/truncating the run log or any
  `run-ledger.jsonl` and re-invoking without `--resume`; (3) hand-editing
  step 3's logged status from `FAILED` to `VALIDATED`/`COMPLETED` instead
  of genuinely fixing and retrying. A fourth failure mode unique to this
  spec's shape: re-running steps 1 and 2 "just to be safe" via a fresh
  (non-resumed) invocation instead of trusting `--resume`'s
  skip-reconstruction of both. A fifth, specific to this spec's failure
  mode: "fixing" step 3 by hand-editing its content instead of patching
  the actual root-cause defect (`validate-artifact.py`'s missing `--json`
  support) -- EMPIRICALLY CONFIRMED this cannot work anyway (content edits
  alone never clear the error), so an oracle would only ever see this
  attempted, not succeed by it; the real, required fix is a repository code
  change, independently verifiable by re-running
  `scripts/validate-artifact.py --json` directly against both a valid and
  a deliberately-invalid artifact and confirming it now discriminates
  correctly (mirrors the disposable T3 pilot's own Check 5/5b).
  Committing each invocation's own run artifacts plus the required
  `validate-artifact.py` patch to restore a clean tree before `--resume`
  is REQUIRED operational hygiene, not reset laundering.
idempotency_expectations: |
  REVISED after review: scoped entirely to ledger content (two separate
  ledger files in two separate numbered directories, read together).
  `step_id: "1"` must show exactly ONE full 4-event sequence (ending
  `validated`/`passed`), located ONLY in invocation 1's ledger.
  `step_id: "2"` must ALSO show exactly ONE full 4-event sequence, located
  ONLY in invocation 1's ledger -- a second occurrence of EITHER in the
  resumed run's ledger would mean that step was silently re-executed. This
  is the specific duplication risk this multi-step case introduces
  relative to a 1-prior-step spec: two independent things to NOT
  duplicate, not one. `step_id: "3"` is expected to show TWO sequences
  across the two ledgers: invocation 1 ending
  `validation_completed(status: failed)`, invocation 2 (the resumed run)
  ending `validation_completed(status: passed)` /
  `step_completed(status: validated)` -- EMPIRICALLY CONFIRMED, this exact
  pattern was observed. One `run_started`/`run_completed` pair per
  invocation's own ledger is expected bookkeeping.
oracle_requirements: |
  A materialized oracle must first isolate THIS spec's own invocations
  from the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories (EMPIRICALLY CONFIRMED
  present for unrelated dogfood workflows) and from any other T3H spec's
  own bespoke-workflow directories. Filter by reading each candidate
  directory's `run-ledger.jsonl` first line and matching
  `event=="run_started"`.`workflow_id == "t3h-w4j-review-handoff-workflow"`
  exactly -- never by directory position/number.
  Applying the seven-link recovery chain, using ONLY ledger content: (1)
  the first matching ledger's step 3 genuinely reached FAILED via
  `session_summary.validator.execution_error` (not a content-validation
  error, not a crash with no captured output); (2) that same ledger's
  steps 1 AND 2 are BOTH `step_completed(status: validated)`, each with a
  real, non-fixture artifact that itself independently passed its own
  specialized validator; (3) the SECOND matching ledger contains ZERO
  `step_id: "1"` AND ZERO `step_id: "2"` events of any kind; (4) BOTH
  prior artifacts' file hashes after the resumed run match the hashes
  logged in invocation 1's `artifact_created` events, checked
  INDEPENDENTLY for each artifact (a bug that silently re-ran only ONE of
  the two prior steps must not be missed by checking only one hash); (5)
  the second ledger contains a fresh step_id "3" sequence ending
  `validated`/`passed`; (6) independently, `python
  scripts/validate-artifact.py --json` (now patched) discriminates a
  genuinely-valid vs. genuinely-invalid artifact correctly -- confirming
  the recovery was a real fix, not a bypass (mirrors the disposable T3
  pilot's own Check 5b); (7) none of the `forbidden_reset_restart_behavior`
  items occurred.
complexity_breakdown: |
  HIGH because this is a 3-step workflow where steps 1 AND 2 both
  genuinely succeed before step 3 fails -- this family's first HIGH
  criterion (more than one step before the failure), EMPIRICALLY confirmed
  to actually resolve `resume_skip` to `{1, 2}` in a real run, not just
  predicted from source. This is strictly harder than a 1-prior-step
  MEDIUM spec in three concrete, empirically-verified ways: (a)
  `resume_skip` really does equal `{1, 2}`, not a singleton; (b)
  `protected_work` requires and was given TWO independent byte-identity
  checks, each of which could fail independently; (c)
  `idempotency_expectations` rules out silent re-execution of EITHER prior
  step, not just one -- a hypothetical off-by-one in how `resume_skip` is
  built could skip only the LAST completed step while still re-running an
  earlier one, a bug class a 1-prior-step spec cannot expose at all.
  DISTINCT FROM THE ORIGINAL DRAFT: empirical testing surfaced that this
  spec's failing step (step 3, content-independent generic-validator
  crash) can only ever reach a genuinely VALIDATED final state via the SAME
  underlying repository code fix the disposable T3 pilot's own oracle
  documents (patch `validate-artifact.py` for `--json` support) -- this is
  now made an explicit, required part of `recovery_invocation` rather than
  left implicit. This does NOT make the scenario a reskin of the pilot:
  the pilot is a 2-step, single-resume scenario testing ONE prior
  completed step's protection; this spec's distinguishing value is
  entirely in the multi-step (`resume_skip = {1,2}`) mechanism, which the
  pilot never exercises regardless of which underlying bug causes the
  final-step failure. Flagged here for full transparency rather than
  omitted.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml`:

    id: t3h-w4j-review-handoff-workflow
    display_name: T3H-W4J Review Handoff (pilot-scoped)
    purpose: Disposable pilot-only 3-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (multi-step protection).
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
        skill: repo-sensemaker
        step_type: local_execution
        gate: review_diagnosis
        input_source: repository_state
        output_artifact: repository_sensemaking_brief
      - id: 2
        skill: architectural-review
        step_type: local_execution
        gate: review_recommendation
        input_artifact: repository_sensemaking_brief
        input_source: proposed_direction
        output_artifact: architectural_review_recommendation
      - id: 3
        skill: handoff
        step_type: local_execution
        gate: review_handoff_prompt
        input_artifact: architectural_review_recommendation
        output_artifact: session_summary

  REVISED after review: `allowed_execution_modes: [autonomous_execution]`
  is now explicit (the original draft omitted this key entirely, which
  fails closed to MODE_NOT_ALLOWED per `source_workflow_or_operation`).
  EMPIRICALLY VERIFIED: this exact entry, added to a scratch registry copy
  and committed, let `--mode autonomous_execution` pass preflight and all
  three steps execute for real (once `proposed_direction` was supplied and
  the tree recommitted clean between invocations).
  `proposed_direction` must be supplied before dispatch (a short, scoped
  architectural proposal, e.g. "add response caching to the validator
  dispatcher") so `execute_step()`'s hard-fail at lines 923-931 does not
  fire for the wrong reason on step 2. No fixture repair needed for steps
  1/3 (`repository_sensemaking_brief`, `session_summary` both have fixture
  support via `_get_fixture_artifact_path`); step 2's
  `architectural_review_recommendation` has NO fixture support at the
  frozen SHA (`_get_fixture_artifact_path`'s `skill_map`,
  `workflow-runtime.py:1365-1370`, does not include it) -- the dispatched
  agent produces it directly via real skill execution in production; this
  spec's own verification instead placed it directly at its
  session-scoped resolved path via `--from-session`, EMPIRICALLY confirmed
  to be read and validated identically to a skill-produced file. The
  REQUIRED `validate-artifact.py` `--json` patch (see `recovery_invocation`)
  must be applied to the scratch clone before `--resume` -- without it,
  step 3 can never reach `VALIDATED` regardless of retry count.
spec_sha256: 9440dfa2722cd65f9463494d49bb64cff98aad01cf09fb396141436cb2d42c60
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Recomputed after the post-review fix (mode fix + ledger-based protected
  # work + required validate-artifact.py patch, all empirically verified)
  # with PyYAML safe_load + hashlib.sha256("".join(str(v) for v in fields))
  # over this file's revised content.
qualification: |
  ADMISSIBLE (with the noted dependency: full recovery to VALIDATED
  requires the same validate-artifact.py --json fix the disposable T3
  pilot's own oracle already documents and verifies; this spec's
  distinguishing HIGH-complexity claim, resume_skip protecting two
  simultaneous prior steps, is independent of that fix and was empirically
  confirmed both before and after it was applied)
