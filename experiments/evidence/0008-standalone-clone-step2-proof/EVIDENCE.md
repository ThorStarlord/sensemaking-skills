# 0008 - Standalone-clone Step 2 proof (positive + negative)

Related: issue #51, historical issue #39, PR #59, PR #62 (issue #61), PR #64 (issue #63).

## Setup

- Standalone clone (NOT a linked worktree): `H:/scratch/sensemaking-step2-framework`,
  origin `H:\GithubRepositories\sensemaking-skills` (a real `git clone`, own `.git`).
- HEAD: `4470d0040f5b8966771bb9593efcaa738787a8e9` (merge commit for PR #64,
  "fix/architectural-review-yaml-fence-contract").
- Confirmed NOT present in the primary checkout's `git worktree list` (see
  `primary-worktree-list.txt` in this directory - the standalone clone path does
  not appear in that output; only `.claude/worktrees/*` and other pre-existing
  worktrees/clones are listed).
- `git status --short` clean at clone time; `skills/`, `scripts/workflow-runtime.py`,
  `docs/mode-coverage.yaml`, `.git/` all present.
- Pre-run manifest: 3282 tracked files (`git ls-files`), captured as
  path|size|mtime in `pre-run-manifest.txt`.
- `scripts/skill_executor.py` (read directly from the standalone clone) confines
  the live agent to `allowed_tools=["Read", "Write", "Glob", "Grep"]` - no Bash,
  no PowerShell - confirmed before either run, not assumed.
- Disposable targets: `H:/scratch/target-positive` and `H:/scratch/target-negative`,
  each a `git worktree add --detach` off the standalone clone (HEAD
  `4470d0040f5b8966771bb9593efcaa738787a8e9`), not off the primary checkout.

## Inputs

PR #59's real Step-1 evidence, from
`experiments/evidence/0006-semantic-authorities-live-step1/` inside the standalone
clone:
- `final-run-e787fc41/repository_sensemaking_brief.md`
- `final-run-e787fc41/run_log_architectural-review-planning-workflow_guided_execution.md`
  (Step 1 status APPROVED, session `orchestration-20260725-180432-e787fc41`)
- `mid-run-snapshot-misdiagnosed-as-crash/00-user-intent.md` - verified as the
  correct file (not `final-run-e787fc41`, which has none) by matching
  `run_id: orchestration-20260725-180432-e787fc41` in `run-ledger.jsonl` in both
  directories.

Copied unmodified into two disposable sessions:
- `H:/scratch/step2-positive-session/` (+ hand-written `proposed_direction.md`)
- `H:/scratch/step2-negative-session/` (no `proposed_direction.md`)

`proposed_direction.md` (positive session) addresses the brief's stated weakest
boundary - "unproven multi-phase orchestration" (Section 6) - by proposing to
prove the existing 2-step architectural-review-planning-workflow end-to-end
(positive + negative path) rather than building a fifth untested workflow. Full
text in `positive/proposed_direction.md`.

## Preflight (mandatory, before either run)

- `validate-brief.py` on positive session's brief: PASSED
  ("Brief verification passed! All required fields are present and valid.")
- `validate-artifact.py proposed_direction` on positive session:
  PASSED (`[PASS] Required fields present`, `[OK] All fields (required +
  recommended) present`)
- Direct check of the real `OrchestrationRunner._find_resume_state()` from the
  standalone clone's own `scripts/workflow-runtime.py`, pointed at the copied
  run log: `{'completed_steps': [1], 'paused_step': None, ...}` - Step 1
  confirmed resumable.
- Both disposable targets confirmed clean (`git status --short` empty) at
  HEAD `4470d0040f5b8966771bb9593efcaa738787a8e9`.
