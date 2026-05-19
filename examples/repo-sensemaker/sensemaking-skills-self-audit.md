# Example: Repository Sensemaking Brief (sensemaking-skills)

## 1. Repository goal
Standardize repository diagnosis and orchestration through a meta-layer of sensemaking skills.

## 2. Current shape
- `skills/`: `repo-sensemaker` and `workflow-planner`.
- `workflows/`: Composite chains for execution.
- `examples/`: Validation fixtures for both skills.
- `scripts/`: Automated governance.

## 3. Strong signals
The split between Diagnosis and Orchestration is successfully implemented. Machine-readable registries and templates are in place.

## 4. Missing pieces
- Complete skill coverage in `skill-registry.yaml`.
- Documented packaging validation process.

## 5. Improvement opportunities
Consolidate all templates into a top-level `templates/` directory to improve reuse across skills.

## 6. Weakest boundary
The handoff contract between the two skills is currently the most fragile point, as it relies on the model correctly parsing the machine-readable YAML block.

## 7. Evidence
- [SKILL.md](../../skills/repo-sensemaker/SKILL.md): Mentions the handoff but lacks a hard schema check.
- [repo-analysis-template.md](../../skills/repo-sensemaker/references/repo-analysis-template.md): Section 12 is a new addition and unproven in automated tests.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/SKILL.md
    lines: L21-L23
    quote: "The output of this skill is a diagnostic artifact"
    supports_claim: "Diagnosis/Action boundary exists."
```

## 9. Why this boundary matters
What breaks if this remains weak.

## 10. Candidate next steps
1. Implement registry parity validation in `scripts/validate-repo.py`.
2. Add a negative fixture for unsafe orchestration.
3. Polish skill frontmatter.

## 11. Recommended next step
Implement registry parity validation to ensure all workflow steps are registered.

## 12. Recommended workflow
`docs-contract-reconciliation`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: guided_execution
weakest_boundary: registry-parity
required_inputs:
  - repository_sensemaking_brief
```

## 13. Ready-to-copy prompt
```markdown
/workflow-orchestrator

Brief: [Link to this brief]
Target: Harden the registry parity.
Mode: guided_execution
```

## Expected Behavior Checklist
- [x] Identifies the "Weakest Boundary" as the handoff contract.
- [x] Cites specific file evidence in Section 7.
- [x] Includes the machine-readable YAML block in Section 12.
- [x] Recommends a specific workflow from the registry.
