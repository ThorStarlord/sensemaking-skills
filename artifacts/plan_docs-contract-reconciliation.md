# Orchestration Plan: Docs & Contract Reconciliation

- **Session ID**: orchestration-20260516-203712-ee9f455b
- **Date**: 2026-05-16
- **Workflow**: docs-contract-reconciliation
- **Execution Mode**: guided_execution
- **Purpose**: Resolve drift between documentation, registries, artifact contracts, templates, and validator rules.

## Skills in Sequence

### Step 1: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_drift_diagnosis
- **Output**: repository_sensemaking_brief

### Step 2: sensemaking-docs-reconciler
- **Type**: local_execution
- **Gate**: review_reconciliation_patch
- **Output**: docs_contract_reconciliation_report

### Step 3: prompt-handoff
- **Type**: local_execution
- **Gate**: review_next_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

## Approval Gates

- **Mode**: guided_execution
- **Gate Behavior**: mandatory

- review_drift_diagnosis: REQUIRED (user must approve)
- review_reconciliation_patch: REQUIRED (user must approve)
- review_next_prompt: REQUIRED (user must approve)

## Stop Conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

---

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: guided_execution
status: created
session_id: orchestration-20260516-203712-ee9f455b
initial_inputs:
  repository_state: external_context
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_drift_diagnosis
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: sensemaking-docs-reconciler
    step_type: local_execution
    gate: review_reconciliation_patch
    output_artifact: docs_contract_reconciliation_report
  - id: 3
    skill: prompt-handoff
    step_type: local_execution
    gate: review_next_prompt
    output_artifact: prompt_handoff
approval_gates:
  behavior: mandatory
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
