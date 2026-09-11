# Campaign Completion & Archival v1

**Status:** repository/hermetic implementation contract  
**Campaign schema:** remains v2  
**Authority:** completion observes an already-terminal Campaign; archive is a nondestructive marker

## Purpose

Campaigns already have an explicit semantic terminal decision through `campaign close`. Completion & Archival v1 adds a deterministic final mechanical receipt and an optional archive marker without allowing the tool to infer that work succeeded or to close a Campaign by itself.

```text
agent/human authors campaign close
        ↓
terminal Campaign state
        ↓
campaign closeout
        ↓
deterministic completion receipt
        ↓
campaign archive (optional)
```

```text
closeout != close
terminal != successful
archive != successful
archive != delete/move
completion receipt != proof of engineering correctness
```

## Commands

```bash
sensemaking-skills campaign closeout \
  --workspace /path/to/CMP-0001 \
  --json

sensemaking-skills campaign completion-receipt \
  --workspace /path/to/CMP-0001 \
  --json

sensemaking-skills campaign archive \
  --workspace /path/to/CMP-0001 \
  --json

sensemaking-skills campaign inventory \
  --root /path/to/campaigns \
  --include-archived \
  --json
```

## Completion receipt

`completion-receipt.json` is generated only after Campaign state is already terminal. It binds mechanically available terminal state including:

- Campaign/schema identity;
- durable terminal classification and current state;
- final transition identity/count;
- Campaign evidence refs and deferred responsibility identities;
- active uncertainty identity if one remains recorded;
- primary target snapshot digest when present;
- Campaign Preflight check statuses;
- provenance-graph mechanical validity;
- a deterministic manifest of durable workspace file paths, sizes, and SHA-256 values;
- an aggregate workspace manifest digest;
- its own receipt SHA-256.

The completion and archive files plus transaction scratch space are excluded from the workspace manifest so the receipt remains self-verifiable.

`campaign completion-receipt` recomputes the current terminal projection. If durable workspace bytes change after closeout, the existing receipt becomes stale and validation fails until the caller explicitly runs `campaign closeout` again.

## Archive marker

`archive-receipt.json` is created only when the current completion receipt is valid. It binds the Campaign ID, terminal state, and completion receipt SHA-256.

Archive is intentionally nondestructive:

```text
workspace_moved = false
workspace_deleted = false
semantic_success_established = false
```

This matters for terminal states such as `external_blocker`, `evidence_insufficient`, or `owner_decision_required`: they may be archived as durable records without being mislabeled successful.

## Inventory behavior

Campaign inventory hides valid archived workspaces by default. `--include-archived` includes them with `archived` and `archive_integrity` fields. Inventory still does not prioritize Campaigns.

An invalid archive marker is never silently used to hide a workspace.

## Failure behavior

The feature fails closed when:

- closeout is requested before an explicit terminal decision;
- durable workspace content includes a symlink that cannot be safely included in the completion manifest;
- a completion receipt no longer matches current terminal workspace bytes;
- archive is requested without a valid current completion receipt;
- an existing archive marker conflicts with the current receipt.

## Evidence ceiling

```text
completion receipt valid
!= terminal decision semantically correct
!= goal achieved
!= repository change correct

archive valid
!= Campaign successful
!= work publishable
!= release authorized
```

No native-harness run, external publication, deployment, semantic planner, or experiment state is part of this feature.
