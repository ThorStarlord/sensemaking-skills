# Stage 1 Auteur Execution Package

**Date**: 2026-07-27 (revised: this revision is a documentation-only refresh
prepared for possible owner consideration of a **second** controlled Stage 1
run, after the first authorized run — Evidence 0013 — completed with result
`STAGE 1 FAIL`, and after the remediation that followed it (PR #91, PR #92,
PR #94) merged to `main`.)
**Nature of this document**: planning and documentation only. It resolves and
records the exact configuration a **second**, new Stage 1 controlled `auteur`
run *would* use. **No experiment was run to produce this revision. No auteur
rerun occurred. No code, test, validator, prompt, contract, or runtime file
was changed by this document. No historical evidence was modified.**

```text
Stage 1 second-run execution authorization status = NOT AUTHORIZED

Planning-package preparation: authorized (this revision).
Execution: NOT authorized by this revision or by merging its PR.
Merging the documentation PR that carries this revision does not authorize
  execution. A separate, explicit owner instruction — issued after this
  package revision is merged and reviewed — is required.
At most one future invocation could be authorized by such an instruction.
No automatic retry, repair, or rerun would be permitted even then.

Proposed second-run framework baseline:
1098acfd614e497bdf551040d3b1dee30afb9834

Historical first-run framework baseline:
68b44835be43b86ee7c0d7eb968e67efcd368443

Historical Stage 1 result:
FAIL (Evidence 0013 — see new §1a)

Historical model:
claude-sonnet-5

Historical target:
b40db654e0df9e90074f7ad85b40d7362378e07d

Owner model decision (unchanged from the first run):
Provider = Anthropic via Claude Agent SDK
Model identifier = claude-sonnet-5
Historical model identity (pre-PR #87 runs) = unknown and unrecoverable
Purpose = controlled comparison baseline — same target, same model,
  remediated framework
```

The technical blocker addressed by PR #87 (no code-level way to pin and
enforce an explicit model) remains resolved and unaffected by this revision.
This revision's purpose is different: the first authorized run under that
enforcement (Evidence 0013, PR #88) reached structural validation and
**failed** with three blocking `EVIDENCE_QUOTE_NOT_FOUND` errors. Issues
#89, #90, and #93 were opened, remediated, and closed; the fixes (PR #91,
PR #92, PR #94) are now on `main` at the pinned SHA above. This package
proposes pinning a **second, new controlled run** to that remediated SHA —
it is **not** a claim that the first run's failure is now proven fixed, only
that the specific failure mechanisms it exposed have been addressed in code.

**This is a new proposed baseline, not a historical-equivalence claim.** The
proposed framework intentionally differs from the first run's framework
because it includes the three remediation PRs above. Retaining the same
target SHA and the same model identifier is a deliberate controlled-
comparison choice (see §1a/§1b), not an oversight.

**Nothing in this revision authorizes Stage 1 execution.** Execution
authorization is a separate owner decision, recorded (still blank) in §13.
Merging the documentation PR that carries this revision approves this
package as an accurate, current planning artifact — it does not itself
authorize running Stage 1, and no automatic retry, repair, or rerun would be
permitted even after a future authorization; at most one invocation could
ever be authorized by such an instruction.

## 1. Governance boundary

- Proposed second-run baseline: `main@1098acfd614e497bdf551040d3b1dee30afb9834`
  (verified: this is the exact `origin/main` HEAD used to prepare this
  revision; a fixed, pinned commit, not a moving branch reference). This SHA
  contains, in addition to everything the first-run pin contained:
  - PR #81 (brief-contract redesign — `weakness_type` structured field);
  - PR #84 (governance ratification — D7/D8/E4 staged-validation record);
  - PR #87 (explicit model-selection and executor enforcement — issue #86);
  - PR #88 (Evidence 0013 — the first authorized Stage 1 run, result FAIL);
  - PR #91 (deterministic evidence-quote extraction — issue #89);
  - PR #92 (section-aware duplicate-key safeguard foundation — issue #90);
  - PR #94 (safeguard integrated into authoritative brief validation —
    issue #93).
- The first-run framework SHA `68b44835be43b86ee7c0d7eb968e67efcd368443` is
  **historical**: it is the exact commit Evidence 0013 was executed against
  (PR #88). It is **superseded** by `1098acfd614e497bdf551040d3b1dee30afb9834`
  as the active proposed pin throughout this revision. `68b44835...` remains
  an ancestor of the new pin.
- PR #84: merged, `main`, docs-only (`docs/PHASE-80-81-CLOSURE.md`,
  `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`,
  `docs/adr/0021-production-readiness-requirements.md`).
- PR #87: merged, `main`, code (`scripts/workflow-runtime.py`,
  `scripts/skill_executor.py`, `tests/test_model_enforcement.py`) — adds
  explicit `--model` / `--controlled-experiment` enforcement. See §3/§3a.
- PR #88: merged, `main` — Evidence 0013, the first authorized Stage 1
  controlled run under PR #87's enforcement. Result: **STAGE 1 FAIL**
  (structural validation failed; three blocking `EVIDENCE_QUOTE_NOT_FOUND`
  errors; substantive review not reached). See new §1a for full detail.
- PR #91, PR #92, PR #94: merged, `main` — remediation of the three failure
  mechanisms Evidence 0013 exposed. See new §1b for full detail.
- Issue #83 ("Run controlled auteur validation after brief-contract
  redesign"): **CLOSED as completed-with-failure**. The single authorized
  Stage 1 run it scoped occurred (PR #88 / Evidence 0013) and produced a
  definitive `STAGE 1 FAIL` result; the issue was closed on that basis, not
  reopened, and this revision does not reopen it. A **second** run is a new,
  separately-scoped proposal — this package — not a continuation of issue
  #83.
- Issues #89, #90, #93: **CLOSED**, each after its corresponding remediation
  PR (#91, #92, #94 respectively) merged. See §1b.
- D7 = Externally validated (ratified). D8 = success on at least two
  structurally different external repositories, including clean structural
  validation, substantive audit, no target mutation, pinned revisions,
  repeatability, and human usefulness review on at least one target
  (ratified).
- E4 = staged plan (ratified): Stage 1 = controlled auteur rerun; Stage 2 =
  second structurally different repository (conditional, unauthorized);
  Stage 3 = real-maintainer usefulness evaluation (conditional,
  unauthorized). The first Stage 1 attempt (Evidence 0013) failed
  structurally; Stage 2/3 remain unauthorized and are unaffected by this
  revision.
- **Preparation of this second-run planning package is authorized. Stage 1
  second-run execution is NOT authorized** and requires a separate, explicit
  owner instruction after reviewing this package. Merging the documentation
  PR that carries this revision does not supply that instruction.
- ADR 0021 remains **Proposed** (three other named owner-decision items —
  cost/concurrency policy, supported-agent commitments, platform scope —
  remain outstanding regardless of D7/D8 ratification). This revision does
  not change ADR 0021's status.
- Current achieved readiness remains **"Externally exercised"** (Level C).
  Neither the first run's failure nor this planning revision changes this
  level. Ratifying D7/D8/E4 does not itself advance this level.

### 1a. Historical result: Evidence 0013 (PR #88) — STAGE 1 FAIL

The first authorized Stage 1 run executed under this package's prior
revision, pinned to `main@68b44835be43b86ee7c0d7eb968e67efcd368443`, target
`b40db654e0df9e90074f7ad85b40d7362378e07d`, model `claude-sonnet-5`. Full
record: `experiments/evidence/0013-stage1-auteur-run-model-enforcement/`.

```text
Invocations: exactly one (model/workflow invocation count = 1)
Model requested: claude-sonnet-5
Model reported (all AssistantMessage events): claude-sonnet-5 (uniform)
model_match: true
Fallback: none
Retry: none
Target mutation: none (target-directed Write attempt observed, denied by
  the framework's target-confinement gate before completion; zero completed
  target writes)
Structural validation: FAIL — three blocking EVIDENCE_QUOTE_NOT_FOUND errors
Substantive review: NOT reached (gated on structural PASS, which did not
  occur)
Final result: STAGE 1 FAIL
```

The three blocking quote-fidelity defects, by class (these are citation
**quote-fidelity** defects — paraphrasing/normalization introduced while
transcribing an otherwise-real, otherwise-correctly-cited excerpt — not
hallucinated files; all three cited files and line ranges exist in the
target at the pinned SHA):

1. **Em-dash normalization** — `src/auteur/decision/service.py` L1: the
   generated brief's quote used `--` where the actual source uses an em dash
   (`—`).
2. **Omitted indentation** — `src/auteur/cli_parser.py` L419-L420: the
   brief's quote dropped the actual file's leading 4-space indentation on
   the first quoted line.
3. **Lost Markdown/backtick formatting** — `CHANGELOG.md` L349-L362: the
   brief's quote dropped bold/backtick formatting present in the source and
   normalized an em dash in the heading.

**Historical transparency note on validator invocation**: the first
validator pass in that run (`validator-output.txt`) was invoked without
`--target-repo` and incorrectly reported `HALLUCINATED_FILE` errors as a
result of that missing flag — a mistake in how the validator was invoked
that run, not a defect in the brief or the validator itself. The corrected
invocation (`validator-output-corrected.txt`, run with both `--repo-root`
and `--target-repo` set) is the authoritative historical result: **zero**
`HALLUCINATED_FILE` errors; the three `EVIDENCE_QUOTE_NOT_FOUND` errors above
are the real, blocking structural result. §6 and §9 of this revision are
written so that no new verification procedure repeats the missing-
`--target-repo` mistake.

Evidence 0013, PR #78, and this document's historical narrative are not
modified by this revision.

### 1b. Remediation now included in the proposed framework pin

The proposed pin `1098acfd614e497bdf551040d3b1dee30afb9834` includes three
merged fixes targeting the specific failure mechanisms Evidence 0013
exposed. This does **not** guarantee a passing second run — it removes the
known failure mechanisms that produced the first run's `STAGE 1 FAIL`.

**PR #91 (issue #89) — deterministic evidence-quote extraction**:
- The model identifies a source path, line/char range, and rationale only;
  it is no longer treated as the authoritative source of the quoted text.
- The runtime extracts the exact quote text from the source file at the
  identified range itself; model transcription is not authoritative.
- Unicode normalization, indentation preservation, Markdown/backtick
  formatting, and newline handling are governed by deterministic,
  code-level policy rather than model transcription fidelity.
- Path containment and target-root authority are enforced (the extraction
  path cannot escape the declared target root).
- The strict quote-grounding validator itself is unchanged; it validates the
  now-deterministically-extracted quote against source, same as before.

**PR #92 (issue #90) — section-aware duplicate-key safeguard foundation**:
- The authoritative Section 13 handoff block is located structurally (by
  heading), not by a document-wide first-fence regex — this directly fixes
  the mechanism Evidence 0013's manual-inspection note flagged (a malformed
  doubled fence in Section 8 defeating a naive single-fence regex).
- Duplicate-key-safe YAML loading replaces `safe_load`'s silent
  last-value-wins behavior for the handoff block.
- The standalone diagnostic CLI (`scripts/weakness_type_safeguard.py`)
  remains available for manual, non-authoritative use.

**PR #94 (issue #93) — pipeline integration**:
- The safeguard from PR #92 now executes automatically inside
  `validate_brief()` — it is no longer a separate script a human must
  remember to run.
- It runs before ordinary YAML parsing can collapse duplicate keys, so a
  duplicate-key defect surfaces as a validator error rather than being
  silently resolved by last-value-wins.
- Its outcomes surface as first-class blocking/non-blocking error codes in
  standard `validate-and-report.py` output: `DUPLICATE_WEAKNESS_TYPE_KEYS`,
  `MALFORMED_HANDOFF_FENCE`, `MISSING_HANDOFF_SECTION`,
  `MISSING_HANDOFF_BLOCK`, `HANDOFF_YAML_PARSE_ERROR`.
- A normal `validate-and-report.py` invocation (with `--repo-root` and
  `--target-repo` both set) is the authoritative validation path; no
  separate script invocation is required or authoritative.
- Missing `weakness_type` remains non-blocking under ratified D2 (a
  validator-policy fact) — this is distinct from this package's own
  **experiment success policy**, which still requires the required
  metadata to be present for the run to count as Stage 1 success. See §12.
- The obsolete experiment-local regex script
  (`check_duplicate_weakness_type.py`, preserved only inside the Evidence
  0013 directory for historical transparency) is superseded and must not be
  treated as authoritative for a second run.

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
#84 merged, issue #83 closed as completed-with-failure, and ADR 0021 status
are all independently confirmed correct above) — it is a separate fact
surfaced by
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
Framework SHA (proposed second-run baseline): 1098acfd614e497bdf551040d3b1dee30afb9834
Why this SHA: exact origin/main HEAD at the time this revision was prepared,
  and the current owner-supplied authoritative baseline. Confirmed via
  `git rev-parse origin/main` and `git merge-base --is-ancestor
  1098acfd614e497bdf551040d3b1dee30afb9834 origin/main`. A fixed commit, not
  a moving branch reference, is recorded here deliberately.
Contains PR #81 contract redesign: yes (ancestor)
Contains PR #84 governance record: yes (ancestor)
Contains PR #87 explicit model-selection enforcement: yes (ancestor; adds
  --model / --controlled-experiment, ClaudeAgentOptions(model=),
  requested/reported-model evidence, and hard-stop-on-mismatch behavior --
  see §3/§3a)
