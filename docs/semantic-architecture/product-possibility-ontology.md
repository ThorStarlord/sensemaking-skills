# Product Possibility Ontology v1

**Status:** Conceptual Level-2 extension of the Product (Layer 6) and Knowledge (Layer 4) ontology, v1. Descriptive only; no executable schema change.  
**Introduced:** 2026-10-28 at `main@d0af33b`, as the first increment of the owner-supplied [Product Possibility Ontology & Idea Library v1 plan](../superpowers/plans/2026-10-28-product-possibility-idea-library.md).  
**Authority:** semantic vocabulary only. Describing something as a ProductPossibility creates no Strategic Frontier membership, priority, implementation authorization, owner decision or ADR ratification. [ADR 0031](../adr/0031-persistent-semantic-stewardship.md) governs the product destination, [ADR 0029](../adr/0029-current-product-boundary.md) the product boundary, and [`STATUS.md`](../../STATUS.md) the current Level-3 state.  
**Curated instance:** [`../idea-library.md`](../idea-library.md).  
**Competency questions:** CQ-079 to CQ-088 in [`competency-questions.md`](competency-questions.md), section M.

## 1. Why the concept exists

Sensemaking can already explore possible futures and retain reviewed knowledge, but the two do not meet:

- The [Strategic Exploration Funnel](../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md) produces a breadth "opportunity landscape" with grounded and counterfactual divergence (sections 4, "Grounded and counterfactual divergence" and "Breadth output"). It gives that landscape no stable identity or durable home, and "prior exploratory ideas remain hypotheses" (section 2). A later session regenerates or forgets them.
- The [idea reservoir](../strategic-candidate-directions.md) preserves candidates with rationale, but one lifecycle label mixes realization, disposition, horizon and authority (for example `LONG_HORIZON + REQUIRES_EVIDENCE`), and cross-candidate relationships are mostly implicit. Its header is dated 2026-10-05, and apart from a 2026-10-15 note recording that ADR 0031 selected persistent stewardship, it has no entries for ADR 0031-era knowledge-plane possibilities.
- Reviewed knowledge has `opportunity`, `hypothesis` and `alternative` claim kinds (`src/sensemaking_skills/semantic_architecture/knowledge.py:23`). At `d0af33b` its 88 claims include no `opportunity`, no `hypothesis` and 3 `alternative` records, all attached to design decisions rather than product futures.

**Decision this concept changes:** a later agent doing Level-3 breadth exploration, architecture exploration or a reconsideration can start from previously considered futures, their rationale and their relationships (CQ-079, CQ-083, CQ-084), and can tell a retained possibility from selected, implemented or authorized work (CQ-081, CQ-087).

## 2. Definition and boundary

**ProductPossibility:** a retained representation of a potential future product state, capability, product change or strategic direction, together with its value hypothesis, assumptions, relevant relationships and historical disposition. It does not imply feasibility, endorsement, implementation or authorization.

It is a Layer-6 concept whose statements are Layer-4 claims. Its value hypothesis is normally a Hypothesis; implementation evidence about it is an Observation; the judgment that something realizes it is an inferred claim; its dispositions are Decisions with their own authority.

```text
ProductPossibility != Feature, backlog item or implementation task
ProductPossibility != Strategic Frontier item
ProductPossibility != ProductChange      (zero or more ProductChanges may realize it, in whole or in part)
ProductPossibility != ProductCapability  (a realized capability is what exists; the possibility is what was proposed)
ProductPossibility != construction path  (a way of advancing toward a possibility)
ProductPossibility != evidence prerequisite (an Assumption or Uncertainty)
retained != feasible != endorsed != implemented != authorized
```

A possibility may sit at any product level of the [product-change taxonomy](product-change-taxonomy.md) (need, capability, feature, change, strategic direction). Implemented baselines stay legitimate possibilities, but the possibility and what realizes it are different entities: the possibility preserves the original proposal and its history, and the realized ProductCapability, ProductChange or RepositoryElement is what exists. Link them with `realizedBy`; never let one identifier stand for both (CQ-081).

Neighbouring things that are not possibilities:

