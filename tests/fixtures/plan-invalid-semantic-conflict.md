# Workflow Orchestration Plan (Invalid - Semantic Conflict)

## 1. Overview

This is a plan with misaligned primary_fog_type and chosen_workflow_id without manual_override routing.

## 2. Fog Type and Workflow

**Primary Fog Classification**: product_fog (product requirement fog)
**Chosen Workflow**: ui-implementation-workflow (misaligned - should be product-implementation-workflow)

The workflow choice does not align with the fog type, unless routing_decision_method is manual_override.

## 13. Machine-readable handoff

```yaml
artifact_id: workflow_orchestration_plan
primary_fog_type: product_fog
chosen_workflow_id: ui-implementation-workflow
routing_decision_method: automated
workflow_steps:
  - step_id: step-1
    skill: clarify-requirements
    input_artifact: repository_sensemaking_brief
    output_artifact: clarified_requirements
    gate: null
    description: Clarify vague product requirements
created_at: 2026-05-25T10:30:00Z
```
