# Decision-quality rubric v1

```
schema: evaluation-design-e1-v1/decision-quality-rubric-v1
purpose: categorical definitions for judging whether an A/B brief difference is a
  decision-quality difference, and whether the frozen metric captures it.
basis: Task-D blind subagent verdicts + workflow/mode extraction from packet
  Section-13 handoffs + analyst reads. No weighted scoring.
```

## Metric under test

`weakest_boundary_accuracy` = fraction of repositories where the brief's
`weakness_type` equals the frozen ground-truth `weakness_type`. A candidate label
that differs from ground truth counts as REGRESSED even if the baseline also
differed or if the alternative label is defensible. Fog classification and routing
are tracked separately (fog was "tracked, not gated"; routing validity was a
separate gate). This rubric asks whether that exact-label comparison is a useful
proxy for decision quality.

## Outcome classes (used in case-matrix-v1.md)

- **FP (false-positive regression candidate):** the metric flags the candidate as
  regressed, but both diagnoses are defensible (or partially defensible) AND lead to
  materially the same engineering work.
- **FN (false-negative candidate):** the metric reports equal/correct (or no
  regression), while the two briefs would produce materially different or worse
  engineering decisions (typically via fog/routing, which the metric does not read).
- **GT-ambiguous:** the frozen ground-truth label itself appears questionable for
  this fixture (blind agent or both briefs disagree with it for well-reasoned
  grounds).
- **Label-matters:** exact weakness-label agreement genuinely changes the first
  engineering task or the workflow (the metric has real signal here).
- **clean:** metric verdict and decision-quality verdict agree.

## Six decision-quality dimensions (categorical)

For each A/B pair, assess each dimension with a categorical value; never sum or
weight them.

1. **Evidence defensibility** - are the important claims actually supported by
   repository evidence?
   Values: both-strong / both-adequate / A-stronger / B-stronger / one-weaker.
   Basis: Task-D blind reads of citation support and inference labeling.

2. **Boundary defensibility** - is the chosen weakest boundary a reasonable
   diagnosis of the fixture?
   Values per brief: defensible / partially / not defensible. Recorded as
   A/B pair (e.g. "defensible / partially").

3. **Decision materiality** - would A vs B change what engineering work happens
   next?
   Values: cosmetic (same practical next actions) / material (different first
   task, different deliverable, or different workflow) / cannot-tell.

4. **Routing consequence** - does the fog diagnosis (and the resulting workflow +
   execution mode) send work to a meaningfully different place?
   Values: same / WF (different workflow id) / MODE (same workflow, different
   execution mode: plan_only vs guided_execution).
   Basis: `recommended_workflow_id` + `recommended_execution_mode` extracted from
   each brief's Section-13 handoff.

5. **Action quality** - is the recommended next action appropriate to the observed
   repository problem?
   Values: equal / baseline-better / candidate-better. Basis: Task-D blind
   usefulness verdicts plus the concrete first-step each brief recommends.

6. **Uncertainty quality** - does the brief distinguish observed / inferred /
   unknown appropriately (labels its inferences, flags what it did not run)?
   Values: both-adequate / baseline-better / candidate-better. Basis: Task-D
   blind reads of inference labeling and epistemic care.

## How to read the matrix

The metric column ("metric verdict") is the ground-truth label-match result.
The material/routing/action columns are the decision-quality view. A case is a
false positive when the metric's verdict disagrees with the decision-quality view
in the direction of punishing a harmless label difference; a false negative when
the metric sees nothing while the decision-quality view sees a consequential
difference. Task-D blind preference is listed LAST and is non-human evidence only;
it never determines a class by itself.