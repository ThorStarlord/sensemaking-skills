# Task P2 — Assisted-Baseline Decision-Sharpening Probe (Charter v1)

experiment_type: product_interaction
record: charter-v1
recorded_at: 2026-08-08 03:05:37 -03:00 (freeze time, PHASE 0)
status: FROZEN — one-shot, no reruns, no repairs
branch: experiments/product-interaction-p2-v1 (fresh, from canonical origin/main)
owner: ThorStarlord (repository owner)

---

## Purpose

Run a lightweight product-discovery experiment to test whether the current
canonical `repo-sensemaker` helps the owner reach a useful engineering
decision. This is a product-value / interaction experiment, NOT an
implementation task, validator repair, hardening-v2, synthetic evaluation,
scorer design, installation/distribution experiment, or Task P3.

## Target decision

> "After P1, should the standalone repo-sensemaker validation failure become
> the next engineering task, or is there higher-value product work to do
> first?"

## Evidence claim (weakened, deliberately below P1)

P2 does NOT measure an independently captured PRE->POST decision delta. P2 may
support a claim of the form:

"Given an existing real owner question and the documented context available
before investigation, repo-sensemaker produced a recommendation that the owner
judged useful, decision-relevant, or action-sharpening."

There is deliberately NO `OWNER_PRE` artifact. The baseline is an
`ASSISTED_BASELINE` reconstructed from previously documented owner context
(P1 evidence + this prompt). It must never be labeled `OWNER_PRE` and must not
be used to claim a clean PRE->POST delta.

## One-shot constraints

- Exactly ONE canonical, read-only `repo-sensemaker` interaction.
- Canonical in-repository skill from `origin/main` only (no hardening
  candidate, no stale global copy, no unmerged repair branch, no experimental
  version).
- No implementation. No validator change. No skill/prompt/template change.
- Standalone validation, if part of the canonical normal execution path, runs
  exactly ONCE; failure is preserved as evidence (no repair, no rerun).
- PHASE 0 boundary: before the assisted baseline is frozen, no inspection of
  validator implementation, validator failure mechanics, validator branches,
  validator issues, validator commit history, validator PRs, candidate fixes,
  relevant tests, or detailed code associated with the target decision.
- After presenting `owner-synthesis-v1.md`, stop and ask the owner ONLY the
  three lightweight POST questions. Record the answer faithfully; do not
  reinterpret it.

## Prohibited work (hard stop)

Do not: fix the standalone validator; change repo-sensemaker or its
prompt/template; salvage the frozen hardening candidate; modify evaluation
metrics; implement `decision_delta`; start another hardening cycle; start Task
P3; start the installation-solution comparison; publish or repair PyPI; touch
the v0.2.2 release/tag situation; modify EXP-0002; merge unrelated work; or
perform repairs merely because P2 exposes a defect. If P2 identifies a
promising next action, record it as a proposed follow-up probe — do not
execute it.

Do not create: a P2 numeric scorer, aggregate P1/P2 metric, new schema,
experiment-artifact validator, campaign machinery, or authorization machinery.
Two product interactions are not a dataset.

## Frozen identities (PHASE 0, from canonical origin/main)

- Target repository: `sensemaking-skills` (origin: `https://github.com/ThorStarlord/sensemaking-skills.git`)
- Canonical SHA (origin/main): `e2e859b60c255c5b02ea74083cfca94db28601d0`
- Canonical repo-sensemaker skill path: `skills/repo-sensemaker/SKILL.md`
  (plus its `references/` tree: evidence-rules.md, repo-analysis-template.md,
  ui-fog-signals.md, weakness-types.md)
- Canonical skill-file blob SHA (SKILL.md): `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3`
- Note: root-level `repo-sensemaker/` contains only a legacy `references/`
  copy; the canonical skill lives under `skills/`.
- Owner question (exact): "After P1, should the standalone repo-sensemaker
  validation failure become the next engineering task, or is there
  higher-value product work to do first?"
- Execution mode: fresh interactive coding-agent session (Reasonix on
  Windows/PowerShell), owner present, one-shot interaction, read-only wrt
  product code.
- Timestamp (freeze): 2026-08-08 03:05:37 -03:00

## Expected artifacts (experiments/product-interaction-p2-v1/)

1. charter-v1.md (this file)
2. assisted-baseline-v1.md
3. repo-sensemaker-investigation-v1.md
4. owner-synthesis-v1.md
5. owner-post-v1.md (only after owner's POST judgment)
6. learning-v1.md
7. validation-result-v1.json (only if canonical standalone validation is part
   of the normal execution path)

## Repository discipline

Only files under `experiments/product-interaction-p2-v1/**` are added/changed
for the P2 evidence package. No product/source file changes. Pre-existing
working-tree noise (modified `src/sensemaking_skills.egg-info/PKG-INFO`,
untracked `.reasonix/`) is left untouched and uncommitted.
