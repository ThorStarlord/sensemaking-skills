# Orchestration Plan: Product Autonomous Sprint (Drafting)

- **Session ID**: orchestration-20260516-171520-2c62af7f
- **Date**: 2026-05-16
- **Workflow**: product-autonomous-sprint
- **Execution Mode**: plan_only
- **Purpose**: Generate a full proposed product artifact chain from product fog to implementation-ready handoff.

## Skills in Sequence

### Step 1: persona
- **Type**: local_execution
- **Gate**: review_persona
- **Output**: persona_definition

### Step 2: discovery
- **Type**: local_execution
- **Gate**: review_discovery
- **Output**: discovery_findings

### Step 3: opportunity-tree
- **Type**: local_execution
- **Gate**: review_opportunity_tree
- **Output**: opportunity_map

### Step 4: hypothesis
- **Type**: local_execution
- **Gate**: review_hypothesis
- **Output**: hypothesis_statement

### Step 5: prd
- **Type**: local_execution
- **Gate**: review_prd
- **Output**: prd

### Step 6: user-stories
- **Type**: local_execution
- **Gate**: review_user_stories
- **Output**: story_list

### Step 7: acceptance-criteria
- **Type**: local_execution
- **Gate**: review_acceptance_criteria
- **Output**: criteria_list

### Step 8: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **repository_sensemaking_brief** (artifact): A diagnostic brief defining the initial product fog.

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
chosen_workflow_id: product-autonomous-sprint
execution_mode: plan_only
status: created
session_id: orchestration-20260516-171520-2c62af7f
initial_inputs:
  repository_sensemaking_brief: artifact
steps:
  - id: 1
    skill: persona
    step_type: local_execution
    gate: review_persona
    output_artifact: persona_definition
  - id: 2
    skill: discovery
    step_type: local_execution
    gate: review_discovery
    output_artifact: discovery_findings
  - id: 3
    skill: opportunity-tree
    step_type: local_execution
    gate: review_opportunity_tree
    output_artifact: opportunity_map
  - id: 4
    skill: hypothesis
    step_type: local_execution
    gate: review_hypothesis
    output_artifact: hypothesis_statement
  - id: 5
    skill: prd
    step_type: local_execution
    gate: review_prd
    output_artifact: prd
  - id: 6
    skill: user-stories
    step_type: local_execution
    gate: review_user_stories
    output_artifact: story_list
  - id: 7
    skill: acceptance-criteria
    step_type: local_execution
    gate: review_acceptance_criteria
    output_artifact: criteria_list
  - id: 8
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    output_artifact: prompt_handoff
approval_gates:
  behavior: none
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
