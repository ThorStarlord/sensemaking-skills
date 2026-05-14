# Workflow Orchestration Plan: Docs & Contract Reconciliation

## 1. Brief Consumed
The repository is `sensemaking-skills`.

## 2. Chosen Workflow
- **Workflow ID**: `docs-contract-reconciliation`
- **Display Name**: Docs & Contract Reconciliation

## 3. Why This Workflow
Reconciliation of drift.

## 4. Skills in Sequence
1. `repo-sensemaker`
2. `sensemaking-docs-reconciler`
3. `prompt-handoff`

## 5. Inputs and Outputs
| Step | Skill | Input | Output |
| :--- | :--- | :--- | :--- |
| 1 | `repo-sensemaker` | `repository_state` | `repository_sensemaking_brief` |
| 2 | `sensemaking-docs-reconciler` | `repository_sensemaking_brief` | `docs_contract_reconciliation_report` |
| 3 | `prompt-handoff` | `docs_contract_reconciliation_report` | `prompt_handoff` |

## 6. Approval Gates
- `review_drift_diagnosis`
- `review_reconciliation_patch`
- `review_next_prompt`

## 7. Stop Conditions
- Gate rejection.

## 8. Execution Mode
- `plan_only`

## 9. Prompt Chain
N/A — mode is plan_only.

## 10. Run Log Template
N/A

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
initial_inputs:
  - id: repository_state
    type: external_context
    source: repository
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: sensemaking-docs-reconciler
    step_type: local_execution
    gate: review_reconciliation_patch
    input_artifact: repository_sensemaking_brief
    output_artifact: docs_contract_reconciliation_report
  - id: 3
    skill: prompt-handoff
    step_type: local_execution
    gate: review_next_prompt
    input_artifact: docs_contract_reconciliation_report
    output_artifact: prompt_handoff
approval_gates:
  - review_drift_diagnosis
  - review_reconciliation_patch
  - review_next_prompt
stop_conditions:
  - user_rejection_at_gate
  - artifact_validation_failure
  - invalid_handoff
  - validator_failure
```