- An **engineering alternative** (a candidate implementation approach, local repair, refactoring, or responsibility weighed during engineering work, including the ones discovery declines) is a way of doing work, not a product future. It stays in the task report, the PR decision note or the decision history; when a reviewed `decision` records the choice, a useful rejected alternative may be an `alternative` claim linked to it.
- An **architecture option** (a coherent proposed software structure) is an ArchitectureOption ([prospective reasoning ontology](prospective-reasoning-ontology.md), section 3), retained as an `arch:` record when material, and compared in an `architectural_synthesis`. It may propose to realize a possibility; it is not one.
- A **construction path** (for example PATH-1 or PATH-2 of a strategic analysis) is a way of advancing toward a possibility. It keeps its identity, comparison and disposition in the analysis that defined it. The library may point to it from the possibility it would advance.
- An **evidence prerequisite** (for example evidence that separate sessions reuse retained knowledge) is an Assumption or Uncertainty. A possibility records it as an assumption or in `revisit_when`; it is never the object of `potentiallyEnabledBy`, which takes a capability or another possibility.

**Classify before retaining.** When work produces candidates worth keeping, decide what each one is before choosing where it goes; the kind decides the home, not the wish to keep it. A declined engineering responsibility becomes a ProductPossibility only through explicit reasoning: state the product future it points to (a state, capability, change or direction users or the product would have) separately from the task, check it against stored possibilities as restated, revised or new, and record the episode as its origin. Most declined responsibilities point to no new product future and stay engineering alternatives.

## 3. Relationship to existing concepts

| Existing concept | Where defined | Relationship to ProductPossibility |
| --- | --- | --- |
| ProductCapability | [ontology](ontology.md) Layer 6 | The realized ability a possibility may become (`realizedBy`), or a realized prerequisite that may enable one (`potentiallyEnabledBy`). Distinct from the possibility itself |
| ProductChange | ontology Layer 6 | A proposed or implemented modification that may realize a possibility |
| Initiative | ontology Layer 6 | A coordinated effort that may advance a selected possibility |
| Construction path | `strategic_repository_analysis` paths (for example PATH-1) | A Level-3 way of advancing toward a possibility; not a possibility |
| Assumption, Uncertainty | ontology Layer 4 | Evidence prerequisites and unresolved premises a possibility depends on; not possibilities |
| Opportunity | executable `opportunity` claim kind only; not yet an ontology.md concept | The stewardship plan (section 3.1) groups opportunity with hypothesis and uncertainty as a defeasible claim family. Typed ProductPossibility records use this kind with a `poss:` identifier and `attributes.concept: ProductPossibility` (section 6.2). The conceptual need that motivates a possibility stays part of its statement and value hypothesis |
| Hypothesis | ontology Layer 4 | A defeasible claim about the possibility's value, feasibility or consequences |
| Alternative | executable `alternative` claim kind | A competing means or direction; between possibilities, see `alternativeTo` |
| Decision | ontology Layer 4 | Records a selection, deferral, rejection or supersession, with its authority |
| Evidence | ontology Layer 3 | Grounds claims about current state or observations |
| Constraint, RatifiedIntent | ontology Layer 1 | Bound what may be built under current authority; a possibility may conflict with them |
| Strategic Frontier | [CONTEXT.md](../../CONTEXT.md), `STATUS.md` | The current material Level-3 set. A possibility enters it only through Level-3 reassessment (section 8) |

## 4. Independent descriptive dimensions

Six dimensions describe a possibility. Each is assessed separately, records its basis and assessed revision, and may be `NOT_ASSESSED`. No dimension implies another, and no combination implies priority. A change in one dimension does not update another: a possibility becoming implemented does not retroactively make its old deferral wrong.

### 4.1 A. Strategic alignment

| Value | Meaning |
| --- | --- |
| `ALIGNED` | Compatible with currently accepted intent (product strategy, accepted ADRs, ratified owner decisions) |
| `ADJACENT` | Plausible extension that needs scope clarification before it could be called aligned |
| `COUNTERFACTUAL` | Explores an explicitly altered premise that no accepted commitment or non-goal forbids |
| `CONFLICTS_WITH_CURRENT_STRATEGY` | Contradicts a named accepted commitment or non-goal; cite it |
| `NOT_ASSESSED` | No adequate alignment judgment exists |

Use `CONFLICTS_WITH_CURRENT_STRATEGY` rather than `COUNTERFACTUAL` whenever a specific accepted commitment or non-goal is contradicted. Either label leaves exploration legitimate. Neither label by itself requires Level-4 review: under [`product-thesis-revision.md`](../product-thesis-revision.md) section 4, Level 4 activates only when a material product-thesis commitment becomes decision-changing, for example when a real decision would act on a conflicting possibility.

