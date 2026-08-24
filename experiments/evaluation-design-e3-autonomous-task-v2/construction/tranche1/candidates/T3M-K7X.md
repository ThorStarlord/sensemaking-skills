candidate_id: T3M-K7X
family: T3
complexity_level: MEDIUM
source_workflow_or_operation: |
  REVISED after review: the real registered workflow `setup-sensemaking-repo`
  cannot be used as originally specified, for two independently
  disqualifying, empirically-confirmed reasons: (1) its
  `allowed_execution_modes` at frozen SHA
  (`skills/workflow-planner/references/workflow-registry.yaml:105-108`) is
  `[plan_only, prompt_chain, guided_execution]` — `autonomous_execution` is
  NOT in that list, so `_load_registries()`
  (`scripts/workflow-runtime.py:401-428`, specifically the `MODE_NOT_ALLOWED`
  check at lines 417-426) appends an error during `OrchestrationRunner.__init__`,
  and `main()` (lines 3106-3109) `return 1`s before `run()` is ever called —
  the very first invocation would abort before step 1 executes, before any
  run log or ledger exists; (2) its real step 3 (`handoff` ->
  `session_summary`) is unreachable in a FAILED first attempt (the step loop
  breaks at step 2), but WOULD genuinely execute for the first time once
  step 2 is fixed and resumed — and `session_summary` is not one of the 3
  artifact types `select_validator()` special-cases
  (`scripts/validate-and-report.py:311-319`), so it falls to the generic
  `scripts/validate-artifact.py`, invoked with `--json`
  (`validate-and-report.py:370-377`). Empirically confirmed against this
  validator directly: `validate-artifact.py`'s own argparse does not define
  `--json` and errors out (`unrecognized arguments: --json`) unconditionally
  — regardless of `session_summary`'s content. Accounting for step 3 "genuinely
  executing" would therefore mean the resumed run deterministically ends in
  a SECOND, unrelated FAILED step (the same argparse-crash defect class the
  disposable T3 pilot exists to test), which would make this spec no longer
  a "single clear fix" MEDIUM case (a full green run would need two
  independent fixes, not one) and would blur this spec's
  `failure_producing_condition` into a reskin of the pilot's own bug class.

  Fix chosen (of the two offered): restructure to a bespoke 2-step workflow,
  `t3m-k7x-diagnostic-setup-workflow`, assembled VERBATIM from the real
  `setup-sensemaking-repo`'s steps 1-2 only (its step 3 is dropped, not
  "out of scope by convention" — dropped by construction, so it can never
  execute at all), with one explicit addition:
  `allowed_execution_modes: [autonomous_execution]` (mirroring how the
  disposable T3 pilot's own bespoke workflow entry, `T3-PILOT-TASK.md`,
  declares `allowed_execution_modes: [autonomous_execution]` for its own
  entry). This keeps `--mode autonomous_execution` and every
  VALIDATED-status claim elsewhere in this spec correct (no need to
  downgrade to `guided_execution`/`APPROVED`), while resolving both
  disqualifying issues by construction rather than by exclusion or
  after-the-fact accounting:
    - Step 1: skill `setup-sensemaking-skills`, gate `review_setup_plan`,
      `input_source: repository_state`, no `output_artifact` (copied
      verbatim from workflow-registry.yaml:110-114).
    - Step 2: skill `repo-sensemaker`, gate `review_repo_brief`,
      `input_source: repository_state`, `output_artifact:
      repository_sensemaking_brief` (copied verbatim from
      workflow-registry.yaml:115-120).
  Invoked via `scripts/workflow-runtime.py` in `--mode autonomous_execution`
  against a disposable scratch clone at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, with the one scratch-only
  registry addition described in `initial_state_specification` applied
  before dispatch (never a change to the real registry).
