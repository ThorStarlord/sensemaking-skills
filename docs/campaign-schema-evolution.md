# Campaign Schema Evolution

Durable Campaigns outlive individual agent contexts and therefore must outlive individual representation versions. Schema evolution is intentionally mechanical: it can normalize representation, but it cannot reinterpret evidence, select work, or change authority.

## Current contract

Campaign semantic artifacts now use schema version `2`. The runtime can read historical v1 artifacts and deterministically migrate them in memory to v2. Unknown future versions fail closed.

The v1 -> v2 representation migration is deliberately narrow:

- `campaign-state.yaml`: historical top-level `owner_routing` is moved under `extensions.owner_routing`.
- `campaign-handoff.yaml`: historical `allowed_actions` is canonicalized to `allowed_next_actions`, and an embedded v1 state is migrated with the same state migration.
- transition, policy, and trace artifacts receive only the explicit schema-version upgrade; their decision-relevant content is unchanged.

New dumps always emit v2.

## Why old files are not rewritten

Transition records are append-only history. Rewriting them merely to modernize serialization would destroy the exact historical bytes that Campaign provenance is meant to preserve. The same non-destructive rule is applied uniformly to legacy Campaign artifacts.

Instead, a schema upgrade records a content-addressed receipt that binds:

- the exact source artifact path and SHA-256,
- the source and target schema versions,
- the deterministic migration steps,
- the full canonical migrated payload plus its SHA-256.

The migrated payload is retained in the receipt so the current representation is
durable provenance rather than only a transient read-time transformation.

A receipt becomes stale automatically if the source bytes change. Old receipts remain append-only provenance and do not qualify new bytes.

## Agent-visible workflow

Inspect a workspace:

```bash
python -m sensemaking_skills.campaign_schema_cli status \
  --workspace /path/to/CMP-0001
```

Qualify every currently migratable legacy artifact:

```bash
python -m sensemaking_skills.campaign_schema_cli upgrade \
  --workspace /path/to/CMP-0001
```

Both commands support `--json`.

Status classifies each Campaign artifact as:

- `current` — source bytes already use the current schema;
- `pending` — deterministic migration is available but no exact receipt covers these source bytes;
- `qualified` — an append-only receipt binds these exact legacy bytes to their exact current representation.

`upgrade` is idempotent. It writes receipts only for `pending` artifacts and never rewrites the source Campaign artifacts.

## Fail-closed boundaries

Qualification fails rather than guessing when:

- a schema version is unsupported;
- a v1 alias conflicts with its canonical representation;
- a Campaign artifact or receipt escapes the workspace or is a symlink/non-file;
- a migrated representation fails the normal production loader;
- a receipt is malformed, tampered with, or names a non-current migration engine/target;
- workspace bytes change while an upgrade is being qualified.

This establishes representation compatibility, not semantic correctness. A successful migration receipt means only that exact historical bytes have a deterministic, contract-valid current representation.
