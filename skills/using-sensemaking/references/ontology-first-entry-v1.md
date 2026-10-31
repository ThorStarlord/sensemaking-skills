# Ontology-First Repository Entry (v1)

**Purpose:** How the active agent enters a repository-level request: establish
or reuse source-grounded understanding of what the repository is before any
repository-wide selection, then explore what it could become broadly enough
before converging. This reference belongs to the distributed
`using-sensemaking` Skill. It is a conceptual journey, not a workflow engine,
a checklist to complete, or a grant of authority.

**Load when:** the request is repository-level ("apply Sensemaking to this
repository", "what could this product become", a broad delegated mission), or
a returning session must judge whether existing semantic and possibility
coverage is adequate for its goal.
**Skip when:** the request is narrow (section 5). Even when adequate, current
knowledge answers a repository-level question, use section 6 for any
consequential final recommendation.

## 1. Three layers, kept distinct

| Layer | What it holds | Where it lives |
| --- | --- | --- |
| **Framework ontology** | Sensemaking's reusable vocabulary: goals, evidence, constraints, capabilities, components, dependencies, decisions, possibilities, architecture options, consequences | The Steward's knowledge contract; shared across repositories |
| **Target domain ontology** | The product's own concepts, states, invariants, boundaries and rules | Reviewed records in the target repository, expressed with the framework vocabulary |
| **Target knowledge instances** | Source-grounded statements about what the repository contains, proposes, decides and does not yet know | Reviewed records with sources, status and history |

A domain with unfamiliar nouns does not need new framework types. Express its
concepts with the existing vocabulary; propose a narrow extension only through
the Steward's schema-evolution procedure when a real distinction cannot be
represented.

## 2. First engagement

```text
IDENTIFY REPOSITORY AND GOVERNING INTENT
ASSESS SEMANTIC KNOWLEDGE COVERAGE
BOOTSTRAP REPOSITORY ONTOLOGY            (Steward BOOTSTRAP)
MAP CURRENT SYSTEM AND CAPABILITIES
DIVERGENT POSSIBILITY EXPLORATION        (funnel breadth)
CONVERGENT FRONTIER EXPLORATION
ARCHITECTURAL / STRATEGIC SYNTHESIS      (only where it changes the choice)
COMPARATIVE EVALUATION
CONSEQUENCE DEPTH / FEEDBACK
SELECT / DEFER / INVESTIGATE / NO_CHANGE
PERSIST SOURCE-GROUNDED KNOWLEDGE
  -> stop with a complete reasoning outcome
  -> or an optional, separately authorized implementation handoff
```

Repeat, reorder or skip steps when evidence warrants it. The one fixed point is
the **default entry responsibility**: establish the repository's semantic
foundation before a repository-wide strategic selection. Who owns each step
and when each is warranted: `adaptive-skill-composition-v1.md`.

### Is the existing model adequate?

Adequacy is relative to the goal, not a size or density threshold. For a
repository-level goal, ask whether a later agent could answer from reachable
sources:

- What is the product for, and which accepted decisions and non-goals govern it?
- Which major systems and capabilities exist, and who owns them in source?
- Which domain distinctions must not be conflated?
- Which areas were assessed, and which remain `NOT_ASSESSED`?
- Is the model current against the revision you are reasoning about?

Recalled records answer these questions only where a current source check
confirms them for the areas the goal turns on. A summary of records is not an
inspection of the systems they describe.

If the answers exist and are current, reuse them and go to exploration. If they
are missing or materially stale for the area the goal turns on, bootstrap or
deepen that area by invoking the `repository-semantic-steward` Skill in
BOOTSTRAP mode (its procedure: `../../repository-semantic-steward/references/bootstrap.md`).
Bootstrapping does not require running product code or an exhaustive
inventory.

### Without write authority

Produce a source-grounded **provisional** model and coverage report in the
session's report. Continue reasoning from it, but say plainly that it was not
persisted and that later agents will not inherit it. Do not claim retention.

## 3. Breadth before convergence

A well-supported local finding can still be strategically inferior to an
opportunity elsewhere in the product. After a foundation exists, the expected
next responsibility for a repository-level goal is broad possibility
exploration through the `strategic-repository-analysis` Skill's Strategic
Exploration Funnel
(`../../strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`).
Its analysis artifact follows that Skill's template and validator.
Explore the major systems and cross-system relationships, and consider
capability expansion, new user experiences, compositions, simplifications,
alternative boundaries and relevant counterfactual futures. Recall retained
`poss:` records first. Classify before retaining: product possibilities,
engineering alternatives, architecture options and construction paths are
different things.

**Possibility coverage assessment.** Before selecting a repository-wide
direction, answer qualitatively:

- Were the major product systems and intended user outcomes considered?
- Were cross-system and compositional opportunities examined?
- Were retained possibilities and earlier rejected alternatives recalled?
- Were meaningful counterfactuals considered without treating them as authorized?
- Is the analysis converging because the evidence supports it, or because the
  first visible candidate was easiest?
- Which material areas remain unexamined, and could an excluded direction
  plausibly overturn the preference?

This is a sufficiency judgment, not a score or candidate quota, and it never
claims every future was explored. Report the unexamined areas with the result.
A repository-wide selection is not justified by one isolated defect. When
exploration itself is the requested outcome, stop after it.

## 4. Subsequent engagements

Do not repeat the full bootstrap. Instead:

1. Identify the target and its source revision.
2. Retrieve the existing ontology, reviewed knowledge and prior analyses.
3. Check source relevance, semantic coverage and material currentness.
4. Reconcile only consequential gaps or contradictions.
5. Determine the current unresolved reasoning question.
6. Apply the specialist that owns it.
7. Persist meaningful changes.
8. Stop, or continue within the delegated reasoning mission.

**Currentness reconciliation.** Step 3 is not met by noting that the analyzed
revision trails a newer accessible one. When a relevant newer revision or later
evidence exists (a merged PR, a newer receipt or normal-use record, a source
revision ahead of the checkout), decide whether it could change the pending
claim, comparison, recommendation or closure:

1. Establish current source identity: the revision analyzed, and the latest
   relevant revision accessible within the granted scope.
2. Find candidate newer changes from commit subjects, changed paths and linked
   PR or receipt records. A narrow task that the request bounds needs no history
   scan.
3. Inspect only the changes that could alter the decision.
4. Classify each finding's effect as `material` (it changes a claim, comparison,
   recommendation or closure), `immaterial` (it confirms or leaves the
   conclusion unchanged) or `unresolved` (it could matter, and inspection could
   not settle it).
