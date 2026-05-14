# Usage Research Report (Scenario: False-Routing Strong Product Language)

## 1. Scenario Tested
- **Scenario Name**: False-Routing Strong Product Language
- **Raw Fog**: "I want to create a product strategy workflow for AI apps. I need this repo to help me decide what product artifact to generate first, how to pick between roadmap, PRD, customer research, and prompt handoff, and how to avoid choosing the wrong skill too early."
- **Primary Risk**: High "Keyword Gravity" pull toward domain implementation artifacts (PRD, Roadmap) instead of meta-workflow engineering.

## 2. Expected Behavior
- **Object Under Pressure**: Must identify `workflow-registry.yaml` or the repo's skill selection boundary.
- **Problem Under the Problem**: Correctly identifies that the user is building a "process" using the repo.
- **Discipline**: Resists the urge to draft a Roadmap or PRD.

## 3. Actual Behavior
- **Outcome**: Success. The framing correctly prioritized the repository's internal registry over the domain keywords.
- **Artifacts Produced**:
    - `problem_frame.md`: Identified `workflow-registry.yaml` as the OUP.
    - `unknowns_map.md`: Flagged "Registry Gap" as the primary unknown.

## 4. What Worked
- **Orchestration Shield**: The internal logic correctly identified that the user's mention of "workflow" and "avoiding wrong skill" meant the problem was about orchestration, not product.
- **Counterfactual Awareness**: The reasoning explicitly addressed why starting a PRD would be premature.

## 5. Friction Points
- **Redundancy**: Some overlap between the Frame's success condition and the Map's stopping rule.
- **Search Seed Precision**: The search seed for the registry could have been more specific (targeting the `drafting` section).

## 6. Handoff Quality
- **Score**: 3/3
- **Evidence**: `unknowns_map.md` Path 2: "Compare the user's requested sequence... against the existing drafting ecosystem in `skill-registry.yaml`."

## 7. Routing Quality
- **Score**: 3/3
- **Evidence**: The recommended next artifact was an "Unknowns Map" focused on repository gaps, not a product artifact.

## 8. Recommended Skill Edits
### [problem-framer](skills/problem-framer/SKILL.md)
- **Implemented**: Added "Orchestration Shield" to explicitly protect against domain keyword gravity in process-heavy requests.

### [unknowns-mapper](skills/unknowns-mapper/SKILL.md)
- **Implemented**: Added "Registry Search Seed" requirement to force grounded searching in meta-sensemaking tasks.

## 9. Next Test
- **Scenario**: "False Routing: Broken Registry". Test how the pipeline behaves when the `workflow-registry.yaml` is mentioned but contains malformed or missing entries for the requested domain.
