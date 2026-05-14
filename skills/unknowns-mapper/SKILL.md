---
name: unknowns-mapper
description: separate knowns, unknowns, assumptions, and risks for a given problem frame or repository. use when a project is starting and research paths need to be defined.
---

# unknowns-mapper

Produces an **Unknowns Map** to separate what we know from what we are guessing. This skill prevents premature implementation by making the "information gaps" visible.

## Workflow
1. **Intake**: Review the Problem Frame or Repository goal.
2. **Classification**:
    - **Known**: Facts backed by code or documentation.
    - **Unknown**: Explicitly missing information.
    - **Assumed**: Beliefs treated as facts but not yet verified.
    - **Risk**: Potential failures or blockers.
3. **Pathfinding**: Define "Research Paths" to convert unknowns/assumptions into knowns.
    - **Rule**: Each critical assumption or risk should map to at least one research path.
4. **Stopping Rules**: Define when research should stop (to prevent rabbit holes).
    - **Weak**: Stop when we understand the problem.
    - **Strong**: Stop when we have checked 3 core files and identified the next workflow with evidence.
5. **Handoff Readiness Check**: Before finalizing, verify that the map is ready for the next skill (typically `repo-sensemaker` or `prompt-handoff`).
    - **Rule**: Ensure the map provides a clear `Object Under Pressure` or `Search Seed`.
    - **Rule**: Ensure at least one concrete research path exists for each high-impact risk.
    - **Rule**: Ensure the `Stopping Rule` is verifiable and not a tautology.
    - **Rule**: Identify any required repository context or artifact input needed for the next step.

## Output Format
Every response must follow the [Unknowns Map](references/unknowns-map-template.md) structure.

## Boundary Rule
Do not perform the research yourself. Your job is to map the gaps and define the paths, not to travel them.

## References
- [Unknowns Map Template](references/unknowns-map-template.md)
