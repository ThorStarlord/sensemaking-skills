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
  - file: skills/repo-sensemaker/SKILL.md
    lines: 18
    quote: "The output of this skill is a diagnostic artifact"
    supports_claim: "Diagnosis/Action boundary exists."
  - file: skills/repo-sensemaker/SKILL.md
    lines: 25-30
    quote: "Diagnose Codebase: Analyze the code structure to determine what fog type the actual problems require"
    supports_claim: "The skill performs codebase diagnosis."
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
Workflow: full-local-sensemaking
Mode: guided_execution
```
