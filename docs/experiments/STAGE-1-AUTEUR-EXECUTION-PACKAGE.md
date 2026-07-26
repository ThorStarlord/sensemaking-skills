# Stage 1 Auteur Execution Package

**Date**: 2026-07-26
**Nature of this document**: planning and documentation only. It resolves and
records the exact configuration a Stage 1 controlled `auteur` rerun *would*
use. **No experiment was run to produce this document. No auteur rerun
occurred. No code, test, validator, prompt, contract, or runtime file was
changed. No historical evidence was modified.**

## 1. Governance boundary

- Baseline: `main@ac5de55c700cd1b15f2eea1ca2726e83cd8d3284` (verified: this is
  the exact `origin/main` HEAD at the time this package was prepared — merge
  commit for PR #84, "docs: ratify external-validation target and staged
  evidence plan").
- PR #84: merged, `main`, docs-only (`docs/PHASE-80-81-CLOSURE.md`,
  `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`,
  `docs/adr/0021-production-readiness-requirements.md`).
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

## 2. Pinned revisions

### Framework revision

```text
Framework repository: ThorStarlord/sensemaking-skills
Framework SHA: ac5de55c700cd1b15f2eea1ca2726e83cd8d3284
Why this SHA: exact origin/main HEAD, the merge commit for PR #84. Confirmed
  via `git log origin/main -1` and `git merge-base --is-ancestor
  ac5de55c700cd1b15f2eea1ca2726e83cd8d3284 origin/main`. Using this exact
  commit avoids a moving branch at execution time and requires no advance
  past the caller-supplied baseline.
Contains PR #81 contract redesign: yes (PR #81 merged at 9a7d7d5, an
  ancestor of ac5de55)
Contains PR #84 governance record: yes (ac5de55 is PR #84's own merge commit)
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

```text
Provider: Anthropic, via the Claude Agent SDK (claude_agent_sdk.query()),
  not the raw Anthropic Python SDK client. Confirmed at
  scripts/skill_executor.py — the executor path actually used in the
  historical campaign (`--executor claude-code`) constructs
  ClaudeAgentOptions and calls `query()`; a separate, unused code path in the
  same file (an `AnthropicSkillExecutor`-style fallback, ~line 1432-1443)
  calls `Anthropic().messages.create(model="claude-opus-4-7", ...)` directly,
  but that is NOT the path the historical campaign used and is NOT what
  --executor claude-code invokes.
Model: NOT explicitly pinned in code for the claude-code executor path.
  scripts/skill_executor.py's ClaudeAgentOptions construction (around line
  1229) sets cwd, setting_sources, skills, allowed_tools, and hooks, but does
  NOT set a `model` field. The model actually used is therefore whatever the
  ambient Claude Agent SDK / Claude Code CLI installation resolves as its
  default at invocation time — this is a genuine, pre-existing gap, not
  something this package can respecify without a code change (which is out
  of scope for this planning task).
Model version or immutable identifier, if available: none pinned in code;
  this package cannot supply one without either (a) a runtime code change to
  pass an explicit `model=` to ClaudeAgentOptions, out of scope here, or (b)
  the owner confirming the ambient CLI/SDK default at actual execution time
  and recording it in the authorization block below before running.
Temperature: not set anywhere in scripts/skill_executor.py's
  ClaudeAgentOptions construction; SDK default applies.
Max tokens: not set in the claude-code executor path (ClaudeAgentOptions has
  no max_tokens field set); SDK default applies. (The separate, unused
  Anthropic-direct fallback path hardcodes max_tokens=4096, but is not
  invoked by --executor claude-code.)
