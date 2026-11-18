# Contextual historical learning assessment: #908 disposition (2026-11-18)

**Status:** source-grounded consumer disposition for [#908](https://github.com/ThorStarlord/sensemaking-skills/issues/908) under parent [#906](https://github.com/ThorStarlord/sensemaking-skills/issues/906). Disposition: **`NO_CODE_CHANGE`**. No proactive mechanism, notification default, scheduler, controller or schema is authorized or recommended. This record is **not** independent qualification evidence; independent later-agent behavior remains under [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872) and comparative benefit under [#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874).

**Source boundary:** `origin/main` at `4ef419a2` (merge of PR #911, the #907 disposition). Clean worktree cut from that commit. Local unit and synthetic evidence tests were **NOT_RUN** under the construction policy in CLAUDE.md. Checks run: real `semantic workspace-query --operation search` (lesson and observation kinds), source inspection of ADRs 0035 and 0036, the recall reference, the #908 issue body, and prior receipts and episode records.

## 1. Question

Is the current host-initiated recall path (`using-sensemaking`, SCL, RECALL and `context-for`, all invoked when the agent judges them warranted) adequate at a consequential engineering decision? Or does a specific missing, late, noisy or poorly applicable candidate warrant a separately decided contextual-assistance change?

## 2. Evidence distinguished

For each decision, the levels below are kept separate: relevant knowledge available; encountered before deciding; source and applicability verified; applied, adapted, rejected or ignored; resulting useful action; incremental cognitive benefit.

| Decision | Available | Encountered before deciding | Source / applicability verified | Applied, adapted or rejected | Useful action | Incremental benefit |
| --- | --- | --- | --- | --- | --- | --- |
| **D1.** PR #898 selected a graph correction over method-learning issues #859, #860 and #864 (2026-11-17) | Lesson `separate-construction-from-learning-qualification-gates` retained | Retrospective only. Not observable, so the original selection is not reconstructed | Not applicable (retrospective) | Not observable | Graph correction merged | **NOT QUALIFIED** |
| **D2.** Fresh subagent episode, 2026-11-17 (construction-gate decision) | Yes | **Yes.** The lesson source text was read at the start, and the search returned the lesson first | Source read; the applicability check was **not observed** | **Rejected categorically**, the pattern the lesson warns against. The #860 owner amendment, which answers the rejection, sat in an issue comment the agent did not fetch | Unrelated, reviewed encoding fix (PR #900) | **NOT QUALIFIED** |
| **D3.** Fresh subagent check, 2026-11-18 (see [#907 record](2026-11-18-shared-learning-candidate-907.md), section 3) | Yes | **Yes**, through its own query (rank 1) | Opened the authority file. Hash match reported | **Applied** the two-gate check (self-reported). Adapted for harness limits | Recommendation only; no engineering action | **NOT QUALIFIED** (shared ambient context; the question used the lesson's vocabulary) |
| **D4.** This disposition (#908), recorded below | Yes, though weakly (section 3) | **Yes.** The recall query ran after #908 and the recall reference had been read, and before this record was written | Governing ADRs read; no lesson addressed proactive assistance | Disposition reached from ADR and source authority, not from a lesson | This record | **NOT QUALIFIED** |

D2 and D3 are the only decisions with a retrieval-and-use trace. D2 shows the failure the lesson warns about; D3 shows the same retrieval giving a method-consistent recommendation. Neither is independent evidence of benefit, and both share ambient guidance with the host.

## 3. Forward observation: the decision in this record

Before writing this disposition, the host-initiated recall path was run with the question the decision actually turned on, using the zero-setup command:

```bash
PYTHONPATH=src python -m sensemaking_skills.cli semantic workspace-query \
  --operation search --query-text "proactive lesson assistance at consequential decisions versus host initiated recall" \
  --search-kind lesson --json
```

Results on `4ef419a2`:

- **Lesson kind:** three hits, all weak. `source-anchored-context-reentry` matched on "decisions"; `safe-mode-alone-does-not-confine-file-reads` on "lesson"; `console-guard-literal-print-arguments-only` on "host". None addresses proactive assistance.
- **Observation kind:** nine hits, again weak or topically off. Matches included "consequential" and "recall" (a strategic-funnel observation), "decisions" (several unrelated records) and "host" (a calibration record). The nearest relevant record was `observation:pr898-construction-qualification-selection-20261117`, which does not address proactive assistance.

Interpretation: the store has no retained lesson that answers this question. Lexical search correctly returned no strong match, but it still surfaced low-precision hits. That low precision is an input to the cost comparison in section 5, not a missed record. Absence is **NOT ASSESSED** outside the indexed lexical scope.

Source checks made before deciding: ADR 0035 item 4 (decision-time continuity is discovery from current task context, with use, adaptation or justified rejection before deciding), ADR 0035 item 7 (single controller), ADR 0036 item 2 (no second controller or scheduler), and the #908 governing boundaries (no generic observer, scheduler, second controller, mandatory interruption or automatic method switch).

## 4. Shortfall diagnosis

The acceptance categories are applied to what the record shows, not to what a proactive design would need.

| Category | Observed? | Evidence and status |
| --- | --- | --- |
| Retrieval or exposure | **Previously**, and fixed | Dropped `recorded_conditions` on `context-for` items (PR #882). Function words and the `lesson:` prefix led lexical ranking (#889, fixed by PR #890). The inline preview showed claim attributes before the statement (2026-11-17 addendum). The CLI now lists `id` and `statement` first (PR #905). No open retrieval defect was found on `4ef419a2`. |
| Applicability judgment | **Yes** | D2. The agent read and retrieved the lesson, then rejected the candidate categorically without the applicability check. More retrieval would not change this. |
| Method choice | Overlaps with applicability | D2's rejection is the method choice the lesson names. The remedy the record names is the lesson's own check, not a notification. |
| Lack of relevant history | **NOT ASSESSED** | Section 3's query found no lesson about proactive assistance. Lexical scope only. |
| Host or tool limitation | **Yes, three instances** | (a) `gh issue view --json body` omitted the #860 owner amendment held in a comment. `docs/agents/issue-tracker.md` documents `--comments`, and the agent did not consult it (D2). (b) Lexical `--query-text` is bounded to 1 to 24 distinct words of length 2 or more, within 300 characters. The bound is explicit, and D3's first longer query hit it. (c) The checkout at `9ae5338b` has a `CLAUDE.md` without the lesson trigger that `origin/main` carries (verified: the loaded text contains no lesson clause; `origin/main` contains one). This session's host instructions therefore lacked the trigger. |
| Adequate behavior with no defect | **Yes** for retrieval | D3 found the lesson from a relevant question without its ID, and the source it opened carried the stated limits. |

**Diagnosis:** no current retrieval defect explains the observed shortfalls. The shortfall that did matter was applicability judgment (D2). Host-side causes were an incomplete issue read and a stale local checkout, which is an operator issue and not a Sensemaking product gap. A proactive mechanism would not repair applicability judgment, and it would not repair a stale checkout.

## 5. Alternatives compared

| Option | Consumer value | Cost and risk | Evidence status |
| --- | --- | --- | --- |
| **A. Current host-initiated recall** (agent chooses `search` or `context-for` when warranted) | Timing stays with the agent. Each result shows its scope, claim ceiling and revisit condition. Cheap | Depends on the agent or loaded instructions triggering it. A stale checkout removed the trigger for this session | Observed working in D2 and D3. The trigger gap is fixed on `origin/main` |
| **B. Quiet availability** (lessons supplied or surfaced in context at each consequential decision) | Could raise exposure | Attention and anchoring. Lexical precision is low (section 3). Timing and false positives. Needs a runtime or hook, which ADR 0036 excludes for now | No evidence that exposure is the bottleneck. In D2 exposure already happened |
| **C. Nonbinding explicit presentation** (a suggestion at a decision point, which the host may ignore) | Makes candidates visible while the host keeps control | Needs a trigger that decides when to present, which is a second controller in practice. Adds overhead and false positives. #908 excludes it without separate authorization | Not demonstrated to be needed |

**Comparison:** A is sufficient for the decisions observed. B and C would add cost and risk against an unobserved benefit, and the one shortfall observed (applicability judgment) is not in their reach. Any new proactive mechanism needs separate owner authorization under #908.

## 6. Disposition

**`NO_CODE_CHANGE`.** The existing path is sufficient for the observed decisions. The shortfalls found were applicability judgment and host or operator conditions. None is a retrieval gap that a repository change would close. No narrow demonstrated consumer gap was found that would justify a code change.

Actions that remain outside this repository change:

1. **Local checkout staleness.** The local `main` checkout at `9ae5338b` is 105 commits behind `origin/main`. Its `CLAUDE.md` lacks the lesson trigger that current `origin/main` carries. Updating the checkout is an operator action.
2. **Issue-reading guidance.** `docs/agents/issue-tracker.md` already names `--comments`. Whether agents follow it is a host and agent behavior question, not a code change.

## 7. Claim levels

| Level | Status |
| --- | --- |
| Current recall path retrieves a relevant retained lesson from a question without its ID | Observed (D3, #907 record) |
| Retrieved lesson is source-checked before a decision | Observed (D2 source read; D3 authority file opened) |
| Retrieved lesson is applied by an independent later agent in a genuine consequential decision | **NOT QUALIFIED** (#872) |
| Host-initiated recall is adequate at consequential decisions | Observed for the decisions above only; **NOT ASSESSED** more broadly |
| Proactive assistance would improve decisions | **NOT ASSESSED**; no evidence supports it |
| Comparative or cognitive benefit of any option | **NOT QUALIFIED** (#874) |

## 8. Limits

- Only a small number of decisions was examined, on one host, mostly by same-context or same-harness agents. None is independent qualification evidence.
- D3 used the lesson's own vocabulary. It tests retrieval from a relevant question, not blind discovery.
- Lexical search is ranked word overlap. Low-precision hits are visible in section 3. Absence in the index is not absence of history.
- This record does not reconstruct the original private reasoning of any agent.
