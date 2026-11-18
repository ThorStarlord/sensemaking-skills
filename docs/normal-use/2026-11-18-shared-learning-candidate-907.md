# Shared learning candidate discovery: #907 disposition (2026-11-18)

**Status:** source-grounded construction disposition for [#907](https://github.com/ThorStarlord/sensemaking-skills/issues/907) under parent [#906](https://github.com/ThorStarlord/sensemaking-skills/issues/906). Disposition: **`NO_CODE_CHANGE`**. This record adds no runtime, query, schema, lesson or policy. It is **not** independent later-agent reuse, predecision use, improved decision quality or comparative benefit; those remain under [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872) and [#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874).

**Source boundary:** `origin/main` at `55059e3f` (merge of PR #905). Working tree was a clean worktree cut from that commit. Local unit and synthetic evidence tests were **NOT_RUN** under the current construction policy in CLAUDE.md. Checks run: real `semantic knowledge-build`, real `semantic knowledge-query --operation search`, real `semantic workspace-query --operation search`, and source/diff inspection.

## 1. Originating experience (traced)

| Element | Source |
| --- | --- |
| Experience (observation) | PR #898 (merged 2026-11-17, `04:21:06Z`) selected a goal-graph correction over method-learning issues #859, #860 and #864, which it grouped as "gated on instrument and qualification work". Its receipt is `.sensemaking/receipts/2026-11-17-cognitive-selection-consumer.session.yaml`. |
| Interpretation (candidate) | `lesson:separate-construction-from-learning-qualification-gates` in `.sensemaking/knowledge/stewardship.json`, citing `docs/normal-use/2026-11-17-construction-vs-qualification-selection-lesson.md` (source captured at commit `12e07a83`). It is a conditional method caution, not a rule. |
| Attributable authority | Issue #860's 2026-11-15 owner amendment comment separates a construction track (may advance without independent qualification) from a qualification track (#872, #873, #874). The issue body alone does not contain this amendment. |
| Context | Open-ended engineering responsibility selection under the two-track amendment. |
| Limits | The lesson's own `claim_ceiling` says it is "not proof of an inferior choice, improved cognitive behavior, independent application, transferable learning or comparative advantage". The original private reasoning of the PR #898 agent is not reconstructed. |
| Uncertainty | One recorded selection. Whether the alternative was feasible at the time is not established. |

## 2. Discovery path (existing consumer)

The highest existing agent-facing path is zero-setup lexical search over reviewed lesson claims:

```bash
PYTHONPATH=src python -m sensemaking_skills.cli semantic workspace-query \
  --operation search --query-text "<question>" --search-kind lesson --json
```

Checks performed on `55059e3f`:

- **Same-context check (this session).** Query: "Does an independent later-agent qualification gate block useful SCL construction work". The candidate returned first. `matched_tokens` were `independent`, `later`, `agent`, `qualification`, `gate`, `useful`, `scl`, `construction`. A second wording, "should a new learning feature wait for independent qualification before construction", also returned it first. The candidate was returned without its ID being supplied. This check does not count as independent, because the author of this record had already read the lesson text.
- **Fresh-context check.** A general-purpose subagent with no access to this conversation was given an evidence-collection question and asked to search for records itself. Its result is recorded in section 3.
- **Consumer inspection.** Each returned claim includes `authority_ref`, `evidence_refs`, `epistemic_status` and `attributes` (scope, `claim_ceiling`, `revisit_when`). Each claim's attributes state `authority_verified: false`, and the response states `action_authorized: false`. This keeps agent-local origin, shared candidate and reviewed policy distinct. A lesson is a `lesson` claim, not a `rule` or policy claim, so source visibility does not promote it into mandatory shared doctrine.

The contribution path from an agent's own work already exists. A discovery is retained as an `observation` or `lesson` claim in `.sensemaking/knowledge/*.json`, or in a bounded normal-use record, and becomes shared through the ordinary reviewed Git change. No new learning log, query API, controller or schema is needed. The 2026-11-17 episode retained its own finding as an `observation` claim in the same way.

## 3. Fresh-context receiving-agent check

One general-purpose subagent received an evidence-collection question: whether a planned SCL/AMS construction item should wait for independent later-agent qualification. It was not given the lesson ID, the candidate's text, a method or an expected conclusion, and it formed its own queries. It inherits the repository CLAUDE.md, the user's memory index and the user-level Skill list ([`lesson:subagent-inherits-ambient-context`](../../.sensemaking/knowledge/stewardship.json)), so this is a fresh execution context, **not** an isolated comparison arm.

- **Question vocabulary.** The question used the lesson's own terms ("independent", "qualification", "construction"). The check therefore tests retrieval from a relevant question, **not** blind discovery.
- **Retrieval.** The subagent's first, longer query was rejected by the code's input bound: `knowledge_retrieval.py` accepts 1 to 24 distinct words of length 2 or more, within 300 characters. A shorter query, `search --query-text "independent later-agent qualification construction sequencing" --search-kind lesson`, returned `lesson:separate-construction-from-learning-qualification-gates` first, without its ID.
- **Source check.** The subagent opened the lesson's authority file and the 2026-11-17 fresh-agent observation. It reported that their recorded source hashes matched.
- **Use (self-reported, not verified).** The subagent reported applying the two-gate check, rejecting any reading that PR #898 was wrong or that the lesson proves benefit, and adapting its recommendation for the harness limits in a calibration lesson. It also reported that the retrieved lesson shaped its recommendation. That report is not independent evidence of benefit.
- **Not assessed.** The subagent did not fetch Issue #860's comments and relied on repository descriptions. The owner amendment is also quoted in the lesson's own source (section 1), so the gap lies in the agent's reading, not in retrieval.

Evidence level for this check: fresh-context retrieval **observed** from a relevant question; source check **observed**; application **self-reported**; independent predecision use **NOT QUALIFIED** (see #872).

## 4. Disposition

`NO_CODE_CHANGE`. The shared-candidate path works for the two acceptance conditions that do not require later-agent behavior:

1. A retained originating interpretation is discoverable from a question that does not contain its ID.
2. The receiving consumer can inspect the original source, its claim ceiling and its revisit condition.

No defect in this path was found on `55059e3f`. The earlier defects it had were fixed before this check: lexical ranking of function words and kind prefixes (#889, fixed by PR #890), and dropped `recorded_conditions` on `context-for` history items (fixed by PR #882).

## 5. Evidence levels

| Level | Status |
| --- | --- |
| Originating experience and source traced | Observed (repository source and receipt) |
| Retained interpretation exists as a reviewed claim | Observed (`lesson:separate-construction-from-learning-qualification-gates`) |
| Discoverable from a question without its ID | Observed (same-context and fresh-context checks above) |
| Receiving consumer inspects source and limits | Observed (output fields and original authority file) |
| Agent-local origin, shared candidate and policy kept distinct | Observed in output fields; no change needed |
| Independent predecision encounter by a later agent | **NOT QUALIFIED** (see #872) |
| Source-verified application or rejection in a real decision | **NOT QUALIFIED** (see #872) |
| Outcome or comparative benefit | **NOT QUALIFIED** (see #874) |

## 6. Remaining work

Nothing in #907's construction scope remains. #909 depends on this disposition and becomes ready for an agent after this record merges. Its qualification remains with #872 and #874.
