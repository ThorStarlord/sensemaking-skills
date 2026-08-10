# ADR 0024: Section 15 "Extended analysis" field classification

**Status**: ACCEPTED — owner decision 2026-08-10: (a) accept the
`candidate/sensemaking-vnext` architecture as the working default, and (b)
classify the four surviving `extended_analysis` fields as ordinary optional,
model-constrained contract fields (no permanent `candidate_machine_fields`
tier). Merge to `main` is a separate repository action, pending and not part
of this record.
**Date**: 2026-08-10 (drafted 2026-08-09 on `candidate/sensemaking-vnext`
as an unfiled sketch; revised 2026-08-10 after the architecture stress-test
round; filed as this numbered ADR on owner acceptance)
**Depends on**: ADR 0015 (Accepted — the classification taxonomy this ADR
instantiates), ADR 0016 (Accepted — governs `evidence_excerpts`, untouched
by this ADR), ADR 0014 (Accepted — the repo-sensemaker / architectural-review
boundary this ADR's Decision relies on), ADR 0010 (Accepted — the runtime
owns artifact paths; Section 15 is spliced through the runtime-owned
skeleton/reconcile mechanism).

---

## 1. Context and problem statement

`prototype/repo-sensemaker-vnext` (PR #164, exploratory, never merged)
built five additive brief fields (`domain`, `discovery_confidence`,
`consequential_boundary`/`is_demonstrated_weakness`, `uncertainty`,
`owner_intent_state`) and exercised them across four rounds of testing,
including two genuinely-isolated real-use replications (see
`docs/prototypes/real-use-experiment-2026-08-09/` on that branch). That
branch never wired these fields through the real runtime
(`scripts/brief_skeleton.py`'s skeleton/reconcile mechanism) — it was
invoked outside `workflow-runtime.py` throughout its history, so the fields
never had to survive `reconcile()`, which only ever splices model content
into pre-declared holes and discards everything else.

`candidate/sensemaking-vnext` closed that gap: the fields (with revisions —
see below) were wired into a real, dedicated `## 15. Extended analysis`
section, harvested and spliced by `brief_skeleton.reconcile()`, checked
(non-blockingly) by `validate-brief.py`, and declared in
`artifact-contracts.yaml`. Per ADR 0015's own consequence ("any new field
added to a contract must be classified at proposal time"), that declaration
needs the classification this ADR records.

The candidate architecture then survived a frozen-architecture stress-test
round (six adversarial cases, 2026-08-10, see
`docs/candidate/stress-test-2026-08-10/`; architecture files verified
byte-identical to the pre-registration reference throughout) plus three
targeted reruns after narrow revisions. One of the five fields was falsified
by that experiment and deliberately removed; no case demanded a new Skill,
a packaging change, a new validator, or a new governance mechanism. On the
strength of that record, the owner accepted the surviving architecture and
the four surviving fields as the working default design.

## 2. Decision

Classify the four surviving `extended_analysis` fields as **model,
constrained** (the same class ADR 0015 already uses for `weakness_type`) —
not free prose, not machine-programmatic-routing:

| Field | Shape | Classification |
|---|---|---|
| `domain` | list of canonical fog-vocabulary base names | model, constrained |
| `consequential_boundary` | `{description, rationale, is_demonstrated_weakness: bool}` | model, constrained |
| `uncertainty` | `{source: repository_evidence\|empirical\|owner_intent\|external_environment, question: string}` | model, constrained |
| `owner_intent_state` | `{known: string, status: sufficient\|thin\|blocking_unknown}` | model, constrained |

They are ordinary **optional, non-blocking** contract fields — declared in
`artifact-contracts.yaml`'s `recommended_machine_fields` for
`repository_sensemaking_brief`, not under any candidate/incubation key. The
`candidate_machine_fields` key is removed; no permanent candidate lifecycle
tier exists. Canonical does not mean required: a brief without Section 15 is
complete and valid; a brief with it is richer.

**Enum/type checks are non-blocking (`severity="warning"`)** — stronger
than `weakness_type`'s ADR-0015-ratified "required but non-blocking" (D2):
this block is **optional and non-blocking**. Absence produces nothing;
presence with an invalid value never fails the artifact.

**Not classified as routing-deterministic**: none of the four fields are
added to `workflow-runtime.py`'s `_WORKFLOW_ID_FIELDS` / `_FOG_TYPE_FIELDS`
or read anywhere in automated routing. `tests/test_field_contract_agreement.py`
is unaffected by this ADR by design, not by oversight. The fields exist for
a human, or a downstream skill reading the brief directly, to use at their
own discretion (see `repo-sensemaker`'s Interact section).

**Section shape**: a single Section 15 `extended_analysis:` YAML mapping
(`## 15. Extended analysis`, `schema_version: 1` inside the block),
harvested and spliced by `brief_skeleton.reconcile()` through the
runtime-owned `<!-- MODEL_SECTION:extended_analysis:BEGIN/END -->` markers.

**Revision from the prototype's schema** (see
`docs/candidate/architecture-decision.md`, Decision 2, for full rationale):
`owner_intent_state` drops the prototype's freestanding `unresolved` prose
field — what's unresolved, when `uncertainty.source` is `owner_intent`, is
already `uncertainty.question`; keeping a second, separately-authored copy
of the same fact risked the two silently drifting apart.
`evidence_status_notes` (the prototype's sixth field) is dropped entirely —
never exercised in any real run across the prototype's full history.

## 3. What the stress test changed — and why `discovery_confidence` is gone

The frozen-architecture stress-test round (six cases, 2026-08-10) earned
three narrow revisions, applied without expanding the architecture:

1. **`discovery_confidence` dropped, not wired in.** Case 4 established
   that neither documented consumer (`architectural-review`'s Boundary Rule
   6, `repo-sensemaker`'s Interact decision tree) read this field at all,
   regardless of its value — the correct verdict in Case 4 came entirely
   from `consequential_boundary`, a different, licensed field. This matched
   the pre-registered drop criterion ("decorative — nothing reads it"), so
   the field was removed completely (skeleton, template, contract,
   validator, tests) rather than given an invented consumer. This is the
   intended failure mode of a discovery prototype: the architecture got
   smaller because testing killed something. If a future real case demands a
   confidence-bounding concept, it should be rediscovered from that
   evidence, not resurrected because it once existed.
2. **`uncertainty.source` taxonomy kept structurally unchanged; its
   `repository_evidence`/`empirical` decision rule clarified.** Cases 1 and
   3 classified structurally similar "has X already happened" questions two
   different ways. The discriminant is not the question's subject or tense —
   it is whether the answer already exists somewhere inspectable
   (`repository_evidence`: files, logs, traces, run history — unsearched,
   not unknowable) versus requires generating a new observation
   (`empirical`: nothing existing can answer it; answering means
   running/executing/probing something that hasn't happened yet). The rule
   is now stated explicitly at the point of use in
   `repo-analysis-template.md` and `repo-sensemaker/SKILL.md`'s Interact
   section. The principle that empirical uncertainty is never resolved by
   asking the owner to guess is preserved.
3. **`architectural-review` Boundary Rule 6, narrow revision.** Case 5's
   finding was not "Section 6 and Section 15 can disagree" (already
   known/allowed by design) — it was that a consumer facing that
   disagreement had two equally-faithful readings of one sentence,
   producing different verdicts. The rule now states explicitly:
   `is_demonstrated_weakness`'s partial-coverage penalty applies to whatever
   `consequential_boundary` itself describes, never assumed to be Section
   6's `weakest_boundary` by co-occurrence; a proposal that was never
   targeting Section 15's named boundary gets that boundary disclosed as a
   separate, still-open finding. Deliberately **no** schema- or
   validator-level equality requirement between Section 6 and Section 15 —
   they are allowed to legitimately differ.

**Verdict semantics (accepted as a consequence of the Rule 6 revision)**: a
post-revision rerun of Case 4 produced a verdict change (`pursue_narrowed`
→ `pursue`) on identical input — not because the field removal changed
anything, but because the reviewer now judged the selected fix unrelated to
Section 15's named boundary, and disclosed the stronger-priority competing
candidate as a separate finding instead of narrowing the verdict.
Architectural review judges the **quality/scope of the proposed direction**
against the brief's named boundary; it does **not** double as a repository
prioritization engine. Priority-vs-other-work questions remain the owner's
to decide, and are surfaced as separate findings when the reviewer has
grounds. This behavior was provisionally accepted by the owner rather than
re-revised.

## 4. Consequences

- No validator may ever reject an otherwise-valid brief because of Section
  15's content — this is the one hard invariant this ADR keeps, regardless
  of what else changes about the field shapes.
- If any of these fields is later promoted to drive real routing (e.g.
  `uncertainty.source` gating an automated escalation), that promotion needs
  its own classification decision at that time — this ADR does not
  pre-authorize it.
- Any future field promotion or change of shape requires an explicit owner
  decision per field. The `candidate_machine_fields` key does not exist and
  a permanent incubation tier is deliberately **not** introduced: the
  stress cycle found no governance mechanism necessary, and machinery
  should not be built until observed behavior demands it.
- `## 15. Extended analysis` is now part of the runtime-owned skeleton, so
  the heading is produced by `brief_skeleton.py` and validated
  (non-blockingly) by `validate-brief.py`. The validator still tolerates the
  pre-ratification `## 15. Extended analysis (candidate)` heading spelling
  in already-written artifacts.

## 5. Supporting evidence

- `tests/test_extended_analysis_end_to_end.py` proves the real handoff: a
  realistic model response run through the actual
  `brief_skeleton.reconcile()`, validated through both real validators in
  the chain `artifact-contracts.yaml` declares (`validate-artifact.py`,
  `validate-brief.py`) — not a hand-authored fixture assuming the shape. A
  second test in the same file proves the block's absence changes nothing
  about validation of the pre-existing contract.
- `tests/test_brief_skeleton_extended_analysis.py` (9 tests) and
  `tests/test_validate_brief_extended_analysis.py` (7 tests) prove the
  skeleton/reconcile mechanics and the non-blocking validator behavior in
  isolation, including adversarial/malformed input never crashing or
  blocking.
- Real-runtime run against this repository itself (genuine analysis,
  `docs/candidate/real-runtime-run-2026-08-09/`): the real
  `build_skeleton()`/`reconcile()` sequence, validated through both real
  validators with zero blocking errors and zero `EXTENDED_ANALYSIS_*`
  warnings.
- The frozen-architecture stress-test round and its targeted reruns:
  `docs/candidate/stress-test-2026-08-10/` (`00-pre-registration.md`,
  `99-report.md`, `round2-results.md`, six case briefs + outputs, two rerun
  transcripts). The architecture files were verified byte-identical to the
  pre-registration reference throughout all six cases.
- The underlying *behavior* these fields carry (investigate-first, neutral
  clarification, evidence-resolved-vs-owner-authorized distinction) has
  real-use evidence from `prototype/repo-sensemaker-vnext` — see that
  branch's `docs/prototypes/real-use-experiment-2026-08-09/`, specifically
  the round 3b interaction-layer independence replication.

## 6. Missing evidence / experiment triggers

- The "model" step of the real-runtime run was performed directly rather
  than via a live, separate `ClaudeAgentSdkSkillExecutor`/SDK invocation
  (see that record's `00-context.md` for exactly what differs) — a live
  SDK-invoked run remains a further, not-yet-taken step if that distinction
  ever matters for a decision.
- Revisit this ADR if: a real runtime-invoked run produces a Section 15 a
  human finds actively misleading or unhelpful; any field needs to drive
  real routing; or the cross-section-consistency question (Section 6 vs
  Section 15) is forced by a real case.
- Incidental finding recorded during this work (unrelated to this ADR's
  scope, not fixed by this branch): `brief_skeleton.py`'s pre-existing
  generic flat-field splice stringifies a harvested Python `None` as literal
  text `None`, which parses back as the *string* `"None"`, not YAML `null` —
  see `docs/candidate/real-runtime-run-2026-08-09/02-findings.md`. Affects
  `MODEL_YAML_FIELDS` generally, predates this branch, orthogonal to
  Section 15.

## 7. Status rationale

ACCEPTED: the owner accepted the candidate architecture and the four
surviving fields as the working default design on 2026-08-10, after six
adversarial stress-test cases and three targeted reruns falsified one field
and narrowed two semantic ambiguities without demanding structural
expansion. Per the repository convention, "Accepted" records the operative
decision; the merge of the carrying branch to `main` is a separate
repository action, not part of this record's content.
