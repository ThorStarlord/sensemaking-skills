# Semantic usefulness evaluation protocol

Semantic Architecture usefulness is an empirical claim, not a consequence of
mechanical conformance. This protocol defines the minimum study required
before changing the claim from `deferred`.

## Design

Compare two conditions on the same bounded repository tasks:

1. baseline: the agent works without Semantic Architecture assistance;
2. treatment: the agent may use semantic observations, maps, and provenance.

Freeze the task set, agent/model configuration, repository commit, and scoring
rubric before collecting results. Use multiple independent episodes and retain
the raw transcripts, generated artifacts, and evaluator decisions.

## Measures

Record at least:

- time to reconstruct prior work;
- repeated investigation count;
- unsupported-claim count;
- artifact reconstruction success;
- handoff completeness;
- reviewer-rated decision quality.

Report sample size, exclusions, failures, and uncertainty. A passing validator
is not a treatment success. The claim may be promoted only when the predefined
comparison shows a meaningful improvement and an independent reviewer accepts
the evidence package.
