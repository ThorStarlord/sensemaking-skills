---
validator_case: negative
expected_error_contains: "value 'integration_fog'"
---
# Example: Repository Sensemaking Brief (integration_fog)

## 1. Repository goal
Turn vague project uncertainty into clear problem frames, research paths, and next-step prompts.

## 2. Current shape
- `skills/`: Five-skill sensemaking pipeline (`problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-planner`, `prompt-handoff`).
- `workflows/`: Experimental high-velocity chains.
- `examples/`: Validation fixtures for diagnosis and orchestration.
- `scripts/`: Automated governance.

## 3. Strong signals
The five-skill pipeline provides a high-leverage diagnostic frame. The separation of "diagnosis" from "action" protects the repo's core intent.

## 4. Missing pieces
- Automated parity tests for the new five-skill architecture.
- More diverse "Weakness Types" examples (e.g., Vocabulary Drift).

## 5. Improvement opportunities
Consolidate shared references (like `skill-registry.yaml`) into a root `references/` directory to avoid duplication.

## 6. Weakest boundary
Contract Mismatch: The linkage between `repo-sensemaker` output and `workflow-planner` input. It is currently manual and "vibe-based" rather than contract-enforced.

## 7. Evidence
- [SKILL.md](../../skills/repo-sensemaker/SKILL.md): Mentions the handoff but lacks a hard schema check.
- [repo-analysis-template.md](../../skills/repo-sensemaker/references/repo-analysis-template.md): Section 12 is a new addition and unproven in automated tests.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L6
    quote: "2. **Contract Mismatch**: Files claim to be one format (e.g., `.yaml`) but are actually another (e.g., Markdown)."
    supports_claim: "Confirms Contract Mismatch is a registered weakness type."
```

## 9. Why this boundary matters
If the brief doesn't explicitly name a workflow ID, the orchestrator might guess the wrong path, leading to unsafe or irrelevant execution. Logic trace: the template defines the handoff shape but no automated check exists to enforce workflow ID accuracy.

## 10. Candidate next steps
1. Create a `shared-vocabulary.md` reference.
2. Add a `validator-tdd` run to implement a brief-to-plan contract.

## 11. Recommended next step
Implement the `full-local-sensemaking` workflow to harden the contract between the two skills.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: integration_fog
evidence:
  - "skills/repo-sensemaker/SKILL.md: Mentions the handoff but lacks a hard schema check."
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: guided_execution
weakest_boundary: manual-handoff
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-05-19T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner

Brief: [Link to this brief]
Target: Harden the contract between repo-sensemaker and workflow-planner.
Workflow: validator-tdd
Mode: guided_execution
```
