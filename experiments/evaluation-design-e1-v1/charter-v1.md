# E1 charter v1 - evaluation-design experiment

```
schema: evaluation-design-e1-v1/charter-v1
experiment: E1 - does weakest_boundary_accuracy track decision quality?
branch: experiments/evaluation-design-e1-v1 (from origin/main @ 40d4631)
status: MANUAL MEASUREMENT-DESIGN EXPERIMENT - no code, no scorer, no implementation
date: 2026-08-07
inputs: 16 Task-D packet pairs + preserved Task-D analysis (see below)
```

## Question

Does the frozen `weakest_boundary_accuracy` metric (exact weakness-type label match
vs the frozen generator-authored ground truth) track the repository-sensemaking
outcome we actually care about -- decision quality -- or does it over-penalize
harmless label disagreement and miss consequential routing/action differences?

The question is deliberately NOT "which brief wins?" It is a measurement-validity
question about the metric used to judge the hardening experiment.

## Inputs (only these; nothing else is read or modified)

1. `experiments/post-hardening-adjudication-probe-v1/packets/**` - the 16 Task-D
   packet pairs (fixture + baseline brief + candidate brief; A/B identities known
   from sealed-key.yaml, reproduced in case-matrix-v1.md).
2. `experiments/post-hardening-adjudication-probe-v1/results/analysis-v1.md` and
   `.../protocol-deviation-v1.md` - the preserved Task-D agent analysis. All Task-D
   contamination limits apply: agent preference is NOT human ground truth; the
   analysis is non-independent with known identities.

## Non-goals and hard constraints

- Do NOT modify `repo-sensemaker`, validators, workflow registry, scorer, corpus,
  ground truth, or any prior Task C/D artifact.
- Do NOT design or implement a replacement scorer. The deliverable is a measurement
  argument, not code.
- No push, PR, scorer change, or implementation follows from this package.
- Stop after committing the E1 evidence package locally.

## Method

Manual categorical judgment per A/B pair over six decision-quality dimensions
(defined in decision-quality-rubric-v1.md). No invented weighted score. Each
dimension gets a categorical value; cells cite their evidence basis (Task-D blind
subagent verdict vs analyst read) where it matters. Task-D blind-agent preference
appears in the matrix only as secondary, clearly-labeled non-human evidence.

## Outputs (this directory)

- charter-v1.md (this file)
- decision-quality-rubric-v1.md
- case-matrix-v1.md
- metric-assessment-v1.md
- final-decision-v1.md

## Decision rule (final-decision-v1.md)

Choose exactly one of:

- KEEP - exact weakest-boundary accuracy meaningfully tracks decision quality;
- DEMOTE - keep exact label accuracy as a diagnostic/submetric, but not a primary
  quality gate;
- REPLACE-HYPOTHESIS - evidence strongly suggests a different primary outcome should
  be tested next;
- UNRESOLVED - the existing 16 cases cannot discriminate.

If DEMOTE or REPLACE-HYPOTHESIS, propose the SMALLEST next experiment needed to test
a replacement metric. Do not implement it.