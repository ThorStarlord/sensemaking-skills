# Orchestration Plan: Setup Sensemaking Repo

- **Session ID**: orchestration-20260518-005613-e46d2741
- **Date**: 2026-05-18
- **Workflow**: setup-sensemaking-repo
- **Execution Mode**: plan_only
- **Purpose**: Configure repository agent docs, artifact contracts, execution mode defaults, and downstream skill mappings.

## Skills in Sequence

### Step 1: setup-sensemaking-skills
- **Type**: local_execution
- **Gate**: review_setup_plan
- **Output**: N/A

### Step 2: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_repo_brief
- **Output**: repository_sensemaking_brief

### Step 3: prompt-handoff
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
chosen_workflow_id: setup-sensemaking-repo
execution_mode: plan_only
status: created
session_id: orchestration-20260518-005613-e46d2741
initial_inputs:
  repository_state: external_context
steps:
  - id: 1
    skill: setup-sensemaking-skills
    step_type: local_execution
    gate: review_setup_plan
    output_artifact: N/A
  - id: 2
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_repo_brief
    output_artifact: repository_sensemaking_brief
  - id: 3
    skill: prompt-handoff
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
