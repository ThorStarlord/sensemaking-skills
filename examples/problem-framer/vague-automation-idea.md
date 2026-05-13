# Example: Problem Frame (Vague Automation Idea)

## 1. Raw Fog
"I think this repo needs more automation, but I am not sure what kind."

## 2. Problem Under the Problem
The repository has defined a two-skill architecture (Diagnosis and Orchestration), but the actual handoff between these skills is still manual and non-deterministic. The "lack of automation" is specifically a lack of contract enforcement between diagnosis and action.

## 3. Object Under Pressure
The handoff contract between `repo-sensemaker` and `workflow-orchestrator`.

## 4. Failure Mode
The orchestrator guesses the wrong workflow or mode because the brief was ambiguous, leading to unsafe execution or user frustration.

## 5. Success Condition
A machine-readable section in the Sensemaking Brief that the orchestrator can parse to select the correct workflow and mode without ambiguity.

## 6. What Must Be True
- `repo-sensemaker` must support YAML output sections.
- `workflow-orchestrator` must prioritize these sections over prose.

## 7. Next Artifact
Unknowns Map

## Expected Behavior Checklist
- [x] Captures the raw idea accurately.
- [x] Identifies the structural "handoff" as the real problem.
- [x] Defines success as a machine-readable contract.
- [x] Recommends Unknowns Map as the next artifact.
