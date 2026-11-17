# Fresh-agent episode observation (2026-11-17)

**Status:** observation record for the independent later-agent question in Issues #859, #872 and #874. It is one subagent episode on one host. It is not qualification evidence, a matched comparison or proof of cognitive benefit.

**Source baseline:** `origin/main` at `cd285136` (PR #899 merge). The episode ran in a worktree cut from that commit.

## 1. Original conditions

- **Executor:** a general-purpose subagent with worktree isolation. It was not given a Sensemaking entrypoint, a lesson ID, a method or an expected conclusion.
- **Inherited ambient context:** the repository `CLAUDE.md`, the user's auto-memory index and the user-level Skills. Calibration C1 ([2026-11-15 record](2026-11-15-cognitive-method-learning-construction.md), section 2) showed these load into a fresh subagent on this host. The episode is therefore a fresh execution context under ordinary guidance, not a clean-room run.
- **Brief (paraphrased):** advance the repository's product purpose (ADR 0037) through the single most valuable warranted increment, or justify no change. Consider alternatives. Do not push, open a PR or merge. Do not add or run unit tests, as the construction policy requires.
- **Transcript:** persisted on the host as a subagent JSONL file. It contains 61 tool-use blocks, including plan-tool calls. The transcript is not committed. This record summarizes its tool calls in order.

## 2. Ordered observations

| Tool call | What the agent did | Observed result |
|---|---|---|
| #01-#09 | Read ADR 0037, the product strategy and the value-directed construction doc | Compass documents only |
| #10-#16 | Read `STATUS.md` sections | Current next step and dispositions |
| #17 | `git log`, `ls -t docs/normal-use`, `git show --stat` on the PR 899 lesson commit | Lesson-related files surfaced through ordinary exploration |
| #18 | `cat` of `docs/normal-use/2026-11-17-construction-vs-qualification-selection-lesson.md` and the goal-routes note | The lesson's source text was returned, and it refers to the Issue #860 owner amendment |
| #19 | Read a divergent-exploration doc that mentions the two-track amendment | Context only |
| #20 | `gh issue view` on Issues #860 and #859 with `--json title,body,state` | **Body only.** The 2026-11-15 owner amendment is held in an issue comment, which this call did not fetch |
| #21-#22 | Source and CLI layout exploration | Context only |
| #23-#24 | `semantic workspace-query --operation search --query-text "should I build a useful increment or wait for independent qualification evidence" --json`, unfiltered | 44 claims, about 82 KB. The first claim was `lesson:separate-construction-from-learning-qualification-gates` |
| #25-#29 | Parsed the saved output and noticed a cp1252 byte in the JSON file | A consumer-visible encoding defect |
| #30-#48 | Read the retrieval, store and CLI source; ran `product-outline`; grep checks | Confirmed the emitter and the callers |
| #49-#51 | Created `claude/semantic-cli-ascii-json` and edited `_emit` | One-function change |
| #60 | Committed `8f6b7fa6` | Decision note in the commit message |

The agent's final report rejected Issues #859, #872 and #874 as an "owner-gated qualification track, not a construction increment". That rejection appears only in the final report. The transcript contains no intermediate text that states it. The report was written after the work, so it is retrospective.

## 3. Claim levels

- **Pre-decision exposure to the lesson's source text: observed.** The text was returned in call #18, before the first Sensemaking query (#23) and before the final increment was chosen. The exposure came from ordinary repository exploration, not from a Steward RECALL step.
- **Applicability check of the lesson: not observed.** The lesson states a conditional rule: check construction and qualification gates separately before rejecting a behavioral capability. No intermediate text or tool call applies that check. The final rejection of #859, #872 and #874 is the pattern the lesson names. The owner amendment that answers that rejection is in the #860 comment, which the agent did not fetch.
- **Use of the lesson in the decision: not established.** The chosen increment emerged from a consumer failure found while parsing output. The query came after the lesson read, so the query is not an independent test of recall.
- **Useful engineering outcome: observed.** The agent found a real encoding defect in the semantic CLI's JSON output and made a one-function fix. That fix is PR #900, merged as `ffcec0e1`. Manual CLI observation, not a test, showed the before state as 84,268 bytes with a raw `0x97` byte and a UTF-8 decode failure. After the change the output was 84,278 bytes, ASCII-only, UTF-8-valid, with 44 claims identical to the before parse.
- **Self-report:** the agent reported that its reading of the lesson before its search means the episode is not clean independent evidence. This record agrees.

## 4. Interpretation (kept separate from the observations above)

- One episode cannot separate the possible causes of the gap. Candidates include the ambient guidance, the wording of the lesson, the body-only issue read and the agent's own weighting. None is established.
- The episode does show that a fresh agent can read a retained method lesson before a choice, and still make a categorical gate judgment that the lesson warns against.
- The episode also shows that a useful, verified consumer fix can come from an ordinary responsibility. That is separate from any cognitive-benefit claim.

## 5. Reconciliation of `lesson:separate-construction-from-learning-qualification-gates`

- **Revisit condition met:** the lesson's `revisit_when` names a real later choice in which the construction/qualification distinction is consequential. This episode is that choice.
- **Disposition: confirmed as consequential, not applied in this episode.** The lesson's text is unchanged. It is neither narrowed nor superseded. The PR 898 observation is kept as it was written.
- **Retained as:** a new `observation` claim and a `references` relation, both linked to this record. No new lesson is created.

## 6. Not established

- Independent cognitive benefit, a matched comparison, repeatability or transfer across tasks or domains.
- That the lesson changed the agent's choice, or would have changed it.
- Whether the pattern recurs. The Issues #872 and #874 qualification requirements stay open.

## 7. Follow-ups not built here

- **Bounded default for ranked lesson recall.** An unfiltered decision-time query returned 44 full records, about 82 KB. That is a context-cost question. It changes a default contract, so it needs its own decision.
- **Issue reads should include comments when the status is in comments.** This is a process note for agents. It is not a product change.
- **ASCII sweep across the campaign and strategy CLI modules,** about 47 stdout sites. It needs a separate reviewed change.

## 8. Addendum (2026-11-17, reconciliation)

Sections 1–7 are the original record and are unchanged. This addendum records a review of the record and one new consumer observation. It does not change any claim level in section 3.

**Review of the record.** The load-bearing factual statements were checked against the transcript and the source. The owner amendment is in the lesson source text (`docs/normal-use/2026-11-17-construction-vs-qualification-selection-lesson.md`, section 1, item 3). The issue read in call #20 was body-only JSON. The search in call #24 returned the lesson first. No factual or contract defect was found.

**New observation: the inline view of the search result.** The host stored the 82.3 KB search result and showed the agent a 2 KB preview. The preview contained the first claim's `attributes` (claim ceiling, method, scope and revisit condition, which name the construction/qualification distinction). It ended before that claim's `id` and `statement`. Stored claim payloads use canonical sorted-key JSON (`knowledge_store.py`, `sort_keys=True`), so `attributes` precede `statement` in every claim. The operative sentence of the rank-1 lesson was therefore not in the one search result the agent saw. The agent had read the lesson's source text in call #18, which states the rule, so this does not show the rule was unseen.

**Bounded-default decision.** The owner decided NO_CHANGE for the default size. This observation concerns field order and inline visibility, not result size, so that decision stands. Statement-first output, a changed canonical key order and a compact view each change a public output contract or the snapshot checksum. They are an owner question, not a repair.

**Issue reading.** `docs/agents/issue-tracker.md` documents `gh issue view <number> --comments`. The agent used a body-only JSON call and did not open that guidance. The documented access path is correct. No repository change is warranted.
