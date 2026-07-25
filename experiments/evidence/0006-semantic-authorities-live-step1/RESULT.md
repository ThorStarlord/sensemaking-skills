# 0006 — Semantic Authorities Live Step-1 Rerun — Result

## Classification: LIVE STEP 1 PROVEN

The live Step-1 rerun completed and the model-produced
`repository_sensemaking_brief` passed validation (`validate-and-report.py`,
1.0s, `[OK]`) without any manual repair. The injected semantic authorities
were consumed correctly: `recommended_workflow_id: skill-maintenance-loop`
(a real top-level ID from the 22-item list), the weakness-type line uses
`Safety Gaps` (one of the 7 canonical enum values, not a fog-type value),
`primary_fog_type: architecture_fog` is kept separate from the weakness
type, and Section 7's prose contains literal file citations (e.g.
`src/sensemaking_skills/skills/workflow_planner.py (lines 88-116)`,
`PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 40-65)`), satisfying the Section 7
file-citation requirement PR #59 added.

Full artifact, ledger, tool-call trace, run log, and workflow summary are
under `final-run-e787fc41/` in this directory.

## IMPORTANT — process-fidelity disclosure

**This run took longer to complete (~6 minutes) than it first appeared,
and Step 2 (architectural-review) auto-cascaded and ran, in violation of
the task's instruction to run Step 1 only.** This must be reported honestly:

1. The run was launched as `run3` (background). An early poll loop (using
   `pgrep -f "workflow-runtime.py"`) reported `PROCESS_ENDED` after ~60s with
   both stdout/stderr at 0 bytes, which I misread as an early silent crash
   (`pgrep` was almost certainly not matching the actual child process on
   this Windows/git-bash setup, and the 0-byte logs were block-buffered
   output not yet flushed, not evidence the process had died).
