---
validator_case: negative
expected_error_contains: "NO_EVIDENCE_FILE_CITATIONS"
---
# Repository Sensemaking Brief (Missing File Citations)

## 1. Repository goal
Test that missing file citations in Evidence section is detected.

## 2. Current shape
Standard fixture layout.

## 3. Strong signals
Fixture-driven testing.

## 4. Missing pieces
No file-level citations in the Evidence section.

## 5. Improvement opportunities
Add automated checks.

## 6. Weakest boundary
Zero Validation: No validator checks for file citations in the Evidence section.

## 7. Evidence
The Evidence section here has no file paths with extensions. This makes it impossible for a reviewer to verify the claims against actual source files. Logic trace: file citations are the primary mechanism for grounding diagnostic claims.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: tests/fixtures/validate-brief/invalid/no-file-citations.md
    lines: L1-L5
    quote: "frontmatter metadata"
    supports_claim: "Fixture structure is valid."
```

## 9. Why this boundary matters
Without file citations, the brief's claims cannot be independently verified, reducing reviewability.

## 10. Candidate next steps
- Add file citation check to validate-brief.py.

## 11. Recommended next step
Add the check and a negative fixture.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: zero-validation
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
Add file citation validation.
