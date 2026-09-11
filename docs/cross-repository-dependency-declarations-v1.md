# Cross-Repository Dependency Declarations v1

**Status:** repository/hermetic implementation contract  
**Campaign schema:** remains v2  
**Authority:** relations are explicitly authored by the caller; Sensemaking validates representation/integrity only

## Purpose

Multi-Repository Campaigns v1 establishes which repositories are explicitly in scope. Dependency Declarations v1 adds a bounded append-only companion for recording why two already-declared target aliases are related without asking Sensemaking to infer architecture, work order, or repository selection.

Supported relation classes:

```text
depends_on
provides_interface_to
consumes_interface_from
must_change_with
release_after
```

These names record caller-authored intent. A valid relation is not proof that the relationship is architecturally correct.

## Commands

```bash
sensemaking-skills campaign multi-target relate \
  --workspace /path/to/CMP-0001 \
  --relation-id REL-17 \
  --source-alias frontend \
  --target-alias backend \
  --relation-type depends_on

sensemaking-skills campaign multi-target dependency-check \
  --workspace /path/to/CMP-0001 \
  --json

sensemaking-skills campaign multi-target graph \
  --workspace /path/to/CMP-0001 \
  --format mermaid
```

Relations may reference existing Campaign evidence with repeated `--evidence-ref` options.

## Representation

`multi-target-relations.jsonl` is append-only. Each record binds:

- schema/campaign identity;
- stable relation ID;
- source and target aliases that already exist in `multi-targets.json`;
- one declared relation class;
- optional Campaign-authorized evidence refs;
- previous-record digest;
- current-record digest;
- `semantic_truth_established: false`.

The chain rejects tampering, duplicate relation IDs, duplicate source/target/type declarations, unknown aliases, unknown evidence, and self-edges.

## Ordering constraints

Only `depends_on` and `release_after` are treated as ordering relations for a deterministic cycle check. A relation that would introduce an ordering cycle is rejected before persistence.

Descriptive reciprocal relationships remain possible. For example, `backend provides_interface_to frontend` and `frontend consumes_interface_from backend` are not treated as a scheduling cycle.

```text
ordering DAG valid != execution plan correct
relationship recorded != relationship inferred
relation evidence valid != architectural truth
```

## Preflight integration

When `multi-target-relations.jsonl` exists, Campaign Preflight adds `multi_target_relation_integrity`. A broken hash chain, dangling alias/evidence reference, malformed record, or ordering cycle makes the mechanical preflight fail. When the companion is absent, the check is `not_applicable`.

Preflight still does not decide whether the declared cross-repository responsibility is warranted or which target should be changed first.

## Evidence ceiling

This feature establishes mechanically valid caller-authored dependency declarations only. It does not establish:

- that the repositories were semantically selected correctly;
- that a declared relation is architecturally true;
- that work should follow the relation direction;
- deployment/release authorization;
- transactional or rollback semantics;
- cross-repository semantic correctness;
- native-harness/product-value evidence.
