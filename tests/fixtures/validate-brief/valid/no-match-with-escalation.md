---
validator_case: positive
---
# Example: Repository Sensemaking Brief — truthful no-match (escalated)

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
No supported downstream workflow can be recommended with confidence from this repository evidence. Logic trace: the evidence establishes the boundary but does not support any registry workflow recommendation, so the brief escalates instead of naming a closest match.

## 10. Candidate next steps
1. Create a `shared-vocabulary.md` reference.
2. Add a `validator-tdd` run to implement a brief-to-plan contract.

## 11. Recommended next step
Escalate: no workflow recommendation is supported by the repository evidence.

## 12. Recommended workflow
null

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/SKILL.md: Mentions the handoff but lacks a hard schema check."
recommended_workflow_id: null
recommended_execution_mode: plan_only
escalation_recommended: true
weakest_boundary: manual-handoff
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-08-14T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
Escalate: no downstream workflow is recommended by this brief (ADR 0014 no-match state).
```
