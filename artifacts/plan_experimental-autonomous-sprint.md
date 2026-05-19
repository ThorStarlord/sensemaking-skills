# Orchestration Plan: Autonomous Sprint (Experimental)

- **Session ID**: orchestration-20260516-171525-cc12bf0e
- **Date**: 2026-05-16
- **Workflow**: experimental-autonomous-sprint
- **Execution Mode**: plan_only
- **Purpose**: High-velocity execution using Matt Pocock skills.

## Skills in Sequence

### Step 1: docs-aligner
- **Type**: local_execution
- **Gate**: review_domain_alignment
- **Output**: domain_alignment_report

### Step 2: to-prd
- **Type**: local_execution
- **Gate**: review_prd
- **Output**: prd

### Step 3: to-issues
- **Type**: local_execution
- **Gate**: review_issue_list
- **Output**: issue_list

### Step 4: triage
- **Type**: local_execution
- **Gate**: review_agent_briefs
- **Output**: agent_brief

### Step 5: tdd
- **Type**: local_execution
- **Gate**: verify_tests
- **Output**: code_patch

### Step 6: handoff
- **Type**: local_execution
- **Gate**: session_close
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
chosen_workflow_id: experimental-autonomous-sprint
execution_mode: plan_only
status: created
session_id: orchestration-20260516-171525-cc12bf0e
initial_inputs:
  repository_state: external_context
steps:
  - id: 1
    skill: docs-aligner
    step_type: local_execution
    gate: review_domain_alignment
    output_artifact: domain_alignment_report
  - id: 2
    skill: to-prd
    step_type: local_execution
    gate: review_prd
    output_artifact: prd
  - id: 3
    skill: to-issues
    step_type: local_execution
    gate: review_issue_list
    output_artifact: issue_list
  - id: 4
    skill: triage
    step_type: local_execution
    gate: review_agent_briefs
    output_artifact: agent_brief
  - id: 5
    skill: tdd
    step_type: local_execution
    gate: verify_tests
    output_artifact: code_patch
  - id: 6
    skill: handoff
    step_type: local_execution
    gate: session_close
    output_artifact: prompt_handoff
approval_gates:
  behavior: none
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
