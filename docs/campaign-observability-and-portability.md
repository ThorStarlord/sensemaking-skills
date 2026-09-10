# Campaign Observability and Portability

**Status:** Executable additive product capability candidate  
**Campaign schema:** remains v2  
**Semantic authority:** unchanged; commands project, connect, or transport durable state and provenance only

## Purpose

Campaign durability becomes more useful when a fresh agent/operator can inspect, reconstruct, compare, visualize, and transport state without manually reading every workspace file.

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

This is provenance explanation, not semantic explanation. It can answer “where was this ref recorded or consumed?” but not “was this claim or decision correct?”

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
- assert semantic truth from archive integrity;
- turn provenance edges into causal/architectural claims;
- promote the Phase 10 companion profile into Campaign admission.
