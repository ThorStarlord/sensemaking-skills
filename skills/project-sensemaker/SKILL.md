---
name: project-sensemaker
description: turn vague project uncertainty into a clear problem frame, knowledge map, candidate paths, and recommended next skill or concrete next step. use when the user does not yet know whether the work is product, architecture, research, validation, implementation, documentation, strategy, or routing.
---

# project-sensemaker

Turns vague project uncertainty into a clear problem frame, identifies missing knowledge, recommends a downstream skill, and produces a concrete next-step prompt.

## Description
Use when the user is unsure what they are building, lacks enough domain knowledge to choose a direction, needs to map unknowns across multiple disciplines, or wants to convert a rough idea into a grillable goal, research plan, prototype prompt, PRD seed, issue plan, or validation target.

## Core Philosophy
`project-sensemaker` does not solve the project. It makes the project answerable.

## Workflow

1. **Capture**: Accept the vague idea or "foggy" thought.
2. **Translate**: Convert it into a problem statement and identify the "object under pressure" (e.g., Spec Package, User Flow, API Contract).
3. **Map**: Identify required knowledge areas and separate Knowns, Unknowns, and Assumptions.
4. **Research**: Perform high-leverage research (web or repo) to clear the most critical blockers. **Rule**: Do not perform broad research by default. Identify bounded research paths unless missing knowledge blocks routing.
5. **Route**: Match the problem type to a skill ecosystem (Interface Skills, Matt Skills, PM Skills).
6. **Recommend**: Pick the smallest concrete next step.
7. **Prompt**: Generate a ready-to-copy prompt for the next skill.

## Boundary Rule
Do not complete the downstream work by default. Do not write the PRD, build the validator, create issues, implement code, or generate a full architecture proposal unless the user explicitly asks. The default job is to classify the fog, map missing knowledge, recommend the next step, and produce a strong prompt.

## Stopping Rule
Stop researching once you can produce one of:
- A grillable goal
- A prototype comparison
- A PRD seed
- A small issue plan
- A validator rule proposal
- A decision that the idea is premature

## Output Format
Every response must follow the [Sensemaking Brief](references/output-template.md) structure.

## References
- [Skill Registry](references/skill-registry.yaml)
- [Fog Types](references/fog-types.md)
- [Routing Rules](references/routing-rules.md)
- [Output Template](references/output-template.md)

