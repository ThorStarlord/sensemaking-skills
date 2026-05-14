# Hidden Expected Behavior (Scenario 003)

Despite the heavy use of "Product Strategy", "Roadmap", and "PRD", the core problem is still **Workflow Selection and Sequencing within the Sensemaking Repository**.

## Success Criteria
1.  **Object Under Pressure**: Must identify the repository's internal workflow logic (e.g., `workflow-registry.yaml` or `skill-registry.yaml`).
2.  **Problem Under the Problem**: Identifying that the user is trying to build a "Product Strategy Workflow" *using* this repo, which requires first understanding how this repo structures such meta-workflows.
3.  **Failure Mode (Counterfactual)**: A failure occurs if the agent routes to a `product-manager` skill to *write* a PRD or Roadmap, instead of a `repo-sensemaker` or `orchestrator` skill to *define* the workflow.
4.  **Stopping Rule**: Must be tied to the successful selection of a workflow ID from the registry.
