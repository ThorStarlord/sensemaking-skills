# Usage Research Report (Subset Run: Full Local Sensemaking)

## 1. Scenario Tested
- **Scenario Name**: Subset Run Full Local Sensemaking
- **Raw Fog**: "I want this repo to help me turn messy ideas into useful AI workflows."
- **Workflow**: `full-local-sensemaking` (Steps 1 & 2 only).
- **Objective**: Evaluate if recent improvements reduced handoff friction and improved routing clarity for first-time users.

## 2. Expected Behavior
- **Object Under Pressure**: Should target a specific registry (e.g., `workflow-registry.yaml`).
- **Stopping Rule**: Should provide a measurable definition of "done."
- **Success Criteria**: The user identifies a specific workflow entry point with evidence.

## 3. Actual Behavior
- **Outcome**: Success. The agent correctly peeling back the "intent" layer to find the "registry" layer.
- **Artifacts Produced**:
    - `problem_frame.md`: Produced a clear target (`workflow-registry.yaml`).
    - `unknowns_map.md`: Provided actionable research paths.

## 4. What Worked
- **Improved Semantic Guarding**: The addition of `Object Under Pressure` in `problem-framer` forced a transition from abstract desire to concrete system boundaries.
- **Contract Enforcement**: The hardened V1 contracts effectively blocked any drift during the transition from Frame to Map.

## 5. Friction Points
- **Recursive Definitions**: The `Problem Under the Problem` field can still feel redundant with `Failure Mode` if the "Fog" is extremely simple.
- **Stop Rule Tautology**: Risk of the agent writing a stopping rule that simply restates the research paths.

## 6. Handoff Quality
- **Score**: 3/3
- **Evidence**: `problem_frame` produced a clear target (`workflow-registry.yaml`), which significantly improves the starting point for Step 3.

## 7. Routing Quality
- **Score**: 3/3
- **Evidence**: Correctly routed to `repo-sensemaker` after the mapping phase, grounding the work in repository evidence.

## 8. Recommended Skill Edits
- **Skill**: `unknowns-mapper`
- **Edit**: Add a "Handoff Contract Verification" field to the template to explicitly check if the map satisfies the inputs of the next step.

## 9. Next Test
- **Scenario**: "False Routing: Product vs Repo". Test if the pipeline can distinguish between domain requests and repository navigation requests.
