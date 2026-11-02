# Longitudinal Engineering Learning — construction and evidence plan

**Date:** 2026-11-02. **Status:** owner-authorized Level-3 construction continuation, with separate qualification evidence gates.
**Baseline:** `ThorStarlord/sensemaking-skills` `main@8e323641df00dc358c6ac82ec82ec27f3e7b4a1f`.
**Authority:** ADR 0029/0031/0034, accepted PATH-1, `CLAUDE.md` construction/merge policy; no Level-4 rewrite.

## Product outcome and decision

A later coding agent confronting consequential engineering uncertainty should find source-linked relevant prior experience, critically check its applicability, use or reject it in an actual engineering decision, and retain subsequent corrections for still-later agents. **Selected:** agent-native, situation-aware, case-based longitudinal engineering learning; no `LearningEngine`, mandatory memory lookup, automatic Skill mutation, lesson ranking or new semantic controller.

Distinguish (A) current responsibility learning, (B) durable target-repository learning, (C) evidence-gated cross-episode capability learning. Loop C does not become canonical implementation simply because A/B work. A lesson retained or retrieved does not prove it helped, and a later anecdote is not a causal or comparative result.

## Baseline: existing real learning evidence

- `.sensemaking/knowledge/stewardship.json`: six authored `lesson` claims including `lesson:query-completeness-is-evidence`, `lesson:uncited-change-is-coverage-gap`, `lesson:distinguish-provenance-content-and-meaning`, `lesson:installed-skill-currency-includes-references`, `lesson:console-guard-literal-print-arguments-only`, `lesson:grounding-waiver`; some explicit `learned_from` relations. Each lesson's original source and revision bound must still be checked before use.
- `skills/repository-semantic-steward/references/recall.md`: current literal `search`, `explain`, revision-aware `context-for`, source-only fallback, bounded `history`; already expressly supports cross-session learning questions, not a mandatory lookup stage.
- `skills/using-sensemaking/references/ontology-first-entry-v1.md` section 4 and `learning-reconciliation-policy-v0.md` section 13A: longitudinal evidence classes and cross-episode generalization/authority boundaries already exist.
- `docs/research/capability-learning-loop-v0.md`: Loop C is conceptually supported and evidence-gated. `poss:capability-learning-analysis` remains deferred. Do not create an additional Skill without repeated stable normal-use need.
- `docs/normal-use/operational-qualification-001.md`: one qualitative returning/source-only pair supports narrow consequential knowledge reuse, with complementary gaps and a separately observed authority-adherence failure. It does not prove replicated benefit, broad transfer or causal superiority.
- `component:knowledge-store` in `.sensemaking/knowledge/stewardship.json` owns `knowledge_store.py` and `knowledge_retrieval.py`; source inspection at this baseline finds no explicit `references` relation connecting its source-owner node to the two relevant query lessons. The existing `context-for` implementation admits history only through explicit owner/rule links. This is a **source-inspected reachability candidate**, not a previously executed baseline-query failure.

## Work program (warranted, not a fixed runtime sequence)

| WP | Responsibility | Intended useful output | Evidence / boundary |
| --- | --- | --- | --- |
| 0 | Preserve Level-3 continuity and reviewed baseline | Source- and SHA-grounded continuation | Current product thesis unchanged |
| 1 | Ask longitudinal competency questions CQ-115..130 | Identify actual guidance/coverage/consumer gaps | No automatic new schema |
| 2 | Source-verify existing lesson origins, scope, file ownership | Reconstructible relevant historical cases | Sparse/uncited != absent |
| 3 | Selective situation-aware lesson recall | Ordinary agent can find prior lesson when decision-relevant | No routine compulsory lookup |
| 4 | Applicability/adversarial challenge | Apply, narrow, or reject historical lesson for sourced reasons | Similarity != transfer |
| 5 | Authentic new engineering use | Normal-use result with observed decision effect | A self-review is not a fresh independent coding agent |
| 6 | Reconcile lessons into reviewed memory | History and corrected interpretations coexist | No automatic truth/authority promotion |
| 7 | Compare materially similar independent episodes | Bounded recurring-pattern analysis, including counterexamples | Repeated symptoms != common cause |
| 8 | Qualify smallest reusable guidance change | Real improvement in existing reference/contract | Cross-episode doctrine requires appropriate warrant |
| 9 | Revisit/supersede stale lessons | Current applicability without erasing historical sources | Changed file != changed meaning |
| 10 | Independent R6/R7/S5 use/comparison | Real separately loaded coding-agent decision evidence | CI / same-context replay != independent learning |
| 11 | Separately authorized repository transfer | Target-verified analogy, not foreign authority | No implicit other-repository mutation |
| 12 | Reconsider a dedicated learning Skill only after repeated stable need | Optional small specialist responsibility | No autonomous policy/Skill self-edit |

## Selected first vertical

**Actual question:** An agent editing the semantic knowledge query store asks which prior query-completeness, source-coverage, or provenance lessons could change its approach. Starting from the real source file (not a hard-coded lesson ID), can the existing `context-for` query return the owning component and a directly relevant source-linked lesson?

