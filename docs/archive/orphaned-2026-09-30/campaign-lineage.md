# Campaign artifact and evidence lineage

**Status:** P8 product contract  
**Scope:** mechanically reconstructible evidence identity, provenance, and explicit transition-consumption links

## Purpose

P8 makes a durable Sensemaking Campaign able to answer:

> Which exact evidence bytes did an authored decision cite, how did those bytes enter the Campaign, and which committed transition explicitly consumed them?

The product boundary is deliberately narrower than semantic justification:

```text
lineage
!= semantic truth
!= evidence sufficiency
!= recommendation
!= execution authority
```

P8 records and reconstructs **identity, provenance, and explicit consumption**. The active coding agent remains responsible for deciding what evidence means and whether it warrants a decision.

## Product surface

P8 adds the read-only inspection command:

```text
sensemaking-skills campaign lineage \
  --workspace /path/to/CMP-0001 \
  [--json]
```

The command reconstructs current evidence identity and committed transition-consumption edges from durable Campaign files. It does not create evidence, change transition meaning, or infer missing links.

## Existing contracts reused

P8 is intentionally layered over facts already shipped in P1-P7:

- P1 raw `evidence/` records and physical-containment rules;
- P2 ordered `TransitionRecord` + `CampaignTrace` reconstruction;
- P2 transition digests preserved in trace events;
- P4 content-addressed admitted artifacts;
- P4 append-only admission receipts;
- P4 evidence eligibility: arbitrary `artifacts/` files are not evidence;
- P5 `TransitionRecord.evidence` as the explicit evidence refs supplied with an authored decision;
- P7 fresh-process durable reconstruction.

P8 does **not** replace any of these authorities.

## Durable lineage layout

P8 creates its storage lazily inside an initialized Campaign workspace:

```text
CMP-XXXX/
└── lineage/
    ├── evidence/
    │   └── <sha256>
    └── consumptions/
        └── <transition-id>/
            └── <receipt-digest>.yaml
```

`lineage/evidence/<sha256>` contains exact consumed bytes when the original Campaign evidence path is not already immutable by source contract.

`lineage/consumptions/<transition-id>/<receipt-digest>.yaml` is an append-only precommit consumption intent. Its filename is the SHA-256 of its canonical payload.

## Consumption receipt

A consumption receipt contains only mechanically decidable facts:

```text
campaign_id
transition_id
evidence_bindings[]
schema_version
```

Each evidence binding records:

```text
source_ref
immutable_ref
sha256
kind
provenance
```

The receipt does not contain a conclusion, confidence score, evidence ranking, or assertion that the evidence is sufficient.

### Zero-evidence decisions

A P8-authored decision that explicitly cites no evidence still receives a receipt:

```yaml
evidence_bindings: []
```

This is important. It distinguishes:

```text
P8-authored decision that explicitly cited zero evidence
```

from:

```text
pre-P8 / direct-P2 transition whose evidence consumption was never bound
```

The former is `bound`; the latter is reported honestly as `legacy_unbound`.

## Evidence kinds

P8 distinguishes three evidence kinds.

### 1. Raw Campaign evidence

A ref under:

```text
evidence/**
```

retains the existing P1 evidence semantics. Because that path is not content-addressed, P8 snapshots the exact bytes at decision preparation time:

```text
evidence/brief.md
        ↓ SHA-256
lineage/evidence/<sha256>
```

The transition continues to cite the original durable ref. The lineage receipt additionally preserves the exact consumed byte identity and immutable snapshot.

If the original raw evidence file is later edited, lineage does not rewrite history. Inspection reports that the current source no longer matches the consumed bytes while the immutable snapshot remains available.

### 2. Admitted artifact

A P4 artifact ref such as:

```text
artifacts/<artifact-id>/<sha256>.<ext>
```

is already content-addressed and validated against its admission receipt by the P4 evidence contract.

P8 therefore reuses the P4 artifact itself as `immutable_ref` rather than copying it again. Provenance identifies the artifact ID and the admission receipt ref(s) that establish how it entered Campaign evidence.

### 3. Admission receipt

An admission receipt under:

```text
admissions/<artifact-id>/<receipt-payload-digest>.yaml
```

is itself Campaign evidence under P4. Its filename content-addresses the canonical semantic payload, but YAML formatting bytes may differ while preserving that payload.

When a decision explicitly cites an admission receipt, P8 snapshots its exact bytes into `lineage/evidence/<sha256>` and records P4 provenance such as artifact ID, artifact ref, artifact digest, validator identity, and validation timestamp.

## Precommit intent and lifecycle commit

P8 prepares lineage **before** the existing P2 lifecycle primitive commits the authored decision:

```text
agent-authored evidence refs
        ↓
P1/P4 evidence eligibility check
        ↓
exact byte identity
        ↓
content-addressed immutable ref
        ↓
append-only P8 consumption intent
        ↓
existing P2 lifecycle commit
        ↓
TransitionRecord.evidence + trace
```

This ordering preserves exact cited bytes without changing P2 transaction meaning.

The crucial distinction is:

```text
lineage receipt exists
!= transition committed
```

A receipt becomes a committed consumption binding only when all of the following are true:

```text
valid receipt
+ matching Campaign identity
+ committed transition with same transition_id
+ exact receipt evidence-ref sequence == TransitionRecord.evidence
+ valid transition digest from Campaign trace
= bound explicit consumption
```

P8 never infers a committed edge merely because a precommit file exists.

## Orphan intents

