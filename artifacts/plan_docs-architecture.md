# Orchestration Plan: Docs & Architecture Alignment

- **Session ID**: orchestration-20260516-203036-111f9d18
- **Date**: 2026-05-16
- **Workflow**: docs-architecture
- **Execution Mode**: guided_execution
- **Purpose**: Align documentation with domain language and generate copy-paste prompts for implementation.

## Skills in Sequence

### Step 1: grill-with-docs
- **Type**: local_execution
- **Gate**: review_alignment_report
- **Output**: domain_alignment_report

### Step 2: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **repository_state** (external_context): Current repository files, registries, templates, and contracts.

## Approval Gates

- **Mode**: guided_execution
- **Gate Behavior**: mandatory

- review_alignment_report: REQUIRED (user must approve)
- review_handoff_prompt: REQUIRED (user must approve)

## Stop Conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

---

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-architecture
execution_mode: guided_execution
status: created
session_id: orchestration-20260516-203036-111f9d18
initial_inputs:
  repository_state: external_context
steps:
  - id: 1
    skill: grill-with-docs
    step_type: local_execution
    gate: review_alignment_report
    output_artifact: domain_alignment_report
  - id: 2
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    output_artifact: prompt_handoff
approval_gates:
  behavior: mandatory
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
