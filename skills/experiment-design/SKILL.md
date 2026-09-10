---
name: experiment-design
description: Design a bounded product experiment from a testable hypothesis, riskiest assumption, target population, method, exposure/sample plan, primary and guardrail metrics, preregistered decision thresholds, kill criteria, analysis plan, and authority needs. Use for experimentation responsibility and produce experiment_plan. A design is not evidence that an experiment ran or succeeded; never invent sample size, baseline, budget, dates, traffic, or approval.
---

# Experiment design

Satisfy an `experimentation` responsibility by producing `experiment_plan`.

## Inputs

Require a testable product hypothesis and target population/context. Prefer `hypothesis_statement` plus known baselines, traffic, constraints, and evidence. External experiment execution remains separately authorized.

## Procedure

1. Read [references/contract.md](references/contract.md).
2. Identify the riskiest assumption and select a method appropriate to the product stage (for example pretotype, prototype/usability study, or controlled experiment).
3. Define the intervention/exposure and inclusion/exclusion rules.
4. Define one primary decision metric plus relevant guardrails.
5. Preserve baseline, sample-size, duration, budget, and traffic as known, estimated, proposed, or unknown according to evidence.
6. Preregister decision thresholds and kill/integrity criteria before observing results.
7. Define analysis method, evidence capture, owner/authority dependencies, and follow-up branches.
8. Return `experiment_plan` and control. Do not execute the experiment.

## Boundary

`experiment plan != experiment evidence`, `proposed sample != observed sample`, `decision threshold != result`, and `plan approval != external execution authority`.
