# ADR 0035: Sensemaking Continuous Learning as a First-Class Product Capability

**Status:** ACCEPTED — owner-selected direction recorded on 2026-11-12; implementation and independent benefit remain separately unqualified.
**Date:** 2026-11-12
**Level:** 4 — Product Thesis / Strategy Revision
**Disposition:** REINTERPRET/EXTEND the compounding-knowledge outcome of ADR 0031; preserve ADR 0034's single semantic controller and ADR 0029's protected product boundary
**Authority:** direct owner direction in the 2026-11-12 discussion: continuous learning should become an explicit capability; learn deliberately from engineering episodes; accept the proposed selective-retention architecture; implement the detailed plan autonomously within existing scope. The present ADR records that choice rather than inferring it from a coding agent.
**Affected strategy:** [product-strategy.md](../product-strategy.md); [revision contract](../product-thesis-revision.md).
**Implementation basis:** [SCL design](../superpowers/specs/2026-11-12-sensemaking-continuous-learning-design.md); [SCL plan](../superpowers/plans/2026-11-12-sensemaking-continuous-learning.md).

## Context and owner selection

[ADR 0031](0031-persistent-semantic-stewardship.md) already chose persistent semantic knowledge and reasoning as Sensemaking's destination, including the hypothesis that knowledge should compound across agents and time. [ADR 0034](0034-ontology-first-adaptive-sensemaking.md) made ontology-grounded understanding and prospective reasoning, with `using-sensemaking` as the sole public semantic controller, the product identity. The [Capability Learning Loop v0](../research/capability-learning-loop-v0.md) described responsibility and repository learning as canonical guidance; higher-order capability learning was a candidate extension without a runtime.

The owner asked that learning from ordinary engineering work become an **explicit, first-class product capability**, not only an occasional favorable consequence of other workflows. The proposed name is **Sensemaking Continuous Learning (SCL)**. The owner accepted a design in which all *observable, in-scope* engineering episodes are eligible for cheap learning consideration, but only consequential, source-grounded knowledge is retained. This is an explicit owner commitment to a *product end*, not an empirical assertion that the end has already been realized.

## Decision

1. **Explicit capability:** SCL is an intended product capability within Persistent Semantic Stewardship, spanning product/domain knowledge and the adaptive effectiveness and limitations of Sensemaking's own reasoning methods.
2. **Every episode eligible:** a real completed, blocked or otherwise observed engineering episode offers a low-cost opportunity to reconsider important claims, assumptions, uncertainty, responsibility, or method applicability. A trivial outcome may remain an implicit `NO_MODEL_CHANGE` without a new artifact.
3. **Selective durability:** retain lessons in the narrowest existing authoritative Git-reviewed or execution evidence surface when future reuse matters. Do not create a central append-only learning dump, new mandatory transcript, arbitrary experience score, or blanket "learned" claim.
4. **Decision-time continuity:** a later agent should be able to discover relevant earlier experience from current task context or question, verify its original source and current applicability, and use, adapt or justifiably reject it before deciding. History and interpretation are distinct.
5. **Feedback and correction:** actual subsequent results may confirm, narrow, contest, supersede or leave unchanged an earlier lesson, without deleting original observations or importing a past actor's authority.
6. **Higher-order capability learning:** comparable independent episodes may warrant bounded revisions to existing Skill/reference/runbook guidance, qualified by counterevidence, provenance and a later real consumer. Such revisions remain reviewed and authorized, not automatic.
7. **Single controller:** `using-sensemaking` remains the semantic decision maker; current Learning/Reconciliation and repository Steward RECALL are reused. There is no independent SCL controller, new policy hierarchy, automatic cognitive-mode ranker or universal learning runtime.
8. **Authority and epistemics:** current owner intent and repository scope govern; a transferable lesson transfers information, not permission. Source-index presence, retrieval, use, outcome and comparative improvement are separate levels of evidence.

The product goal favors progressively better engineering judgment, not maximizing the number of recorded lessons or doctrine edits.

## Alternatives and rejected interpretations

- **Leave learning implicit/opportunistic:** minimal footprint but underspecifies the owner's deliberate continuous-learning objective.
- **Mandatory lesson artifact on every task:** mechanically visible, but inflates memory, overhead and false positive claims, and risks replacing useful construction with ceremony.
- **Automatic cross-episode method extraction and self-modification now:** would presume causal generalizations, duplicate existing controller/authority and exceed demonstrated consumer need.
- **Chosen:** deliberate episode eligibility with selective evidence-grounded retention and re-entry, eventually qualified adaptation and optional automation where warranted.

## Implementation and qualification boundaries

- Existing foundations include the [Longitudinal Engineering Learning plan](../superpowers/plans/2026-11-02-longitudinal-engineering-learning.md) and PRs #702–705 (reviewed lessons and path-oriented retrieval). Do **not** rebuild them to rename the capability.
- [PR #832](https://github.com/ThorStarlord/sensemaking-skills/pull/832) added an optional exact-kind filter to historical question searches; it is a retrieval implementation, not evidence of autonomous learning.
- [PR #833](https://github.com/ThorStarlord/sensemaking-skills/pull/833) made every observable episode eligible for cheap learning consideration through the existing agent-facing policy; it is guidance, not independently verified agent behavior.
- The [SCL program](../superpowers/plans/2026-11-12-sensemaking-continuous-learning.md) stages decision-time reuse, feedback, default coverage, cross-episode synthesis, guarded transfer, comparative outcome evidence and conditional mechanization. Its tasks are conditional responsibilities, not automatic permission to invent a test episode, deploy an engine, or claim independent benefit.
- No model-weight training, autonomous Skill edit/merge/release/deploy/publish, second controller or cross-repository write is authorized. Such protected transitions require their own review and authorization.

**Evidence ceiling:** source and code changes show which queries/guidance exist at reviewed revisions. Independent predecision lesson exposure, consequential use, repeated benefit, causal improvement and general cross-repository transfer remain OPEN / NOT QUALIFIED until observed through an appropriate real later agent and source evidence.

## Level-3 reconciliation

The existing PATH-1 strategy of improving reviewed semantic knowledge through genuine engineering responsibilities remains compatible. The SCL objective is a purpose/beneficiary clarification, not a command to execute a fixed backlog or a reason to reopen the entire Strategic Exploration Funnel. Reassess concrete responsibilities against current code, prior source and value; preserve independent-agent and release qualification as separate gates. If evidence later shows that the selected learning approach harms decisions, correct or retire the method rather than defend this ADR through learning activity volume.

## Owner ratification

The owner explicitly selected the SCL direction and the proportionate, evidence-based approach in conversation on 2026-11-12, then requested implementation without further per-task approval. This ADR records the owner-supplied end and repository-compatible interpretation. No agent-authored implementation choice is represented as an additional owner vote.

