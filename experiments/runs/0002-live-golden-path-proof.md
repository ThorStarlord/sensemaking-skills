# Run 0002 — live golden-path proof (pre-execution record)

Written BEFORE execution, per remediation protocol for the follow-up to
issue #39 (tracked in issue #51).

## Code verification (from `scripts/workflow-runtime.py`, read before this run)

1. **Does Step 1 run under `--from-session`?** No. `main()` only sets
   `runner.create_intent_artifact = True` in the `else` branch when
   `--from-session` is NOT given (workflow-runtime.py lines 2959-2963,
   comment at 2960: "New session: enable artifact creation AFTER preflight").
   `initialize_from_session()` (lines 256-297) requires an existing
   `00-user-intent.md` in the given directory (lines 279-283) and reuses that
   directory's session id; it does not itself invoke any skill.
2. **One invocation or two?** A single invocation of
   `architectural-review-planning-workflow` WITHOUT `--from-session` executes
   both of the workflow's steps (registry: `skills/workflow-planner/references/
   workflow-registry.yaml` lines 963-978 — step 1 `repo-sensemaker` ->
   `repository_sensemaking_brief`, step 2 `architectural-review` ->
   `architectural_review_recommendation`) in one run, because step
   invocation is driven by iterating `workflow["steps"]`, not by
   `--from-session`. However, step 2 requires `proposed_direction` content to
   already exist on disk (workflow-runtime.py lines 856-864): if it resolves
   to "not present", the step FAILS explicitly with an `ARTIFACT_NOT_FOUND`
   error whose message says "Supply it as a prewritten artifact before
   invoking this workflow (see --from-session)" (line 861). Because the
   session directory's name (`session_id`) is generated at runtime
   (`_generate_session_id()`, lines 142-146) and there is no CLI flag to pin
   it in advance, `proposed_direction.md` cannot be pre-placed at the correct
   session-scoped path before a fresh session exists. Therefore the
   documented, code-confirmed positive-path sequence is TWO commands:
   - **Stage 1** (new session, no `--from-session`): run the workflow once.
     Step 1 (repo-sensemaker) executes live and produces the brief. Step 2
     (architectural-review) is expected to FAIL explicitly (proposed_direction
     not yet present) — this failure is itself proof the input contract is
     enforced, and it leaves the session directory (with `00-user-intent.md`
     and the brief) intact for reuse.
   - Copy the hand-written `proposed_direction.md` into that session
     directory at its session-scoped path (`artifacts/proposed_direction.md`
     relative to the session dir, per `_scope_to_session_dir`, lines
     1439-1450, and the contract path in `skills/workflow-planner/references/
     artifact-contracts.yaml` line 656).
   - **Stage 2** (`--from-session <that dir>`): re-run the same workflow. The
     runtime reuses the existing session id and intent (lines 2951-2958).
     Step 1 will execute again live (no skip-if-exists guard exists for
     `repository_sensemaking_brief`'s output — that guard, at lines 842-845,
     is written specifically and only for `workflow_orchestration_plan`) and
     regenerate the brief; step 2 now finds `proposed_direction` present and
     executes live, producing the recommendation.
3. **Must `--target-repo` be supplied?** Yes, to analyze a repository other
   than the framework root — `runner.target_repo` defaults to
   `self.repo_root` if omitted (lines 216-219), so the disposable target must
   be passed explicitly via `--target-repo <path>` while `--repo-root` stays
   the framework root, to keep framework and target separated.
4. **Where is the session directory created?** Under
   `<repo_root>/artifacts/<session_id>/` (via `_scope_to_session_dir`,
   scoping any `artifacts/...` path into `self.artifact_session_dir`), i.e.
   under the FRAMEWORK root's `artifacts/` tree, not the target repo.
5. **What does `--gate-decision auto-approve` approve?** Every gate
   encountered during the run (`review_diagnosis` after step 1,
   `review_recommendation` after step 2) is auto-approved and recorded in
   `self.gate_decisions` (lines 1709-1722, 1751-1763) instead of blocking on
   a TTY prompt.
6. **Does any gate still pause?** Only if `--gate-decision` is omitted and
   stdin is not a TTY, which raises an explicit error (lines 1740-1746) —
   with `--gate-decision auto-approve` supplied, no gate pauses.
7. **Exit codes:** `main()` returns `runner.run()`'s return value; a FAILED
   step or unmet preflight returns 1 (see lines 2955-2957 for the
   `--from-session` init-failure path, and the step-FAILED early return at
   lines 863-864 propagating up). A fully successful run is expected to
   return 0. This run record predicts Stage 1 will exit non-zero (step 2
   FAILED by design) and Stage 2 will exit 0 if both steps and both gates
   succeed.

## Planned invocation

- Framework commit (repo-root): `dd8b3e23c133536144c935e9d659cfed3a448873`
  (this worktree, `H:\GithubRepositories\sensemaking-skills\.claude\worktrees\
  agent-a71d0c50e38cec9fe`)
- Target commit: `dd8b3e23c133536144c935e9d659cfed3a448873`
- Target path: disposable `git worktree add --detach` checkout under the
  session scratchpad (outside the framework tree), created read-only for the
  duration of the run (no experiment files or runtime artifacts are written
  into it by design — the runtime writes all artifacts under
  `<repo_root>/artifacts/<session_id>/`, i.e. the framework root, never
  `--target-repo`).
- Session path: not known until Stage 1 runs (session id is generated at
  runtime); will be recorded in the evidence directory after Stage 1
  completes.

### Stage 1 command
```
python scripts/workflow-runtime.py \
  "Analyze this repository's workflow-runtime architecture, identify the weakest boundary affecting reliable evidence-backed orchestration, and recommend the smallest architectural improvement supported by repository evidence." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --gate-decision auto-approve \
  --executor claude-code \
  --target-repo <disposable target path> \
  --repo-root .
