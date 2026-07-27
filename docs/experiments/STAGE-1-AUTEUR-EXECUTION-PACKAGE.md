# Stage 1 Auteur Execution Package

**Date**: 2026-07-26 (revised same day: model-enforcement implementation
merged via PR #87; package updated to reflect the merged code and rebased
onto the new framework baseline)
**Nature of this document**: planning and documentation only. It resolves and
records the exact configuration a Stage 1 controlled `auteur` rerun *would*
use. **No experiment was run to produce this document. No auteur rerun
occurred. No code, test, validator, prompt, contract, or runtime file was
changed by this document. No historical evidence was modified.**

```text
Stage 1 execution authorization status = NOT AUTHORIZED

Former blocking prerequisite:
explicit model selection and executor enforcement = RESOLVED by PR #87

Owner model decision:
Provider = Anthropic via Claude Agent SDK
Model identifier = claude-sonnet-5
Historical model identity = unknown and unrecoverable
Purpose = reproducible new controlled-experiment baseline
```

The technical blocker (no code-level way to pin and enforce an explicit
model) is now resolved: PR #87 ("fix: enforce explicit model for controlled
experiments", merged, issue #86) added `--model` and
`--controlled-experiment` to `scripts/workflow-runtime.py`, threaded an
explicit `model=` value through `create_executor(...)` into
`ClaudeAgentOptions(model=...)` in `scripts/skill_executor.py`, and added
hard-stop enforcement (requested-vs-reported mismatch, multiple distinct
reported models, missing model in controlled-experiment mode) with no
fallback and no retry. §3/§3a below describe the merged behavior in detail.

**This resolves the technical blocker only. It does not authorize Stage 1
execution.** Execution authorization is a separate owner decision, recorded
(still blank) in §13. Merging PR #85 would approve this documentation package
as accurate and complete — it would not itself authorize running Stage 1.

## 1. Governance boundary

- Baseline: `main@68b44835be43b86ee7c0d7eb968e67efcd368443` (verified: this is
  the exact `origin/main` HEAD used to update this package; it is a fixed,
  pinned commit, not a moving branch reference). This SHA contains:
  - PR #81 (brief-contract redesign — `weakness_type` structured field);
  - PR #84 (governance ratification — D7/D8/E4 staged-validation record);
  - PR #87 (explicit model-selection and executor enforcement — issue #86).
- The previously pinned framework SHA
  `ac5de55c700cd1b15f2eea1ca2726e83cd8d3284` (PR #84's merge commit) is
  **superseded** by `68b44835be43b86ee7c0d7eb968e67efcd368443` throughout this
  document. `ac5de55` remains an ancestor of the new pin; nothing about the
  PR #81/#84 content it recorded has changed, it has simply been carried
  forward to include PR #87.
- PR #84: merged, `main`, docs-only (`docs/PHASE-80-81-CLOSURE.md`,
  `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`,
  `docs/adr/0021-production-readiness-requirements.md`).
- PR #87: merged, `main`, code (`scripts/workflow-runtime.py`,
  `scripts/skill_executor.py`, `tests/test_model_enforcement.py`) — adds
  explicit `--model` / `--controlled-experiment` enforcement. See §3/§3a.
- Issue #83 ("Run controlled auteur validation after brief-contract
  redesign"): **OPEN, planning-only**. Its own text states: "Creating this
  issue does not itself execute the experiment. A separate, explicit owner
  instruction is required to run Stage 1."
- D7 = Externally validated (ratified). D8 = success on at least two
  structurally different external repositories, including clean structural
  validation, substantive audit, no target mutation, pinned revisions,
  repeatability, and human usefulness review on at least one target
  (ratified).
- E4 = staged plan (ratified): Stage 1 = controlled auteur rerun; Stage 2 =
  second structurally different repository (conditional, unauthorized);
  Stage 3 = real-maintainer usefulness evaluation (conditional,
  unauthorized).
- **Stage 1 planning is authorized. Stage 1 execution is NOT authorized** and
  requires a separate, explicit owner instruction after reviewing this
  package.
- ADR 0021 remains **Proposed** (three other named owner-decision items —
  cost/concurrency policy, supported-agent commitments, platform scope —
  remain outstanding regardless of D7/D8 ratification).
- Current achieved readiness remains **"Externally exercised"** (Level C).
  Ratifying D7/D8/E4 does not itself advance this level.

**This document authorizes nothing.** It is input to the owner's decision.

### Governance discrepancy found and disclosed

Part 2 of this package instructs pinning the auteur revision to "the same
pinned target revision used in the final historical campaign." That
historical evidence is recorded in **PR #78** ("Evidence 0012: final
authorized auteur rerun — Stage A BRIEF VALIDATION FAILED"). Verification via
`gh pr view 78` shows **PR #78 is OPEN, unmerged** (`mergedAt: null`,
`baseRefName: main`, `headRefName: evidence/auteur-campaign-final-rerun`).
The evidence directory
`experiments/evidence/0012-external-repo-auteur-final-rerun/` does **not**
exist on `main` — it exists only on the unmerged branch
`origin/evidence/auteur-campaign-final-rerun` (commit `a328c80`, verified
`git merge-base --is-ancestor a328c80 origin/main` → not an ancestor).

