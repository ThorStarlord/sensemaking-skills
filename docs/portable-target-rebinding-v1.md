# Portable Target Rebinding v1

**Status:** repository/hermetic implementation contract  
**Campaign schema:** remains v2  
**Authority:** caller supplies the new path; Sensemaking verifies identity/state only

## Purpose

Campaign snapshots intentionally bind repository identity and exact Git/worktree state. Their recorded filesystem path is a locator, not semantic identity. Portable Target Rebinding v1 lets an imported, moved, or relocated Campaign continue against an explicitly supplied local path without asking Sensemaking to discover or choose repositories.

```text
caller-selected path
-> exact identity/state verification
-> durable locator rebind

rebind != repository discovery
rebind != target refresh
rebind != authorization to modify repository
```

## Primary target

```bash
sensemaking-skills campaign target rebind \
  --workspace /path/to/CMP-0001 \
  --target-repo /new/path/to/repository

sensemaking-skills campaign target verify-rebind \
  --workspace /path/to/CMP-0001
```

The primary target's canonical `CampaignState.target_snapshot` is not rewritten. `target-rebind.json` stores a hash-bound locator companion for the same recorded repository identity and snapshot. `CampaignService` consults that companion only when no explicit `target_repo` override was supplied.

A candidate path is accepted only when:

- repository identity and `identity_source` match the recorded snapshot;
- HEAD, tree, tracked/untracked worktree digest, dirty state, and VCS are equivalent;
- the Campaign workspace and target remain disjoint directory trees.

For origin-backed repositories this permits filesystem relocation while preserving the original target provenance. A `local_path` identity is path-derived by design and therefore cannot be safely rebound to a different path under this contract.

## Multi-target aliases

```bash
sensemaking-skills campaign multi-target rebind \
  --workspace /path/to/CMP-0001 \
  --alias backend \
  --target-repo /new/path/to/backend
```

The exact existing alias is caller-selected. The target entry is replaced only with an equivalent snapshot whose repository identity/state matches the prior entry. The target-set digest changes because the locator bytes changed. An append-only `multi-target-rebind-history.jsonl` records the before/after roots and snapshot digests.

Multi-target preflight continues to use the rebound snapshot, so a successful rebind restores normal live verification without treating relocation as semantic completion.

## Failure behavior

Rebinding fails closed for:

- wrong repository identity;
- changed HEAD/tree/worktree state;
- invalid/tampered locator companion;
- unknown multi-target alias;
- workspace/target containment overlap;
- missing/non-Git paths.

A changed repository must use the existing explicit transition/refresh mechanisms. Rebind is deliberately not a way to bless drift.

## Evidence ceiling

```text
rebind valid
!= repository semantically correct
!= repository selected by Sensemaking
!= work authorized
!= changed target state accepted
!= native-harness portability proven
```

The feature improves deterministic transport/continuation mechanics only. It does not create empirical portability evidence or expand the product's semantic authority.