2. Believing run3 dead, I launched a second attempt (`run4`) with `python -u`
   to capture a traceback for what I thought was a crash. `run4` immediately
   failed pre-flight (repo-root dirty from run3's in-progress writes) — this
   is what I initially reported as a repeatable "EXECUTOR FAILURE."
3. **Run3 was in fact still alive the whole time**, executing a genuine live
   model call against the `--target-repo`, and only reported its real
   completion (exit code 2) several minutes later, well after I had already
   started cleaning up what I believed was crash pollution and had drafted
   an incorrect "EXECUTOR FAILURE" classification.
4. Because guided_execution's `--gate-decision auto-approve` auto-approves
   every gate in the workflow (not just Step 1's gate), and I was not
   actively watching the live log at the moment Step 1's gate resolved, the
   runtime proceeded directly into Step 2 (`architectural-review`) rather
   than stopping after Step 1 as instructed. By the time this was
   discovered (from the completion notification and `stdout3.log`), Step 2
   had already been attempted and had already failed.
5. **What Step 2 actually did**: per `run_log_architectural-review-planning-workflow_guided_execution.md`,
   Step 2 failed immediately on a precondition check —
   `ARTIFACT_NOT_FOUND: Step 2 (architectural-review) requires 'proposed_direction'
   but no content was found at .../artifacts/05-orchestration-run/proposed_direction.md`
   — before the `architectural-review` skill or its executor was ever
   invoked. The `tool-call-trace.jsonl` confirms the trace ends at the Step 1
   reconciliation event; no Step-2 tool calls (Read/Write/Edit/etc.) exist.
   **No live architectural-review model work was performed.** This is a
   scope violation of the letter of the task instruction ("do not run Step
   2"), but not of its substance (no actual architectural-review execution,
   analysis, or artifact happened) — it was an instant, harmless
   precondition failure caused by the same auto-approve gate cascading past
   Step 1.

This is reported here in full rather than omitted, per this repo's own
"done requires running the real path" / evidence discipline. The correct
process for a Step-1-only run under this runtime would require actively
watching gate resolution in real time and killing the process the instant
Step 1's gate is approved — `--gate-decision auto-approve` does not offer a
"stop after step 1" option on its own, and my polling logic failed to
observe the process in real time during the ~6-minute window it was
actually alive.

## Pre-existing structural verification (Phase 1)

- Branch `fix/repo-sensemaker-semantic-authorities`, HEAD `a3ea1e0440ce7eb68e2a3bdffe273c294cd1c5db`.
- `scripts/skill_executor.py` contains `build_semantic_authorities_block`,
  `get_allowed_workflow_ids`, `get_allowed_weakness_types`, and
  `build_skeleton_prompt` (confirmed by direct grep).
- `pytest tests/test_semantic_authorities.py tests/test_brief_skeleton.py tests/test_skill_executor_skeleton_and_trace.py`
  → 36 passed.
- `python scripts/test-validators.py` → 66/66 passed.
- Injected authorities captured directly from code
  (`injected_semantic_authorities_block.txt`): 22 top-level workflow IDs,
  7-value weakness-type enum, fog-type/weakness-type/workflow-ID
  disambiguation, Section 7 file-citation requirement.

## Exact command

```
python scripts/workflow-runtime.py "Analyze this repository's workflow-runtime architecture, identify the weakest boundary affecting reliable evidence-backed orchestration, and recommend the smallest architectural improvement supported by repository evidence." --workflow architectural-review-planning-workflow --mode guided_execution --gate-decision auto-approve --executor claude-code --target-repo "H:/scratch-0006-live-step1/target" --repo-root . --log-dir "H:/scratch-0006-live-step1/logs"
```

Run from the framework worktree root. Session ID:
`orchestration-20260725-180432-e787fc41`. Total wall-clock: approx. 6
minutes (well within the 15-minute cap). Final process exit code: 2
(`"failed"` — attributable entirely to Step 2's auto-cascade, not Step 1,
which succeeded and validated).

## Target immutability

`H:/scratch-0006-live-step1/target` (disposable git worktree,
`--target-repo`) had **empty `git status --short` before and after** the
full run, including after Step 1's live model call. The tool-call trace
shows the model briefly attempted a `Write` to
`H:\scratch-0006-live-step1\target\artifacts\05-orchestration-run\repository_sensemaking_brief.md`
(flagged `targets_expected_artifact: false`) before correctly reading from
and writing to the actual runtime-authorized path under the framework
worktree's `artifacts/05-orchestration-run/` (flagged
`targets_expected_artifact: true`), which reconciled successfully
(`Reconciliation ... integrity_ok: true`). No file was left behind in the
target from that initial off-target attempt — target confinement held.

## Framework pollution (flagged, not fixed — same pattern as issue #56)

Both attempts wrote a new, untracked `artifacts/05-orchestration-run/`
directory into the **framework** worktree (`--repo-root .`) rather than
under `--target-repo`. This traces directly to
`OrchestrationRunner._resolve_artifact_path` in `scripts/workflow-runtime.py`
(around line 1428): `os.path.join(self.repo_root, resolved_path)` — this
join always uses `self.repo_root` and never consults `self.target_repo`.
This is purely additive (a new untracked directory, nothing overwritten)
and has been removed from the framework worktree after being copied into
this evidence directory (`final-run-e787fc41/`).

**More serious finding**: `update_mode_coverage()` (invoked at Phase 5)
**destructively overwrote** the existing `docs/mode-coverage.yaml` entry for
`architectural-review-planning-workflow` / `guided_execution` — it replaced
run 0005's `run_log_path`, `steps_completed` (1 -> 0), and `notes` fields in
place rather than adding a new entry or preserving history. This is exactly
the destructive-overwrite pattern flagged under issue #56 and is **not
fixed here** per the task's explicit instruction not to repair that pattern
in this task. `docs/mode-coverage.yaml` was reverted (`git checkout --`) to
its pre-run committed state before this evidence was committed, so this
run's mutation is not persisted — only documented here.

## Answers to Phase 5 classification menu

**LIVE STEP 1 PROVEN.** Brief passed validator without manual repair; target
unchanged. (See process-fidelity disclosure above for the Step-2 scope
overrun and its cause — it does not change the Step 1 result, since Step 2
never performed real work and never touched the target or produced a
competing artifact.)

## Conclusion for issue #58 / PR #59

Issue #58's live Step-1 criterion is now satisfied: the injected semantic
authorities (workflow-ID list, weakness-type enum, fog-type/weakness-type/
workflow-ID disambiguation, Section 7 file-citation requirement) were
demonstrated, in a live model call against a disposable target repo, to
produce a brief that validates on first attempt with correct values drawn
from all three vocabularies. Step 2 (architectural-review) remains
separately unproven — the one attempt that occurred was an immediate,
harmless precondition failure with zero real analysis performed, and is not
a legitimate Step-2 trial. Step 2 / the full golden path should not be
considered justified by this run.