Reasoning mode: not configured/exposed by this executor path.
Tool permissions: allowed_tools=["Read", "Write", "Glob", "Grep"] only.
  Bash/PowerShell/Agent (subagent spawn) are NOT in allowed_tools; the
  historical evidence (PR #78) confirms PowerShell and Agent invocation
  attempts were denied (PreToolUse only, no PostToolUse completion).
Filesystem permissions: PreToolUse hook `artifact_permission_gate` +
  `pre_trace`; PostToolUse hook `post_trace`. Historical evidence shows this
  gate denied both target-directed Write attempts in the PR #78 rerun.
Network permissions: none granted by allowed_tools; no network-capable tool
  is in the allowed set.
Any fallback model: NONE documented or configured anywhere in the executor.
  No fallback, no retry, no escalation logic exists in
  scripts/skill_executor.py's claude-code path for a failed/errored SDK call
  — a ResultMessage error is captured and classified, not retried.
```

Requirements restated and confirmed against the actual code:

- No model fallback exists in code — none should be introduced for Stage 1.
- No silent provider substitution — the executor path is single, fixed
  (`claude_agent_sdk.query()`), not switchable at runtime by the model.
- No automatic retry — confirmed absent in `scripts/skill_executor.py`.
- No automatic model escalation — confirmed absent.
- No second run after failure — this is an owner/process rule for Stage 1,
  not currently enforced by code; the exact command plan in §6 is a single
  invocation, and the hard-stop matrix (§11) requires stopping, not rerunning,
  on failure.

**Difference from the historical campaign**: none identified — the
historical campaign (PR #78) used the identical `--executor claude-code`
path with the same unpinned-model characteristic. This package does not
introduce a new model/provider risk relative to history; it inherits and
discloses a pre-existing one (no explicit model pin in code).

**Owner action required before authorizing execution**: confirm the ambient
Claude Agent SDK / Claude Code CLI default model at the moment of execution
and record it explicitly in the authorization block (§16) so the run is not
silently subject to a future default-model change between authorization and
execution.

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
  workspace layout (§5), command sequence (§6).
- **Inherited from the runner/executor environment at execution time**:
  Python/Node/git patch versions beyond what's recorded above, locale,
  timezone, Claude Agent SDK package version, authentication mechanism,
  resolved default model (see §3).
- **Unknown until execution**: exact ambient default model identifier;
  exact Claude Agent SDK version; exact wall-clock start time.

## 5. Disposable workspace layout

Following the historical campaign's own pattern (`H:\scratch\auteur-campaign-final\`,
outside both the primary checkout and `.claude/worktrees/`), a fresh,
standalone, disposable set of clones is proposed for Stage 1:

```text
H:\scratch\stage1-auteur-rerun\
  framework\        <- fresh clone of ThorStarlord/sensemaking-skills,
                       checked out to ac5de55c700cd1b15f2eea1ca2726e83cd8d3284
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
git checkout ac5de55c700cd1b15f2eea1ca2726e83cd8d3284

git clone <auteur-repo-source> H:\scratch\stage1-auteur-rerun\target-auteur
cd H:\scratch\stage1-auteur-rerun\target-auteur
git checkout b40db654e0df9e90074f7ad85b40d7362378e07d

# 2. SHA verification
cd H:\scratch\stage1-auteur-rerun\framework
git rev-parse HEAD
# expect: ac5de55c700cd1b15f2eea1ca2726e83cd8d3284

cd H:\scratch\stage1-auteur-rerun\target-auteur
git rev-parse HEAD
# expect: b40db654e0df9e90074f7ad85b40d7362378e07d

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
# EXECUTION BOUNDARY -- DO NOT RUN WITHOUT OWNER AUTHORIZATION
# ============================================================

# 5. Experiment invocation (INVOKES THE MODEL -- gated)
python scripts\workflow-runtime.py \
  "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --gate-decision auto-approve \
  --repo-root "H:/scratch/stage1-auteur-rerun/framework" \
  --target-repo "H:/scratch/stage1-auteur-rerun/target-auteur" \
  --log-dir "H:/scratch/stage1-auteur-rerun/logs"

# 6. Brief validation
python scripts\validate-and-report.py H:\scratch\stage1-auteur-rerun\framework\artifacts\...\repository_sensemaking_brief.md

# 7. Duplicate-key check (see Part 7 script below)
python H:\scratch\stage1-auteur-rerun\evidence\check_duplicate_weakness_type.py H:\scratch\stage1-auteur-rerun\framework\artifacts\...\repository_sensemaking_brief.md

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

Issue #83 records this as a known, undetected residual gap
(`docs/PHASE-80-81-CLOSURE.md` §1a/§2): PyYAML's `safe_load` silently keeps
the last value on a duplicate mapping key, and no code in
`scripts/validate-brief.py` / `_validator_utils.py` currently detects this.

Proposed script (to be placed in the experiment's own `evidence\` directory,
NOT committed to production code as part of this task):

```python
# H:\scratch\stage1-auteur-rerun\evidence\check_duplicate_weakness_type.py
"""Deterministic check: Section 13 YAML fence contains exactly one
top-level `weakness_type` key. Uses raw YAML parsing (not safe_load) so
duplicate keys are actually detected rather than silently resolved."""
import re
import sys
import yaml

def check(brief_path: str) -> int:
    with open(brief_path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not m:
        print("FAIL: no ```yaml fence found in brief")
        return 2
    yaml_block = m.group(1)

    # Count raw top-level `weakness_type:` key occurrences textually,
    # independent of PyYAML's last-value-wins behavior.
    key_lines = [
        line for line in yaml_block.splitlines()
        if re.match(r"^weakness_type\s*:", line.strip())
    ]
    count = len(key_lines)

    if count == 0:
        print("FAIL: no weakness_type key found")
        return 2
    if count > 1:
        print(f"FAIL: duplicate weakness_type key found ({count} occurrences) -- HARD STOP")
        for i, line in enumerate(key_lines, 1):
            print(f"  occurrence {i}: {line.strip()}")
        return 1
    print(f"PASS: exactly one weakness_type key found: {key_lines[0].strip()}")
    return 0

if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
```

```text
Exact command: python check_duplicate_weakness_type.py <brief_path>
Expected success output: "PASS: exactly one weakness_type key found: weakness_type: <value>"
  -> exit code 0
Expected failure output: "FAIL: duplicate weakness_type key found (N occurrences) -- HARD STOP"
  followed by each occurrence line -> exit code 1
Expected no-key-found output: "FAIL: no weakness_type key found" -> exit code 2
```

Requirements honored: duplicate key = hard stop (exit 1, non-zero); the
artifact is never edited to repair it; it is preserved as-is in
`evidence\`; no automatic rerun follows a duplicate-key failure.

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
| Provider/model mismatch | Recorded model at execution time differs from what was authorized in §16 | Stop before invocation, or stop and flag if discovered after | Preserve authorization block + actual observed config |
| Automatic fallback or retry | Any retry/fallback logic observed in logs (none should exist per §3) | Stop; treat as a process violation | Preserve logs |
| Output written into target repository | §8 manifest/status diff shows a new file under `target-auteur\` | Stop | Preserve manifests, diff |

For every hard stop: stop immediately; preserve all evidence; do not patch;
do not edit the generated brief; do not rerun; return to the owner.

## 12. Success definition

Stage 1 succeeds only if **all** of the following hold:

1. Exact pinned revisions used (framework `ac5de55c700cd1b15f2eea1ca2726e83cd8d3284`,
   target `b40db654e0df9e90074f7ad85b40d7362378e07d`).
2. Expected model/provider used (as recorded and confirmed in the
   authorization block at execution time — see §3's disclosed gap).
3. No automatic retry or fallback.
4. Structural Stage A completion (§9 = PASS).
5. No blocking validator error.
6. No duplicate `weakness_type` key (§7 script exit 0).
7. Deterministic quote grounding (no `EVIDENCE_QUOTE_NOT_FOUND`).
8. No target mutation (§8 all checks clean).
9. Complete trace and logs present.
10. Substantive review passes (§10 all sections satisfactory).
11. Every high-risk claim is Confirmed (none Rejected or Inconclusive).
12. Brief judged useful enough to justify considering Stage 2.

**Stage 1 success proves only** that the redesigned contract (PR #81) cleared
the historical `auteur` target under the pinned configuration and survived
the required review.

**Stage 1 success explicitly does NOT prove**:

- D8 is satisfied (D8 requires at least two structurally different
  repositories plus human usefulness review — this experiment covers
  neither by itself).
- Cross-repository generality.
- Production readiness.
- Autonomous trustworthiness.
- Maintainer usefulness (beyond this one reviewer's judgment on this one
  target).
- Stage 2 authorization (Stage 2 remains conditional on separate, explicit
  owner review of Stage 1's actual evidence after it runs).

## 13. Owner authorization block

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

This block is intentionally blank. No approval is pre-filled.
