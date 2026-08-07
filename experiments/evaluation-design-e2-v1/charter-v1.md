# E2 charter v1 - decision-materiality detector experiment

```
schema: evaluation-design-e2-v1/charter-v1
experiment: E2 - can routing/action delta reliably identify cases where two briefs
  would lead to materially different engineering decisions?
branch: experiments/evaluation-design-e2-v1 (from origin/main @ 3bdfb8f, E1 merged)
status: MANUAL MEASUREMENT EXPERIMENT - no code, no scorer, no implementation
date: 2026-08-07
inputs: 16 Task-D packet pairs (frozen) + Task-D material/cosmetic judgments
  (clearly labeled non-human evidence). No fresh sealed key - this is not a blinded
  preference experiment.
```

## Question

Can routing/action delta (mechanically observable differences between two briefs)
reliably identify cases where two briefs would lead to materially different
engineering decisions?

This is NOT the question "can routing/action disagreement replace label-match
accuracy" and it is NOT "which brief is better". Routing/action delta is tested
only as a MATERIALITY DETECTOR: a cheap trigger that says "these two diagnoses
would cause different work; adjudicate direction/quality here", vs "the
difference is cosmetic; do not over-penalize".

## Definitions (mechanical, from the frozen briefs)

- `routing_delta = recommended_workflow_id differs OR recommended_execution_mode
  differs` (extracted from each brief's Section-13 handoff).
- `action_delta = normalized first engineering action differs materially`
  (extracted from each brief's Section-11 recommended next step; categories in
  delta-matrix-v1.md; normalization judgment calls are recorded, not hidden).
- `decision_delta = routing_delta OR action_delta`.

Reference classification: Task-D material/cosmetic judgments (blind subagent,
non-human) - the thing decision_delta is tested against.

## Constraints

- Use only the existing 16 frozen A/B pairs.
- No skill, scorer, corpus, ground-truth, validator, workflow-registry, or prior
  Task C/D/E artifact changes.
- Do NOT judge which brief is better. E2 tests the detector, not the candidates.
- No push, PR, scorer change, skill change, corpus change, or implementation.
- Stop after committing the E2 evidence package locally.

## Outputs (this directory)

- charter-v1.md (this file)
- delta-matrix-v1.md
- assessment-v1.md
- final-decision-v1.md

## Decision rule (final-decision-v1.md)

Choose one of:

- USE_AS_TRIAGE_SIGNAL - decision_delta reliably separates material from cosmetic
  disagreement and is a useful trigger for targeted adjudication;
- INSUFFICIENT - the 16 cases cannot discriminate;
- REJECT - decision_delta does not track materiality.

If USE_AS_TRIAGE_SIGNAL, propose a minimal evaluation architecture
(evidence validity -> decision-delta detection -> targeted adjudication) with exact
weakness-label accuracy retained only as a diagnostic. Do not implement it.