This does not contradict anything in the confirmed governance baseline (PR
#84 merged, issue #83 open/planning-only, and ADR 0021 status are all
independently confirmed correct above) — it is a separate fact surfaced by
Part 2's own research requirement. It is recorded here rather than silently
treated as settled, because `docs/PHASE-80-81-CLOSURE.md` and
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md` both refer to "Historical PR
#67/#70/#73/#78 evidence artifacts" in language that could be read as
implying that evidence is merged and permanent on `main`. It is not, today.
The evidence content itself (read via `git show` against the remote branch,
read-only, no merge, no checkout of that branch's working tree) is internally
consistent and detailed enough to use as the historical comparison source,
and is the only historical campaign evidence located for the final rerun —
but the owner should know its container PR is unmerged before treating it as
a permanent record.

**Historical evidence permanence rules (this revision, explicit)**:

- PR #78 remains **open and unmerged**. This document does not merge it,
  does not modify its artifacts, and does not authorize doing so.
- The historical comparison source is pinned to the **exact evidence commit
  `a328c80`** (`origin/evidence/auteur-campaign-final-rerun`) and PR #78 —
  not to the branch name, not to "whatever PR #78 currently contains."
- Stage 1 must not depend on a moving branch ref. Any execution plan must
  re-verify `a328c80` by exact SHA (`git show a328c80:...` /
  `git merge-base --is-ancestor a328c80 origin/evidence/auteur-campaign-final-rerun`),
  not by re-reading the branch tip.
- Before Stage 1 execution, the exact evidence commit `a328c80` must still
  be retrievable (the remote ref must still exist and still resolve to a
  commit containing it). This is a **preflight check**, to be added to §6's
  step 2/4 verification alongside the framework/target SHA checks.
- Disappearance or mutation of that reference (branch deleted, force-pushed,
  rebased such that `a328c80` is no longer reachable, or PR #78 closed in a
  way that removes the branch) is a **preflight hard stop** — add this
  condition to §11's hard stop matrix.

## 2. Pinned revisions

### Framework revision

```text
Framework repository: ThorStarlord/sensemaking-skills
Framework SHA: 68b44835be43b86ee7c0d7eb968e67efcd368443
Why this SHA: exact origin/main HEAD at the time this package was updated,
  and the current owner-supplied authoritative baseline. Confirmed via
  `git rev-parse origin/main` and `git merge-base --is-ancestor
  68b44835be43b86ee7c0d7eb968e67efcd368443 origin/main`. A fixed commit, not
  a moving branch reference, is recorded here deliberately.
Contains PR #81 contract redesign: yes (ancestor of 68b4483)
Contains PR #84 governance record: yes (ancestor of 68b4483)
Contains PR #87 explicit model-selection enforcement: yes (ancestor of
  68b4483; adds --model / --controlled-experiment, ClaudeAgentOptions(model=),
  requested/reported-model evidence, and hard-stop-on-mismatch behavior --
  see §3/§3a)
```

### Auteur (target) revision

```text
Target repository: auteur (local path referenced in historical evidence as
  H:\GithubRepositories\auteur; no GitHub remote was queried or contacted as
  part of preparing this package — no clone or network access to the target
  was performed)
Target SHA: b40db654e0df9e90074f7ad85b40d7362378e07d
Historical comparison source: PR #78 / evidence directory
  experiments/evidence/0012-external-repo-auteur-final-rerun/EVIDENCE.md,
  read via `git show origin/evidence/auteur-campaign-final-rerun:...`
  (read-only; that branch is NOT merged to main — see the governance
  discrepancy note in §1).