A failure after lineage preparation but before the P2 lifecycle commit can leave an append-only receipt whose transition never committed.

That receipt is reported as an **orphan precommit intent**. It is not a transition and does not create a consumption edge.

This is deliberate fail-safe behavior:

```text
possible orphan intent
> false historical consumption claim
```

Retrying the same transition ID is idempotent only when the exact lineage payload is unchanged. A different evidence binding for the same transition ID fails closed rather than silently replacing history.

## Legacy compatibility

P2 remains a lower-level lifecycle primitive. Historical transitions, or callers that bypass `CampaignDecisionService`, may have a valid `TransitionRecord.evidence` list but no P8 consumption receipt.

P8 reports those transitions as:

```text
legacy_unbound
```

It may show the evidence refs already present in `TransitionRecord.evidence`, but it does **not** invent a historical consumed digest or immutable snapshot.

There is no retroactive claim that P8 observed bytes it did not observe.

## Transition digest

Every lineage transition includes the existing transition digest from its canonical Campaign trace event.

P8 does not calculate a competing transition identity. The normal `CampaignService.resume()` reconstruction must already prove that the persisted `TransitionRecord` matches that trace digest.

Therefore lineage consumes the existing P2 identity rather than creating another transition ledger.

## Read model

JSON lineage output has the shape:

```json
{
  "ok": true,
  "code": "CAMPAIGN_LINEAGE",
  "campaign_id": "CMP-0001",
  "evidence_count": 2,
  "transition_count": 1,
  "consumption_edge_count": 2,
  "evidence": [],
  "transitions": [],
  "consumption_edges": [],
  "orphan_intent_refs": []
}
```

Evidence records expose current identity/provenance. Transition records expose existing trace digest, explicit evidence refs, receipt ref, and binding status. Consumption edges expose exact consumed SHA-256 and immutable ref when P8 actually bound them.

For mutable source refs, an edge may additionally report:

```text
source_matches_consumed_bytes: true | false
```

This is byte comparison only. `false` does not determine whether the new or old evidence is semantically better.

## Integrity behavior

P8 fails closed on mechanically ambiguous durable lineage, including:

- invalid or unsafe transition IDs;
- invalid workspace-relative lineage refs;
- symlink/reparse/physical-containment ambiguity;
- non-directory lineage control paths;
- unexpected entries in a committed consumption directory;
- multiple consumption receipts for one committed transition;
- receipt filename/payload digest mismatch;
- receipt Campaign/transition identity mismatch;
- receipt evidence refs differing from `TransitionRecord.evidence`;
- missing or modified immutable consumed bytes;
- admitted artifact digest disagreement with P4 admission provenance;
- conflicting precommit intent for the same transition ID.

P8 does not weaken P4 or P2 validation to make lineage inspection succeed.

## Read-only inspection

`campaign lineage` is read-only. All mutation required to preserve exact consumed evidence happens during the explicit authored decision path, before the existing P2 lifecycle commit.

Running lineage inspection must not:

- create snapshots;
- repair receipts;
- rewrite evidence;
- mutate transitions;
- refresh handoffs;
- infer missing consumption bindings.

## Relationship to handoff/resume

P7 handoff remains the fresh-context reconstruction surface. P8 does not change the `CampaignHandoff` semantic schema or P7 binding protocol in this milestone.

A fresh agent can:

```text
campaign resume
→ reconstruct Campaign state/history
→ campaign lineage
→ inspect evidence identity/provenance/consumption
→ make its own semantic judgment
```

Harness-specific automatic presentation remains a P10 concern.

## Failure and trust model

P8 uses SHA-256 content identities and the same filesystem trust assumptions as the rest of the current Campaign product. These digests are integrity bindings, not signatures.

P8 does not claim authenticity against an actor that can rewrite all Campaign records and recompute every digest.

## Explicit non-goals

P8 does **not**:

- interpret artifact findings;
- determine whether evidence logically supports a decision;
- determine evidence sufficiency;
- rank evidence;
- recommend or select capabilities;
- grant execution authority;
- infer consumption edges absent from durable records;
- rewrite historical transitions;
- grandfather arbitrary `artifacts/` files as evidence;
- make validator success equivalent to semantic truth;
- create a second semantic decision log;
- replace P4 admission receipts or P2 trace identity;
- alter P7 handoff semantics.

Therefore:

```text
explicit consumption
!= semantic warrant
```

## Qualification expectations

A qualified P8 candidate must prove at least:

1. raw evidence cited by an authored decision is snapshotted by exact SHA-256 before lifecycle commit;
2. later raw-source drift does not rewrite the consumed-byte identity;
3. admitted artifacts reuse the exact P4 content address and expose admission provenance;
4. cited admission receipts preserve exact consumed bytes and P4 provenance;
5. unadmitted/orphan files under `artifacts/` never become evidence lineage;
6. transition-to-evidence edges equal `TransitionRecord.evidence` exactly;
7. every P8-authored transition, including zero-evidence decisions, has an explicit bound receipt;
8. historical/direct-P2 transitions without receipts remain honestly `legacy_unbound`;
9. orphan precommit intents never become false committed edges;
10. conflicting or ambiguous lineage state fails closed;
11. tampered immutable consumed evidence fails closed;
12. lineage inspection is deterministic and read-only;
13. output contains no recommendation, ranking, semantic-sufficiency, or authority inference;
14. a fresh process can reconstruct lineage from durable Campaign files alone;
15. the installed wheel exposes lineage without requiring a source checkout.
