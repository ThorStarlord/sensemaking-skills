# Connected Prospective Inquiry v1 — Conditional Agent Reference

**Load when:** a bounded task needs **(a)** deeper consequences of a particular premise/possibility, **(b)** reconsideration of a source-attributed earlier comparison, **(c)** a targeted adversarial objection/response, or **(d)** a coherent product-and-technical design proposal from grounded intent and alternatives. Load only the relevant profile(s). This guide can serve standalone conceptual inquiry or a component of Strategic Repository Analysis or architectural work.

**Result:** source-grounded conditional consequence reasoning, an explained changed/unchanged judgment, target-grounded critique/response, or a traceable proposed design. Valid completion also includes no further meaningful consequence, unchanged preference, unresolved objection, no coherent proposal or an authority handoff. This is **not** a new public Skill, obligatory four-stage workflow, registered artifact, reasoning engine, automatic reranker or authorization.

**Portable promise:** operate from whatever target sources and user intent are actually accessible. The target **does not need** this framework's `CONTEXT.md`, ADRs, `.sensemaking/` directory, graph index, CLI, knowledge store or installed additional Skills. A reviewed index is an optional discovery aid, never the sole truth source.

## 1. Decide which question is actually open

| Actual uncertainty | Use | Do not confuse with |
| --- | --- | --- |
| "If X could be done, what follows and when would the chain fail?" | **Focused Depth Exploration** (`ConsequenceStructure`) | A generic list of implementation tasks or a proof of empirical causation |
| "Do these specific new effects change what we previously preferred?" | **Convergent Reassessment** (existing `AssessmentRevisionAccount`) | Automatic reranking, a new direction selection, or rewriting prior decisions |
| "Which exact claim/design would fail, why, and how would we respond?" | **Adversarial Review** (`ChallengeResponseAccount`) | Automatic critic veto, a presumed software defect or repair verification |
| "How do the intended product outcomes, requirements and technical responsibilities fit together coherently?" | **Architecture Synthesis** (`DesignRationaleView`) | Multi-option `architectural_synthesis` alone, a new PRD producer, implementation approval |

The active agent **chooses the warranted responsibility before any procedural detail**. If the task is a direct authorized local edit with sufficient evidence, do it and stop; do not summon these profiles for ceremony. If the task remains divergent, use appropriate exploration guidance instead of selecting a design. A profile may follow another, return to an earlier question, or be used alone.

### Shared source discipline (short, without a form)

Record when material: actual user question and intended beneficiary; actor/date/scope and any protected authority; original typed target and original IDs; source path and assessed target revision; earliest relevant predecessor judgment; observed premises; hypothetical mechanism with its conditions and counterevidence; new conclusion and its alternatives; which decision it could change; what remains unresolved; reason for stop/re-entry.

Preserve source-observed facts, deductive conditionals, causal hypotheses, creative possibilities, attributed judgments, real decisions, authorized work and verified outcomes separately. A source change can make a fact stale without changing its historical correctness. A graph miss means **not assessed in that graph**, not that the product lacks the relation. Read decisive original sources.

A `ProductPossibility` is a possible future end, not a proposed component or work order. An `ArchitectureOption` / `ConstructionPath` remains proposed. A `ConsequenceHypothesis` remains conditional. A `ProvisionalPreference` is not a `Decision`. One target can be considered by many activities while keeping its original identity. A grouping is not `sameAs`.

## 2. Focused Depth Exploration — if X, what follows?

**Trigger:** a particular source-grounded premise, prospective capability or relationship can change a meaningful product/architecture/strategy assessment, but its downstream consequences are too shallow to decide the next question.

**Do this:**

1. State **the specific conditional world**, source/assessed revision, context/horizon, affected beneficiary and closest existing alternative. What would it mean for X to hold, fail or be unavailable?
2. Trace the **first direct effect**. Distinguish an implication under stipulated premises from a possible behavior and from an *observed* outcome.
3. Follow only decision-relevant **second-order and systemic interactions**. For each link name the mechanism, assumptions and possible blockers. Include cross-boundary effects, option loss/gain, feedback and maintenance when consequential; do not count layers for their own sake.
4. Examine **counterfactual forks** that materially change conclusions (owner authority, unsupported user value, consumer absence, source-only agent success, environment changes, beneficiary conflicts). Include benefits and harms from affected perspectives; avoid an artificial branch count.
5. Ask whether a consequence exposes a **genuinely different desired end**, a familiar end through a different mechanism, an alternative future question, or nothing new. Keep a non-adopted possibility hypothetical unless separately curated under actual policy.
6. State **what is knowable**, what is hypothetical, what evidence would change the judgment, and why additional consequence depth is or is not worth pursuing.

