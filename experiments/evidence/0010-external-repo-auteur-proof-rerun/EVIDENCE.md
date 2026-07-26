# Evidence: External-repo validation rerun (auteur) — architectural-review-planning-workflow

This experiment **supersedes/completes** the attempt in PR #67, which was blocked by a
citation-resolution bug (target-repo citations checked against `repo_root` instead of
`target_repo`) that is now fixed and merged in PR #69 (issue #68).

**Result: campaign stopped at Stage A. Do not merge. Evidence only.**

## Setup

- Framework clone: `H:\scratch\sensemaking-external-exp2-framework`
  (`git clone H:\GithubRepositories\sensemaking-skills`)
  - HEAD: `9acd0e34af8925c99fc8803821c1456c8f37ebbc`
  - Confirmed NOT a linked worktree of the primary repo (own `.git` dir; does not
    appear in `git -C H:\GithubRepositories\sensemaking-skills worktree list`).
  - `git status --short` clean at clone time.
- Target clone: `H:\scratch\auteur-target-readonly-2`
  (`git clone H:\GithubRepositories\auteur`)
  - HEAD: `23b9075ce373eca5fca19ffd6e4e2c33f2589258`
  - Never modified. `git status --short` empty before and after the run; HEAD unchanged
    after the run.
- Confirmed executor confinement in the fresh framework clone before running:
  `scripts/skill_executor.py` line 883 — `allowed_tools=["Read", "Write", "Glob", "Grep"]`
  (Bash/PowerShell not in the allowed set; the tool-call trace shows one `PowerShell`
  PreToolUse event that was merely *observed*, i.e. not permitted/executed).

## Stage A — external live Step 1

Command run from `H:\scratch\sensemaking-external-exp2-framework`:

```
python scripts/workflow-runtime.py "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --gate-decision auto-approve \
  --target-repo H:/scratch/auteur-target-readonly-2 \
  --repo-root H:/scratch/sensemaking-external-exp2-framework \
  --log-dir H:/scratch/exp2-logs/stageA
```

PID: 16380. Launched 2026-07-26T07:50:45 local. Process exited on its own at
approximately 07:53:33 (after ~18 poll iterations of 5s = ~90s post the first 30s poll,
total wall time ~3 min), well inside the 15-minute bound. No manual kill was needed.

### Outcome: repo-sensemaker ran, but the produced brief FAILED the real validator

- `repo-sensemaker` was invoked exactly once (see `stageA/tool-call-trace.jsonl`:
  one `SkillInvocation` event for `repo-sensemaker`, followed by `Read`/`Glob`/`Grep`
  calls into `H:\scratch\auteur-target-readonly-2`, one `Write` to the framework's
  session artifact path, and one `Reconciliation` event).
- `repository_sensemaking_brief.md` was written to the runtime-authorized framework
  session path: `artifacts/05-orchestration-run/repository_sensemaking_brief.md`
  (not under the target repo). See `stageA/repository_sensemaking_brief.md`.
- The unified validator (`validate-and-report.py`, invoked with
  `--target-repo H:/scratch/auteur-target-readonly-2`) **rejected the artifact** with
  10 errors — see `stageA/validator_output.json`:
  - `NO_LOGIC_TRACE`: brief does not include a logic trace showing diagnostic reasoning.
  - `EVIDENCE_EXCERPT_FIELD` x9: `Excerpt[0..4]` each missing required `quote` and/or
    `supports_claim` fields.
- This is a **different, new root cause** than the PR #67 bug. The PR #67 bug was
  `HALLUCINATED_FILE` from citations being resolved against the wrong repo root; that
  path is now confirmed fixed — the validator got far enough to check evidence-excerpt
  *structure* rather than rejecting citations as nonexistent. The new failure is a
  structural/schema conformance issue in the brief's evidence-excerpt blocks (missing
  `quote` / `supports_claim` fields) plus a missing logic trace — i.e. the model-produced
  content did not conform to the `repository_sensemaking_brief` artifact contract
  (`skills/workflow-planner/references/artifact-contracts.yaml`), independent of the
  citation-path issue PR #69 fixed.