### 4.2 B. Ambition

| Value | Meaning |
| --- | --- |
| `INCREMENTAL` | Extends or improves within the current product shape |
| `SUBSTANTIAL` | Adds a materially new capability or capability combination |
| `TRANSFORMATIVE` | Would change what the product is or how it is used |
| `NOT_ASSESSED` | Not judged |

Ambition describes scope or aspiration, not quality or priority.

### 4.3 C. Horizon

| Value | Meaning |
| --- | --- |
| `FORESEEABLE` | Its prerequisites exist or could be built within currently foreseeable construction |
| `LONG_HORIZON` | Prerequisites, evidence or scope put it beyond foreseeable construction |
| `NOT_ASSESSED` | Not judged |

Horizon is temporal and independent of ambition: a possibility can be `TRANSFORMATIVE` and `LONG_HORIZON`, or `INCREMENTAL` and `LONG_HORIZON` when its prerequisite evidence is far off. It is not desirability.

### 4.4 D. Realization state

| Value | Meaning |
| --- | --- |
| `NOT_IMPLEMENTED` | A completeness basis for the stated scope shows no realization |
| `PARTIALLY_IMPLEMENTED` | Part of the proposed future exists; state which part |
| `IMPLEMENTED_BASELINE` | The core of the proposed future exists as product or support machinery |
| `SUPERSEDED_BY_IMPLEMENTATION` | Implementation overtook the original proposal in a different form |
| `NOT_ASSESSED` | No adequate inspection, or an inspection without a completeness basis |

Keep two claims apart and preserve each status:

- **Implementation evidence** is `OBSERVED`: a file, symbol, command, Skill text or behavior exists at a named revision.
- **The realization judgment** (this evidence realizes that part of the possibility, so the state is X) is `INFERRED`.

Use `NOT_IMPLEMENTED` only with a completeness basis for its stated scope, such as a closed enumeration in code or an exhaustive check of a named location ([relations-and-epistemics.md](relations-and-epistemics.md), "Absence claims"). A lexical search that found nothing gives `NOT_ASSESSED` plus the bounded observation "none found in <scope>". A statement that something is "not qualified" is about evidence, not implementation. Documentation alone does not establish operational completeness, and Skill guidance realizes a guidance-shaped possibility without being evidence that agents follow it.

### 4.5 E. Epistemic status

No new status vocabulary. Documentary claims about a possibility use the Level-2 statuses in [relations-and-epistemics.md](relations-and-epistemics.md) (`OBSERVED`, `INFERRED`, `HYPOTHESIZED`, `RATIFIED`, ...). Typed records use the executable `epistemic_status` values in `knowledge.py:29` (`declared`, `observed`, `hypothetical`, `contested`, `superseded`, `invalidated`), and an authored normative claim still cannot be `observed` (`knowledge.py:275`). Status attaches to each claim and each relationship, not to the possibility as a whole: one possibility can have `OBSERVED` implementation evidence, an `INFERRED` realization judgment and a `HYPOTHESIZED` value. Owner ratification and action authorization stay separately recorded.

### 4.6 F. Strategic disposition

| Value | Meaning |
| --- | --- |
| `EXPLORATORY` | Retained for consideration; no selection decision has been made |
| `FRONTIER_CANDIDATE` | A Level-3 analysis considered it as a frontier candidate. This does not place it in the Strategic Frontier |
| `SELECTED` | A competent authority selected it, or a bounded part of it, for construction |
| `DEFERRED` | Considered and postponed, with a reason and, where consequential, a `revisit_when` |
| `REJECTED_FOR_NOW` | Considered and declined under current evidence or authority, with a reason |
| `SUPERSEDED` | Replaced for current reasoning by another possibility or decision; link it |

Dispositions form an append-only history (section 7). Each entry records date, authority (owner, ADR, Level-3 analysis, agent), rationale, reason class where applicable and `revisit_when` where consequential.

### 4.7 Prohibited inferences

