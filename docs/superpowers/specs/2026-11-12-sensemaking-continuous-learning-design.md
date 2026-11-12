# Sensemaking Continuous Learning (SCL) — Product Design v0

**Date:** 2026-11-12
**Status:** owner-endorsed proposed product direction; planning, **not implemented behavior or ratified new ADR**.
**Assessed repository:** `ThorStarlord/sensemaking-skills@3a5658b58029535dd5400388343cac8e760c3468`. Recheck current `main` before execution.
**Companion:** [SCL development plan](../plans/2026-11-12-sensemaking-continuous-learning.md).
**Existing authority:** [product strategy](../../product-strategy.md), ADRs [0029](../../adr/0029-current-product-boundary.md), [0031](../../adr/0031-persistent-semantic-stewardship.md), [0034](../../adr/0034-ontology-first-adaptive-sensemaking.md), [Level-4 contract](../../product-thesis-revision.md), [Capability Learning Loop v0](../../research/capability-learning-loop-v0.md), [Learning/Reconciliation](../../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md).

## 1. Desired end

**Sensemaking Continuous Learning (SCL)** is the proposed first-class capability through which ordinary engineering work contributes to progressively better, source-grounded understanding of a product and better context-sensitive engineering judgment across sessions, agents and repositories.

The owner favors deliberate learning from **every engineering episode**. Interpret "every" as **every in-scope observable episode is eligible for lightweight learning consideration**, not "persist a new lesson or modify doctrine every time." This protects the intended user end: better subsequent decisions, not more records or compulsory reasoning ceremony.

### Beneficiaries

- **Current agent:** revise a mistaken premise or method choice without needlessly halting construction.
- **Fresh successor:** retrieve relevant experience at a future decision and recognize when it does not apply.
- **Repository/product owner:** inspect evidence, limits and effect on product outcomes.
- **Other repository (when explicitly authorized):** use experience as an analogy, without transferring the originating repository's authority.
- **Sensemaking maintainer:** qualify bounded reusable method improvements from comparable independent episodes.

No model-weight training, capture of private reasoning or automatic Git/Skill mutation is implied.

## 2. Baseline and actual gap

Existing work is substantial. [Longitudinal Engineering Learning](../plans/2026-11-02-longitudinal-engineering-learning.md) and PRs #702–705 already provide source-linked lesson records, owner-to-lesson reachability through `context-for`, agent-facing RECALL/applicability guidance and a scoped cross-episode lesson candidate. The [knowledge CLI](../../semantic-architecture/persistent-knowledge-cli.md) builds an exact-source, read-only SQLite projection. [Capability Learning Loop v0](../../research/capability-learning-loop-v0.md) names responsibility and repository learning and a proposed capability-learning loop. [Adaptive methodological exploration](../../explorations/2026-11-12-adaptive-methodological-learning-divergent-exploration.md) expresses open possibilities, not observed method improvement.

The unqualified end-to-end transition is **retained evidence -> decision-time encounter -> source-qualified use/rejection -> supported future improvement**. Source and CI evidence does not establish routine independent agent adoption or comparative benefit. Do not rebuild already delivered retrieval solely to create an SCL-branded module.

## 3. Alternatives and selected architecture

| Alternative | Strength | Counterpressure | Disposition |
| --- | --- | --- | --- |
| A. Continue only opportunistic episode learning | Low ceremony | No deliberate end-to-end continuity; ordinary episodes can be missed | Insufficient |
| **B. Continuous eligibility, selective retention, decision-time reuse** | Extends actual source-backed work without a second controller | Requires reliable encounter feedback, counterevidence and overhead discipline | **Selected design recommendation** |
| C. Universal automatic `LearningEngine` that extracts, ranks and revises doctrine on every event | Possible processing coverage | Unwarranted attribution, noise, duplicated authority and self-reinforcing errors | Deferred |

"Explicit product capability" means an intentional, discoverable and independently assessable outcome. It does not require an automatic learning process or new artifact kind.

### Learning unit

An **engineering episode** is actual authorized work with a reconstructible question/responsibility and a result (action, investigation, construction, review, strategic reassessment, or justified nonaction). Hypothetical examples and idea generation do not by themselves establish engineering-learning benefit.

An **experience** is what happened at the original source/revision. A **lesson candidate** is a source-attributed *interpretation* of that experience, with applicability limits. A **reusable methodological rule** is a later separately reviewed, authorized and qualified guidance change.

