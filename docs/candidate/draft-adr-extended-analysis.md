# DRAFT ADR (unfiled, unnumbered): Section 15 "Extended analysis" field classification

**Status**: DRAFT — not Proposed, not Accepted, no owner review yet. This
is a sketch prepared per ADR 0015's own requirement ("any new field added
to a contract must be classified at proposal time"), originally for five
fields added to `repository_sensemaking_brief` on `candidate/sensemaking-vnext`,
now **four** after an architecture stress-test round dropped `discovery_confidence`
(see "Round 2" below). If this branch's work is ever brought toward
`main`, this sketch is the starting point for a real, numbered,
owner-reviewed ADR — it is not one itself, and nothing in it should be
cited as ratified.
**Date**: 2026-08-09, revised 2026-08-10
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

Classify all four surviving `extended_analysis` fields as **model,
constrained** (the same class ADR 0015 already uses for `weakness_type`)
— not free prose, not machine-programmatic-routing:

| Field | Shape | Classification |
|---|---|---|
| `domain` | list of canonical fog-vocabulary base names | model, constrained |
| `consequential_boundary` | `{description, rationale, is_demonstrated_weakness: bool}` | model, constrained |
| `uncertainty` | `{source: repository_evidence\|empirical\|owner_intent\|external_environment, question: string}` | model, constrained |
| `owner_intent_state` | `{known: string, status: sufficient\|thin\|blocking_unknown}` | model, constrained |

(`discovery_confidence` — dropped 2026-08-10; see "Round 2" below.)

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

~~Five~~ **Four** (revised 2026-08-10, `discovery_confidence` dropped)
additive, non-blocking `model, constrained` fields can carry the vNext
interaction behavior's evidence (uncertainty routing, demonstrated-
weakness scoping) through the real runtime pipeline without weakening any
existing guarantee on the ratified Section 1-14 contract.

## Supporting evidence

- `tests/test_extended_analysis_end_to_end.py` proves the real handoff:
  a realistic model response run through the actual
  `brief_skeleton.reconcile()`, validated through both real validators in
  the chain `artifact-contracts.yaml` declares (`validate-artifact.py`,
  `validate-brief.py`) — not a hand-authored fixture assuming the shape.
  A second test in the same file proves the block's absence changes
  nothing about validation of the pre-existing contract.
- `tests/test_brief_skeleton_extended_analysis.py` (9 tests) and
  `tests/test_validate_brief_extended_analysis.py` (7 tests, after
  removing the `discovery_confidence`-specific case 2026-08-10) prove the
  skeleton/reconcile mechanics and the non-blocking validator behavior in
  isolation, including adversarial/malformed input never crashing or
  blocking.
- The underlying *behavior* these fields carry (investigate-first,
  neutral clarification, evidence-resolved-vs-owner-authorized
  distinction) has real-use evidence from `prototype/repo-sensemaker-vnext`
  — see that branch's `docs/prototypes/real-use-experiment-2026-08-09/`,
  specifically the round 3b interaction-layer independence replication.

## Missing evidence

- ~~No real owner-in-the-loop run has exercised Section 15 through the
  actual runtime end to end~~ **Closed, 2026-08-09/10**: ran the real
  `brief_skeleton.build_skeleton()`/`reconcile()` sequence against this
  repository itself, with genuine (not fabricated) analysis, validated
  through both real validators with zero blocking errors and zero
  `EXTENDED_ANALYSIS_*` warnings. See
  `docs/candidate/real-runtime-run-2026-08-09/`. Still a single instance,
  and the "model" step was performed directly rather than via a live,
  separate `ClaudeAgentSdkSkillExecutor`/SDK invocation (a real
  distinction — see that record's `00-context.md` for exactly what
  differs and why what remains is still a faithful exercise of the real
  path) — a live SDK-invoked run remains a further, not-yet-taken step
  if that distinction ever matters for a decision.
