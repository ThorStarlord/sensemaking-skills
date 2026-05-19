# Repository Sensemaking Brief

## 1. Repository goal
Standardize the creation and maintenance of agentic skills and workflows via auditable artifacts.

## 2. Current shape
- `skills/`: Atomic logic units.
- `skill-registry.yaml`: Registration of all available skills.
- `workflow-registry.yaml`: Registration of orchestrated paths.

## 3. Strong signals
- **Structured Registration**: `skill-registry.yaml` contains metadata like `produced_artifacts` and `consumed_artifacts`.
- **Validation Suite**: `scripts/validate-repo.py` checks for registry/filesystem consistency.

## 4. Missing pieces
- **Skill Scaffolding Skill**: No atomic skill currently exists to "scaffold" a new skill directory (though templates might exist).
- **Interactive Triage**: The gap between "I want a new skill" and "Here is the PR" requires a high-level triage step.

## 5. Improvement opportunities
- Create a `skill-creator` skill that automates directory and `SKILL.md` production.

## 6. Weakest boundary
**Skill Promotion/Registration**: The link between creating a file in `skills/` and updating `skill-registry.yaml` is a manual, unenforced boundary.

## 7. Evidence
- Registry file: `skill-registry.yaml` (L1-L10).
- Validation script: `scripts/validate-repo.py` (L15-L25).

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skill-registry.yaml
    lines: L1-L10
    quote: "skills:\n  - id: problem-framer\n    name: problem-framer"
    supports_claim: "Skills must be manually registered in this YAML file."
  - file: scripts/validate-repo.py
    lines: L100-L110
    quote: "def validate_registries(repo_root):"
    supports_claim: "The repository uses a central script to verify registry consistency."
```

## 9. Why this boundary matters
If a skill is created but not registered, the `workflow-planner` cannot see it. If registered incorrectly, the entire pipeline fails during autonomous execution.

## 10. Candidate next steps
- Run the `skill_maintenance_workflow` to prepare the registration patch.
- Research existing skill templates in `skills/`.

## 11. Recommended next step
Execute `workflow-planner` to plan the "New Skill Addition" using the `skill_maintenance_workflow`.

## 12. Recommended workflow
`skill_maintenance_workflow`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: skill_maintenance_workflow
recommended_execution_mode: plan_only
weakest_boundary: skill_registration_process
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
Plan the addition of a new skill using the `skill_maintenance_workflow`. Focus on creating a valid `SKILL.md` and updating `skill-registry.yaml` to include the new artifact IDs.
