# Campaign handoff and fresh-context resume

**Status:** P7 product contract  
**Scope:** durable reconstruction UX over the existing `CampaignHandoff` and `CampaignService` lifecycle primitives

## Purpose

P7 makes fresh-agent continuation a first-class Sensemaking Campaign experience.

The product boundary is:

```text
current durable campaign state
        ↓
deterministic handoff generation
        ↓
exact reconstruction pointers + integrity binding
        ↓
fresh agent / fresh process
        ↓
strict resume validation
        ↓
agent reconstructs context and decides what to do next
```

A handoff is **not** a semantic recommendation and is not a substitute for the durable campaign records.

```text
handoff
!= source of truth
!= next-action recommendation
!= execution authority
```

The authoritative facts remain the reconstructible Campaign workspace: current state, transition history, trace, evidence/admission records, and optional policy.

## Product surfaces

P7 adds:

```text
sensemaking-skills campaign handoff \
  --workspace /path/to/CMP-0001 \
  [--allowed-next-action <agent-authored-context>]... \
  [--stop-condition <terminal-state>]... \
  [--json]

sensemaking-skills campaign resume \
  --workspace /path/to/CMP-0001 \
  [--json]
```

`campaign handoff` creates or replaces the current handoff for the exact current Campaign state.

`campaign resume` is deliberately stricter than ordinary `campaign status`: it requires a current P7-bound handoff and verifies that the handoff still binds to the exact reconstructible durable context.

## Reuse of P2 contracts

P7 does not create another handoff state machine.

It reuses:

- `CampaignHandoff`;
- `CampaignService.generate_handoff()`;
- `CampaignService.resume()`;
- `CampaignStore.write_handoff()` / `load_handoff()`;
- the existing lifecycle rule that a committed transition invalidates the prior handoff.

The semantic `CampaignHandoff` schema remains unchanged:

```text
campaign_id
current_state
canonical_artifacts
allowed_next_actions
stop_conditions
schema_version
```

This matters because `campaign-handoff.yaml` remains readable by the existing strict campaign-semantic loader. P7 adds reconstruction integrity without creating a competing representation.

## Reconstruction integrity binding

After the canonical P2 handoff write succeeds, P7 computes a SHA-256 reconstruction checksum over the canonical representation of:

```text
protocol identity
campaign state
ordered transition records
campaign trace
durable evidence refs
optional campaign policy
CampaignHandoff semantic record
```

The checksum is written as the first YAML comment in `campaign-handoff.yaml`:

```text
# p7_reconstruction_sha256: <64 lowercase hex characters>
```

Because this is a YAML comment, it does not add an unknown semantic field to `CampaignHandoff` and does not weaken strict loading.

`campaign resume` requires the marker and recomputes the checksum from the fresh reconstruction. A mismatch fails closed.

This checksum is an **integrity binding, not a cryptographic signature**. It does not establish filesystem trust, identity, authorization, or authenticity against an attacker who can rewrite every Campaign file and recompute checksums. It has the same purpose as the Campaign's other digest bindings: detect stale, accidental, partial, or unbound durable representations under the product's filesystem trust model.

## Canonical reconstruction artifacts

P7 derives `canonical_artifacts` mechanically from durable Campaign facts rather than asking the model to remember which files matter.

The set contains, when present:

```text
campaign-state.yaml
trace.yaml
campaign-policy.yaml
transitions/<transition-id>.yaml
<every current durable evidence ref>
```

Evidence refs retain the P4 trust model. In particular, a file merely existing under `artifacts/` does not become a handoff reconstruction input unless it is admitted under the Campaign evidence contract.

The list is deduplicated and deterministically ordered. This ordering is mechanical convenience, not semantic priority.

## Agent-authored guidance

`allowed_next_actions` and `stop_conditions` are context fields inside the existing `CampaignHandoff` contract.

P7 deliberately does **not** infer them.

If the agent supplies no guidance:

```text
allowed_next_actions: []
stop_conditions: []
```

Even when a Campaign policy contains stop conditions, P7 does not silently copy those values into the handoff's agent-authored guidance. The policy remains separately visible in the reconstruction envelope.

An `allowed_next_action`:

- must be non-empty;
- may be repeated only with distinct values;
- is preserved as supplied after surrounding-whitespace normalization;
- does not select a capability;
- does not authorize execution;
- does not become a durable Campaign transition merely by appearing in a handoff.

`stop_condition` values must be canonical `TerminalState` values and may not contain duplicates.

## Fresh-context resume envelope

