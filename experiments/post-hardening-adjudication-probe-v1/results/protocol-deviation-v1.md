# Protocol deviation v1 - Task D executed as agent analysis

```
schema: post-hardening-adjudication-probe-v1/protocol-deviation-v1
date: 2026-08-07
status: RECORDED - supersedes the original blinded human-adjudication protocol for this run
```

## Original protocol (probe-design-v1.md)

Independent human adjudication: the owner (or a second human) reads each of 16 blinded
packets (fixture + brief-A + brief-B) and answers Q1-Q6; sealed-key.yaml stays closed
until all 16 are judged; precommitted decision thresholds (probe-design-v1.md section 6)
map the outcome to a next action. The human is the measurement instrument; the agent must
not decide "candidate is more useful" on the owner's behalf.

## Deviation (owner-directed)

The owner stated they could not analyze the briefs and directed: "weaken the task or
claim and analyse it for me", then selected mode: agent analyzes all 16 packets; owner
reviews the final report. Recorded requirements:

- Evidence classification: AGENT ANALYSIS ONLY. Non-independent. The analyst (and the
  executing model) know the treatment identities (built the sealed key) and have prior
  exposure to the hardening evidence and ground truth.
- The result must NOT be described as human adjudication, owner ratification, blinded
  evaluation, or resolution of the original experimental claim.
- The original precommitted human-adjudication thresholds are NOT treated as satisfied.
- This run is used only to decide (a) whether another independent review is worth the
  cost and (b) the cheapest next action.
- No repo-sensemaker implementation change.

## Execution notes

- Per-packet merit reads were performed by four blind subagents (identity-ignorant; they
  saw only fixture/ + brief-A.md + brief-B.md and were explicitly barred from
  sealed-key.yaml, ground truth, phase15/18/19 artifacts, and the decision probe docs).
  Their verdicts are the least contaminated data in this run.
- Aggregation, identity mapping, fog interpretation, and the robust/vulnerable split were
  done by the main analyst (contaminated by construction).
- The sealed key was opened by the analyst for the identity mapping; it is reproduced in
  analysis-v1.md. The original blinded human protocol remains available to run later with
  a fresh key if an independent reviewer is funded.

## Resulting artifact

analysis-v1.md (per-packet table + aggregate + recommendation). This deviation note must
be read before interpreting it.