- ~~`discovery_confidence.level: low`'s downstream behavior remains
  untested~~ **Closed by removal, 2026-08-10**: the architecture
  stress-test round didn't just fail to test `low` — it confirmed no
  consumer instruction anywhere (`architectural-review`'s Boundary Rule
  6, `repo-sensemaker`'s Interact) reads `discovery_confidence` at all,
  regardless of value. Dropped rather than wired in; see "Round 2" below.
- ~~No case has yet tested what happens when Section 15 disagrees with
  Section 1-14's own content~~ **Closed, 2026-08-10**: stress-test Case 5
  deliberately constructed exactly this (confirmed to pass both real
  validators with zero errors — no cross-section consistency check
  exists, as expected). The downstream consumer noticed the conflict and
  didn't silently merge the two, but hit a genuine textual ambiguity in
  Boundary Rule 6 (does `is_demonstrated_weakness` require relating to
  Section 6's boundary, or is it free-standing) that produced two
  different, individually-defensible verdicts on identical input.
  Boundary Rule 6 revised in response (see "Round 2"); still deliberately
  **not** adding a validator-level consistency requirement between
  Section 6 and Section 15 — they're allowed to legitimately differ.

## Incidental finding (real-runtime run, unrelated to this proposal's scope)

Building the real-runtime record surfaced a genuine, previously-
undiscovered defect in `brief_skeleton.py`'s pre-existing, unmodified
`reconcile()` logic: its generic flat-field splice stringifies a
harvested Python `None` as literal text `None`, which parses back as the
*string* `"None"`, not YAML `null` — confirmed directly against the
run's own reconciled artifact. This would defeat
`WEAKNESS_TYPE_OTHER_NO_EXPLANATION`'s truthiness check in the exact
case D4 exists to catch, for any model that echoes an explicit `null`
back for a flat field. Not part of this proposal's classification
question (it affects `MODEL_YAML_FIELDS` generally, predates this
branch, and is orthogonal to Section 15's own fields) — recorded here
only because it was found while validating this proposal's real-run
evidence, and belongs on the record. See
`docs/candidate/real-runtime-run-2026-08-09/02-findings.md` for detail.
Not fixed by this branch.

## Round 2 — stress-test-informed revision (2026-08-10)

Per the owner's explicit instruction after reviewing the stress-test
report: apply only the findings the frozen-architecture experiment
earned, nothing broader. Full case detail in
`docs/candidate/stress-test-2026-08-10/`.

1. **`discovery_confidence` dropped, not wired in.** Case 4 established
   that neither documented consumer (`architectural-review`'s Boundary
   Rule 6, `repo-sensemaker`'s Interact decision tree) reads this field
   at all, regardless of its value — the correct verdict in Case 4 came
   entirely from `consequential_boundary`, a different, licensed field.
   Deliberately not inventing a consumer for it now ("field failed to
   earn behavior → invent behavior so it can survive" was explicitly
   rejected as backwards for a discovery prototype) — if a future real
   case demands a confidence-bounding concept, it should be rediscovered
   from that evidence, not resurrected because it already existed once.
2. **`uncertainty.source` taxonomy kept structurally unchanged; its
   `repository_evidence`/`empirical` decision rule clarified.** Case 1
   and Case 3 classified structurally similar "has X already happened"
   questions two different ways. The discriminant was never the
   question's subject or tense — it's whether the answer already exists
   somewhere inspectable (`repository_evidence`: files, logs, traces,
   run history — unsearched, not unknowable) versus requires generating
   a new observation (`empirical`: nothing existing can answer it;
   answering means running/executing/probing something that hasn't
   happened yet). This is now stated explicitly in
   `repo-analysis-template.md` and `repo-sensemaker/SKILL.md`'s Interact
   section, at the point of use, not just implied by example. No new
   value added to the four-way enum.
3. **`architectural-review` Boundary Rule 6, narrow revision.** Case 5's
   actual finding wasn't "Section 6 and Section 15 can disagree" (already
   known/allowed by design) — it was that a consumer facing that
   disagreement had two equally-faithful readings of one sentence,
   producing different verdicts. Revised the rule to state explicitly:
   `is_demonstrated_weakness`'s partial-coverage penalty applies to
   whatever `consequential_boundary` itself describes, never assumed to
   be Section 6's `weakest_boundary` by co-occurrence; a proposal that
   was never targeting Section 15's named boundary at all gets that
   boundary disclosed as a separate, still-open finding, not folded into
   the verdict on what the proposal actually addressed. Deliberately
   **no** schema-level or validator-level equality requirement introduced
   between Section 6 and Section 15 — this is a reading-scope
   clarification for the consumer, not a new producer-side constraint.

Verification: Cases 3, 4, and 5 rerun after these three changes (not the
full six-case round) — see `docs/candidate/stress-test-2026-08-10/round2-results.md`
for the before/after comparison.

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
