# Problem Frame

## 1. Raw Fog
"I want this repo to help me turn messy ideas into useful AI workflows."

## 2. Problem Under the Problem
The user lacks a structured methodology for converting high-entropy concepts ("messy ideas") into low-entropy, executable machine instructions ("AI workflows"). The core tension is the translation gap between human intuition and agentic execution.

## 3. Object Under Pressure
`workflow-registry.yaml`

(Grounding: Per the Orchestration Shield rule, since the user is focused on "workflows", the primary inspectable proxy is the registry that defines these executable paths.)

## 4. Failure Mode
The agent produces "hallucinated" workflows that use non-existent skills, skip critical validation gates, or fail to produce auditable handoff artifacts, leading to unreliable automation.

## 5. Success Condition
A raw input file ("Fog") can be autonomously transformed into a valid, executable `workflow_orchestration_plan.md` that passes all repository-level validation scripts.

## 6. What Must Be True
- The repository contains a curated set of stable, verified skills.
- The `workflow-registry.yaml` contains correct metadata for all available workflows.
- Artifact contracts between skills (e.g., Problem Frame -> Unknowns Map) are strictly enforced by validators.

## 7. Next Artifact
`unknowns_map.md`
