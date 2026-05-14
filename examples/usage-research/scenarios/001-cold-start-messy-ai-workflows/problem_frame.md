# Problem Frame

## 1. Raw Fog
"I want this repo to help me turn messy ideas into useful AI workflows."

## 2. Problem Under the Problem
The "Cognitive-to-Canonical Gap": A first-time user has high-level strategic intent but lacks the mental model of the repository's internal skill contracts. The "messy idea" is often a compound statement of desire that needs to be atomized before it can be routed to specific skills.

## 3. Object Under Pressure
The `workflow-registry.yaml` and the `repo-sensemaker` skill boundary. Specifically, how "raw fog" is mapped to a specific workflow ID without requiring the user to know the registry exists.

## 4. Failure Mode
"Semantic Drift / Hallucinated Orchestration": The system accepts the messy idea but selects a workflow that is either too complex (over-engineering) or too simple (missing the point), leading to a prompt handoff that fails because the downstream agent doesn't have the context it needs.

## 5. Success Condition
A user can enter a vague idea and consistently arrive at Step 3 (`repo-sensemaker`) with a `problem_frame` and `unknowns_map` that correctly isolate the "weakest boundary" in their specific repository context.

## 6. What Must Be True
- The `problem-framer` must prioritize "The Problem Under the Problem" over technical solutions.
- The `Object Under Pressure` must be a specific file, registry, or workflow node.
- The `handoff` between Step 1 and Step 2 must be machine-verifiable.

## 7. Next Artifact
Unknowns Map
