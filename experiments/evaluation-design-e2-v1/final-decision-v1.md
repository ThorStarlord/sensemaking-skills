# Final decision v1 - E2 outcome

```
schema: evaluation-design-e2-v1/final-decision-v1
status: DECISION RECORDED - evidence package only. No push, PR, scorer change,
  skill change, corpus change, or implementation. Next decision is separate.
```

## Decision

**USE_AS_TRIAGE_SIGNAL.**

`decision_delta` (workflow/mode delta OR normalized first-action delta) reliably
identifies cases where two briefs would lead to materially different engineering
decisions on this 16-case sample: 7/7 material cases caught, 0 misses, 1 cosmetic
false flag (generated-heavy, workflow-name-only with identical action; 1-3 under
the recorded normalization judgment calls). Weakness-label disagreement adds no
decision-relevant information beyond decision_delta - it re-flags only the cosmetic
cases (the over-penalization mode) and misses exactly the same-label/routing-
differs cases that decision_delta catches.

This is a verdict about the DETECTOR, not about either candidate. No brief is
scored as better or worse anywhere in this package.

## What decision_delta is and is not

- It IS a materiality detector: "these two diagnoses would cause different work;
  adjudicate direction/quality here."
- It is NOT a quality metric: it cannot say which diagnosis is better. Direction
  and quality still require targeted adjudication (human or claim-level).
- It is NOT a replacement for evidence validity checks (a brief can be material
  and still wrong).

## Minimal evaluation architecture (proposal - not implemented)

```
brief (baseline or candidate)
  |
  v
evidence validity (existing validator + semantic checks: claims supported,
inference labeled)
  |
  v
decision-delta detection (mechanical: workflow/mode/first-action delta vs the
reference brief; refinement: do not fire on workflow-name-only deltas with
identical first-action category)
  |
  +-- no delta  -> taxonomy disagreement may be cosmetic; do not over-penalize
  |
  +-- delta     -> consequential case; targeted adjudication of direction/quality
                   (human review or claim-level evidence), then the decision
```

Exact weakness-label accuracy is retained ONLY as a diagnostic submetric (label
drift, taxonomy hygiene), not as the primary gate - consistent with the E1 DEMOTE
verdict.

## Smallest next experiment to harden the triage signal (E3 proposal - not implemented)

- Inputs: all 25 frozen baseline/candidate brief pairs on the closed hardening
  branch (no new corpus, no new runs).
- Method: mechanically extract workflow/mode (Section 13) and first-action category
  (Section 11) for all 25; code action categories with one human pass (~2-4 h);
  compute decision_delta; spot-check materiality with one human on ~6-8 pairs to
  remove the blind-subagent circularity from the reference.
- Deliverable: decision_delta catch/miss/false-flag rates on the full corpus with a
  human-coded reference; decides whether the triage architecture is worth
  formalizing.

## Explicit non-authorizations

- No scorer, skill, validator, runtime, workflow-registry, or corpus change.
- No judgment of which brief is better was made or is implied.
- No salvage/merge of the hardened candidate is implied by USE_AS_TRIAGE_SIGNAL.
- No push or PR of this package. The next decision (run E3, fund a human
  adjudication pass, or stop) is made separately.