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
    - **Meta-Sensemaking**: Stop when we have identified a specific workflow ID from the registry that matches the user's intent with evidence.
5. **Handoff Readiness Check**: Before finalizing, verify that the map is ready for the next skill (typically `repo-sensemaker` or `prompt-handoff`).
    - **Rule**: Ensure the map provides a clear `Object Under Pressure` or `Search Seed`.
    - **Rule**: Ensure at least one concrete research path exists for each high-impact risk.
    - **Rule**: Ensure the `Stopping Rule` is verifiable and not a tautology.
    - **Rule**: Identify any required repository context or artifact input needed for the next step.
- **Grounding Rules**:
    - **Registry Search Seed**: For any meta-sensemaking task (where the OUP is a registry or workflow), the mapper MUST provide a specific "Search Seed" targeting the relevant entry or section of that file.
    - **Handoff Contract Verification**: Before finalizing, explicitly check if the map satisfies the input artifacts and context required for the next recommended skill (e.g., if Step 3 is `repo-sensemaker`, ensure a `Search Seed` exists).

## Output Format
Every response must follow the [Unknowns Map](references/unknowns-map-template.md) structure.

**CRITICAL**: When invoked as part of a workflow, write the final Unknowns Map to:
```
artifacts/unknowns_map.md
```

This is the standard artifact path for this skill's output.

### Generating Routing Signals (REQUIRED)

Before finalizing, you MUST:

1. **Count unknowns**: Each `### Unknown:` section header = 1 unknown. Total count all sections under "Unknowns" categories.
2. **Count assumptions**: Each distinct assumption or "Assumptions to Validate" item = 1 assumption.
3. **Assess clarity**:
   - `"critical"` = Problem statement is ambiguous or contested (0-3 knowns, >15 unknowns)
   - `"low"` = Major gaps exist (4-6 knowns, 10-15 unknowns)
   - `"medium"` = Some clarity but gaps remain (7-10 knowns, 5-9 unknowns)
   - `"high"` = Clear problem space (10+ knowns, <5 unknowns)
4. **Calculate research_needed**: `true` if `unknowns_count >= 5` OR `clarity_assessment in ("low", "critical")`, else `false`

Then append this YAML block exactly at the end of the artifact:

```
---

## Routing Signals

```yaml
clarity_assessment: "medium"
unknowns_count: 12
assumptions_count: 5
research_needed: true
```
```

Do not skip this section. Orchestration systems depend on these signals to route downstream work.

## Routing Signals
The unknowns-mapper produces four machine-readable routing fields that guide downstream workflow execution:

- **clarity_assessment** (`high`, `medium`, `low`): A judgment call on how well-defined the problem frame is. Low clarity indicates the problem space is contested, ambiguous, or has multiple valid interpretations.
- **unknowns_count** (integer): Total number of explicitly identified unknowns in the map.
- **assumptions_count** (integer): Total number of unverified assumptions that could block progress.
- **research_needed** (boolean): A signal to the router about whether additional research/sensemaking skills should be inserted into the workflow.

**Routing Heuristic (provisional):**
```
research_needed = (unknowns_count >= 5) OR (clarity_assessment == "low")
```

This heuristic is empirically validated in early runs and refined based on outcomes:
- If `research_needed` is `true`, the router inserts additional discovery, sensemaking, or diagnostic skills before implementation.
- If `research_needed` is `false`, the map is deemed sufficiently detailed for immediate action.

**Responsibility Boundary:**
- unknowns-mapper makes the clarity judgment and counts unknowns/assumptions based on available evidence.
- The router (workflow executor) reads `research_needed` and inserts research skills into the plan as needed.

## Boundary Rule
Do not perform the research yourself. Your job is to map the gaps and define the paths, not to travel them.

## References
- [Unknowns Map Template](references/unknowns-map-template.md)
