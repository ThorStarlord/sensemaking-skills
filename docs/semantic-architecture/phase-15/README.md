# Semantic Architecture Phase 15 — Registry Liveness Drift Pilot

**Status:** QUALIFIED BOUNDED PILOT  
**Trigger:** repeated mechanically detectable liveness/status drift observed during recent PM and semantic handoffs  
**Scope:** canonical Skill-tree existence versus compatibility Skill-registry liveness claims only  
**Implementation PR:** #325  
**Qualified candidate:** `1ff498b8fd57c85d590db249a43e8c17a13f5bda`  
**Merge:** `d24e9bda18225bf7aa338df1decb5c201474a66e`

## Why this pilot was authorized

Phase 15 was intentionally deferred until a real maintenance defect appeared. That trigger occurred more than once:

- the PM frontier had to be reconciled after repository state advanced beyond stale status prose;
- Wave 5 qualification exposed a missing canonical registry identity for a new live Skill;
- the PM domain handoff had to repair historical registry notes that still said several now-live capabilities had no current implementation.

Existing Campaign/catalog tests already cover important identity/output/liveness contracts. The remaining uncovered class was narrower: **compatibility registry prose can contradict the mechanically observable canonical Skill tree**.

This pilot does not attempt to validate arbitrary documentation truth.

## Competency question

> Can deterministic machinery reject an internally contradictory Skill-registry liveness statement without deciding whether the Skill is semantically correct, useful, promoted, or supported by a native harness?

**Qualified answer:** yes for the bounded relation implemented here.

## Mechanical claims established

The qualified validator may establish only:

```text
skills/<id>/SKILL.md exists or does not exist
status == proposed while that exact canonical Skill tree exists
status_note contains an explicit no-current-implementation claim while that exact Skill tree exists
status_note explicitly points to a current canonical skills/<id>/ path that is wrong or missing
registry Skill IDs are unique within the inspected registry
```

It may **not** establish:

```text
the Skill is semantically correct
the Skill is repository-qualified
the Skill is native-harness-qualified
the historical invocation metadata is current execution authority
a deprecated historical registry entry must be removed because a current Skill exists
```

In particular:

```text
status: deprecated
+
current canonical Skill tree exists
```

is valid when `deprecated` describes historical invocation metadata and the note correctly identifies the current canonical implementation.

## Qualified validator

`scripts/validate-skill-registry-liveness.py`

Its structured result includes:

```text
semantic_truth_established: false
```

The validator checks by default:

`skills/workflow-planner/references/skill-registry.yaml`

It also accepts `--repo-root` and `--registry` overrides for bounded fixtures and local conformance checks.

## Qualified rejection coverage

The exact candidate passed tests proving rejection of:

1. a registry note claiming `no current implementation yet` while `skills/<id>/SKILL.md` exists;
2. `status: proposed` while `skills/<id>/SKILL.md` exists;
3. a note saying the current canonical implementation lives under `skills/<other-id>/`;
4. a note pointing to `skills/<id>/` when that referenced `SKILL.md` is missing;
5. duplicate registry Skill IDs.

It also proved acceptance of:

- historical/deprecated absent Skills whose notes truthfully describe absence;
- deprecated historical invocation metadata whose note correctly points to an existing current canonical Skill.

The current repository itself passed the new liveness conformance rule on the qualified candidate.

## Integration boundary

The checker runs in Product Validation's existing **Repository and Skill contracts** lane.

It is not:

- a Campaign artifact validator;
- a semantic router;
- a capability selector;
- a universal documentation checker;
- an ontology compiler.

## Phase 15 lifecycle

Phase 15 is now **incremental / trigger-driven** rather than globally complete.

One conformance rule is qualified. Any additional rule requires its own observed maintenance defect, mechanically decidable boundary, rejection fixtures, and exact-head qualification.

A successful liveness checker does not authorize broad Phase 15 expansion.

See `../phase-15-handoff.md` for qualification evidence and future-phase boundaries.
