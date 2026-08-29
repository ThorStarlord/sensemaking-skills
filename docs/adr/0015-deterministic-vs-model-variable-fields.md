# ADR 0015: Deterministic versus Model-Variable Artifact Fields

**Status**: ACCEPTED (with a ratified addendum) — 2026-07-26 by explicit
owner decision (D2, D3, D4) recorded in
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`
**Date**: 2026-07-25 (revised 2026-07-26)
**Resolves**: Issue #30

**2026-07-26 addendum, owner-ratified**: the auteur campaign's final rerun
(PR #78) failed on `UNKNOWN_WEAKNESS_TYPE` — the classification taxonomy (7
registered weakness types) had no dedicated field, only a substring-match
check against free prose (`scripts/validate-brief.py:279-286`), which the
2026-07-26 product-contract review
(`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md`, Part 3) identified as the
same class of over-strict, prose-brittle validation this ADR's Consequences
section already warns against. The owner explicitly approved:
- **D2**: `weakness_type` is required metadata but **non-blocking** — its
  absence or an unrecognized value must not, by itself, invalidate a brief.
- **D3**: `weakness_type` becomes a **dedicated controlled-vocabulary
  deterministic field** (the classification class already defined below),
  separate from and not overriding the free-form weakest-boundary prose.
- **D4**: the enum includes `Other`, which requires a companion explanation
  field; an unmatched/unmappable weakness type resolves to `Other` plus
  explanation, not to a hard failure.

This is a new instance of the existing "controlled-vocabulary deterministic"
field class defined below (same class as `primary_fog_type`), not a new
class. **This ADR ratifies the field's classification, not its
implementation** — the contract entry, skeleton, prompt, and validator
changes are tracked separately under D10's contract-redesign phase and are
not authorized by this revision alone.

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
~~Largely descriptive of existing behavior; owner should confirm no untested
normative choice is being smuggled in before promoting to Accepted.~~

**Given, 2026-07-26**: the owner ratified the `weakness_type` addendum
(D2/D3/D4) in `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`. Promoted to
Accepted, with the `weakness_type` addendum noted as a ratified
classification, implementation tracked separately (D10).

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

**2026-07-26 update — promoted to Accepted.** Formal owner sign-off on the
classification taxonomy was the sole blocking condition, and it has now been
given, extended explicitly to cover the `weakness_type` field gap surfaced
by PR #78 (D2/D3/D4). Preserved for record, the prior rationale:

**Provisional** rather than Proposed: unlike ADR 0014, this ADR mostly
describes contracts and validator behavior that already exist and were
exercised live in PR #59 and #65, not a first-time policy choice. It was not
moved all the way to Accepted because the "any new field must be classified
at proposal time" process commitment had not yet been exercised, and formal
owner sign-off on the classification taxonomy itself was pending. The
`weakness_type` field is itself the first live exercise of that "any new
field must be classified at proposal time" process commitment — it was
classified (as controlled-vocabulary deterministic, per D3) at the point of
proposal, before implementation, which is exactly what this ADR's
Consequences section committed to.


---

## 2026-08-29 addendum (owner-ratified): representation_sufficiency as primary MODEL_WARRANT authority

Owner decision recorded in `experiments/product-hypothesis-b/PRODUCT_HYPOTHESIS_B_EXPERIMENT.md`
(sections 67-72, directives #25-#28). This addendum canonically ratifies the final
field classification and warrant-authority semantics. Historical experiment records
remain append-only and are not rewritten (the jtbl final dogfood stays SAFE_INCONCLUSIVE).

### Decision

`representation_sufficiency` is the PRIMARY, task-relative MODEL_WARRANT authority on
the Repository Sensemaking Brief. It is a controlled model-authored semantic field
(a new instance of the controlled-vocabulary/model-judgment class, alongside
`weakness_type`/`outcome`): the producer supplies the reasoning-episode judgment, the
runtime maps it deterministically, the validator is the acceptance authority. It is an
additive, optional field: absent/invalid fails closed (INCONCLUSIVE), so no
schema_version bump is required merely for its addition.

Authoritative mapping (single canonical judge):
- `sufficient` -> NO
- `insufficient_bounded` (contract-valid: rationale names a consequential gap AND
  non-empty `needed_representation`) -> PARTIAL
- `inconclusive` -> INCONCLUSIVE
- missing / malformed / contract-invalid -> INCONCLUSIVE (fail closed)
- FULL remains deferred and is never inferred.

Mechanical probes (behavioral_flow_unassembled, provenance_scattered,
existing_artifact_self_derived) are diagnostic/supporting evidence to the assessment,
NOT independent MODEL_WARRANT vetoes. `fresh_comprehension_needed` does NOT gate
production warrant. `minimum_subset_suffices` is subsumed by the
`insufficient_bounded` + `needed_representation` contract. Absence of evidence is never
treated as insufficiency (no absent->FALSE).

### Related ratified canonical points

- Section 8 `evidence_excerpts` is the structured evidence authority for the
  deterministic Section-13 `evidence` projection (fail-closed).
- Section 13 is ONE atomic runtime-serialized YAML mapping (no field-by-field splice).
- MODEL_WARRANT and REPOSITORY_ACTION_OUTCOME are ORTHOGONAL; NO_CHANGE is
  affirmative-only; INCONCLUSIVE gates before representation materialization, action
  routing, and NO_CHANGE terminalization (STOPPED_WITHOUT_ACTION / MODEL_WARRANT_INCONCLUSIVE).
- The local Probe Engine uses the runtime/session-owned same-episode
  `expected_probe_report_path` when that contract is available (no heuristic discovery).
- The runtime warrant seam must consume the newly validated brief (producer ->
  reconciliation -> validation -> MODEL_WARRANT evaluation), never a stale/nonexistent one.
- The warrant target_revision is the exact target-checkout revision (git -C <target>
  rev-parse HEAD), not a framework branch name; it fails closed when not establishable.

### Evidence

187-test candidate qualification (warrant/atomic/evidence-projection/probe/orthogonality/
validator/runtime suites), the jtbl SAFE_INCONCLUSIVE external agent-mediated observation,
and the frozen jtbl P+C re-evaluation to NO under these semantics (regression, not a
historical rewrite). See ADR 0013 (agent-native orchestration primary) for the execution/CLI
claim boundary.
