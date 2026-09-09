# Campaign Narrative Verification Receipts

**Status:** product contract  
**Scope:** mechanical verification of current Campaign narrative claims against durable Campaign evidence  
**Control boundary:** claim/evidence binding is provenance, not semantic truth

## Purpose

A durable Campaign can already preserve state, evidence, transitions, lineage, and target-repository provenance. Narrative verification adds one narrower capability:

> Record that an exact claim was present in the current Campaign narrative and that the agent cited exact durable evidence bytes when it reviewed that claim.

The receipt does not interpret the evidence. The active coding agent still decides whether the evidence supports the claim and how strongly.

```text
Campaign narrative claim
        +
agent-selected durable evidence refs
        ↓
mechanical membership + evidence-contract checks
        ↓
exact Campaign-state digest
+ exact evidence-byte digests
        ↓
append-only narrative verification receipt
```

The permanent claim ceiling is:

```text
claim bound to evidence != evidence proves claim
verification receipt exists != semantic truth
mechanical verification != warranted transition
historical verification != current Campaign state
```

## Supported narrative scopes

Package 2 intentionally verifies only narrative that is already first-class in `CampaignState`:

- `current_state` — the claim must exactly equal `CampaignState.current_state`;
- `established_fact` — the claim must exactly occur in `CampaignState.established_facts`;
- `resolved_question` — the claim must exactly occur in `CampaignState.resolved_questions`.

No fuzzy matching, paraphrase detection, entailment, scoring, or inference is performed. An invented claim is rejected even if an agent believes it follows from the evidence.

## Claim contract

The service reuses the existing `ClaimEvidence` type:

```python
from sensemaking_skills.campaign_semantics import ClaimEvidence
from sensemaking_skills.campaigns import CampaignNarrativeVerificationService

claim = ClaimEvidence(
    claim="Repository diagnosis is complete",
    scope="established_fact",
    method="agent_cross_check",
    coverage=("repository_sensemaking_brief section 7",),
    claim_strength="supported",
    evidence=("artifacts/repository_sensemaking_brief/<sha>.md",),
)

result = CampaignNarrativeVerificationService(workspace).verify(
    receipt_id="NV-001",
    claims=(claim,),
)
```

`method`, `coverage`, and `claim_strength` are agent-authored descriptive metadata. The deterministic layer stores them but does not decide whether they are appropriate.

Each claim must cite at least one durable Campaign evidence ref. In particular:

```text
file under artifacts/
!= admitted Campaign evidence
```

An orphan artifact cannot support a narrative verification receipt.

## Append-only receipt

Receipts are stored beneath:

```text
narrative-verifications/
```

using a content-addressed filename:

```text
<receipt-id>--<receipt-sha256>.yaml
```

A receipt records:

```text
campaign_id
receipt_id
state_sha256
claims[]
evidence_sha256{ref -> digest}
schema_version
```

`state_sha256` is the canonical digest of the exact current `CampaignState` at verification time. `evidence_sha256` binds every cited evidence ref to the exact bytes present at that time.

Receipt IDs are append-only. Reusing an existing ID is rejected rather than overwriting history.

## Historical verification

A later legitimate Campaign transition does not invalidate an older receipt. The receipt remains evidence of what was reviewed at its own state boundary.

`CampaignNarrativeVerificationService.history()` reports whether each receipt's state digest equals the current Campaign-state digest:

```text
current_state_match = true   -> receipt binds the current state bytes
current_state_match = false  -> receipt is historical
```

Historical is not failure. Rewriting the old receipt to match the new state would destroy provenance.

## Fail-closed integrity

Narrative verification fails closed when:

- a claim is not an exact member of the declared current narrative scope;
- a claim cites no evidence;
- a cited ref is not durable Campaign evidence;
- an artifact exists but has not been admitted under the Campaign evidence contract;
- a receipt ID is unsafe or already exists;
- a receipt file is malformed, aliased, or tampered;
- receipt content no longer matches its content-addressed filename;
- cited evidence disappears;
- cited evidence bytes no longer match the recorded digest;
- a receipt belongs to a different Campaign.

Representative diagnostics include:

```text
INVALID_NARRATIVE_VERIFICATION_RECEIPT
DUPLICATE_NARRATIVE_VERIFICATION_RECEIPT
NARRATIVE_VERIFICATION_CAMPAIGN_ID_MISMATCH
NARRATIVE_VERIFICATION_DIGEST_MISMATCH
NARRATIVE_VERIFICATION_EVIDENCE_MISSING
NARRATIVE_VERIFICATION_EVIDENCE_DIGEST_MISMATCH
NARRATIVE_VERIFICATION_DIRECTORY_INVALID
```

## YAML claim input

For agents that prefer a machine-readable intermediate file, `load_narrative_claims()` accepts:

```yaml
claims:
  - claim: Repository diagnosis is complete
    scope: established_fact
    method: agent_cross_check
    coverage:
      - repository_sensemaking_brief section 7
    claim_strength: supported
    evidence:
      - artifacts/repository_sensemaking_brief/<sha>.md
```

Unknown fields and duplicate claim/scope bindings are rejected. The loader does not normalize claim meaning or infer missing metadata.

## Relationship to transitions and lineage

Narrative verification is deliberately not a lifecycle transition. Writing a receipt leaves `CampaignState`, `CampaignTrace`, and transition history unchanged.

The agent may later use its semantic review of the evidence when authoring an `advance`, `defer`, or `close` decision. That is a separate action and a separate claim.

```text
narrative receipt
!= transition
!= responsibility selection
!= authority grant
```

Existing P8 lineage answers which evidence a transition consumed. Narrative verification answers which exact durable evidence bytes an agent cited while reviewing an exact Campaign narrative claim. The two records are complementary and do not substitute for one another.

## Non-goals

This package does not:

- determine whether a claim is true;
- infer claims from artifacts;
- convert prose into `established_facts`;
- score or rank evidence;
- decide whether evidence is sufficient;
- select a responsibility or capability;
- authorize repository mutation;
- automatically advance a Campaign;
- create a semantic truth validator;
- replace real-harness empirical qualification.

The architecture remains:

```text
Agent owns semantic judgment.
Deterministic machinery owns representation, persistence, provenance, and integrity.
```
