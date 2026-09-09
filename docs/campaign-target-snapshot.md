# Durable Campaign Target Snapshot Binding

**Status:** product contract  
**Scope:** Campaign initialization, lifecycle provenance, reconstruction, lineage, and handoff/resume  
**Semantic boundary:** target provenance is mechanical evidence, not semantic judgment

A Sensemaking Campaign may be bound to one explicit Git target repository. The binding answers a narrow mechanical question:

> **Which exact repository identity and working-tree state did this Campaign reconstruct at this lifecycle point?**

It does not answer whether that state is correct, whether a change succeeded, whether work is warranted, or which capability should be selected.

## Initialization

```text
sensemaking-skills campaign init ... --target-repo /path/to/repo
```

captures a first-class `CampaignState.target_snapshot` before the Campaign workspace is committed. Workspace isolation remains enforced independently: the Campaign workspace must not be created inside the target repository.

The durable snapshot contains:

```text
repository_root
repository_id
identity_source       # origin | local_path
head_sha
tree_sha
worktree_sha256
dirty
vcs                    # git
```

`repository_root` is a locator hint for fresh-context reconstruction. `repository_id` is a SHA-256 identity derived from a credential-sanitized `origin` locator when available; otherwise it is derived from the canonical local repository root. Raw credential-bearing remote URLs are never persisted in the snapshot.

## Worktree identity

`worktree_sha256` is deterministic and contains no timestamp. It binds:

- Git index entries (`git ls-files -s`);
- porcelain status, including tracked changes and untracked non-ignored files;
- sorted tracked + untracked non-ignored path names;
- regular-file bytes and executable/mode information;
- symbolic-link targets;
- submodule/directory Git HEAD and status when applicable.

Ignored files are outside this snapshot contract. A repository with the same HEAD but modified tracked bytes or new untracked non-ignored bytes therefore has a different target snapshot.

## Lifecycle transitions

Repository mutation between Campaign decisions is legitimate. Therefore the target snapshot is not globally immutable.

Each new target-bound `TransitionRecord` carries:

```text
from_target_snapshot_sha256
to_target_snapshot_sha256
```

The source digest identifies the exact snapshot recorded by the source Campaign state. At lifecycle commit, deterministic machinery captures the live target and stores it as the destination Campaign state plus the transition destination digest.

```text
previous durable target snapshot
        ↓
agent performs bounded work
        ↓
live repository may change
        ↓
agent authors a Campaign decision
        ↓
deterministic target capture
        ↓
source snapshot digest -> destination snapshot digest
        ↓
existing recoverable Campaign lifecycle commit
```

A transition records that repository state changed. It does **not** claim the change was correct, complete, or warranted.

Target-bound transition history must remain mechanically continuous: after binding begins, a later transition source target digest must equal the prior transition destination digest, and the final transition destination must equal the current Campaign state's target snapshot digest.

## Drift detection

Ordinary target-aware reconstruction (`campaign status`, `campaign validate`, handoff/resume, and user-facing lineage inspection) compares the durable current snapshot with the live target repository.

Fail-closed diagnostics include:

```text
TARGET_REPOSITORY_UNAVAILABLE
TARGET_REPOSITORY_IDENTITY_MISMATCH
TARGET_SNAPSHOT_DRIFT
TARGET_TRANSITION_BINDING_INCOMPLETE
TARGET_TRANSITION_BINDING_REGRESSION
TARGET_TRANSITION_CHAIN_MISMATCH
TARGET_CURRENT_SNAPSHOT_MISMATCH
TARGET_SNAPSHOT_MISSING
```

Unrecorded drift does not automatically create a transition. The next lifecycle decision remains agent-authored; the target machinery only records the destination snapshot when that explicit transition is committed.

## Handoff and fresh-context resume

`CampaignHandoff` already embeds the exact current `CampaignState`, so a target-bound handoff contains the current target snapshot as part of its normal integrity-bound reconstruction digest. Fresh-context resume additionally verifies that the live target still matches the durable snapshot before accepting the handoff.

Thus a fresh agent can reconstruct both:

1. the Campaign's semantic state; and
2. the exact repository identity/state that semantic state concerns.

Neither reconstruction chooses what the fresh agent should do next.

## Lineage

Existing P8 lineage digests the exact `TransitionRecord`, so target source/destination snapshot digests are transitively integrity-bound by transition lineage. The `campaign lineage` surface also exposes the current target snapshot and each transition's source/destination target snapshot SHA-256 values.

Evidence lineage and target lineage remain separate claims:

```text
transition consumed evidence X
!=
repository snapshot Y proves X was correct
```

## Backward compatibility

Target binding is an additive schema-v2 contract. Historical Campaigns remain valid and honestly **target-unbound**.

When target fields are absent, canonical serialization omits them. This is deliberate: pre-binding schema-v2 Campaign state/transition bytes and their existing trace digests retain their original canonical shape.

A legacy target-unbound Campaign is not retroactively assigned a repository identity. Deterministic machinery never invents historical provenance.

## Control boundary

The invariant is:

```text
target snapshot bound
!= repository correct

repository changed
!= repair succeeded

target identity
!= warranted responsibility

target drift
!= automatic transition

target provenance
!= capability selection or execution authority
```

And the existing architectural boundary remains unchanged:

```text
Campaign Controller != semantic router
```
