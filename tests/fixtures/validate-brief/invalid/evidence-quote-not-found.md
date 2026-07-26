---
validator_case: negative
expected_error_contains: "EVIDENCE_QUOTE_NOT_FOUND"
---
# Repository Sensemaking Brief (Evidence Quote Not Found)

The cited `file`/`lines` location is real, but the `quote` text does not
actually occur there (or within the fixed grounding window). This is a
deterministic evidence-integrity defect and must remain blocking (issue #80).

## 1. Repository goal
Test that an ungrounded evidence quote is rejected.

## 2. Current shape
Fixture layout.

## 3. Strong signals
Fixture-driven testing.

## 4. Missing pieces
N/A

## 5. Improvement opportunities
N/A

## 6. Weakest boundary
Zero Validation: the cited evidence quote does not exist at the cited location.

## 7. Evidence
- `skills/repo-sensemaker/references/weakness-types.md:1` is cited, but the quote below does not match its content.

Logic trace: the cited file and line exist, but the quoted text was
fabricated, which is exactly what EVIDENCE_QUOTE_NOT_FOUND must catch.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L1
    quote: "This sentence does not appear anywhere near line 1 of that file."
    supports_claim: "Deliberately ungrounded citation for the negative fixture."
```

## 9. Why this boundary matters
An ungrounded quote could be fabricated or miscited, undermining trust in the brief.

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
  - "skills/repo-sensemaker/references/weakness-types.md: deliberately ungrounded citation"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: ungrounded-quote
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-26T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
N/A -- test fixture.
