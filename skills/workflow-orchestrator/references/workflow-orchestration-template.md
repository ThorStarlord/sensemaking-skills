# Workflow Orchestration Plan

## 1. Brief consumed
Short summary of the `repo-sensemaker` diagnosis, including fog type classification.

## 1.5. Problem classification (fog type)
The primary type of uncertainty identified:
- **product_fog**: Vague user needs, feature requirements unclear
- **ui_fog**: Navigation or screen design issues
- **docs_fog**: Missing documentation, knowledge gaps
- **architecture_fog**: Code structure, design boundary issues (default)

This determines which implementation workflow will be automatically invoked.

## 2. Chosen workflow
Name of the workflow.

## 3. Why this workflow
Why it fits the weakest boundary.

## 4. Skills in sequence
Ordered chain of skills to be used.

## 5. Inputs and outputs
What each skill receives and produces.

## 6. Approval gates
Where the user must approve before continuing.

## 7. Stop conditions
When to stop instead of continuing.

## 8. Execution mode
`plan_only` / `prompt_chain` / `guided_execution` / `autonomous_execution`.

## 9. Prompt chain
Ready-to-copy prompts (if applicable).

## 10. Run log template
How to record what happened during the execution.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
fog_type: # product_fog, ui_fog, docs_fog, or architecture_fog
recommended_implementation_workflow: # optional override (e.g., product-implementation-workflow, ui-implementation-workflow, docs-implementation-workflow, or implementation-workflow). If omitted, orchestrator routes based on fog_type.
chosen_workflow_id: 
execution_mode: 
steps:
  - id: 
    skill: 
    step_type: 
    gate: 
    input_artifact: 
    input_source: 
    output_artifact: 
```