JSON resume returns a mechanically reconstructed envelope with:

```json
{
  "ok": true,
  "code": "CAMPAIGN_RESUMED",
  "campaign_id": "CMP-0001",
  "handoff_ref": "campaign-handoff.yaml",
  "reconstruction_sha256": "...",
  "state": {},
  "transitions": [],
  "trace": {},
  "evidence_refs": [],
  "policy": null,
  "handoff": {}
}
```

This is intentionally more complete than a conversational summary. A fresh agent or later harness adapter can reconstruct the durable context without the previous chat transcript.

The envelope contains data; it does not contain a `recommended`, `selected`, ranked, or scored next action.

## Staleness and lifecycle transitions

P2 already invalidates `campaign-handoff.yaml` whenever a lifecycle transition commits.

Therefore:

```text
handoff created at state S
→ lifecycle transition S → S2 commits
→ old handoff removed
→ fresh-context resume requires a new handoff for S2
```

P7 does not silently refresh a missing or stale handoff during `campaign resume`. Doing so would make resume mutate durable context and could hide an important lifecycle boundary.

## Legacy/unbound handoffs

The low-level P2 `CampaignService.generate_handoff()` primitive remains capable of producing a valid semantic `CampaignHandoff` without the P7 comment binding.

Such a handoff remains valid as a P2 semantic artifact, but it is **not sufficient for the P7 fresh-context UX**.

`campaign resume` fails closed with:

```text
HANDOFF_RECONSTRUCTION_BINDING_MISSING
```

until `campaign handoff` creates a current bound handoff.

This avoids silently treating historical or low-level handoffs as if they had passed the stronger P7 reconstruction contract.

## Tamper / drift behavior

Examples that fail closed include:

- handoff state no longer matching `campaign-state.yaml`;
- missing or malformed P7 reconstruction marker;
- valid-shape edits to `allowed_next_actions` after handoff generation;
- valid-shape edits to stop conditions or canonical artifact refs after binding;
- trace/transition/evidence/policy drift that changes the reconstruction checksum;
- any existing Campaign reconstruction defect detected by P2.

The expected integrity diagnostic for a valid-shape checksum mismatch is:

```text
HANDOFF_RECONSTRUCTION_BINDING_MISMATCH
```

A lifecycle transition normally removes the old handoff entirely rather than producing a mismatch.

## Terminal campaigns

Terminal Campaigns may be handed off and resumed.

The reconstruction must preserve the terminal classification honestly:

```text
status: terminal
terminal_state: <canonical terminal state>
active_responsibility: null
```

P7 does not invent a continuation action merely because a fresh agent opened the Campaign.

## Failure classes

P7 reuses the existing Campaign CLI failure taxonomy.

Examples:

```text
no current handoff after latest transition
→ CAMPAIGN_TRANSACTION_ERROR
→ exit 4

malformed/tampered reconstruction binding
→ CAMPAIGN_INTEGRITY_ERROR
→ exit 3
```

Strict campaign-semantic `ContractError` handling remains part of the existing integrity class.

## Explicit non-goals

P7 does **not**:

- summarize or recover unstored conversation history;
- infer a next responsibility;
- infer a capability selection;
- rank or recommend capabilities;
- interpret evidence semantics;
- grant execution authority;
- turn allowed-next-action text into an executable command;
- automatically refresh a stale/missing handoff during resume;
- make the handoff a second source of Campaign truth;
- provide cryptographic authenticity against a fully compromised filesystem;
- implement harness-specific Skill discovery or handoff transport (P10).

Therefore:

```text
fresh-context reconstruction
!= semantic continuation decision
```

## Qualification expectations

A qualified P7 candidate must prove at least:

1. `campaign handoff` binds the exact current reconstructed Campaign without changing semantic state;
2. `campaign resume` reconstructs the same state, transitions, trace, evidence refs, policy, and handoff in a fresh service/process;
3. no prior conversation memory is required;
4. no next action or stop condition is inferred when the agent supplies none;
5. valid-shape handoff guidance edits fail the reconstruction binding;
6. unbound legacy/P2 handoffs are not silently promoted to P7-bound handoffs;
7. a subsequent lifecycle transition removes the old handoff and resume fails until a new one is created;
8. terminal Campaigns resume as terminal without fabricated executable work;
9. malformed/blank/duplicate agent guidance fails closed;
10. JSON exposes reconstruction facts without recommendation/ranking/selection fields;
11. the commands work from an installed wheel in a fresh environment outside a source checkout.
