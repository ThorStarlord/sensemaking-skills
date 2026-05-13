# Example: Unknowns Map (Vague Automation)

## 1. Knowns
- The repo has a `repo-analysis-template.md`.
- `workflow-orchestrator` has a `workflow-registry.yaml`.
- The user wants more automation.

## 2. Unknowns
- Does the current agent environment support YAML parsing within Markdown blocks for these specific skills?
- What are the most common workflows that actually need this automation?

## 3. Assumptions
- We assume that adding a YAML block to the brief won't break existing human-readability.
- We assume that the `workflow-orchestrator` can reliably extract this block.

## 4. Risks
- Adding too much machine-readable "noise" to the brief might make it less useful for human review.
- The orchestrator might fail to parse the YAML and fallback to a less-safe prose-based guess.

## 5. Research Paths
- Test the agent's ability to parse nested YAML in a mock sensemaking session.
- Review existing `repo-sensemaker` outputs to see where a YAML block fits best.

## 6. Stopping Rule
Research is complete once we have a verified YAML schema for the handoff and a successful test parse by the orchestrator.

## Expected Behavior Checklist
- [x] Separates verified knowns from assumptions.
- [x] Identifies parsing reliability as a key risk.
- [x] Defines a clear research path for YAML validation.
- [x] Provides a concrete stopping rule.
