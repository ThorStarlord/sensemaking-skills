# Campaign Observability and Portability

**Status:** Executable additive product capability  
**Campaign schema:** remains v2  
**Semantic authority:** unchanged; commands project or transport durable state and provenance only

## Purpose

Campaign durability becomes more useful when a fresh agent/operator can inspect, reconstruct, compare, visualize, and transport the state without manually reading every workspace file.

This feature family adds deterministic projections over existing Campaign v2 state. It does not add a new semantic planner or infer a next action.

## `campaign inspect`

Produces the mechanically reconstructible Campaign snapshot:

- canonical Campaign state;
- trace-ordered transitions;
- evidence refs;
- policy when present;
- handoff when present.

The JSON result explicitly reports:

```text
semantic_recommendation_included: false
semantic_truth_established: false
```

## `campaign explain --ref`

Looks up an **exact durable identifier/reference** and reports where it occurs in reconstructed state/history, including supported cases such as:

- active responsibility ID;
- active uncertainty ID;
- deferred responsibility ID;
- transition ID;
- evidence ref consumed by transitions;
- matching trace event values.

This is provenance explanation, not semantic explanation. It can answer “where was this ref recorded/used?” but not “was this decision good?”

## `campaign diff`

Compares two exact transition records field-by-field.

It does not claim that changed metadata represents improvement or regression. The active agent interprets the significance of the diff.

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
```

It deliberately does **not** emit “recommended next step.”

The capsule's explicit limit is:

> This capsule reconstructs durable declared state; it does not decide the next warranted action.

This command is designed to reduce manual fresh-context reconstruction while preserving the Campaign principle that the active agent owns semantic judgment.

## Replay — `campaign replay`

`campaign replay --at-transition <id>` reconstructs the trace prefix through an exact transition and reports:

- transition prefix;
- state label at that cursor;
- cumulative transition evidence refs.

Campaign schema v2 does not store a complete `CampaignState` snapshot after every historical transition. Replay therefore explicitly reports:

```text
historic_full_state_reconstructed: false
```

It must not fabricate old state fields from the present state.

## Provenance graph — `campaign graph`

Outputs either JSON or Mermaid for mechanically established Campaign relations:

```text
Campaign contains_transition Transition
Transition followed_by Transition
Transition references_evidence EvidenceRef
```

The graph is intentionally a provenance graph, not a semantic causal graph.

It does not infer that evidence supports a decision, only that a transition record references that evidence.

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
- exact workspace bytes preserved;
- no semantic-success claim.

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

Import first verifies the bundle, requires a new destination, writes only declared safe members, and removes a partially created destination if extraction fails.

After import, normal `campaign validate` remains the authority for Campaign reconstruction integrity.

## Fresh-context and machine portability

Together:

```text
Campaign workspace
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
- turn provenance edges into causal/architectural claims.
