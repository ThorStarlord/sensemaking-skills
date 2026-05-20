# Orchestration Plan: Full Fog Path - Comprehensive Sensemaking & Orchestration

- **Session ID**: orchestration-20260519-212505-f981bfeb
- **Date**: 2026-05-19
- **Workflow**: full-fog-workflow
- **Execution Mode**: prompt_chain
- **Purpose**: Comprehensively analyze ambiguous projects from raw fog through diagnosis to automatic implementation workflow invocation.

## Skills in Sequence

### Step 1: problem-framer
- **Type**: local_execution
- **Gate**: review_problem_frame
- **Output**: problem_frame

### Step 2: unknowns-mapper
- **Type**: local_execution
- **Gate**: review_unknowns_map
- **Output**: unknowns_map

### Step 3: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_diagnosis
- **Output**: repository_sensemaking_brief

### Step 4: workflow-planner
- **Type**: local_execution
- **Gate**: review_orchestration_plan
- **Output**: workflow_orchestration_plan

## Inputs and Outputs

- **user_intent** (artifact): User's problem statement and scope mode (created by workflow-runtime)
- **raw_fog** (external_context): Vague problem statement, project goals, team context, and current state of confusion.
- **repository_state** (external_context): Current repository files, folder structure, README, documentation, and git state.

## Approval Gates

- **Mode**: prompt_chain
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
source_intent_ref: ../../00-user-intent.md
chosen_workflow_id: full-fog-workflow
system_recommended_workflow: full-fog-workflow
selected_workflow: full-fog-workflow
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
execution_mode: prompt_chain
status: created
session_id: orchestration-20260519-212505-f981bfeb
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    description: User's problem statement and scope mode (created by workflow-runtime)
  - id: raw_fog
    type: external_context
    required: true
    description: Vague problem statement, project goals, team context, and current state of confusion.
  - id: repository_state
    type: external_context
    required: true
    description: Current repository files, folder structure, README, documentation, and git state.
steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    gate: review_problem_frame
    output_artifact: problem_frame
  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    gate: review_unknowns_map
    output_artifact: unknowns_map
  - id: 3
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_diagnosis
    output_artifact: repository_sensemaking_brief
  - id: 4
    skill: workflow-planner
    step_type: local_execution
    gate: review_orchestration_plan
    output_artifact: workflow_orchestration_plan
approval_gates:
  behavior: none
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