5. Reconcile proportionately: revise the affected claim, state the limit, or
   record that no change is needed. Reopening strategy is a separate judgment
   (`../SKILL.md` section 7).

If the newer evidence is unavailable (offline, a shallow checkout, no remote, or
an authoritative branch outside the granted scope), complete the appropriately
scoped reasoning, name the revision actually inspected, and do not assert global
currentness. Do not checkout or rewrite a repository merely to resolve a
revision difference; that environment change needs its own authority.

**Re-warrant recorded next steps.** A receipt's `next`, a `STATUS.md`
recommendation or an earlier queue names a candidate responsibility, not the
current one. Before applying a specialist to it, check that its trigger and
premises still hold at the current revision, and compare it on the same terms
as the alternatives in section 3: productive reasoning, reversible construction
within the granted authority, investigation that could change the decision,
reconsideration of an upstream assumption, and stopping. Compare expected
contribution to the decision, opportunity cost, dependencies, reversibility and
consequences. A missing qualification or observation result is evidence about
confidence; it is not by itself the most important next responsibility.

Understanding should improve across sessions; a session that only re-derives
what the records already say has not used them.

## 5. Narrow requests

A narrow request, such as evaluating one proposed architectural change, uses
the relevant existing knowledge instead of repository-wide exploration. Keep
the requested scope and never present a narrow result as a repository-wide
possibility evaluation. An explicit implementation request can go to the
portable construction loop without a new strategic exploration when an
adequate governing decision and relevant context already exist.

## 6. Outcomes

Each of these is a complete result: a semantic foundation with a coverage
report; a possibility landscape; an architecture synthesis; a strategic
selection, deferral, investigation or justified no-change; reconciled
knowledge. An implementation handoff needs an independently warranted
direction and its own authority; a selected direction does not invoke an
implementation planner by itself.

### Explain a consequential repository-level recommendation

Give the reader enough substance to challenge the judgment, proportionate to
its scope and consequences. Connect the argument rather than merely listing
sources, candidate names or labels. In the final report:

- State the user's actual request and the product outcome and governing
  decisions that apply; distinguish those decisions from observations and
  agent hypotheses. Cite the decisive sources and their relevant revision.
- Explain what the evidence shows, why each material observation changes the
  choice, and the consequences for the product or its users. A source citation
  alone does not establish priority.
- Compare credible directions actually evaluated: their expected value,
  limitations, dependencies and material consequences. Explain why the selected
  direction is more warranted now, or why the evidence cannot support a
  selection. Do not substitute enumeration, a fixed candidate count or an
  invented tradeoff for a real comparison.
- State the evidence or changed conditions that would overturn the preference;
  distinguish a bounded, independently useful enabling step from a choice of
  repository-wide strategic priority. Do not present a local defect as proof
  that every alternative is less valuable.
- Identify the specialist capabilities that actually contributed and how they
  were used, with observable invocation or source evidence when available.
  Distinguish native invocation from manual loading, and disclose unknowns;
  neither fabricate a prior decision nor force a specialist call for a report.
- State the decision-relevant uncertainties, unexamined areas, evidence ceiling,
  next warranted responsibility and its authorization boundary. A bounded
  comparison is not exhaustive coverage, and a recommendation is not permission
  to implement it.

Use this same substantive standard in ordinary repository-level use and in
maximum transparency. The latter additionally records contemporaneous
selection rationales and observed execution under `decision-observability-v1.md`;
more procedural narration alone does not improve the decision synthesis. No
fixed headings or receipt fields are required. Focused and narrow tasks use
only the explanation their actual scope needs. An illustrative worked comparison
appears in `../../../examples/decision-observability-example.md` when present.

## 7. Evidence ceiling

This entry follows an owner-selected product identity. That it improves
decisions, transfers across hosts or is reused by later sessions is not yet
established; report what a session actually observed.
