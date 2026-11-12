# Adaptive methodological learning — discussion synthesis (2026-11-12)

**Status:** Owner-requested, conversation-origin synthesis and source reconciliation.
**Authority:** Exploratory and non-authoritative; not a new Divergent Exploration
pass, ratified product possibility, strategy decision, Skill contract, machine
schema, implementation plan, or evidence of autonomous reasoning improvement.
**Repository baseline inspected:** `ThorStarlord/sensemaking-skills@4a3e1736df51de69cb09580193c3461d39c0ace7`.
**Origin:** User–assistant discussion culminating in the request to preserve a
concise, deduplicated account. The original chat is not a committed agent trace
or an independently observed engineering episode; the distinctions below are
attributed interpretations, not empirical performance findings.

## 1. Questions and intellectual outcome

The discussion examined whether Sensemaking should learn only about a repository
and its possible futures or also about the effectiveness and limitations of its
own reasoning methods; whether those lessons should influence future choices;
how experience may transfer across sessions and repositories; and where such
ideas belong in the existing ontology, knowledge schema, and documentation.

The resulting *interpretive synthesis* is:

- **Product knowledge** describes repository reality and possible futures;
  **methodological knowledge** concerns the conditional usefulness of ways to
  investigate, choose, construct, challenge, verify, or stop.
- **Decision understanding** reconstructs explicit rationale and evidence;
  **decision-process assessment** asks whether the approach was adequate; and
  **adaptive metareasoning** may change the next approach when warranted.
  A retrospective rationale is not proof of the agent's hidden causal process.
- Historical methodological experience can **qualitatively inform**, but not
  dictate, agent-owned selection among `ACT`, `INQUIRE`, `CHALLENGE`,
  `EXPLORE`, `VERIFY`, `ESCALATE`, and `STOP`. More mode switching or more
  ideas generated does not itself mean a better engineering decision.
- **Origin, retention, applicability, and authority** are distinct boundaries.
  Transfer should compare mechanisms, scope conditions, source revisions, and
  counterexamples rather than equate superficial similarity with relevance.
  An appropriately justified *rejection* of a precedent can be successful use.
- Session adaptation, repository-longitudinal learning, and cross-repository
  methodological transfer have different horizons and evidence requirements.
  The receiving repository's authority never travels with the source lesson.

These are discussions of existing and proposed semantics, **not evidence that
an independent agent autonomously applies or benefits from them**.

## 2. Existing conceptual and operational owners

| Concern | Existing owner and disposition |
| --- | --- |
| Qualitative choice of cognitive activity | [Metareasoning Policy v0](../../skills/using-sensemaking/references/metareasoning-policy-v0.md): existing agent-facing guidance, not a numeric ranker or automatic router. |
| Interpreting and retaining consequential returned evidence | [Learning / Reconciliation Policy v0](../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md): already distinguishes retention, retrieval, decision influence, outcomes, and independent/comparative benefit. |
| Learning scopes and evidence-gated generalization | [Capability Learning Loop v0](../research/capability-learning-loop-v0.md): responsibility and repository learning are canonical guidance; cross-episode capability learning remains a candidate extension, not an autonomous runtime. |
| Methodological preference and transfer boundary | [Context-qualified methodological learning and transfer](../research/capability-learning-loop-v0.md#context-qualified-methodological-learning-and-transfer): clarification integrated through [PR #826](https://github.com/ThorStarlord/sensemaking-skills/pull/826); it does not mandate method changes. |
| Framing, expressive ideas and attributed novelty | [Divergent Exploration Ontology v1](../semantic-architecture/divergent-exploration-ontology.md), its [portable guide](../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md), and earlier [adaptive-metareasoning exploration](2026-11-07-adaptive-metareasoning-divergent-exploration.md). |
| Durable prospective product ideas | [Product Possibility Ontology](../semantic-architecture/product-possibility-ontology.md), [Idea Library](../idea-library.md), and source-linked reviewed possibilities when independently warranted. |
| Earlier conclusion about the research stage | [Adaptive-metareasoning Stage 4](2026-11-08-adaptive-metareasoning-depth-misleading-progress-question-evolution.md) and [authentic-use observation](../normal-use/2026-11-08-adaptive-metareasoning-authentic-use-observation.md): conceptual exploration closed for its stated purpose; authentic evidence remains partial. |

The discussion did **not** discover a missing universal concept or establish a
new product opportunity requiring another `poss:` identity. It mainly made
relationships among already documented owners easier to reconstruct.

## 3. Representation and retention decision

Sensemaking distinguishes [conceptual ontology](../semantic-architecture/README.md)
(meaning), the [executable knowledge contract](../../src/sensemaking_skills/semantic_architecture/knowledge.py)
(permitted kinds/relations and mechanical validation), and source records
(specific assertions, provenance, and uncertainty).

- This **dated Markdown record** is the source-readable home for the conversation's
  intellectual distinctions and the assessment that most already existed.
- [`.sensemaking/knowledge/divergent-exploration.json`](../../.sensemaking/knowledge/divergent-exploration.json)
  currently indexes conceptual role definitions; it is not an append-only list
  of all brainstormed ideas. No additional `CandidateExpression` machine kind
  follows from this discussion.
- [`.sensemaking/knowledge/possibilities.json`](../../.sensemaking/knowledge/possibilities.json)
  already records curated, individually grounded `ProductPossibility` records.
  Mere restatements of existing possibilities should not be duplicated there.
- A `source` or `lesson` claim may be added *later* only if a concrete
  future retrieval or consequential learning need justifies its reviewed,
  source-pinned representation. This record itself does not establish one.

No graph update, schema migration, new ontology, new Skill, policy rewrite,
knowledge-index mutation, or automatic promotion is authorized by this record.

## 4. Reusable diagnostic distinction, not a mandatory four-stage workflow

The discussion proposed a compact check before treating a repository-improvement
idea as new:

1. **Locate the existing definition.** Is the proposed concept absent, already
   defined, or merely refined? Inspect the governing concept and source state.
2. **Establish implementation and qualification separately.** Distinguish
   agent-facing instructions, executable capabilities, observed independent
   behavior, and demonstrated decision or product benefit.
3. **Identify the actual gap.** A missing concept, missing implementation,
   unreliable retrieval/use, inadequate evidence, or poor outcomes call for
   different responses; do not infer one from another.
4. **Select the smallest warranted response.** Existing-policy application,
   bounded construction, evidence gathering, a documentation clarification,
   or `NO_CHANGE` can each be appropriate.

This condenses existing orientation, warrant, learning, and metareasoning
guidance. It is **not** a new ontology class, machine schema, obligatory audit,
or reason to delay otherwise warranted construction.

## 5. Evidence ceiling and stopping decision

The important unresolved behavioral question is whether relevant retained
methodological experience reaches a later independent agent **before** a
consequential mode or responsibility choice, is correctly applied or rejected
against the receiving context, and contributes useful decision value.
Availability, retrieval, influence, engineering success, and causal/comparative
benefit are distinct claims. The discussion and this record establish **none**
of those stronger empirical outcomes.

**Disposition:** preserve this concise source-linked synthesis for continuity;
do not reopen completed divergent stages or create a new learning system.
Return to authentic product construction. Reconsider a specific guidance,
retrieval, representation, or evidence-capture change only when a consequential
normal-use case reveals a sufficiently grounded gap, within current authority.