Every observable episode is an opportunity for the cheap question: **Did the result revise a consequential claim, falsify an assumption, change an uncertainty/responsibility, or suggest a potentially transferable lesson?** NO_CHANGE and no extra artifact are acceptable outcomes. Preserve material learning in the narrowest existing owner surface: PR/history, receipt, Campaign/handoff, strategic reconciliation, source-linked knowledge record or a bounded normal-use record.

### Two dimensions of learning

- **Product knowledge:** purpose, domain, behavior, architecture, decisions, constraints, evidence, opportunities, consequences.
- **Methodological knowledge:** when ACT, INQUIRE, CHALLENGE, EXPLORE, VERIFY, ESCALATE or STOP was useful, when it failed, what evidence it made visible and why it should not be copied elsewhere.

One episode may support either, both or neither. The two dimensions share provenance and reconciliation but must not collapse product facts into method preferences or method patterns into product authority.

### Evidence ladder (descriptive, not a new machine enum)

1. Original episode evidence exists.
2. An interpretation was retained.
3. A later distinct actor encountered it **before** a consequential choice.
4. That actor verified origin/current sources and considered context, limits and contrary evidence.
5. The actor used, adapted **or justifiably rejected** the lesson while deciding.
6. Returned engineering evidence supports or challenges that decision.
7. Independent reuse and, when needed, credible comparative benefit are established.

Do not claim a higher rung from a lower one. A `context-for` hit or passing CI is not evidence of better reasoning.

## 4. Proposed flow and product seams

```text
NORMAL ENGINEERING EPISODE
  -> cheap learning eligibility / Learning-Reconciliation
  -> [only if consequential] source-attributed episode interpretation
  -> narrowest existing durable owner; no generic dump
  -> [later decision] situation-aware recall and original-source verification
  -> use / adapt / reject / no applicable precedent
  -> engineering action or justified nonaction
  -> observed results; feedback on historical lesson applicability
  -> [when independent episodes justify] bounded doctrine candidate
  -> governed review, qualification, possible Skill/reference revision
  -> later ordinary use
```

**Entry point:** `using-sensemaking` remains the single public semantic controller. **Recall:** existing Repository Semantic Steward guidance and source-pinned `semantic knowledge-query` / `context-for`. **Memory:** authored Git source is authority; SQLite is a rebuildable derived index. **Feedback:** Learning/Reconciliation and narrow repository-owned durable records. **Future Skill / parsed schema:** only if real consumers repeatedly demonstrate a stable unserved responsibility.

## 5. Trust, safety and performance boundaries

- **Origin:** exact repository, source and commit, observed act distinct from hindsight interpretation.
- **Retention:** where knowledge survives, currentness and actual later retrieval.
- **Applicability:** current task, goal, risk, reversibility, environment, source changes, counterexamples.
- **Authority:** local owner intent and current repository policy govern; foreign lessons transfer information, never permission.
- **Privacy:** no private chain-of-thought, secrets, credentials or indiscriminate external-repo ingestion.
- **Selection bias:** verification can detect *more* problems without causing more problems; exposure and measurement depend on methods.
- **Economy:** learning must not create mandatory post-task documentation, repeated prompts, memory inflation or automatic extra investigations.
- **Uncertainty:** missing original trace, stale index, unavailable external executor or inadequate comparator are reported as unassessed/blocked.

## 6. Acceptance and future evolution

**First real product increment:** demonstrate, within ordinary authorized engineering, that an independent later agent can encounter a relevant retained lesson before choosing an action and use or reject it with source-backed reasons. When only archival or retrospective evidence exists, describe the lower evidence ceiling honestly.

**Then:** close the loop with consequential later-episode feedback; preserve a corrected/contested historical interpretation without destroying the original record. Require independently comparable episodes and counterevidence for broad method changes.

**Outcome measures:** fewer material rediscoveries, better justified responsibility selection, reduction of repeated false assumptions/rework, improved source and authority adherence, and acceptable total learning overhead. Do not optimize record count, retrieval hit count or reflections per task as substitutes.

**Later conditional opportunities:** deliberate cross-episode synthesis, targeted skill/reference improvements, safe cross-repository transfer, human-readable learning explanation, and eventually mechanized assistance at a proven narrow seam. An automatic extractor, background monitor or generalized learning engine requires a separate warrant, governance and safety decision.

The owner accepted the direction conversationally; this design does not silently change `docs/product-strategy.md` or an ADR. A canonical Level-4 ratification uses `docs/product-thesis-revision.md` and an explicit owner-authorized update, separate from product construction and empirical qualification.