```text
TRANSFORMATIVE          -> high priority                (invalid)
LONG_HORIZON            -> low value                    (invalid)
ALIGNED                 -> selected                     (invalid)
IMPLEMENTED_BASELINE    -> owner-ratified               (invalid: ADR 0033 vocabulary is implemented but PROPOSED)
REJECTED_FOR_NOW        -> permanently prohibited       (invalid)
FRONTIER_CANDIDATE      -> Strategic Frontier member    (invalid)
COUNTERFACTUAL          -> forbidden to explore         (invalid)
COUNTERFACTUAL          -> Level-4 review required      (invalid unless a thesis commitment is decision-changing)
no search result        -> NOT_IMPLEMENTED              (invalid without a completeness basis)
revisit_when satisfied  -> possibility selected         (invalid)
```

### 4.8 Reading the reservoir's lifecycle labels

The reservoir keeps its labels. This table only reads them into the dimensions above; it does not rewrite them.

| Reservoir label | What it informs |
| --- | --- |
| `IMPLEMENTED_BASELINE` | Realization `IMPLEMENTED_BASELINE` |
| `PARTIALLY_IMPLEMENTED` | Realization `PARTIALLY_IMPLEMENTED` |
| `SUPERSEDED_BY_IMPLEMENTATION` | Realization `SUPERSEDED_BY_IMPLEMENTATION`; disposition often `SUPERSEDED` |
| `CANDIDATE_EXTENSION` | Disposition `EXPLORATORY`; assess alignment separately |
| `REQUIRES_EVIDENCE` | A reconsideration condition (`revisit_when`), not a value of any dimension |
| `DEFERRED_BY_OWNER_DIRECTION` | Disposition `DEFERRED`, reason `owner_direction` |
| `LONG_HORIZON` | Horizon `LONG_HORIZON`; assess ambition separately |
| `REQUIRES_LEVEL_4_REVIEW` | Alignment `COUNTERFACTUAL` or `CONFLICTS_WITH_CURRENT_STRATEGY` (assess which). Exploring needs no review; Level 4 applies when acting on it would make a thesis commitment decision-changing |
| `REJECTED_FOR_NOW` | Disposition `REJECTED_FOR_NOW` |

A combined label such as `IMPLEMENTED_BASELINE + CANDIDATE_EXTENSION` usually describes two possibilities: a realized baseline and a further extension that `extends` it. Record them separately when the distinction matters.

## 5. Identity, provenance and governing authority

Each retained possibility has:

- a stable identifier `poss:<slug>`, chosen once and kept when the title or wording changes. It matches the executable ID pattern (`knowledge.py`, `ID_PATTERN`), so a typed record can reuse it whichever claim kind encodes it, and a later kind change need not change identity;
- a statement of the proposed future;
- its origin: source reference, original author or authority, and the date first recorded;
- the product objective it serves (for example `goal:compounding-product-knowledge`);
- a value hypothesis and its material assumptions;
- referenced capabilities and evidence, with the assessed revision;
- the six dimensions with their bases;
- its disposition history and any `revisit_when`;
- its relationships.

Never derive identity from current wording, reuse an identifier for a different future, or silently merge two possibilities. Replace with `supersedes` and keep both.

**Two kinds of authority apply, with different scopes:**

- The **originating document governs its own historical record**: what was proposed, when, by whom, and what disposition it recorded at the time. The library cites that record and must not rewrite it.
- The **latest applicable accepted authority governs current product commitments**: accepted ADRs, `docs/product-strategy.md` and ratified owner decisions within their scope. When an origin's historical disposition and a later accepted authority differ about what the product currently commits to, the later authority governs the present and the origin still governs its history. For example, the reservoir's `LONG_HORIZON` label for cross-repository transaction coordination remains its historical record, while ADR 0029 governs the current scope.

## 6. Relationships

The relationship meanings are canonical in [relations-and-epistemics.md](relations-and-epistemics.md), "Possibility relations (proposed, conceptual)": `potentiallyEnabledBy`, `complements`, `alternativeTo`, `conflictsWith`, `extends`, `derivedFrom`, `realizedBy`, `supersedes`, `sharesAssumptionWith` and `motivatesReconsiderationOf`. Conceptual names use camelCase, like the rest of the Level-2 relation dictionary; snake_case names are reserved for predicates that `knowledge.py` actually accepts. None of these is an executable predicate today.

### 6.1 Evidence each material relationship preserves

