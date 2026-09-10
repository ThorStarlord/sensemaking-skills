# Customer Discovery artifact contracts

## Authority

For the current PM pilot, the concise human contracts live beside each canonical Skill at `skills/<skill>/references/output-contract.md`. `scripts/validate-pm-artifact.py` is the deterministic specialized validator used by the canonical validation router for the five artifact identities below.

This current PM validation contract is intentionally narrower and stronger than the historical Wayfinder entries that still appear in `skills/workflow-planner/references/artifact-contracts.yaml`. Those historical entries preserve compatibility/provenance; they are not the current PM semantic authority.

## Routed artifact identities

- `persona_definition`
- `discovery_findings`
- `synthesis_report`
- `opportunity_map`
- `hypothesis_statement`

`scripts/validate-and-report.py` routes exactly those identities to `validate-pm-artifact.py`; unrelated artifact routing remains unchanged.

## Deterministic scope

The validator may check required sections and machine fields, allowed representation states, unique IDs, local source-reference relationships, frequency arithmetic, and the declared opportunity-score formula.

It may not decide whether a persona is representative, a finding is important, an opportunity should be prioritized, or a hypothesis is strategically correct.

## Admission boundary

`ArtifactAdmissionService` invokes the canonical router over an immutable snapshot. A valid PM artifact therefore produces an admission receipt bound to:

- exact artifact bytes;
- `validate-and-report.py` bytes;
- `validate-pm-artifact.py` bytes;
- exact structured validation result.

`artifact admitted != PM conclusion warranted` remains unchanged.
