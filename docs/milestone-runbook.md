# Historical Milestone Runbook — Features #298–#300

**Status:** historical milestone record; **not current operational authority**  
**Applies to:** CI Authority Reconciliation, v0.3 Release Baseline Rebuild, Durable Target Snapshot Binding  
**Product version at milestone:** 0.3.0  
**Feature-3 product baseline:** `24a88bf6311122dae1257999f5a7379cb0b095d5`

This document previously served as the post-milestone operating runbook for Features #298–#300. It is retained for historical reconstruction only.

For **current** repository operations and qualification commands, use:

```text
docs/operations-runbook.md
```

Executable CI authority remains:

```text
.github/workflows/validation.yml
.github/workflows/lab-validation.yml
.github/workflows/release-candidate.yml
```

Do not use historical command lists from this milestone as evidence that current Product Validation or repository-contract validation has been reproduced.

## Milestone ledger

| Feature | PR | Historical operational result |
|---|---:|---|
| CI Authority Reconciliation | #298 | `pyproject.toml` became sole literal version authority; Product Validation and Lab Validation received distinct claim boundaries; installed-wheel tests moved under product validation; stray `.claude/worktrees/*` gitlinks were rejected/removed. |
| v0.3 Release Baseline Rebuild | #299 | Version 0.3.0 release candidate; installed canonical validator runtime; wheel/sdist qualification; `twine check`; fresh-install proofs. |
| Durable Target Snapshot Binding | #300 | Campaign state gained durable target repository identity, source/destination target digests, live drift detection, target-aware lineage and handoff/resume. |

## Historical invariants preserved

The milestone established several boundaries that remain useful context:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
lineage != semantic warrant
handoff != semantic recommendation
Skill copied to discovery root != harness observed or invoked Skill
external verifier PASS != semantic truth

target snapshot bound != repository correct
repository changed != repair succeeded
target identity != warranted responsibility
target drift != automatic transition
target provenance != capability selection or execution authority
```

Later repository changes added substantial Product Validation and repository-contract coverage, including B7 semantic-reference audit and Strategic State Contract Validation v0. Those later commands are intentionally **not copied into this historical document**; the current runbook owns operator navigation.

## Historical reconstruction

If exact former procedures are needed, inspect Git history for this path at the relevant milestone commit. Do not restore historical "source of truth" wording as current authority.
