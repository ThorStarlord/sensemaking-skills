# Experiment 0009 — External-Repository Validation: auteur (Stage A only)

**Status: CAMPAIGN STOPPED AT STAGE A. Stage A did not pass. The evidence-quality
audit and Stage B (positive/negative Step-2 proofs) were NOT run**, per the
campaign's explicit stop condition ("STOP THE CAMPAIGN if Stage A does not pass —
do not proceed to the evidence audit or Stage B").

This experiment tests transfer of the already-proven
`architectural-review-planning-workflow` to **one** external repository
(`H:\GithubRepositories\auteur`, HEAD `b40db65`). It does not prove product-wide
generality or production readiness, per ADR 0021's external-repo disclaimer.
Nothing here should be read as "the workflow doesn't work" — it demonstrates a
scoping bug in one validator on a specific two-repo topology, described below.

## Research question

Does the already-proven `architectural-review-planning-workflow` produce a valid,
evidence-grounded, useful architectural recommendation when applied unchanged to
an independent repository (auteur)?

**Answer for this experiment: inconclusive on the recommendation itself.** The
live model produced a brief that (on manual inspection) cites real files at real
paths in auteur with content that appears to genuinely support its claims — but
the repo's own brief validator rejected it on the first (only) attempt due to a
validator bug unrelated to the model's actual output quality (see "Root cause"
below). Per the campaign's explicit rule ("Do not manually repair the brief to
force a pass"), the run was not repaired and the campaign stopped here.

## Environment

