# Campaign CLI — v0.3 P3+

The campaign CLI exposes durable campaign state without taking semantic control away from the active coding agent.

## Commands

```text
sensemaking-skills campaign init
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign history
```

### `campaign init`

Creates a new campaign workspace from explicitly supplied values.

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaign \
  --campaign-id CMP-0001 \
  --mission "Determine the next warranted development step"
```

An optional `--target-repo` may be supplied. The workspace is rejected if it would live inside that target repository.

When `--target-repo` is present, `init` **mechanically inspects** that Git worktree and persists a first-class target snapshot containing sanitized repository identity, HEAD/tree identity, and a deterministic tracked/untracked non-ignored worktree digest. This is provenance only: `init` still does not infer an uncertainty, responsibility, capability, authority, or semantic conclusion.

See [`campaign-target-snapshot.md`](campaign-target-snapshot.md).

### `campaign status`

Reconstructs and displays the current durable campaign snapshot.

```bash
sensemaking-skills campaign status --workspace /path/to/campaign
```

For a target-bound Campaign, reconstruction also verifies that the live target repository still matches the last durably recorded target snapshot. Unrecorded repository drift therefore fails closed instead of silently allowing a stale Campaign context to masquerade as current state.

It reports what durable state says. It does not recommend what the campaign should do next, and target drift does not automatically create a transition.

### `campaign validate`

Runs deterministic recovery/reconstruction validation.

```bash
sensemaking-skills campaign validate --workspace /path/to/campaign
```

Success prints `CAMPAIGN_VALID`. Structural/integrity failure prints `CAMPAIGN_INVALID` or a stable campaign error code and exits non-zero. Target-bound validation includes target transition-chain integrity and live target snapshot comparison.

### `campaign history`

Displays transition history in the canonical order reconstructed by `CampaignService` from the campaign trace.

```bash
sensemaking-skills campaign history --workspace /path/to/campaign
```

History order is not inferred from transition filenames. Target-bound transition records carry source/destination target snapshot SHA-256 values as mechanical provenance; those fields do not classify the repository change as correct or successful.

## JSON output

All four P3 commands accept `--json`.

The JSON surface is intended for coding agents and other deterministic consumers. Stable top-level `code` values include:

- `CAMPAIGN_INITIALIZED`
- `CAMPAIGN_STATUS`
- `CAMPAIGN_VALID`
- `CAMPAIGN_INVALID`
- `CAMPAIGN_HISTORY`
- `CAMPAIGN_ALREADY_EXISTS`
- `CAMPAIGN_NOT_INITIALIZED`
- `CAMPAIGN_IDENTITY_ERROR`
- `CAMPAIGN_TRANSACTION_ERROR`
- `CAMPAIGN_INTEGRITY_ERROR`
- `CAMPAIGN_WORKSPACE_ERROR`

Target-specific integrity diagnostics include `TARGET_REPOSITORY_UNAVAILABLE`, `TARGET_REPOSITORY_IDENTITY_MISMATCH`, `TARGET_SNAPSHOT_DRIFT`, and target transition-chain diagnostics documented in [`campaign-target-snapshot.md`](campaign-target-snapshot.md).

## Exit semantics

The P3 campaign commands define the following campaign-specific exit contract:

| Exit | Meaning |
|---:|---|
| `0` | command completed successfully / campaign is valid |
| `2` | Click command-line usage error |
| `3` | persisted campaign is invalid or its semantic contract cannot be reconstructed |
| `4` | workspace/lifecycle precondition failure such as missing, existing, isolated-path, identity, or transaction state |

P3 does not define a new campaign-specific interrupt exit code; interruption behavior remains part of the existing top-level Click entrypoint rather than this campaign protocol.

Unexpected internal failures continue to use the CLI's generic non-zero failure path.

## Architectural boundary

```text
CLI
 ↓
CampaignService
 ↓
CampaignStore
 ↓
campaign_semantics
```

Lifecycle-changing CLI surfaces must go through `CampaignService`; P3 does not bypass it by writing campaign state directly.

The deterministic product layer may validate, persist, reconstruct, expose decisions, and capture target provenance. It does not decide:

- what repository evidence means;
- whether a repository change is correct;
- which uncertainty is consequential;
- which responsibility is warranted;
- which capability is best;
- what action should happen next.

Those remain agent/human judgments.
