# Unknowns Map

## 1. Knowns
- The repository uses a centralized `workflow-registry.yaml` to define "useful AI workflows."
- The `workflow-planner` skill is the consumer of this registry.
- The user's intent is to move from "messy ideas" (raw fog) to "useful AI workflows."
- A `problem_frame.md` has been generated, identifying the `workflow-registry.yaml` as the Object Under Pressure.

## 2. Unknowns
- Does the `workflow-registry.yaml` contain a specific workflow for "cold starts" or "sensemaking"?
- What are the mandatory input artifacts (e.g., repo brief, unknowns map) required by the candidate workflow?
- Is there a "Sensemaking Pipeline" workflow that chains these skills?

## 3. Assumptions
- We assume the `workflow-registry.yaml` contains an entry that matches the "messy idea to workflow" intent.
- We assume the `repo-sensemaker` skill is a prerequisite for any meaningful orchestration in this repository.

## 4. Risks
- **Registry Mismatch**: No workflow explicitly addresses the "cold start" phase, requiring manual skill chaining.
- **Dependency Gap**: The selected workflow might require a `repo_sensemaking_brief.md` which has not yet been grounded in the current repo state.

## 5. Research Paths
- **Search Seed**: `skills/workflow-orchestrator/references/workflow-registry.yaml` -> Search for keywords: `sensemaking`, `pipeline`, `cold-start`, `research`.
- **Handoff Verification**: Check if the `repo-sensemaker` skill provides the necessary `recommended_workflow_id` for the orchestrator.

## 6. Stopping Rule
Stop when the `workflow-registry.yaml` has been searched and at least one workflow ID matching the "sensemaking" or "initial research" intent has been identified with its required input contracts.

## 7. Search Seed
`skills/workflow-orchestrator/references/workflow-registry.yaml`
