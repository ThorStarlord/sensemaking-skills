# Evidence 0013: Stage 1 controlled auteur run (owner-authorized, PR #87 model enforcement)

**Run date**: 2026-07-26/27 (UTC). **Result: STAGE 1 FAIL.**

## Authorization

Owner (in chat) explicitly authorized exactly one Stage 1 `repo-sensemaker`
Stage A controlled-experiment run per
`docs/experiments/STAGE-1-AUTEUR-EXECUTION-PACKAGE.md` at
`main@6846ed03ba6f3a26d8c25a04e7f5caf1e25563fa`, pinning framework SHA
`68b44835be43b86ee7c0d7eb968e67efcd368443`, target SHA
`b40db654e0df9e90074f7ad85b40d7362378e07d`, historical evidence commit
`a328c80`, and model `claude-sonnet-5` via the Claude Agent SDK.

## Preflight (all passed)

- Framework commit `68b44835be43b86ee7c0d7eb968e67efcd368443`: confirmed via `gh api .../commits/...`.
- Target commit `b40db654e0df9e90074f7ad85b40d7362378e07d`: confirmed present in the local `auteur` repository (used as the clone source; no GitHub remote exists for this private target).
- Historical evidence commit `a328c80` (`origin/evidence/auteur-campaign-final-rerun`): confirmed reachable (`git show`, `git merge-base --is-ancestor` both exit 0). PR #78 confirmed OPEN/unmerged.
- Issue #83: confirmed OPEN.
- PR #78: confirmed untouched (open, unmerged, not modified by this run).
- Fresh disposable clones created at `H:\scratch\stage1-auteur-rerun\{framework,target-auteur}`, outside `.claude/worktrees/`, both working trees clean before the run.
- `python scripts/validate-repo.py` and `python scripts/test-validators.py`: both PASS in the framework clone.
- `scripts/workflow-runtime.py` confirmed to contain the `--model`/`--controlled-experiment` enforcement (lines ~228, 1312-1314, 2985-3005) from merged PR #87.
- Environment: Python 3.14.3, Git 2.51.0.windows.1, `claude-agent-sdk` 0.2.82, Claude Code CLI 2.1.101.

## Execution boundary and invocation

Printed the required `EXECUTION BOUNDARY` banner, then invoked exactly once:

```
python scripts\workflow-runtime.py "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." --workflow architectural-review-planning-workflow --mode guided_execution --executor claude-code --controlled-experiment --model claude-sonnet-5 --gate-decision auto-approve --repo-root "H:/scratch/stage1-auteur-rerun/framework" --target-repo "H:/scratch/stage1-auteur-rerun/target-auteur" --log-dir "H:/scratch/stage1-auteur-rerun/logs"
```

Invocation count: **1**. No retry, no fallback, no second invocation of any kind.

## Model-enforcement check (PASS)

