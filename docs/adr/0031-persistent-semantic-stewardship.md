# ADR 0031: Persistent Semantic Stewardship as the Long-Term Product Direction

**Status**: ACCEPTED — owner-selected 2026-10-15; this ADR records the selection, not an implemented capability  
**Date**: 2026-10-15  
**Level**: Level 4 — Product Thesis / Strategy Revision  
**Disposition**: REVISE the product purpose and long-term architectural direction; preserve the delegated engineering and external-runtime boundaries  
**Related authority**: ADR 0029 (product boundary), ADR 0030 (compact Grounding Pack), `docs/product-strategy.md`  
**Construction plan**: `docs/persistent-semantic-stewardship-plan.md`

## Context and owner decision

The owner explicitly chose **Path 3 — Persistent Semantic Stewardship Platform**
after comparing lean decision assistance, continuous product-grounded construction,
and a persistent semantic knowledge platform. The clarified primary goal is not
another way to implement bounded coding tasks: already-capable coding agents
need durable, progressively better **understanding of the software product**
over years of changes and independent agent sessions.

Previous guidance centered on selecting the next warranted engineering
responsibility and minimizing knowledge retained beyond what current code
could reveal. That remains valuable for local tasks, but does not fully
represent the owner's intended product: accumulation and reuse of product,
domain, architectural, decision, evidence, and engineering-history knowledge.

The earlier conclusion that Path 3 was merely an optional later optimization
is superseded **as a strategic choice**. It was not a negative empirical verdict
about typed semantic memory. The empirical advantage of the selected direction
has still not been established.

## Decision

1. **Product destination.** Sensemaking Skills will evolve toward a
   **persistent, typed, queryable, provenance-aware semantic knowledge system
   operated through specialized Skills**. Its long-term purpose is to improve
   agents' capacity to understand, reason about, maintain, and evolve complex
   software across tasks, agents, repositories, and time.

2. **Two complementary planes.**
   - The **knowledge plane** captures meaningful product intent, goals,
     capabilities, entities, invariants, constraints, architectural contracts,
     dependencies, implementation mappings, verification/evidence, uncertainty,
     alternatives, decisions, incidents, lessons, and temporal history.
   - The **reasoning/action plane** uses Skills and the active coding agent for
     exploration, architectural synthesis, adversarial review, responsibility
     selection, construction, verification, semantic reconciliation, and
     knowledge improvement. A knowledge graph is not an agent or a planner.
   **Path 2** (continuous product-grounded development) is the operational
   loop that uses and enriches **Path 3**. **Path 1** (lean assistance) remains
   the low-ceremony operating mode where deeper memory has no consequence.

3. **Epistemic separation.** Preserve at least three kinds of knowledge:
   **prescriptive** (authorized desired behavior and commitments),
   **descriptive** (what source/runtime/test observations establish), and
   **epistemic** (interpretations, hypotheses, conflicts, unknowns, limitations
   and their evidence). Neither extraction from buggy code nor syntactic
   validation silently creates owner intent or semantic truth.

4. **Durable, reconstructible claims.** Consequential relationships require
   stable identity, source/authority attribution, Git-revision or observation
   scope, derivation method, currentness, uncertainty, and supersession or
   contradiction handling. Missing knowledge is **NOT ASSESSED**, not safe or
   absent. Preserve historical reasons even when current claims are revised.
   Mechanical facts should normally be **recomputed** from canonical sources;
   non-derivable choices, hypotheses, and hard-won lessons merit durable,
   reviewable preservation.

5. **Knowledge usefulness rather than document volume.** A larger and richer
   typed ontology is an explicitly selected long-term capability, not a
   prohibited form of documentation. Depth should increase where relationships
   improve consequential reasoning, including architecture and multi-session
   continuity. Reject duplication and stale claims; do **not** impose a
   universal small size cap on the semantic model. Context retrieval remains
   selective and task-relevant.

