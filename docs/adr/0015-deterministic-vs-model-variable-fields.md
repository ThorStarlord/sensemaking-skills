# ADR 0015: Deterministic versus Model-Variable Artifact Fields

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #30

---

## Context

Infrastructure-level determinism is already established (artifact type,
output path, validator, workflow step, failure classification — see ADR
0010). The open question is at the content-contract level: which fields
inside an artifact must be structurally consistent across runs, and which
may vary.

## Decision

Split every artifact field into one of two classes, declared per-field in
`skills/workflow-planner/references/artifact-contracts.yaml`:

**Deterministic (machine-readable YAML block fields)** — must always be
present, always the same type/shape, validated by `validate-artifact.py` +
the specialized validator:
- `artifact_id`, `created_at`, `created_by`, `immutable`
- Routing fields (`primary_fog_type`, `recommended_workflow_id`,
  `chosen_workflow_id`, `escalation_recommended`)
- Traceability fields (`source_intent_ref`)
- Any field a downstream consumer parses programmatically

**Model-variable (prose/Markdown body)** — free-form, validated only for
required section *presence*, not content:
- Summary, evidence narrative, recommendation prose, weakest-boundary
  analysis text

**Evidence attachment**: required on every major finding/claim that drives
a routing decision (fog type, recommended workflow); not required on
incidental prose observations. This narrows and feeds ADR 0016 (evidence
policy).

**Canonical format**: Markdown remains canonical (matches ADR 0004's
"machine-produced Markdown" pattern and the existing validator suite).
JSON/YAML blocks embedded in Markdown are the machine-readable subset, not
a separate canonical format — this avoids a dual-source-of-truth problem
and matches every validator already in the repo.

**Validator strictness**: validators must accept variation in the
model-variable class and enforce exact shape only on the deterministic
class — already this repo's practice (`validate-brief.py` etc.), and
explicitly the principle behind relaxing evidence-line format acceptance
per CLAUDE.md's verification-discipline notes.

## Consequences
- No validator should reject an artifact for prose-level variation.
- Any new field added to a contract must be classified at proposal time.
- This directly informs ADR 0016 (evidence policy) and ADR 0021
  (production-readiness — "is the artifact contract stable").

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.
