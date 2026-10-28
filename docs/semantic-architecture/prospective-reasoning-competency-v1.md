# Prospective Reasoning Competency Check v1

**Status:** vocabulary-fit assessment for [`prospective-reasoning-ontology.md`](prospective-reasoning-ontology.md) (plan PR B). Predictions at `main@b6cf509`; plan PR C tests the knowledge column by encoding the reference case.  
**Reference case:** [`../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md`](../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md)  
**Vocabulary tested:** `src/sensemaking_skills/semantic_architecture/knowledge.py` (18 v1 claim kinds, 16 v1 predicates, v2 additions), the `strategic_repository_analysis` v2 contract, and existing Skill guidance.  
**Purpose:** find which distinctions need executable formalization before building any, without delaying construction for an exhaustive assessment.

## Verdict scale

Same scale as the [architecture competency check](architecture-ontology-competency-v1.md):

- **expressible:** an existing kind, predicate, artifact field or guidance carries the meaning.
- **awkward:** the meaning fits only in prose or unchecked `attributes`; it is retrievable but not typed.
- **not expressible:** nothing carries the meaning.

A **masquerade risk** is flagged where the nearest existing construct asserts something stronger than the prospective meaning (for example an observed change for a proposed one).

## Assessment

| CQ | Decision it supports | Closest representation at `b6cf509` | Verdict | Loss | Resolution candidate |
| --- | --- | --- | --- | --- | --- |
| CQ-089 activity vs entity | Whether a record describes what was done or what exists | Artifacts record activities (strategic analysis, query receipt); claims record entities | awkward | Which operation or orientation produced or changed an entity is not recorded | A provenance field in analysis artifacts when a consumer needs it; no knowledge change |
| CQ-090 possibility motivating an option | Whether an option still serves an open possibility | `alternative` claim `references` the `poss:` claim with `conceptual_relation: proposesToRealize` | awkward | Meaning only in an attribute | `target_possibility_refs` in `architectural_synthesis` (plan PR D) |
| CQ-091 proposed changes to components, contracts, boundaries | Impact and authority of a proposal before building it | `references` with an attribute; `affected_by_change` exists but asserts an observed change | awkward, masquerade risk | Nothing typed separates "would change" from "was changed" | Candidate prospective-change predicate (plan PR I) if encoding confirms the risk |
| CQ-092 structural differences and reuse | Which option reuses more and changes less | Option prose; `requires_capability` for reused capabilities | awkward | Target structure is prose | Option fields in `architectural_synthesis` |
| CQ-093 path's future state and transitions | Where a path leads and through which steps | Strategic path `future_state` and `path_transitions` | expressible | None in the artifact; paths are not knowledge records, by design | None |
| CQ-094 consequences of a preferred option | What choosing it would set in motion | Strategic `unlocks` and `risks` (unidentified prose); `hypothesis` claims with `references` | awkward | No identity or per-consequence assumptions in the artifact | `conseq:` hypothesis records (plan PR C); a consequence section (plan PR F) |
| CQ-095 consequences resting on assumptions vs observed effects | How much to trust a predicted benefit or risk | `hypothesis` (`hypothetical`) vs `observation` (`observed`) claims; shared premises as `hypothesis` nodes | expressible | None | None |
| CQ-096 consequence that produced a new possibility | Provenance of a new idea | `opportunity` claim `derived_from` a `hypothesis` claim | expressible | None | None |
| CQ-097 consequence that could change the comparison | Whether to reopen a preference | Attribute on the consequence; prose in the analysis | awkward | No typed link from a consequence to the judgment it affects | A feedback field in the synthesis (plan PR D or PR F) |
| CQ-098 why preferred, selected, deferred or rejected, and by whom | Whether a direction is settled and under what authority | Possibility `disposition_history`; `decision` claims with `decided_by`; no form for a provisional preference other than a `decision` | awkward, masquerade risk | A preference encoded as `decision` would read as settled | `provisional_preference` with status in `architectural_synthesis`; never a `decision` claim |
| CQ-099 reconstruct without conversation | Continuity across sessions | This reference case (prose) and future records | awkward | Prose only until records and a contract exist | Plan PR C (records) and PR D (artifact) |
| CQ-100 restated, revised, new or already rejected | Avoid rediscovery and silent reactivation | Funnel section 4 guidance (since PR #627); disposition history; library | expressible | None | None |
| CQ-101 stop deeper exploration | Spend depth only where it can change the decision | Consequence Depth v0 stop rule (section 5) | expressible | None | None; the synthesis may record its stop reason |
| CQ-102 ordinary work without full analysis | Keep the loop conditional | `using-sensemaking` direct bounded work; Consequence Depth v0 section 1 | expressible | None | None; preserve it |

## Tally and gate

- **expressible:** 6 (CQ-093, CQ-095, CQ-096, CQ-100, CQ-101, CQ-102)
- **awkward:** 8 (CQ-089, CQ-090, CQ-091, CQ-092, CQ-094, CQ-097, CQ-098, CQ-099), two with masquerade risk (CQ-091, CQ-098)
- **not expressible:** 0

**What this warrants:**

1. **An `architectural_synthesis` artifact contract (plan PR D).** It resolves CQ-090, CQ-092, CQ-097, CQ-098 and CQ-099 at the analysis level without touching the knowledge schema. Its decisive job is CQ-098: a provisional preference needs a home that cannot be read as a decision.
2. **Reviewed records with existing kinds (plan PR C).** These test the predicted encodings for CQ-090, CQ-094 and CQ-096, and whether the CQ-091 masquerade risk is real in practice.
3. **No new knowledge kind or predicate yet.** The one candidate is a prospective-change predicate for CQ-091 (plan PR I), only if PR C shows that `references` plus an attribute loses the distinction.

**Not warranted now:** a standalone consequence artifact. Consequence Depth v0 section 6 warns against one without independent reuse, and the reference case's consequences fit inside its synthesis.

## Results after encoding (plan PR C)

The reference case is encoded in `.sensemaking/knowledge/prospective-reasoning.json` (schema version 1; 15 claims, 29 relations), plus `poss:repository-local-prospective-decision-memory` in `possibilities.json`. It was indexed at `2ecf261`. Queries are recorded in `.sensemaking/receipts/2026-10-28-prospective-reasoning-ontology.query.yaml`.

| CQ | What retrieval returned | Verdict after encoding |
| --- | --- | --- |
| CQ-090 | `explain` on the possibility returns all four options, each by a `references` edge with `conceptual_relation: proposesToRealize` | awkward, as predicted; retrievable, meaning in an attribute |
| CQ-091 | `explain contract:receipt-schema` returns option B's proposed change as a `hypothetical` `references` edge, never `affected_by_change` | awkward, **no masquerade** when the convention is followed; no new predicate warranted |
| CQ-092 | `explain` on option A returns its reused capabilities (`requires_capability`) and three alternatives; target structure is an attribute | awkward, as predicted |
| CQ-094 | `explain` on option A returns its six consequences | awkward (`mayProduce` as an attribute); complete |
| CQ-095 | `explain` on the write-authority consequence separates two `observed` premises from the `hypothetical` assumption it challenges | expressible, confirmed |
| CQ-096 | `explain` on the derived possibility returns `derived_from` its consequence | expressible, confirmed |
| CQ-097 | The consequence carries `decision_changing` and `feedback_outcome: REVISE_PREFERENCE` as attributes | awkward, as predicted |
| CQ-098 | `why` on an option is refused ("requires a decision claim"); the preference, its scope and history come back through `explain` attributes | awkward; the refusal is correct, because a preference must not read as a decision |
| CQ-099 | `history` traces the possibility across 6 indexed revisions; `changes` separates the 16 added records from the 1 re-authored possibility | expressible with records and the analysis record together |
| CQ-100 | Option C is linked `derived_from` the earlier declined possibility, recording that it restates that premise | expressible, confirmed |

**Conclusion:** no competency question lost an answer, and neither masquerade risk materialized under the encoding convention. Plan PR I (new kinds or predicates) stays unwarranted. The remaining gaps (CQ-092, CQ-097, CQ-098 structure) belong in an analysis artifact, which plan PR D provides.

## Results after the artifact contract (plan PR D)

The reference case conforms to the `architectural_synthesis` contract and passes `scripts/validate-output.py architectural_synthesis` (generic and focused validators).

| CQ | Field that now carries it | Mechanical check |
| --- | --- | --- |
| CQ-090 | `target_possibility_refs` | `poss:` ids |
| CQ-092 | each option's `proposed_structure`, `reuses_refs`, `proposed_transitions` (`target_ref`, `change`) | at least two options; transitions name what would change |
| CQ-097 | `preference_feedback` (`consequence_ref`, `outcome`, `effect`) | the consequence must be cited by an option; outcome from the ontology's feedback list |
| CQ-098 | `provisional_preference` (`status: PROVISIONAL`, attribution, rationale, scope) or `null` with `no_preference_reason`; each option's `comparison_outcome` and `comparison_reason` | any other status is rejected; exactly the preferred option is `PROVISIONALLY_PREFERRED` |
| CQ-099 | the whole artifact, with `target_source_identity` and `analysis_ref` | authorization and truth flags must be `false` |

The checks are structural. They cannot tell whether options are materially different, a comparison is sound or a preference is warranted; that stays agent judgment, open to review.

## Encoding predictions for plan PR C

| Concept | Predicted encoding | Reason |
| --- | --- | --- |
| ArchitectureOption | `alternative` claim, `arch:` id, `attributes.concept: ArchitectureOption`, `hypothetical` | `alternative` means a competing means; the option is unchosen and prospective |
| ConsequenceHypothesis | `hypothesis` claim, `conseq:` id, category and assumptions in attributes | Conditional predicted effect |
| `proposesToRealize`, `mayProduce`, `mayEnable`, `alternativeTo` | `references` plus `attributes.conceptual_relation` | No matching predicate; must not be `implemented_by` or `depends_on` |
| new possibility from a consequence | `opportunity` `derived_from` the `conseq:` claim | `derived_from` matches |
| reused existing capability | option `requires_capability` the capability | A genuine prerequisite |
| proposed change to an existing contract | `references` plus `conceptual_relation: proposesChangeTo`, never `affected_by_change` | Avoid the CQ-091 masquerade |
| provisional preference | attributes on the analysis reference and the option's disposition history (`PROVISIONAL`), never a `decision` claim | Avoid the CQ-098 masquerade |
| strategic paths | not encoded; cited as `<analysis ref>#PATH-n` in attributes | Paths live in their analyses |