**Useful output:** a short `ConsequenceStructure` in the task report: target/premise; direct consequence; 1-2 material downstream links if real; assumptions/causal bridges; non-effects or divergent forks; beneficiaries/tradeoffs; possible opportunity; undecided grounds; stop. More detail only when the actual decision warrants it.

**Failure to avoid:** `A may produce B` + `B may enable C` does **not** establish "A causes C"; the effect may not exist, B may be merely enabling, and C may lack demonstrated value. Do not assign an `arch:`/`conseq:` identity to general prose just to populate a graph, or widen the architecture/path-specific `mayProduce` endpoints. No mandatory experiment follows from a lack of measured effect.

**Stop when:** the decisive chain has a reasoned extent; a crucial premise/actor is absent; further branches would not change the judged target; or an empirical ceiling prevents stronger causal claims. `NO_FURTHER_DEPTH` is descriptive prose here, **not a new enum**.

## 3. Convergent Reassessment — do new consequences change preference?

**Trigger:** a **specific earlier judgment, comparison or portfolio** is decision-relevant now and a new consequence, changed assumption, observation or owner purpose might alter its grounds.

**Do this:**

1. Identify the *exact predecessor*: author/date, source and assessed revision, original typed operands, beneficiary/purpose, criteria and any previously unassessed/incomparable alternatives.
2. Name **what is new** relative to the old frame and how it affects a concrete criterion, prerequisite, value mechanism or applicability condition. A newer document or richer explanation alone is not evidence of changed preference.
3. Ask whether the **same question** is being answered. Inquiry-learning priority, attractiveness of a future product, and implementation order are separate assessments. If the purpose changed, compare only with an explicit new frame and avoid pretending an ordinal reversal.
4. Record a sourced **AssessmentRevisionAccount** in the existing report/decision surface: predecessor, new grounds, changed/unchanged judgment, unaffected members, counterarguments, reversal conditions and status. Appropriate outcomes include *same preference, new rationale*; *same preference, narrower applicability*; *local pairwise reorder*; *incomparable*; *no change*; *more evidence needed*; or **actual decision reconsideration only with its proper actor/authority**.
5. Keep historical snapshots intact. A pairwise preference does not become a global total order. Never infer owner adoption, a strategic thesis change or authorized execution from an assessment.

**Useful output:** "Originally A preferred to B for [purpose] because [source]; new consequence C depends on [premise]; therefore [same/narrowed/changed/incomparable] under [conditions]; others [unchanged/not assessed]; this does/does not reopen an actual decision; stop/next hinge." In low-stakes work, one paragraph suffices.

**Failure to avoid:** unfamiliar new information may affect a mechanism but not the previously evaluated product goal; do not rerank simply to be "responsive." If existing policy reserves the decision for the owner, present options and bounded evidence, not an invented selection.

**Stop when:** no decision-relevant change is supported, the narrow modification is explained, or the remaining decision depends on genuinely missing evidence/authority.

## 4. Adversarial Review — exactly where could it break?

**Trigger:** the consequence, inference, comparison, proposed contract, architecture, selected action, user requirement or work-closure claim has material downside, conflicting source evidence, an unverified bridge, hidden consumers or weakly supported certainty.

**Do this:**

1. Name **one exact target** with its original source/ID/revision. Critique the proposition actually being made, not a plausible but unrelated straw man.
2. State the challenge as an **evidence- or premise-qualified failure path**: observed counterevidence, hypothetical fault mode, incomplete source/consumer, incorrect applicability, changed assumption, rival interpretation, violated constraint or missing authority. Separate current fact from scenario.
3. State **impact if true**: would the challenge negate an effect, narrow a comparison, disrupt a component contract, harm a beneficiary, or prohibit a protected action?
4. Answer with a **rebuttal grounded in source**, accepted defect, narrowed claim, modified proposal, explicitly tolerated risk, bounded inquiry, or unresolved uncertainty. A solution idea must address the *original* weakness; a changed design can create a new consequence.
5. Preserve a **ChallengeResponseAccount**: target, challenge/grounds, response/grounds, unresolved issue, warranted correction/inquiry and verification needed for any claimed repair. Hand evidence back to the active agent; a critic does not own the final authority.

**Useful output:** a few source-linked objections with substantive responses, or one decisive objection. Prefer depth on material failure mechanisms over a large enumeration of generic threats.

**Failure to avoid:** a conjectured failure is **not** an observed defect. A source-review rebuttal is **not** a successful deployed repair. A finding is not permission to modify code. A missing graph edge is **not** proof that a system component lacks a consumer. If reviewing concrete architecture through an available `architectural-review` Skill, preserve that Skill's actual input requirement (`repository_sensemaking_brief` plus concrete `proposed_direction`); this guide is not a substitute.

