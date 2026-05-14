# Usage Research Report (Subset Run)

## 1. Scenario Tested
**Scenario**: A first-time user with a vague idea: "I want this repo to help me turn messy ideas into useful AI workflows."
**Workflow**: `full-local-sensemaking` (Steps 1 & 2 only).
**Objective**: Evaluate if recent improvements reduced handoff friction and improved routing clarity.

## 2. What Worked
- **Improved Semantic Guarding**: The addition of `Object Under Pressure` in `problem-framer` forced a transition from abstract desire to concrete system boundaries.
- **Actionable Exit Criteria**: The `Stopping Rule` in `unknowns-mapper` provided a measurable definition of "done" for the sensemaking phase.
- **Contract Enforcement**: The hardened V1 contracts effectively blocked any drift during the transition from Frame to Map.
- **Formal Subset Orchestration**: This run triggered the formalization of `subset_run` semantics, allowing research-mode runs to stay contract-valid without weakening the main workflow registry.

## 3. Friction Points
- **Recursive Definitions**: The `Problem Under the Problem` field can still feel redundant with `Failure Mode` if the "Fog" is extremely simple.
- **Stop Rule Tautology**: There is a risk of the agent writing a stopping rule that simply restates the research paths (e.g., "Stop when the research paths are complete").

## 4. Hard-to-fill Fields
- **Object Under Pressure**: For a non-technical user, identifying a specific registry or file might be difficult. However, for an agentic pair-programmer, it is a powerful "Search Seed."
- **What Must Be True**: This field often overlaps with `Knowns` in the next step, causing some redundancy in the handoff.

## 5. Validation Friction
- No significant friction found with `scripts/validate-artifact.py`. 
- **Validation Evidence**: The orchestration plan was successfully validated using:
  `python scripts/validate-plan.py examples/workflow-orchestrator/subset-run-full-local-sensemaking.md`
- **Result**: PASSED. Subset validation logic correctly identified and verified the included steps.

## 6. Handoff Quality
- **Comparison to Previous Run**: The previous run (3298b853) lacked a specific "Search Seed." This run's `problem_frame` produced a clear target (`workflow-registry.yaml`), which significantly improves the starting point for Step 3 (`repo-sensemaker`).
- **Context Sufficiency**: Step 3 now has enough context because it can combine the `Object Under Pressure` (Filter) and the `Stopping Rule` (Boundary) with the actual `repository_state`.

## 7. Recommended Skill Edits
- **Skill**: `unknowns-mapper`
- **Edit**: Add a "Handoff Contract Verification" field to the template to explicitly check if the map satisfies the inputs of the next step (Step 3).

## 8. Next Test
- Test a "False Routing" scenario where the user provides fog that *looks* like a product problem but is actually a repo setup problem, to see if `Object Under Pressure` catches the mismatch.
