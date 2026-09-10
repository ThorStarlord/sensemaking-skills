# Semantic Architecture Phase 15 — Registry Liveness Drift Pilot

**Status:** ACTIVE BOUNDED PILOT  
**Trigger:** repeated mechanically detectable liveness/status drift observed during recent PM and semantic handoffs  
**Scope:** canonical Skill-tree existence versus compatibility Skill-registry liveness claims only

## Why this pilot is authorized

Phase 15 was intentionally deferred until a real maintenance defect appeared. That trigger has now occurred more than once:

- the PM frontier had to be reconciled after repository state advanced beyond stale status prose;
- Wave 5 qualification exposed a missing canonical registry identity for a new live Skill;
- the PM domain handoff had to repair historical registry notes that still said several now-live capabilities had no current implementation.

Existing Campaign/catalog tests already cover important identity/output/liveness contracts. The remaining uncovered class is narrower: **compatibility registry prose can contradict the mechanically observable canonical Skill tree**.

This pilot does not attempt to validate arbitrary documentation truth.

## Competency question

> Can deterministic machinery reject an internally contradictory Skill-registry liveness statement without deciding whether the Skill is semantically correct, useful, promoted, or supported by a native harness?

## Mechanical claims allowed

The pilot may establish only:

```text
skills/<id>/SKILL.md exists or does not exist
status == proposed while that exact canonical Skill tree exists
status_note contains an explicit no-current-implementation claim while that exact Skill tree exists
status_note explicitly points to a current canonical skills/<id>/ path that is wrong or missing
registry skill IDs are unique within the inspected registry
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

is allowed when `deprecated` describes historical invocation metadata and the note correctly identifies the current canonical implementation.

## Candidate validator

`scripts/validate-skill-registry-liveness.py`

Expected machine result includes:

```text
semantic_truth_established: false
```

The validator checks one registry by default:

`skills/workflow-planner/references/skill-registry.yaml`

It accepts `--repo-root` and `--registry` overrides so rejection tests can use bounded fixtures.

## Rejection cases

The pilot must reject at least:

1. a registry note claims `no current implementation yet` while `skills/<id>/SKILL.md` exists;
2. `status: proposed` while `skills/<id>/SKILL.md` exists;
3. a note says the current canonical implementation lives under `skills/<other-id>/`;
4. a note points to `skills/<id>/` but that referenced `SKILL.md` is missing;
5. duplicate registry Skill IDs.

It must accept historical/deprecated absent Skills whose notes truthfully say no implementation exists.

## Integration boundary

The pilot is a repository conformance gate, not a Campaign artifact validator and not a semantic router.

If qualified, add its test surface to Product Validation. Do not add the result to Campaign state, capability ranking, or artifact admission.

## Expansion rule

Do not generalize Phase 15 from this pilot unless later observed defects justify another bounded mechanically decidable rule.

A successful liveness checker does not authorize a universal documentation truth checker, ontology compiler, or prose parser.
