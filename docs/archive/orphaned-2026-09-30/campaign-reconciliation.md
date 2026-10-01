# Campaign reconciliation lifecycle

**Status:** P9 product contract  
**Scope:** deterministic inspection of admitted reconciliation evidence and explicit Campaign disposition state

## Purpose

P9 connects the repository's existing reconciliation/repair-verification artifacts to the durable Sensemaking Campaign lifecycle without turning those artifacts into a semantic router.

The product question is:

> Which admitted reconciliation or repair-verification reports exist, and has an explicit agent-authored Campaign transition consumed each exact report yet?

P9 deliberately does **not** answer:

> What should the Campaign do because of the report?

That remains the active coding agent's semantic responsibility.

## Product surface

P9 adds:

```text
sensemaking-skills campaign reconciliation \
  --workspace /path/to/CMP-0001 \
  [--json]
```

The command is read-only.

It does not create reconciliation work, invoke a Skill, repair the repository, mutate Campaign state, or author a transition.

## Existing concepts reused

P9 introduces no new semantic artifact type.

It reuses:

- P4 `ArtifactAdmission` receipts;
- P4 content-addressed admitted artifacts;
- P5 explicit agent-authored `advance`, `defer`, and `close` transitions;
- P6 capability metadata for reconciliation responsibilities;
- P8 evidence identity and transition-consumption lineage;
- existing `reconciliation_report` artifact identity;
- existing `repair_verification_report` artifact identity.

## Reconciliation responsibilities

### `output-reconciler`

Existing responsibility type:

```text
output_reconciliation
```

Existing output artifact:

```text
reconciliation_report
```

The Skill may classify claims such as:

```text
verified
disputed
omitted
```

Those classifications are evidence for agent judgment. They are not Campaign transition instructions.

### `repair-verifier`

Existing responsibility type:

```text
repair_verification
```

Existing output artifact:

```text
repair_verification_report
```

The Skill may record:

```text
findings_closed
findings_remaining
```

Those findings are evidence for agent judgment. They are not automatic terminal/continuation states.

## Required control shape

```text
bounded work / durable work claim
        ↓
AGENT decides reconciliation is warranted
        ↓
reconciliation capability produces report
        ↓
P4 validates + admits exact report
        ↓
P9 reports disposition_required
        ↓
AGENT interprets report
        ↓
explicit P5 advance / defer / close
        ↓
P8 binds exact report consumption
        ↓
P9 reports disposition_recorded
```

Optional authorized repair/repair-verification can occur between reconciliation and final disposition, but P9 does not infer or invoke it.

## P9 read model

Each admitted reconciliation report is represented by mechanically verifiable facts:

```text
artifact_id
artifact_ref
artifact_sha256
admission receipts
validator identities
validation timestamps
validation-result digests
disposition_status
disposition_required
bound transition IDs
legacy-unbound transition IDs
```

P9 does not parse the report prose/YAML to determine a recommended action.

## Artifact eligibility

A report enters P9 only when P8 reconstructs it as an `admitted_artifact` whose P4 `artifact_id` is one of:

```text
reconciliation_report
repair_verification_report
```

Therefore:

```text
file named reconciliation_report.md
!= reconciliation evidence
```

and:

```text
file under artifacts/
!= admitted reconciliation evidence
```

P4 admission remains the trust boundary.

## Disposition states

P9 exposes three mechanical states.

### `disposition_required`

```text
admitted reconciliation artifact
+ no committed transition cites the exact artifact through a P8 bound edge
= disposition_required
```

This means only that no exact P8-bound Campaign disposition is yet represented.

It does not say what the disposition should be.

### `disposition_recorded`

```text
admitted reconciliation artifact
+ one or more committed P8 bound transition-consumption edges
= disposition_recorded
```

P9 exposes the exact transition IDs.

The transition itself remains authoritative for whether the agent advanced, deferred, or closed.

### `legacy_unbound`

A historical/direct-P2 transition may cite the report in `TransitionRecord.evidence` without a P8 exact-byte consumption receipt.

P9 reports:

```text
legacy_unbound
```

and keeps:

```text
disposition_required: true
```

because P9 cannot claim that P8 observed/bound the exact consumed bytes.

This preserves the existing P8 claim ceiling.

## Why any bound transition counts as a disposition

P9 does not attempt to interpret the type of semantic decision.

If an agent explicitly authored a valid P5 transition and cited the exact reconciliation artifact, P8 preserves that exact evidence-consumption edge.

P9 can therefore say mechanically:

```text
an explicit Campaign disposition consumed this report
```

It does not say:

```text
this was the correct disposition
```

or:

```text
reconciliation is semantically complete forever
```

## Multiple reports

Multiple admitted reports are all retained as independent durable evidence identities.

P9 orders the read model deterministically by:

```text
artifact_id
artifact_ref
```

It does **not** infer:

```text
latest
best
canonical winner
superseded
preferred
```

from timestamps or content.

Validation timestamps are provenance facts only.

If a future milestone needs explicit supersession, that relation must be represented durably rather than inferred from file order or prose.

## Report contents do not drive state

P9 must not implement rules such as:

