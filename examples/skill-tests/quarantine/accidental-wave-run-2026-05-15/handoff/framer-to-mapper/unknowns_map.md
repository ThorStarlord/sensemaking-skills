# Unknowns Map

## 1. Knowns
- **Core Goal**: Automate the transition from "messy ideas" to "useful AI workflows".
- **Primary Object**: `workflow-registry.yaml` is the central registry for orchestration.
- **Success Criteria**: Production of a valid `workflow_orchestration_plan.md`.
- **Repository State**: A set of "stable" skills exists, but their mapping to the user's specific "messy idea" is unproven.

## 2. Unknowns
- Which specific `workflow_id` in the registry handles "initial sensemaking" vs "domain implementation"?
- What are the required input artifacts for the `workflow-planner` to begin execution?
- Are there any broken skill references in the `workflow-registry.yaml` that would cause execution to fail?

## 3. Assumptions
- We assume the `workflow-registry.yaml` is up-to-date with current repository capabilities.
- We assume the `problem_frame` provides enough signal to distinguish between a "cold start" and a "logic maintenance" task.

## 4. Risks
- **Registry Out-of-Sync**: The registry might refer to skills that have been renamed or deleted in `skills/`.
- **Validation Blind Spot**: The `workflow-planner` might accept a plan that satisfies structural constraints but fails semantically in the specific repository context.

## 5. Research Paths
- **Path 1**: Scan `workflow-registry.yaml` for keywords like `sensemaking`, `cold-start`, or `idea` to find matching workflows.
- **Path 2**: Inspect `skills/workflow-orchestrator/references/artifact-contracts.yaml` to verify the required input sections for an orchestration plan.
- **Path 3**: Cross-reference the skills listed in candidate workflows against the contents of the `skills/` directory to ensure they exist.

## 6. Stopping Rule
**Meta-Sensemaking**: Stop when a specific `workflow_id` (e.g., `sensemaking_to_prompt`) is identified in the registry that matches the user's intent, and its required input skills are confirmed to exist in the repository.
