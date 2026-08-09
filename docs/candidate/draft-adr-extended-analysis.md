# DRAFT ADR (unfiled, unnumbered): Section 15 "Extended analysis" field classification

**Status**: DRAFT — not Proposed, not Accepted, no owner review yet. This
is a sketch prepared per ADR 0015's own requirement ("any new field added
to a contract must be classified at proposal time") for the five fields
added to `repository_sensemaking_brief` on `candidate/sensemaking-vnext`.
If this branch's work is ever brought toward `main`, this sketch is the
starting point for a real, numbered, owner-reviewed ADR — it is not one
itself, and nothing in it should be cited as ratified.
**Date**: 2026-08-09
**Depends on**: ADR 0015 (Accepted — the classification taxonomy this
sketch instantiates), ADR 0016 (Accepted — governs `evidence_excerpts`,
untouched by this proposal), ADR 0014 (Accepted — the repo-sensemaker /
architectural-review boundary this proposal's Decision 4 relies on).

---

## Context

`prototype/repo-sensemaker-vnext` (PR #164, exploratory, never merged)
built five additive brief fields (`domain`, `discovery_confidence`,
`consequential_boundary`/`is_demonstrated_weakness`, `uncertainty`,
`owner_intent_state`) and exercised them across four rounds of testing,
including two genuinely-isolated real-use replications (see
`docs/prototypes/real-use-experiment-2026-08-09/` on that branch). That
branch never wired these fields through the real runtime
(`scripts/brief_skeleton.py`'s skeleton/reconcile mechanism) — it was
invoked outside `workflow-runtime.py` throughout its history, so the
fields never had to survive `reconcile()`, which only ever splices model
content into pre-declared holes and discards everything else.

`candidate/sensemaking-vnext` closes that gap: the same five fields (with
two revisions — see Decision below) are wired into a real, dedicated
`## 15. Extended analysis (candidate)` section, harvested and spliced by
`brief_skeleton.reconcile()`, checked (non-blockingly) by
`validate-brief.py`, and declared in `artifact-contracts.yaml` under a
new `candidate_machine_fields` key. Per ADR 0015's own consequence
("any new field added to a contract must be classified at proposal
time"), that declaration needs the classification this sketch documents
— written down now, before any owner reviews it, not after.

## Decision (proposed, not ratified)

Classify all five `extended_analysis` fields as **model, constrained**
(the same class ADR 0015 already uses for `weakness_type`) — not free
prose, not machine-programmatic-routing:

| Field | Shape | Classification |
|---|---|---|
| `domain` | list of canonical fog-vocabulary base names | model, constrained |
| `discovery_confidence` | `{level: high\|medium\|low, why_bounded: string}` | model, constrained |
| `consequential_boundary` | `{description, rationale, is_demonstrated_weakness: bool}` | model, constrained |
| `uncertainty` | `{source: repository_evidence\|empirical\|owner_intent\|external_environment, question: string}` | model, constrained |
| `owner_intent_state` | `{known: string, status: sufficient\|thin\|blocking_unknown}` | model, constrained |

**Enum/type checks are non-blocking (`severity="warning"`)** — stronger
than `weakness_type`'s ADR-0015-ratified "required but non-blocking"
(D2): this block is **optional and non-blocking**. Absence produces
nothing; presence with an invalid value never fails the artifact. This
is a deliberately weaker commitment than `weakness_type` got, reflecting
that these fields have real-use evidence behind the *behavior* they
support but no owner ratification of the *fields themselves* yet.

**Not classified as routing-deterministic**: none of the five fields are
added to `workflow-runtime.py`'s `_WORKFLOW_ID_FIELDS` / `_FOG_TYPE_FIELDS`
or read anywhere in automated routing. `tests/test_field_contract_agreement.py`
is unaffected by this proposal by design, not by oversight.

**Revision from the prototype's schema** (see
`docs/candidate/architecture-decision.md`, Decision 2, for full
rationale): `owner_intent_state` drops the prototype's freestanding
`unresolved` prose field. What's unresolved, when `uncertainty.source`
is `owner_intent`, is already `uncertainty.question` — keeping a second,
separately-authored copy of the same fact risked the two silently
drifting apart. `evidence_status_notes` (the prototype's sixth field) is
dropped entirely — it was never exercised in any real run across the
prototype's full history (four construction/validation rounds), the
weakest evidentiary tier in the working evidence hierarchy
(speculative, never exercised).

## Consequences

- No validator may ever reject an otherwise-valid brief because of
  Section 15's content — this is the one hard invariant this sketch
  asks a future real ADR to keep, regardless of what else changes about
  the field shapes.
- If any of these fields is later promoted to drive real routing
  (e.g. `uncertainty.source` gating an automated escalation), that
  promotion needs its own classification decision at that time — this
  sketch does not pre-authorize it.
- Promoting any field out of `candidate_machine_fields` into
  `recommended_machine_fields` or `required_machine_fields` requires an
  explicit owner decision per field, not a blanket promotion of the
  whole block — matching [[vnext-three-lane-promotion-strategy]]'s
  "behavioral rule can promote before schema/packaging does, and
  per-concept, not as a bundle" principle.

## Owner sign-off required

Nothing in this document is ratified. It exists so that if/when this
branch's work is proposed for real promotion, the classification
decision doesn't have to be made for the first time under review
pressure — it is drafted, in the open, now.

---

## Hypothesis

Five additive, non-blocking `model, constrained` fields can carry the
vNext interaction behavior's evidence (uncertainty routing, demonstrated-
weakness scoping, confidence bounding) through the real runtime pipeline
without weakening any existing guarantee on the ratified Section 1-14
contract.

## Supporting evidence

- `tests/test_extended_analysis_end_to_end.py` proves the real handoff:
  a realistic model response run through the actual
  `brief_skeleton.reconcile()`, validated through both real validators in
  the chain `artifact-contracts.yaml` declares (`validate-artifact.py`,
  `validate-brief.py`) — not a hand-authored fixture assuming the shape.
  A second test in the same file proves the block's absence changes
  nothing about validation of the pre-existing contract.
- `tests/test_brief_skeleton_extended_analysis.py` (9 tests) and
  `tests/test_validate_brief_extended_analysis.py` (8 tests) prove the
  skeleton/reconcile mechanics and the non-blocking validator behavior in
  isolation, including adversarial/malformed input never crashing or
  blocking.
- The underlying *behavior* these fields carry (investigate-first,
  neutral clarification, evidence-resolved-vs-owner-authorized
  distinction) has real-use evidence from `prototype/repo-sensemaker-vnext`
  — see that branch's `docs/prototypes/real-use-experiment-2026-08-09/`,
  specifically the round 3b interaction-layer independence replication.

## Missing evidence

- No real owner-in-the-loop run has exercised Section 15 through the
  actual runtime (`ClaudeAgentSdkSkillExecutor`) end to end — the
  end-to-end test above proves the mechanism works, not that a real
  diagnostic run produces a useful Section 15 in practice.
- `discovery_confidence.level: low`'s downstream behavior remains
  untested in any run, prototype or candidate.
- No case has yet tested what happens when Section 15 disagrees with
  Section 1-14's own content (e.g. `consequential_boundary` describing a
  different boundary than Section 6's `weakest_boundary`) — the validator
  doesn't check cross-section consistency, and whether it should is an
  open question this sketch doesn't resolve.

## Experiment or review trigger

Revisit if: a real runtime-invoked run produces a Section 15 a human
finds actively misleading or unhelpful; any field needs to drive real
routing; or the cross-section-consistency question above is forced by a
real case.

## Status rationale

Kept as DRAFT rather than advanced to Proposed because no owner has
reviewed it yet — per Mode B+'s retained boundary, drafting a
replacement/amendment candidate is authorized; claiming any status beyond
DRAFT is not.
