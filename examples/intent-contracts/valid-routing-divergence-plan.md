---
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: "../../00-user-intent.md"
chosen_workflow_id: full-fog-workflow
execution_mode: guided_execution
status: ready
system_recommended_workflow: fast-local-diagnostic
selected_workflow: full-fog-workflow
routing_divergence: true
routing_decision_method: user_explicit_cli_override
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    description: "User's problem statement and scope"
steps:
  - step_id: 1
    skill: problem-framer
    inputs:
      - user_intent
  - step_id: 2
    skill: unknowns-mapper
    inputs:
      - problem_frame
  - step_id: 3
    skill: repo-sensemaker
    inputs:
      - unknowns_map
approval_gates:
  - gate_id: escalation_check
    condition: "escalation_recommended == true"
    behavior: pause_for_user_decision
gate_behavior:
  default: pause_for_user_decision
stop_conditions:
  - condition: insufficient_evidence
    action: halt_with_recommendation
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
---

## Brief Consumed

Fast-path diagnostic recommends continuing with full-fog due to high complexity in authentication architecture.

## Chosen Workflow

User explicitly selected full-fog-workflow via CLI --workflow flag despite system recommendation for fast-local-diagnostic.

## Routing Decision

- **System recommended**: fast-local-diagnostic
- **User selected**: full-fog-workflow
- **Divergence**: true (user override)
- **Decision method**: user_explicit_cli_override

This fixture tests that routing divergence is properly recorded when user overrides system recommendation.