1. Its meaning, using one of the relations above.
2. The entities it connects, with endpoint types that match the relation's declared endpoints in [`ontology.md`](ontology.md) (Layer 6, "Product relations"). For example, `realizedBy` targets a capability, change or repository element, never another possibility; `potentiallyEnabledBy` targets a capability or possibility, never a construction path or an evidence prerequisite.
3. Its own epistemic status (observed, inferred or hypothesized), kept separate from the status of the evidence it rests on. A mechanically observed file or command does not make a semantic relationship drawn from it observed.
4. Its source or reasoning artifact.
5. Relevant assumptions and the revision at which it was assessed.
6. The conditions under which it would stop applying.

Frequent co-mention is not a relationship, and a relationship is not a dependency unless a prerequisite is actually claimed.

### 6.2 Fit with the executable vocabulary (after encoding)

Predicted from `knowledge.py` at `d0af33b`, then tested by encoding the Idea Library in `.sensemaking/knowledge/possibilities.json` (plan PR 3, schema version 1, no schema change). Verdicts use the [architecture competency check](architecture-ontology-competency-v1.md) scale: **awkward** means the link is a typed edge that queries return, but its specific meaning lives only in an unchecked attribute.

| Conceptual element | Encoded as | Verdict after encoding |
| --- | --- | --- |
| ProductPossibility | `opportunity` claim, `poss:` id, `attributes.concept` | expressible; `search --term poss:` recovers the set |
| serves a product objective | `serves_goal` (selected) or `candidate_opportunity_for` (not selected) | expressible |
| `derivedFrom` | `derived_from` | expressible |
| `supersedes` | `supersedes` | expressible (not yet exercised) |
| `realizedBy` | `implemented_by` from the possibility to a `capability` claim, `attributes.realized_part` | expressible for the link; partial scope is awkward |
| implementation evidence | `observation` claim (`observed`, authority `code` or `document`) referenced from the capability | expressible; two hops from the possibility |
| `conflictsWith` | `contradicts` to a non-goal or ADR claim | expressible; `contradictions` returns them |
| `potentiallyEnabledBy` | `requires_capability` when a prerequisite is genuinely claimed; otherwise `references` plus `conceptual_relation` | expressible for prerequisites; awkward for weaker enabling |
| `sharesAssumptionWith` | both possibilities `references` one shared `hypothesis` claim | expressible; `explain` on the hypothesis returns both |
| `alternativeTo`, `complements`, `extends` | `references` plus `conceptual_relation` | awkward: the link is retrievable, the meaning is unchecked |
| `motivatesReconsiderationOf` | not yet needed | not exercised |
| relation establishment (inferred, ratified, hypothesized) | executable `epistemic_status` (`declared` or `hypothetical`) plus `attributes.establishment` | awkward: the executable statuses have no "inferred" or "ratified" value for relations |
| dimensions and disposition history | claim attributes | awkward: returned with every claim but not filterable |

No awkward encoding lost an answer to CQ-079 to CQ-087 at the current scale (17 possibilities). PR 6 remains unwarranted until one does, for example when the set is too large to read and filtering by alignment or horizon becomes necessary.

Do not substitute the v2 `relates_to` predicate: it requires a `cardinality` attribute (`knowledge.py`, `validate_v2_attributes`) and was introduced for domain-concept cardinality, not product futures.

**Citation granularity (learned during encoding).** Evidence is matched by file, so `workspace-impact` flags every record that cites an edited file. A possibility record should cite its record of origin, and cite the library only when the library is that origin or the subject of its realization.

### 6.3 Recombination

A synthesis of several possibilities or capabilities is a new possibility with its own identifier, value hypothesis, assumptions and provenance (who synthesized it, when, from which possibilities). Link it to its sources with `derivedFrom`. Relationships proposed during synthesis stay hypothesized until evidence or authority establishes more. Recombination is not acceptance.

## 7. History, dispositions and reconsideration

### 7.1 Preserve consequential history

A possibility does not disappear because it was rejected, implemented or superseded. Append each new assessment; never overwrite the original conclusion with today's reading, which would make the outcome look inevitable (CQ-078).

### 7.2 Reason classes for deferral and rejection

`feasibility`, `cost`, `opportunity_value`, `strategic_incompatibility`, `contrary_evidence`, `better_alternative`, `missing_authority`, `owner_direction`. A reason describes a disposition at a time, not a permanent property of the idea.

### 7.3 Reconsideration conditions

