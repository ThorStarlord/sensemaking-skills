---
validator_case: negative
expected_error_contains: "HALLUCINATED_WORKFLOW_ID"
---
# Example: Real Skill ID Written Into Workflow-ID Field (Negative Fixture)

This is distinct from `repo-sensemaker-id-hallucination.md` (a purely invented
string, `wave-1-execution`). Here the value is a **real skill ID**
(`docs-aligner`, a real directory under `skills/docs-aligner/`) mistakenly
written into `recommended_workflow_id`, which requires a top-level workflow ID
from `workflow-registry.yaml`. This reproduces the exact live failure recorded
in PR #52 / issue #51.

## 1. Repository goal
Test that a real skill ID is still rejected from the workflow-ID field.

## 2. Current shape
Standard repo structure with a skills/ directory containing docs-aligner.

## 3. Strong signals
- Skill IDs and workflow IDs are namespaced separately in this repo.

## 4. Missing pieces
- Prompt guidance previously did not distinguish skill IDs from workflow IDs.

## 6. Weakest boundary
Contract Mismatch: a real skill ID can be typed into a field that requires a workflow ID with no rejection at authoring time.

## 7. Evidence
`skills/repo-sensemaker/SKILL.md` (L97-L99) previously did not distinguish skill IDs from workflow IDs.

Logic trace: docs-aligner is a legitimate skill ID, so a naive check for "is this a known identifier anywhere in the repo" would wrongly accept it; only checking against workflow-registry.yaml's top-level `id` values catches this.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/SKILL.md
    lines: L97-L99
    quote: "Registry Grounding"
    supports_claim: "Prior boundary rule did not distinguish skill IDs from workflow IDs."
```

## 9. Why this boundary matters
A skill ID substituted for a workflow ID causes orchestrator failure downstream (ARTIFACT_NOT_FOUND / no matching workflow).

## 10. Candidate next steps
1. Add explicit skill-ID vs workflow-ID guidance to SKILL.md.

## 11. Recommended next step
Add the identifier-rules section.

## 12. Recommended workflow
docs-aligner

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/SKILL.md (lines L97-L99): boundary rule lacked skill/workflow distinction"
recommended_workflow_id: docs-aligner
recommended_execution_mode: guided_execution
weakest_boundary: skill_workflow_id_ambiguity
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-25T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner
Brief: [Link to this brief]
Workflow: docs-aligner
Mode: guided_execution
```
