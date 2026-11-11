# Consequential Decision Traceability — Divergent Exploration

**Status:** DIVERGENT ONLY — source-grounded possibility landscape; not a Coverage Assessment, Convergent Evaluation, architecture selection, feature specification, enacted Decision, schema extension, benchmark, or authority grant.  
**Target:** ThorStarlord/sensemaking-skills. **Inspected canonical revision:** [main@28a7c1269ceace2fa2c7dff9e0a21a83c9783eb8](https://github.com/ThorStarlord/sensemaking-skills/tree/28a7c1269ceace2fa2c7dff9e0a21a83c9783eb8). **Date:** 2026-11-11 (UTC).  
**Requested responsibility:** explore how consequential autonomous engineering decisions could become observable, reconstructible, challengeable and reusable; preserve distinct options for subsequent intellectual evaluation.  
**Method:** [Divergent Exploration v1](../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md) under [using-sensemaking](../../skills/using-sensemaking/SKILL.md); no Level-3 reanalysis, strategic path selection, mechanical feature, ontology mutation or independent qualification.

This inquiry concerns the **Sensemaking product** rather than the invoked reasoning method. Its governing intent is the accepted persistent, ontology-grounded repository understanding and prospective reasoning destination ([ADR 0031](../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md)), while [ADR 0029](../adr/0029-current-product-boundary.md), the four-level control model and [product strategy](../product-strategy.md) keep semantic choice and protected authority with the relevant agent/owner. The current Level-3 PATH-1 construction is background, not a new selection. Source references below are inspected at the stated main revision unless a different historical SHA is explicitly attached.

## 1. Inquiry and frames

### Q1 — Accountability

How could a later engineer tell what consequential responsibility was **actually chosen**, what was **declared before action**, what evidence and alternatives were referenced, under what authority, what subsequent execution was observed and which claims cannot be substantiated? A readable rationale is useful evidence of authorship but not the model's hidden computation.

### Q2 — Better engineering judgment

How could available product knowledge and possibility discovery change the agent's actual choice of goal, responsibility or scope, rather than merely improving the explanation of a choice already made? The product may improve accountability without improving decisions, or improve choices without leaving an adequate audit trail.

### Q3 — Candidate-set adequacy

When the evaluated options are well compared but strategically impoverished, what would expose a consequential **unconsidered** opportunity without pretending a record can enumerate all alternatives? Do not confuse a missing recorded alternative with a proved missed opportunity.

### Q4 — Cumulative adaptation

How could source-grounded decisions, deferrals, competing rationales and observed outcomes inform a later decision at the right revision and authority level without turning old recommendations into a task queue or a trace into a semantic truth oracle?

The exploration uses several **nonmandatory lenses**: acting agent vs independent reviewer; local repair vs cross-component/architectural/product opportunity; decision-time vs post-implementation vs later session; knowledge available vs queried vs demonstrably applied; observable Git/host actions vs unavailable cognition; information richness vs privacy/portability/operational cost. These lenses are used to distinguish mechanisms, not stages that every coding agent must execute. The beneficiary could be an autonomous executor, later coding agent, repository owner or reviewer; their needs are not interchangeable.

## 2. Existing model: rich documentary coverage, uneven operational continuity

The existing ontology is **already expressive enough for a substantive human-readable account** of consequential selections. This is not evidence that all corresponding operational data are currently collected, joined or queried. Most specialized selection terms are **documentary roles of existing kinds**, not machine entities.

| Level | Inspected source | What exists | What is not thereby established |
| --- | --- | --- | --- |
| Conceptual repository/epistemic model | [Layered ontology](../semantic-architecture/ontology.md), especially Intent, Evidence, Knowledge and Work layers | Goal, RatifiedIntent, Constraint, EvidenceSource, Observation, Provenance, Claim, Assumption, Uncertainty, Decision, Responsibility, Authority and Outcome with relations | A runtime record of every considered alternative or decision-time host event |
| Prospect and exploration | [Prospective reasoning](../semantic-architecture/prospective-reasoning-ontology.md), [Divergent Exploration ontology](../semantic-architecture/divergent-exploration-ontology.md) | Questions, frames, candidate expressions, transformations, source-relevant possibilities and different reasoning operations | Every discovered expression became a decision candidate or was read by a later agent |
| Scoped choice | [Convergent Direction Selection ontology](../semantic-architecture/convergent-direction-selection-ontology.md) and [portable method](../../skills/strategic-repository-analysis/references/convergent-direction-selection-v1.md) | ChoiceQuestion, ConsideredChoiceSet, CandidateWarrant, ConvergenceRationale, ScopedDirectionSelection, AlternativeDispositionAccount, SelectionReconsiderationBoundary and SelectionHandoff | Eight new executable kinds or a validated choice-set producer |
| Scope and revisability | [Warrant / Choice policy](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md), including conditional scope comparison; [consequence depth](../research/consequence-depth-and-systems-reasoning-v0.md) | Defeasible target warrant, smaller/broader scope when material, value/cost/authority tradeoffs, deferred work re-warranting | A required global exploration on every repair or an objective priority ranking |
| Learning/reassessment | [Strategic Evolution & Learning ontology](../semantic-architecture/strategic-evolution-learning-ontology.md), [strategic reconciliation Skill](../../skills/strategic-repository-reconciliation/SKILL.md) | Attributed change in evidence, interpretation or owner intent; earlier choice and new warranted continuation remain distinct | Automatic correct hindsight, causal improvement or strategy mutation |
| Authored persistent knowledge | [knowledge.py](../../src/sensemaking_skills/semantic_architecture/knowledge.py), [knowledge sources](../../src/sensemaking_skills/semantic_architecture/knowledge_sources.py) and [Steward](../../skills/repository-semantic-steward/SKILL.md) | Reviewed decision/alternative/observation/lesson claims and source-linked relations, indexed from Git-authored knowledge | An automatic mapping of a session's original comparison, the order sources were read, or why a retrieved fact affected a choice |
| Session continuation | [Session Receipt v1](../../skills/using-sensemaking/references/session-receipt-v1.md), [receipt validator](../../scripts/validate-receipt.py) and [summary consumer](../../scripts/summarize-receipts.py) | Goal, bounded reasons, statuses, authority, findings, source refs, outstanding questions and stop; an open receipt can precede implementation | A complete alternatives portfolio, full source-access history, or a causal reasoning trace |
| Knowledge query continuity | [Semantic Query Receipt](../../skills/repository-semantic-steward/references/query-receipt.md), [knowledge CLI](../../src/sensemaking_skills/semantic_cli.py) | Query target, indexed revision, claim IDs, explicit miss/outcome, source-check and reconciliation fields, with a validator and a summarizer for misses | A query was actually issued in a session merely because its contract exists; a retrieved claim actually influenced the decision |
| Strategy/execution journey | [Decision Journey Productization](../decision-journey-productization-v1.md), [journey CLI](../../src/sensemaking_skills/decision_journey_cli.py), [strategic loop](../../skills/strategic-sensemaking-loop/SKILL.md) | Read-only inspect/context/delta/impact-closure/guide over explicitly supplied strategy, Campaign, handoff, worker result, reconciliation and change-impact artifacts | Automatic PR/receipt/Git/host timeline join, evaluation of option adequacy or proof of semantic closure |
| Optional diagnostic | [Decision Observability v1](../../skills/using-sensemaking/references/decision-observability-v1.md) | Contemporaneous user-visible rationale, distinctions among native invocation, loaded instructions, considered-skipped, and retrospective interpretation | Every ordinary session records those details, all hosts expose comparable events, or transparency improves selection quality |

### A critical representation distinction

The machine knowledge model currently allows reviewed claims of kinds such as **decision**, **alternative**, **observation** and **lesson**, with supported relation predicates such as **decided_by**, **constrained_by**, **derived_from**, **references** and **learned_from**. It does **not** make the conceptual ChoiceQuestion/ConsideredChoiceSet/SelectionReconsiderationBoundary roles automatic typed runtime records. A future reader may compose these meanings in an existing report/PR/receipt without extending the parsed knowledge schema.

For a first-class machine representation, the deciding question is **which real consumer requires independent stable identity, queries, update semantics or integrity checks that the existing composition cannot supply?** This is an exploratory competency, not an established schema gap. Existing Campaign Responsibility/Authority and canonical strategic artifacts remain authoritative in their scopes; an indexed knowledge claim does not override them.

## 3. Actual producers, consumers and the discontinuities between them

The map distinguishes **documented conditional authorship** from a recorded, automatically executed data path. Existing code was inspected; an unrun CLI feature is not called an observed invocation.

| Information / operation | Existing producer and time | Existing consumer | Current discontinuity |
| --- | --- | --- | --- |
| Governing objective and current scope | Owner/ADR/product strategy; authored strategic analysis and agent's decision note | Agent reading sources; strategy inspect/context when supplied | Source existence does not establish it was reached when a particular choice was made |
| Questions and candidate alternatives | Divergent/Convergent source reports; optional DirectionSelectionRecord/PR note | Human/agent reading that report; some linked knowledge-query operations | No automatic, universally applicable candidate-set capture; original considered set must not be reconstructed from later ideas |
| Warrant and responsibility choice | Active agent; PR decision note; session receipt responsibilities[].reason | Future reader; receipt summary; handoff | Normal receipt text cap is 300 characters; linked substantial analysis is not assembled by the receipt reader |
| Source retrieval and misses | Steward-authored semantic_query_receipt when that workflow uses it | summarize-receipts, later Steward RECONCILE, human review | Knowledge-query CLI alone is not a host-observed cognitive-consumption log; relevant results still require source verification |
| Host-native tools and execution events | Actual host when it exposes events; repository commits, PR and CI as independent retained events | Host UI/log reader, GitHub history; optional diagnostic audit | Host-event availability, completeness, retention and cross-host identity were not established for arbitrary sessions |
| Execution and returned evidence | Git/PR/CI; Campaign execution handoff and result if actually used | Campaign working context; journey inspect | journey inspect accepts explicit strategic/Campaign inputs; it does not currently automatically reconstruct arbitrary GitHub PRs or receipt history |
| Evidence-to-choice interpretation | Active agent's reconciliation, strategic_decision_delta or PR note | Later agent/reviewer; explicit journey delta | A new authored explanation is not an observed causal decision mechanism |
| Durable lessons and changed assumptions | Reviewed knowledge pack, fresh dated reconciliation/receipt | knowledge-query and session receipt reader; later agent if queried | No blanket proof of longitudinal application; historical records are defeasible and must be checked at current source |
| Reviewer criticism | Separate human/agent review, possible nonauthoritative report | Human or later agent | No default first-class answer to whether omission, narrow scope or unsupported warrant caused the outcome |

**Implementation inspection:** [journey inspect](../../src/sensemaking_skills/decision_journey_cli.py) loads only explicitly supplied supported machine blocks/Campaign workspace, and reports missing manifest references rather than inferring a decision path. [summarize-receipts](../../scripts/summarize-receipts.py) scans normal session/query receipts for unfinished state, next responsibilities and query misses; it does not score candidate-set adequacy. [knowledge_sources](../../src/sensemaking_skills/semantic_architecture/knowledge_sources.py) indexes tracked Grounding Pack, ADR and reviewed knowledge records; session receipts are not knowledge claims merely by being committed. None of these consumers establishes that an unobserved alternative was internally considered.

## 4. Decision competency questions: representation versus actual answers

This is an inquiry-specific **question map**, not a new canonical ontology, required trace schema or evaluation score. Coverage labels mean: **DOCUMENTARY** = existing concepts and a suitable authored surface; **PARTIAL OPERATIONAL** = some real producer/reader supports the answer if used; **UNOBSERVED** = not established in the inspected episode or host; **INTERPRETIVE** = requires qualified judgment.

| Local question | Current basis | Answer/evidence limit |
| --- | --- | --- |
| DT-Q01: Which accepted goal and authority governed? | Strategy, ADR, receipt, Campaign authority | DOCUMENTARY; actual source consultation may be UNOBSERVED |
| DT-Q02: What specific choice question and beneficiary framed selection? | ChoiceQuestion, goal, PR note | DOCUMENTARY; normal receipt may omit explicit question |
| DT-Q03: Which evidence was **available** before selection? | Pinned source revision and dated sources | PARTIAL; reachable bytes differ from what was read or noticed |
| DT-Q04: Which knowledge was **retrieved** and checked? | Optional query receipt and host events | PARTIAL when issued/retained; not a proof of application |
| DT-Q05: Which candidates were discovered and how? | Divergent report, candidate expressions, choice-set role | DOCUMENTARY; no automatic discovery inventory |
| DT-Q06: Which candidates were actually compared before commitment? | Pre-action report/receipt; possible host transcript | PARTIAL; post-action PR prose cannot establish pre-action chronology |
| DT-Q07: What consequential alternative was never discovered? | No positive historical producer by definition | UNOBSERVED; later possibilities are retrospective challenges, not historical facts |
| DT-Q08: Why was a local, broader or no-change scope chosen? | Warrant/Choice conditional scope guidance and ConvergenceRationale | DOCUMENTARY; meaningful at decision time only if authored and grounded |
| DT-Q09: What value/assumptions/defeaters were attached to each option? | CandidateWarrant, assumption/uncertainty, consequence models | DOCUMENTARY; no mandatory option-by-option operational record |
| DT-Q10: Which selecting actor and action permission applied? | ScopedDirectionSelection, receipt, Campaign/PR | PARTIAL; selected target and authorized side effect are separate |
| DT-Q11: Was the rationale retained before implementation? | Git-committed pre-action artifact and timestamps | PARTIAL OPERATIONAL in cases with such evidence |
| DT-Q12: Which operations and outcomes occurred afterward? | PR commits/timeline/CI; Campaign result when present | PARTIAL OPERATIONAL; no inference about unseen host calls |
| DT-Q13: Did subsequent evidence justify a changed judgment? | LearningAccount, reconciliation, delta, source currentness | INTERPRETIVE; mechanical drift alone cannot decide |
| DT-Q14: What did a later agent actually reuse? | Query receipts, later decision note and host evidence | PARTIAL; relevance/consultation does not imply causal use |
| DT-Q15: Was the candidate set sufficient for the decision? | ConsideredChoiceSet role and bounded challenger | INTERPRETIVE; cannot certify exhaustive search |
| DT-Q16: Would a richer rationale improve choice quality? | Hypothesis, not established from existing artifact | UNOBSERVED; requires independent decision-relevant use evidence |
| DT-Q17: Which events can ethically be retained and shared? | Existing scope/authority/confidentiality contract | Context-dependent, host- and target-specific; not a global capture right |

The existing [competency questions](../semantic-architecture/competency-questions.md), notably CQ-039 (exact evidence and snapshot), CQ-041/047 (uncertainty/responsibility), CQ-053 (deferral), CQ-060 (evidence-to-change chain), CQ-073/078 (cross-session and historical reconstruction), CQ-079/083 (possible futures and dispositions), and CQ-098 (preferred direction and authority), already cover many underlying meanings. The DT-Q labels above reorganize *this inquiry*; they do not silently modify that document.

## 5. Authentic reference case — PR #812

**Case scope:** one observed repository-local construction sequence at its actual historical revisions, not a replay, experiment or adjudication of whether the chosen repair was right.

### What the retained evidence establishes

1. **Initial governing state:** main at [da223b37fd706e8700636d465c6263c9ab028362](https://github.com/ThorStarlord/sensemaking-skills/commit/da223b37fd706e8700636d465c6263c9ab028362); PR #811's conditional scope guidance was already integrated. Presence in source does not prove it caused this decision.
2. **Contemporaneous authored choice:** the [original in-progress receipt, committed at 7eb18a59](https://github.com/ThorStarlord/sensemaking-skills/blob/7eb18a59ad14d19125063f95d445a5c5b1e4b48c/.sensemaking/receipts/2026-11-11-filter-safe-source-check.session.yaml) states that a protected worktree inspector already existed, while source-building and workspace-query used raw Git status. It selects reuse of that inspector, records a stale Windows encoding candidate and unsubstantiated cache work as skipped, and names the authorization/source boundary. GitHub records this commit at **2026-11-11 02:46:09 UTC**.
3. **Implementation:** [2b2742c2de134d06f7f8298d9fe41920c2376328](https://github.com/ThorStarlord/sensemaking-skills/commit/2b2742c2de134d06f7f8298d9fe41920c2376328), authored at **02:47:00 UTC**, changes the two Python source paths and CLI documentation. The original receipt is its Git parent, which establishes a retained pre-implementation authored artifact.
4. **Later, richer decision explanation:** [PR #812](https://github.com/ThorStarlord/sensemaking-skills/pull/812), created **02:48:03 UTC**, describes the safety rationale and mentions Windows encoding, cache-concurrency, more query features and a separate source-check framework. It was created *after* the implementation commit. Its present body is not proof that every listed item was deliberated before 02:47.
5. **Final receipt:** [66fff7b973010fae776b50a4c80e360861714298](https://github.com/ThorStarlord/sensemaking-skills/commit/66fff7b973010fae776b50a4c80e360861714298) retains findings, execution checks and explicitly unqualified claims; it describes source/diff review and local unit/synthetic tests as NOT_RUN.
6. **Canonical integration:** [1e198d6f8d0bf6769e220b7028ab7009debc012b](https://github.com/ThorStarlord/sensemaking-skills/commit/1e198d6f8d0bf6769e220b7028ab7009debc012b), merged at **02:49:15 UTC**. The PR's final feature-head Product Validation, Release Candidate Distribution and Semantic Context Re-entry completed successfully in the inspected GitHub workflow history. This establishes configured checks, not a demonstrated external-filter exploit or independently observed later decision value.

The chronology is sourced from Git ancestry, commit metadata and PR events. The in-progress receipt is **self-authored rationale before code**; the commits, PR creation/merge and CI are **externally recorded repository events**; the account here is **retrospective interpretation**. They must not be collapsed.

### Faithfully answerable, scattered, and unavailable questions

| Case question | Answer warranted |
| --- | --- |
| Which repair was selected, and what source inconsistency motivated it? | **Yes** — the original receipt and implementation source establish the authored concern and resulting code change |
| Were some other technical tasks explicitly mentioned before implementation? | **Yes, narrowly** — the original R-1 reason mentions stale encoding and cache changes; it is not an exhaustive option list |
| Were other alternatives discussed in a PR note? | **Yes** — the current PR body lists them, but it postdates the implementation and may have been edited |
| Did a pre-action decision artifact actually exist? | **Yes** — the committed ancestor and authored timestamp precede the code commit |
| Did a verified host tool event show each file/query/Skill the agent loaded? | **Not established** by this retained Git/PR/receipt evidence |
| Did reviewed knowledge change the selection, or did PR #811 guidance cause it? | **Not established** — neither a source link nor manual Skill load identity is a causal observation; the receipt's sensemaking_source_ref is null |
| Did the agent adequately discover all materially valuable repository-level responsibilities? | **Not established** — no comprehensive or purpose-relative candidate-set coverage record survives |
| Was a larger capability more valuable than the chosen safety repair at that point? | **Not established** — requires a sourced comparison under the actual goal, not later speculation |
| Was the safety repair a mistaken choice? | **Not established** — source-based defect repair is real and consistent with the governing intent; choice quality remains a separate question |

The subsequent [PR #813](https://github.com/ThorStarlord/sensemaking-skills/pull/813) added a zero-setup first-visit product capability. It illustrates that a different kind of valuable responsibility was *later* developed; it cannot be inserted retroactively into PR #812's pre-implementation considered set or used to prove that PR #812 should have chosen it first.

**Central observation:** PR #812 demonstrates that simple, durable **decision chronology is possible today**. It does not prove **decision discovery adequacy**, **internal cognition**, or **decision improvement**. More verbose notes would increase inspectable testimony but not by themselves bridge those differences.

## 6. Local Completion Bias and the missing-option distinction

[Consequence-depth guidance](../research/consequence-depth-and-systems-reasoning-v0.md) names Local Completion Bias as a possible pressure toward the immediately visible green local result when downstream consequences matter. It is a general risk hypothesis, **not a diagnosis established for PR #812**. The opposite pressure—unbounded exploration preventing a justified local repair—is also real within the current policies.

A useful reviewer should distinguish five different situations rather than treating a thin trace as an error:

| Scenario | What would be needed to support it | What retained source evidence alone cannot establish |
| --- | --- | --- |
| Adequate discovered set; good choice | Purpose-relative credible alternatives, faithful source warrants, and consequences under relevant authority | Objective global optimality |
| Adequate discovered set; poor choice | Original set and governing objective, plus actual violated premise or superior warranted choice at that time | Poor choice just because the selected work is small |
| Inadequate discovered set | A credible, decision-changing alternative absent from the documented candidate set *and* grounds that it was discoverable/relevant then | That the agent never privately considered that alternative |
| Justified local work despite broader options | Smallest sufficient scope, no decision-changing downstream dependency, acceptable opportunity cost | That all wider product possibilities are inferior |
| Inassessable choice | Missing decision-time source exposure, alternative coverage or outcome evidence | A forced positive/negative verdict |

**Negative-space problem:** an omitted idea creates no original event to log. Possible later evidence is a retrospective **coverage challenge** at a frozen historical source revision, with separately marked later knowledge and an explicit comparison objective. Such a challenge may identify a missed *recorded* alternative or construct a new plausible one. It cannot prove an absent thought, a particular cognitive cause, or a universal best option.

A source-grounded local conclusion should not require a default full-repository divergent pass. A reasonable trigger for **considering** wider scope is an actual cross-component consumer, repeated local workaround, changed product goal, meaningful omission cost, unstable original problem framing or a concrete higher-value alternative already present. The agent still decides whether the extra search is worth it under current Warrant/Choice and inquiry guidance.

## 7. Possibility landscape — genuinely different mechanisms

All C identifiers below denote **expressions in this inquiry**, not durable ProductPossibility IDs, actual capabilities, backlog tickets or adopted design. They are not ranked. Shared constraints: source identity, active agent judgment, real authority, minimal data collection, source-drift awareness and a valid no-change outcome. A conceptual label does not authorize a new CLI command, schema field or host integration.

### Family A — Compose the existing surfaces better

#### C01 — Consequential decision handoff without new data classes

**Expression:** When an actual choice warrants future reconstruction, compose existing goal/PR/receipt/choice-source pointers into a compact *decision context*, with the one live choice, its material alternatives, decisive sources, authority and revisit trigger. The producer is the active agent; a future reader uses existing artifacts and links.

**Distinct value:** reconstructability by convention and reference discipline, minimal maintenance, portable without framework runtime. **Cost/unknown:** the content is manually authored; inconsistent use and absent host evidence persist. This is not a proposal to force a report for every fix.

#### C02 — Decision-time witness note as a bounded optional use of existing receipts

**Expression:** For particularly consequential selections, record a brief pre-action, source-linked reason and known competitor set with a stable Git source artifact; then add outcomes separately. The normal compact session receipt may point at a substantial existing report rather than receive new machine fields.

**Difference from C01:** changes **when** a selected account is retained, not primarily how sources are assembled. **Risk:** process overhead and persuasive but incomplete self-report; historical omission remains unknown.

### Family B — Make consequential decisions independently addressable

#### C03 — First-class *documentary* Direction Selection Record

**Expression:** Give important decisions stable documentary identity and typed roles for ChoiceQuestion, ConsideredChoiceSet, CandidateWarrant, actual selection, nonselection dispositions and reconsideration conditions, represented in a PR/ADR/strategy artifact or optional Markdown. This uses the [already defined conceptual roles](../semantic-architecture/convergent-direction-selection-ontology.md), not a new ontology.

**Value:** prevents the loss of alternatives and makes later challenges cite one decision rather than reconstruct scattered prose. **Risk:** dual truth with existing Campaign, ADR, strategy or receipt if its scope is not sharply limited; an optional report alone has no automatic reader.

#### C04 — Queryable, versioned machine decision record *if a consumer needs it*

**Expression:** A future machine-queryable decision representation could bind stable target/choice identity, source state, attributed alternative dispositions, prereqs and reconsideration links. Candidate producers might be explicit selection/handoff operations and readers an existing index/journey API.

**Distinct from C03:** machine addressability, validation and migrations are the point; documentary expressiveness alone is insufficient warrant. **Hard question:** which real operation requires cross-session machine joins not achievable using current reviewed decision/alternative claims and strategic artifacts? Without that consumer, new schema would be overhead.

### Family C — Join the existing Decision Journey to real construction history

#### C05 — Read-only Git/PR/receipt journey bridge

**Expression:** A caller-supplied PR, commit or receipt reference could allow a read-only journey view to display **observed order**: pre-action authored account, code commits, PR notes, hosted checks and later reconciliation. It would state source coverage and not infer hidden choices or causality.

**New purpose:** inspect a normal coding episode even without a Campaign workspace. **Dependency:** explicit source identities and trustworthy access to Git/host records. **Risk:** confusing chronology with the reasons a model acted or with correctness of the initial responsibility.

#### C06 — Historical decision-to-outcome delta, not a causal verdict

**Expression:** A reader could compare original expectations/warrants and scope to the verified implemented change and later observed outcome, keeping **not evaluated**, **contradicted**, **source drift** and **still plausible** distinct. Existing change-impact and strategic-decision-delta surfaces supply much of the vocabulary.

**Different from C05:** interprets *anticipated vs observed* semantic content after an externally grounded timeline, not just temporal order. **Limit:** requires explicit authored expectations; missing expectations cannot be reconstructed as if stated originally.

### Family D — Independently observed event provenance where available

#### C07 — Optional portable host-event references

**Expression:** When an agent host exposes file reads, Skill loads, tool calls/results or execution IDs, retain **pointers to selected consequential events** with host type, revision, timestamps, accessible source and coverage limits. A reader can compare those observed events with authored claims.

**Value:** stronger attribution of what was actually run or loaded. **Cost:** host portability and stable event identifiers; permissions, confidentiality and retention policies differ. **Nonclaim:** event observation cannot expose private internal causation.

#### C08 — Sparse event evidence / explicit noncapture as a product mode

**Expression:** Rather than exporting full logs, retain only independently verifiable event IDs or bounded summaries needed to challenge one material decision; mark absent/inaccessible events as NOT_ASSESSED. Other hosts may support only Git history and existing receipts.

**Difference from C07:** the *epistemic/minimization contract* is central rather than rich telemetry. It may deliberately deliver less trace detail to reduce cost, privacy risk and false completeness. **Tradeoff:** less direct evidence for later independent review.

### Family E — Retrospective judgment and option-set scrutiny

#### C09 — Source-pinned candidate-set adequacy critique

**Expression:** An independent later agent could reframe the original *decision question*, examine original candidate descriptions and the then-current repository, and identify plausible missing domains, stakeholder outcomes or scopes. The result is a **retrospective challenge report** that labels original-not-recorded, newly constructed and genuinely unassessed candidates separately.

**Value:** targets the gap a precise rationale cannot solve. **Limitation:** a later challenger is not a recording device for the original agent's unobserved thoughts; hindsight and later knowledge create asymmetry.

#### C10 — Consequence-depth review of the selected boundary

**Expression:** Review whether the actual change had dependent consumers, later effects or a wider governing invariant for which the selected scope was inadequate. Use [existing consequence-depth guidance](../research/consequence-depth-and-systems-reasoning-v0.md) and change-impact artifacts; a well-justified local repair remains an acceptable outcome.

**Difference from C09:** evaluates *scope fitness* of the selected responsibility, not whether the original option set spanned product opportunities. **Risk:** retroactive escalation from merely imaginable dependencies.

#### C11 — Opportunity cost and justified omission account

**Expression:** A later evaluator may ask what materially promising product advancement was deferred by the chosen work, and whether that tradeoff was acceptable at the actual source/authority/time horizon. A no-change or bounded repair may still be most justified.

**Difference from C09/C10:** the object is **foregone value over time**, not missing discovery or technical consequence. **Limit:** counterfactual benefit is hypothetical unless separately evidenced; no numeric regret score follows.

### Family F — Longitudinal decisions that learn without rewriting history

#### C12 — Deferral-to-reselection continuity chain

**Expression:** When a previously deferred responsibility is reconsidered, link the original dated source, the original deferral reason, the current evidence/owner intent and the newly authored warrant. A changed judgment need not pretend that an earlier unobserved trigger occurred.

**Value:** later agents need not repeatedly rediscover why an option was left open. **Existing overlap:** Warrant/Choice and session receipt guidance already support this. **Gap candidate:** discoverability and consumers across multiple contexts, not conceptual semantics.

#### C13 — Outcome-bound lesson and revised assumption

**Expression:** Record what an engineering decision *expected*, what later source/runtime evidence *established*, what remains unqualified, and which assumption a later agent should recheck. Review and source-link only consequential lessons in existing knowledge/reconciliation surfaces.

**Different from C12:** follows an executed decision to outcomes and actionable learning rather than a deferred item to renewed selection. **Risk:** forgetting actual benefit cannot be inferred from a successful merge, and 'learned' claims can ossify.

### Family G — Make retained knowledge useful at the instant of a choice

#### C14 — Decision-sensitive source retrieval with explicit coverage

**Expression:** At a genuinely consequential selection, use existing workspace-query, context-for, relevant ADR/strategy and prior decision records to find governing constraints, alternatives, affected consumers and history **before** committing; disclose NOT_ASSESSED and query misses.

**Value:** improves the *inputs* that could affect selection. **Overlap:** RECALL/Steward and query receipt contracts exist. **Limit:** a query log proves only what was asked/returned if honestly recorded; seeing a source does not prove it changed judgment.

#### C15 — Applied-knowledge connection, not another retrieval count

**Expression:** In the retained selection rationale, explicitly identify the one or few source-grounded claims that **materially support or defeat** an option, with the actual inferential consequence and source revision. Distinguish available, retrieved, verified, decisive and merely cited knowledge.

**Different from C14:** represents **decision relevance/application**, not retrieval coverage. **Risk:** still authored interpretation, not objective causality; avoid treating a graph link as an authorization or truth proof.

### Family H — Improve the active agent's deliberation when stakes warrant it

#### C16 — Conditional consequential choice checkpoint

**Expression:** For a consequential, ambiguous choice, ask the active agent to distinguish candidate warrant from preference, inspect one decision-changing omitted scope, estimate downside/reversibility qualitatively, and state the stop/revisit condition *before* acting. Ordinary clear repairs bypass it.

**Value:** may improve judgment directly, not just later audit. **Overlap:** already present in Warrant/Choice, Convergent Evaluation, Goal Fitness and consequence-depth guidance. **Uncertainty:** method efficacy, unnecessary ceremony and reactivity to a transparency request are not established.

#### C17 — Independent perspective or critic for narrow-option risks

**Expression:** When warranted by high consequence or poor option coverage, a separate reviewer/agent may challenge the problem framing, discover a neglected beneficiary or identify a falsifying source. The selecting agent receives this as **evidence**, not automatic veto, hidden delegated authority or mandatory subagent choreography.

**Different from C16:** independent *perspective acquisition* rather than the same agent writing more rationale. **Costs:** context duplication, possible shared assumptions, host availability, and human oversight; no independent qualification is implied.

### Family I — Challenge the premise that 'more trace' is the best end

#### C18 — Reviewer-facing decision contestability without exhaustive logs

**Expression:** A human/reviewer-facing view could organize the few challengeable points: 'What goal?', 'What alternative?', 'Which source?', 'Who had authority?', 'What would overturn it?', 'What happened?'. The artifact might be a better question interface into existing records rather than a detailed step-by-step reasoning trace.

**New beneficiary:** improves reviewer comprehension and ability to dispute a consequential claim. **Difference:** traceability as **contestable claims** rather than transcript volume. **Boundary:** user interface design is a hypothesis, not evidence of reviewer benefit.

#### C19 — Deliberate nonretention and graduated trace fidelity

**Expression:** Treat sensitive host prompts, tool outputs, local paths and secrets as **data not automatically eligible for capture**. A decision account can retain stable redacted references, evidence category, unavailable status and verification boundary while deliberately discarding raw inputs. Richer capture would require a distinct justified use and authority.

**New frame:** maximize trustworthy usable evidence per permissible disclosure rather than maximize volume. **Tradeoff:** some later questions become unanswerable by design; the UI must not imply a redacted account is complete.

## 8. Relationships, possible combinations and real tensions

These are **possibility relationships**, not adopted architecture:

| Relationship | Distinction that matters before any convergence |
| --- | --- |
| C01/C02 and C03 | Existing reports may suffice for many decisions; stable documentary identity could help cross-context challenge but also duplicate receipts, strategic decisions or reviewed knowledge |
| C03 and C04 | Document roles are already expressive; a machine schema is justified only by an actual cross-session query/consumer that cannot use existing kinds/contracts |
| C05 with C07/C08 | Git/PR timeline is often retained, host events may be absent; richer event capture should be optional and never silently simulated by PR data |
| C06 with C13 | A mechanically shown implementation delta is different from an authored learning statement; both must keep their respective claim ceilings |
| C09/C10/C11 | Candidate discovery, responsibility scope and opportunity cost are **different axes**. One failure does not prove the other two |
| C09 with C16/C17 | A later challenger may improve later review, a decision-time intervention may change the choice; they are not substitutes and cannot inherit one another's evidence |
| C12 with C14/C15 | A retained deferral matters only if re-retrieved at the next consequential choice; retrieval alone is not demonstrated application |
| C16/C17 versus C01/C02 | Deliberation may change behavior at cost; rationale/retention may leave behavior unchanged. Accountability and decision improvement need different success conditions |
| C18 with C07/C08/C19 | Independent challenge can be supported by selective, confidential, incomplete evidence; UX must disclose provenance holes and avoid claiming a complete host trace |
| All families and authority | A decision record cannot grant merge, product-thesis revision, external access, deployment or release rights. Source/provenance links do not establish truth |

**Transformation accounts (attributed to this report's source-based interpretation, not hidden cognition):**

- **T1 (concept to operation):** existing ConsideredChoiceSet/SelectionReconsiderationBoundary documentary meanings + PR #812's brief original receipt suggest separating *what the ontology can describe* from *what a routine decision producer actually retained* -> C03/C04 versus C01/C02.
- **T2 (journey to historical evidence):** the existing caller-supplied journey inspect contract + PR #812's Git-anchored chronology suggest a different reader problem: joining ordinary PR/receipt histories without inventing reasoning events -> C05/C06.
- **T3 (visible choices to negative space):** the original receipt's limited alternatives + Convergent option-set adequacy semantics show a reviewer may need a *new, labeled retrospective inquiry* rather than a longer original trace -> C09/C11.
- **T4 (retrieval to meaningful use):** semantic_query_receipt can record query/claim IDs; the product strategy asks for decisions changed by retained knowledge -> C14 is retrieval availability and C15 is applied interpretation, not equivalent outcomes.
- **T5 (transparency to contestability):** the optional decision-observability guide and limits of host events suggest a different beneficiary/end: source-grounded challenges under confidentiality constraints -> C18/C19.

These accounts describe how the **authored exploration** relates sources to expressions. They are neither claims of model causal reasoning nor new registered semantic predicates.

## 9. Operational responsibility: extend, compose, or create?

No proposed new action below is authorized for implementation. The table identifies **possible product responsibility owners** so that future comparison can test whether there is an unmet consumer, rather than interpreting a new label as a new tool requirement.

| Responsibility | Existing owner/surface | Extension possibility; boundary to test |
| --- | --- | --- |
| Produce decision-time rationale | using-sensemaking Warrant/Choice, Convergent guidance, PR note, session receipt | Compose linked authored account (C01–C03); no mandatory new action or hidden-trace requirement |
| Persist original decision/alternatives with identity | ADR, strategic analysis, optional DirectionSelectionRecord, reviewed decision/alternative claims | New machine command only if a consumer demonstrably needs stable record semantics beyond these (C04) |
| Capture retrieval attempts and misses | Steward RECALL/query-receipt guidance; receipt validator and summary | Confirm authorship/use frequency; distinguish query from application before adding any output (C14–C15) |
| Observe actual host execution | Host's native events when accessible; PR/Git/CI retained independently | Optional reference importer/export **if available**; cannot create missing past host events (C07/C08) |
| Connect decision and outcome history | Journey inspect/context/delta/impact-closure and Git/PR reader | Caller-selected read-only Git/receipt adapter might have a distinct user purpose (C05/C06); no automatic selection |
| Assess candidate adequacy and decision scope | Convergent method, Warrant/Choice, consequence depth, change-impact analysis | Optional retrospective challenge or decision-time critic, not a universal completeness validator (C09–C11/C16–C17) |
| Reconsider a deferred responsibility | Receipt predecessor refs, Warrant/Choice, learning/reconciliation | Stronger source-linked re-warrant continuity/readers only if normal sessions show failure (C12) |
| Preserve and reuse consequences | Steward RECONCILE, reviewed knowledge, strategic reconciliation, journey delta | Link lessons back to decisions and later applications without automatic causal inference (C13/C15) |
| Help independent reviewers challenge | Existing optional decision observability mode; PR/receipt/CLI inspection | A scoped read-only review experience is a distinct possible beneficiary, not an automatic privileged audit engine (C18/C19) |

Proposed operational novelty is conditional. A new **inspect** action for ordinary PR/receipt journeys might have a different consumer from current Campaign-oriented journey inspect; a new **host event import** action might require genuinely new cross-host data semantics; a **decision record query** might require indexed identity beyond the existing authored graph. Conversely, an additional action named after decision traceability that only concatenates existing notes is not a distinct capability.

## 10. Evidence boundaries, privacy and portability

1. **Chronology:** Git commit ancestry and PR timestamps support source/event order; they do not show the earlier state of a later-edited PR body unless that earlier version is independently retained.
2. **Reasoning:** contemporaneous authored rationale is self-report; source-grounded reviewer explanations are retrospective; neither reveals private internal cognition or demonstrates why model parameters produced a choice.
3. **Source exposure:** a source present in a repository at a revision was *available* in one sense, not necessarily loaded, read, comprehended or applied by the particular agent. A citation is not a tool event.
4. **Candidate absence:** no record of an alternative is **NOT DOCUMENTED**, not evidence it was never conceived. Even an event-rich stream cannot certify every internal alternative. A later challenger must identify its own assessed revision and hindsight.
5. **Semantic truth and authority:** receipts, decision records, index queries, journey projections, PR source review and green CI cannot certify original selection quality, external benefit or reserved permission. Historical decisions remain source-scoped.
6. **Sensitive events:** host prompts, tool arguments, credentials, private customer repositories and logged outputs may be confidential. Collect only authorized, necessary, appropriately redacted events; retain provenance and limitation of redaction.
7. **Host portability:** Git/PR provenance is broadly reusable but host-native event schema, retention, invocation and tool coverage vary. Do not promise uniform events, native Skill invocation or cross-host causality.
8. **Cost and interference:** more frequent checkpoints, longer explanations and independent critique consume context/effort and may change behavior. Competing mechanisms include selective capture and conditional activation; no universal mandatory reasoning diary is justified.
9. **Longitudinal benefit:** an inspectable decision may help later agents but does not prove they consulted or acted on it. Merged implementations and retrospective stories are insufficient to show durable knowledge improved decisions.

## 11. Open territory for the subsequent Coverage Assessment and Convergent Evaluation

**These are questions to hand off, not assessments already performed or product priorities.**

### Coverage Assessment

- **CA-Q1:** Does the landscape distinguish materially different **ends** (accountability, decision improvement, later reuse, reviewer contestability) and mechanisms, or are some entries merely variants of authored text?
- **CA-Q2:** Are decision-time authorship, host execution and retrospective interpretation represented without false equivalence, including when host evidence is permanently absent?
- **CA-Q3:** Could any proposed mechanism actually diagnose **option-set inadequacy** without pretending a missing option leaves a detectable historical event?
- **CA-Q4:** Is the affected beneficiary primarily autonomous agent, later agent, owner/reviewer or safety/compliance operator, and would that alter success conditions?
- **CA-Q5:** Do the existing conceptual ontology, v1/v2 reviewed-knowledge kinds, receipts and journey consumers already support each competency **faithfully** in some composition?
- **CA-Q6:** Which uncovered real source/consumer/host cases would change whether the current breadth is sufficient for convergence? Which omissions cannot be addressed without unavailable external host evidence?
- **CA-Q7:** Have source-version identity, authority, risk, privacy, context burden and portable delivery been examined proportionately, or is a materially different source of failure missing?
- **CA-Q8:** Is another divergent lens likely to change the **question or outcome**, rather than produce more near-duplicate trace formats? It is valid to conclude sufficient coverage.

### Convergent Evaluation (only after an independent coverage judgment)

- **CE-Q1:** For the current governing decision, which **specific competence and consumer** is underserved, and what independent product value would addressing it create?
- **CE-Q2:** Which options provide better **retained value at acceptable total cost** compared with composed existing actions, including legitimate no-change?
- **CE-Q3:** Is there any demonstrated need for new first-class typed data versus a documentary record with existing identity and reference semantics?
- **CE-Q4:** If read-only Git/receipt integration is considered, what does it answer that current journey inspect cannot, and what must it refuse to infer?
- **CE-Q5:** Which hypotheses concern **choice quality** rather than mere trace richness, and what normal-use evidence could discriminate them without inventing a benchmark now?
- **CE-Q6:** Under what stakes should a deliberative checkpoint or critic be activated, with what stop rule against process inflation?
- **CE-Q7:** How can later reuse be shown as more than record retrieval or authored attribution? What remain legitimate NOT_ASSESSED outcomes?
- **CE-Q8:** What authority, privacy, source-version and host availability conditions would make a particular future architecture **inadmissible**, irrespective of expected usefulness?
- **CE-Q9:** Which materially different possibilities conflict, complement or share prerequisites, and which remain genuinely incomparable without prematurely ranking them?

No final architecture, preferred candidate, new action, machine schema, score or implementation responsibility is selected by this report.

## 12. Source ledger and stopping boundary

**Repository evidence at main@28a7c1269ceace2fa2c7dff9e0a21a83c9783eb8:**

- [ADR 0029](../adr/0029-current-product-boundary.md), [ADR 0031](../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md), [product strategy](../product-strategy.md), [STATUS](../../STATUS.md), [CLAUDE](../../CLAUDE.md): governing intent, value, current stage, construction and authority.
- [Ontology](../semantic-architecture/ontology.md), [competencies](../semantic-architecture/competency-questions.md), [prospective ontology](../semantic-architecture/prospective-reasoning-ontology.md), [divergent ontology](../semantic-architecture/divergent-exploration-ontology.md), [convergent ontology](../semantic-architecture/convergent-direction-selection-ontology.md), [strategic learning](../semantic-architecture/strategic-evolution-learning-ontology.md): existing meanings and documentary roles.
- [Using Sensemaking](../../skills/using-sensemaking/SKILL.md), [divergent method](../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md), [Warrant/Choice](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md), [observability](../../skills/using-sensemaking/references/decision-observability-v1.md), [consequence depth](../research/consequence-depth-and-systems-reasoning-v0.md), [strategic loop](../../skills/strategic-sensemaking-loop/SKILL.md): current agent-owned guidance and boundaries.
- [Session receipt](../../skills/using-sensemaking/references/session-receipt-v1.md), [query receipt](../../skills/repository-semantic-steward/references/query-receipt.md), [artifact contracts](../../skills/workflow-planner/references/artifact-contracts.yaml), [validator](../../scripts/validate-receipt.py), [receipt summary](../../scripts/summarize-receipts.py): available authored persistence and some consumers.
- [Decision Journey product](../decision-journey-productization-v1.md), [journey implementation](../../src/sensemaking_skills/decision_journey_cli.py), [knowledge schema](../../src/sensemaking_skills/semantic_architecture/knowledge.py), [knowledge ingestion](../../src/sensemaking_skills/semantic_architecture/knowledge_sources.py), [query CLI](../../src/sensemaking_skills/semantic_cli.py): implemented operational projections and limits.
- Historical PR #812: [initial receipt at exact commit](https://github.com/ThorStarlord/sensemaking-skills/blob/7eb18a59ad14d19125063f95d445a5c5b1e4b48c/.sensemaking/receipts/2026-11-11-filter-safe-source-check.session.yaml), [implementation commit](https://github.com/ThorStarlord/sensemaking-skills/commit/2b2742c2de134d06f7f8298d9fe41920c2376328), [PR note](https://github.com/ThorStarlord/sensemaking-skills/pull/812), [final receipt commit](https://github.com/ThorStarlord/sensemaking-skills/commit/66fff7b973010fae776b50a4c80e360861714298), [integrated merge](https://github.com/ThorStarlord/sensemaking-skills/commit/1e198d6f8d0bf6769e220b7028ab7009debc012b). Those sources have distinct event times and claim ceilings.
- [Decision Observability Qualification preflight](../normal-use/decision-observability-qualification-001.md) explicitly reports NOT RUN for that proposed study. It is evidence of a preflight boundary, not comparative proof of traceability efficacy.

**Inspected limits:** GitHub history, canonical repository text and available source contracts were inspected. No arbitrary private host tool event stream, model internal deliberation, external affected-user interview or new independent agent task was available/used. Other repositories and hosts were not sampled for coverage; historical PR #812 is an authentic one-case reference, not a representative sample. No synthetic experiment was conducted.

**Substantive outcome:** preserved **19 distinguishable exploratory expressions across nine overlapping families**, plus a purpose-relative competency map, operational producer–consumer map, source-bound PR #812 account, candidate-adequacy distinctions, cross-family tensions and stage-specific follow-up questions. Candidate count is a description of this record, **not** a coverage sufficiency threshold.

**Stopping reason:** source-grounded differences are developed enough to permit a *subsequent* Coverage Assessment to judge novelty, omissions and diminishing returns. Another invented trace variant now would add little without changing the question; additional coverage is not presumed complete. **Coverage Assessment and Convergent Evaluation have not been performed.** No runtime, ontology, schema, receipt contract, host instrumentation or strategic authority has been changed.
