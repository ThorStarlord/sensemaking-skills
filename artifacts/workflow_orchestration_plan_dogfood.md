# Workflow Orchestration Plan

## 1. Brief consumed

**Repository**: `sensemaking-skills`
**Primary fog type**: `docs_fog`
**Weakest boundary**: `Implicit Dependencies` — the validation wrapper hardcodes `python3` while the documented invocation uses `python`.
**Source brief**: `artifacts/repository_sensemaking_brief_dogfood.md`
**Probe**: `artifacts/repo-sensemaker-dogfood-probe-report.yaml`

The brief also records secondary contract signals: `vg=0.67`, validator fixture coverage `0.74`, conflicting version declarations, and three ADR status findings requiring semantic review.

## 1.5. Problem classification (fog type)

The primary classification is `docs_fog`: the most actionable mismatch is between documented commands, validator implementation, and enforcement contracts. The existing owner-intent artifact implies `architecture_fog`, so the brief marks a diagnosis conflict and recommends escalation if the targeted reconciliation cannot resolve the authority questions.

## 2. Chosen workflow

`docs-contract-reconciliation`

## 3. Why this workflow

This workflow directly addresses drift between documentation, registries, artifact contracts, templates, and validator rules. It is the smallest registered workflow that can reconcile the documented `python` command with the wrapper's hardcoded `python3` dependency, then review version, fixture, CI, and ADR inconsistencies under explicit approval gates.

The plan deliberately keeps the scope narrow. The brief's broad escalation path is `full-fog-workflow`; that broader route is deferred while the targeted contract reconciliation is evaluated. If the authority questions remain unresolved, stop and escalate rather than expanding scope automatically.

## 4. Skills in sequence

1. `repo-sensemaker` — refresh or confirm the drift diagnosis.
2. `sensemaking-docs-reconciler` — produce a proposed reconciliation report covering the interpreter handoff and related contract findings.
3. `handoff` — convert the approved reconciliation result into the next-session prompt and summary.

## 5. Inputs and outputs

| Step | Input | Skill | Output | Purpose |
|---|---|---|---|---|
| 1 | `repository_state` | `repo-sensemaker` | `repository_sensemaking_brief` | Confirm current state, evidence, and weakest boundary. |
| 2 | `repository_sensemaking_brief` | `sensemaking-docs-reconciler` | `docs_contract_reconciliation_report` | Propose authority decisions and contract/documentation changes. |
| 3 | `docs_contract_reconciliation_report` | `handoff` | `session_summary` | Prepare the approved next action without executing it. |

## 6. Approval gates

- `review_drift_diagnosis`: approve the refreshed diagnosis and evidence before reconciliation.
- `review_reconciliation_patch`: approve the proposed interpreter, metadata, fixture, CI, and ADR resolutions before any mutation.
- `review_next_prompt`: approve the final handoff and scope of any subsequent implementation.

## 7. Stop conditions

Stop the plan if any of the following occurs:

- A validator fails or a workflow step fails.
- The user denies an approval gate.
- The authority for a version, dependency, ADR status, or enforcement rule cannot be decided from repository evidence and owner input.
- The proposed change expands beyond documentation/contract reconciliation without explicit approval.
- The Windows validation command remains untestable because the supported interpreter contract is still unspecified.

## 8. Execution mode

`plan_only`

No workflow steps are executed and no repository mutation is authorized by this artifact.

## 9. Prompt chain

N/A - mode is plan_only. No prompt chain generated.

## 10. Run log template

No run log is produced in `plan_only` mode. If this plan is later executed, record for each step: the interpreter path, command or skill invocation, input artifact paths, output artifact path, approval decision, validation result, and any unresolved authority question. Persist the wrapper failure/success transcript separately so the portability finding is durable.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: 00-user-intent.md
primary_fog_type: docs_fog
user_implied_fog_type: architecture_fog
diagnosis_conflict: true
chosen_workflow_id: docs-contract-reconciliation
recommended_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
system_recommended_workflow: full-fog-workflow
selected_workflow: docs-contract-reconciliation
routing_divergence: true
routing_decision_method: escalation_recommended_rejected
escalation_recommended: true
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
    description: "Current repository files, registries, templates, validator scripts, and git state."
workflow_steps:
  - id: 1
    skill: repo-sensemaker
    status: PENDING
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
    description: "Refresh the measured diagnosis and confirm the interpreter-handoff boundary."
  - id: 2
    skill: sensemaking-docs-reconciler
    status: PENDING
    step_type: local_execution
    gate: review_reconciliation_patch
    input_artifact: repository_sensemaking_brief
    output_artifact: docs_contract_reconciliation_report
    description: "Propose an authority matrix and reconciliation for interpreter, metadata, fixtures, CI, and ADR findings."
  - id: 3
    skill: handoff
    status: PENDING
    step_type: local_execution
    gate: review_next_prompt
    input_artifact: docs_contract_reconciliation_report
    output_artifact: session_summary
    description: "Prepare the next approved prompt without executing implementation changes."
approval_gates:
  - review_drift_diagnosis
  - review_reconciliation_patch
  - review_next_prompt
gate_behavior:
  default: pause_for_user_decision
  review_drift_diagnosis: manual_review
  review_reconciliation_patch: manual_review
  review_next_prompt: manual_review
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
  - unresolved_authority_decision
  - scope_expansion_without_approval
subset_run: false
subset_reason: null
included_steps:
  - 1
  - 2
  - 3
excluded_steps: []
created_at: "2026-08-12T04:56:31Z"
immutable: true
```
