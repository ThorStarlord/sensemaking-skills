---
validator_case: positive
---
# Repository Sensemaking Brief (Unrecognized Weakness Type -- Warning Only)

This fixture used to be `invalid/unknown-weakness-type.md`, which asserted that
an unregistered weakness type was a BLOCKING `UNKNOWN_WEAKNESS_TYPE` error.
PR #78 was correctly rejected under that then-current structural contract;
the rejection exposed the brittleness of prose-substring taxonomy validation
(the substantive diagnosis in PR #78 was never audited and remains neither
confirmed nor disproven). That blocking check is retired (issue #80). Under
the redesigned contract (D2/D3), an unrecognized `weakness_type` value is
non-blocking metadata: the validator emits a `WEAKNESS_TYPE_UNKNOWN` warning
but the artifact stays valid=true and the validator exits 0. This fixture
proves that.

## 1. Repository goal
Test that an unrecognized structured weakness_type value produces a non-blocking warning, not a validation failure.

## 2. Current shape
Standard fixture layout.

## 3. Strong signals
Fixture-driven testing.

## 4. Missing pieces
None relevant to this fixture.

## 5. Improvement opportunities
Add automated checks.

## 6. Weakest boundary
Hyperdimensional Coupling: The resonance between the repository's ambient entropy and the skill's fractal abstraction layer creates an unbridgeable ontological gap.

## 7. Evidence
- `tests/fixtures/validate-brief/valid/unrecognized-weakness-type-warning.md` uses a made-up type. Logic trace: the weakness type key "Hyperdimensional Coupling" is not in the recognized types list, which is why this fixture exists to prove that condition is a warning, not a blocking error.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L1
    quote: "# Weakness Types in Repositories"
    supports_claim: "Confirms the registered taxonomy file this fixture deliberately does not match."
```

## 9. Why this boundary matters
Unrecognized weakness types are still surfaced to a human reviewer via a warning, even though they no longer block the artifact.

## 10. Candidate next steps
- None; this is a fixture, not a real diagnosis.

## 11. Recommended next step
None.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md: registered taxonomy the fixture deliberately does not match"
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: hyperdimensional-coupling
weakness_type: Hyperdimensional Coupling
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-26T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
N/A -- validator fixture only.
