# Campaign Observability and Portability

**Status:** Repository-qualified additive product capability  
**Campaign schema:** remains v2  
**Semantic authority:** unchanged; commands project, connect, audit, or transport durable state and provenance only

## Purpose

Campaign durability becomes more useful when a fresh agent/operator can inspect, reconstruct, compare, visualize, audit, and transport state without manually reading every workspace file.

This feature family adds deterministic projections over existing Campaign v2 state plus an optional companion semantic-reference log. It does not add a semantic planner or infer a next action.

## `campaign inspect`

Produces the mechanically reconstructible Campaign snapshot:

- canonical Campaign state;
- trace-ordered transitions;
- evidence refs;
- policy when present;
- handoff when present;
- summary of the optional `semantic-state.jsonl` companion.

The result explicitly reports that no semantic recommendation/truth is established.

## `campaign explain --ref`

Looks up an **exact durable identifier/reference** and reports where it occurs in reconstructed Campaign or companion state, including supported cases such as:

- active responsibility/uncertainty IDs;
- deferred responsibility IDs;
- transition IDs;
- transition evidence refs;
- matching trace-event values;
- semantic companion entry IDs;
- companion artifact/profile/evidence/claim/uncertainty refs.

After B7 Semantic Reference Resolution & Integrity Audit v0, matching semantic-companion references also render their mechanically established reference-audit result when an authoritative resolver exists. This keeps two questions separate:

```text
reference occurrence != reference resolution
reference resolution != semantic support
```

A Campaign-internal ref may resolve, be dangling, or remain not addressable under current contracts. The command does not infer evidence relevance, currentness, semantic support, or whether a decision was correct.

## `campaign diff`

Compares two exact transition records field-by-field. It does not claim that changed metadata represents improvement or regression.

## Campaign semantic companion

Commands:

```text
campaign semantic-state-append
campaign semantic-state
```

The companion is stored as `semantic-state.jsonl` in the Campaign workspace but is **not a field in `CampaignState`**. Campaign schema therefore remains v2.

Each entry can reference a source Skill, artifact, evidence, claims, uncertainties, parent semantic entries, and an optional `semantic_reasoning_profile`. Entries are append-only and SHA-256 chained.

For repository-bound Campaigns, new entries derive their target identity from the current TargetSnapshot digest. A caller-supplied target ref that disagrees is rejected. Targetless Campaigns require an explicit target ref.

```text
semantic companion chain valid
!=
referenced claim true
```

Because the companion is a workspace file, portable Campaign bundles carry it automatically without a Campaign schema migration.

## B7 semantic-reference audit

B7 adds a standalone mechanical reference-audit primitive in `sensemaking_skills.semantic_architecture.reference_audit`. Campaign observability is a rendering adapter over that primitive; it is not the owner of reference semantics.

The audit separates three dimensions:

```text
resolution
  resolved | dangling | ambiguous | not_addressable

reference class
  campaign_internal | legacy_opaque | unknown

integrity effect
  pass | fail | informational
```

`AMBIGUOUS` is reserved by the result vocabulary but is not emitted by the current v0 resolvers because existing authorities do not mechanically produce multiple valid matches.

Current authoritative resolution is deliberately bounded:

- `parent_entry_ids` reuse `SemanticStateStore` parent integrity;
- Campaign `evidence_refs` resolve through existing Campaign evidence/admission authority;
- exact admitted artifact refs resolve through that same authority rather than a new registry;
- an exact current `active_uncertainty.id` may resolve from Campaign state;
- opaque claim/profile refs remain `not_addressable` when no canonical resolver exists;
- target identity may be reported without inferring currentness.

Important distinctions:

```text
not_addressable != invalid
resolved != current
reference resolved != claim warranted
reference audit pass != semantic truth
```

`campaign semantic-state` renders chain diagnostics plus aggregate/detail reference-audit results. A corrupt companion chain prevents trustworthy outbound audit and surfaces the existing structural diagnostics rather than weakening `SemanticStateStore.validate()`.