1. Inspect the actual `component:knowledge-store` owned paths and the historical lesson/incident sources. Do not infer an unexecuted query failure.
2. If the reviewed owner-to-lesson relationship is missing, add only the accurate explicit edges with both original episode and implemented-source provenance. Preserve epistemic status; no new type or query.
3. Make a bounded optional guidance improvement, if existing RECALL and reconciliation text do not already cover applicability, counterevidence and rejection adequately.
4. Use the *existing* source-pinned hosted Semantic Context Re-entry consumer for a real exact-head `context-for` query. Its output proves retrieval mechanics and asserted graph links only, not application by an independent coding agent.
5. In any genuine follow-on task, re-warrant the next action from current sources, observe whether the lesson changed the agent's reasoning, and reconcile only actual consequential learning.

## Concrete PR boundaries

- **PR-A:** baseline/program and CQ-115..130, existing ontology fit, source-inspected retrieval question.
- **PR-B:** minimal optional situation-aware RECALL / applicability / learning-feedback guidance; no second controller.
- **PR-C:** source-grounded lesson graph reachability correction plus one actual exact-head CLI CI consumer; only if relevant links are truly missing.
- **PR-D:** bounded cross-episode historical analysis of real comparable cases; retain one repository-local candidate when only overlapping self-repository evidence exists, and require genuinely independent corroboration before broader doctrine or cross-repository transfer.
- **Later conditional PRs:** reusable guidance or retrieval code only for observed consumer need; independent qualification only from actual independent host; cross-repository only with explicit authority.

## Qualification ladder and completion

Distinguish retention, retrieval, source verification, semantic applicability, consequential decision use, fresh independent-session correction, comparative improvement and cross-repository transfer. Each requires its own evidence. Existing `knowledge-proposal-check`, source-pinned index and `context-for` can validate representation and retrieval. They cannot validate an agent's cognition. Under `CLAUDE.md` construction policy, local unit/synthetic tests are `NOT_RUN`; retain hosted CI/protections, review exact source/diff, merge within explicit owner policy. Repair actual hosted failures rather than attributing them to unrelated work.

**Initial done:** source-verified, reachable lessons and optional applicability guidance integrated without new infrastructure. **Longitudinal done:** a later genuinely independent agent applies, narrows, or rejects prior knowledge in a material real decision; report `NOT_EXECUTED` until such an executor actually runs. **Strategic result:** improve accumulated engineering judgment, not merely increase node count.

## Risks and stopping boundaries

Memory inflation, historical anchoring, false transfer, causal overclaims, stale lessons, authority laundering, process-only busywork and verification theater are real risks. Prefer selective source inspection and reversible capability work. No universal append-only `LEARNINGS.md`, automatic lesson extractor, idea scorer, policy router or mandatory lesson lookup. Stop at lack of warranted productive work or a genuinely unavailable independent agent/authority boundary; do not pretend that a CI run crossed it.

## Construction return / evidence reconciliation (2026-11-02)

| Increment | Integrated repository result | Verification and remaining uncertainty |
| --- | --- | --- |
| [#702](https://github.com/ThorStarlord/sensemaking-skills/pull/702) | Plan and CQ-115..130 | Source/diff reviewed; no new runtime, graph schema or mechanical qualification claim |
| [#703](https://github.com/ThorStarlord/sensemaking-skills/pull/703) | Optional source-verified historical recall and lesson applicability/rejection feedback in existing Steward/using-sensemaking references | Agent-facing guidance; not a separately demonstrated host behavior |
| [#704](https://github.com/ThorStarlord/sensemaking-skills/pull/704) | Three lesson relationships from the existing query-store owner plus a real two-file `context-for` consumer | [Run 41480135285](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41480135285) passed at exact PR head `c74c3e68`; no independent agent performance claim |
| [#705](https://github.com/ThorStarlord/sensemaking-skills/pull/705) | One scoped local incident and lesson connected by `learned_from` and two source owner references; cross-case counterevidence retained | [Run 41480921119](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41480921119) passed at exact PR head `86bfc959`; repeated benefit and transfer NOT_ASSESSED |

**Current assessment:** initial WP-0..4 source/competency/guidance construction and narrow WP-6/7/9 reconciliation were performed. WP-5/10 authentic later-agent learning and independent comparative benefit remain `NOT_EXECUTED` from this GitHub-connector session, not implied by CI or the same-agent source review. WP-8 generalized reusable doctrine, WP-11 cross-repository change, and WP-12 dedicated `capability-learning-analysis` Skill were **not promoted**, because the available evidence/authority does not warrant them. The local lesson is not an automatic future work item.

**Decision trace:** source-grounded owner/history links plus optional agent guidance created immediate valuable retrieval while also generating exact-head mechanical evidence. A docs-only plan would leave the reviewed file-first history gap open; a new learning runtime, new ontology predicate, or automatic doctrine engine would add unwarranted maintenance and authority risk. Preserve ADR 0029/0031/0034 and PATH-1. Future work begins from current source and a real engineering question, not from this table as an automatic queue.
