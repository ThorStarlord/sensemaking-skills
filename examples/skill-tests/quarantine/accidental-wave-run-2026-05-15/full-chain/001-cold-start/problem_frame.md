# Problem Frame

## 1. Raw Fog
"I want to add a new skill to this repo."

## 2. Problem Under the Problem
The user wants to extend the repository's capabilities but lacks clarity on the "Skill Contract" requirements and the registry registration process. The tension is between decentralized development and centralized orchestration stability.

## 3. Object Under Pressure
`skill-registry.yaml`

## 4. Failure Mode
The new skill is added without a valid `SKILL.md`, or it is registered with incorrect metadata in the registry, leading to routing failures in the `workflow-planner`.

## 5. Success Condition
A new skill directory exists with a valid `SKILL.md`, and a corresponding entry is added to `skill-registry.yaml` that passes `validate-repo.py`.

## 6. What Must Be True
- There is a template for new skills.
- The `skill-registry.yaml` structure is known.
- The `workflow-planner` can recognize the new skill ID.

## 7. Next Artifact
`unknowns_map.md`
