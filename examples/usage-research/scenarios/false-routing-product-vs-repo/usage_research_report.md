# Usage Research Report (Scenario: False-Routing Product vs Repo)

## 1. Scenario Tested
- **Scenario Name**: False-Routing Product vs Repo
- **Raw Fog**: "I want this repo to help me launch better AI products faster. Right now I have lots of ideas, but I don’t know which workflow to use, what artifact should come first, or when to hand off to another skill."
- **Primary Risk**: Premature handoff to a domain-specific skill (e.g., `product-manager`) due to keyword gravity ("Product", "Launch").

## 2. Expected Behavior
- **Object Under Pressure**: Should identify the `workflow-registry.yaml` or the `skill-selection-boundary` as the bottleneck.
- **Routing**: Should avoid `to-prd` or `to-issues` and instead stay in meta-sensemaking or repo-audit.
- **Discipline**: Should acknowledge that the "Product" talk is noise compared to the "Workflow" confusion.

## 3. Actual Behavior
- **Outcome**: Success. The agent correctly identified that the primary friction point is the repository's own usage, not the product's strategy.
- **Artifacts Produced**:
    - `problem_frame.md`: Correctly identified `workflow-registry.yaml` as the Object Under Pressure.
    - `unknowns_map.md`: Correctly flagged "User Intent Mapping" as the critical unknown.

## 4. What Worked
- **Object-Proxy Rule**: The requirement to identify an "inspectable proxy" for conceptual objects (like "onboarding flow" or "workflow confusion") forced the agent to name a file (`workflow-registry.yaml`), which grounded the reasoning.
- **Semantic Stability**: The prompt's emphasis on "Problem Under the Problem" helped peel back the "Product" layer to find the "Workflow" layer.

## 5. Friction Points
- **Keyword Gravitation**: The term "AI Product" is highly evocative. In 1/3 internal tests, the agent still attempted to mention a "Product Roadmap" in the Success Definition, showing that domain keywords still bleed into the framing.
- **Registry Obscurity**: If the `workflow-registry.yaml` isn't prominently mentioned in the `repository_state`, the agent might struggle to name it as the OUP.

## 6. Handoff Quality
- **Score**: 3/3
- **Evidence**: The resulting `unknowns_map` provides a clear search seed for `repo-sensemaker`: "Locate all workflows in `workflow-registry.yaml` that accept `Raw Fog` or `Idea` as an input."

## 7. Routing Quality
- **Score**: 3/3
- **Evidence**: The recommended next step is "Registry Audit" rather than "PRD Creation." This saves the user from starting a heavy product workflow for a task that is actually about repo setup.

## 8. Recommended Skill Edits
### [problem-framer](file:///h:/GithubRepositories/sensemaking-skills/skills/problem-framer/SKILL.md)
- **Add Rule**: "Domain Keyword Guard: If the user uses domain-heavy keywords (e.g., 'Product', 'Engineering', 'Marketing') but explicitly mentions confusion about 'how to start', 'which workflow', or 'where to go', the `Object Under Pressure` MUST be the repository's own routing or registry files."
- **Example**: Add a "False Routing" example to the references.

### [unknowns-mapper](file:///h:/GithubRepositories/sensemaking-skills/skills/unknowns-mapper/SKILL.md)
- **Add Example**: Add a `Stopping Rule` example specifically for meta-sensemaking: "Stop when we have identified a specific workflow ID from the registry that matches the user's intent with evidence."

## 9. Next Test
- **Scenario**: "False Routing: Missing Repository State". Test how the framer behaves when the user is confused about workflows but the `repository_state` (provided as input) is empty or malformed.
