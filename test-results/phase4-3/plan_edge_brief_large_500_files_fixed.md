# Workflow Orchestration Plan

## 1. Brief Consumed

**Repository**: (from brief)
**Primary Fog Type**: product_fog
**Source Brief**: test-results/phase4-3/edge_brief_large_500_files.md

---

## 2. System Recommendation

Based on fog type classification:
- Fog Type: `product_fog`
- Recommended Workflow: `product-implementation-workflow`
- Escalation Recommended: true
- Brief Recommended: `full-fog-workflow`

---

## 3. Workflow Selection

**Selected Workflow**: `full-fog-workflow`
**Routing Decision Method**: `escalation_recommended_accepted`
**Routing Divergence**: true

---

## 4. Why This Workflow

The `full-fog-workflow` is designed to address product_fog by:
- Identifying the root cause of the identified problem
- Producing diagnostic outputs and implementation artifacts
- Preparing the repository for the next phase of work

---

## 5. Workflow Steps

The selected workflow includes the following steps:

| Step | Skill | Input | Output | Gate | Description |
|------|-------|-------|--------|------|-------------|
| 1 | problem-framer | — | problem_frame | review_problem_frame |  |
| 2 | unknowns-mapper | problem_frame | unknowns_map | review_unknowns_map |  |
| 3 | repo-sensemaker | — | repository_sensemaking_brief | review_diagnosis |  |
| 4 | workflow-planner | repository_sensemaking_brief | workflow_orchestration_plan | review_orchestration_plan |  |

---

## 6. Execution Mode

**Recommended Mode**: `plan_only`
**Auto-Invocation**: Enabled (workflow runtime will read `recommended_workflow_id` and invoke next workflow)

---

## 7. Approval Gates

Steps in this workflow include approval gates. Each gate requires user or automated approval before proceeding.

---

## 8. Next Steps

After this plan is approved and executed:
1. Execute the selected workflow (`full-fog-workflow`)
2. Produce diagnostic/implementation artifacts
3. Continue to Phase 3 implementation (if applicable)

---

## 9. Escalation Handling

If the selected workflow encounters issues:
- Attempted fixes will be recorded in validation logs
- Escalation will occur after 3 failed attempts
- Escalation messages will include detailed error context and suggested next steps

---

## 10. Decision Rationale

The routing decision was made using `escalation_recommended_accepted`:
- System recommendation based on fog type: `product-implementation-workflow`
- Brief recommendation: `full-fog-workflow`
- Selected workflow: `full-fog-workflow`
- Divergence detected: true

---

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
primary_fog_type: product_fog
chosen_workflow_id: full-fog-workflow
routing_decision_method: escalation_recommended_accepted
routing_divergence: true
escalation_recommended: true
auto_escalation_allowed: false
created_at: "2026-05-25T05:32:32.390624Z"
immutable: true
workflow_steps:
  - step_id: 1
    skill: problem-framer
    input_artifact: null
    output_artifact: problem_frame
    gate: review_problem_frame
    description: ""
  - step_id: 2
    skill: unknowns-mapper
    input_artifact: problem_frame
    output_artifact: unknowns_map
    gate: review_unknowns_map
    description: ""
  - step_id: 3
    skill: repo-sensemaker
    input_artifact: null
    output_artifact: repository_sensemaking_brief
    gate: review_diagnosis
    description: ""
  - step_id: 4
    skill: workflow-planner
    input_artifact: repository_sensemaking_brief
    output_artifact: workflow_orchestration_plan
    gate: review_orchestration_plan
    description: ""
```
