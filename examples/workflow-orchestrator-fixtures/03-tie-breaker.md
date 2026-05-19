# Workflow Orchestration Plan: Tie-Breaker Decision

**Scenario**: Repository signals mixed fog (product + UI equally strong), multiple workflows equally valid. Orchestrator applies tie-breaker rule to select one.

---

## 1. Brief Consumed

From repository_sensemaking_brief:
- primary_fog_type: mixed
- secondary_fog_type: product_fog, ui_fog (equal weight)
- diagnosis_conflict: false
- escalation_recommended: false
- recommended_workflow_id: product-implementation-workflow (orchestrator's tie-breaker choice)

## 1.5. Problem Classification

The diagnosis indicates **mixed fog**: both product features AND UI interaction patterns need definition. Code signals are ambiguous; multiple workflows could apply equally. Tie-breaker applied: user intent implies product-first (user_implied_fog_type: product_fog), so product-implementation-workflow selected.

## 2. Chosen Workflow

**product-implementation-workflow**

Diagnosis shows both product features AND UI interaction patterns need definition. Two workflows are equally valid:
- product-implementation-workflow (discovery → opportunity-tree → PRD)
- ux-iteration-workflow (persona → user-journey → interaction-spec)

Tie-breaker rule: When diagnosis is inconclusive, use user intent to break the tie. User's stated intent focuses on feature delivery, so product-implementation-workflow selected first.

## 3. Why This Workflow

Mixed fog requires both product and UX clarity, but starting point matters. User's intent prioritizes feature delivery. Product-implementation-workflow provides discovery → opportunity-tree → PRD path focused on feature delivery. UX patterns can be refined within product stories as acceptance criteria. Smallest first step with highest leverage. No conflict between intent and diagnosis; tie-breaker is automatic.

## 4. Skills in Sequence

1. **discovery** — Synthesize user needs from interviews/research
2. **opportunity-tree** — Map needs to product opportunities
3. **to-prd** — Convert opportunities into product requirements

## 5. Inputs and Outputs

| Skill | Input | Output |
|-------|-------|--------|
| discovery | user_intent, repository_state | discovery_findings |
| opportunity-tree | discovery_findings | opportunity_map |
| to-prd | opportunity_map, domain_alignment_report | prd |

## 6. Approval Gates

- **After discovery**: review_discovery_findings (pause for user validation)
- **After opportunity-tree**: review_opportunity_map (pause for user validation)
- **After to-prd**: review_prd (pause for final review)

## 7. Stop Conditions

- **validator_failure**: If any artifact fails schema validation
- **gate_denial**: If user rejects findings at any gate
- **step_failure**: If a skill execution fails
- **user_interrupt**: If user explicitly stops the run
- **mixed_fog_ambiguity**: If evidence suggests UX-first is actually better, user can escalate to full-fog-workflow

## 8. Execution Mode

**guided_execution** (required to collect user feedback on tie-breaker choice)
- User is shown the mixed fog diagnosis and tie-breaker reasoning
- User can approve product-first approach OR request escalation to UX-first or full-fog
- All approval gates are mandatory to gather direction at each step

## 9. Prompt Chain

N/A - mode is guided_execution. Each skill invocation includes handoff context from prior steps. User approval is required before proceeding.

## 10. Run Log Template

```
## Run Log: product-implementation-workflow (tie-breaker)

**Status**: [in_progress | complete | failed]
**User**: [who approved]
**Date**: [execution date]

### Pre-flight
- Mixed fog detected: [yes]
- Equally valid workflows: [product-implementation-workflow, ux-iteration-workflow]
- Tie-breaker applied: [user_implied_fog_type: product_fog]
- User confirmed product-first approach: [yes | no]

### Step 1: discovery
- Input: user_intent.md, repository files
- Output: discovery_findings.md
- Status: [pending | complete | failed]
- Tie-breaker validated: [findings confirm product-first is correct OR switch to UX-first?]

### Step 2: opportunity-tree
- Input: discovery_findings.md
- Output: opportunity_map.md
- Status: [pending | complete | failed]
- User feedback: [proceed OR request alternative workflow]

### Step 3: to-prd
- Input: opportunity_map.md, domain_alignment_report.md
- Output: prd.md
- Status: [pending | complete | failed]

### Summary
[Describe what was completed, whether tie-breaker choice was validated, if UX workflow should be next iteration]
```

## 11. Machine-Readable Plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
source_intent_ref: ../../00-user-intent.md
chosen_workflow_id: product-implementation-workflow
execution_mode: guided_execution
status: ready
system_recommended_workflow: product-implementation-workflow
selected_workflow: product-implementation-workflow
routing_divergence: false
routing_decision_method: diagnosis_mixed_tiebreak_to_user_intent
escalation_recommended: false
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
  review_discovery_findings: "User reviews findings and confirms product-first approach is correct"
  review_opportunity_map: "User reviews opportunity mapping"
  review_prd: "User reviews product requirements"
gate_behavior:
  default: pause_for_user_decision
  allow_workflow_switch_at_discovery: true
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
  - user_requests_ux_first_workflow
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
created_at: "2026-05-19T17:30:00Z"
```
