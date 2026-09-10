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

## Customer Modeling routed identities

`scripts/validate-pm-customer-model.py` validates:

- `journey_map`
- `ideal_customer_profile`

### `journey_map`

The artifact binds a named persona/segment, journey scope, and evidence window before representing stages and critical moments. Stage and critical-moment identities/order/reference relationships are mechanically checked. Any journey emotion, metric, or critical moment marked `observed` requires evidence references. A purely hypothesis-based journey cannot silently contain observed claims; mixed evidence/hypothesis artifacts use `status: mixed`.

The local artifact evidence states intentionally correspond to the Semantic Architecture distinction among observation, inference, hypothesis, and unresolved knowledge, without promoting the Level-2 ontology into a universal Campaign schema. The validator does not decide whether an emotion is representative, whether an Aha Moment is causal, whether the stage model is complete, or whether a recommendation deserves priority.

### `ideal_customer_profile`

The artifact binds a segment and evidence window and separates observed customer claims from inference/hypothesis/unknown status across profile characteristics, behaviors, jobs, pains, ideal indicators, and disqualifiers. Observed customer claims require evidence. GTM implications remain `proposed`, may cite known customer-claim IDs, and cannot establish external sales/marketing authority.

The validator does not decide which segment is truly ideal, infer causality from high-value correlations, make disqualifier recommendations into sales policy, or validate willingness-to-pay, LTV, CAC, churn, buying-cycle, or other customer facts merely because the fields are present.

## Launch, GTM, Enablement, and Communication routed identities

`scripts/validate-pm-launch-communication.py` validates:

- `readiness_report`
- `gtm_plan`
- `battlecard`
- `feature_announcement`
- `stakeholder_update`

### `readiness_report`

The report distinguishes `unknown`, `planned`, `evidence_backed_complete`, `blocked`, and `not_applicable` readiness checks. Completion requires evidence and not-applicable checks require a reason. A `go` recommendation cannot coexist with unresolved launch-blocking checks. Rollback triggers remain proposals.

A readiness assessment never grants launch authority and does not prove a rollback mechanism is configured or tested.

### `gtm_plan`

Observed positioning claims and baselines require evidence. Channels and messages cite declared positioning claims where used. Targets and timeline commitments remain proposed unless an authority reference establishes ratification. The plan cannot represent outreach, publication, campaign activation, ad spend, scheduling, or other external tactics as executed.

### `battlecard`

Observed competitive claims require source evidence under an explicit cutoff. Comparison records reference declared `us` and `competitor` claims and remain interpretations rather than observations. Talk tracks remain proposed enablement language. Missing competitor evidence cannot be turned into an advantage claim.

### `feature_announcement`

The artifact remains a draft. `shipped` and `beta` availability require observed release evidence; tickets, PRDs, or planned work are insufficient. Coming-soon items remain planned, and ratified future commitments require authority evidence. Publication permission, if supplied, does not convert the draft into a published state.

### `stakeholder_update`

Consequential claims may distinguish `observed`, `derived`, `inferred`, `hypothesized`, `ratified`, and `unresolved`. Observed/derived claims require evidence, derived claims record their derivation rule, and ratified claims/decisions/commitments require authority references. Proposed owners and dates are not assignments. The artifact remains a draft and cannot claim distribution.

The validator establishes representation, source/currentness, and authority-reference integrity only. It does not establish launch readiness, GTM effectiveness, competitive superiority, successful shipment, stakeholder agreement, or external execution.

## Admission boundary

`ArtifactAdmissionService` invokes the canonical router over an immutable snapshot. A routed specialized PM artifact produces an admission receipt bound to exact artifact bytes, router bytes, selected validator bytes, and exact structured validation result.

`artifact admitted != PM conclusion warranted` remains unchanged.

## Qualification boundary

Passing these validators and Campaign admission may contribute to `REPOSITORY_QUALIFIED`. It does not establish native-harness qualification, portability qualification, customer truth, PMF, statistical significance, pricing effectiveness, implementation completion, test execution, publication/distribution, launch execution, or real-world success.
