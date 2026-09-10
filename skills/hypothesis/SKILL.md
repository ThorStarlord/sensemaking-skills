---
name: hypothesis
description: Turn a product opportunity or proposed change into a falsifiable product hypothesis with target user, expected behavior, success and guardrail measures, risk assumptions, validation approach, and kill criteria. Use when the active agent has a product-hypothesis responsibility and needs a testable bet before implementation. Produce hypothesis_statement and never treat a validation plan as experiment evidence.
---

# Hypothesis

Satisfy a `product_hypothesis` responsibility by producing `hypothesis_statement`.

## Inputs

Require a target user/segment, an opportunity/problem, and a proposed intervention or belief to test. Prefer an `opportunity_map` and relevant evidence when available.

## Procedure

1. Read [references/methodology.md](references/methodology.md).
2. Express one falsifiable belief linking intervention, target, expected user behavior/outcome, measure, and decision horizon.
3. Separate user behavior from internal business metric where possible.
4. Define a primary measure plus secondary or guardrail measures only when useful and observable.
5. Identify consequential assumptions across value, usability, viability, and feasibility.
6. Define a bounded validation approach and explicit success, pivot, and kill criteria before results exist.
7. Cite supporting evidence and label unsupported premises as assumptions.
8. Render [references/output-contract.md](references/output-contract.md) and return control.

## Stop or downgrade

- If success cannot be falsified under any result, rewrite the hypothesis before returning it.
- If baseline or target values are unknown, keep them unknown or explicitly proposed; do not present invented numbers as observations.
- Do not claim the hypothesis passed or failed without actual experiment or operational evidence.
- Do not launch the test without separate external-action authority when the test changes external state.

## Boundary

`hypothesis card != experiment result`, and `validation approach != validation evidence`.