6. **Verification is essential but instrumental.** Code review, static
   analysis, tests, CI, and real product behavior supply evidence and
   contradictions to the knowledge model. They remain mandatory where the
   engineering claim requires them. They are not the sole long-term product
   objective or a substitute for understanding *why* the system exists and
   *how* it should evolve.

7. **Build incrementally toward the chosen destination.** Start with a
   versioned conceptual model and useful queries over real repository
   knowledge. Reuse the existing Semantic Architecture, source probes,
   Grounding Pack, strategic continuity, change-impact and learning surfaces
   where possible. Develop persistent query/index capabilities as an
   intentional product trajectory, with concrete consumer contracts,
   incremental maintenance, and migration support. Do not wait for a
   comprehensive ontology before allowing normal engineering.

8. **Authority remains external to the representation.** Authoritative
   owner/product commitments remain in approved owner/ADR/product sources;
   code and tests remain authoritative for their own observed behaviors;
   the semantic index stores citations and typed projections, not an
   unconditional replacement truth. Agent-authored guesses and delegated
   design choices cannot promote themselves to owner decisions. No graph
   edge authorizes changing the product thesis, granting permissions,
   merging, releasing, or deploying.

## Relationship to existing ADRs and plans

- **ADR 0029 remains the current external product boundary.** Semantic
  stewardship expands the intended product capability *within* an agent-native
  decision-support/knowledge layer. It does **not** make Sensemaking a coding
  model, general coding runtime, semantic truth oracle, centralized task
  selector, or autonomous software factory. Dark Factory remains the separately
  owned durable execution/factory runtime.
- **ADR 0030 remains operative for the compact human/agent Grounding Pack.**
  Its file budgets, citation rules, decision ratchet and evidence history apply
  to **that pack**, not to the future typed semantic index. Its
  "only non-derivable facts" inclusion rule is *not* a prohibition against
  indexing derived code structure or relationships in the knowledge plane.
  This ADR refines that broader interpretation and supersedes using compact
  pack scope as the complete product vision.
- **`docs/repository-grounding-plan.md` remains an evidence-bounded
  subprogram.** Its incomplete Phase 3 comparison remains incomplete.
  Grounding Pack success cannot be promoted into semantic stewardship benefit.
- **PR #541** is an optional lexical, read-only preview and has no established
  architectural-impact or long-term memory value. It is not the persistent
  knowledge plane and need not be merged to validate this thesis.
- Historical experiments and simplification verdicts remain valid **within
  their tested time horizon**, not as decisive evidence against an untested
  multi-month knowledge-compounding hypothesis.

## Success and failure conditions

Long-term success requires **better decisions in later, genuinely separate
engineering episodes**, not more ontology rows:

- a later agent can reconstruct relevant intent, capabilities, dependencies,
  rationale, and evidence at a precise source revision;
- past validated knowledge prevents a consequential mistake, helps select a
  better architectural path, or reduces rediscovery/rework;
- contradictions and invalidated assumptions are recognized rather than
  canonized;
- the model remains maintainable as the application evolves, with automated
  refresh of derivable facts and transparent human/agent authority boundaries;
- the knowledge system stays queryable without loading its full contents into
  model context.

Tests and schemas can prove integrity/shape; they cannot by themselves prove
those long-horizon effects. Evidence must distinguish implementation,
usefulness, comparative benefit, and cross-session learning.

## Immediate consequences and limits

- Update the canonical Level-4 product purpose, success measures and
  Level-3 direction. Begin the phased design and construction defined in the
  linked plan under separate ordinary repository work decisions.
- No code, schema, CLI, runtime, Skill instructions, release contract,
  installed Skill distribution, merge authorization, or target-repository
  knowledge migration is changed merely by accepting this ADR.
- No comprehensive upfront extraction is required for each engineering task.
  The platform may grow toward substantial domain coverage without making
  incomplete indexing a blanket blocker on independent construction.
- Reassess this architectural direction through Level 4 if real maintenance,
  correctness, security, or decision-value evidence materially defeats its
  foundational assumptions; absence of immediate single-task improvement alone
  does not constitute that evidence.
