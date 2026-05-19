# Workflow Orchestration Plan: Routing Override

**Scenario**: System recommends full-fog workflow due to conflict, but user explicitly selects product-focused workflow.

---

## 1. Brief Consumed

From repository_sensemaking_brief:
- primary_fog_type: architecture_fog
- user_implied_fog_type: ui_fog
- diagnosis_conflict: true
- escalation_recommended: true
- recommended_workflow_id: full-fog-workflow

## 1.5. Problem Classification

The diagnosis indicates **architecture_fog** (code structure, design boundaries), but user intended **ui_fog** (navigation, screen design). Conflict detected; escalation recommended. User chooses to override and focus on product delivery.

## 2. Chosen Workflow

**product-implementation-workflow**

System recommended full-fog-workflow to resolve intent/diagnosis conflict. User explicitly overrode with product-implementation-workflow to stay focused on product deliverables rather than full system redesign.

## 3. Why This Workflow

Intent/diagnosis conflict would normally trigger full-fog-workflow (comprehensive analysis of all fog types). However, user prioritizes shipping product features over architectural redesign. Product-implementation-workflow provides discovery → opportunity-tree → PRD path focused on feature delivery. User accepts architecture debt as acceptable for this iteration. Routing divergence: true.

## 4. Skills in Sequence

1. **discovery** — Synthesize user needs from interviews/research
2. **opportunity-tree** — Map needs to product opportunities
3. **to-prd** — Convert opportunities into product requirements

## 5. Inputs and Outputs

| Skill | Input | Output |
|-------|-------|--------|
| discovery | user_intent, repository_state | discovery_findings |
| opportunity-tree | discovery_findings | opportunity_map |
| to-prd | opportunity_map | prd |

## 6. Approval Gates

- **Before Step 1**: Confirm user wants product-focused path despite escalation recommendation
- **After discovery**: review_discovery_findings (pause for user validation)
- **After opportunity-tree**: review_opportunity_map (pause for user validation)
- **After to-prd**: review_prd (pause for final review)

## 7. Stop Conditions

- **validator_failure**: If any artifact fails schema validation
- **gate_denial**: If user rejects findings at any gate
- **step_failure**: If a skill execution fails
- **user_interrupt**: If user explicitly stops the run
- **routing_divergence_acknowledgment**: User must acknowledge override before continuing

## 8. Execution Mode

**guided_execution** (required due to routing divergence)
- User must explicitly confirm override of system recommendation
- All approval gates are mandatory
- Allows inspection of artifacts and intermediate results

## 9. Prompt Chain

N/A - mode is guided_execution. Each skill invocation includes handoff context from prior steps. User approval is required before proceeding.

## 10. Run Log Template

```
## Run Log: product-implementation-workflow (override)

**Status**: [in_progress | complete | failed]
**User**: [who approved]
**Date**: [execution date]

### Pre-flight
- Routing divergence acknowledged: [yes | no]
- User override reason: [stated reason]
- System recommendation deferred: full-fog-workflow
- Repository state: [clean | with changes]

### Step 0: Override Confirmation
- Message: "System recommended full-fog-workflow due to architecture signals. Continue with product-implementation-workflow?"
- User response: [approved]
- Approved by: [user name]
- Approved at: [timestamp]

### Step 1: discovery
- Input: user_intent.md, repository files
- Output: discovery_findings.md
- Status: [pending | complete | failed]

### Step 2: opportunity-tree
- Input: discovery_findings.md
- Output: opportunity_map.md
- Status: [pending | complete | failed]

### Step 3: to-prd
- Input: opportunity_map.md
- Output: prd.md
- Status: [pending | complete | failed]

### Summary
[Describe what was completed, decisions made, architecture debt accepted, next steps]
```

## 11. Machine-Readable Plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: ../../00-user-intent.md
chosen_workflow_id: product-implementation-workflow
execution_mode: guided_execution
status: ready
system_recommended_workflow: full-fog-workflow
selected_workflow: product-implementation-workflow
routing_divergence: true
routing_decision_method: user_explicit_override
escalation_recommended: true
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    description: "User's problem statement and scope"
  - id: repository_state
    type: artifact
    required: true
    description: "Current repository structure and files"
steps:
  - id: 0
    skill: user_confirmation
    step_type: decision_point
    gate: confirm_override
    output_artifact: null
  - id: 1
    skill: discovery
    step_type: skill_execution
    gate: review_discovery_findings
    output_artifact: discovery_findings
  - id: 2
    skill: opportunity-tree
    step_type: skill_execution
    gate: review_opportunity_map
    output_artifact: opportunity_map
  - id: 3
    skill: to-prd
    step_type: skill_execution
    gate: review_prd
    output_artifact: prd
approval_gates:
  confirm_override: "User confirms product-focused path despite escalation recommendation"
  review_discovery_findings: "User reviews and approves discovery findings"
  review_opportunity_map: "User reviews and approves opportunity mapping"
  review_prd: "User reviews and approves product requirements"
gate_behavior:
  default: pause_for_user_decision
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
  - user_override_not_confirmed
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
created_at: "2026-05-19T17:15:00Z"
```
