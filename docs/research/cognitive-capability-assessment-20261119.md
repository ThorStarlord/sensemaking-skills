# Cognitive capability assessment (2026-11-19)

**Status:** research assessment under ADR 0037's integrated cognitive-development purpose. It is non-authoritative. It changes no ADR, Skill, policy, shared method, product thesis or qualification record, and it is not independent evidence of agent behavior or cognitive benefit.
**Source baseline:** `origin/main` at `0c6a1cf8` (PR #923 merge). Inspected in a clean worktree cut from that commit.
**Currentness correction (2026-11-19):** L5, O1 and the owner question in section 6 were rechecked against `origin/main` at `853ae740`. PR #905 had already changed search presentation. The NO_CODE_CHANGE disposition and the #872 and #874 boundaries are unchanged.
**Verification:** source and record inspection, and one lesson search through the real CLI. Unit and synthetic evidence tests were NOT_RUN under the construction policy in CLAUDE.md.
**Relation to existing records:** this document does not restate [#906](https://github.com/ThorStarlord/sensemaking-skills/issues/906), [#917](https://github.com/ThorStarlord/sensemaking-skills/issues/917), the evolutionary-hybrid section in [capability-learning-loop-v0.md](capability-learning-loop-v0.md) (section 16), the opportunity landscape in [cognitive-construction-opportunity-landscape](../explorations/2026-11-17-cognitive-construction-opportunity-landscape.md), or the decision records for [#907](../normal-use/2026-11-18-shared-learning-candidate-907.md) and [#908](../normal-use/2026-11-18-contextual-recall-assessment-908.md). It uses them as sources.

## 1. Decision-changing question

Which genuine agent limitation currently costs the most product value, and does an existing AMS/SCL/RECALL capability already address it? The answer decides whether the next responsibility is construction, observation or neither.

## 2. Existing capabilities (what the repository implements)

| Capability (owner's list, plus extensions) | Implemented as | Behavioral evidence so far | Status |
| --- | --- | --- | --- |
| Purpose and authority orientation | ADR 0037, product strategy, `STATUS.md`, read-only `product-outline` | A fresh subagent read these before choosing work (D2, calls 1-16) | Availability and use of sources observed. Choice quality not assessed |
| Retained experience (SCL) | Reviewed lessons (12), observations (27) and incidents (4) in `.sensemaking/knowledge/*.json`, each with source references | Written with source attribution and explicit claim ceilings | Implemented |
| Decision-time retrieval | `search` (lesson kind), `context-for`, `recall_conditions`, `citing_records` (PRs #919, #921, #922) | A relevant question returned the construction-gate lesson first in a fresh subagent (D3) and in this session | Retrieval observed working. Preview order was addressed by PR #905 (section 3, L5) |
| Applicability judgment | Metareasoning policy section 5a; RECALL step 4 ("verify applicability at current SHA") | Mixed: not applied in D2; applied (self-reported) in D3 (section 3, L2) | Guidance exists. Reliable use not established |
| Method choice (ACT, INQUIRE, CHALLENGE, EXPLORE, VERIFY, ESCALATE, STOP) | Guidance only, by design (ADR 0036 sections 2 and 8) | The one authentic-use observation has an insufficient trace (2026-11-08 record) | Not established |
| Feedback without reinforcing mistaken conclusions | Incident -> lesson records with conditional scope (PR #838 incident; PR #909 receiving-agent extension) | Records keep scope limits and avoid overgeneralizing. Authored by the same lineage, so not independent | Careful authored interpretation observed. Behavioral effect not established |
| Carrying adaptations into later work | Learning candidates and reconciliation (#907-#910) | No later application of a retained method lesson in authentic work was observed. The merge-base lesson was retrieved, but no later decision it could change occurred (E1), and one encounter came after the decision (E2) | Not established |
| Metacognitive calibration | Claim levels and NOT QUALIFIED labels in records | Strong in documentation. Effect on behavior not measured | Documentary calibration observed |
| Question fitness and reframing | AMS section 5a; PR #825 selection case | Partial. No authentic in-task reframing trace | Not established |
| Adaptive reflection effort | AMS proportionality rule (no quota, no mandatory reflection) | No authentic trace of reflection cost or benefit | Consistent with policy; not established as a capability |
| Methodological creativity | Divergent exploration (11-17 landscape) | Produced possibilities, not behavior | Not established |

Summary: retention, retrieval and documentary calibration are implemented and observed. Applicability judgment, method choice, carry-forward and reframing are guidance or records without behavioral confirmation.

## 3. Observed limitations and their evidence

Each limitation is dated to the source revision where it was observed. It is a current limitation only if the present consumer or behavior still shows it.

**L1. A retained, read lesson did not prevent a categorical gate rejection.** In PR #898 (2026-11-17), an agent grouped Issues #859, #860 and #864 as gated on qualification and dismissed them as not an immediately available construction responsibility (record: [construction-vs-qualification lesson](../normal-use/2026-11-17-construction-vs-qualification-selection-lesson.md), section "What the source actually shows", item 2). Later the same day, a fresh subagent (D2) read the lesson source before its first query, and the lesson ranked first in its search. It then rejected #859, #872 and #874 as "owner-gated qualification track, not a construction increment". No applicability check of the lesson's conditional rule is visible in its transcript ([fresh-agent observation](../normal-use/2026-11-17-fresh-agent-episode-observation.md), sections 2 and 3). The rejection repeats the pattern that the lesson names. This concerns the recorded premise, not the outcome. PR #898's graph correction was a useful coverage change, and the lesson itself says the graph repair may still have been the best choice. The record does not show that the selected responsibility was inferior.

**L2. The same information produced different applicability behavior.** D2 and D3 ([907 record](../normal-use/2026-11-18-shared-learning-candidate-907.md), section 3) both read the lesson source, which quotes the Issue #860 owner amendment. Neither fetched the issue comments, and D2 read the issue body only. D3 reported applying the two-gate check (self-reported) and adapting its recommendation for harness limits. D2 did not show the check. The difference is not explained by access to the amendment text. D2 was a selection among several candidates; D3 was a single-item evidence question. Those task framings differ, so the pair is not a controlled comparison. It shows only that the same access produced different observed behavior under different framings. With two instances, one self-reported, it is not a rate.

**L3. Carry-forward is not demonstrated.** A merge-base scope lesson from PR #838 was retrieved in the 2026-11-15 construction episode (E1), but that decision was not one the lesson could change, so the disposition was NO_MODEL_CHANGE. A second encounter (E2) came after the code choice. Neither shows a retained method changing a later choice.

**L4. Method-choice content is thin.** Of 12 reviewed lessons, four mention method. None is a method-selection rule for the ACT-to-STOP choice itself. E1 found no method-choice precedent for its question, so the substrate cannot supply method content until authentic episodes produce it.

**L5. Presentation hid the operative sentence at an earlier revision (historical; addressed).** At the revision of the 2026-11-17 fresh-agent episode, search JSON sorted keys, so each claim's `attributes` preceded its `statement`. A 2 KB preview of an 82 KB unfiltered result showed the attributes but cut off the statement ([fresh-agent observation](../normal-use/2026-11-17-fresh-agent-episode-observation.md), section 8). That observation is kept as written. The rule text had already been read before the search (call #18), so presentation did not cause the D2 rejection, and PR #905 does not change what that agent saw. [PR #905](https://github.com/ThorStarlord/sensemaking-skills/pull/905) (`55059e3f`, merged 2026-11-17) changed the search emitter so that each claim leads with `id` and `statement`. Stored records and snapshot digests are unchanged. At `origin/main` `853ae740`, the same query text restricted to lesson results put the top lesson's `id` at byte 419, and its `statement` ended at about byte 1047, inside the first 2 KB. L5 is therefore no longer a current defect of the search consumer. It remains as evidence that a preview can hide the operative sentence.

Not limitations, on the evidence: retrieval recall for a relevant question (observed working); the body-only issue read (process guidance already names `--comments`); and the stale operator checkout (an operator condition, recorded in [#908](../normal-use/2026-11-18-contextual-recall-assessment-908.md)).

## 4. Competing explanations for L1 and L2

- **E-a: candidate-set framing.** Gate dismissal occurs when the agent chooses among several candidates and one is gated. A single go/no-go check (D3) is more likely to get the check. Consistent with both L1 instances, which were selections among candidates, and with D3 being a single-item check. Not tested; the instances differ in other ways too.
- **E-b: ambient framing.** Repository and user guidance keep qualification salient. STATUS.md's Q-2 disposition describes independent qualification as the gate for comparative claims in detail, and CLAUDE.md's construction-policy text is framed around construction against evidence. The full text of the Issue #860 two-track amendment is in an issue comment and quoted in the lesson's authority document. Predicts variation across hosts or guidance versions. Not tested.
- **E-c: self-weighting and anchoring.** A selection can reuse an earlier premise (for example "gated, therefore not feasible"), which D1 and D2 both show. Untestable without a time-ordered trace.
- **E-d: exposure order.** The preview-order defect (L5) was real at its revision and PR #905 has addressed it. It cannot be the sole cause of D2, because the rule was read before the decision through another path.
- **E-e: issue-read path.** Disconfirmed as the sole cause, because the amendment text was also in the lesson's source. It remains a real incomplete-evidence hazard for other questions.
- **Chance.** Two instances are too few to rule out.

## 5. Opportunities (qualitative comparison, no scores)

| Opportunity | Value if it works | Evidence | Feasibility and reversibility | Verdict |
| --- | --- | --- | --- | --- |
| O1. Statement-first presentation of search claims | Already implemented by PR #905 (`55059e3f`), so not a current opportunity | L5 (historical), rechecked at `853ae740` | None needed | Done. Do not re-implement |
| O2. Comparative consumer for a choice among candidates (A4 in the landscape) | Unknown. Could expose gated alternatives' beneficiary effects | L1 pattern | Moderate cost. Risk of post-hoc argument formatting. Lesson already gives the comparison instruction, and that was not followed | Not warranted yet. Would add a surface without evidence it changes choice |
| O3. Decision-note discipline for lesson checks | Could make later checks observable for qualification | Existing policy already requires a decision note | No new mechanism. It uses the existing PR decision note | Use in ordinary work (section 6). Not a new procedure |
| O4. Method-choice precedent (new lessons) | High in principle | L4 | Only authentic episodes can supply it. Synthetic lessons are excluded | Blocked on authentic episodes |
| O5. Changes to #872 or #874 qualification | Required for comparative claims | C1 calibration found the fresh-subagent harness NOT_ADMISSIBLE for a matched comparison | Protected qualification track | Keep separate, unchanged |
| O6. Currentness pointers for lesson amendments | Low. The lesson already quotes the amendment | D2 and D3 both had the text | Trivial | No change |

## 6. Strongest warranted next responsibility

**No product code change now (NO_CODE_CHANGE).** No current limitation has a repository-side defect that a bounded change would plausibly fix. L5 is no longer a current defect. O2 has no evidence that a tool would change choice. O4 needs authentic episodes.

**Next responsibility: observe, do not build.** In the next ordinary, consequential selection among candidates where a retained construction or qualification lesson is retrieved, state in the existing PR decision note: which lesson was retrieved, whether its check was run, and what the check found. This is the cheapest observation that separates E-a from E-b without a new procedure, a manufactured episode or a synthetic test. It is not a claim of benefit.

**Presentation:** statement-first search output already exists (PR #905). No owner authorization is pending for it, and this assessment recommends no change to it.

## 7. What would change these conclusions

- An authentic selection among candidates performs the check and records a changed decision. L1 is then weak, and the next limitation is throughput or breadth.
- Further authentic selections dismiss gated candidates categorically, with the check visible or not performed. E-a gains support, and O2 becomes worth a proposal, with a pre-stated consequence test and no scalar score.
- A host without the ambient construction text behaves differently in an equivalent selection. E-b gains support, and the wording of shared guidance becomes an owner-gated change.
- Evidence that the current search output hides an operative statement in an authentic consequential decision would reopen L5 as a current defect.
- An authentic later agent applies a retained method lesson in a consequential decision it could otherwise have missed. That is the first piece of carry-forward evidence (L3), still not a comparison.

## 8. Limits

- One retrospective selection (D1, PR #898), one fresh-subagent selection (D2) and one fresh-subagent check (D3), all on one host. D2 and D3 inherit ambient guidance, so neither is independent (C1 calibration; [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872)).
- D3's application is self-reported. Retrospective PR rationales do not show the original reasoning.
- D2 and D3 differ in task framing (a selection among candidates versus a single-item check). They are observations under different framings, not an independently controlled comparison.
- The recorded premise in PR #898 was overbroad. That does not show the responsibility it selected was an inferior choice.
- This assessment's own selection was made after reading the construction lesson and the D2 and D3 records, and after a search that ranked the same lesson first. It is therefore not an independent decision and is not evidence of benefit.
- Nothing here establishes a causal effect of AMS, SCL or RECALL, a comparative advantage over a capable direct agent, or transfer across domains ([#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874)).
