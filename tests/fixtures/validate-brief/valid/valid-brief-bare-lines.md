---
validator_case: positive
---
# Example: Repository Sensemaking Brief (bare-number evidence lines)

This fixture is identical in structure to valid-brief.md but cites evidence using
bare line numbers (e.g. `18`, `25-30`) instead of the `Lx`/`Lx-Ly` form. Bare line
numbers are a valid, semantically-complete line reference and no consumer depends
on the `L` prefix, so the validator must accept them.

## 1. Repository goal
Turn vague project uncertainty into clear problem frames, research paths, and next-step prompts.

## 2. Current shape
- `skills/`: Five-skill sensemaking pipeline (`problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-planner`, `prompt-handoff`).
- `scripts/`: Automated governance.

## 3. Strong signals
The five-skill pipeline provides a high-leverage diagnostic frame. The separation of "diagnosis" from "action" protects the repo's core intent.

## 4. Missing pieces
- Automated parity tests for the new five-skill architecture.

## 5. Improvement opportunities
Consolidate shared references into a root `references/` directory to avoid duplication.

## 6. Weakest boundary
Contract Mismatch: The linkage between `repo-sensemaker` output and `workflow-planner` input is currently manual rather than contract-enforced.

## 7. Evidence
- [SKILL.md](../../skills/repo-sensemaker/SKILL.md): Mentions the handoff but lacks a hard schema check.

Logic trace: the template defines the handoff shape but no automated check enforces workflow ID accuracy, so the brief-to-plan boundary is the weakest link.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: 5
    quote: "1. **Vocabulary Drift**: Terms used in the README don't match the code or directory structure."
    supports_claim: "Confirms Vocabulary Drift is a registered weakness type."
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: 6-7
    quote: "2. **Contract Mismatch**: Files claim to be one format (e.g., `.yaml`) but are actually another (e.g., Markdown)."
    supports_claim: "Confirms Contract Mismatch is a registered weakness type."
```

## 9. Why this boundary matters
If the brief doesn't explicitly name a workflow ID, the orchestrator might guess the wrong path, leading to unsafe or irrelevant execution.

## 10. Candidate next steps
1. Create a `shared-vocabulary.md` reference.
2. Add a brief-to-plan contract check.

## 11. Recommended next step
Implement the `full-local-sensemaking` workflow to harden the contract between the two skills.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
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
Workflow: full-local-sensemaking
Mode: guided_execution
```
