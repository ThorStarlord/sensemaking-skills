# Usage Research Report: Scenario 004 (Broken Registry)

## 1. Scenario Tested
Testing whether the agent can distinguish between "User Intent Confusion" and "Registry Malformation" when a specific workflow request fails.

## 2. Expected Behavior
Agent identifies `workflow-registry.yaml` as the Object Under Pressure (OUP) and identifies the missing fields in the `product-discovery-sprint` entry.

## 3. Actual Behavior
The agent incorrectly concluded that the user's "Raw Fog" was too vague and suggested re-running `problem-framer`, despite the user citing a specific (albeit broken) workflow by name.

## 4. What Worked
- Agent correctly identified that the user was in the "Product" ecosystem.

## 5. Friction Points
- **Registry Blindness**: The agent assumed that if a workflow failed, it must be because the user didn't have enough "domain context", rather than checking the registry's structural integrity.
- **Over-Correction**: The agent defaulted to "more framing" as a universal fix for execution errors.

## 6. Handoff Quality
- Poor. The handoff back to `problem-framer` was a dead end because the user had already completed that step.

## 7. Routing Quality
- **FAIL**. Routed to `problem-framer` instead of a registry audit.

## 8. Recommended Skill Edits
- **skill-maintainer**: Propose a `Registry Defect Guard` for the `problem-framer` to ensure that if a specific workflow name is mentioned, the registry is checked for defects before asking for more fog clarification.

## 9. Next Test
Rerun Scenario 004 after applying registry diagnostics.
