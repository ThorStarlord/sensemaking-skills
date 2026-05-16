# Orchestration Plan: Fast Local Diagnostic

- **Session ID**: orchestration-20260516-171849-05acdea6
- **Date**: 2026-05-16
- **Workflow**: fast-local-diagnostic
- **Execution Mode**: plan_only
- **Purpose**: Quickly identify the weakest boundary and produce a handoff prompt.

## Skills in Sequence

### Step 1: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_sensemaking_brief
- **Output**: repository_sensemaking_brief

### Step 2: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

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
chosen_workflow_id: fast-local-diagnostic
execution_mode: plan_only
status: created
session_id: orchestration-20260516-171849-05acdea6
initial_inputs:
  repository_state: external_context
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
    output_artifact: prompt_handoff
approval_gates:
  behavior: none
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
