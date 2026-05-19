# Unknowns Map

## 1. Knowns
- The user's intent is to bridge the gap between "messy ideas" and "AI workflows".
- The `workflow-registry.yaml` is the core registry defining executable orchestration paths.
- The repository uses a multi-step sensemaking pipeline (Problem Frame -> Unknowns Map -> Repo Brief).
- A `repo-sensemaker` skill exists to ground the analysis in the repository's state.

## 2. Unknowns
- Which workflow IDs in `workflow-registry.yaml` are designed for initial "idea to workflow" transitions?
- What are the specific input requirements for the downstream `workflow-planner`?
- Are there any skills in the registry currently marked as `draft` that are being incorrectly considered for this workflow?

## 3. Assumptions
- We assume the `workflow-registry.yaml` is the single source of truth for orchestration logic.
- We assume the `repo-sensemaker` skill is capable of resolving the specific technical boundaries identified in the Problem Frame.
- We assume "messy ideas" can be atomized into a single primary workflow rather than requiring multiple parallel branches.

## 4. Risks
- **Registry Drift**: The `workflow-registry.yaml` might refer to skill IDs that have been renamed or deleted.
- **Semantic Over-fitting**: The `unknowns-mapper` might define research paths that are too specific to the "AI workflows" domain, ignoring general repository health.
- **Handoff Failure**: The `repo-sensemaker` might not receive enough evidence from the search seeds to validate the success conditions defined in the Problem Frame.

## 5. Research Paths
- **Path 1**: Scan `workflow-registry.yaml` for keywords like "cold-start", "sensemaking", or "workflow-generation" to identify candidate IDs.
- **Path 2**: Inspect `skills/repo-sensemaker/SKILL.md` to verify its artifact consumption contract (specifically for `problem_frame` and `unknowns_map`).
- **Path 3**: Verify the existence and status of skills referenced in the candidate workflows within `skill-registry.yaml`.

## 6. Stopping Rule
**Meta-Sensemaking**: Research is complete when we have identified a concrete `workflow_id` from the registry that satisfies the "Success Condition" of the Problem Frame, backed by evidence from the registry and skill logic.