- **Framework clone** (disposable, standalone, not a worktree):
  `H:\scratch\sensemaking-external-exp-framework`
  - HEAD: `72ac3cf18abec779f5209d35d063f9f0456e12f6` (matches required baseline:
    includes PR #57, #59, #60, #62, #64, #65, #66)
  - Confirmed via `git worktree list` run from inside the clone itself: only
    itself is listed — not a linked worktree of the primary repo.
  - `git status --short` clean at start and clean at end except for the
    session's own authorized writes (see "Framework integrity" below).
- **Target clone** (disposable, standalone, read-only in practice):
  `H:\scratch\auteur-target-readonly`
  - HEAD: `b40db654e0df9e90074f7ad85b40d7362378e07d` (matches required target HEAD)
  - `git status --short` clean before and after Stage A.

### Pre-existing condition noted (not caused by this experiment)

The **original** `H:\GithubRepositories\auteur` working tree had an uncommitted
modification (`M src/auteur/structure/revision_service.py`) present *before* any
clone was made. This is irrelevant to the clone's integrity: `git clone` only
copies committed history, so `H:\scratch\auteur-target-readonly` came up clean
at HEAD `b40db65` regardless. `H:\GithubRepositories\auteur` itself was never
written to by this experiment. Flagged here for transparency only.

The original auteur repo also has a large amount of **pre-existing, tracked,
`.gitignore`d-going-forward** `artifacts/` content (`01-orchestration-run`
through `08-orchestration-run`, `full-local-sensemaking/`, PRD/issue-list files,
etc.) — these were committed to auteur's history before its `.gitignore` rule for
`/artifacts/` was added, from unrelated prior work on that repo. They are not
part of this experiment and were not touched by it (see tool-call-trace
analysis below).

## Stage A — external live Step 1

### Command run

```
python scripts/workflow-runtime.py "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --gate-decision auto-approve \
  --target-repo H:/scratch/auteur-target-readonly \
  --repo-root H:/scratch/sensemaking-external-exp-framework \
  --log-dir H:/scratch/logs-stageA
```

- Launched PID: **10626** (bash wrapper PID 10625, verified as the correct
  child process via `ps -ef`, polled directly by PID — not by name pattern)
- Session ID: `orchestration-20260726-001654-da9b4d83`
- Started: 2026-07-26 00:16:54, ended: 2026-07-26 00:21:51 (~5 minutes; well
  under the 15-minute bound)
- Exit: process ended naturally (not killed) — see `stage-a/watcher-poll-log.log`
  for the poll trail (sentinel + target-dirty checks every ~30-40s, all clean).
- `allowed_tools` for the live executor confirmed as `["Read", "Write", "Glob",
  "Grep"]` in `scripts/skill_executor.py` (line 883 at framework HEAD `72ac3cf`)
  before the run — Bash and PowerShell were NOT available to the model.
  Confirmed in the tool-call trace: one `PreToolUse` event for `PowerShell` is
  observed at 00:17:32 with **no matching `PostToolUse`** — consistent with the
  call being blocked/denied, not executed.

### Result

Step 1 (`repo-sensemaker`) executed once, produced
`repository_sensemaking_brief.md` at
`H:\scratch\sensemaking-external-exp-framework\artifacts\05-orchestration-run\repository_sensemaking_brief.md`
(the correct, runtime-authorized **framework** session path — see
`stage-a/tool-call-trace.jsonl`, `PostToolUse Write ... completed` at
00:21:30 targeting that exact path).

`validate-and-report.py` (which runs `validate-brief.py`) ran once against this
artifact and **FAILED** on the first (and only) attempt:

```
HALLUCINATED_FILE: Excerpt[0] references non-existent file: src/auteur/structure/diagnostics.py
HALLUCINATED_FILE: Excerpt[1] references non-existent file: src/auteur/structure/analyzer.py
HALLUCINATED_FILE: Excerpt[2] references non-existent file: src/auteur/structure/state.py
HALLUCINATED_FILE: Excerpt[3] references non-existent file: src/auteur/structure/cartographer_audit.py
```

Full validator output: `stage-a/validation_run_log.md`. Full run log:
`stage-a/run_log.md`. Full stdout: `stage-a/stdout.log`.

### Root cause (spot-checked manually, not fixed)

All four cited files **do exist** in the auteur clone at exactly those paths:

```
$ find /h/scratch/auteur-target-readonly/src/auteur/structure -maxdepth 1
.../src/auteur/structure/analyzer.py
.../src/auteur/structure/cartographer_audit.py
.../src/auteur/structure/diagnostics.py
.../src/auteur/structure/state.py
```

`scripts/validate-brief.py` (function `validate_brief`, ~line 305) checks
citation existence with:

```python
full_path = os.path.join(repo_root, file_path)
if not os.path.exists(full_path): ...HALLUCINATED_FILE...
```

`repo_root` here is injected by `scripts/_validator_utils.py`'s
`run_subprocess`/`inject_repo_root` machinery, which passes the orchestrator's
`--repo-root` (the **framework** clone,
`H:\scratch\sensemaking-external-exp-framework`) — not `--target-repo` (the
**auteur** clone, where the cited source files actually live). So the validator
checked `H:\scratch\sensemaking-external-exp-framework\src\auteur\structure\...`,
which naturally does not exist, and flagged four real, correctly-cited files as
hallucinated.

**This is a concrete runtime blocker, reported only, not fixed**, per the task's
hard constraint. It is specific to the `--target-repo` != `--repo-root`
topology, which internal (single-repo) proofs never exercise — this appears to
be the first time this code path has run against a genuinely external repo.

### Stage A classification: **BRIEF VALIDATION FAILED**

Justification against the 10 Stage-A success criteria:

1. repo-sensemaker invoked exactly once — **held** (trace shows one
   `SkillInvocation` event).
2. Brief produced at the runtime-authorized framework session path — **held**.
3. Real brief validator passes on the first artifact, no repair — **NOT held**
   (failed with 4 errors; per campaign rules the artifact was not repaired).
4. No manual repair occurred — **held** (none performed).
5. Canonical workflow IDs / weakness types used correctly — appears **held**
   on inspection (`Weakness Type: Zero Validation` matches
   `weakness-types.md` vocabulary; workflow ID matches the registry entry
   used to launch the run).
6. Evidence citations refer to real files that exist in auteur — **held**
   (verified manually; the validator's rejection was a false positive, see
   root cause above).
7. Cited files/line ranges actually support the claims — **partially spot
   checked**, see "informal spot check" below; a full evidence audit was not
   run since Stage A did not pass.
8. Target repository stays unchanged — **held** (`git status --short` empty
   before and after; see below re: one blocked write attempt).
9. Framework clone stays intact — **held** (only `docs/mode-coverage.yaml`
   and the new `artifacts/05-orchestration-run/` session dir changed; see
   `stage-a/framework-post-run-diff-stat.txt` and
   `stage-a/framework-post-run-git-status.txt`).
10. Brief identifies a concrete, auteur-specific weakest boundary, not generic
    advice — appears **held** on inspection (see brief excerpt below).

Because criterion 3 failed, Stage A as a whole is **BRIEF VALIDATION FAILED**,
independent of how criteria 5–10 look.

### One near-miss worth recording: a blocked write attempt into the target clone

The tool-call trace (`stage-a/tool-call-trace.jsonl`) shows a `PreToolUse`
event at 00:19:53 for `Write` targeting
`H:\scratch\auteur-target-readonly\artifacts\05-orchestration-run\repository_sensemaking_brief.md`
(inside the **target**, not the framework session path) — but **no matching
`PostToolUse` completion event** follows it. The model's very next actions
(00:20:33 onward) correctly `Read`/`Edit`/`Write` the framework session path
instead, and that `Write` *does* have a matching `PostToolUse ... completed`.

Manually confirmed no file was actually created: the only file under
`auteur-target-readonly/artifacts/05-orchestration-run/` is
`00-user-intent.md`, which is **pre-existing tracked content already in
auteur's git history at HEAD b40db65** (`git log --oneline -- <path>` shows
commit `15699ea`, unrelated to this experiment), not something this run wrote.
`git status --short` on the target clone was empty both before and after the
run. This is recorded as a near-miss / confinement-working observation, not a
target mutation — abort criteria were not triggered because the target never
actually became dirty.

