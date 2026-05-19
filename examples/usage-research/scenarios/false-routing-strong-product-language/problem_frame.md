# Problem Frame (Scenario 003)

## 1. Raw Fog
"I want to create a product strategy workflow for AI apps. I need this repo to help me decide what product artifact to generate first, how to pick between roadmap, PRD, customer research, and prompt handoff, and how to avoid choosing the wrong skill too early."

## 2. Problem Under the Problem
The user is attempting to perform **meta-workflow engineering**. They aren't just asking for a product strategy; they are asking for the repository to help them *define the process* of product strategy. The core tension is between **domain implementation** (writing a PRD) and **workflow orchestration** (deciding the sequence of skills).

## 3. Object Under Pressure
`workflow-registry.yaml` and the `workflow-planner` skill-selection boundary.

## 4. Failure Mode
**premature-implementation-loop**: The system interprets "product strategy" as a direct command to start a PRD workflow, thereby choosing the wrong skill "too early"—exactly what the user said they wanted to avoid.

## 5. Success Condition
A new entry is added to `workflow-registry.yaml` (or an existing one is selected) that explicitly defines the "Product Strategy" sequence of artifacts, with validated input/output contracts.

## 6. What Must Be True
- The `workflow-planner` must support recursive or user-defined workflow definitions.
- The user must provide evidence for *why* one artifact should precede another in their specific context.

## 7. Next Artifact
Unknowns Map (focused on the gaps in the current `workflow-registry.yaml` regarding product strategy workflows).