```text
all claims verified
→ advance

one disputed claim
→ defer

all findings closed
→ goal_achieved

one finding remaining
→ external_blocker
```

Even if those strings appear in report bytes, running:

```text
campaign reconciliation
```

must leave `CampaignState` unchanged.

## Authority boundary

Reconciliation findings and recommendations do not grant repair authority.

Therefore:

```text
finding requires repair
!= repair authorized
```

The active responsibility's existing authority contract remains controlling.

P9 does not modify P6 capability availability/authority metadata.

## Relationship to P4

P4 remains authoritative for:

- validator execution;
- `valid=true` admission;
- content-addressed artifact storage;
- append-only admission receipts;
- exact artifact digest;
- validator/router/result provenance.

P9 re-loads the exact admission receipts surfaced through P8 and checks that Campaign ID, artifact ID, artifact ref, and artifact digest still agree.

It does not create a second admission mechanism.

## Relationship to P8

P8 remains authoritative for exact evidence consumption.

P9 consumes P8's reconstructed `ConsumptionEdge` records.

Only:

```text
binding_status: bound
```

can satisfy P9's `disposition_recorded` state.

A P8 `legacy_unbound` edge remains visible but cannot be promoted to an exact P9 disposition record.

P9 does not create, repair, or rewrite lineage receipts.

## Relationship to P5

P9 introduces no semantic write command.

After inspecting reconciliation state, the active agent uses the existing explicit decision surface:

```text
campaign advance
campaign defer
campaign close
```

and supplies the exact reconciliation artifact ref as evidence when it is part of the decision.

That preserves:

```text
reconciliation evidence
→ AGENT judgment
→ explicit P5 decision
→ P8 exact consumption lineage
```

rather than:

```text
reconciliation evidence
→ automatic transition
```

## JSON surface

Example shape:

```json
{
  "ok": true,
  "code": "CAMPAIGN_RECONCILIATION",
  "campaign_id": "CMP-0001",
  "report_count": 1,
  "disposition_required_count": 1,
  "disposition_recorded_count": 0,
  "legacy_unbound_count": 0,
  "reports": [
    {
      "artifact_id": "reconciliation_report",
      "artifact_ref": "artifacts/reconciliation_report/<sha>.md",
      "artifact_sha256": "<sha>",
      "admissions": [],
      "disposition_status": "disposition_required",
      "disposition_required": true,
      "bound_transition_ids": [],
      "legacy_unbound_transition_ids": []
    }
  ]
}
```

The surface deliberately contains no recommended action/capability, semantic score, inferred authority, repair authorization, or automatic transition.

## Read-only guarantee

`campaign reconciliation` must not modify:

- Campaign state;
- transition records;
- trace;
- evidence;
- P4 artifacts/admissions;
- P8 lineage snapshots/receipts;
- handoff state.

All returned values are reconstructed from existing durable Campaign facts.

## Failure behavior

P9 relies on normal P2/P4/P8 fail-closed reconstruction.

It additionally fails closed when reconciliation provenance is internally inconsistent, including:

- malformed admission refs;
- missing admission provenance for an admitted reconciliation artifact;
- admission Campaign ID mismatch;
- admission artifact ID/ref/digest disagreement with the P8 evidence identity.

It does not suppress P4/P8 integrity errors merely to produce a reconciliation summary.

## Semantic-control invariant

Agent decides:

- whether reconciliation is warranted;
- what a reconciliation report means;
- whether repair is warranted and authorized;
- whether repair verification is sufficient;
- whether to advance, defer, close, or do ordinary work.

Deterministic machinery decides:

- whether the artifact is admitted evidence;
- its exact P4 identity/provenance;
- whether a P8-bound transition consumed the exact report;
- whether an explicit disposition is mechanically represented;
- whether Campaign history remains reconstructible.

Therefore:

```text
validator passed
!= conclusion is true

reconciliation_report admitted
!= reconciliation semantically accepted

repair_verification_report admitted
!= repair sufficient

finding closed
!= Campaign goal achieved

finding remaining
!= automatic defer/close

reconciliation evidence
!= repair authority

reconciliation evidence
!= Campaign decision
```

## Qualification expectations

A qualified P9 candidate must prove at least:

1. admitted `reconciliation_report` evidence is discovered by exact P4 provenance;
2. admitted `repair_verification_report` evidence is discovered independently;
3. unadmitted artifact-like files are ignored;
4. unconsumed admitted reports are `disposition_required`;
5. a P5 transition that explicitly consumes the report becomes `disposition_recorded` through P8 lineage;
6. direct/pre-P8 consumption remains `legacy_unbound` and does not overclaim exact binding;
7. report verdict-like content does not mutate Campaign state;
8. multiple reports remain independent and deterministic without inferred latest/supersession semantics;
9. tampered P4/P8 state fails closed;
10. `campaign reconciliation` is read-only;
11. JSON contains no recommendation, ranking, semantic-sufficiency, inferred authority, or automatic disposition;
12. a fresh process can reconstruct P9 state from durable Campaign files;
13. the installed wheel exposes the command without requiring a source checkout.
