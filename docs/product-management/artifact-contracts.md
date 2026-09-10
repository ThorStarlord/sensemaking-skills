# Product Management artifact contracts

## Authority

Concise human contracts live beside each canonical Skill in that Skill's `references/` directory. The canonical validation router selects specialized deterministic validators where PM machine-contract invariants add value.

Historical Wayfinder entries in `skills/workflow-planner/references/artifact-contracts.yaml` preserve compatibility/provenance. They do not become semantic authority merely because an identifier is reused.

## Customer Discovery routed identities

`scripts/validate-pm-artifact.py` validates:

- `persona_definition`
- `discovery_findings`
- `synthesis_report`
- `opportunity_map`
- `hypothesis_statement`

It checks mechanically decidable representation/evidence-shape contracts such as required sections/fields, allowed statuses, unique IDs, source-reference relationships, frequency arithmetic, and declared opportunity-score arithmetic.

It may not decide whether a persona is representative, a finding is important, an opportunity should be prioritized, or a hypothesis is strategically correct.

## Feature Definition routed identities

`scripts/validate-pm-feature-definition.py` validates:

- `story_list`
- `criteria_list`
- `risk_analysis`

`story_list` preserves bounded source traceability, scope status, story identity, user/capability intent, acceptance intent, dependencies, and unresolved questions. The validator does not estimate effort or choose priority.

`criteria_list` preserves source traceability and explicit Given/When/Then behavior. `status` remains `specified`; pass/execution evidence belongs elsewhere.

`risk_analysis` preserves risk class, evidence status, urgency, impact/probability, mitigation, ownership role, escalation signal, and an agent-authored recommendation. A purely hypothetical item cannot be encoded as a current Tiger, and the recommendation grants no launch authority.

## PRD authority

`prd` remains produced by the existing canonical `to-prd` Skill. Upstream `prd` methodology is merged into `to-prd`; no second current `prd` capability is created.

The existing PRD scope-expansion contract remains authoritative. Existing PRD validation is retained; Wave 2 does not silently replace its historical contract with a competing PM artifact identity.

## Strategy and Prioritization routed identities

`scripts/validate-pm-strategy.py` validates:

- `market_analysis`
- `strategy_doc`
- `prioritized_list`
- `north_star_metric`
- `okr_list`
- `roadmap`
- `business_canvas`

These checks intentionally constrain representation without turning frameworks into semantic routers.

### `market_analysis`

Observed competitor claims require source references and an explicit evidence cutoff. Inferred and unknown claims remain distinguishable. The validator does not decide which competitor matters or which positioning is correct.

### `strategy_doc`

The generated strategy status is `proposed`. Choices, non-choices, measures, roadmap themes, assumptions, and risks remain agent-authored analysis. An observed metric baseline requires evidence; the Skill cannot self-ratify strategy.

### `prioritized_list`

When complete numeric RICE inputs are declared, the validator recomputes:

```text
(reach * impact * confidence) / effort
```

It does not require the semantic recommended order to equal raw score order. Dependencies, evidence strength, risk, strategic fit, and other trade-offs remain agent judgment.

### `north_star_metric`

Candidate identity and selection references must resolve, and an observed baseline requires evidence. Candidate scores are assessments, not measurements; the selected NSM remains `proposed` until separately ratified.

### `okr_list`

Objective and KR identities are unique. KRs are encoded as outcomes rather than delivery outputs; observed baselines require evidence and targets remain proposed. The validator does not require a dogmatic number of KRs or certify target quality.

### `roadmap`

Initiative identities and dependencies are checked. Timing may be unknown, estimated, or committed; `committed` timing requires an explicit authority reference. A roadmap remains a planning artifact rather than execution authority.

### `business_canvas`

All nine Lean Canvas blocks are represented with evidence states. Blocks marked observed require evidence refs. The overall canvas remains a hypothesis map; it cannot self-declare validation.

## Admission boundary

`ArtifactAdmissionService` invokes the canonical router over an immutable snapshot. A routed specialized PM artifact therefore produces an admission receipt bound to:

- exact artifact bytes;
- `validate-and-report.py` bytes;
- selected specialized validator bytes;
- exact structured validation result.

`artifact admitted != PM conclusion warranted` remains unchanged.

## Qualification boundary

Passing these validators and Campaign admission may contribute to `REPOSITORY_QUALIFIED`. It does not establish native-harness qualification, portability qualification, customer truth, strategic correctness, implementation completion, test execution, or real-world success.