**Stop when:** significant objections have supported disposition and limits, or actual verification/owner evidence is needed before the agent could claim more.

## 5. Architecture Synthesis — a coherent product-and-technical proposal

**Trigger:** the goal and scope are grounded and the current decision calls for a coherent proposed solution rather than further unconstrained possibility generation. Option comparisons, consequence analysis and meaningful critique inform this proposal, but need not be redone when already adequate.

**Do this:**

1. **Purpose:** identify source user intent, beneficiary, desired experience/outcome, non-goals, acceptance questions and needed authority. Separate user requirement from an agent-invented desirable extension.
2. **Requirement view:** describe what behavior should exist, why, evidence and unknown baselines. For a **canonical PRD artifact**, use the existing `to-prd` capability **if installed/available and warranted**, preserving its `source_intent_ref` and scope-expansion authority. The core entrypoint-only installation does not guarantee the optional product-management PRD Skill is present; do not pretend the produced prose is the canonical `prd` when its producer is unavailable.
3. **Architecture alternatives:** reuse prior source-grounded option comparisons. If a durable *multi-option* comparison is needed, use the current `architectural_synthesis` contract and architecture-exploration producer, **not** a new freeform substitute for its machine-readable fields. A provisional preference is still not an adopted architecture.
4. **Technical design view:** propose coherent responsibilities, boundaries, components, dependencies, interfaces/data/control paths, adaptation/migration and failure behavior appropriate to the target's observed structure. Use repository-native prose/spec unless a real existing design artifact producer is applicable.
5. **Traceability:** for material design elements explain `beneficiary/outcome -> requirement/constraint -> technical responsibility/contract -> expected consequence -> assumption/evidence -> relevant challenge/response`. State accepted tradeoffs and non-selected alternatives.
6. **Coherence check:** look for contradictory requirements, two owners for one responsibility, contracts with no consumer, unintended authority transfer, false evidence claims, unbounded changes and unaddressed material harms. No implementation or verification is implied by coherence.
7. **Approval and continuation:** record explicitly what is proposed, what an authorized actor has selected (if anything), what requires owner approval, and whether a separate engineering plan/build is warranted.

**Useful output:** a `DesignRationaleView` in a proposal/PRD+technical-spec set, or a short section linking existing artifacts. If no coherent design is warranted, preserving alternatives/open premises is valid completion. Never manufacture an `architecture_spec` artifact ID or register a stage without a real producer/consumer.

**Failure to avoid:** a structurally detailed spec with no beneficiary/end/requirements is not an adequate product solution. A PRD target metric is not measured baseline; a plan is not implementation; a preference is not a selecting actor; owner-approved product scope is not inferred from a diagram.

**Stop when:** an intelligible internally consistent *proposal* is reconstructible and its remaining evidence, authority and build boundaries are stated—or when a decisive unknown blocks further design. Do not auto-build.

## 6. Integration and proportional return

If several profiles are used, connect them **by explicit evidence and source-qualified questions** rather than a fixed controller:

```text
source / original possibility / proposed architecture
   -> (if useful) conditional consequence structure
   -> (if consequential) earlier preference reconsideration
   -> (if risky/contested) exact-target challenge and response
   -> (if coherent design is warranted) requirement + technical rationale
   -> any new consequence, uncertainty or alternative returns as evidence
   -> active agent decides next responsibility under actual authority
```

**No mandatory stage progression.** Depth may happen after a design revision. Adversarial review may be the entire task. Reassessment may end `NO_CHANGE`; synthesis may stop at options. The [optional record template](connected-prospective-inquiry-record-template.md) is only for cross-session work where ordinary source-linked prose would lose material reasoning. It is not a machine schema and does not replace a real PRD, `architectural_synthesis`, strategic artifact or receipt.

**Portable crosswalk:** when installed, `divergent-exploration-v1.md` handles expression/frame breadth; `possibility-assessment-v1.md` handles coverage and purpose-relative portfolios; `convergent-direction-selection-v1.md` handles actual choice/warrant. This guide covers the *consequence/reassessment/challenge/design* distinctions without repeating those separate responsibilities.

**Evidence ceiling:** valid source citations and consistent proposed explanations establish **documentary fidelity**, not improved independent creativity, automatic causal inference, better owner choices, proved user value, host loading/Skill invocation or deployed functionality. `installed != loaded != invoked != applied`. A later genuine task or observation may warrant further qualification, but don't run a contrived experiment because the guide exists.
