# Multi-Repository Campaigns v1

**Status:** owner-authorized repository-only/hermetic construction package  
**Empirical experiments:** none required or performed  
**Campaign schema:** remains v2  
**Representation:** additive target-set companion

## Purpose

Support one explicitly scoped responsibility that spans multiple Git repositories without weakening the existing single-primary-target Campaign contract or giving Sensemaking authority to discover/select repositories semantically.

## Representation

The existing `CampaignState.target_snapshot` retains its current meaning. Multi-repository scope is represented by `multi-targets.json`, a deterministic companion whose identity is SHA-256 over its canonical target-set content.

Each target records:

```text
alias
role
authority
evidence_refs
TargetSnapshot
TargetSnapshot SHA-256
```

The target set records:

```text
schema_version
Campaign ID
sorted target entries
semantic_truth_established: false
target_set_sha256
```

`multi-target-history.jsonl` records explicit per-target refresh edges after authorized work.

## CLI

```text
campaign multi-target add
campaign multi-target inspect
campaign multi-target verify
campaign multi-target refresh
```

`add` requires the caller to explicitly provide repository path, alias, role, and authority. It captures mechanical Git/worktree identity using the existing TargetSnapshot implementation.

`verify` detects repository unavailability, identity mismatch, and unrecorded worktree/snapshot drift. It can check one explicit alias or all declared targets.

`refresh` records the current live snapshot for one explicit alias only when repository identity still matches. It does not decide whether the change was correct or whether refresh should occur.

## Identity and safety rules

- target aliases are unique and bounded to safe identifiers;
- one repository identity cannot be bound twice under different aliases;
- Campaign workspace and target repository trees must be disjoint;
- evidence refs must already be within Campaign evidence authority;
- recorded snapshot hashes and the target-set hash fail closed on tampering;
- refresh refuses repository identity replacement;
- the original Campaign schema v2 primary-target field is not rewritten automatically.

## Drift / verification semantics

```text
TargetSnapshot captured
        ↓
work occurs externally/through an authorized capability
        ↓
multi-target verify
        ↓
PASS: live bytes match recorded snapshot
or
FAIL: unavailable / identity mismatch / snapshot drift
        ↓
explicit multi-target refresh (when authorized)
        ↓
new snapshot + append-only history edge
```

## Atomicity boundary

This implementation does **not** claim cross-repository transactional atomicity. Each target has independent identity and snapshot state. A Campaign may therefore temporarily contain mixed before/after target snapshots while explicit refreshes are being recorded.

```text
multi-target integrity != cross-repo transaction
all targets verified != semantic completion
same Campaign != atomic deployment unit
```

If true cross-repository atomic commit/deploy semantics are ever required, that is a separate responsibility and likely a substantially larger architecture decision.

## Authority boundary

```text
target supplied by agent/owner
        ↓
mechanical snapshot capture
        ↓
deterministic target-set persistence
        ↓
mechanical drift verification

NOT:
repository discovery
→ automatic scope expansion
→ automatic repository selection
```

## Non-goals

This package does not introduce:

- automatic repository discovery or selection;
- cross-repository semantic dependency inference;
- cross-repository transaction/rollback machinery;
- automatic responsibility selection;
- automatic deployment or merge;
- Campaign schema v3;
- native-harness/product-value experimentation.

Repository qualification establishes the representation, identity, drift, and rejection contracts only.