- Standalone clone confirmed clean/intact before each run (manifest diffed
  against the captured pre-run baseline; the only diff across both runs was
  `docs/mode-coverage.yaml`'s mtime/size, an expected PHASE 5 side effect of
  the runtime itself, checked back out to a clean state between runs so each
  run's own preflight git-clean check would pass).

## Positive run

Command (see `positive/stdout.log` for full output):
```
python scripts/workflow-runtime.py "<00-user-intent.md's raw_problem_statement>" \
  --workflow architectural-review-planning-workflow --mode guided_execution \
  --from-session H:/scratch/step2-positive-session --resume \
  --gate-decision auto-approve --executor claude-code \
  --target-repo H:/scratch/target-positive \
  --repo-root H:/scratch/sensemaking-step2-framework \
  --log-dir H:/scratch/step2-positive-session
```
- PID: 9171. Polled directly every 15-30s for liveness, sentinel existence
  (`skills/`, `scripts/workflow-runtime.py`, `docs/mode-coverage.yaml`, `.git/`),
  and clone `git status` for the run's ~71s duration. No sentinel loss, no
  unexpected clone mutation observed while running.
- Exit: process completed normally (`run_completed`, `status: completed,
  exit_code: 0` in `run-ledger.jsonl`; CLI summary printed "Execution completed
  successfully.").
- **Resume-detection stdout** (exact lines, `positive/stdout.log`):
  ```
  [OK] Found resume state: 1 completed, paused at step None
  [OK] Resuming: skipping steps [1], starting from step 2
  ~ Step 1 already completed in previous session, skipping (resume mode)
  ```
- **repo-sensemaker not invoked**: `positive/tool-call-trace.jsonl` contains
  only `SkillInvocation` for `architectural-review` plus a `Read` of
  `validate-architectural-review-recommendation.py` - zero repo-sensemaker
  entries. `run-ledger.jsonl` likewise starts at `step_started, step_id: 2`
  with no step_id 1 activity in this run.
- **architectural-review invoked exactly once**: one `SkillInvocation`
  ("started") for `architectural-review` in the trace; one
  `step_completed`/`step_id: 2` in the ledger.
- Recommendation written to `H:\scratch\step2-positive-session\architectural_review_recommendation.md`
  (the runtime-authorized session path passed via `--log-dir`/`--from-session`).
- Fence check: exactly one ` ```yaml ` ... ` ``` ` block (lines 143-185 of
  `positive/architectural_review_recommendation.md`), no tilde fences.
- **Real recommendation validator**:
  `python scripts/validate-architectural-review-recommendation.py <path> --repo-root <clone>`
  -> `OK: Validation passed for ...architectural_review_recommendation.md` (exit 0).
- No manual repair performed on any generated artifact.
- Target (`H:/scratch/target-positive`) remained at HEAD
  `4470d0040f5b8966771bb9593efcaa738787a8e9` with clean `git status` after the run.
- Standalone framework clone manifest unchanged outside `docs/mode-coverage.yaml`
  (expected PHASE 5 bookkeeping write, restored to clean after capture).

**Classification: LIVE STEP 2 PROVEN.**

## Negative run

Same session/target/preflight discipline (minus `proposed_direction` validation,
deliberately absent). First attempt aborted at preflight
(`[FAIL] GIT: Git working tree is not clean`) because the positive run's
mode-coverage.yaml write hadn't yet been checked back out - clone was restored
to clean and the run repeated; this is a preflight-plumbing artifact of running
both proofs back-to-back in the same clone, not a finding about the negative
path itself.

Command:
```
python scripts/workflow-runtime.py "<same intent>" \
  --workflow architectural-review-planning-workflow --mode guided_execution \
  --from-session H:/scratch/step2-negative-session --resume \
  --gate-decision auto-approve --executor claude-code \
  --target-repo H:/scratch/target-negative \
  --repo-root H:/scratch/sensemaking-step2-framework \
  --log-dir H:/scratch/step2-negative-session
```
- PID: 9310. Same sentinel/liveness polling discipline; no sentinel loss.
- Exit: `run_completed`, `status: failed, exit_code: 2` (`negative/run-ledger.jsonl`);
  CLI summary: "Execution completed with failures." (this failure is the expected,
  correct outcome for the negative path).
- **Resume-detection stdout** (same as positive):
  ```
  [OK] Found resume state: 1 completed, paused at step None
  [OK] Resuming: skipping steps [1], starting from step 2
  ~ Step 1 already completed in previous session, skipping (resume mode)
  ```
- **Missing proposed_direction reported**: run log records
  `ARTIFACT_NOT_FOUND: Step 2 (architectural-review) requires 'proposed_direction'
  but no content was found at H:\scratch\step2-negative-session\proposed_direction.md.`
- **architectural-review never invoked**: `negative/` has NO
  `tool-call-trace.jsonl` file at all (contrast with the positive run, where
  the trace file exists and contains the SkillInvocation). `run-ledger.jsonl`
  shows `step_started` for step_id 2 immediately followed by
  `step_completed, status: failed` with no `artifact_created` or
  `validation_completed` events - zero Step-2 tool calls, zero skill
  invocations, before the precondition failure. No recommendation artifact
  exists anywhere in the session directory.
- Target (`H:/scratch/target-negative`) remained at HEAD
  `4470d0040f5b8966771bb9593efcaa738787a8e9`, clean.
- Framework clone manifest unchanged outside the same expected
  `docs/mode-coverage.yaml` bookkeeping write.

**Classification: MISSING-PROPOSED-DIRECTION PATH PROVEN.**

## Golden-path claim

Both classifications above are fully successful (LIVE STEP 2 PROVEN and
MISSING-PROPOSED-DIRECTION PATH PROVEN). Combined with PR #59's existing
Step 1 proof (repo-sensemaker producing an APPROVED brief) and this run's
proof of Step 2 both succeeding and correctly failing closed, **the narrow
golden path (Step 1 + Step 2, positive and negative) is now justified** for
the architectural-review-planning-workflow specifically. This does NOT extend
to the other three implementation workflows, which remain unproven with real
agents (per the brief's own weakest-boundary section).

## Historical partial evidence (NOT this run's result - included for context only)

An earlier attempt at `H:/scratch-step2-positive/session/` (prior to PR #64)
proved resume-skip and exactly-once architectural-review invocation, but its
recommendation output FAILED validation only because the template at the time
instructed a tilde fence (now fixed by PR #64, which also corrected the
template's own worked example). Separately, a harness-managed worktree
(`.claude/worktrees/agent-a4f55c551e2d0c93a`) lost its tracked files during
that earlier session for an unresolved, external reason - confirmed in a prior
forensic investigation to be unrelated to `workflow-runtime.py`/
`skill_executor.py` code and unrelated to the live model (which had no Bash/
PowerShell access). That investigation is not reopened here.

## Files in this directory

- `primary-worktree-list.txt` - `git worktree list` from the primary checkout,
  showing the standalone clone's path absent.
- `pre-run-manifest.txt`, `post-positive-manifest.txt`, `post-negative-manifest.txt`
  - tracked-file path|size|mtime manifests of the standalone clone.
- `positive/`, `negative/` - full session artifacts, logs, traces, and
  recommendation/validator output for each run.
