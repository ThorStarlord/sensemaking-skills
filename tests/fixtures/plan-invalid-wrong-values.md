# Workflow Orchestration Plan (Invalid - Wrong Values)

## 1. Overview

This is an invalid workflow orchestration plan with wrong data types and enum values.

## 2. Fog Type

**Primary Fog Classification**: unknown_fog_type

This is not a valid fog type.

## 3. Chosen Workflow

**Workflow ID**: nonexistent-workflow-xyz

This workflow does not exist in the registry.

## 4. Workflow Steps

**Steps**: "This should be an array, not a string"

## 13. Machine-readable handoff

```yaml
artifact_id: workflow_orchestration_plan
primary_fog_type: unknown_fog_type
chosen_workflow_id: nonexistent-workflow-xyz
routing_decision_method: automated
workflow_steps: "This should be an array, not a string"
created_at: 2026-05-25T10:30:00Z
```
