# Final decision v1 - E1 outcome

```
schema: evaluation-design-e1-v1/final-decision-v1
status: DECISION RECORDED - evidence package only. No push, PR, scorer change, or
  implementation follows. Next decision is separate.
```

## Decision

**DEMOTE.**

Exact `weakest_boundary_accuracy` (weakness-type label match vs frozen ground
truth) should be kept as a diagnostic/submetric - label drift, taxonomy hygiene,
first-task sensitivity - but it is NOT a reliable primary quality gate for
repo-sensemaker. Evidence (metric-assessment-v1.md):

- 5 of the 8 regressions it flagged in this sample are false positives (cosmetic:
  same engineering work, both labels defensible);
- 4 false-negative cases where it reported equality (or both-wrong) while the
  briefs drive materially different work via fog/routing;
- its reference standard (frozen gt) is contested in roughly half the sample;
- its only genuinely useful signal (3 label-matters cases) is partly redundant
  with routing consequence and cannot express direction.

This is NOT a verdict that the hardened candidate was better or worse - the Task-D
analysis explicitly does not support either direction, and agent preference is not
human evidence. DEMOTE is a verdict about the metric, not about the candidate.

## Replacement hypothesis (proposed, NOT selected for implementation)

**REPLACE-HYPOTHESIS candidate:** a routing-consequence outcome carries more
decision-relevant signal than exact label match - in this sample 7 packets differ
in routing (workflow id and/or execution mode), and 5 of the 7 material cases are
routing-driven. A primary outcome such as "diagnosis-to-workflow disagreement
rate" or a categorical decision-materiality outcome (cosmetic vs material, with
the first task named) should be tested as the successor metric. This is a
hypothesis to test, not an adopted replacement.

## Smallest next experiment to test the replacement (do not implement now)

**E2 proposal - routing/action delta table (artifact-only, no code):**

- Inputs: the existing frozen briefs for the 25-repo corpus (baseline/ and
  candidate/ on the closed hardening branch) - or the 16 packet pairs already on
  main if the narrower scope is preferred.
- Method: for each pair, extract from the Section-13 handoff `recommended_workflow_id`
  + `recommended_execution_mode`, and categorize the recommended first action
  (from Section 11/14) into a small fixed set of action categories. Produce a
  delta table: how many pairs differ in (a) workflow, (b) mode, (c) first-action
  category, (d) only label.
- Deliverable: a comparison of "routing/action disagreement rate" vs the frozen
  label-match rate on the same pairs, showing whether the routing signal separates
  the material cases from the cosmetic ones better than the label metric.
- Cost: one manual pass over 25 (or 16) brief pairs; no new scorer, no validator,
  no skill change. A human reviewer can do the action-category coding in ~2-4 h.

Only if E2 shows the routing/action signal cleanly separates material from
cosmetic disagreement would a replacement primary metric be worth designing - as a
separate, charter-authorized experiment.

## Explicit non-authorizations

- No replacement scorer is designed or implemented.
- No repo-sensemaker skill/validator/runtime/workflow/scorer/corpus change.
- No salvage or merge of the hardened candidate is implied by DEMOTE.
- No push or PR of this package. The next decision (run E2, fund a human review,
  or stop) is made separately from this evidence package.