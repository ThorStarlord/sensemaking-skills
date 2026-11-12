# SCL normal-use feedback: a passing PR review examined the wrong change set

**Date:** 2026-11-12  
**Repository:** `ThorStarlord/sensemaking-skills`  
**Status:** independently checkable Git/hosted *mechanical incident* and a bounded later interpretation; **not** independent coding-agent reuse or causal SCL benefit.  
**Current-source inspection:** `main@5fdfd03f55936567b889152510ead1129650d9c9`, after PR #838 and SCL/AMS integration. This report does not make later branches or other hosts current by assertion.

## The real engineering responsibility

[PR #838](https://github.com/ThorStarlord/sensemaking-skills/pull/838) implemented a useful committed-change review consumer: combine changed committed paths with BASE-revision source-fingerprint overlap and per-file `context-for`, while preserving source identity, candidate relevance and incomplete coverage. This is product construction, not a task invented to demonstrate SCL.

The originating agent's [session receipt](../../.sensemaking/receipts/2026-11-12-committed-review-evidence-overlap.session.yaml) records three earlier source-checked historical lessons, the selected review-context responsibility and its alternatives. The receipt's pre-action commit `11d207850b0046be5d4677e989520c924be5a19f` precedes the first implementation commit `846ef093e6cecc91c32f8bc7e9647b2f8c5f6447`. This ordering supports **authored, pre-implementation availability and consultation reports**; it does **not** independently reproduce the original tool reads, identify private cognition, establish a different actor or prove a better design than an unexposed alternative.

The cited prior episodes remain intact: [bounded query completeness](semantic-stewardship-episode-a-2026-10-15.md), [uncited changes/source drift](semantic-steward-workspace-impact-2026-10-21.md), and [source-linked re-entry](2026-11-02-cross-episode-source-reentry-learning.md). Historical *applicability* is conditional, not a requirement to imitate an older method.

## A new, separately observed failure at the hosted consumer boundary

The original hosted **Semantic Context Re-entry** consumer passed at exact PR head `8121ed5508efc1c3d3747986f3009aa97c61c303` ([run 43175086527](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/43175086527), completed SUCCESS). The job log nevertheless printed:

| Original event | Revision/baseline | Logged changed paths |
| --- | --- | ---: |
| Initial successful hosted review | moving PR base tip `c644323abab5f9ca7808f1f2369b2ccb22286828` → head `8121ed5508efc1c3d3747986f3009aa97c61c303` | **10** |
| Actual PR change set | the PR's Git merge-base → head | **7 files** |
| Corrected successful hosted review | merge-base `a8dcc05261db08ffe166459f2949a2e231ab4354` → head `ed6391547cc096023a12b54b5a4c5651b434f27e` | **7** |

The corrected job is [run 43175430045](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/43175430045), completed SUCCESS; its source-pinned log reports `source_ref=a8dcc052...`, `pr_base_tip=c644323...`, `changed_paths=7`, `uncited_changed_paths=2`, `truncated=true` and `agent_benefit_established=false`. These are **directly observed hosted outputs**, not a retrospective interpolation from the PR's prose.

GitHub PRs show changes from the *merge base* of target branch and topic branch. A caller comparing two diverged branch tips instead answers a different, valid two-tree question and can include files changed on the target branch after the topic branch diverged. In the first hosted consumer, all shape/identity assertions passed **for the wrong comparison scope**. This was not an erroneous `workspace-review-context` response to the refs it was given.

The [corrective commit `ed639154`](https://github.com/ThorStarlord/sensemaking-skills/commit/ed6391547cc096023a12b54b5a4c5651b434f27e) changes the workflow caller: fetch revisions, calculate `git merge-base` with a full-history fallback, and supply that baseline to the **existing** CLI. `.github/workflows/semantic-context-reentry.yml` is the current executable caller. `workspace-review-context` still permits explicit arbitrary committed revision pairs and still discloses `git_ancestry_assessed: false`; no universal policy to treat every comparison as a PR comparison follows.

**What changed in evidence:** the first job's mechanical PASS no longer supports the claim “the packet represents the PR's actual files.” The corrected job supports the narrower claim “this PR caller passed the actual merge-base/head pair and displayed the expected seven paths.” Neither job establishes the *semantic correctness* of every relevant graph claim, a human review improvement or an agent's independent use of learning.

## Bounded lesson and legitimate feedback

**Incident:** a successful hosted review was internally consistent but scoped to a different Git comparison than the intended PR change set.

**Conditional lesson for a future PR-review consumer:** establish whether the question is “what changed in this PR?” or “what differs between these two exact commits?” For the former, use the PR merge base; retain the moving base tip as a separate identity when relevant, and compare the reported changed-path set/count with the authoritative PR file set before treating the packet as adequate review context. If the user intentionally requests an arbitrary two-tree comparison, do **not** silently substitute a merge base.

This lesson qualifies the *scope and measurement* of a source review, not a general prohibition on two-tree diffs. It is a product/domain fact about this caller plus a transferable **candidate methodological caution**, not an observed causal improvement of VERIFY, RECALL or any cognitive control move. The earlier `lesson:query-completeness-is-evidence` is an informative analogy—both episodes show that seemingly complete results can conceal a missing inference boundary—but their **concrete causes differ** (truncation disclosure versus wrong comparison baseline). They do not constitute a matched causal experiment or license a universal new metareasoning policy.

The originating PR #838 session's `NO_NEW_LESSON` disposition described what was known when it finalized. This **later** evidence came from the hosted result and subsequent corrective source change; do not rewrite or backdate that final receipt. A new source-linked `incident` and `lesson` may be indexed with the current document as provenance, and reached through the current semantic-CLI component's file ownership. Both remain *historical claims*, never permissions or automatic rules.

## SCL program evidence and stopping conditions

| SCL responsibility | Disposition after this episode |
| --- | --- |
| Independent later agent decision (Task 4) | **NOT QUALIFIED:** the originating agent was a later engineering episode, but independence from the prior active actor and original native predecision read trace are not established. Git chronology is stronger than a post-code-only rationale, weaker than independent behavioral observation |
| Later feedback (Task 5) | **BOUNDED CONSEQUENCE:** retain the new observed caller-scope incident, interpretation and explicit applicability limit in the existing knowledge owner; do not rewrite the original episode or infer that old lessons caused the repair |
| Coverage/overhead (Task 7) | **PARTIAL:** this episode supplies an authored pre-action receipt and two original hosted results. An apparent PASS needed source/log review; elapsed CI or PR times cannot identify cognitive overhead or learning benefit. Missing traces in other episodes remain NOT_ASSESSED |
| Cross-episode method synthesis (Task 8) | **NO_GLOBAL_METHOD_CHANGE:** overlap with the October 15 episode is a caution about interpreting result scope, not a demonstrated shared mechanism or qualified method advantage |
| Cross-repository transfer (Task 9) | **NOT_EXECUTED:** no authorized receiving-agent task or recipient repository owner context is present in this evidence |
| Outcome/automation (Task 10) | **KEEP BOUNDED SOURCE RECALL AND CORRECTED CALLER; NO AUTOMATIC LEARNING ENGINE:** corrected job PASS and original error support local product value, not comparative performance. The negative case and extra review cost argue against inflating general requirements without a concrete consumer |

**Next genuinely qualifying action:** during unrelated real engineering by a distinct agent, examine original predecision source/Skill-read and task decision evidence as available. Record a justified application, narrowing, rejection or `NO_MODEL_CHANGE` with its actual outcome; independently compare an alternative only when attribution is possible. Do not create synthetic proof of learning, mandatory per-task reports or foreign-repository mutations to force a positive SCL verdict.