- Per the campaign's hard stop rule, this halts the campaign at Stage A. No manual
  repair was performed. No evidence audit or Stage B was attempted.

### Integrity checks

- Target (`H:\scratch\auteur-target-readonly-2`): `git status --short` empty before and
  after; HEAD unchanged (`23b9075c...`). No target mutation occurred.
- Framework (`H:\scratch\sensemaking-external-exp2-framework`): only expected
  session/bookkeeping paths changed — `docs/mode-coverage.yaml` (modified, expected
  runtime bookkeeping) and the new `artifacts/05-orchestration-run/` session directory
  (untracked, expected). No other tracked framework file was touched.

## Stage A classification

**BRIEF VALIDATION FAILED**

Justification: `repo-sensemaker` executed exactly once and produced an artifact at the
correct runtime-authorized path, but the real (target-repo-aware, post-PR#69) validator
rejected it on its first pass, for reasons unrelated to citation-path resolution
(`NO_LOGIC_TRACE`, `EVIDENCE_EXCERPT_FIELD` x9 on the brief's evidence excerpts). No
manual repair was applied, per the campaign's rules. This is a **new** concrete failure
mode, not a recurrence of the already-fixed citation bug.

## Evidence audit / Stage B

Not attempted — the campaign's rules require stopping immediately when Stage A does not
pass. Do not treat any part of Stage B as attempted or proven.

## What is now known about `auteur` specifically

Narrowly: on this one run, against `H:\GithubRepositories\auteur` at HEAD
`23b9075c`, the `architectural-review-planning-workflow`'s first step
(`repo-sensemaker`, `guided_execution`, `claude-code` executor) produced a
repository-goal/current-shape/strong-signals/missing-pieces/weakest-boundary brief
whose *prose content* (see `stageA/repository_sensemaking_brief.md`) identifies the
boundary between auteur's core library and its `scripts/` orchestration
infrastructure (missing external registry files) as the weakest boundary — but this
claim was **not validated** by the real validator due to structural artifact-contract
non-conformance (missing per-excerpt `quote`/`supports_claim` fields and no logic
trace), so **no conclusion can be drawn about whether that specific weakest-boundary
claim is evidence-grounded or useful**. This experiment does not establish, either
positively or negatively, that `architectural-review-planning-workflow` transfers
cleanly to `auteur` — it establishes only that the previously-fixed citation-path bug
(PR #69) is no longer the blocker, and that a distinct evidence-excerpt schema issue is.

## New concrete runtime blocker surfaced

Yes — reportable, not fixed here per the campaign's constraints. The `repo-sensemaker`
skill (as exercised by `architectural-review-planning-workflow` in `guided_execution`
mode against an external target repo) produced evidence excerpts that do not satisfy the
`repository_sensemaking_brief` contract's per-excerpt `quote` / `supports_claim` field
requirements, and omitted the required logic trace. Whether this is a skill-prompt
issue (the model doesn't know to fill in those fields for this artifact shape), a
contract-vs-skeleton mismatch, or something else was not diagnosed further — diagnosis
was intentionally out of scope for this evidence-only campaign per the "do not modify
runtime code" / "report only" constraint.

## Files in this evidence set

- `stageA/stdout.log` — full runtime stdout for the Stage A run
- `stageA/run_log.md` — runtime-produced run log
- `stageA/implementation_report.md` — runtime-produced implementation report
- `stageA/workflow_summary.json` — machine-readable run summary
- `stageA/repository_sensemaking_brief.md` — the model-produced brief that failed validation
- `stageA/tool-call-trace.jsonl` — full tool-call trace for the repo-sensemaker invocation
- `stageA/run-ledger.jsonl` — session run ledger
- `stageA/validator_output.json` — full structured validator error output (10 errors)

## Scope

This evidence concerns `H:\GithubRepositories\auteur` only, on one run, at one HEAD.
No claim is made about other repositories or about the workflow's general reliability.
