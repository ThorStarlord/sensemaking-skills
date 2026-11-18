# Collective reconciliation of methodological experience: #910 record (2026-11-18)

**Status:** record for [#910](https://github.com/ThorStarlord/sensemaking-skills/issues/910) under parent [#906](https://github.com/ThorStarlord/sensemaking-skills/issues/906). It makes distinct, authentic agent outcomes on a shared candidate visible as attributed evidence. It does **not** settle the candidate, promote a shared method or change any policy. Independent reuse and comparative benefit remain NOT QUALIFIED under [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872) and [#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874).

**Source boundary:** `origin/main` at `cf4fe15c`. Local unit and synthetic evidence tests were **NOT_RUN** under the construction-phase policy in CLAUDE.md. Checks run: a clean `semantic knowledge-build` of the committed revision, and downstream `knowledge-query` search and explain on the same index.

## 1. Baseline gap

Before this change, a downstream agent searching observations about the construction-gate lesson saw two episodes:

- `observation:pr898-construction-qualification-selection-20261117`, the rationale of the originating selection;
- `observation:fresh-agent-episode-20261117-construction-gate-exposure`, a fresh agent that rejected qualification-gated items categorically with no visible applicability check.

The 2026-11-18 episode that reported applying the two-gate check was recorded only in the #907 normal-use document. Downstream agents therefore could not see that counterevidence through the index. That is a narrow, demonstrated consumer gap.

## 2. Candidates and distinct outcomes

**Candidate A: `lesson:separate-construction-from-learning-qualification-gates`.** Three distinct, authentic outcomes:

| Episode | Task and actor | Observed outcome | Status in the index |
| --- | --- | --- | --- |
| PR #898 selection, 2026-11-17 | Originating responsibility selection; the agent that wrote the rationale | Grouped #859, #860 and #864 as qualification-gated; the rationale is broader than the owner's amendment | `observation:pr898-...-20261117` (existing) |
| Fresh subagent, 2026-11-17 | Responsibility selection; read the lesson first | Rejected qualification-gated items categorically; no visible applicability check; body-only issue read | `observation:fresh-agent-episode-20261117-...` (existing) |
| Fresh subagent, 2026-11-18 | Evidence-collection question; ran its own query and opened the source | Reported applying the two-gate check; recommended against deferring construction solely for qualification (self-reported) | `observation:construction-gate-application-20261118` (**added here**) |

**Candidate B: `lesson:console-guard-literal-print-arguments-only`.** One receiving-agent interpretation from #909 extends the lesson's sufficiency claim. There is no competing outcome, so there is nothing to reconcile. It stays as `observation:receiving-agent-console-output-20261118`, as recorded in [the #909 record](2026-11-18-receiving-agent-adaptation-909.md).

## 3. Reconciliation

**Candidate A.** The disagreement is about execution, not the rule's conditions. The lesson's scope is open-ended engineering responsibility selection under the two-track amendment in #860. The 2026-11-17 rejection is the pattern the lesson names, and it occurred without the check being visible. The 2026-11-18 application shows the check performed on a question of the same kind. Neither episode is a reason to change the lesson's conditions, and neither episode settles whether the lesson is generally right.

The episodes differ in task. The 2026-11-17 episode made its own selection; the 2026-11-18 episode answered an evidence question. The disagreement is therefore not a controlled contest.

**Disposition: leave the lesson unchanged.** Both observations stay attributed and bounded by their claim ceilings. The lesson's `revisit_when` condition, which names a real later choice where the distinction is consequential, is now met by two episodes that behaved differently. No consensus is forced.

**Candidate B.** A single extension with no contest: `NO_MODEL_CHANGE` on the lesson. The extension remains an attributed observation.

## 4. Authority boundaries preserved

- The lesson, the rule in CLAUDE.md and the guard test are unchanged.
- The new observation's `decision_changed` is "None". The 2026-11-18 recommendation caused no engineering action.
- Neither observation is shared policy. Visibility in the index does not make a candidate approved, and the lesson keeps `authority_verified: false`.
- No agent's learned state was rewritten.

## 5. Verification

- The reviewed knowledge file was extended by one observation claim and one `references` relation. The JSON diff is additive.
- `semantic knowledge-build` on the committed revision indexes the new claim.
- The same observation-kind search that returned two episodes before the change now returns the three observations (section 1). `knowledge-query --operation explain` on the lesson shows both `references` relations.

## 6. Limits

- All three episodes ran on this host under ambient repository guidance. The two 2026-11-17 and 2026-11-18 fresh agents are not independent of each other.
- The 2026-11-18 application is self-reported. The orchestrator did not verify the two-gate check beyond the opened sources.
- The episodes differ in task (section 3). Nothing here shows that either agent's method was better.
- No later real consequential decision has used any of these observations.

## 7. Remaining work

#910 is complete at construction level for this candidate: distinct outcomes are visible together, the disagreement is preserved, and the shared policy boundary holds. Two items remain. A genuinely independent later agent must make a consequential decision that uses the competing evidence. That is a qualification question under #872 and #874, not a construction gap.