verified_failed_boundary: |
  Step 2's `repository_sensemaking_brief` artifact is validated by
  `scripts/validate-brief.py` (routed there, not the generic
  `validate-artifact.py`, by `select_validator()` at
  `scripts/validate-and-report.py:311-312`, which special-cases
  `artifact_id == "repository_sensemaking_brief"` before falling through to
  the generic/`--json`-crashing path). `invoke_validator()`
  (`validate-and-report.py:378-386`) calls it as
  `[artifact_path, --repo-root, --json]`; validate-brief.py's own argparse
  (`scripts/validate-brief.py:902-916`) defines `--json`, so this call does
  NOT crash (unlike the generic validator's argparse gap discussed above and
  used by the T3 pilot).
  The real failure condition lives in validate-brief.py's Phase-1
  required-field check for `recommended_workflow_id`
  (`scripts/validate-brief.py:579-596`): when the field is present but its
  value is not among `{w["id"] for w in registry.get("workflows", [])}`
  loaded from `workflow-registry.yaml`, it appends
  `error_id: "repository_sensemaking_brief.recommended_workflow_id.unknown_value"`
  (`error_type: unknown_value`). `validation_json["valid"]` is then False.
  In `scripts/workflow-runtime.py`'s `execute_step()`
  (frozen-SHA lines 833-1094), `_run_validator_stack()` is called at line
  1023; `_run_validate_and_report()` (lines 1587-1716) appends
  `{"result": "FAILED", ...}` to the validator stack (line 1679, since
  `passed = validation_json.get("valid", False)` is False). Back in
  `execute_step()`, `v_failures` at line 1038 is non-empty, so line 1046 sets
  `result["status"] = "FAILED"` and returns
  `self._finalize_step_result(result, step_num)` (line 1047) — which still
  logs a `step_completed` ledger event (line 1091-1094) with
  `status: "failed"`, per the normal flow, before halting the run
  (`run()` lines 2626-2631 break the step loop on `status == "FAILED"`).
  This is a genuine, reproducible content-validation failure, not the
  pilot's argparse-crash bug and not a fabricated one — driven entirely by
  the brief's own field content. EMPIRICALLY CONFIRMED: a constructed test
  artifact with this exact content (all Phase-1 fields valid except
  `recommended_workflow_id` set to a nonexistent id) run directly through
  `python scripts/validate-brief.py <file> --repo-root . --json` against a
  frozen-SHA archive returned `"valid": false` with exactly ONE error,
  `repository_sensemaking_brief.recommended_workflow_id.unknown_value`.
pre_failure_completed_work_expectations: |
  Step 1 (`setup-sensemaking-skills`) must complete successfully first.
  Because it declares no `output_artifact`, `execute_step()`'s
  artifact/validator branches never activate for it: `output_artifact` is
  falsy, so the `if output_artifact:` guard at line 889 is skipped
  (`artifact_path` stays `""`), the `if artifact_path and
  os.path.exists(artifact_path):` guard at line 1022 is False, and the
  `elif output_artifact and output_artifact != "N/A":` guard at line 1048 is
  also False (nothing to be "expected but not produced"). Execution falls
  straight through to gate management (line 1065); assuming the gate
  auto-approves (mode: autonomous_execution, `gates: "automated"` per
  `KNOWN_MODES` — now legally reachable for this workflow because the
  bespoke registry entry explicitly lists `autonomous_execution` in
  `allowed_execution_modes`, unlike the real `setup-sensemaking-repo`), the
  step finishes at line 1086 with `result["status"] = "VALIDATED"`
  (MODE_CEILINGS["autonomous_execution"] == "VALIDATED"). The run log's
  `### Step 1` block logs status `VALIDATED`. Ledger-wise, step 1 gets
  exactly `step_started` (line 864-869) and `step_completed` (line
  1091-1094) events for `step_id: "1"` — no `artifact_created` or
  `validation_completed` events, since no artifact path ever exists for
  this step.
failure_producing_condition: |
  The step-2 `repository_sensemaking_brief`'s authoritative machine YAML
  block sets `recommended_workflow_id: repo-maintenance-workflow` (a
  plausible-sounding but nonexistent id — not among the real ids listed in
  `skills/workflow-planner/references/workflow-registry.yaml`'s
  `workflows:` list at the frozen SHA, e.g. not `setup-sensemaking-repo`,
  `fast-path-workflow`, `docs-implementation-workflow`, etc., and not the
  bespoke `t3m-k7x-diagnostic-setup-workflow` id either, which is also not
  a member of that same registry list), while every other Phase-1-required
  field (`artifact_id`, `primary_fog_type` set to one of the four allowed
  enum values, `evidence` as a non-empty list with a real file-level
  citation, `created_at`, `immutable: true`) is populated validly, and the
  brief's prose includes a genuine logic-trace section and file-level
  evidence citations (so the structural/content checks at
  validate-brief.py:600-609 also pass). EMPIRICALLY CONFIRMED (see
  `verified_failed_boundary`): this isolates the failure to exactly one
  blocking error, `recommended_workflow_id.unknown_value`; a follow-up test
  changing only that one field to a real registry id
  (`architecture-implementation-workflow`) and re-running the same
  validator produced `"valid": true`, `"errors": []`.
