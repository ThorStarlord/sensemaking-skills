# Surface Simplification & Contract Consolidation v1

**Status:** repository/hermetic implementation contract  
**Scope:** mechanical companion IO only  
**Campaign schema:** remains v2

## Purpose

Recent Campaign portability/completion features introduced several bounded companion files that independently repeated the same representation mechanics: compact sorted JSON hashing, pretty atomic JSON replacement, and fsync'd JSONL append.

This package centralizes only those repeated mechanics in:

```text
src/sensemaking_skills/campaigns/companion_io.py
```

The shared primitives are:

```text
canonical_json_bytes
mapping_sha256
atomic_write_json
append_jsonl_fsync
```

## Migrated consumers

The bounded refactor covers the recent companion surfaces:

- `target_rebind.py`
- `multi_target_rebind.py`
- `multi_target_relations.py`
- `completion.py`

Their file names, field contracts, digest inputs, semantic limits, CLI behavior, and validation ownership remain with the individual feature modules.

## Explicit non-goals

This is not a universal persistence framework and does not merge companion schemas.

```text
shared IO != shared semantic model
shared hash primitive != shared authority
refactor != schema migration
```

Older Campaign and Semantic Architecture persistence code is deliberately not bulk-migrated merely for stylistic uniformity. In particular, Semantic Architecture keeps its own state/chain implementation because it is a distinct subsystem with existing contracts and tests.

## Compatibility rule

The consolidation must preserve:

- compact sorted UTF-8 JSON bytes used for SHA-256 inputs;
- existing record/core field selection in each owning module;
- pretty sorted JSON object files ending in one newline;
- one sorted JSON object per JSONL line;
- explicit fsync before returning from writes;
- existing negative/tamper behavior.

The existing target-rebind, multi-target relation, completion/archive, and broader Campaign tests are therefore behavioral regression guards in addition to direct `companion_io` tests.

## Evidence ceiling

This package establishes only that duplicate representation/IO code was consolidated behind a tested mechanical primitive while existing repository tests remain green.

It does not establish product-value improvement, semantic correctness, stronger durability than the underlying filesystem provides, native-harness usefulness, or a reason to migrate every persistence subsystem to the helper.
