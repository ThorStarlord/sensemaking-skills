# Product Management artifact contracts

## Authority

Concise human contracts live beside each canonical Skill at `skills/<skill>/references/output-contract.md`. The canonical validation router selects specialized deterministic validators where PM machine-contract invariants add value.

Historical Wayfinder entries in `skills/workflow-planner/references/artifact-contracts.yaml` preserve compatibility/provenance. They do not become semantic authority merely because an identifier is reused.

## Customer Discovery routed identities

`scripts/validate-pm-artifact.py` validates:

- `persona_definition`
- `discovery_findings`
- `synthesis_report`
- `opportunity_map`
- `hypothesis_statement`

It checks mechanically decidable representation/evidence-shape contracts such as required sections/fields, allowed statuses, unique IDs, source-reference relationships, frequency arithmetic, and declared opportunity-score arithmetic.

It may not decide whether a persona is representative, a finding is important, an opportunity should be prioritized, or a hypothesis is strategically correct.

## Feature Definition routed identities

`scripts/validate-pm-feature-definition.py` validates:

- `story_list`
- `criteria_list`
- `risk_analysis`

### `story_list`

The machine contract preserves:

- one bounded source artifact reference;
- aggregate scope status (`approved`, `proposed`, or `mixed`);
- unique story identities;
- user/capability intent (`actor` where meaningful, `want`, `value`);
- source traceability;
- acceptance intent;
- dependencies;
- per-story scope status;
- unresolved questions.

The validator does not estimate effort, choose priority, or establish that a story is valuable.

### `criteria_list`

The machine contract preserves:

- one bounded source artifact reference;
- unique scenario identities;
- source story/requirement traceability;
- scenario category;
- explicit Given / When / Then behavior;
- `status: specified`;
- unresolved questions.

A criteria artifact may specify expected behavior. It cannot claim `passed`, QA approval, or automated-test execution without separate execution evidence.

### `risk_analysis`

The machine contract preserves:

- one bounded source artifact reference;
- unique risk identities;
- risk class (`tiger`, `paper_tiger`, `elephant`);
- evidence status (`observed`, `inferred`, `hypothetical`, `unknown`);
- evidence refs;
- urgency, impact, probability, mitigation, owner role, success criterion, and escalation signal;
- an agent-authored recommendation plus conditions and unresolved questions.

A purely hypothetical item cannot be encoded as a current Tiger. This is an evidence-shape constraint, not a claim that the validator knows real-world risk probability.

`go`, `go_with_conditions`, `no_go`, and `insufficient_evidence` are analysis outcomes only. They grant no launch or external-action authority.

## PRD authority

`prd` remains produced by the existing canonical `to-prd` Skill. Upstream `prd` methodology is merged into `to-prd`; no second current `prd` capability is created.

The existing PRD scope-expansion contract remains authoritative. Existing PRD validation is retained; Wave 2 does not silently replace its historical contract with a competing PM artifact identity.

## Admission boundary

`ArtifactAdmissionService` invokes the canonical router over an immutable snapshot. A routed specialized PM artifact therefore produces an admission receipt bound to:

- exact artifact bytes;
- `validate-and-report.py` bytes;
- selected specialized validator bytes;
- exact structured validation result.

`artifact admitted != PM conclusion warranted` remains unchanged.

## Qualification boundary

Passing these validators and Campaign admission may contribute to `REPOSITORY_QUALIFIED`. It does not establish native-harness qualification, portability qualification, customer truth, strategic correctness, implementation completion, test execution, or launch readiness in the real world.
