# Campaign CLI — v0.3 P3

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

`init` does not inspect the target repository and does not infer an uncertainty, responsibility, capability, or authority.

### `campaign status`

Reconstructs and displays the current durable campaign snapshot.

```bash
sensemaking-skills campaign status --workspace /path/to/campaign
```

It reports what durable state says. It does not recommend what the campaign should do next.

### `campaign validate`

Runs deterministic recovery/reconstruction validation.

```bash
sensemaking-skills campaign validate --workspace /path/to/campaign
```

Success prints `CAMPAIGN_VALID`. Structural/integrity failure prints `CAMPAIGN_INVALID` or a stable campaign error code and exits non-zero.

### `campaign history`

Displays transition history in the canonical order reconstructed by `CampaignService` from the campaign trace.

```bash
sensemaking-skills campaign history --workspace /path/to/campaign
```

History order is not inferred from transition filenames.

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

The deterministic product layer may validate, persist, reconstruct, and expose decisions. It does not decide:

- what repository evidence means;
- which uncertainty is consequential;
- which responsibility is warranted;
- which capability is best;
- what action should happen next.

Those remain agent/human judgments.
