# Campaign CLI — v0.3 P3+

The campaign CLI exposes durable campaign state without taking semantic control away from the active coding agent.

## Normal commands

Root help/completion intentionally exposes the small durable kernel:

```text
sensemaking-skills campaign init
sensemaking-skills campaign ingest
sensemaking-skills campaign status
sensemaking-skills campaign validate
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
sensemaking-skills campaign inspect
sensemaking-skills campaign resume-profile
sensemaking-skills campaign working-context
sensemaking-skills campaign advanced
```

Secondary history, graph, portability, lineage, strategy, schema-evolution, and
compatibility surfaces are discoverable under `campaign advanced`. Their
historical root paths remain callable during the compatibility window, but they
are not part of the normal mental model.

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

For a target-bound Campaign, status performs read-only inspection of the last materialized durable state and reports live target/recovery diagnostics. If target drift or a blocking lifecycle transaction is present, status still orients the caller but reports `continuation_safe: false`.

This is deliberately weaker than continuation authority: strict resume, validation, and mutation remain fail-closed until the integrity condition is resolved. Status never recommends the next action and drift never creates a transition.

### `campaign validate`

Runs deterministic recovery/reconstruction validation.

```bash
sensemaking-skills campaign validate --workspace /path/to/campaign
```

Success prints `CAMPAIGN_VALID`. Structural/integrity failure prints `CAMPAIGN_INVALID` or a stable campaign error code and exits non-zero. Target-bound validation includes target transition-chain integrity and live target snapshot comparison.

### `campaign advanced history`

Displays transition history in the canonical order reconstructed by `CampaignService` from the campaign trace. The historical `campaign history` alias remains callable during the compatibility window.

```bash
sensemaking-skills campaign advanced history --workspace /path/to/campaign
```

History order is not inferred from transition filenames. Target-bound transition records carry source/destination target snapshot SHA-256 values as mechanical provenance; those fields do not classify the repository change as correct or successful.

### Read-only orientation under drift or recovery failure

`campaign inspect` reads the last materialized Campaign snapshot without
running lifecycle recovery. It surfaces reconstruction/target diagnostics and
pending/invalid transaction-journal observations even when strict
`resume`/`validate` cannot continue.

```text
cannot safely continue
!= cannot safely inspect

inspect available
!= continuation authorized
```

### Explicit decisions with derived bookkeeping

`campaign advance|defer|close` keep semantic judgment agent-authored while
deriving routine bookkeeping when the caller does not care about those labels.
Transition IDs and target-state labels are optional; `advance` also generates a
responsibility ID when omitted. Explicit values remain supported for stable
external references.


## JSON output

The normal inspection/status commands and secondary advanced projections preserve their existing `--json` contracts where supported.

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
