# Orchestration Plan: Product Strategy Sprint

- **Session ID**: orchestration-20260516-171516-5157c83a
- **Date**: 2026-05-16
- **Workflow**: product-strategy-sprint
- **Execution Mode**: plan_only
- **Purpose**: Translate a validated hypothesis into high-level roadmap and goal alignment.

## Skills in Sequence

### Step 1: lean-canvas
- **Type**: external_routing
- **Gate**: review_canvas
- **Output**: business_canvas

### Step 2: north-star
- **Type**: external_routing
- **Gate**: review_metric
- **Output**: north_star_metric

### Step 3: okr
- **Type**: external_routing
- **Gate**: review_goals
- **Output**: okr_list

### Step 4: roadmap
- **Type**: external_routing
- **Gate**: review_roadmap
- **Output**: roadmap

### Step 5: stakeholder-update
- **Type**: external_routing
- **Gate**: review_stakeholder_update
- **Output**: stakeholder_update

## Inputs and Outputs

- **hypothesis_statement** (artifact): A testable bet about the product.

## Approval Gates

- **Mode**: plan_only
- **Gate Behavior**: none

No gates required for this mode.

## Stop Conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

---

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: product-strategy-sprint
execution_mode: plan_only
status: created
session_id: orchestration-20260516-171516-5157c83a
initial_inputs:
  hypothesis_statement: artifact
steps:
  - id: 1
    skill: lean-canvas
    step_type: external_routing
    gate: review_canvas
    output_artifact: business_canvas
  - id: 2
    skill: north-star
    step_type: external_routing
    gate: review_metric
    output_artifact: north_star_metric
  - id: 3
    skill: okr
    step_type: external_routing
    gate: review_goals
    output_artifact: okr_list
  - id: 4
    skill: roadmap
    step_type: external_routing
    gate: review_roadmap
    output_artifact: roadmap
  - id: 5
    skill: stakeholder-update
    step_type: external_routing
    gate: review_stakeholder_update
    output_artifact: stakeholder_update
approval_gates:
  behavior: none
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
