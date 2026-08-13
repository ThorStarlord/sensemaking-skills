---
validator_case: positive
---
# Example: Docs Contract Reconciliation Plan

## 1. Brief consumed
Diagnosis of vocabulary drift between `CONTEXT.md` and `artifact-contracts.yaml`.

## 2. Chosen workflow
docs-contract-reconciliation

## 3. Why this workflow
It is designed to identify and fix discrepancies in the orchestration contract.

## 4. Skills in sequence
1. repo-sensemaker
2. sensemaking-docs-reconciler
3. handoff

## 5. Inputs and outputs
- Step 1: repo -> brief
- Step 2: brief -> report
- Step 3: report -> handoff

## 6. Approval gates
- review_drift_diagnosis
- review_reconciliation_patch
- review_next_prompt

## 7. Stop conditions
- user_rejection
- vocabulary_stable

## 8. Execution mode
plan_only

## 9. Prompt chain
N/A

## 10. Run log template
N/A

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
primary_fog_type: docs_fog
routing_decision_method: manual_override
created_at: "2026-05-19T16:00:00Z"
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
    source: repository
workflow_steps:
  - id: 1
    skill: repo-sensemaker
    status: PENDING
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: sensemaking-docs-reconciler
    status: PENDING
    step_type: local_execution
    gate: review_reconciliation_patch
    input_artifact: repository_sensemaking_brief
    output_artifact: docs_contract_reconciliation_report
  - id: 3
    skill: repair-verifier
    status: PENDING
    step_type: local_execution
    gate: review_reconciliation_verified
    input_artifact: docs_contract_reconciliation_report
    input_source: repository_state
    output_artifact: repair_verification_report
  - id: 4
    skill: handoff
    status: PENDING
    step_type: local_execution
    gate: review_next_prompt
    input_artifact: repair_verification_report
    output_artifact: session_summary
approval_gates:
  - review_drift_diagnosis
  - review_reconciliation_patch
  - review_reconciliation_verified
  - review_next_prompt
gate_behavior:
  review_drift_diagnosis: manual_review
  review_reconciliation_patch: manual_review
  review_reconciliation_verified: manual_review
  review_next_prompt: manual_review
stop_conditions:
  - user_rejection
  - vocabulary_stable
```
