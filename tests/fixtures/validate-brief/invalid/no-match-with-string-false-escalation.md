---
validator_case: negative
expected_error_contains: MISSING_WORKFLOW_ID
---
# Example: Repository Sensemaking Brief — null workflow id with string "false" escalation

## 1. Repository goal
Turn vague project uncertainty into clear problem frames, research paths, and next-step prompts.

## 2. Current shape
- `skills/`: Five-skill sensemaking pipeline (`problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-planner`, `prompt-handoff`).
- `workflows/`: Experimental high-velocity chains.
- `examples/`: Validation fixtures for diagnosis and orchestration.
- `scripts/`: Automated governance.

## 3. Strong signals
The five-skill pipeline provides a high-leverage diagnostic frame.

## 4. Missing pieces
- Automated parity tests for the new five-skill architecture.

## 5. Improvement opportunities
Consolidate shared references (like `skill-registry.yaml`) into a root `references/` directory.

## 6. Weakest boundary
Contract Mismatch: The linkage between `repo-sensemaker` output and `workflow-planner` input.

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
A quoted `escalation_recommended: "false"` string must not enable the no-match gate: only unambiguous truthy values do. Logic trace: the strict boolean parser treats "false" as false, so null without escalation is a contract violation.

## 10. Candidate next steps
1. Create a `shared-vocabulary.md` reference.

## 11. Recommended next step
Name a supported workflow or set escalation_recommended to true.

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
escalation_recommended: "false"
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
Name a supported workflow or set escalation_recommended: true.
```