recovery_invocation: |
  python scripts/workflow-runtime.py "<same problem statement used in the
  first attempt>" --repo-root <scratch-clone-root> --workflow
  t3m-k7x-diagnostic-setup-workflow --mode autonomous_execution --log-dir
  <scratch-clone-root>/artifacts/<first-attempt-session-dir> --resume

  `--log-dir` here must point at the directory that holds the FIRST
  attempt's `run_log_t3m-k7x-diagnostic-setup-workflow_autonomous_execution.md`,
  since `_find_resume_state()` (line 1956) builds the path to read as
  `os.path.join(self.log_dir, f"run_log_{self.workflow_id}_{self.mode}.md")`.
  Per the substrate note: `--log-dir` only controls where the PRIOR run log
  is read from for resume-state discovery — it does NOT control where the
  new attempt's own ledger goes. Absent `--from-session`, a fresh
  `artifact_session_dir` (and thus a fresh `run-ledger.jsonl`) is
  auto-generated via `_generate_session_id()` (line 151-155,
  `orchestration-<timestamp>-<uuid8>`) for this second invocation.

  REVISED after a third cross-tranche finding (same gap class already fixed
  in T3M-P4W and T3M-R2B): `_check_clean_git()` (workflow-runtime.py:
  130-139) runs a plain `git status --porcelain` check, and
  `preflight_check()` (lines 537-560) turns any non-clean result into a
  hard `PREFLIGHT_FAILED` for `autonomous_execution` mode — unconditionally,
  before Phase 2 ever runs. Unlike T3M-P4W/T3M-R2B, K7X does NOT use
  `--from-session`, so there is no per-attempt seed directory to commit
  before invocation 1 — the only initial-state commit is the ONE-TIME
  bespoke-registry-entry commit already documented in
  `initial_state_specification` (applied once, before invocation 1, not
  repeated per attempt). But a SECOND commit is still required, and was
  previously undocumented: invocation 1's own output (the new
  `<NN>-orchestration-run/` session directory — `00-user-intent.md`,
  `plan_*.md`, `diagnostic_*.md`, `implementation_*.md`,
  `workflow_summary.json`, `run-ledger.jsonl`, run log,
  `repository_sensemaking_brief.md` — plus the modified
  `docs/mode-coverage.yaml`) leaves the tree dirty and must be committed
  (`git add -A && git commit -m "invocation 1 output: t3m-k7x attempt 1"`)
  before the resume invocation above, or the resume aborts before step 1
  is even skip-reconstructed.

  EMPIRICALLY CONFIRMED end-to-end against a REAL git-tracked clone
  (git-init'd frozen-SHA archive with the bespoke registry entry committed
  as baseline, real commits, stub skill-invocation layer standing in only
  for the actual model call): (a) with the registry entry already
  committed as baseline, invocation 1 succeeds cleanly and reaches step 2
  FAILED with the target validator error (not a preflight abort), leaving
  the tree dirty (`M docs/mode-coverage.yaml` plus the new untracked
  session directory); (b) running the resume WITHOUT committing that
  output genuinely aborts with `PREFLIGHT_FAILED: Git working tree is not
  clean:\nM docs/mode-coverage.yaml\n?? artifacts/<NN>-orchestration-run/`;
  (c) after committing invocation 1's output, the resume succeeds: step 1
  skip-reconstructed (`COMPLETED`, `resumed_from_previous_session`), step 2
  genuinely re-executed and reached `VALIDATED`, writing to a NEW
  auto-generated session directory exactly as this field already
  documented, with no duplicate step-1 events across the two attempts'
  separate ledgers (2 step_id-"1" events total, both from attempt 1's own
  ledger; 8 step_id-"2" events total across both ledgers' two genuine
  sequences).