```
Expected: step 1 EXECUTED (brief produced), step 2 FAILED
(`proposed_direction` not present) — exit code 1.

### Stage 2 command (after copying hand-written `proposed_direction.md` into
the Stage 1 session dir)
```
python scripts/workflow-runtime.py \
  "Analyze this repository's workflow-runtime architecture, identify the weakest boundary affecting reliable evidence-backed orchestration, and recommend the smallest architectural improvement supported by repository evidence." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --gate-decision auto-approve \
  --executor claude-code \
  --target-repo <disposable target path> \
  --repo-root . \
  --from-session artifacts/<session_id>
```
Expected: step 1 EXECUTED (brief regenerated), step 2 EXECUTED (recommendation
produced) — exit code 0.

- Explicit mode: `guided_execution` (required — `yolo_execution`, the CLI
  default, is not in `allowed_execution_modes` for this workflow).
- Executor: `claude-code` (`ClaudeAgentSdkSkillExecutor`); real skill
  invocation via the Claude Agent SDK, `supports_real_execution=True`.
- Gate policy: `--gate-decision auto-approve` (non-interactive; both gates
  auto-approved and logged).
- Expected brief path: `artifacts/<session_id>/repository_sensemaking_brief.md`
  (exact relative path depends on `artifact-contracts.yaml`; resolved and
  recorded after Stage 1).
- Expected recommendation path:
  `artifacts/<session_id>/architectural_review_recommendation.md`.
- Expected run-log path: within the same session directory (recorded after
  execution).
- Expected exit behavior: Stage 1 exit 1 (step 2 fails by design), Stage 2
  exit 0 (full success) — or, if the live executor is unavailable in this
  sandbox, an EXECUTOR BLOCKER is reported instead of a faked result (see
  Phase 8 verdict in the task report).
- Framework status before run: clean (`git status --short` empty at
  `dd8b3e2`).
- Target status before run: clean, freshly checked out at `dd8b3e2`, in a
  disposable worktree outside the framework tree.

## Negative-path plan (separate fresh session)

A second, independent Stage-1-only invocation (new session, no
`--from-session`) against the SAME disposable target, WITHOUT ever creating a
`proposed_direction.md` for that session. Step 1 (repo-sensemaker) is expected
to execute; step 2 is expected to fail explicitly with the same
`ARTIFACT_NOT_FOUND` message, at input resolution, before any
architectural-review invocation, with no recommendation artifact produced and
the target repository unchanged.
