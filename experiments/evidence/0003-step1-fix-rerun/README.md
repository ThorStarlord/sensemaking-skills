# Live Step 1 rerun after the prompt-hardening fix (issue #53)

## Purpose

After the prompt/template/guidance changes in this branch
(`fix/repo-sensemaker-live-contract`, commit `d412382`), execute exactly ONE
live `repo-sensemaker` Step 1 attempt against a disposable checkout, using the
real `claude-code` executor, to determine whether the fix resolves the
failure recorded in PR #52 / issue #51.

## Exact command

```
python scripts/workflow-runtime.py "Analyze this repository's workflow-runtime architecture, identify the weakest boundary affecting reliable evidence-backed orchestration, and recommend the smallest architectural improvement supported by repository evidence." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --gate-decision auto-approve \
  --executor claude-code \
  --target-repo <disposable-target-0003 checkout of origin/main @ dd8b3e2> \
  --log-dir <scratch log dir>
```

Framework root: this worktree, on `fix/repo-sensemaker-live-contract` at
commit `d412382`.

Target: a disposable `git worktree add --detach origin/main` checkout
(HEAD `dd8b3e2`), created fresh for this run, located outside the framework
repository tree.

## Exit code

Overall orchestrator exit code: 1 (`Status: failed`, `Steps: 0/2`, `Errors: 1`).
See `stage1_stdout.txt` for full stdout/stderr.

## What happened

Step 1 (`repo-sensemaker`) executed live via the real `claude-code` executor
(`ClaudeAgentSdkSkillExecutor`) and produced
`session/repository_sensemaking_brief.md`, but `validate-and-report.py`
rejected it:

```
unknown.artifact_id.missing_field: Cannot determine artifact_id from file. Generic validator requires artifact_id ...
```

Execution halted before Step 2 (`architectural-review`) was ever attempted.

## Result classification: NEW CONTRACT FAILURE

This is **not** a repeat of the three defects diagnosed in issue #53 (no
`HALLUCINATED_WORKFLOW_ID`, no `INVALID_LINE_FORMAT` errors this time), but
it is also not a pass. Inspecting the generated brief
(`session/repository_sensemaking_brief.md`) shows the model:

- Did **not** use the required `repo-analysis-template.md` section structure
  or headings at all (its own custom sections: "Executive Summary", "Project
  Type & Domain", etc., not "1. Repository goal" / "6. Weakest boundary" /
  "13. Machine-readable handoff").
- Contains **no fenced `yaml` block at all** for the machine-readable handoff
  (only two unrelated plain fenced blocks appear in the whole file), so there
  is no `artifact_id`, no `recommended_workflow_id`, nothing for the
  validator to parse — hence the generic-validator fallback error instead of
  the specific brief-validator errors seen in PR #52.
- Opens with `**Status**: Production Ready (Phase 4 Complete)` and restates
  historical/self-reported milestone claims (e.g. "Beta (v0.2.1), but
  Production-Ready ... following completion of Phase 4 testing") as
  present-tense fact at the very top of the document -- exactly the
  stale-authority failure mode Defect 3 was meant to prevent, still occurring
  despite the new Evidence Authority Hierarchy section in SKILL.md.

## Honest assessment

The three specific error signatures from PR #52 did not reproduce, so the
identifier-rules and evidence-line-grammar guidance may well be effective --
but this run does not exercise them, because the model didn't reach the point
of populating those fields at all. The deeper problem this run surfaces: the
live model is not reliably being made to follow
`repo-analysis-template.md`'s literal structure (including the required
machine-readable block) via the current skill-loading path, and continues to
treat historical status documents as current fact even with the new authority
hierarchy present in SKILL.md. This is a genuine, different live-contract
failure, not a success -- reported as-is, per instructions, without manual
repair of the generated artifact.

## Target immutability

`git status --short` in the disposable target checkout: empty both before
and after the run (confirmed).

## Framework pollution

`git status --short` in the framework worktree after the run showed only:
- `artifacts/05-orchestration-run/` (new session artifacts -- expected)
- `docs/mode-coverage.yaml` (run-tracking file, updated by design)

No other framework files were modified. `_tmp_evidence_0003/` (this run's
`--log-dir` target) has been copied into this `experiments/evidence/` folder
and the temp directory removed.

## Files in this evidence folder

- `stage1_stdout.txt` -- exact stdout/stderr of the orchestrator run.
- `diagnostic_architectural-review-planning-workflow_guided_execution.md`
- `implementation_architectural-review-planning-workflow_guided_execution.md`
- `run_log_architectural-review-planning-workflow_guided_execution.md`
- `validation_run_log.md`
- `workflow_summary.json`
- `session/00-user-intent.md`
- `session/plan_architectural-review-planning-workflow.md`
- `session/repository_sensemaking_brief.md` (the live-generated, failing brief)
- `session/run-ledger.jsonl`

## Consequence for Step 2 / golden path

Step 2 (`architectural-review`) was never invoked and remains unproven. A
full golden-path rerun (Step 1 + Step 2) is **not** justified until Step 1
reliably produces a validator-passing brief -- this run demonstrates it does
not yet.
