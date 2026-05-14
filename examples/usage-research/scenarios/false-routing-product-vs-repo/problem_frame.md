# Problem Frame (Scenario: False-Routing Product vs Repo)

## 1. Raw Fog
"I want this repo to help me launch better AI products faster. Right now I have lots of ideas, but I don’t know which workflow to use, what artifact should come first, or when to hand off to another skill."

## 2. Problem Under the Problem
The user's high-level desire for "product velocity" is masked by a foundational struggle with the **sensemaking meta-workflow**. The technical tension is not in the product domain, but in the repository's own **discovery and routing layer**.

## 3. Object Under Pressure
`workflow-registry.yaml` and the `workflow-orchestrator` skill selection logic.

## 4. Failure Mode
**Premature Domain Routing**: The system takes the "product" keywords at face value and routes the user to a Product Manager skill (e.g., creating a PRD). This results in "garbage in, garbage out" because the user hasn't yet framed their specific idea within the repository's sensemaking capabilities.

## 5. Success Condition
The user reaches a state where they can map a specific "idea" to a concrete workflow in `workflow-registry.yaml` with a clear understanding of the input/output artifact sequence.

## 6. What Must Be True
- The `workflow-registry.yaml` must be sufficiently documented to allow for disambiguation.
- The user must understand the difference between "sensemaking" (deciding what to do) and "implementation" (doing the domain work).

## 7. Next Artifact
Unknowns Map (focused on repository capabilities vs. user intent gaps).