A consequential deferral or rejection may carry a `revisit_when`: a prerequisite is implemented, a constraint is removed, consumer evidence appears, an assumption is contradicted, accepted strategy changes, or another possibility makes an expensive approach practical. These are semantic conditions, not scheduled jobs or triggers.

The repository already implements this shape for strategic paths: `strategic_repository_analysis` records `assumptions` and `reassessment_triggers`, `strategy assumptions` projects them and `strategy drift` reports mechanical currentness without invalidating strategy (`src/sensemaking_skills/strategy_cli.py`, commands `assumptions` and `drift`). A possibility's `revisit_when` is the same kind of statement and should reuse that discipline.

### 7.4 Reconsideration procedure

1. Retrieve the possibility and its disposition history.
2. Inspect the original evidence and reasoning.
3. Identify which premise may have changed.
4. Verify current source and authority.
5. Reassess qualitatively.
6. Append the new assessment, linked to the old one.
7. Escalate to Level 3 or Level 4 only if the result warrants it.

`NO_CHANGE` is a legitimate outcome. Reconsideration produces a question for the active agent, never an authorized action.

## 8. Relationship to the Strategic Frontier and Level 3

The Idea Library is memory of possible futures, including counterfactual ones. The Strategic Frontier is the current, material set of decision-relevant gaps and opportunities at Level 3, projected in `STATUS.md`.

```text
retained possibility
  -> consulted during Level-3 breadth exploration (funnel section 4) when one is warranted
  -> frontier candidate in one Level-3 analysis
  -> Strategic Frontier in STATUS.md, only through Level-3 reassessment
  -> one selected, authorized responsibility
```

- The library is an input to Level 3, never a replacement for it, and it does not reopen settled analysis by existing.
- An exploration-only request ends with a landscape, not a selected task (funnel section 2, "Exploration-only requests").
- Before a repository-wide direction is selected, a qualitative possibility coverage assessment (funnel section 4) asks whether retained possibilities, cross-system compositions and counterfactuals were considered and records what was left unexamined (ADR 0034, decision D). It is not a score, and it never claims every future was explored.
- Ordinary bounded engineering does not need to consult the library.
- Counterfactual and thesis-conflicting possibilities can be explored and retained without review. The Level-4 process in [`product-thesis-revision.md`](../product-thesis-revision.md) applies only when a product-thesis commitment becomes decision-changing, typically when a real decision would act on such a possibility.

## 9. Representation now and next

**Now:** this conceptual model, a curated documentary library (`docs/idea-library.md`) and typed records using existing kinds and predicates (`.sensemaking/knowledge/possibilities.json`). No claim kind, predicate, schema version, Skill, runtime, planner or validator is added. The dimension labels are conceptual vocabulary, not entries in `docs/canonical-vocabulary.yaml`: no artifact producer or consumer reads them.

**Why no new runtime:** storage (Git-authored knowledge and its rebuildable index), generation (the exploration funnel and architecture exploration) and history/currentness (strategic continuity, knowledge `history` and `changes`) already exist. What was missing is semantic: stable identity, separated dimensions, explicit relationships and preserved rationale. That judgment belongs to the active agent (ADR 0013; `con:agent-owns-semantic-control`).

**Built since:** exploration guidance that recalls and retains possibilities (plan PR 4, funnel section 4 and the steward knowledge contract) and construction-time reconciliation through `workspace-impact` (plan PR 7 guidance, steward reconciliation reference).

**Next, per the plan:** add retrieval only where existing queries prove insufficient (PR 5); specialize the schema only after a documented failed competency question (PR 6, following ADR 0033's competency-check precedent, which this plan does not ratify).

## 10. Competency questions served

| Element | Competency questions |
| --- | --- |
| ProductPossibility definition and boundary, including paths and prerequisites | CQ-079, CQ-082, CQ-087 |
| Alignment (A) | CQ-080, CQ-087 |
| Ambition (B) and horizon (C) | CQ-079 |
| Realization (D), evidence versus judgment | CQ-081 |
| Epistemic status (E) | CQ-081, CQ-082, CQ-085 |
| Disposition, reason classes, history (F, section 7) | CQ-083, CQ-084 |
| Governing authority (section 5) | CQ-080, CQ-083 |
| Relationships (section 6) | CQ-082, CQ-085 |
| Recombination (6.3) | CQ-085 |
| Identity and provenance (section 5) | CQ-086 |
| Frontier boundary (section 8) | CQ-087, CQ-088 |
