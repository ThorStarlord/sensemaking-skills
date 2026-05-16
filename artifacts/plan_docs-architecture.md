# Orchestration Plan: Docs & Architecture Alignment

- **Session ID**: orchestration-20260516-171510-b1c0877c
- **Date**: 2026-05-16
- **Workflow**: docs-architecture
- **Execution Mode**: plan_only
- **Purpose**: Turn an approved brief or PRD into copy-paste prompts for external implementation skills.

## Skills in Sequence

### Step 1: grill-with-docs
- **Type**: local_execution
- **Gate**: review_alignment_report
- **Output**: domain_alignment_report

### Step 2: to-prd
- **Type**: local_execution
- **Gate**: review_prd
- **Output**: prd

### Step 3: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **repository_state** (external_context): Current repository files, registries, templates, and contracts.

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
chosen_workflow_id: docs-architecture
execution_mode: plan_only
status: created
session_id: orchestration-20260516-171510-b1c0877c
initial_inputs:
  repository_state: external_context
steps:
  - id: 1
    skill: grill-with-docs
    step_type: local_execution
    gate: review_alignment_report
    output_artifact: domain_alignment_report
  - id: 2
    skill: to-prd
    step_type: local_execution
    gate: review_prd
    output_artifact: prd
  - id: 3
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