Contains PR #88 (Evidence 0013, first Stage 1 run, result FAIL): yes
  (ancestor) -- see §1a
Contains PR #91 (deterministic evidence-quote extraction, issue #89): yes
  (ancestor; confirmed `git merge-base --is-ancestor <PR-91-merge-sha>
  1098acfd614e497bdf551040d3b1dee30afb9834`) -- see §1b
Contains PR #92 (section-aware duplicate-key safeguard, issue #90): yes
  (ancestor, same verification method) -- see §1b
Contains PR #94 (safeguard pipeline integration, issue #93): yes (ancestor,
  same verification method) -- see §1b

Historical first-run framework SHA (superseded, retained for comparison):
  68b44835be43b86ee7c0d7eb968e67efcd368443 -- pinned in the prior revision
  of this package and used to produce Evidence 0013 (PR #88, STAGE 1 FAIL).
```

Note on the documentation PR's own merge commit: the eventual merge commit
that lands this revision's documentation PR is **not** a new runtime
baseline and must not be treated as one. The proposed framework pin for a
second run remains exactly `1098acfd614e497bdf551040d3b1dee30afb9834` — the
precise code baseline being reviewed, prior to and independent of this
docs-only PR. A docs-only merge commit is control-plane documentation, not
an execution pin; it would not be substituted in as the second run's
framework SHA even after this PR merges.

### Auteur (target) revision

```text
Target repository: auteur
Canonical clone URL (resolved for issue #98, verified — not guessed):
  https://github.com/ThorStarlord/auteur.git
  Verified by: read-only inspection of a local auteur repository's `origin`
  remote (`git -C <local-auteur-path> remote -v`); confirmation the
  repository is public (`gh repo view ThorStarlord/auteur --json
  visibility` => PUBLIC); confirmation the pinned target SHA is reachable
  from that remote's `main` branch (`git -C <local-auteur-path> branch -r
  --contains b40db654e0df9e90074f7ad85b40d7362378e07d` includes
  `origin/main`). No credentials are embedded in this URL; safe to commit.
  See §6a for the full source-resolution procedure, the local-source
  fallback, hard stops, and the source/execution-clone distinction.
Target SHA: b40db654e0df9e90074f7ad85b40d7362378e07d
Historical comparison source: PR #78 / evidence directory
  experiments/evidence/0012-external-repo-auteur-final-rerun/EVIDENCE.md,
  read via `git show origin/evidence/auteur-campaign-final-rerun:...`
  (read-only; that branch is NOT merged to main — see the governance
  discrepancy note in §1).
Why this SHA (unchanged for a second run): this is the exact commit pinned
  in the final, most recent historical campaign rerun (PR #78), the same
  commit that previously produced the PR #73 "ghost feature" false-positive
  finding, and the same commit the first authorized Stage 1 run (Evidence
  0013, PR #88) used. Holding the target SHA fixed across the first and
  proposed second run preserves before/after comparability on exactly one
  axis: the remediated framework (PR #91/#92/#94). Changing the target SHA
  for a second run would introduce a second, uncontrolled variable and make
  it impossible to attribute a different outcome to the remediation.
Moving branch avoided: yes — an exact SHA, not a branch name, is recorded;
  §6a's hard stops explicitly prohibit a source branch, remote HEAD, or
  local checked-out branch ever substituting for this pinned SHA.
```

No clone of, or write to, the target repository was performed to prepare
this or the prior revision of this package. Resolving issue #98 involved only
read-only inspection of a pre-existing local auteur repository's Git
configuration (`git remote -v`, `git branch -r --contains ...`) and a
read-only GitHub API query for repository visibility — no clone, no write,
no network access to the target's contents. The target SHA above is
independently confirmed reachable from the canonical remote's `main` branch
by that inspection (see §6a); it was not merely repeated from the historical
evidence record.

Historical note (Evidence 0014, PR #96): the prior revision of this package
left the clone-source command as a literal, unresolved placeholder
(`<auteur-repo-source>`). That gap forced the Evidence 0014 operator to
improvise, using a clean local working copy at `H:\GithubRepositories\auteur`
as an undisclosed deviation. Issue #98 tracked closing that gap. §6a below
resolves it; the local path above is retained only as that historical example
and as the fallback procedure's documented example value — it is not a
universal or hard-coded path for future runs.

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
- No automatic or self-authorized second run — a deliberate second run is
  exactly what this package proposes, but only under a separate, explicit
  owner instruction (§13); the exact command plan in §6 is, once authorized,
  a single invocation, with no automatic retry/repair/rerun even then (see
  §16-style hard stops in §11).

**Difference from the historical (pre-PR #87) campaign**: the historical
campaign (PR #78) used the identical `--executor claude-code` path but with
no explicit model pin — its actual model is unknown and unrecoverable (see
§3a Part 2). The first authorized Stage 1 run under PR #87's enforcement
(Evidence 0013, PR #88) did pin and confirm `claude-sonnet-5`
(`model_match: true`); this proposed second run retains that same pinned
model. It is not a claim of equivalence with the pre-PR #87 historical
campaign's (unknown) model — it is a controlled repeat of the model axis
that Evidence 0013 already established and confirmed.

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
H:\scratch\stage1-auteur-rerun-2\
  framework\        <- fresh clone of ThorStarlord/sensemaking-skills,
                       checked out to 1098acfd614e497bdf551040d3b1dee30afb9834
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
- No reuse of any previous output directory (a new `stage1-auteur-rerun-2`
  root, distinct both from the first run's `stage1-auteur-rerun\` directory,
  which produced Evidence 0013, and from the older historical
  `auteur-campaign-final\`).
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
git clone https://github.com/ThorStarlord/sensemaking-skills.git H:\scratch\stage1-auteur-rerun-2\framework
cd H:\scratch\stage1-auteur-rerun-2\framework
git checkout 1098acfd614e497bdf551040d3b1dee30afb9834

# Auteur (target) clone -- see §6a for the full source-resolution
# procedure, preflight checks, and hard stops. Primary source: the
# canonical remote (requires network access at execution time). Fallback:
# a preflight-checked local AUTEUR_SOURCE_REPO (offline). Do not improvise
# outside these two documented alternatives.
git clone https://github.com/ThorStarlord/auteur.git H:\scratch\stage1-auteur-rerun-2\target-auteur
# -- OR, only if the canonical remote is unavailable (fallback; the
#    AUTEUR_SOURCE_REPO variable must be set explicitly by the operator and
#    must pass every §6a local-source preflight check before this is run):
# git clone "$AUTEUR_SOURCE_REPO" H:\scratch\stage1-auteur-rerun-2\target-auteur

cd H:\scratch\stage1-auteur-rerun-2\target-auteur
git checkout --detach b40db654e0df9e90074f7ad85b40d7362378e07d

# 2. SHA verification
cd H:\scratch\stage1-auteur-rerun-2\framework
git rev-parse HEAD
# expect: 1098acfd614e497bdf551040d3b1dee30afb9834

cd H:\scratch\stage1-auteur-rerun-2\target-auteur
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

# 2b. Remediation-ancestor check (new for this revision): PR #91, #92, #94
#     merge commits must each be an ancestor of the checked-out framework
#     HEAD. (Merge SHAs as recorded when this revision was prepared:
#     PR #91 = e65da78b3e519768d09568dcf64d5a1dc8526d6b,
#     PR #92 = f8c40fd6e79d961ad14d83df586430177d4012d2,
#     PR #94 = 1098acfd614e497bdf551040d3b1dee30afb9834 (== framework HEAD).)
git merge-base --is-ancestor e65da78b3e519768d09568dcf64d5a1dc8526d6b HEAD
git merge-base --is-ancestor f8c40fd6e79d961ad14d83df586430177d4012d2 HEAD
git merge-base --is-ancestor 1098acfd614e497bdf551040d3b1dee30afb9834 HEAD
# expect: exit 0 for all three. Failure is a preflight hard stop (see §11).

# 3. Dependency setup
cd H:\scratch\stage1-auteur-rerun-2\framework
python -m pip install -r requirements.txt   # if present; record exact versions installed

# 4. Preflight validation (framework repo only, no target touched)
python scripts\validate-repo.py
python scripts\test-validators.py
git status --short                          # expect: clean
cd H:\scratch\stage1-auteur-rerun-2\target-auteur
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
  --repo-root "H:/scratch/stage1-auteur-rerun-2/framework" \
  --target-repo "H:/scratch/stage1-auteur-rerun-2/target-auteur" \
  --log-dir "H:/scratch/stage1-auteur-rerun-2/logs"

# NOTE: --repo-root and --target-repo above are pinned by preceding
# checkout to 1098acfd614e497bdf551040d3b1dee30afb9834 (framework) and
# b40db654e0df9e90074f7ad85b40d7362378e07d (target); this command has no
# moving branch reference of its own.

# 6. Brief validation -- AUTHORITATIVE. Must include both --repo-root and
#    --target-repo (see §1a's historical-transparency note: the first run's
#    initial validator invocation omitted --target-repo and produced
#    spurious HALLUCINATED_FILE errors as a result; this command must not
#    repeat that mistake). This automatically runs the section-aware,
#    duplicate-key-safe weakness_type safeguard as part of validate_brief()
#    -- see §1b / Part 7 below.
python scripts\validate-and-report.py H:\scratch\stage1-auteur-rerun-2\framework\artifacts\...\repository_sensemaking_brief.md --repo-root H:\scratch\stage1-auteur-rerun-2\framework --target-repo H:\scratch\stage1-auteur-rerun-2\target-auteur

# 7. (Optional, diagnostic-only) standalone safeguard re-check -- NOT
#    authoritative on its own and must not replace step 6; see Part 7 below.
python scripts\weakness_type_safeguard.py H:\scratch\stage1-auteur-rerun-2\framework\artifacts\...\repository_sensemaking_brief.md

# 8. Target-mutation check
cd H:\scratch\stage1-auteur-rerun-2\target-auteur
git status --porcelain
git diff --exit-code
git diff --cached --exit-code
git rev-parse HEAD
# compare HEAD before/after; expect identical to b40db654e0df9e90074f7ad85b40d7362378e07d

# 9. Evidence collection
#   copy brief, logs, trace, manifests into H:\scratch\stage1-auteur-rerun-2\evidence\

# 10. Final status reporting
#   summarize PASS/FAIL/INCONCLUSIVE per Part 9 below; return to owner
```

## 6a. Auteur clone-source procedure (resolves issue #98)

This section replaces the prior revision's literal, unresolved
`<auteur-repo-source>` placeholder (§6 step 1) with a deterministic,
reviewable procedure. It authorizes nothing beyond documentation review —
see §16/§13; no Stage 1 run is authorized by this revision.

```text
The clone source is transport. The exact target SHA is authority.
```

Changing the source never changes the target. A source branch, the
canonical remote's default branch, its remote `HEAD`, or a local checked-out
branch must never be substituted for
`b40db654e0df9e90074f7ad85b40d7362378e07d`.

### Source repository vs. execution clone (required distinction)

```text
source repository: an existing, trusted repository used only as the
  object/ref source for cloning. It is never passed to the runtime as
  --target-repo.
execution clone: a fresh, disposable clone created from the source
  repository and checked out at the exact target SHA. This is the only
  path ever supplied as --target-repo.

Required invariant:
  trusted source -> fresh disposable clone -> checkout exact target SHA
  -> verify clean detached state -> use disposable clone as --target-repo
```

### Primary source: canonical remote (verified for this revision)

```text
Canonical clone URL: https://github.com/ThorStarlord/auteur.git
Verified: public GitHub repository (`gh repo view ThorStarlord/auteur
  --json visibility` => PUBLIC); the pinned target SHA
  (b40db654e0df9e90074f7ad85b40d7362378e07d) is reachable from this
  remote's `main` branch, confirmed via read-only inspection of a
  pre-existing local auteur repository's `origin` remote-tracking refs
  (`git branch -r --contains b40db654e0df9e90074f7ad85b40d7362378e07d`
  lists `origin/main`). No credentials are embedded in this URL.
Requires network access to github.com at execution time.
```

Clone command (primary):

```text
git clone https://github.com/ThorStarlord/auteur.git <fresh-execution-clone-path>
cd <fresh-execution-clone-path>
git checkout --detach b40db654e0df9e90074f7ad85b40d7362378e07d
```

### Fallback source: approved local-source procedure (offline / no network)

Use this only when the canonical remote above is unavailable at execution
time.

```text
Required variable (the operator must set this explicitly before execution;
it must never be hard-coded in this package as a universal path):
  AUTEUR_SOURCE_REPO=<absolute path to an existing, trusted local auteur
    repository>

Historical example only (Evidence 0014, PR #96) -- not a universal value
and not a default:
  AUTEUR_SOURCE_REPO=H:\GithubRepositories\auteur
```

Local-source preflight — PowerShell (primary shell in this environment):

```powershell
Test-Path "$env:AUTEUR_SOURCE_REPO\.git"
git -C $env:AUTEUR_SOURCE_REPO rev-parse --is-inside-work-tree
git -C $env:AUTEUR_SOURCE_REPO cat-file -e b40db654e0df9e90074f7ad85b40d7362378e07d^{commit}
git -C $env:AUTEUR_SOURCE_REPO status --porcelain
```

Local-source preflight — POSIX/bash equivalent (label clearly; not directly
runnable under plain Windows PowerShell without a bash-style shell):

```bash
test -d "$AUTEUR_SOURCE_REPO/.git"
git -C "$AUTEUR_SOURCE_REPO" rev-parse --is-inside-work-tree
git -C "$AUTEUR_SOURCE_REPO" cat-file -e \
  b40db654e0df9e90074f7ad85b40d7362378e07d^{commit}
git -C "$AUTEUR_SOURCE_REPO" status --porcelain
```

All checks must succeed, and the final `status --porcelain` must report an
empty (clean) working tree, before cloning from the local source. A dirty
`AUTEUR_SOURCE_REPO` working tree is a hard stop (§11). This clean-source
requirement is retained as an operational safety invariant even though
cloning from a repository's object database does not itself depend on
working-tree state.

Clone command (fallback):

```text
git clone "$AUTEUR_SOURCE_REPO" <fresh-execution-clone-path>
cd <fresh-execution-clone-path>
git checkout --detach b40db654e0df9e90074f7ad85b40d7362378e07d
```

### Post-checkout verification (both source models)

```text
git -C <fresh-execution-clone-path> rev-parse HEAD
  # expect: b40db654e0df9e90074f7ad85b40d7362378e07d
git -C <fresh-execution-clone-path> status --porcelain
  # expect: empty
git -C <fresh-execution-clone-path> diff --exit-code
git -C <fresh-execution-clone-path> diff --cached --exit-code
```

Also confirm, before use:

```text
<fresh-execution-clone-path> is a fresh path (did not already exist / was
  not non-empty before the clone).
<fresh-execution-clone-path> is outside .claude/worktrees/.
<fresh-execution-clone-path> does not resolve to the same repository as the
  source (AUTEUR_SOURCE_REPO, or a local working copy of the canonical
  remote) -- e.g. compare `git -C <fresh-execution-clone-path>
  rev-parse --show-toplevel` against the resolved source path.
```

### Offline and network behavior

```text
Local/offline source: a clean, existing local auteur repository that
  contains the exact target commit may be used as the clone source (the
  fallback procedure above). No network lookup of the target commit is
  required once the local preflight checks above pass.
Canonical remote source: if used, requires that the exact target commit
  (b40db654e0df9e90074f7ad85b40d7362378e07d) is retrievable from
  https://github.com/ThorStarlord/auteur.git before authorization is
  consumed. Do not rely on the remote's default/moving branch name --
  the pinned SHA remains authoritative regardless of which source is used.
```

### Evidence fields required for a future run (in addition to §8/§9)

```text
source type: canonical remote | local repository
source value (sanitized -- the canonical URL may be recorded in full; a
  local path may be recorded in full only in private, non-published
  evidence -- see the privacy note below)
source repository HEAD (for a local source), or the canonical remote's
  `main` branch tip at time of use (for the canonical remote)
source target-commit existence check: PASS/FAIL
clone command issued (sanitized -- never record credentials)
execution clone path
execution clone HEAD
execution clone status (`git status --porcelain` output)
source/execution path non-equivalence check: PASS/FAIL
```

Privacy/portability note: a local `AUTEUR_SOURCE_REPO` path may reveal an
operator's local filesystem layout. This package permits recording the full
local path in private, non-published evidence, but operators should weigh
that before including it anywhere shared more broadly.

### Hard stops specific to source resolution

The consolidated hard-stop matrix in §11 includes the following
source-resolution rows: source variable unset, source path absent, source
not a Git repository, canonical remote unavailable, target commit absent
from the source, source URL containing credentials, source and execution
paths resolving to the same repository, destination already existing or
non-empty, clone failure, checkout failure, execution clone `HEAD`
mismatch, dirty execution clone, execution clone under
`.claude/worktrees/`, inability to prove which source was used, and
operator improvisation outside the two documented alternatives above. Every
source-resolution hard stop occurs before any model invocation; because no
`query()`/SDK call has been made at that point, it does not consume a model
invocation under this package's existing authorization semantics (§3,
§13) — corrected preflight configuration remains part of the same
not-yet-consumed attempt.

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
| Framework SHA mismatch | `git rev-parse HEAD` on `framework\` != `1098acfd614e497bdf551040d3b1dee30afb9834` | Stop before invocation | Record observed vs. expected SHA |
| Target SHA mismatch | `git rev-parse HEAD` on `target-auteur\` != `b40db654e0df9e90074f7ad85b40d7362378e07d` | Stop before invocation | Record observed vs. expected SHA |
| Historical evidence commit `a328c80` unreachable or mutated | `git show a328c80:...` / ancestor check against `origin/evidence/auteur-campaign-final-rerun` fails at preflight | Stop before invocation | Preserve the failing verification output |
| PR #91/#92/#94 not ancestors of framework HEAD | §6 step 2b `git merge-base --is-ancestor` fails for any of the three merge SHAs | Stop before invocation | Preserve the failing verification output |
| PR #78 touched or modified | `gh pr view 78` shows a state/head change from open/unmerged, or its evidence branch is force-pushed | Stop; do not proceed | Preserve `gh pr view 78` output |
| Auteur source variable unset (fallback path) | `AUTEUR_SOURCE_REPO` not set when the canonical remote is unavailable | Stop before invocation | Preserve the CLI error output |
| Auteur source path absent | `Test-Path "$env:AUTEUR_SOURCE_REPO\.git"` (or `test -d`) fails | Stop before invocation | Preserve the check output |
| Auteur source not a Git repository | `git -C $env:AUTEUR_SOURCE_REPO rev-parse --is-inside-work-tree` fails | Stop before invocation | Preserve the check output |
| Canonical auteur remote unavailable | `git clone https://github.com/ThorStarlord/auteur.git ...` fails (network/DNS/auth error) | Stop; fall back to the documented local-source procedure (§6a) or stop entirely if that is also unavailable | Preserve the clone error output |
| Target commit absent from auteur source | `git -C <source> cat-file -e b40db654e0df9e90074f7ad85b40d7362378e07d^{commit}` fails | Stop before invocation | Preserve the check output |
| Auteur source URL contains credentials | Clone URL/path contains an embedded token, username:password, or other credential material | Stop; do not commit or log the URL as-is | Preserve a redacted description only |
| Auteur source and execution clone are the same repository | `git -C <execution-clone> rev-parse --show-toplevel` resolves to the same path as the resolved source | Stop before use | Preserve both resolved paths |
| Execution clone destination already exists or is non-empty | Pre-clone check on `<fresh-execution-clone-path>` | Stop before cloning | Preserve the directory listing |
| Auteur clone or checkout failure | `git clone` / `git checkout --detach` returns non-zero | Stop before invocation | Preserve the command output |
| Execution clone `HEAD` mismatch | `git -C <execution-clone> rev-parse HEAD` != `b40db654e0df9e90074f7ad85b40d7362378e07d` | Stop before invocation | Record observed vs. expected SHA |
| Dirty execution clone | `git -C <execution-clone> status --porcelain` non-empty immediately after checkout | Stop before invocation | Preserve `git status`/`git diff` output |
| Execution clone under `.claude/worktrees/` | Path check on `<fresh-execution-clone-path>` | Stop before invocation | Preserve the resolved path |
| Cannot prove which auteur source was used | Evidence fields in §6a ("Evidence fields required for a future run") cannot be completed | Stop; do not proceed on an unverifiable source | Preserve whatever partial evidence exists |
| Operator improvisation outside §6a's two documented alternatives | Any clone-source procedure other than the canonical URL or the preflight-checked `AUTEUR_SOURCE_REPO` fallback | Stop before invocation | Preserve the command actually proposed/issued |
| Missing required metadata under experiment success policy | Generated brief lacks `weakness_type` even though the validator treats it as non-blocking under D2 | Treat as Stage 1 non-success under this package's own success bar (§12), even though the validator itself does not block | Preserve brief + validator output |
| Owner authorization block incomplete | §13's "Owner authorization" subsection contains any blank required field | Stop before invocation | N/A -- execution never begins |

For every hard stop: stop immediately; preserve all evidence; do not patch;
do not edit the generated brief; do not rerun; return to the owner.

## 12. Success definition

This second run succeeds only if **all** of the following hold:

1. Framework SHA exactly `1098acfd614e497bdf551040d3b1dee30afb9834`.
2. Target SHA exactly `b40db654e0df9e90074f7ad85b40d7362378e07d`.
3. Requested model exactly `claude-sonnet-5` (`requested_model ==
   "claude-sonnet-5"`).
4. Reported model exactly matches (`reported_models == ["claude-sonnet-5"]`,
   `model_match == true`; repeated identical reported values may be
   de-duplicated, but no other value may appear).
5. No fallback (`fallback_model` never set; none observed in logs).
6. No retry (`query()`/the transport invoked at most once).
7. Structural Stage A validation passes (§9 = PASS) via the authoritative
   `validate-and-report.py` invocation with both `--repo-root` and
   `--target-repo` set.
8. No duplicate `weakness_type` key (integrated safeguard reports no
   `DUPLICATE_WEAKNESS_TYPE_KEYS`, `MALFORMED_HANDOFF_FENCE`,
   `MISSING_HANDOFF_SECTION`, `MISSING_HANDOFF_BLOCK`, or
   `HANDOFF_YAML_PARSE_ERROR`).
9. Deterministic quote grounding (no `EVIDENCE_QUOTE_NOT_FOUND`) — the exact
   structural failure class Evidence 0013 hit.
10. No target mutation (§8 all checks clean).
11. Complete logs and trace present (`tool-call-trace.jsonl`, `run_log_*.md`,
    `workflow_summary.json`, `validation_run_log.md`).
12. Substantive review passes (§10 all sections satisfactory).
13. Every high-risk claim is Confirmed (none Rejected or Inconclusive).
14. Human reviewer judges the brief useful enough to justify considering
    Stage 2.
15. **Required metadata present under this package's experiment success
    policy**: the generated brief contains a `weakness_type` key. Note the
    distinction from validator policy: `validate-brief.py` treats a missing
    `weakness_type` as **non-blocking** under ratified D2 (a validator
    exits clean without it) — but this package's own experiment success bar
    is stricter than the validator's minimum: a brief missing that metadata
    does not count as Stage 1 success for this experiment, even though the
    validator alone would not have blocked it. This preserves D2 while
    keeping the experiment's own evidence bar high.

**Success would prove only** that this pinned Stage A repository-sensemaking
brief, on this pinned `auteur` revision, with this exact remediated
framework and model, passed structural validation, passed the high-risk
substantive audit, preserved target safety, and was judged useful under this
package's review standard.

**It would not, by itself, prove**:

- D8 satisfaction;
- cross-repository generality (positive or negative);
- production readiness;
- autonomous trustworthiness;
- architectural-review workflow Step 2;
- Stage 2 authorization (Stage 2 remains conditional on separate, explicit
  owner review of this run's actual evidence after it runs);
- real-maintainer usefulness beyond this one reviewer's judgment on this one
  target.

Current achieved readiness remains **"Externally exercised"** until actual
new evidence justifies a later, separate owner decision to change it.

## 13. Owner authorization block

### Proposed configuration (reviewed values, not an approval)

```text
Stage 1 second-run execution authorization status = NOT AUTHORIZED

Former blocking prerequisite: explicit model selection and executor
  enforcement = RESOLVED by PR #87 (§3a)
First-run result: STAGE 1 FAIL (Evidence 0013, PR #88) -- see §1a
Remediation applied since first run: PR #91, PR #92, PR #94 -- see §1b

Proposed framework SHA: 1098acfd614e497bdf551040d3b1dee30afb9834
Proposed target SHA: b40db654e0df9e90074f7ad85b40d7362378e07d
Proposed provider/model: Anthropic via Claude Agent SDK, claude-sonnet-5
Proposed environment: see §4 (fixed/inherited/unknown breakdown)
Proposed command: see §6, step 5 (below the execution boundary)
```

This "proposed configuration" block reflects the values reviewed and
recorded elsewhere in this package. It is not an authorization. Only the
block below, filled in and dated by the owner, authorizes execution.

**DO NOT EXECUTE unless this block has been completed through a separate,
explicit owner instruction after this package revision is merged and
reviewed.** Do not infer authorization from chat history surrounding the
first run: the authorization that covered Evidence 0013's single invocation
was consumed by that run and does not carry forward to a second run. Any
future authorization covers exactly one invocation; no automatic retry,
repair, or rerun would be permitted even after it is granted.

### Owner authorization (blank — no approval pre-filled)

```text
Owner authorization decision:
Authorized by:
Authorization date/time:
Authorized framework SHA:
Authorized target SHA:
Authorized model:
Authorized invocation count:
Special conditions:
```

This block is intentionally blank. No signature, date, approval token,
checkmark, or wording that could be read as authorization has been added.
The technical model-enforcement prerequisite is resolved (§3a, PR #87), but
Stage 1 second-run execution still requires a separate, explicit owner
instruction filling in and dating the block above. Merging the documentation
PR that carries this revision approves this package as an accurate,
up-to-date planning artifact; it does not fill in this block and does not
authorize execution.
