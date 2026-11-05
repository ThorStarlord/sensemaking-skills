# Connected Prospective Inquiry — Source-Pinned Cases v1

**Date:** 2026-11-05.  
**Purpose:** exercise the [connected conceptual ontology](connected-prospective-inquiry-ontology.md) against dated, inspectable source history; provide positive and negative controls for the [CPI-CQ-01..16 competency account](connected-prospective-inquiry-competency-v1.md).  
**Status:** source-annotation and normative examples **only**. Not a new Depth Exploration, a reranked portfolio, an adversarial finding, a newly ratified PRD/design, a real repair or an independent-agent study.

## 1. Source snapshots, original baselines and attribution

**Report-containing snapshot:** `ThorStarlord/sensemaking-skills@d8c0f4de30e989a5e99501942bf9167148bd16a3` (2026-11-05, immediately after merged planning PR #748). The file snapshots below are linked at that exact repository commit; each historical report's own **inspected earlier baseline** is a separate revision and must not be overwritten.

| Key | Original source at pinned snapshot | Its own assessment source / meaning |
| --- | --- | --- |
| **H-A** | [Discovery Memory prospective synthesis](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md) | 2026-10-28 assessment of current architecture at `main@b6cf509`; four `arch:` alternatives, conditional `conseq:` and a *revised provisional preference*, not a product decision. |
| **H-B** | [Situated Knowledge focused depth](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/docs/explorations/2026-11-03-depth-situated-knowledge-and-possible-futures.md) | 2026-11-03 report, inspected `main@0991209b17b6a1e969ac113eeb1441d07da4f795`; an explicit *hypothetical agent episode*, not observed creativity. |
| **H-C** | [Architectural Generativity portfolio reassessment](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/docs/explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md) | 2026-11-03, inspected `main@a1b1872a4d212fc9fd6e1576b966fbb71b6da67f`; changes one **pairwise inquiry preference**, not the older global ranks or any implementation decision. |
| **H-D** | [Graph Activation architectural synthesis](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/artifacts/history/2026-11-01-graph-activation-architectural-synthesis.md) | Dated 2026-11-01, source-backed comparison of three mechanisms, `arch:` identities and conditional downsides; provisional architecture judgment, not a tested runtime change. |
| **N-E** | [`to-prd` Skill](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/skills/to-prd/SKILL.md), [architecture synthesis contract](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/skills/workflow-planner/references/artifact-contracts.yaml), [architectural synthesis template](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/skills/repository-semantic-steward/references/architectural-synthesis-template.md) | **Normative contract crosswalk**, not a historical combined PRD+technical-design outcome. |

**Annotation identities** like `A-D1`, `C-R1` and `D-X2` below are *local to this account*. They do not rename the original `poss:`, `arch:`, `conseq:`, portfolio or decision. The fact that source documents exist at H-A through H-D establishes what those authors wrote, not that a future independent agent benefited.

## 2. A — A real conditional consequence narrows, but does not reverse, preference

**Source:** H-A ``4–11. **Profiles:** Focused Depth Exploration and Convergent Reassessment. **Evidence status:** source-grounded historical analysis with observed source constraints and hypothetical later benefit.

**Original intended end:** retain meaningful prospective alternatives and their reasons across authorized target-repository sessions. **Operands:** A = `arch:git-reviewed-local-memory`; B = `arch:receipt-based-memory`; C = `arch:strategic-artifact-projection`; D = `arch:grounding-pack-decision-log`. They remain four distinct source-local alternatives, not one composite design identity.

**Previous evaluation:** H-A `6 provisionally prefers A under fidelity, possible reconsideration and existing contracts, with B a lighter alternative and C/D weaker in that purpose-relative comparison. Preference is explicitly **not** an authorized selected architecture.

**Depth unit A-D1:** `conseq:persistence-requires-write-authority`. The source observes that default discovery is read-only and that uncommitted receipts are lost. *If* a later session cannot edit and commit to the target's knowledge surface, *then* neither an envisioned persistent local record nor an expanded receipt will realize the cross-session retention goal in that session.

- **Direct:** a proposed local record cannot persist without write/commit authority.
- **Second-order, conditional:** later retrieval of that record cannot benefit from an unsaved record; there is no observed later-agent comparison.
- **Counterfactual fork:** when authorized knowledge edits and commits *are* available, A retains its expected fidelity advantage *if* later agents actually consult the records.
- **Systemic risk:** target-side maintenance/citation noise can accrue; magnitude and incidence remain unmeasured.
- **Opportunity:** H-A `9 describes `poss:repository-local-prospective-decision-memory` as a *hypothetical derived possibility* with existing plan overlap; not independent proof of a novel owner goal.
- **Stop:** extra speculative layers would not change the A-D comparison under the stated authority.

**Reassessment A-R1:** H-A `8 explicitly records `REVISE_PREFERENCE`, **narrowed** to sessions with knowledge-edit/commit authority. A remains preferred over B in that scope. The prior evaluation, all compared options and the read-only exception are preserved. No global product ranking, Level-4 adoption or implementation authorization follows.

**Negative control A-N1:** "The newly mentioned possibility proves retained knowledge improved creative discovery" is unsupported: the report authors a hypothesis and notes its overlap with planned work; it does not contain a later-agent observation.

**CPI coverage:** 01–03, 06–10, 16.

## 3. B — A source-faithful direct/second-order/systemic cascade with two opposite hazards

**Source:** H-B ``1–7. **Profile:** Focused Depth Exploration with adversarial forks. **Evidence status:** **hypothetical episode** grounded in actually accepted ADR distinctions, not a behavior observation.

**Premise B-P1:** suppose a future coding agent understands the *artifact-, revision- and authority-scoped applicability* of two source-faithful constraints and uses those distinctions in prospective reasoning.

**Observed source anchors:** ADR 0030 governs a compact Grounding Pack; ADR 0031 authorizes a richer typed semantic knowledge system and explicitly bounds ADR 0030's size limitations to the compact pack; ADR 0034 makes repository understanding and prospective reasoning primary product outcomes. Coexistence of compact entry and rich knowledge is already accepted—not a newly discovered feature.

**Conditional chain B-D1:**

1. **Direct, partially logical:** artifact-scoped constraints do not contradict solely because they have different sizes or audiences. Holding their original scopes avoids an *invalid inference* that one must replace the other.
2. **Second-order, behavioral hypothesis:** if a later agent applies both scopes correctly, it may keep *both existing experiences* in view: small first-engagement orientation and selectively retrieved deeper historical understanding. This is not yet proof that graph memory improves the agent over ordinary ADR prose.
3. **Systemic, hypothetical:** repeated scope errors could accumulate into an artificially narrow possibility landscape, or fabricated exceptions could accumulate into false permissions and unavailable product futures.
4. **Creative opportunity:** ask which new future questions become conceivable while honoring both constraints. The identified entry/deep knowledge outcomes already belong to accepted intent: **RESTATED or mechanism-level reframing**, not a new `poss:`.
5. **Counterfactual fork 1:** if an agent globally applies the compact-pack budget to all knowledge, it hides legitimate deeper alternatives.
6. **Counterfactual fork 2:** if it invents a context exception to a real owner constraint, it wrongly treats forbidden paths as permissible.
7. **Counterfactual fork 3:** if a competent source-only agent already understands the ADRs, the specific marginal benefit of retained typed relationships is not demonstrated.

**Beneficiaries and harms:** repository owner and later coding agents may gain relevant options and source-aware judgment; maintainers and affected users may suffer needless complexity, inapplicable alternatives or false confidence. This is a *distribution of hypothesized outcomes*, not observed user testimony.

**Stop:** the historical report explicitly declines to infer automatic contextual truth, observed agent creativity or owner-endorsed new goals. No new architecture, strategic ranking or executable schema is selected.

**Negative control B-N1:** `A mayProduce B` and `B mayEnable C` cannot be composed into `A definitely causes valuable user end C`. Each link has its own assumptions, and the final user end has no independent value/novelty proof.

**CPI coverage:** 01–06, 11–12, 16.

## 4. C — Real portfolio reassessment is local and purpose-specific

**Source:** H-C ``1–4, with its [original priority portfolio](https://github.com/ThorStarlord/sensemaking-skills/blob/d8c0f4de30e989a5e99501942bf9167148bd16a3/docs/explorations/2026-11-03-depth-exploration-prioritization.md). **Profile:** Convergent Reassessment. **Status:** provisional *intellectual inquiry* preference.

**Original operands/frame:** B = Longitudinal Engineering Judgment (historical global **rank 3** for depth inquiry); A = Architectural Possibility Generation (historical global **rank 5**). Other directions and exit/public frames are not peers in the particular reassessment and remain outside its updated pair.

**New source reason C-G1:** three depth inquiries investigated aspects of longitudinal applicability, changed premises and collective interpretation. They did **not** exhaust longitudinal judgment, but had investigated some of its original territory. Architectural transformation into qualitatively new desired product ends lacked equivalent consequence-driven depth. The basis is *what remained intellectually unexplored under this one purpose*, **not document count, generic novelty or strategic benefit proof**.

**Reassessment C-R1:** H-C provisionally prefers **A ahead of B for one next, separately authorized Focused Depth Exploration**. It **does not** amend historical ranks 5 and 3 in the prior portfolio, rerank other directions, select a product architecture, create an approved `poss:` or authorize the proposed inquiry's execution.

**Conditional reversal:** A's advantage disappears if a follow-up shows mere rewording of the existing Idea Library, if independent agent evidence changes B's open question, or if owner intent/beneficiary frame materially changes. These are *reconsideration hinges*, not evidence that the future inquiry actually ran.

**Negative control C-N1:** converting "A preferred over B for next inquiry" into "A globally ranks #1 in strategic attractiveness and should be implemented first" switches **target type and purpose**, erases unaffected alternatives and invents authority.

**CPI coverage:** 07–10, 16.

## 5. D — Architecture options, challenged assumptions and incomplete proof of benefit

**Source:** H-D ``1–11. **Profiles:** architectural comparison, conditional consequences, adversarial challenge and **partial** design-rationale reconstruction.

**Target end:** make relevant retained knowledge available to a coding agent *when it can change a decision*, while preserving active-agent control, source identity and fallback without required graph-index availability.

**Compared options and existing IDs:**
- **A, `arch:agent-native-selective-recall`:** active agent selectively consults reviewed knowledge, inspects original sources and owns the decision. **Provisionally preferred**.
- **B, `arch:opt-in-campaign-knowledge-context`:** an already selected Campaign can opt into bounded, source-linked knowledge context. **Retained complement**, not a mandatory successor.
- **C, `arch:runtime-forced-graph-context`:** workflow machinery injects context every step. **Declined counterfactual**, not a failed deployed runtime or approved build.

**Challenge D-X1, exact target A's assumption:** "The host loads and the agent applies the available Skill/retrieval reference." The report explicitly warns `installed != loaded != invoked != applied`. *If* relevant knowledge remains unconsulted, A can miss context despite correct installed docs. This is a known possibility and an unanswered behavioral question, not an observed failure of this exact option in a fresh agent run.

**Response D-R1:** preserve selective agent-native default and direct-authored-record fallback; use real host/agent observation to motivate narrower guidance if repeatable decision-changing misses occur. **Residual:** independent later-agent use and comparative value remain unqualified.

**Challenge D-X2, exact target C's mechanism:** forcing graph context may increase overhead and conflate semantic judgment with workflow execution, while incomplete knowledge can be mistaken for a blocker. This is conditional architectural criticism grounded in accepted ADR non-goals and source behavior, **not measured overhead or an actual outage**.

**Response D-R2:** retain C as declined counterfactual, and keep B as conditional context mechanism when an already authorized Campaign warrants it. **Residual:** neither C's hypothetical cost magnitude nor any independent agent behavior was tested by that synthesis.

**Design-rationale trace D-T1 (historical interpretation, not adopted final architecture):** product end -> source-relevant later judgment -> selective knowledge query and original-source review -> active agent controls applicability and action -> risk of missed retrieval -> need real host evidence before changing integration. This trace explains why A is preferred without converting its preference into a PRD, implemented architecture, required runtime adapter or product claim.

**Negative control D-N1:** labeling C "observed broken runtime feature" is false. **D-N2:** a merged Skill file proves availability, not the agent's comprehension or benefit. **D-N3:** a future "repair" that adds a schema or hook would require its own warranted consumer and cannot be declared verified from this comparison.

**CPI coverage:** 02–03, 11–14, 16.

## 6. E — Normative combined product/technical proposal, not a historical construction

**Sources:** N-E. **Profile:** Architecture Synthesis. **Type:** **illustrative contract application only**. No source asserts the following feature was proposed, adopted, desired or built as a separate product change.

Imagine an *authorized* task to specify a read-only experience in which a repository owner can inspect why an earlier architecture choice was preferred. The task's actual user intent, source and authority would have to be established first; none is manufactured by this example.

| Proposed requirement / view | Illustrative role | What would have to be sourced before adoption |
| --- | --- | --- |
| Beneficiary and outcome | Owner retrieves source, alternatives, assumptions and change conditions to understand a past choice. | Actual owner/user intent, scope, relevant historical sources. |
| **PRD** via `to-prd` | Read-only ability to present a selected decision's rationale and open limits; non-goal: auto-approve future changes; proposed success criteria with unknown baseline. | `source_intent_ref`; goal-preservation and scope-expansion approval fields; evidence quality. |
| Existing `architectural_synthesis` if genuinely competing designs | Compare direct source-backed record retrieval vs opt-in Campaign context under same goal, preserving both options and provisional choice. | Real alternatives, architecture contracts, cited target revision, actual producer and validator. |
| Proposed technical design view | A source-pinned query reads existing knowledge/reference sources, displays attribution and applicability, reports `NOT_ASSESSED` when absent, and has no write/merge authority. | Actual repository components, readers, contracts, trust and access review; interaction design and compatibility. |
| Challenge/response | What if a history pointer is stale? Show source revision, check currentness, preserve unresolved/partial state rather than declaring facts absent. | Demonstrable source-reader behavior and verification plan. |
| Construction and approval | The product spec and design remain proposals. An authorized subsequent implementation responsibility could build a bounded slice. | Selecting actor, permitted scope, approved expansion, code/path owners and actual tests. |

**Trace E-T1:** user outcome -> scoped PRD requirement -> proposed read-only source lookup + provenance/currentness representation -> hypothesized reduction of mistaken judgment -> stale-pointer challenge -> bounded verification/stop condition.

**Why it is only normative:** these connections demonstrate the *meaning and separation* of existing `prd` and architecture artifacts, not the value of a new feature, a realized architecture, a valid PRD machine output, or an accepted owner decision.

**Negative controls E-N1–3:** a spec with no named beneficiary is incomplete; a `PROVISIONAL` architecture comparison cannot become "the final approved implementation"; a PRD's proposed metric cannot be reported as an observed baseline.

**CPI coverage:** 14–16, and the authority aspect of 10.

## 7. Cross-case negative controls and honest boundary

| Mistake under review | Counterexample and proper status |
| --- | --- |
| Treating a multi-hop hypothetical chain as a proven causal dependency | B-N1: a source-faithful scope distinction does not prove later creative value. |
| Treating an opportunity hypothesis as independently discovered user demand | A-N1 and B-D1: a hypothetical candidate / restated accepted end is not a validated new goal. |
| Treating local preference changes as global strategic adoption | A-R1 and C-N1: narrowed applicability and pairwise inquiry preference preserve history. |
| Calling a critic's risk an observed defect or actual design repair | D-X1/D-X2 are *conditional*, D-R1/D-R2 are reasoning dispositions, not tested fixes. |
| Smuggling implementation authorization through a synthesis or PRD | D-T1 and E-N1–3 show the choice/producer/authority boundaries. |
| Manufacturing extra depth to satisfy a process | A stops when more branches will not change comparison; B stops at absent behavioral evidence. |
| Assuming silence means an explicit no-change decision | A report without a consequential new frame may simply end, without an invented `AssessmentRevisionAccount`. |
| Requiring an arbitrary linear phase order | B depth, C reassessment and D architectural challenge occurred in different historical contexts, not one predetermined pipeline. |

**What can be checked from this file:** the reader can trace exact source documents and differentiate observed content, historical judgment, hypothetical mechanism, normative example and authority. **What cannot:** a new independent agent actually making better decisions, automatic graph inference, owner approval of E or successful cross-artifact PRD/technical-spec production.

**Reader re-entry:** use the original source for any disputed claim; review [competencies](connected-prospective-inquiry-competency-v1.md) and [portable guidance](../../skills/strategic-repository-analysis/references/connected-prospective-inquiry-v1.md), then stop or perform the bounded responsibility warranted by the *new* task. This case inventory is not a backlog.
