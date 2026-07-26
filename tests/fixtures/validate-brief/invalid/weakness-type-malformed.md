---
validator_case: negative
expected_error_contains: "WEAKNESS_TYPE_MALFORMED"
---
# Repository Sensemaking Brief (Malformed weakness_type)

`weakness_type` is a YAML list instead of a string. Unlike the other
taxonomy conditions (missing/unrecognized/prose-mismatch, all non-blocking
warnings per D2), a wrong YAML *type* is a structural defect and must remain
blocking.

## 1. Repository goal
Test that a malformed weakness_type field is a blocking error.

## 2. Current shape
Fixture layout.

## 3. Strong signals
Fixture-driven testing.

## 4. Missing pieces
N/A

## 5. Improvement opportunities
N/A

## 6. Weakest boundary
Zero Validation: the weakness_type field is malformed in Section 13.

## 7. Evidence
- `skills/repo-sensemaker/references/weakness-types.md:1` confirms the taxonomy file this fixture is testing against.

Logic trace: Section 13 declares weakness_type as a list rather than a
string, which is why the malformed-type check must fire.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L1
    quote: "# Weakness Types in Repositories"
    supports_claim: "Confirms the taxonomy reference file exists."
```

## 9. Why this boundary matters
A malformed taxonomy field cannot be parsed by any downstream consumer.

## 10. Candidate next steps
N/A

## 11. Recommended next step
N/A

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md: taxonomy reference"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: malformed-weakness-type
weakness_type:
  - Zero Validation
  - Safety Gaps
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-26T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
N/A -- test fixture.
