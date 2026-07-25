# Live Step 1 rerun of the runtime-owned brief skeleton (issue #55 / PR #57)

## Purpose

The first live Step 1 attempt for PR #57 was killed by a ~70-second harness
timeout while the model was still analyzing the repository (no `Write` call
in the preserved trace) -- classified INCONCLUSIVE, not a failure of any
kind. This run repeats the attempt with a substantially longer bounded
budget (15 minutes wall-clock) to obtain one actual completed result.

## Framework / target

- Framework: this worktree, branch `fix/runtime-owned-brief-skeleton` @
  commit `32440d7ff590bf146bb0459e7e895b6e0ea9ee51` (PR #57's head, unchanged
  by this run).
- Target: a fresh disposable `git worktree add --detach origin/main`
  checkout at `dd8b3e2` (`sensemaking-skills-target-0005`, outside the
  framework tree), read-only for the duration of the run.

## Exact command

```
python scripts/workflow-runtime.py "Analyze this repository's workflow-runtime architecture, identify the weakest boundary affecting reliable evidence-backed orchestration, and recommend the smallest architectural improvement supported by repository evidence." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --gate-decision auto-approve \
  --executor claude-code \
  --target-repo <disposable target-0005 checkout of origin/main @ dd8b3e2> \
  --log-dir <scratch log dir, same drive as framework root>
```

(The `--log-dir` was placed on the same filesystem drive as the framework
root; an initial attempt using a cross-drive temp directory hit an
`os.path.relpath` `ValueError` -- an environment/path issue unrelated to
PR #57's code, fixed by relocating the log dir rather than by any code
change.)

## Timeout budget

15 minutes wall-clock (substantially longer than the first attempt's ~70
seconds). The run completed naturally in under 5 minutes; the budget was
never exhausted.

## Process outcome

- Overall orchestrator exit code: 2 (`Status: failed`, `Steps: 0/2`).
- Step 1 (`repo-sensemaker`) executed live via the real `claude-code`
  executor and completed: it read the target repository, produced a filled
  brief, and the runtime's reconciliation step ran with
  `integrity_ok: true`.
- The run **halted after Step 1's validator failure** -- **Step 2
  (`architectural-review`) was never started.** Confirmed via the run
  ledger (`run-ledger.jsonl` in this folder): only `step_id: "1"` events
  appear; the process exited (`run_completed`, `status: failed`) before any
  `step_id: "2"` event.

## Tool-call trace summary (see `tool-call-trace.jsonl`)

| Time (approx) | Tool/action | Target | Result | Significance |
|---|---|---|---|---|
| 16:18:57 | SkillInvocation | expected brief path | started, `uses_runtime_skeleton: true` | Confirms the runtime pre-wrote the skeleton before the model ran |
| 16:19:07-16:20:13 | Read / Glob / Grep (repeated) | target repo files: existing brief-shaped artifacts, CONTEXT.md, README.md, PHASE-4-COMPLETE-FINAL-UPDATED.md, CURRENT-PROJECT-STATUS.md, `workflow_planner.py` | observed/completed | Model explored the target repo, including several stale historical status docs already present in the target's committed history |
| 16:21:21 | PreToolUse Write | `sensemaking-skills-target-0005\artifacts\repository_sensemaking_brief.md` | observed, `targets_expected_artifact: false`, **no matching PostToolUse "completed" event follows** | Model attempted to write to a path that is neither the expected output path nor even inside the framework session dir; the write was not completed. Confirmed separately: `git status --short` in the target checkout is empty both before and after the run, so no target mutation occurred. |
| 16:22:31 | Read | expected skeleton path (framework session dir) | observed/completed | Model read back the runtime-generated skeleton |
| 16:23:31 | Write | expected skeleton path (framework session dir) | observed/completed, `targets_expected_artifact: true` | The model's actual, successful write landed at the correct runtime-resolved path |
| 16:23:43 | Reconciliation (`brief_skeleton.reconcile`) | expected skeleton path | `decision: ok`, **`integrity_ok: true`** | Runtime-owned envelope survived reconciliation intact |

