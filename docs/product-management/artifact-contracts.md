# Product Management artifact contracts

## Authority

Concise human contracts live beside each canonical Skill in that Skill's `references/` directory. The canonical validation router selects specialized deterministic validators where PM machine-contract invariants add value.

Historical Wayfinder entries in `skills/workflow-planner/references/artifact-contracts.yaml` preserve compatibility/provenance. They do not become semantic authority merely because an identifier is reused.

## Customer Discovery routed identities

`scripts/validate-pm-artifact.py` validates `persona_definition`, `discovery_findings`, `synthesis_report`, `opportunity_map`, and `hypothesis_statement`.

It checks mechanically decidable representation/evidence-shape contracts and does not decide whether a persona, finding, opportunity, or hypothesis is strategically correct.

## Feature Definition routed identities

`scripts/validate-pm-feature-definition.py` validates `story_list`, `criteria_list`, and `risk_analysis`.

`story_list` preserves traceability/scope, `criteria_list` preserves specified behavior without claiming execution, and `risk_analysis` distinguishes observed/inferred/hypothetical risk from launch authority.

## PRD authority

`prd` remains produced by canonical `to-prd`. Upstream `prd` methodology is merged into that Skill; no second current `prd` capability exists.

## Strategy and Prioritization routed identities

`scripts/validate-pm-strategy.py` validates `market_analysis`, `strategy_doc`, `prioritized_list`, `north_star_metric`, `okr_list`, `roadmap`, and `business_canvas`.

It enforces source-backed observed market claims, proposed strategy/metric/OKR/roadmap states, declared RICE arithmetic, outcome-shaped KRs, authority evidence for committed roadmap timing, and hypothesis/evidence status for Lean Canvas. It does not choose strategy or rank work for the agent.

## Experimentation, PMF, and Pricing routed identities

`scripts/validate-pm-measurement.py` validates:

- `experiment_plan`
- `test_results`
- `pmf_report`
- `pricing_model`

### `experiment_plan`

The artifact is always `status: designed`, references a hypothesis, identifies experiment type/population/intervention, defines primary metric, guardrails, sample/duration plan, preregistered decision and kill criteria, analysis method, and any external execution authority reference.

A plan cannot encode winner/result/effect/p-value fields. An observed baseline requires evidence. The validator establishes planning representation, not experiment execution.

### `test_results`

`status: analyzed` requires preserved observation references, positive control/treatment sample sizes, an explicit primary metric and declared analysis method. `status: insufficient_evidence` cannot recommend a winner/action such as `ship`.

The validator does not decide statistical significance thresholds, practical significance, causal interpretation, or rollout authority.

### `pmf_report`

Survey arithmetic is mechanically checked when counts exist: `very_disappointed_share = very_disappointed_count / response_count`. Survey counts require evidence refs. `status: measured` requires empirical evidence references; `status: not_measured` must use `assessment: insufficient_evidence`.

Framework thresholds remain heuristics. The validator does not establish Product-Market Fit from a percentage alone.

### `pricing_model`

The generated model remains `status: proposed`. Observed current prices, competitor claims, value metrics, or unit-economics values require evidence references. Unknown/proposed values may remain unevidenced hypotheses.

Pricing analysis never grants authority to change or publish a price.

## Admission boundary

`ArtifactAdmissionService` invokes the canonical router over an immutable snapshot. A routed specialized PM artifact produces an admission receipt bound to exact artifact bytes, router bytes, selected validator bytes, and exact structured validation result.

`artifact admitted != PM conclusion warranted` remains unchanged.

## Qualification boundary

Passing these validators and Campaign admission may contribute to `REPOSITORY_QUALIFIED`. It does not establish native-harness qualification, portability qualification, customer truth, PMF, statistical significance, pricing effectiveness, implementation completion, test execution, or real-world success.