resume_expectations: |
  `_find_resume_state()` (line 1951) parses the first attempt's run log with
  the regex at lines 1969-1972, extracting `(step_id, status)` pairs. Step
  1's logged status `VALIDATED` is a member of
  `_resumable_terminal_statuses()` (line 1916-1949, which returns
  `{MODE_CEILINGS["autonomous_execution"], "COMPLETED"}` ==
  `{"VALIDATED", "COMPLETED"}`), so step 1 goes into `completed_steps`.
  Step 2's logged status `FAILED` is in neither `resumable_statuses` nor
  equal to `"PAUSED"`, so it is excluded from both `completed_steps` and
  `paused_step` (lines 1973-1978) — by construction of the membership
  check, not by any special-cased "skip FAILED" branch.
  In `run()`, `resume_skip` (line 2594) is built from `completed_steps`
  (and `paused_step` if any); it will be `{1}`, not `{1, 2}`. The step loop
  (lines 2605-2624): for i=1 (in `resume_skip`), a synthetic `COMPLETED`
  result is appended without calling `execute_step()` (lines 2606-2621);
  for i=2 (not in `resume_skip`), `execute_step()` is called again for real
  (line 2623), genuinely re-invoking the `repo-sensemaker` skill and
  re-running `_run_validator_stack()` against the newly produced artifact.
  Because this bespoke workflow has exactly 2 steps (unlike the real
  `setup-sensemaking-repo`), the step loop ends after step 2 succeeds — there
  is no step 3 to genuinely execute, and therefore no risk of the resumed
  run ending in a second, unrelated FAILED step from the generic-validator
  `--json` bug.
protected_work: |
  Step 1 has no output artifact, so there is no artifact file to compare
  byte-for-byte. The protected invariant is LEDGER SILENCE for `step_id:
  "1"`: the resumed run's OWN `run-ledger.jsonl` (in the NEW
  auto-generated session directory — see below) must contain no
  `step_started`, `artifact_created`, `validation_completed`, or
  `step_completed` events carrying `"step_id": "1"` at all; the first
  attempt's separate ledger (in the OLD session directory) already has
  step 1's only two events (`step_started`, `step_completed`) and those
  must stay unduplicated there.

  REVISED after review — IMPORTANT CORRECTION (same run-log-vs-ledger
  distinction already learned and documented elsewhere in this
  construction — the T3 pilot oracle correction, and Tranche-2 T3's
  "hard-won lesson #2"): the claim that "the first attempt's run log file
  ... must remain byte-identical on disk" was FALSE and is retracted.
  `--log-dir` is passed EXPLICITLY on the resume (pointing at the OLD
  session directory, so `_find_resume_state()` can locate the prior run
  log) — and that explicit value never equals the bare default
  `os.path.join(repo_root, "artifacts")`, so the log_dir-promotion logic in
  `_create_user_intent_artifact()` (lines 481-482: `if not self.log_dir or
  self.log_dir == os.path.join(self.repo_root, "artifacts"):
  self.log_dir = self.artifact_session_dir`) never fires for it. `self.log_dir`
  stays pinned to the OLD session directory for the ENTIRE resumed run, and
  `write_run_log()` (line 1995, `os.path.join(self.log_dir, ...)`) —
  along with `generate_diagnostic_report()` (line 2277) and
  `generate_implementation_report()` (line 2445) and
  `generate_workflow_summary_json()` (line 2394), which all resolve their
  output paths from `self.log_dir` the same way — OVERWRITES the ORIGINAL
  files in place at the SAME path. EMPIRICALLY CONFIRMED by direct hash
  comparison: the run log, diagnostic report, implementation report, and
  `workflow_summary.json` in the first attempt's session directory all had
  DIFFERENT sha256 hashes after the resumed run than after attempt 1 alone
  (same file path each time — `git status` after the resumed run showed
  these four files as `M` — modified tracked files — not new untracked
  ones). None of these four files are protected or diffable as "untouched."
  (`self.artifact_session_dir`, by contrast, DOES get reset to a fresh
  `NN-orchestration-run` directory on the resumed run, since
  `_create_user_intent_artifact()` runs again whenever
  `not self.artifact_session_dir` — true here, since K7X doesn't use
  `--from-session` — which is why `plan_*.md`, `00-user-intent.md`,
  `repository_sensemaking_brief.md`, and `run-ledger.jsonl` DO land in a
  genuinely new directory each attempt, distinct from the `self.log_dir`
  files above.) The only genuinely protected/verifiable state across
  attempts is: (a) `run-ledger.jsonl`, append-only within each attempt's
  own session directory and never rewritten once written (confirmed via
  the step_id "1" event-count check above), and (b) — not applicable here,
  since step 1 produces no artifact to hash-check (unlike T3M-P4W, where
  step 1's `repository_sensemaking_brief.md` IS a hash-checkable protected
  artifact).
