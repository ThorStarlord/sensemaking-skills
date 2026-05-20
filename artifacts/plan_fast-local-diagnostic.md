# Orchestration Plan: Fast Local Diagnostic

- **Session ID**: orchestration-20260520-160318-bd2022ff
- **Date**: 2026-05-20
- **Workflow**: fast-local-diagnostic
- **Execution Mode**: yolo_execution
- **Purpose**: Quickly identify the weakest boundary and produce a handoff prompt.

## Skills in Sequence

### Step 1: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_sensemaking_brief
- **Output**: repository_sensemaking_brief

### Step 2: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: session_summary

## Inputs and Outputs

- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

## Approval Gates

- **Mode**: yolo_execution
- **Gate Behavior**: bypassed

- review_sensemaking_brief: BYPASSED
- review_handoff_prompt: BYPASSED

## Stop Conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

---

```yaml
artifact_id: workflow_orchestration_plan
source_intent_ref: ../../00-user-intent.md
chosen_workflow_id: fast-local-diagnostic
system_recommended_workflow: fast-local-diagnostic
selected_workflow: fast-local-diagnostic
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
execution_mode: yolo_execution
status: created
session_id: orchestration-20260520-160318-bd2022ff
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
    description: Current repository files, registries, templates, validator scripts, and git state.
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_sensemaking_brief
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    output_artifact: session_summary
approval_gates:
  behavior: bypassed
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
