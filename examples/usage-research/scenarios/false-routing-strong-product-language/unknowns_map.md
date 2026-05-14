# Unknowns Map (Scenario 003)

## 1. Knowns
- User's goal: Create a "product strategy workflow".
- User's constraint: Avoid premature skill selection.
- Target artifacts: Roadmap, PRD, Customer Research, Prompt Handoff.

## 2. Unknowns
- **Registry Gap**: Does `workflow-registry.yaml` currently contain any "Drafting" workflows that overlap with these artifacts?
- **Skill Availability**: Are there specialized skills in the repo (or external) for "Customer Research" or "Roadmap" generation?

## 3. Assumptions
- We assume the user is looking for a **meta-workflow** (a sequence of skills) rather than a single atomic action.
- we assume the user's mention of "AI apps" implies specific requirements for prompt engineering artifacts.

## 4. Risks
- **Keyword Gravity (High)**: The agent might ignore the "workflow" part of the request and start generating a PRD for an "AI app."
- **Contract Mismatch**: Designing a workflow that calls skills that don't exist or have incompatible I/O artifacts.

## 5. Research Paths
- **Path 1: Skill Audit**: Search the `skills/` directory for any metadata related to "roadmap" or "research".
- **Path 2: Registry Comparison**: Compare the user's requested sequence (Roadmap -> PRD -> etc) against the existing `drafting` ecosystem in `skill-registry.yaml`.

## 6. Stopping Rule
Stop when we have mapped the user's requested artifacts to either:
1.  Existing skills in `skill-registry.yaml`.
2.  Newly defined skill stubs (if they don't exist).
...and the resulting sequence is documented in a `proposed-product-strategy-workflow.yaml` file.