forbidden_reset_restart_behavior: |
  Explicitly out of bounds for exercising this recovery path: (1) running
  `git reset --hard` / `git clean -fd` on the scratch clone between the
  failed and resumed attempts — note the runtime's own `rollback()` (line
  2511-2521) PRINTS exactly this suggestion after a FAILED step as
  human-facing advice; a materialized oracle must confirm the agent did NOT
  follow it, since doing so would destroy the committed session-directory
  state (including `run-ledger.jsonl`) the resume mechanism depends on; (2)
  deleting or truncating `run-ledger.jsonl` (the genuinely append-only,
  protected record — see `protected_work`) and re-invoking without
  `--resume` (a fresh, non-resumed run from scratch); note the run log,
  diagnostic report, implementation report, and `workflow_summary.json`
  are legitimately OVERWRITTEN in place by the resumed run itself (see
  `protected_work`'s correction) — regenerating/overwriting THOSE is
  normal, expected behavior, not the forbidden act; only deleting the
  ledger (or the whole session directory before it's committed) qualifies;
  (3) hand-editing the first attempt's run log to change step 2's logged
  status from `FAILED` to `VALIDATED`/`COMPLETED` so it gets synthetically
  skipped instead of genuinely retried — note this edit would itself be
  overwritten by the resumed run's own `write_run_log()` call regardless,
  but `_find_resume_state()` reads the run log BEFORE that overwrite
  happens, so a hand-edit performed before the resume invocation would
  still corrupt the resume decision even though the file doesn't survive
  the run afterward.
idempotency_expectations: |
  "No duplicate semantic work" here means: after the resumed run completes,
  `run-ledger.jsonl` (old file plus new file, read together) must show
  exactly ONE `step_started`/`step_completed` pair for `step_id: "1"` (from
  the first attempt only) — a second occurrence for step_id "1" in the new
  ledger would indicate step 1 was silently re-executed rather than
  skip-reconstructed. For step 2, TWO occurrences of
  `step_started`/`artifact_created`/`validation_completed`/`step_completed`
  for `step_id: "2"` are expected and correct (one FAILED sequence from the
  first attempt, one new sequence — ideally VALIDATED — from the resumed
  attempt); that is the genuine retry, not a duplicate. `run_started` (line
  2561-2567) and `run_completed` (~line 2730) firing once per invocation
  (i.e., twice total across both attempts, once per session_id) is expected
  bookkeeping, not evidence of duplicate work, and must not be
  misclassified as such by a materialized oracle. Because this workflow has
  exactly 2 steps, there is no `step_id: "3"` at all — a materialized
  oracle should treat any `step_id: "3"` event appearing anywhere in either
  ledger as a structural anomaly (wrong workflow definition loaded), not as
  legitimate new work.
oracle_requirements: |
  A materialized oracle for this spec needs to check, applying the seven
  recovery-chain links from the substrate to this scenario: (1) the first
  attempt's step 2 genuinely reached FAILED via a real validate-brief.py
  content failure (parse the run log / validator_stack output for
  `recommended_workflow_id.unknown_value`, not a crash/traceback); (2) step
  1's logged status in that same run log is `VALIDATED` (or `COMPLETED`),
  proving genuinely completed prior work; (3) the resumed invocation's
  console/log output or run log shows step 1 skipped with a
  "resumed_from_previous_session" gate_result / synthetic reconstruction,
  not a real re-execution; (4) the resumed invocation's new
  `run-ledger.jsonl` contains a fresh `step_started`...`step_completed`
  sequence for step_id "2" only; (5) no `step_id: "1"` events appear in the
  new ledger (reset-laundering / duplicate-work detector per
  `idempotency_expectations` above); (6) the new attempt's step 2 artifact
  now has a valid `recommended_workflow_id` and the run log (in the FIRST
  attempt's session directory — legitimately overwritten in place by the
  resumed run, not a new file; see `protected_work`'s correction) shows
  step 2 as `VALIDATED`; (7) none of the `forbidden_reset_restart_behavior`
  items occurred — checkable via git reflog / working-tree cleanliness on
  the scratch clone, and via inspecting the append-only
  `run-ledger.jsonl` in EACH session directory separately for the correct
  step_id "1"/"2" event counts (per `protected_work`/`idempotency_expectations`)
  — NOT via diffing the run log file, which is expected to differ (it is
  overwritten by design, not evidence of reset-laundering on its own).
  Additionally specific to this revised spec: (8) the resumed run ends
  cleanly after step 2 (`steps_failed: 0` in the final summary) with no
  step 3 of any kind — confirming the bespoke workflow's 2-step definition
  was loaded, not accidentally the real 3-step `setup-sensemaking-repo`.
complexity_breakdown: |
  MEDIUM: exactly one failing step (step 2) out of two total steps; the fix
  is a single, unambiguous field-value change (replace the hallucinated
  `recommended_workflow_id` with a real id from the registry) with no
  branching logic, no schema redesign, and no dependency on an
  under-specified runtime code path (contrast with `workflow_orchestration_plan`,
  which this spec deliberately avoids per the substrate's own caution about
  its 3-missing-field generator gap). Step 1 contributes no validation
  surface at all (no output_artifact), which keeps the "earlier completed
  work" precondition trivial to satisfy and verify. The 2-step bespoke
  restructuring (vs. the real 3-step `setup-sensemaking-repo`) is itself
  part of what keeps this MEDIUM rather than HIGH: with the real 3rd step
  included, a fully successful resumed run would require fixing TWO
  unrelated defects (the recommended_workflow_id content bug AND the
  generic validator's unconditional `--json` argparse crash), which is not
  a "single clear fix" by any reasonable reading.
initial_state_specification: |
  A disposable scratch clone of the repo at frozen SHA
  0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5, with a clean git working tree
  (required by the runtime's preflight check), PLUS one addition applied
  and committed before dispatch: a new workflow entry inserted into a
  scratch copy of `skills/workflow-planner/references/workflow-registry.yaml`
  (under the top-level `workflows:` key):

    id: t3m-k7x-diagnostic-setup-workflow
    display_name: T3M-K7X Diagnostic Setup (pilot-scoped)
    purpose: Disposable pilot-only 2-step slice for Autonomous Task v2 T3
      recovery-mechanics testing.
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

  This mirrors how the disposable T3 pilot's own task (`T3-PILOT-TASK.md`)
  adds a bespoke workflow entry (including an explicit
  `allowed_execution_modes: [autonomous_execution]`) to a scratch registry
  copy before dispatch — never a change to the real registry. No fixture
  repair is needed: `setup-sensemaking-skills` requires no pre-existing
  example fixture (it reads `repository_state` directly), and the step-2
  `repository_sensemaking_brief` is authored fresh by the dispatched
  agent/skill during execution — the deliberately-wrong
  `recommended_workflow_id` is produced by the agent's own (first-attempt)
  output, not pre-seeded into the repo. `workflow-registry.yaml`'s
  pre-existing entries (used for the recommended_workflow_id cross-reference
  check) must otherwise be left unmodified from the frozen SHA.
spec_sha256: 93335ad0b4f8c9177d3dd0619be5c7bd6c61b417ac9f61cf6785b502b5223db3
  # Convention used: sha256 hex digest of the UTF-8-encoded concatenation,
  # in schema order, of the parsed YAML values of candidate_id, family,
  # complexity_level, source_workflow_or_operation, verified_failed_boundary,
  # pre_failure_completed_work_expectations, failure_producing_condition,
  # recovery_invocation, resume_expectations, protected_work,
  # forbidden_reset_restart_behavior, idempotency_expectations,
  # oracle_requirements, complexity_breakdown, initial_state_specification
  # (every field above this one, excluding spec_sha256 and qualification).
  # Recomputed a third time after correcting protected_work/
  # forbidden_reset_restart_behavior/oracle_requirements: the run log,
  # diagnostic report, implementation report, and workflow_summary.json are
  # legitimately overwritten in place on resume (self.log_dir stays pinned
  # to the old session dir), not preserved as distinct new files -- only
  # run-ledger.jsonl is genuinely append-only/protected. Previously
  # recomputed after adding the missing second git-commit step (invocation
  # 1's output, before the resume) to recovery_invocation, needed to
  # satisfy autonomous_execution's unconditional clean-tree
  # preflight gate -- same gap class already fixed in T3M-P4W/T3M-R2B.
qualification: |
  ADMISSIBLE