## Brief excerpt (for context, not an evidence audit)

The brief identifies a specific weakest boundary: auteur's `DiagnosticLayer`
enum (`src/auteur/structure/diagnostics.py`) declares 9 validation layers, but
`run_all_diagnostics()` in `analyzer.py` only implements Layers 1–7; Layer 8
(Modulation) has zero validators, and Layer 9 (Theme/Resonance) is only
reachable through a parameter (`cartographer_outline`) that the primary
`state_check()` CLI path (`state.py`) never supplies. This is specific to
auteur's actual code, not generic advice, and the cited files/line areas do
exist. **This has not been through the full evidence-quality audit the
campaign specifies** (that step is skipped because Stage A did not pass) —
treat it as a plausible-looking but unaudited claim, not a verified finding.

## Evidence audit table

**Not produced.** Per the campaign definition, the evidence-quality audit only
runs "if Stage A passed." Stage A did not pass, so this step was skipped.

## Stage B (positive and negative)

**Not run.** Per the campaign definition, Stage B only runs "if Stage A AND the
evidence audit both pass." Neither condition was met.

## Framework and target integrity — final state

- Framework clone (`H:\scratch\sensemaking-external-exp-framework`):
  `git status --short` after the run shows only `M docs/mode-coverage.yaml`
  (expected — mode-coverage bookkeeping) and the new
  `artifacts/05-orchestration-run/` session directory (expected — the run's own
  output). No other tracked file changed. `git worktree list` (run from inside
  this clone) still shows only itself.
- Target clone (`H:\scratch\auteur-target-readonly`): `git status --short`
  empty before and after. `H:\GithubRepositories\auteur` (the real repo) was
  never touched by this experiment (only cloned from, read-only).

## What is now known — narrowly, about auteur specifically

1. On this one run, against this one external repository, at framework
   commit `72ac3cf`, the `architectural-review-planning-workflow`'s Step 1
   (`repo-sensemaker`) executed via the live `claude-code` executor and
   produced a brief whose factual citations (four source files under
   `src/auteur/structure/`) are real and exist in auteur at the cited paths.
2. The repo's own brief validator (`validate-brief.py`) incorrectly rejected
   those citations as hallucinated, because of a `repo_root`/`target_repo`
   scoping bug in how file-existence checks are wired for cross-repo runs
   (`--target-repo` != `--repo-root`) — a topology internal single-repo proofs
   never exercise.
3. No conclusion can be drawn about whether the *recommendation* stage
   (Step 2 / architectural-review) would work against auteur, and no
   conclusion can be drawn about the brief's overall evidence quality beyond
   the narrow, manual, non-exhaustive spot check above — the formal
   evidence-quality audit was not performed because the campaign correctly
   stopped at the Stage A failure per its own rules.
4. This says nothing about the workflow's behavior on any other external
   repository, or about product-wide readiness.

## Concrete runtime blocker surfaced (reported only, not fixed)

`scripts/validate-brief.py`'s citation-existence check
(`os.path.join(repo_root, file_path)` around line 305) resolves cited paths
against `repo_root`, but when the orchestrator is invoked with `--target-repo`
different from `--repo-root` (the only way to run this workflow against an
external repository), the artifact's citations describe files in the *target*
repo, not the framework repo. The validator has no visibility into
`target_repo` at all (`validate_brief(artifact_path, repo_root=".")` — no
`target_repo` parameter exists). This causes every genuinely-correct citation
of a target-repo source file to be misclassified as `HALLUCINATED_FILE` in any
cross-repo run. Per the task's hard constraint, this is reported, not fixed.

## Recommended next step

Fix `validate-brief.py`'s (and any sibling validator's) file-existence check to
resolve citations against the artifact's actual target repository, not
unconditionally against `repo_root` — most likely by threading a `target_repo`
argument through `_validator_utils.py`'s subprocess injection and
`validate_brief()`'s signature, defaulting to `repo_root` when they're equal
(the single-repo case, which must keep working exactly as before). Once that
fix lands, re-run this exact Stage A command against the same auteur clone
(fresh clone recommended, since the framework clone used here now has session
artifacts in it) to get an unblocked read on brief quality, then proceed to the
evidence audit and Stage B if Stage A passes.
