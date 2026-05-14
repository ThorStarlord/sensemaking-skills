# Usage Research Report (Scenario: Cold Start Messy AI Workflows)

## 1. Scenario Tested
- **Scenario Name**: Cold Start Messy AI Workflows
- **Raw Fog**: "I want this repo to help me turn messy ideas into useful AI workflows."
- **Workflow**: `full-local-sensemaking` (Steps 1 & 2 only).
- **Objective**: Evaluate if recent improvements reduced handoff friction and improved routing clarity for first-time users.

## 2. Expected Behavior
- **Object Under Pressure**: Should target a specific registry (e.g., `workflow-registry.yaml`) or documentation file.
- **Stopping Rule**: Should provide a measurable definition of "done" for the sensemaking phase.
- **Transition**: Should move smoothly from Problem Frame to Unknowns Map without context loss.

## 3. Actual Behavior
- **Outcome**: Success. The agent successfully navigated the transition and identified the repository's own structure as the initial bottleneck.
- **Artifacts Produced**:
    - `problem_frame.md`: Produced a clear target (`workflow-registry.yaml`).
    - `unknowns_map.md`: Provided actionable research paths.

## 4. What Worked
- **Improved Semantic Guarding**: The addition of `Object Under Pressure` in `problem-framer` forced a transition from abstract desire to concrete system boundaries.
- **Actionable Exit Criteria**: The `Stopping Rule` in `unknowns-mapper` provided a measurable definition of "done" for the sensemaking phase.

## 5. Friction Points
- **Recursive Definitions**: The `Problem Under the Problem` field can still feel redundant with `Failure Mode` if the "Fog" is extremely simple.
- **Stop Rule Tautology**: Risk of the agent writing a stopping rule that simply restates the research paths.

## 6. Handoff Quality
- **Score**: 3/3
- **Evidence**: Step 3 now has enough context because it can combine the `Object Under Pressure` (Filter) and the `Stopping Rule` (Boundary) with the actual `repository_state`.

## 7. Routing Quality
- **Score**: 3/3
- **Evidence**: Correctly routed to `repo-sensemaker` after the mapping phase, grounding the work in repository evidence.

## 8. Recommended Skill Edits
- **Skill**: `unknowns-mapper`
- **Edit**: Add a "Handoff Contract Verification" field to the template to explicitly check if the map satisfies the inputs of the next step.

## 9. Next Test
- **Scenario**: "False Routing: Product vs Repo". Test if the pipeline can distinguish between domain requests and repository navigation requests.
