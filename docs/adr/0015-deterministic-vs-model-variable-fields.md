# ADR 0015: Deterministic versus Model-Variable Artifact Fields

**Status**: PROVISIONAL — codifies existing, implemented behavior; owner
sign-off still requested to promote to Accepted
**Date**: 2026-07-25
**Provisionally addresses**: Issue #30

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
Largely descriptive of existing behavior; owner should confirm no untested
normative choice is being smuggled in before promoting to Accepted.

**Promotion condition**: this ADR promotes from Provisional to Accepted once
the owner explicitly ratifies the deterministic/model-variable classification
taxonomy above (a single sign-off, not additional evidence-gathering) — the
underlying mechanics are already implemented and exercised live.

---

## Hypothesis

Artifact fields split cleanly into a deterministic (machine-parsed,
contract-declared) class and a model-variable (prose) class, and validators
should enforce shape only on the former.

## Supporting evidence

- `skills/workflow-planner/references/artifact-contracts.yaml` already
  declares routing fields (`primary_fog_type`, `recommended_workflow_id`,
  `escalation_recommended`, etc.) as structured fields, and
  `tests/test_field_contract_agreement.py` already enforces that routing
  field reads match declared contract fields (per CLAUDE.md's
  verification-discipline rule) — this is existing, running code, not a
  new proposal.
- PR #59's live Step-1 run and PR #65's live Step-2 runs (positive and
  negative) both exercised real validators (`validate-brief.py`,
  `validate-artifact.py`, `validate-architectural-review-recommendation.py`)
  against live-model-generated prose plus structured YAML blocks, and both
  passed without the validators rejecting prose-level variation — direct,
  repeated evidence for the "validators enforce shape only on the
  deterministic class" principle.
- The `Lx`-vs-bare-number evidence-citation relaxation (cited in CLAUDE.md)
  is a real, already-shipped precedent for "don't over-constrain the
  model-variable class."

## Missing evidence

- No merged evidence tests a case where a *new* field is added and
  classified at proposal time — the "any new field must be classified"
  consequence is aspirational process, not yet exercised.
- Canonical-format choice (Markdown-with-embedded-YAML) is argued by
  analogy to ADR 0004, not independently tested in this campaign.

## Experiment or review trigger

Revisit if a future contract change introduces a field that doesn't cleanly
fit either class, or if a validator is caught enforcing shape on a
model-variable field (which would falsify the "no validator should reject
for prose-level variation" consequence).

## Status rationale

**Provisional** rather than Proposed: unlike ADR 0014, this ADR mostly
describes contracts and validator behavior that already exist and were
exercised live in PR #59 and #65, not a first-time policy choice. It is not
moved all the way to Accepted because the "any new field must be classified
at proposal time" process commitment has not yet been exercised, and formal
owner sign-off on the classification taxonomy itself is still pending —
promotes to Accepted once that sign-off is given (see "Owner sign-off
required" above for the exact condition).
