# Workflow Orchestration Plan: Routing Agreement

**Scenario**: System recommendation matches user selection (or no override provided).

---

## 1. Brief Consumed

From repository_sensemaking_brief:
- primary_fog_type: product_fog
- diagnosis_conflict: false
- escalation_recommended: false
- recommended_workflow_id: product-implementation-workflow

## 1.5. Problem Classification

The diagnosis indicates **product_fog**: vague user needs, unclear feature specs, or undocumented workflows. This determines the product-implementation-workflow path.

## 2. Chosen Workflow

**product-implementation-workflow**

System recommended product-implementation-workflow based on product_fog diagnosis. User did not override. Selection matches recommendation.

## 3. Why This Workflow

Product fog indicates missing user needs, unclear feature specs, or undocumented workflows. The product-implementation-workflow includes discovery, opportunity-tree, and hypothesis-driven user story generation—exactly what product fog requires. No escalation needed; diagnosis and intent align.

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

## 8. Execution Mode

**guided_execution** (default)
- User must approve before each step
- Allows inspection of artifacts and intermediate results
- Safe mode for first iterations

## 9. Prompt Chain

N/A - mode is guided_execution. No copy-paste prompts generated. Each skill invocation includes handoff context from prior steps.

## 10. Run Log Template

```
## Run Log: product-implementation-workflow

**Status**: [in_progress | complete | failed]
**User**: [who approved]
**Date**: [execution date]

### Pre-flight
- Repository state: [clean | with changes]
- Current branch: [branch name]
- Initial context size: [token estimate]

### Step 1: discovery
- Input: user_intent.md, repository files
- Output: discovery_findings.md
- Status: [pending | complete | failed]
- Approved by: [user name]
- Approved at: [timestamp]

### Step 2: opportunity-tree
- Input: discovery_findings.md
- Output: opportunity_map.md
- Status: [pending | complete | failed]
- Approved by: [user name]
- Approved at: [timestamp]

### Step 3: to-prd
- Input: opportunity_map.md, domain_alignment_report.md
- Output: prd.md
- Status: [pending | complete | failed]
- Approved by: [user name]
- Approved at: [timestamp]

### Summary
[Describe what was completed, decisions made, next steps]
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
routing_decision_method: diagnosis_primary_soft_context
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
  review_discovery_findings: "User reviews and approves discovery findings"
  review_opportunity_map: "User reviews and approves opportunity mapping"
  review_prd: "User reviews and approves product requirements"
gate_behavior:
  default: pause_for_user_decision
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
created_at: "2026-05-19T17:00:00Z"
```
