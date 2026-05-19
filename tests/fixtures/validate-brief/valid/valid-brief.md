---
validator_case: positive
---
# Example: Repository Sensemaking Brief (sensemaking-skills)

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
  - file: skills/repo-sensemaker/SKILL.md
    lines: L21-L23
    quote: "The output of this skill is a diagnostic artifact"
    supports_claim: "Diagnosis/Action boundary exists."
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
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: guided_execution
weakest_boundary: manual-handoff
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner

Brief: [Link to this brief]
Target: Harden the contract between repo-sensemaker and workflow-planner.
Workflow: validator-tdd
Mode: guided_execution
```
