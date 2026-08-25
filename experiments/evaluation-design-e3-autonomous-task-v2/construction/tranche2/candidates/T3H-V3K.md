candidate_id: T3H-V3K
family: T3
complexity_level: HIGH
source_workflow_or_operation: |
  A bespoke 2-step workflow, `t3h-v3k-diagnostic-setup-workflow`, assembled
  VERBATIM from the real registered `setup-sensemaking-repo`'s steps 1-2
  only (frozen SHA 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5,
  `skills/workflow-planner/references/workflow-registry.yaml:110-120`), with
  one explicit addition: `allowed_execution_modes: [autonomous_execution]`.
  This is REQUIRED, not optional: `setup-sensemaking-repo`'s own
  `allowed_execution_modes` at the frozen SHA is `[plan_only, prompt_chain,
  guided_execution]` -- `autonomous_execution` is absent, so
  `_load_registries()` (`scripts/workflow-runtime.py:401-428`, the
  `MODE_NOT_ALLOWED` check at lines 418-426) would abort the run before step
  1 ever executes if the real workflow entry were used unmodified.
  EMPIRICALLY CONFIRMED THIS SESSION, not merely read from the registry: the
  bespoke entry (identical 2-step shape to this family's T3M-K7X, T3M-H4Q,
  T3M-L8R, but a fresh, distinct registry id so ledger-based filtering can
  never conflate this spec's runs with theirs) was inserted into a scratch
  copy of `workflow-registry.yaml` in a disposable scratch clone of the
  frozen SHA, and `OrchestrationRunner` was DIRECTLY INSTANTIATED (not
  dispatched through `main()`, and not merely read as YAML) against it:
  `OrchestrationRunner(workflow_id="t3h-v3k-diagnostic-setup-workflow",
  mode="autonomous_execution", repo_root=".", executor="dry-run")` produced
  `runner.errors == []` -- no `MODE_NOT_ALLOWED`. In the SAME script, the
  same instantiation method run against the real `setup-sensemaking-repo`
  with `mode="autonomous_execution"` DID correctly produce
  `MODE_NOT_ALLOWED`, confirming the check discriminates rather than
  vacuously passing everything. This directly answers this construction
  task's standing instruction to verify `allowed_execution_modes` claims by
  actually instantiating `OrchestrationRunner`.
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact`.
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief`.
  Step 3 of the real `setup-sensemaking-repo` (`handoff` -> `session_summary`)
  is dropped by construction, not by convention -- it can never execute, so
  it can never contaminate this spec with the generic validator's unrelated
  `--json` argparse crash.
  What makes this a genuinely different scenario from this family's other
  `repository_sensemaking_brief` specs (T3M-K7X's
  `recommended_workflow_id.unknown_value`, T3H-Z1V's
  `primary_fog_type.unknown_value`/`evidence.logic_error`, T3H-Q8N's
  `EVIDENCE_QUOTE_NOT_FOUND`, T3M-H4Q's `HALLUCINATED_FILE`, T3M-L8R's
  `WEAKNESS_TYPE_MALFORMED`): this spec's failure is not a single `if` in
  `validate-brief.py` itself, but a genuinely cross-module, multi-layer
  structural defect routed through a SEPARATE module,
  `scripts/weakness_type_safeguard.py`, and its custom
  duplicate-key-detecting YAML loader (see `verified_failed_boundary`) --
  this family's second "root cause requires tracing through more than one
  real layer" HIGH criterion, structurally distinct from T3H-Q8N's own
  multi-layer scenario (a single-module windowed text search, entirely
  within `validate-brief.py`).
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at the frozen SHA.
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` is routed to
  `scripts/validate-brief.py` by `select_validator()`
  (`scripts/validate-and-report.py:311-312`), invoked with `--json`
  (accepted by validate-brief.py's own argparse), so this does not crash.
  The genuine failure requires tracing through THREE layers across TWO
  modules, not a single field-presence `if`:
  (1) `validate_brief()` extracts the `## 13.` section's authoritative
  handoff block and calls `weakness_type_safeguard.check()`
  (`scripts/validate-brief.py:622` calls into
  `scripts/weakness_type_safeguard.py:252-326`, imported at
  `validate-brief.py:12`) rather than parsing that block with a plain
  `yaml.safe_load()` directly.
  (2) `weakness_type_safeguard.check()` itself is multi-step:
  `extract_section_body()` (`weakness_type_safeguard.py:146-188`) locates
  the `## 13.` heading and its body; `extract_single_yaml_fence()`
  (lines 191-239) finds the ONE fenced ```yaml block inside that body; then
  `_parse_dup_safe()` (lines 242-249) parses that block's text with
  `_DuplicateKeySafeLoader`, a `yaml.SafeLoader` subclass whose custom
  mapping constructor, `_construct_mapping_no_duplicates` (lines 122-130),
  raises `DuplicateKeyError` the moment it encounters a repeated key at any
  mapping level -- deliberately DIFFERENT behavior from plain `yaml.safe_load`,
  which silently does last-value-wins and can never observe a duplicate
  top-level `weakness_type:` key at all (the exact gap the module's own
  docstring, lines 110-119, states this custom loader exists to close).
  (3) Back in `check()` (lines 281-298), when the raised `DuplicateKeyError`'s
  `.key == "weakness_type"`, it returns
  `SafeguardResult(DUPLICATE_WEAKNESS_TYPE_KEYS, ...)`; back in
  `validate-brief.py` (line 622, `if safeguard_result.outcome !=
  EXACTLY_ONE_WEAKNESS_TYPE_KEY`), `_SAFEGUARD_OUTCOME_TO_CODE` (lines
  114-121) maps this outcome to the validator's own
  `DUPLICATE_WEAKNESS_TYPE_KEYS` error code, and its severity is `"error"`
  (blocking) since the outcome is not `ZERO_WEAKNESS_TYPE_KEYS` (the one
  outcome deliberately downgraded to `"warning"`, per the code comment at
  lines 630-637). `validation_json["valid"]` becomes False via the same
  `execute_step()` / `_run_validator_stack()` / `_run_validate_and_report()`
  chain cited throughout this family (`scripts/workflow-runtime.py` lines
  1023, 1038-1046), and `result["status"] = "FAILED"` is set for step 2.
  EMPIRICALLY CONFIRMED (direct validator invocation, this construction
  session, frozen-SHA archive extracted from `git archive
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`): a constructed brief, otherwise
  identical to a fully-valid baseline (valid `primary_fog_type`, non-empty
  `evidence`, a real `recommended_workflow_id`, a correctly-grounded
  `evidence_excerpts` entry citing an existing file), but with the `## 13.`
  section's single ```yaml fence containing the top-level key
  `weakness_type: "Contract Mismatch"` written TWICE (identical value both
  times, to isolate the structural duplication itself as the cause, not a
  value conflict), run through `python scripts/validate-brief.py <file>
  --repo-root . --json`, produced exactly one error:
  `DUPLICATE_WEAKNESS_TYPE_KEYS: DUPLICATE_WEAKNESS_TYPE_KEYS: top-level
  'weakness_type' key repeated 2 times in the authoritative Section 13 block
  -- HARD STOP ... [duplicate_count=2]` (`valid: false`). The IDENTICAL
  fixture with the duplicate line removed (a single `weakness_type:` key)
  produced `valid: true`, zero errors -- confirming the isolation: this is
  the ONLY error the duplication produces, and confirming (per the module's
  own stated purpose) that a plain `yaml.safe_load()`-based check could
  never have caught this in the first place, since standard YAML parsing
  silently discards the first occurrence.
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first.
  Because it declares no `output_artifact`, `execute_step()`'s
  artifact/validator branches never activate for it (line 889's `if
  output_artifact:` guard is skipped, line 1022's `os.path.exists()` guard
  is False, line 1048's `elif` is also False). Execution falls straight to
  gate management (line 1065); for `autonomous_execution` the step finishes
  at line 1086 with `result["status"] = "VALIDATED"`. Ledger-wise, step 1
  gets exactly `step_started` and `step_completed` events for `step_id:
  "1"` -- no `artifact_created`/`validation_completed`. This is the same
  step-1 shape already established and empirically verified end to end by
  this family's T3M-K7X, T3M-H4Q, T3M-L8R, T3H-Q8N, and T3H-Z1V.
failure_producing_condition: |
  The step-2 `repository_sensemaking_brief` is FIXTURE CONTENT placed as
  part of this spec's initial state (via `--use-fixtures` pointing at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`,
  `--executor dry-run`), not asserted to be organically produced by a
  live-dispatched `repo-sensemaker` invocation -- matching this family's
  established, safe dispatch pattern for fixture-sourced content (T3M-H4Q,
  T3M-L8R, T3H-Q8N, T3H-W4J). `scripts/brief_skeleton.py`'s
  `reconcile_evidence_excerpt_quotes()` (issue #89) is irrelevant here
  regardless -- it only ever touches `evidence_excerpts[].quote` fields
  (`scripts/brief_skeleton.py:336-396`), never the `## 13.` section's raw
  key structure this spec's failure depends on -- but `--use-fixtures
  --executor dry-run` is used anyway for consistency with this family's
  established pattern.
  The fixture's `## 13. Machine-readable handoff` fenced YAML block is
  otherwise fully valid (`artifact_id: repository_sensemaking_brief`,
  `primary_fog_type: architecture_fog`, non-empty `evidence`,
  `recommended_workflow_id: architecture-implementation-workflow`,
  `created_at`, `immutable: true`), but its top-level `weakness_type:
  "Contract Mismatch"` key is written TWICE inside the SAME single fence
  (not two separate fences -- that would instead trip `MALFORMED_FENCE` via
  `extract_single_yaml_fence()`'s "more than one candidate block" check,
  the pitfall this family's T3M-H4Q/T3M-L8R construction notes document; a
  single fence with an internally-repeated key is a structurally different,
  narrower defect). A separately-headed `## 5. Evidence` section contains a
  correctly formed, correctly grounded `evidence_excerpts` block citing a
  real, existing file and a validly-formatted line range with a genuinely
  grounded quote, so `HALLUCINATED_FILE`, `INVALID_LINE_FORMAT`, and
  `EVIDENCE_QUOTE_NOT_FOUND` cannot fire and be confused with this spec's
  target failure. EMPIRICALLY CONFIRMED (see `verified_failed_boundary`):
  this isolates the brief to exactly one blocking error,
  `DUPLICATE_WEAKNESS_TYPE_KEYS`; removing the duplicate line (nothing else
  touched) resolved the fixture to `valid: true`, zero errors.
recovery_invocation: |
  Invocation 1 (initial, no `--resume`): `python scripts/workflow-runtime.py
  "<problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-v3k-diagnostic-setup-workflow --mode autonomous_execution
  --use-fixtures --executor dry-run` (no `--log-dir`; defaults to the
  auto-generated session directory). Ends with step 2 FAILED
  (`DUPLICATE_WEAKNESS_TYPE_KEYS`).

  BEFORE `--resume`: the git working tree must be returned to clean.
  `preflight_check()` (`scripts/workflow-runtime.py:537-560`) requires a
  clean `git status --porcelain` for `autonomous_execution`, and a completed
  invocation always leaves the tree dirty (the new, untracked
  `artifacts/NN-orchestration-run/` ledger directory, plus a modified
  `docs/mode-coverage.yaml`). Commit this new state before `--resume`. Also
  correct the fixture at
  `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md` (remove
  the duplicate `weakness_type:` line, leaving exactly one, nothing else
  touched) before recommitting, since step 2's genuine retry re-reads that
  same fixture path.

  Invocation 2 (`--resume`): `python scripts/workflow-runtime.py "<same
  problem statement>" --repo-root <scratch-clone-root> --workflow
  t3h-v3k-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<invocation-1-session-dir> --resume
  --use-fixtures --executor dry-run`. `--log-dir` must point at the
  directory holding invocation 1's
  `run_log_t3h-v3k-diagnostic-setup-workflow_autonomous_execution.md`
  (`_find_resume_state()`, line 1956). `--log-dir` only controls where the
  PRIOR run log is read from for resume-state discovery -- the new attempt's
  own `run-ledger.jsonl` goes to a freshly auto-generated session directory
  (`_generate_session_id()`, line 151) unless `--from-session` is also
  passed.
resume_expectations: |
  `_find_resume_state()` (line 1951) parses invocation 1's run log. Step 1's
  logged status `VALIDATED` is in `_resumable_terminal_statuses()`
  (`{"VALIDATED", "COMPLETED"}` for autonomous_execution, lines 1916-1949)
  and is added to `completed_steps`; step 2's logged status `FAILED` is
  excluded from both `completed_steps` and `paused_step` (lines 1973-1978)
  by the same membership-check construction, not a special-cased "skip
  FAILED" branch. `resume_skip` (line 2594) resolves to `{1}`. In the step
  loop (lines 2605-2624): step 1 is skip-reconstructed synthetically (no
  `execute_step()` call, hardcoded `"status": "COMPLETED"`, line 2617);
  step 2 is genuinely re-executed via `execute_step()` (line 2623),
  re-invoking `repo-sensemaker` (via the fixture path again) and
  re-running the FULL multi-layer safeguard chain
  (`weakness_type_safeguard.check()` -> `extract_section_body()` ->
  `extract_single_yaml_fence()` -> `_parse_dup_safe()`) against the
  corrected fixture -- this time observing exactly one top-level
  `weakness_type` key and returning `EXACTLY_ONE_WEAKNESS_TYPE_KEY`, which
  produces no error/warning at all (per the code comment at lines 111-113).
  Because this bespoke workflow has exactly 2 steps, the step loop ends
  after step 2 succeeds.
protected_work: |
  Step 1 has no output artifact, so the protected invariant is LEDGER
  SILENCE for `step_id: "1"`: the resumed invocation's own fresh
  `run-ledger.jsonl` (a separate, auto-incrementing numbered directory,
  independent of `--log-dir`) must contain no new `step_started`,
  `artifact_created`, `validation_completed`, or `step_completed` events for
  `step_id: "1"`. The first attempt's run log file is NOT a reliable
  preservation channel: `write_run_log()` (line 1991, path built at line
  1995 from `self.log_dir`) OVERWRITES that same fixed file in place on
  every invocation, since `--resume` must reuse the identical `--log-dir`.
  Only `run-ledger.jsonl`, in each invocation's own separate numbered
  directory, is a reliable, isolated, never-overwritten record.
forbidden_reset_restart_behavior: |
  Same three behaviors ruled out as the rest of this family: (1) `git reset
  --hard` / `git clean -fd` on the scratch clone between attempts -- the
  runtime's own `rollback()` (line 2511-2521) prints exactly this advice
  after every FAILED run; following it would destroy the ledger directories
  the resume mechanism depends on; (2) deleting/truncating
  `run_log_t3h-v3k-diagnostic-setup-workflow_autonomous_execution.md` or any
  `run-ledger.jsonl` and re-invoking without `--resume`; (3) hand-editing
  step 2's logged status from `FAILED` to `VALIDATED`/`COMPLETED` to force
  it into skip-reconstruction instead of genuine retry. A fourth behavior
  specific to this spec's failure mode is also forbidden: "fixing" the
  failure by RENAMING one of the two duplicate keys (e.g. to
  `weakness_type ` with a trailing space, or `Weakness_Type`) so it is no
  longer LITERALLY the same YAML key and the custom loader no longer detects
  a collision, rather than genuinely removing the duplicate and leaving
  exactly one authoritative `weakness_type` key -- independently detectable
  by re-parsing the resumed attempt's `## 13.` fence with the SAME
  `_DuplicateKeySafeLoader`-based `weakness_type_safeguard.check()` function
  the real validator uses and confirming the outcome is
  `EXACTLY_ONE_WEAKNESS_TYPE_KEY` (a renamed-duplicate variant would parse
  to TWO distinct top-level keys, which the safeguard does not check for at
  all -- an oracle relying only on the absence of the specific
  `DUPLICATE_WEAKNESS_TYPE_KEYS` error code, without independently
  re-parsing the actual key set, could be fooled by this).
idempotency_expectations: |
  Across the combined ledger record (invocation 1's file plus invocation
  2's file, read together), `step_id: "1"` must show exactly ONE
  `step_started`/`step_completed` pair (from invocation 1 only). `step_id:
  "2"` is expected to show TWO sequences: invocation 1 ending
  `validation_completed(status: failed)` (the genuine
  `DUPLICATE_WEAKNESS_TYPE_KEYS` result) / `step_completed(status: failed)`,
  invocation 2 ending `validation_completed(status: passed)` /
  `step_completed(status: validated)` once the duplicate key is genuinely
  removed -- that second sequence is the legitimate retry, not duplicate
  work. One `run_started`/`run_completed` pair per invocation is expected
  bookkeeping. Because this workflow has exactly 2 steps, any `step_id: "3"`
  event anywhere would be a structural anomaly, not legitimate work.
oracle_requirements: |
  A materialized oracle must first isolate this spec's own invocations from
  the frozen-SHA repo's pre-existing, committed
  `artifacts/NN-orchestration-run/` directories and from any other
  T3-family spec's own bespoke-workflow directories. Filter by reading each
  candidate directory's `run-ledger.jsonl` first line and matching `event ==
  "run_started"`.`workflow_id == "t3h-v3k-diagnostic-setup-workflow"`
  exactly -- never by directory position/number.
  Applying the seven-link recovery chain, using ONLY ledger content: (1) the
  chronologically-first matching directory's ledger shows step 2 genuinely
  reached FAILED via `DUPLICATE_WEAKNESS_TYPE_KEYS` specifically (not a
  crash, not `WEAKNESS_TYPE_MALFORMED`, not `MALFORMED_HANDOFF_FENCE` -- an
  oracle should confirm the exact error_id, since this family's T3M-L8R
  already exercises the structurally-adjacent-but-distinct
  `WEAKNESS_TYPE_MALFORMED` and this spec's fixture must not accidentally
  reproduce that instead); (2) that same ledger's step 1 status is
  `step_completed(status: validated)`; (3) the chronologically-LAST matching
  directory's ledger contains ZERO `step_id: "1"` events of any kind; (4)
  that same ledger contains a fresh step_id "2" sequence ending
  `validated`/`passed`; (5) the resumed run's step 2 brief, when its `## 13.`
  fence is independently re-parsed by the oracle using the SAME
  `weakness_type_safeguard.check()` function the real validator calls,
  yields outcome `EXACTLY_ONE_WEAKNESS_TYPE_KEY` (not merely "the reported
  error code changed" -- see the renamed-duplicate pitfall in
  `forbidden_reset_restart_behavior`); (6) the fixed `--log-dir` path's run
  log, read only for its latest state, shows step 2 as `VALIDATED`; (7)
  none of the `forbidden_reset_restart_behavior` items occurred, including
  the key-renaming variant specific to this spec.
complexity_breakdown: |
  HIGH because the failure's root cause requires tracing through more than
  one real layer, ACROSS TWO SEPARATE MODULES -- this family's second HIGH
  criterion, but exercised through a structurally different mechanism from
  this family's other multi-layer HIGH spec (Tranche-1's T3H-Q8N, a
  single-module windowed-substring search entirely inside
  `validate-brief.py`). Here, `validate-brief.py` delegates to
  `scripts/weakness_type_safeguard.py` (a genuinely separate module with its
  own custom `yaml.SafeLoader` subclass, `_DuplicateKeySafeLoader`), whose
  behavior deliberately diverges from PyYAML's own standard, silent
  last-value-wins semantics -- the failure is invisible to a naive
  `yaml.safe_load()`-based check entirely (a plain parse of the duplicated
  block would silently succeed with the last value, exactly the gap this
  module's own docstring says it exists to close). This is a single failing
  step (step 2 of 2), so it does NOT also claim the multi-step HIGH
  criterion -- the cross-module, non-standard-parser-semantics root cause is
  this spec's sole, sufficient basis for HIGH.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, clean working tree, PLUS one
  addition applied and committed before dispatch: a new workflow entry
  inserted into a scratch copy of
  `skills/workflow-planner/references/workflow-registry.yaml`:

    id: t3h-v3k-diagnostic-setup-workflow
    display_name: T3H-V3K Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing (duplicate weakness_type key, multi-layer
      cross-module safeguard).
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
  instantiating `OrchestrationRunner(workflow_id="t3h-v3k-diagnostic-setup-workflow",
  mode="autonomous_execution", ...)` and produced zero errors -- confirming
  preflight-level mode gating for real.
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
    weakness_type: "Contract Mismatch"
    weakness_type: "Contract Mismatch"
    ```

  EMPIRICALLY CONFIRMED (this construction session, direct
  `validate-brief.py --json` invocation against this exact fixture text):
  this produces exactly one error, `DUPLICATE_WEAKNESS_TYPE_KEYS`
  (`duplicate_count=2`); removing the second `weakness_type:` line resolves
  it to `valid: true`, zero errors -- and that corrected, single-key version
  is byte-identical to this family's T3M-C5N/T3M-H4Q/T3M-L8R baseline
  fixture pattern, confirming this is a genuinely isolated, single-cause
  defect and not an artifact of some other unrelated fixture problem. The
  `evidence_excerpts` YAML block is placed under its own `## 5. Evidence`
  heading, separate from `## 13.`'s own fence -- required for the same
  structural reason this family's T3M-H4Q/T3M-L8R document (co-locating both
  fences inside one section would instead trip `MALFORMED_FENCE`, a
  different, contaminating error).
  For the RESUME attempt, this same fixture file must be corrected in place
  (the duplicate `weakness_type:` line removed, nothing else touched)
  before `--resume` is invoked -- see `recovery_invocation`.
  `workflow-registry.yaml`'s pre-existing entries must otherwise be left
  unmodified from the frozen SHA.
spec_sha256: 78d7289093778e0057e06e2f39cb30b6ec4de8ad9a3ac18ebca4ec2f478cbbcd
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