No SKILL.md read event is separately logged by this trace (the SDK loads
`SKILL.md` content via `skills=[skill_id]` wiring proven by the existing
`test_repo_sensemaker_live_prompt_contract.py`; this trace instruments
tool calls, not skill-content loading). No whole-file replacement of the
expected path was observed -- the only interaction with the expected path
was a normal `Read` then `Write` then a successful reconciliation.

## Final validator result

`validate-and-report.py` (unified validator) rejected the completed brief on
**three model-authored semantic fields only**:

```
repository_sensemaking_brief.recommended_workflow_id.unknown_value: HALLUCINATED_WORKFLOW_ID:
  Recommended workflow ID 'architecture-orchestration-validation' ...
NO_EVIDENCE_FILE_CITATIONS: Evidence section has no file-level citations (e.g., ...)
UNKNOWN_WEAKNESS_TYPE: Weakest boundary does not include a recognized weakness type ...
```

Inspecting the final brief (`repository_sensemaking_brief.md` in this
folder), Section 13's runtime-owned fields (`artifact_id`, `schema_version`,
`source_intent_ref`, `created_at`, `immutable`) are present and correct.
The three rejected fields are exactly the model-authored ones:
- `recommended_workflow_id: architecture-orchestration-validation` -- not a
  real id in `workflow-registry.yaml`.
- `evidence:` entries use a `"file.md (lines 1-20): ..."` prose citation
  style, not the validator's accepted `Lx` / bare-number grammar.
- `weakest_boundary: unproven_multi_phase_orchestration` -- not one of the
  validator's recognized weakness-type labels.

The model also repeated the pre-existing pattern (seen in PR #54's rerun)
of treating stale historical status docs
(`PHASE-4-COMPLETE-FINAL-UPDATED.md`, `CURRENT-PROJECT-STATUS.md`) in the
target repo as current evidence, despite the Evidence Authority Hierarchy
guidance -- this is not a defect of PR #57 (which only changes structural
ownership, not semantic guidance) but is noted for context.

## Classification: STRUCTURE PROVEN, SEMANTIC VALIDATION FAILED

The runtime-owned skeleton and its structural fields survived the full live
round trip (pre-write, model read/write, reconciliation with
`integrity_ok: true`); the model completed and produced content; the final
brief fails validation **only** on semantic/model-authored contract fields
(workflow-id hallucination, evidence-citation grammar, weakness-type label)
-- not on any structural or runtime-owned field. This is not a skeleton
integrity failure, not an executor failure, not a confinement failure, and
not a timeout.

## Target immutability

`git -C <target-0005> status --short`: empty before and after the run.
The one off-path `Write` attempt observed in the tool-call trace did not
result in any on-disk change to the target.

## Framework pollution

`git status --short` in the framework worktree after the run:
- `docs/mode-coverage.yaml` (modified -- additive new entry plus
  `last_run`/`last_session` pointer updates; no historical entries removed)
- `_tmp_evidence_0005/` (this run's scratch log dir; copied into this
  evidence folder, original left in place per instructions not to
  overwrite/remove pre-existing scratch without need -- safe to delete)
- `artifacts/05-orchestration-run/` (new session artifacts -- expected,
  copied into this evidence folder)

No other framework files were modified. `git diff --check`: clean.

## Verification (Phase 8)

- `python scripts/test-validators.py`: full fixture suite passes (unchanged
  by this run; see `validator_baseline_output.txt`).
- `python scripts/validate-repo.py`: passes.
- `pytest tests/test_brief_skeleton.py tests/test_skill_executor_skeleton_and_trace.py`:
  **19/19 pass**.
- `git diff --check`: clean.
- No orphan `python`/`claude` child processes remained after the run
  completed and was reaped.

## Files in this folder

- `stdout.log` -- full orchestrator stdout/stderr.
- `run-ledger.jsonl` -- ledger events for this run.
- `tool-call-trace.jsonl` -- PreToolUse/PostToolUse/Reconciliation trace
  added by PR #57.
- `repository_sensemaking_brief.md` -- the final (post-reconciliation)
  brief.
- `run_log.md`, `implementation_report.md`, `diagnostic_report.md`,
  `workflow_summary.json` -- standard orchestrator run artifacts.
- `validator_baseline_output.txt` -- `scripts/test-validators.py` output
  captured after this run.
