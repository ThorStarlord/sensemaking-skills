---
validator_case: negative
expected_error_contains: "INVALID_LINE_FORMAT"
---
# Repository Sensemaking Brief (Descriptive Evidence Lines)

Reproduces the exact style of the six `INVALID_LINE_FORMAT` failures recorded
in the live PR #52 evidence: descriptive substitutes such as "Entire skill
file" and "Routing accuracy section" written into `lines`, instead of a
concrete line number or range.

## 1. Repository goal
Test that descriptive (non-numeric) evidence lines are rejected.

## 2. Current shape
- `skills/`: sensemaking pipeline.
- `scripts/`: governance.

## 3. Strong signals
The pipeline separates diagnosis from action.

## 4. Missing pieces
- Prompt guidance previously allowed "if possible" line citations.

## 6. Weakest boundary
Contract Mismatch: producer guidance allowed descriptive line references that the validator rejects.

## 7. Evidence
`skills/repo-sensemaker/references/evidence-rules.md` previously said line numbers were optional ("if possible").

Logic trace: producer guidance and validator grammar disagreed, so a model following the guidance in good faith produced a rejected artifact.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/evidence-rules.md
    lines: Entire skill file
    quote: "Mention the specific file and line numbers (if possible)"
    supports_claim: "Descriptive line references were previously permitted."
  - file: skills/repo-sensemaker/SKILL.md
    lines: Routing accuracy section
    quote: "Registry Grounding"
    supports_claim: "Routing rules existed but line citation format was unconstrained."
```

## 9. Why this boundary matters
Descriptive citations cannot be mechanically verified against the file.

## 10. Candidate next steps
1. Require the strict line-number grammar in evidence-rules.md.

## 11. Recommended next step
Update evidence-rules.md.

## 12. Recommended workflow
docs-implementation-workflow

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: docs_fog
evidence:
  - "skills/repo-sensemaker/references/evidence-rules.md: previously allowed descriptive line citations"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: evidence_line_format_disagreement
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-25T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner
Brief: [Link to this brief]
Workflow: docs-implementation-workflow
Mode: guided_execution
```