B7 deliberately does **not** change Resume Capsule behavior, create Campaign schema v3, introduce a universal reference registry, create universal Claim/Evidence objects, or infer currentness, decision relevance, authority precedence, routing, or semantic truth.

The canonical design authority is `semantic-architecture/b7-semantic-reference-audit-design-preflight.md`.

## Resume Capsule — `campaign resume-context`

Produces a compact deterministic fresh-context projection containing:

```text
mission
Campaign status/current-state label
target snapshot when present
active responsibility
active uncertainty
authority / terminal state
established facts / resolved questions
deferred responsibilities
external boundaries
evidence refs
recent transitions
handoff when present
semantic companion summary when present
```

It deliberately does **not** emit a recommended next action.

Its explicit limit states that the capsule reconstructs durable declared state and optional companion references; the active agent still decides what action is warranted.

B7 does not add reference-resolution details to Resume Capsule v0.

## Replay — `campaign replay`

`campaign replay --at-transition <id>` reconstructs the trace prefix through an exact transition and reports the transition prefix, state label at that cursor, and cumulative transition evidence refs.

Campaign schema v2 does not store a complete `CampaignState` snapshot after every historical transition. Replay therefore explicitly reports:

```text
historic_full_state_reconstructed: false
```

It must not fabricate old state fields from present state.

## Provenance graph — `campaign graph`

Outputs JSON or Mermaid for mechanically established relations such as:

```text
Campaign contains_transition Transition
Transition followed_by Transition
Transition references_evidence EvidenceRef
Campaign has_semantic_companion_entry SemanticStateEntry
SemanticStateEntry semantic_parent_of SemanticStateEntry
SemanticStateEntry references_artifact ArtifactRef
```

The graph is a provenance graph, not a semantic causal graph. A recorded reference edge does not establish that evidence semantically supports a conclusion.

## Portable Campaign Bundles

Commands:

```text
campaign bundle-export
campaign bundle-verify
campaign bundle-import
```

A bundle is a deterministic ZIP containing exact Campaign workspace bytes plus `bundle-manifest.json` with SHA-256 and byte size for every declared member.

### Export properties

- deterministic member ordering and timestamps;
- symlink refusal;
- reserved manifest-name protection;
- export destination must be outside the source workspace;
- exact captured workspace bytes preserved;
- no semantic-success claim.

Rejecting an in-workspace destination prevents the export operation from creating a new workspace file that is absent from the manifest it just generated.

### Verification properties

The verifier fails closed on:

- missing/invalid manifest;
- duplicate archive names;
- absolute/path-traversal/backslash member paths;
- ZIP symlink members;
- missing declared files;
- undeclared archive files;
- SHA-256 mismatch;
- byte-size mismatch;
- unsupported bundle format/version.

A valid bundle establishes only archive integrity relative to its manifest.

```text
bundle valid != Campaign semantically correct
bundle valid != original target still available
bundle valid != imported Campaign should act on a new repository
```

### Import properties

Import verifies first, requires a new destination, writes only declared safe members, and removes a partially created destination if extraction fails.

After import, normal `campaign validate` remains the authority for Campaign reconstruction integrity.

## Fresh-context and machine portability

Together:

```text
Campaign workspace
    -> optional semantic companion
    -> optional B7 reference audit during inspection
    -> bundle export
    -> another machine/session
    -> bundle verification/import
    -> campaign validate
    -> resume-context
    -> fresh active agent semantic judgment
```

This separates **transport/reconstruction** from **meaning/decision**.

## Non-goals

These features do not:

- synchronize workspaces over a network;
- automatically locate a target repository after import;
- rank evidence;
- select a responsibility or Skill;
- reproduce hidden chain of thought;
- reconstruct historical full-state snapshots not stored by Campaign v2;
- assert semantic truth from archive or reference integrity;
- turn provenance or resolution edges into causal/architectural claims;
- promote the Phase 10 companion profile into Campaign admission;
- infer currentness from reference resolution;
- create a universal semantic-reference namespace or registry.
