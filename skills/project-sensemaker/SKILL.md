# project-sensemaker

Turns vague project uncertainty into a clear problem frame, identifies missing knowledge, recommends a downstream skill, and produces a concrete next-step prompt.

## Description
Use when the user is unsure what they are building, lacks enough domain knowledge to choose a direction, needs to map unknowns across multiple disciplines, or wants to convert a rough idea into a grillable goal, research plan, prototype prompt, PRD seed, issue plan, or validation target.

## Workflow

1. **Capture**: Accept the vague idea or "foggy" thought.
2. **Translate**: Convert it into a problem statement and identify the "object under pressure" (e.g., Spec Package, User Flow, API Contract).
3. **Map**: Identify required knowledge areas and separate Knowns, Unknowns, and Assumptions.
4. **Research**: Perform high-leverage research (web or repo) to clear the most critical blockers.
5. **Route**: Match the problem type to a skill ecosystem (Interface Skills, Matt Skills, PM Skills).
6. **Recommend**: Pick the smallest concrete next step.
7. **Prompt**: Generate a ready-to-copy prompt for the next skill.

## Stopping Rule
Stop researching once you can produce one of:
- A grillable goal
- A prototype comparison
- A PRD seed
- A small issue plan
- A validator rule proposal
- A decision that the idea is premature

## Output Format

Every response must follow this structure:

### 1. Raw Idea
What was initially proposed.

### 2. Likely Underlying Problem
The pain or failure mode hiding underneath.

### 3. Subject Map
The disciplines or knowledge areas involved.

### 4. Known / Unknown / Assumed
A table separating facts, gaps, and guesses.

### 5. Research Paths
2–5 highest-leverage paths to explore.

### 6. Findings
Synthesis of research or internal documentation.

### 7. Candidate Directions
2–4 possible next moves (e.g., "Add a run manifest", "Update 00-index.md").

### 8. Weakest Boundary
The part of the system that is most ambiguous or unproven.

### 9. Smallest Useful Next Step
One concrete artifact or action.

### 10. Next Skill Prompt
A ready-to-copy prompt for `grill-me`, `grill-with-docs`, `prototype`, `to-prd`, `to-issues`, or `tdd`. 

For deep implementation, recommend the [Autonomous Sprint](file:///h:/GithubRepositories/sensemaking-skills/workflows/autonomous-sprint.md) composite workflow.

## References
- [Skill Registry](file:///h:/GithubRepositories/sensemaking-skills/skills/project-sensemaker/references/skill-registry.yaml)
- [Fog Types](file:///h:/GithubRepositories/sensemaking-skills/skills/project-sensemaker/references/fog-types.md)
- [Routing Rules](file:///h:/GithubRepositories/sensemaking-skills/skills/project-sensemaker/references/routing-rules.md)