- `requested_model`: `claude-sonnet-5` (from the `--model` flag; process exited before any SDK call would have been possible without it, per PR #87's guard).
- `reported_model` (all `AssistantMessage` events in `tool-call-trace.jsonl`, schema_version 2): uniformly `"claude-sonnet-5"` (120 `AssistantMessage`-adjacent trace lines checked; single distinct value after de-duplication).
- `model_match`: true. No fallback observed (`fallback_model` never set/never appears in trace). No retry observed (`run_started`/`run_completed` each appear exactly once in `run-ledger.jsonl`).

## Target-mutation check (PASS — no mutation)

- Target HEAD before: `b40db654e0df9e90074f7ad85b40d7362378e07d`. Target HEAD after: identical.
- `git status --porcelain`, `git diff --exit-code`, `git diff --cached --exit-code`: all clean/empty before and after.
- `git ls-files` manifest before vs. after: identical (`diff` exit 0).
- Trace shows exactly one `PreToolUse` Write attempt directed at `target-auteur\...\repository_sensemaking_brief.md` (`invocation_id toolu_01CHh5CAejGpDAyo8bxXKExb`), with **no matching `PostToolUse` "completed" event** — the attempt was denied by the framework's target-confinement gate, not completed. The one completed Write (`toolu_018qWcbbjdDRDbiyFwiEt734`) targeted `framework\artifacts\...`, not the target repo.
- **Conclusion: attempted target write = yes; completed target write = no.** Target-mutation check passes.

## Structural validation (FAIL)

Corrected validator invocation (the first pass, in `validator-output.txt`, was run without `--target-repo` and incorrectly reported `HALLUCINATED_FILE` for real target files — an error in how I invoked the validator, not a defect in the brief; superseded by `validator-output-corrected.txt`, run with `--repo-root` and `--target-repo` both set):

```
python scripts/validate-and-report.py artifacts/05-orchestration-run/repository_sensemaking_brief.md --repo-root H:/scratch/stage1-auteur-rerun/framework --target-repo H:/scratch/stage1-auteur-rerun/target-auteur
```

Result: `"valid": false`, 3 blocking errors, all `EVIDENCE_QUOTE_NOT_FOUND`:

1. `src/auteur/decision/service.py` L1 — brief quotes `"""Decision workspace service -- compose real project state from subsystems."""`; actual file uses an em dash (`—`), not `--`. Verified by direct read of the target file.
2. `src/auteur/cli_parser.py` L419-L420 — brief's quote omits the actual file's leading 4-space indentation on the first line. Verified by direct read.
3. `CHANGELOG.md` L349-L362 — brief's quote drops the actual file's markdown bold/backtick formatting (`- **\`auteur decision status\`**:` vs. the brief's plain `- auteur decision status:`) and normalizes the em dash in the heading. Verified by direct read.

These are real quote-fidelity defects (paraphrasing/normalization during citation), not hallucinated files — all three cited files and line ranges exist in the target at the pinned SHA; the semantic content of each claim is directionally accurate, but the verbatim-quote contract is violated in all three excerpts.

Duplicate-`weakness_type` safeguard (`check_duplicate_weakness_type.py`): reported "no weakness_type key found" — this is a **script limitation**, not evidence of a missing/duplicate key: the brief's Section 8 contains a malformed doubled ` ```yaml ` fence (an inner ` ```yaml ` opened without closing the outer one, itself a structural defect in the generated brief), which defeated the script's non-greedy single-fence regex. Manual inspection confirms the real Section 13 handoff block contains exactly one `weakness_type: Vocabulary Drift` key. This malformed nested fence in Section 8 is itself noted as an additional, secondary structural defect in the generated brief, separate from the quote-grounding failures.

**Structural result: FAIL** (blocking `EVIDENCE_QUOTE_NOT_FOUND` errors present). Per the package's own rules (§7/§9), a FAIL stops the experiment before substantive human review.

## Substantive human review

**Not performed.** Per the merged execution package (§9/§12) and the owner's task instructions, substantive review is gated on structural PASS. Structural result is FAIL, so Stage 1 stops here; substantive review was not conducted.

## Final Stage 1 classification

```
STAGE 1 FAIL
```

This proves only that this one controlled run, under this exact pinned
configuration and enforced model, produced a brief with blocking
quote-grounding failures. It does **not** prove:
- that the PR #81 contract redesign is broken in general;
- cross-repository generality (positive or negative);
- production readiness;
- autonomous trustworthiness;
- real-maintainer usefulness;
- anything about D8 or Stage 2 authorization.

No repair, no re-run, and no second invocation occurred or is authorized by
this evidence record.

## Evidence preserved (this directory)

- `repository_sensemaking_brief.md` — the generated brief, unedited.
- `tool-call-trace.jsonl`, `run-ledger.jsonl` — complete trace/ledger.
- `stdout.log` — full run stdout (stderr was empty).
- `run_log.md`, `workflow_summary.json`, `plan.md` — run log / machine summary / plan.
- `validator-output.txt` — first (incorrectly-invoked) validator run, kept for transparency.
- `validator-output-corrected.txt` — corrected validator run (authoritative structural result).
- `check_duplicate_weakness_type.py` — the package's Part 7 script, and its output above.
- `target-manifest-pre.txt` / `target-manifest-post.txt` — target `git ls-files` before/after (identical).
