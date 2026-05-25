# Workflow Orchestration Plan

**Repository**: test-repo

## 1. Brief Consumed
Primary Fog Type: architecture_fog

## 2. System Recommendation
architecture-implementation-workflow

## 3. Workflow Selection
Selected: architecture-implementation-workflow

## 4. Why This Workflow
For architecture diagnosis.

## 5. Workflow Steps
| Step | Skill | Input | Output | Gate |
|------|-------|-------|--------|------|
| 1 | analyzer | brief | analysis | review |

## 6. Execution Mode
plan_only

## 7. Approval Gates
Review gates included.

## 8. Next Steps
Execute workflow.

## 9. Escalation Handling
Per standard procedures.

## 10. Decision Rationale
Standard routing.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
primary_fog_type: architecture_fog
chosen_workflow_id: architecture-implementation-workflow
routing_decision_method: diagnosis_primary_soft_context
routing_divergence: false
escalation_recommended: false
auto_escalation_allowed: false
created_at: "2026-05-25T07:22:00Z"
immutable: true
workflow_steps:
  - step_id: 1
    skill: analyzer
    input_artifact: brief
    output_artifact: analysis
    gate: review
    description: Analysis step
```

