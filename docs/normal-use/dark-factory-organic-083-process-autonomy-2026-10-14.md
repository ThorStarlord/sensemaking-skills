# Normal-use observation — Dark Factory Organic #83, Attempt 15

**Date:** 2026-10-14  
**Status:** real-repository episode / bounded autonomy and delegation evidence; not a benchmark or general full-autonomy proof  
**Systems:** [Dark Factory](https://github.com/ThorStarlord/dark-factory) carrying out a real [Metamorfose-Edutech](https://github.com/ThorStarlord/metamorfose-edutech) feature  
**Companion process postmortem:** [Dark Factory documentation PR #142](https://github.com/ThorStarlord/dark-factory/pull/142)  
**Trackers:** [Organic workload #83](https://github.com/ThorStarlord/dark-factory/issues/83) and [provider investigation #137](https://github.com/ThorStarlord/dark-factory/issues/137)

**Evidence provenance:** GitHub establishes published PRs, their heads, and tracker discussion. The live Windows Campaign journal, local OpenCode sessions, HALT marker and canonical verifier results were inspected and reported by the coding agent; this document did **not** independently inspect those local stores. The exact installed/harness-loaded Sensemaking Skill revision was not captured. Observed behavior cannot be causally attributed to the current Sensemaking guidance.

## 1. Why this qualifies as a normal-use episode

This was ordinary engineering in a real repository, not a synthetic research fixture. Several consequential decisions had plausible alternatives: discard or recover delivered work after an executor failure; continue A2 on the exact successor candidate or rebuild; retry a failed semantic judge or diagnose; preserve a frozen Campaign while independently warranted repository work continues; and stop at a protected integration boundary.

The question relevant to Sensemaking is **whether full delegation preserves the product objective, evidence, resource economy and authority when one external execution seam fails**. It does not require reopening repository-wide strategic analysis or testing every Strategic Exploration Funnel dimension.

## 2. Reported results and boundaries

| Boundary | Observation | Claim ceiling |
| --- | --- | --- |
| Implementation | Metamorfose draft [PR #118](https://github.com/ThorStarlord/metamorfose-edutech/pull/118), then successor [PR #119](https://github.com/ThorStarlord/metamorfose-edutech/pull/119) at **6ec73333cb0a872113573d5dcb423f647e4fa0fe** | Useful retained candidate; not integrated |
| Work continuity | Dark Factory [PR #133](https://github.com/ThorStarlord/dark-factory/pull/133) implements authorized recovered delivery and candidate supersession | Failure of the old executor did not necessarily mean no useful work existed |
| Evidence | Local agent reported admitted **A1 PASS / A2 PASS** for the exact candidate | Candidate-bound verification, not admitted reconciliation |
| Original reconcile | Two failures, then event **16: TERMINAL/BUDGET_EXHAUSTED** | Correct failure accounting, not a negative feature-quality verdict |
| Recovery | Explicit owner authorization; event **17**; recovery code in draft [PR #141](https://github.com/ThorStarlord/dark-factory/pull/141), executed source **88c4464** | One auditable new RECONCILE action, no fabricated earlier success |
| Final attempts | Both recovered RECONCILE attempts failed; event **18: TERMINAL/BUDGET_EXHAUSTED** | **No admitted reconciliation, QUALIFIED_MERGE_READY, merge, deployment, or post-merge observation** |
| Continued engineering | Verifier source repair [#136](https://github.com/ThorStarlord/dark-factory/pull/136), terminal-step correction [#138](https://github.com/ThorStarlord/dark-factory/pull/138), bounded judge [#140](https://github.com/ThorStarlord/dark-factory/pull/140), status [#139](https://github.com/ThorStarlord/dark-factory/pull/139) | Useful reviewable draft improvements; not proof of merged capability |

The operator reported HALT restored and scheduled tasks disabled. These are local reported observations, not independently verified from GitHub.

## 3. Consequential choice — final retry versus diagnosis

**Goal / scope:** deliver and honestly qualify a real feature within the authorized Flash-only model and protected Campaign/merge authority.

**Alternative A — last bounded retry:** It could yield admitted reconciliation without repeating A2 or delivery. The owner granted exact one-attempt authority. Earlier standalone judge calls had succeeded on the same *input artifact*.

**Alternative B — hold and investigate:** It would preserve the remaining budget and might identify a request-construction defect, but the existing logs did not capture the outbound HTTP request, so ordinary local inspection could not resolve the remaining cause.

**Actual decision:** the last retry was authorized and executed. It failed before recorded model token generation; event 18 terminated the Campaign. The agent did not invent another recovery or claim QMR. Later investigation reused OpenCode logs/session records, with no new paid model calls.

**Returned evidence:** successful and failed judge sessions occurred in the same minute from the same visible directory/model/agent context; all 17 relevant sessions reportedly used OpenCode 1.18.32 and unchanged Archon/Flash configuration. Successful runs registered about 23k–47k input tokens; zero-input failures did not complete a first provider call. OpenCode did not store complete outbound request bodies/headers. The input file digest was unchanged, but **input identity is not wire-request identity**. The actual cause is **UNKNOWN**, not a demonstrated intermittent upstream service fault or Dark Factory code defect.

**Learning about the decision:** retry *eligibility* (authority and budget) did not itself establish retry *value*. That last call was an outcome-completion gamble, not a causal diagnostic. If the relevant request-shape evidence had been available, the retry recommendation could have been materially different. This warrants better evidence selection and attribution, not retrospective blame of the executing agent.

## 4. Autonomy dimensions this episode exercises

- **Task/engineering autonomy: substantially supported within this case.** The agent generated and preserved candidate work, reconciled repository state, verified exact heads, corrected tests, handled an accidental generated file and a non-fast-forward branch, and removed a duplicate bounded-judge change.
- **Decision and continuation autonomy: meaningful but bounded support.** The agent recovered work without recomputing it, learned from failed attempts, kept stronger claims separate from successful probes, selected read-only diagnosis after repetitive failure, and stopped at the protected boundary.
- **End-to-end outcome autonomy: NOT established.** Despite A1/A2 PASS, reconciliation was not admitted and the real feature was not integrated. Do not score this workload as full autonomous delivery.

**A failed executor or read-only semantic gate is not automatically the failure of every independently warranted engineering responsibility.** Preserve what is verified, reassess what can still be done under existing authority, and stop the blocked gate without bypassing it.

**Full delegation is not unlimited authority.** Avoid unnecessary owner prompts for ordinary engineering. For HALT removal, terminal-state reopening, paid diagnostics, merge, credential and deployment changes, maintain explicit, bounded authority. Do not label all protected interventions as avoidable; categorize them from actual evidence if evaluating supervision burden.

## 5. Process-first accountability rather than individual blame

Investigate the conditions that created or obscured the failure:

| Process/interface condition | Corrective direction |
| --- | --- |
| Provider error lacked useful HTTP request/error metadata | Preserve sanitized wire-request shape, correlation fields and error code where warranted; never leak secrets or full sensitive prompts |
| Judge wandered into exploratory repository reads | Bound judge to the admitted evidence envelope; prompt text is not hard enforcement |
| Terminalizing tick misleadingly printed steps=0 | Use persisted journal outcome and separately fix operator accounting |
| Verifier could check the wrong source checkout | Pin source identity, working directory, and clean-wheel smoke environment |
| Generated artifacts and PR overlap complicated publication | Exact-file staging, inspect changed files, verify remote head, track actual stacked dependencies |
| Repeated owner-controlled transitions impeded seamless continuity | Make ordinary vs protected authority reconstructible at mission start, without granting protected operations implicitly |

These are **process improvements**, not proven root causes of the failed provider request. The coding agent is accountable for accurate actions and claims, yet available evidence does not justify blaming an individual for the opaque provider failure.

## 6. Transfer and promotion limits

Current [autonomous terminal mission guidance](../../skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md) already covers continuation across warranted responsibilities and legitimate protected stops. [Learning/Reconciliation](../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md) already says execution failure is evidence and not automatic retry. The [Capability Learning Loop](../research/capability-learning-loop-v0.md) requires cross-episode evidence before promoting doctrine.

**Candidate transferable lesson:** distinguish product work preserved, executor transport success, candidate A1/A2 admission, semantic reconciliation, and protected integration. Ask what *new evidence* justifies another attempt, not only whether another attempt is possible. Correctly stop one blocked control path without freezing independent authorized work.

This episode mainly illustrates and challenges application of existing guidance. It **does not** warrant a new Skill, generic retry engine, learning schema, policy, artificial test program, or claim of cross-repository reliability. An independent later episode could test whether these distinctions recur and whether process corrections change actual outcomes; preserve counterevidence and installed-Skill attribution.

**Observation dimensions when available:** product value retained; avoidable versus reserved intervention; evidence/recovery continuity; claim integrity; inquiry/retry cost; correct stop; and integrated end state. These are qualitative lenses, not a mandatory dashboard or score.

**Final disposition:** bounded autonomous engineering **SUPPORTED**; exact-candidate runtime verification **operator-reported PASS**; end-to-end delegated mission **NOT QUALIFIED**; provider root cause **UNKNOWN**; frozen Campaign at event 18; no implied retry/merge/deploy authority.