Why this SHA: this is the exact commit pinned in the final, most recent
  historical campaign rerun (PR #78), the same commit that previously
  produced the PR #73 "ghost feature" false-positive finding — using the same
  pinned commit again keeps this a controlled before/after comparison of the
  PR #81 contract redesign against a known, previously-exercised target
  state, rather than introducing a second uncontrolled variable (a different
  target commit).
Moving branch avoided: yes — an exact SHA, not a branch name, is recorded.
```

No clone of, or write to, the target repository was performed to prepare this
package. The SHA above was obtained entirely from the historical evidence
record (git show against a read-only remote ref) and is not independently
re-verified against a live target clone.

## 3. Model/provider configuration

**Revision note**: the sub-sections below originally described a
pre-enforcement gap (no way to pin a model in code, only an "observe and
record the ambient default" workaround). PR #87 (merged) closed that gap.
This section now describes the merged behavior directly; §3a records the
implementation detail and verification trail that led to it.

```text
Provider: Anthropic, via the Claude Agent SDK (claude_agent_sdk.query()),
  not the raw Anthropic Python SDK client. Confirmed at
  scripts/skill_executor.py — the executor path used (`--executor
  claude-code`) constructs ClaudeAgentOptions and calls `query()`.
Model: explicitly pinned via CLI flag, enforced in code. Requested model
  string:

    Requested model: claude-sonnet-5

  Enforcement path (merged, PR #87):
    scripts/workflow-runtime.py --model claude-sonnet-5
      --> OrchestrationRunner
      --> create_executor(..., model=<value>)
      --> ClaudeAgentSdkSkillExecutor
      --> ClaudeAgentOptions(model=<value>)

  Controlled-mode requirement: --controlled-experiment requires --model to
  be set; scripts/workflow-runtime.py hard-fails before any SDK/model call
  is made if --controlled-experiment is passed without --model (see
  workflow-runtime.py around line 228 and the CLI-arg guard around line
  3005).
Model version or immutable identifier: `claude-sonnet-5` is the owner-
  approved identifier for this experiment's controlled baseline (see §3a
  Part 2 for why a new baseline, not a historical match, is being
  established).
Temperature: not set anywhere in scripts/skill_executor.py's
  ClaudeAgentOptions construction; SDK default applies. Unaffected by PR #87.
Max tokens: not set in the claude-code executor path; SDK default applies.
  Unaffected by PR #87.
Reasoning mode: not configured/exposed by this executor path.
Tool permissions: allowed_tools=["Read", "Write", "Glob", "Grep"] only.
  Bash/PowerShell/Agent (subagent spawn) are NOT in allowed_tools; the
  historical evidence (PR #78) confirms PowerShell and Agent invocation
  attempts were denied (PreToolUse only, no PostToolUse completion).
  Unaffected by PR #87 (regression-tested in tests/test_model_enforcement.py).
Filesystem permissions: PreToolUse hook `artifact_permission_gate` +
  `pre_trace`; PostToolUse hook `post_trace`. Historical evidence shows this
  gate denied both target-directed Write attempts in the PR #78 rerun.
Network permissions: none granted by allowed_tools; no network-capable tool
  is in the allowed set.
Fallback model: NONE. `fallback_model` is never set by the merged code path;
  the plan explicitly prohibits introducing one for a controlled experiment.
Retry: NONE. A requested-vs-reported mismatch, a missing model, or multiple
  distinct reported models is a hard stop, not a retry.
```

Requirements restated and confirmed against the merged code:

- No model fallback exists in code — confirmed absent in the merged diff.
- No silent provider substitution — the executor path is single, fixed
  (`claude_agent_sdk.query()`), not switchable at runtime by the model.
- No automatic retry — confirmed absent in `scripts/skill_executor.py`.
- No automatic model escalation — confirmed absent.
- No second run after failure — enforced as a process rule in §11's hard-stop
  matrix; the exact command plan in §6 is a single invocation.

**Difference from the historical campaign**: the historical campaign (PR
#78) used the identical `--executor claude-code` path but with no explicit
model pin — its actual model is unknown and unrecoverable (see §3a Part 2).
This experiment therefore establishes a new, reproducible controlled-
experiment baseline on the model axis; it is not a historical model
equivalence claim.

## 3a. Model enforcement (implemented — PR #87, merged)

### Part 1 — confirmed installed SDK API

Verified against the actually-installed package in this environment (not
assumed): `pip show claude-agent-sdk` reports **version 0.2.82**, installed
at `.../site-packages/claude_agent_sdk`.

```text
ClaudeAgentOptions.model: str | None                    (types.py:1673-1677)
  Docstring: "Claude model to use. Defaults to the CLI default model.
  Examples: claude-sonnet-4-5, claude-opus-4-5."
  Confirmed plumbing: _internal/transport/subprocess_cli.py:271-272 --
    `if self._options.model: cmd.extend(["--model", self._options.model])`
  -- i.e. an explicit string is passed straight through as a CLI flag; no
  validation/allow-list of identifiers happens in the SDK itself.

ClaudeAgentOptions.fallback_model: str | None            (types.py:1679-1680)
  Plumbed to `--fallback-model` (subprocess_cli.py:274-275). This is a
  fallback mechanism and must NOT be set for a controlled experiment (task
  boundary explicitly prohibits introducing fallback behavior).

Actual resolved model exposure:
  AssistantMessage.model: str                            (types.py:1029)
    -- reported per assistant message; this is the only per-invocation
    "actual model used" field found.
  ResultMessage.model_usage: dict[str, Any] | None        (types.py:1159)
    -- a cost/usage breakdown, keyed by model name if multiple models were
    used; usable as a cross-check, not a single canonical "the model" field.
  ClaudeAgentOptions itself has no field reporting the resolved model (it is
  request-only).

Environment-variable / CLI-setting override risk:
  subprocess_cli.py's transport builds `process_env` by merging the calling
  process's full inherited environment (`inherited_env = {k: v for k, v in
  os.environ.items() if k != "CLAUDECODE"}`) with `self._options.env`
  (explicit `ClaudeAgentOptions.env` always wins over inherited/ambient
  values per that file's own comments). Whether an inherited ambient
  variable (e.g. an ANTHROPIC_MODEL-style variable, if the installed CLI
  recognizes one) could override an explicit `--model` flag at the
  underlying `claude` CLI's own argument-parsing layer was NOT verified in
  this task (that layer is the bundled `claude.exe`, opaque without running
  it, which this task does not authorize). This is exactly why hard
  mismatch-detection (comparing `AssistantMessage.model` against the
  requested value, not just trusting the flag was honored) is required
  rather than optional -- see the implementation plan below.

Temperature / max_tokens / reasoning-effort support:
  No `temperature` or `max_tokens` field exists on `ClaudeAgentOptions` for
  this CLI-subprocess executor path (confirmed by full-file inspection of
  the dataclass; the only sampling-adjacent controls found are
  `max_thinking_tokens: int | None` and `thinking: ThinkingConfig | None`,
  types.py:1851-1870, which govern extended-thinking token budget, not
  sampling temperature or output-length caps). Confirms the doc's original
  claim that these are "not set / SDK default applies" -- refined to "not
  exposed by this executor path at all for temperature/max_tokens", vs.
  thinking budget which IS exposed but is a different axis.
```

### Part 2 — owner-approved model (resolved, not a historical match)

```text
Provider: Anthropic, via the same claude_agent_sdk.query() /
  ClaudeAgentOptions path already used by --executor claude-code (no change
  of provider or executor path).
Owner-approved model identifier: claude-sonnet-5
Historical model known: NO. Read-only inspection of the historical
  evidence (`git show origin/evidence/auteur-campaign-final-rerun:
  experiments/evidence/0012-external-repo-auteur-final-rerun/EVIDENCE.md`)
  contains no recorded model identifier, alias, or version string anywhere
  in that document. Before PR #87, `scripts/skill_executor.py`'s
  claude-code path had never set `model=` in any commit reachable from the
  framework history, so no historical run -- including the one PR #78
  documents -- pinned or recorded which model actually executed it. This
  fact is permanent and unaffected by PR #87: PR #87 gives Stage 1 a way to
  pin and enforce a model going forward, it does not retroactively recover
  what model ran historically.
Historical comparability limitation: because the historical campaign's
  actual model is unrecoverable, Stage 1 CANNOT be a controlled
  before/after comparison on the model axis -- only on the framework-SHA
  (PR #81 contract redesign) axis, which was always the intended controlled
  variable per §2. `claude-sonnet-5` is therefore selected to establish a
  new, reproducible controlled-experiment baseline, not to reproduce
  historical model behavior. This is a permanent, disclosed limitation of
  Stage 1, not something the pin fixes; it only prevents the *additional*
  uncontrolled variable of "we don't even know what we're using this time."
```

### Part 3 — implemented enforcement (PR #87, merged)

Code changes were made and merged in
**https://github.com/ThorStarlord/sensemaking-skills/pull/87**
("fix: enforce explicit model for controlled experiments", closes issue #86).
This package does not itself authorize or perform further implementation,
merge, or execution of anything; it only reflects the already-merged state.

```text
Files touched (merged):
- scripts/workflow-runtime.py   -- added --model (optional str) and
    --controlled-experiment (store_true) CLI arguments (around line 2985);
    hard-fails with a clear error before any SDK/model call if
    --controlled-experiment is set without --model (around line 3005);
    plumbed through create_executor(..., model=self.model) (around line 243)
    and into the constructed executor's CLI invocation (--model /
    --controlled-experiment flags added to the subprocess command around
    line 1312-1314).
- scripts/skill_executor.py     -- ClaudeAgentSdkSkillExecutor accepts a
    model value and passes it into ClaudeAgentOptions(model=...); the
    message loop captures every distinct AssistantMessage.model value into
    reported_models (around line 1281-1344); requested_model,
    reported_models, and model_match are recorded as first-class evidence
    fields on the result (around line 871-894); a "model_mismatch" hard-stop
    error is raised (around line 1408-1418) when model_match is False;
    fallback_model is never set; no retry path exists.
- tests/test_model_enforcement.py (new) -- covers the enforcement paths in
    Part 4 below.
```

### Part 4 — test plan (implemented, in tests/test_model_enforcement.py)

1. Explicit `--model` value reaches `ClaudeAgentOptions(model=...)`.
2. `--controlled-experiment` with no `--model` fails before any
   `query()`/SDK call is made (asserts the call never happens, not just a
   nonzero exit).
3. Requested model value is recorded in trace/run-log output
   (`requested_model`).
4. Actual model(s) (`AssistantMessage.model`) are recorded in trace/run-log
   output as `reported_models` whenever the SDK returns at least one
   `AssistantMessage`.
5. A mocked requested-vs-actual mismatch produces a FAILED result in the
   `model_mismatch` category, not a retry (`model_match: False`).
6. No fallback: `fallback_model` is never set by this code path in any test
   case.
7. No retry: `query()`/the transport is invoked at most once per
   `invoke_skill` call, mismatch or not.
8. `allowed_tools=["Read", "Write", "Glob", "Grep"]` and the
   `artifact_permission_gate`/`pre_trace`/`post_trace` hooks are unchanged
   by this diff (regression-diffed against all `ClaudeAgentOptions` fields
   other than `model`).
9. Target-write confinement (`build_artifact_permission_gate`,
   `is_within_root`) and its existing tests are unaffected.
10. Normal (non-`--controlled-experiment`, no `--model`) invocations keep
    working exactly as before -- this change is additive only.

## 4. Execution environment

```text
Operating system: Windows 10 Home Single Language 10.0.19045 (per this
  session's environment; historical PR #78 evidence also ran on Windows,
  paths shown as H:\scratch\...).
Shell: PowerShell (primary in this environment); the historical evidence's
  exact command was invoked via a bash-style job control layer (shell PID
  17626 / OS PID 19848 per EVIDENCE.md) — record both possibilities, fixed
  choice to be made by whoever executes Stage 1.
Python version: 3.14.3 (verified via `python --version` in this worktree at
  package-preparation time). NOT verified against the historical campaign's
  Python version — EVIDENCE.md does not record it. This is a fixed-value gap:
  the owner/executor should pin and record the exact Python version actually
  used at execution time, since it was not captured historically either.
Node version, if relevant: v24.14.1 (verified this session); not used by the
  Stage A command path (`workflow-runtime.py` is pure Python) — recorded for
  completeness only, likely not relevant to Stage 1.
Git version: 2.51.0.windows.1 (verified this session).
CLI/tool versions: Claude Agent SDK version not pinned anywhere in this
  repository's dependency manifests as verified during this task (out of
  scope to install/inspect further under the "no execution" boundary);
  record exact installed `claude_agent_sdk` package version at execution
  time.
Locale: unknown until execution; not recorded in historical evidence.
Timezone: historical evidence used UTC timestamps (controller clock) and a
  separate "framework clock" session id; record both clocks' timezone
  explicitly at execution time.
Environment variables required: none identified as required by
  scripts/skill_executor.py's claude-code path beyond whatever the Claude
  Agent SDK itself requires for authentication (e.g., an API key or logged-in
  CLI session) — exact variable names are SDK-internal and not enumerated in
  this repository; do not expose secret values in the execution record.
Secrets required: an authenticated Claude Agent SDK / Claude Code session
  (credential mechanism unspecified in this repo's code — inherited from
  the ambient CLI installation). No secret value is recorded in this package.
Working-directory layout: see §5.
```

Fixed vs. inherited vs. unknown, summarized:

- **Fixed by this package**: framework SHA, target SHA, tool-permission set,
  workspace layout (§5), command sequence (§6), requested model
  (`claude-sonnet-5`, explicitly passed via `--model` and enforced — see §3).
- **Inherited from the runner/executor environment at execution time**:
  Python/Node/git patch versions beyond what's recorded above, locale,
  timezone, Claude Agent SDK package version, authentication mechanism.
- **Unknown until execution**: exact Claude Agent SDK version; exact
  wall-clock start time. (The model itself is no longer an ambient unknown —
  it is explicitly requested and enforced; only the reported/confirmed value
  from the run is captured at execution time as evidence, per §3a.)

## 5. Disposable workspace layout

Following the historical campaign's own pattern (`H:\scratch\auteur-campaign-final\`,
outside both the primary checkout and `.claude/worktrees/`), a fresh,
standalone, disposable set of clones is proposed for Stage 1:

```text
H:\scratch\stage1-auteur-rerun\
  framework\        <- fresh clone of ThorStarlord/sensemaking-skills,
                       checked out to 68b44835be43b86ee7c0d7eb968e67efcd368443
  target-auteur\    <- fresh clone of the auteur target repository,
                       checked out to b40db654e0df9e90074f7ad85b40d7362378e07d
                       (treated as strictly read-only)
  outputs\          <- Stage A logs, brief, run artifacts land under
                       framework\artifacts\... per the runtime's own
                       resolution; outputs\ mirrors/collects copies for
                       review, nothing is written under target-auteur\
  logs\             <- stdout/stderr/run logs, mirroring stageA-logs/ from
                       the historical evidence
  evidence\         <- this run's EVIDENCE.md, manifests, trace copies,
                       duplicate-key check output, mutation-check output
```

Requirements confirmed satisfied by this layout:

- No `.claude/worktrees/` involved.
- No reuse of historical experiment directories (a new `stage1-auteur-rerun`
  root, not `auteur-campaign-final`).
- No output written inside the target repository (`target-auteur\` receives
  no writes; the runtime's `--target-repo` flag points there but
  `--repo-root`/`--log-dir` point into `framework\` / `logs\`).
- No historical evidence overwritten (nothing under
  `experiments/evidence/` in the primary repo is touched).
- Framework and target working trees must be verified clean before
  execution (see §6, §8).
- Target repository treated as read-only throughout.
- All generated output placed outside the target repository.

## 6. Exact command plan

Numbered per the required stages. Steps 1-4 and 6-10 may be run to verify the
plan (they do not invoke the model or generate experiment evidence). Step 5
is gated by the execution boundary and must NOT be run without separate,
explicit owner authorization.

```text
# 1. Clone / checkout commands
git clone https://github.com/ThorStarlord/sensemaking-skills.git H:\scratch\stage1-auteur-rerun\framework
cd H:\scratch\stage1-auteur-rerun\framework
git checkout 68b44835be43b86ee7c0d7eb968e67efcd368443

git clone <auteur-repo-source> H:\scratch\stage1-auteur-rerun\target-auteur
cd H:\scratch\stage1-auteur-rerun\target-auteur
git checkout b40db654e0df9e90074f7ad85b40d7362378e07d

# 2. SHA verification
cd H:\scratch\stage1-auteur-rerun\framework
git rev-parse HEAD
# expect: 68b44835be43b86ee7c0d7eb968e67efcd368443

cd H:\scratch\stage1-auteur-rerun\target-auteur
git rev-parse HEAD
# expect: b40db654e0df9e90074f7ad85b40d7362378e07d

# 2a. Historical evidence commit availability check (see §1's governance
#     discrepancy note and §11's hard-stop matrix; verifies the exact commit,
#     not merely that the branch name still exists)
git ls-remote https://github.com/ThorStarlord/sensemaking-skills.git origin/evidence/auteur-campaign-final-rerun
git fetch https://github.com/ThorStarlord/sensemaking-skills.git evidence/auteur-campaign-final-rerun
git show a328c80:experiments/evidence/0012-external-repo-auteur-final-rerun/EVIDENCE.md > NUL
git merge-base --is-ancestor a328c80 FETCH_HEAD
# expect: exit 0 for both the `git show` and the ancestor check; a328c80 must
# resolve and must still be reachable from the evidence branch tip. Failure
# here is a preflight hard stop (see §11) -- stop before proceeding to step 3.

# 3. Dependency setup
cd H:\scratch\stage1-auteur-rerun\framework
python -m pip install -r requirements.txt   # if present; record exact versions installed

# 4. Preflight validation (framework repo only, no target touched)
python scripts\validate-repo.py
python scripts\test-validators.py
git status --short                          # expect: clean
cd H:\scratch\stage1-auteur-rerun\target-auteur
git status --short                          # expect: clean
git diff --exit-code
git diff --cached --exit-code

# ============================================================
# EXECUTION BOUNDARY — DO NOT RUN WITHOUT SEPARATE OWNER AUTHORIZATION
# ============================================================

# 5. Experiment invocation (INVOKES THE MODEL -- gated)
python scripts\workflow-runtime.py \
  "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --controlled-experiment \
  --model claude-sonnet-5 \
  --gate-decision auto-approve \
  --repo-root "H:/scratch/stage1-auteur-rerun/framework" \
  --target-repo "H:/scratch/stage1-auteur-rerun/target-auteur" \
  --log-dir "H:/scratch/stage1-auteur-rerun/logs"

# NOTE: --repo-root and --target-repo above are pinned by preceding
# checkout to 68b44835be43b86ee7c0d7eb968e67efcd368443 (framework) and
# b40db654e0df9e90074f7ad85b40d7362378e07d (target); this command has no
# moving branch reference of its own.

# 6. Brief validation (this automatically runs the section-aware,
#    duplicate-key-safe weakness_type safeguard -- see Part 7 below)
python scripts\validate-and-report.py H:\scratch\stage1-auteur-rerun\framework\artifacts\...\repository_sensemaking_brief.md

# 7. (Optional, diagnostic-only) standalone safeguard re-check -- not
#    authoritative on its own; see Part 7 below for why.
python scripts\weakness_type_safeguard.py H:\scratch\stage1-auteur-rerun\framework\artifacts\...\repository_sensemaking_brief.md

# 8. Target-mutation check
cd H:\scratch\stage1-auteur-rerun\target-auteur
git status --porcelain
git diff --exit-code
git diff --cached --exit-code
git rev-parse HEAD
# compare HEAD before/after; expect identical to b40db654e0df9e90074f7ad85b40d7362378e07d

# 9. Evidence collection
#   copy brief, logs, trace, manifests into H:\scratch\stage1-auteur-rerun\evidence\

# 10. Final status reporting
#   summarize PASS/FAIL/INCONCLUSIVE per Part 9 below; return to owner
```

## 7. Duplicate-`weakness_type` safeguard

**Superseded (issue #93, merged into `scripts/validate-brief.py`).** Issue
#83 originally recorded this as a known, undetected residual gap
(`docs/PHASE-80-81-CLOSURE.md` §1a/§2): PyYAML's `safe_load` silently keeps
the last value on a duplicate mapping key. Issue #90 then found the
document-wide-regex script previously proposed here also grabbed the *wrong*
`yaml` fence when an earlier section (e.g. Section 8) had a malformed doubled
fence -- see Evidence 0013
(`experiments/evidence/0013-stage1-auteur-run-model-enforcement/`).

The corrected, section-aware, duplicate-key-safe implementation is
`scripts/weakness_type_safeguard.py` (PR #92), and the normal brief-validation
command (`scripts/validate-and-report.py` / `scripts/validate-brief.py`)
**automatically runs it as part of `validate_brief()`** (issue #93). Its
outcomes surface as their own stable error codes
(`DUPLICATE_WEAKNESS_TYPE_KEYS`, `MALFORMED_HANDOFF_FENCE`,
`MISSING_HANDOFF_SECTION`, `MISSING_HANDOFF_BLOCK`, `MISSING_WEAKNESS_TYPE`,
`HANDOFF_YAML_PARSE_ERROR`) in `validate-brief.py`'s standard error list. No
separate regex-based duplicate-key command (the `check_duplicate_weakness_type.py`
script formerly proposed in this section) is authoritative, and none should
be written or run for a Stage 1 rerun.

`python scripts/weakness_type_safeguard.py <brief-path>` remains available as
a manual diagnostic tool only -- **diagnostic only; not authoritative; the
validator this brief must pass is `scripts/validate-brief.py`** (invoked via
`scripts/validate-and-report.py`).

Requirements honored: duplicate key = hard stop (a blocking
`DUPLICATE_WEAKNESS_TYPE_KEYS` validation error, non-zero validator exit
code); the artifact is never auto-edited to repair it; no automatic rerun
follows a duplicate-key failure.

## 8. Target-mutation safeguard

Pre-run (inside `target-auteur\`):

```text
git rev-parse HEAD                    # record as target-HEAD-before
git status --porcelain                # expect: empty
git diff --exit-code                  # expect: exit 0, no output
git diff --cached --exit-code         # expect: exit 0, no output
git ls-files > ..\evidence\target-manifest-pre.txt
```

Post-run (inside `target-auteur\`):

```text
git rev-parse HEAD                    # record as target-HEAD-after
git status --porcelain                # must remain empty (or contain only
                                       #   a pre-planted, controller-added
                                       #   sentinel file, per the historical
                                       #   pattern -- never a model-written
                                       #   file)
git diff --exit-code
git diff --cached --exit-code
git ls-files > ..\evidence\target-manifest-post.txt
diff target-manifest-pre.txt target-manifest-post.txt   # expect: no diff
```

Record explicitly:

```text
Target HEAD before run: b40db654e0df9e90074f7ad85b40d7362378e07d (expected)
Target HEAD after run: <to be recorded at execution time; must equal above>
Untracked files before: <none, except any pre-planted sentinel>
Untracked files after: <must match "before" exactly>
Write attempt observed: <yes/no -- from the framework's PreToolUse trace>
Write attempt completed: <must be "no" for Stage 1 to remain valid>
```

A single completed target write, or any HEAD/tracked-file-manifest
divergence, is a hard stop regardless of brief quality.

## 9. Structural validation protocol

Required checks after generation, all against the fresh, framework-generated
brief:

- Artifact existence at the runtime-resolved session path.
- Parser success (brief parses as valid markdown + fenced YAML).
- `python scripts/validate-and-report.py <brief_path>` (or the equivalent
  unified validator entry point used historically,
  `validate-and-report.py` per PR #78's evidence).
- Blocking errors: none (`UNKNOWN_WEAKNESS_TYPE` was the PR #78 blocking
  failure — this contract-redesign rerun exists specifically to test whether
  PR #81's structured `weakness_type` field avoids that failure mode).
- Warnings: record every warning verbatim (e.g.
  `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`, `WEAKNESS_TYPE_PROSE_MISMATCH`,
  `EVIDENCE_QUOTE_WINDOW_MATCH`) — do not collapse into "pass."
- Quote-grounding failures: `EVIDENCE_QUOTE_NOT_FOUND` is blocking; must be
  absent.
- Window-match warnings: `EVIDENCE_QUOTE_WINDOW_MATCH` is non-blocking but
  must be recorded, not silently accepted as equivalent to an exact match.
- High-risk-claim warnings: `HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` must be
  present for any Safety Gaps / Ghost Features claim and must trigger §10
  review — it may not be silently dropped.
- Exactly one `weakness_type`: per §7's script, exit code 0.
- Recognized weakness type or `Other` with explanation: per
  `weakness-types.md`'s 7 registered terms plus `Other`.
- Complete trace: `tool-call-trace.jsonl`, schema_version 2, present and
  non-empty.
- Complete run log: `run_log_*.md`, `workflow_summary.json`,
  `validation_run_log.md` all present.

Structural result, one of:

```text
PASS          -- all of the above hold, zero blocking errors
FAIL          -- any blocking error, missing artifact, missing trace/log,
                 or duplicate weakness_type key
INCONCLUSIVE  -- process did not reach a determinate structural outcome
                 (e.g., crashed before validator ran, timed out, or
                 environmental contamination prevented a clean read)
```

## 10. Substantive-review rubric

Human reviewer form (to be filled in against the actual generated brief at
execution time — blank here):

```text
### Evidence grounding
- Does every cited quote exist? [ ]
- Does the cited range match the recorded quote? [ ]
- Does the quote support the claim? [ ]
- Is the surrounding context consistent with the claim? [ ]

### Contradiction search
- Was contradictory executable evidence actively searched? [ ]
- Were relevant entry points, tests, configuration, and runtime paths checked? [ ]
- Is contrary evidence missing or ignored? [ ]

### High-risk claims (one block per claim)
Claim: ___________________________________________
Substantive audit result:
- [ ] Confirmed
- [ ] Rejected
- [ ] Inconclusive
Reviewer rationale: ___________________________________________
Evidence checked: ___________________________________________
Contradictory evidence checked: ___________________________________________

(A Rejected or Inconclusive result on any high-risk claim means Stage 1 does
not pass, regardless of structural result.)

### Diagnosis quality
- Does the weakest-boundary diagnosis follow from the evidence? [ ]
- Is the finding scoped correctly? [ ]
- Is uncertainty stated honestly? [ ]
- Is the recommendation proportional? [ ]
- Is the proposed direction useful? [ ]

### Usefulness judgment
Useful enough to justify Stage 2:
- [ ] Yes
- [ ] No
- [ ] Inconclusive
Rationale: ___________________________________________
```

## 11. Hard stop matrix

| Condition | Detection method | Immediate action | Evidence preserved |
|---|---|---|---|
| Revision mismatch | `git rev-parse HEAD` on framework/target vs. §2 pinned SHAs | Stop before invocation | Record observed vs. expected SHA |
| Dirty initial working tree | `git status --porcelain` non-empty pre-run on either repo | Stop before invocation | Save `git status`/`git diff` output |
| Target mutation | §8 post-run checks diverge from pre-run | Stop; do not patch | Preserve manifests, HEAD before/after, trace |
| Completed target write | Trace shows `PreToolUse` + matching `PostToolUse` "completed" for a target-directed Write | Stop; do not patch | Preserve full trace JSONL |
| Duplicate `weakness_type` | §7 script exit code 1 | Stop; do not repair the artifact | Preserve brief as-is, script output |
| Blocking validator failure | Validator exit non-zero / blocking error code | Stop; do not repair-and-rerun | Preserve validator output, brief |
| Quote not found | `EVIDENCE_QUOTE_NOT_FOUND` in validator output | Stop | Preserve validator output |
| Missing trace | `tool-call-trace.jsonl` absent or empty | Stop | Preserve whatever partial logs exist |
| Missing run log | `run_log_*.md` / `workflow_summary.json` absent | Stop | Preserve whatever partial logs exist |
| Unsupported high-risk claim | §10 reviewer marks Rejected/Inconclusive on a high-risk claim | Stop; Stage 1 does not pass | Preserve brief + review form |
| Substantive review rejection | §10 reviewer overall rejects | Stop | Preserve brief + review form |
| Substantive review inconclusive | §10 reviewer marks Inconclusive overall | Stop; treat as non-pass | Preserve brief + review form |
| Environmental contamination | Unexpected process/tool errors, unrecorded environment drift | Stop; mark structural result INCONCLUSIVE | Preserve logs, environment snapshot |
| Automatic fallback or retry | Any retry/fallback logic observed in logs (none exists per §3/§3a; `fallback_model` never set) | Stop; treat as a process violation | Preserve logs |
| Output written into target repository | §8 manifest/status diff shows a new file under `target-auteur\` | Stop | Preserve manifests, diff |
| Missing `--model` | `--controlled-experiment` set without `--model`; `workflow-runtime.py` hard-fails before any SDK call (see §3a Part 3) | Stop before invocation | Preserve the CLI error output |
| Missing `--controlled-experiment` | The command in §6 omits `--controlled-experiment`; this is itself a plan deviation for Stage 1 | Stop before invocation | Preserve the command actually issued |
| Requested model not `claude-sonnet-5` | `requested_model` in the result/trace evidence differs from `claude-sonnet-5` | Stop before invocation, or stop and flag if discovered after | Preserve authorization block + `requested_model` evidence |
| No reported model | `reported_models` empty (no `AssistantMessage` observed) while a model was requested | Stop; do not retry | Preserve trace showing empty `reported_models` |
| Reported/requested mismatch | `model_match == false` in the recorded evidence | Stop; do not retry, do not fall back | Preserve trace showing `requested_model` vs. `reported_models` |
| Multiple reported models | `reported_models` (after de-duplication) contains more than one distinct value | Stop; treat as a hard mismatch | Preserve full `reported_models` list |
| Framework SHA mismatch | `git rev-parse HEAD` on `framework\` != `68b44835be43b86ee7c0d7eb968e67efcd368443` | Stop before invocation | Record observed vs. expected SHA |
| Target SHA mismatch | `git rev-parse HEAD` on `target-auteur\` != `b40db654e0df9e90074f7ad85b40d7362378e07d` | Stop before invocation | Record observed vs. expected SHA |
| Historical evidence commit `a328c80` unreachable or mutated | `git show a328c80:...` / ancestor check against `origin/evidence/auteur-campaign-final-rerun` fails at preflight | Stop before invocation | Preserve the failing verification output |

For every hard stop: stop immediately; preserve all evidence; do not patch;
do not edit the generated brief; do not rerun; return to the owner.

## 12. Success definition

Stage 1 succeeds only if **all** of the following hold:

1. Framework SHA exactly `68b44835be43b86ee7c0d7eb968e67efcd368443`.
2. Target SHA exactly `b40db654e0df9e90074f7ad85b40d7362378e07d`.
3. Requested model exactly `claude-sonnet-5` (`requested_model ==
   "claude-sonnet-5"`).
4. Reported model exactly matches (`reported_models == ["claude-sonnet-5"]`,
   `model_match == true`; repeated identical reported values may be
   de-duplicated, but no other value may appear).
5. No fallback (`fallback_model` never set; none observed in logs).
6. No retry (`query()`/the transport invoked at most once).
7. Structural Stage A validation passes (§9 = PASS).
8. No duplicate `weakness_type` key (§7 script exit 0).
9. Deterministic quote grounding (no `EVIDENCE_QUOTE_NOT_FOUND`).
10. No target mutation (§8 all checks clean).
11. Complete logs and trace present (`tool-call-trace.jsonl`, `run_log_*.md`,
    `workflow_summary.json`, `validation_run_log.md`).
12. Substantive review passes (§10 all sections satisfactory).
13. Every high-risk claim is Confirmed (none Rejected or Inconclusive).
14. Human reviewer judges the brief useful enough to justify considering
    Stage 2.

**Stage 1 success proves only** that the redesigned contract (PR #81) cleared
the historical `auteur` target under the pinned configuration and survived
the required review, using a reproducible, explicitly-pinned model baseline
(PR #87 enforcement).

**Stage 1 success does not satisfy D8 by itself.** It also does not prove:

- cross-repository generality;
- production readiness;
- autonomous trustworthiness;
- real-maintainer usefulness (beyond this one reviewer's judgment on this
  one target);
- Stage 2 authorization (Stage 2 remains conditional on separate, explicit
  owner review of Stage 1's actual evidence after it runs).

## 13. Owner authorization block

### Proposed configuration (reviewed values, not an approval)

```text
Stage 1 execution authorization status = NOT AUTHORIZED

Former blocking prerequisite: explicit model selection and executor
  enforcement = RESOLVED by PR #87 (§3a)

Proposed framework SHA: 68b44835be43b86ee7c0d7eb968e67efcd368443
Proposed target SHA: b40db654e0df9e90074f7ad85b40d7362378e07d
Proposed provider/model: Anthropic via Claude Agent SDK, claude-sonnet-5
Proposed environment: see §4 (fixed/inherited/unknown breakdown)
Proposed command: see §6, step 5 (below the execution boundary)
```

This "proposed configuration" block reflects the values reviewed and
recorded elsewhere in this package. It is not an authorization. Only the
block below, filled in and dated by the owner, authorizes execution.

### Owner authorization (blank — no approval pre-filled)

```text
Owner authorization:
- Decision: UNDECIDED
- Authorized framework SHA:
- Authorized target SHA:
- Authorized provider/model:
- Authorized environment:
- Authorized command:
- Authorization date:
```

This block is intentionally blank. No approval is pre-filled. The technical
model-enforcement prerequisite is resolved (§3a, PR #87), but Stage 1
execution still requires a separate, explicit owner instruction filling in
and dating the block above. Merging PR #85 approves this documentation
package as an accurate planning artifact; it does not fill in this block and
does not authorize execution.
