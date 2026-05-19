---
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: ../../00-user-intent.md
chosen_workflow_id: full-fog-workflow
execution_mode: guided_execution
status: ready
system_recommended_workflow: fast-local-diagnostic
routing_divergence: true
routing_decision_method: user_explicit_cli_override
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
steps: []
approval_gates: []
gate_behavior: {}
stop_conditions: []
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
---

## Chosen Workflow

This plan is missing the required field: selected_workflow

The plan has system_recommended_workflow and routing_divergence, but selected_workflow is missing. This should fail validation because we need to know which workflow was actually selected, even if it matches the recommendation.
