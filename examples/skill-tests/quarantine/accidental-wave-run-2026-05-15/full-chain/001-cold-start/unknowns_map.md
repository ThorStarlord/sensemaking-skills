# Unknowns Map

## 1. Knowns
- Target: Adding a new skill.
- Core Registry: `skill-registry.yaml`.
- Success: Valid skill directory and registry entry.

## 2. Unknowns
- Is there a specific "Skill Creator" or "Scaffold" skill available?
- What are the mandatory "Artifact Contracts" the new skill must satisfy?
- Where are the skill templates or examples located?

## 3. Assumptions
- We assume the user has a specific logic in mind for the new skill.
- We assume the `skill-registry.yaml` is the only file requiring registration.

## 4. Risks
- **Contract Mismatch**: The new skill produces artifacts that don't match the consumer's expectations.
- **Namespace Collision**: The new skill ID conflicts with an existing one.

## 5. Research Paths
- **Path 1**: Search for "template" or "scaffold" in the `skills/` directory.
- **Path 2**: Audit `skill-registry.yaml` to see the metadata requirements for existing stable skills.
- **Path 3**: Check `skills/workflow-orchestrator/references/artifact-contracts.yaml` for potential output IDs.

## 6. Stopping Rule
**Meta-Sensemaking**: Stop when a "Skill Scaffolding" workflow or template has been identified and the next step in the `skill_maintenance_workflow` is confirmed.
