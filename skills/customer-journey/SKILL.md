---
name: customer-journey
description: Map a bounded customer journey for a named persona or segment across relevant stages, touchpoints, actions, questions, emotions, pain points, opportunities, and critical moments while preserving evidence status. Use for customer_understanding responsibility and produce journey_map. Do not invent conversion rates, churn triggers, emotions, touchpoints, frequency, or Aha Moments; unsupported journey claims remain hypotheses.
---

# Customer journey

Satisfy a `customer_understanding` responsibility by producing `journey_map`.

## Inputs

Require a named persona/segment, product/service, and journey scope. Prefer durable persona, interview, analytics, support, funnel, retention, and touchpoint evidence when available.

## Procedure

1. Read [references/contract.md](references/contract.md).
2. Choose only the stages warranted by the scoped journey. The upstream Awareness-to-Advocacy seven-stage sequence is a useful heuristic, not a mandatory ontology.
3. For each stage, record touchpoints, actions, questions/thoughts, emotions, pain points, opportunities, and any observed metrics with evidence status and refs.
4. Identify possible `aha`, `moment_of_truth`, and `churn_trigger` moments only at the evidence strength actually supported.
5. Distinguish observations from interview inference and product-team hypothesis.
6. Recommend investigation/improvement opportunities without inventing impact or effort values.
7. Return `journey_map` and control.

## Boundary

`journey hypothesis != observed behavior`, `emotion guess != customer evidence`, `critical moment hypothesis != causal churn evidence`, and `journey recommendation != roadmap priority`.
