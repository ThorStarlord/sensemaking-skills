# Persistent Semantic Stewardship — Detailed Development Plan

**Status:** canonical proposed construction trajectory for the owner-selected long-term product direction; **implementation not yet started by this plan**  
**Owner selection:** 2026-10-15, Path 3 (persistent semantic stewardship platform)  
**Level-4 authority:** [ADR 0031](adr/0031-persistent-semantic-stewardship.md) and [product strategy](product-strategy.md)  
**Level-3 operation:** staged, source-grounded construction under the existing strategic/responsibility authority model  
**Initial repository:** `ThorStarlord/sensemaking-skills`; target-repository pilots require independently verified scope and source identity  
**Baseline during authoring:** `main@c5bb7b045a5557fa03bd57adce7d3df417f1cfff`  
**Execution boundary:** this plan authorizes no merge/release/deploy, new external executor, or automatic Skill publication

## 1. North star, conceptual architecture, and product distinction

The destination is a **living, queryable understanding of software**, which
grows more accurate and useful through actual development. Its consumers are
coding agents operating through specialized Skills. The system must preserve
*meaning, rationale and temporal history*, not just reproduce an AST or store
a static documentation snapshot.

A later independent agent should be able to reconstruct:

1. **Why** the product and its important capabilities exist;
2. **What** domain rules and architectural constraints were accepted;
3. **How** current implementation and tests relate to those capabilities;
4. **Which alternatives were considered and why decisions changed**;
5. **What is established, hypothetical, superseded, contradictory, or unknown**;
6. **What development opportunities become possible** given accumulated knowledge.

A knowledge graph alone does not choose an engineering direction, and a passed
test alone does not establish product correctness. Knowledge and development
form two cooperating loops:

```text
AUTHORITATIVE INTENT + REPOSITORY REALITY + ENGINEERING HISTORY
                          |
        typed knowledge / evidence ingestion
                          v
     VERSIONED CLAIMS + RELATIONSHIPS + TEMPORAL PROVENANCE
                          |
                    targeted queries
                          v
      CODING AGENT + SENSEMAKING SKILLS (reasoning and choice)
                          |
        explore -> evaluate -> build -> verify -> reconcile
                          |
               durable learning / correction
                          +---------------------> knowledge layer
```

**Path 3 is the selected architectural destination.** Path 2 is how it
produces useful software and learning. Path 1 is an economical operating
profile for tasks needing little semantic context. No short-term isolated
coding comparison can alone reverse the owner's long-horizon strategic choice;
such comparisons can still test particular components and guide design.

## 2. Reuse and separation of responsibility

Do not create a second semantic-control loop or a competing software factory.

| Existing surface | Role in the future system |
| --- | --- |
| `src/sensemaking_skills/semantic_architecture/` | Typed mechanical observations, entities/relations, provenance, currentness, semantic-index foundations |
| `semantic_cli.py`, source probes | Bounded source discovery and query/inspection entry points |
| Grounding Pack / ADR 0030 | Compact authoritative-navigation/front-door context and owner-question ratchet; **not** the graph's size limit |
| `strategic-repository-analysis` | Divergent exploration and strategic architectural alternatives using selected knowledge |
| `change-impact-analysis` | Query-guided impact tracing and downstream consequence analysis |
| `using-sensemaking` | Agent judgment, authority and warrant; acquire only the knowledge relevant to the current decision |
| `strategic-repository-reconciliation` | Reconcile learning against earlier strategic claims |
| Strategic history, handoff, Campaign companions | Existing selected-responsibility/continuation history; preserve existing authority and artifact contracts |
| Tests, runtime behavior, CI, code review | Primary *verification and observation surfaces*, not replacements for semantic intent |
| Dark Factory or existing coding agent | Durable execution where appropriate; Sensemaking does **not** schedule, merge or deploy itself |

**Existing PR #541:** optional lexical impact preview is a possible
observation adapter. It is **not** persistent semantic memory, a dependency
oracle or evidence of comparative benefit. Adopt, adapt or retire it based
on the new architecture's explicit consumer needs; do not silently merge
it as fulfillment of this plan.

**Existing research:** the Semantic Control Map persistence trial and earlier
unmerged Stewardship Kernel exploration supply cost/staleness hypotheses.
Neither is a ratified substitute for ADR 0031.

## 3. The target knowledge model

The model should be expressive enough to support whole-product architecture,
while keeping derived facts reproducible and normative claims authoritative.

### 3.1 Core node families

| Family | Example knowledge | Authority/provenance expectation |
| --- | --- | --- |
| Goal / product intention / non-goal | Offline authoring, irreversible data loss prohibited | Owner/accepted product source; never inferred from code alone |
| Domain concept / entity / contract | Experience, Memory, Scene, source of truth | Contract/document/source specific |
| Capability / user outcome | Save and restore authored scenes | Product contract + observed implementation |
| Invariant / constraint | Event revision ordering; no silent overwrites | Accepted rule, rationale and relevant verifier |
| Architectural component / interface | Persistence boundary, UI-to-store contract | Mechanically extracted where possible |
| Implementation / verification | File symbol, schema, test, observed run | Exact revision, file range, test/CI identifiers |
| Decision / alternative | Chosen storage model, rejected alternative, tradeoff | Accepted or delegated decision and reasons |
| Evidence / incident / consequence | Regression, runtime fault, migration result | Source and observation scope |
| Hypothesis / uncertainty / opportunity | Possible need for stronger consistency | Defeasible claim, falsifier and decision it informs |
| Lesson / reusable principle | Why earlier architecture failed | Validated episode, scope and known exceptions |

The pilot need not populate all families comprehensively. The schema must
support these future classes without treating absent rows as negative facts.

### 3.2 Core relationship vocabulary

Examples: `serves_goal`, `requires_capability`, `constrained_by`,
`depends_on`, `implemented_by`, `tested_by`, `decided_by`,
`supersedes`, `contradicts`, `derived_from`, `affected_by_change`,
`learned_from`, `candidate_opportunity_for`.

Each edge must have a stated meaning and derivation rule. Do not equate
co-occurrence in a file with `depends_on`, test mention with verified coverage,
or AI-generated association with normative authority.

### 3.3 A source-bound knowledge claim (conceptual example)

```yaml
id: inv-event-order-001
kind: invariant
statement: "Authoritative revision order wins over delivery order"
authority:
  type: accepted_contract
  ref: docs/DOMAIN.md
epistemic_status: supported
scope:
  repository: example-repo
  examined_revision: 0123456789abcdef0123456789abcdef01234567
evidence:
  - kind: test
    ref: tests/test_replay.py::test_reordered_delivery
    observed_revision: 0123456789abcdef0123456789abcdef01234567
relationships:
  - predicate: constrains
    target: cap-narrative-graph-replay
currentness:
  state: current_at_examined_revision
superseded_by: null
```

This example specifies desired semantics, **not** the final storage schema.
No verifier should infer a universal truth from `supported`, and the recorded
test must really exist in the indexed source revision.

### 3.4 Epistemic and temporal invariants

- Separate **prescriptive**, **descriptive**, and **epistemic** statements.
- Preserve statement identity, source locator, accepted authority and exact
  observation revision; reject unsupported source promotion.
- Represent `unknown`, `not_assessed`, `contested`, `stale`, `superseded`,
  and known falsification explicitly. Do not make a one-way confidence ladder.
- Distinguish **when a claim was observed/recorded** from **which source or
  product interval it is about**. A later fix does not delete the incident.
- Retain decisions, rejected alternatives, causes and rationale that cannot
  be recreated reliably from present code.
- Allow directed, reciprocal and multi-source relations as warranted, but
  never invent symmetric or transitive closure for semantic predicates.
- A contradiction opens a review/evidence question; it does **not**
  automatically overwrite a contract, halt all work or revise product strategy.
- History must be queryable: `as_of_revision` and `what_changed_since`
  queries distinguish observed historical state from current assessment.

### 3.5 Source-of-truth boundary

Authoritative owner goals and decisions remain in accepted documents/records.
Implementation evidence remains in code, tests and platform observations.

A **rebuildable knowledge projection/index** connects these sources. For
authored semantic conclusions or lessons that deserve persistence, use
Git-reviewable records with stable IDs and explicit origin; do not hide
their canonical meaning solely in an unreviewable generated database file.

Persistent SQLite is a strong initial query-index candidate because it is
local, transactional, supports indexed joins and can be rebuilt. Its adoption
should follow a concrete storage/query slice (Wave 3), not a claim that an
already-written implementation exists. Do not mandate an OWL/RDF triple store
or a remote graph service before a query actually needs one.

## 4. Initial query contracts — what agents must be able to ask

The product must not be evaluated by number of indexed symbols or documents.
Build around meaningful questions with correct evidence and abstention:

| Query | Expected output | Key failure to prevent |
| --- | --- | --- |
| `explain_capability(C)` | Product goal, contracts, relevant implementation/verifiers, authoritative rationale | Repeating code without product meaning |
| `trace_change_impact(target)` | Relevant consumers, constraints, tests and *candidate* indirect effects, with per-edge warrant | Fabricated dependencies |
| `why_decision(D)` | Alternatives, reasons, authority, evidence at decision time, later supersession | Lost rationale or owner invention |
| `contradictions(scope)` | Conflicting claims with source identities and unresolved interpretation | Silent conflict resolution |
| `what_changed(since_revision)` | Changed implementation links, contract assumptions and affected semantic beliefs | Treating old tests as current |
| `unresolved_opportunities(goal)` | Hypotheses and candidate capability gaps, with assumptions and falsifiers | Turning missing graph edges into missing product features |
| `resume_context(mission)` | Selected goal, commitments, completed responsibility, current evidence and next decision | Dependence on preceding chat history |
| `related_lessons(change)` | Prior incident/decision lessons and whether they apply to the new context | Context-free precedent reuse |

The active agent must remain free to inspect source artifacts, challenge graph
edges, select an alternative and stop if evidence or authority is insufficient.
No query result is an implementation order.

## 5. Wave 0 — Authoritative thesis reconciliation

**Objective:** Give a new contributor a single current strategic north star.

**Work:** ADR 0031; product-strategy purpose/positioning, scope and success
measures; `CONTEXT.md`; ADR index; reconciliation of the old grounding plan;
Level-3 status reference. Keep historical trials as historical. Avoid broad
Skill rewrites before the product interfaces exist.

**Exit:** The knowledge platform is an explicit **selected** product direction,
not a speculative candidate; ADR 0030 remains in force *for Grounding Packs*;
no existing validation claims are inflated.

**This documentation PR implements Wave 0 only.**

## 6. Wave 1 — Domain model and evidence contracts

**Objective:** Implement a small, evolvable typed semantic core with strong
epistemic boundaries.

**Likely scope:** Extend current `semantic_architecture` models and existing
validation/serialization surfaces; do not invent another ontology package if
the current one is compatible.

**Work packages:**
1. Choose stable node/edge identities and the core family vocabulary.
2. Define authority and source identity, revision/time scope, derivation and
   currentness/epistemic status.
3. Define referential integrity and graph query result contracts, including
   explicit `NOT_ASSESSED`.
4. Provide backward-compatible versioning and migrations for any persistent
   authored record that evolves.
5. Build useful examples from **current real records**, not 500 synthetic
   ontology nodes.

**Verification:** Round-trip serialization; valid and invalid provenance;
source binding; contradictory claims retained; hypothesis not promoted;
missing edge not treated as proof; historical query still returns old claim.

**Exit:** A source-cited set of typed nodes and edges can be constructed,
queried, serialized and inspected without conferring authority.

**Do not conclude:** Ontology usefulness or coverage from structural tests.

## 7. Wave 2 — Source ingestion and semantic reconciliation

**Objective:** Convert current repository information into a reproducible
typed projection while protecting owner and contract authority.

**Work packages:**
1. Create deterministic adapters for Git identity, existing ADR/decisions,
   domain contracts, available language AST/import/dependency surfaces, tests
   and CI receipts. Mark adapter scope (Python/TypeScript/etc.) honestly.
2. Separate source-level *observation* from agent-interpreted semantic claim.
3. Allow deliberate authoring of missing product rationale, architectural
   meaning and design hypotheses with provenance/falsifiers.
4. Detect changed/deleted sources, stale source spans, contradictory claims
   and superseded decisions; preserve history rather than silently overwrite.
5. Introduce bounded incremental refresh triggered by relevant source changes,
   not a mandatory full-repository extraction before every coding action.

**Verification:** Two exact Git revisions with intentional architecture drift;
a deliberately stale source link; an accepted policy versus contradictory
implementation; a test whose assertion changes; manual/owner interpretation
never inferred from keyword search.

**Exit:** A second clean checkout can reconstruct the same mechanical
observations from the same source and retain approved semantic decisions.

## 8. Wave 3 — Persistent knowledge and query API

**Objective:** Deliver the first genuinely *persistent and queryable*
knowledge product—not just a list of candidate file matches.

**Work packages:**
1. Establish an authoritative authored-knowledge format reviewable in Git
   (reuse decision records when they suffice). Preserve stable IDs/history.
2. Implement an indexed local store, initially favoring SQLite if the
   documented query/transaction needs fit it. Index is reproducible from
   authoritative Git records + observed repository source.
3. Implement versioned import/export, rebuild, migration, partial failure
   recovery, provenance recheck, and read-only query semantics.
4. Implement `explain_capability`, `why_decision`, `trace_change_impact`
   and `contradictions` (the smallest coherent set that crosses intent,
   architecture, evidence and history).
5. Return citations, observation revision, derivation and incompleteness for
   every consequence-bearing result; support bounded query depth and
   targeted retrieval rather than dumping the whole model into context.

**Verification:** Fresh-clone deterministic rebuild; clean incremental
update equals full rebuild on supported sources; contradictory decisions
retained; migration preserves old history; deleted code does not silently
delete accepted intent; graph query cost is bounded by scopes/limits.

**Exit:** A fresh independent process reconstructs and queries the same
durable semantic knowledge, including historical rationale and exact revision.

**Technology decision:** Local, reviewable, private-by-default, rebuildable.
Avoid remote account/data services unless target deployment requires them.

## 9. Wave 4 — Skill-native architectural reasoning

**Objective:** Make the knowledge model actively useful to competent coding
agents across architectural tasks.

**Work packages:**
1. Teach existing relevant Skills how to select an appropriate knowledge
   query, verify cited claims and contest or enrich stale/incomplete results.
2. Compose three workflows without a deterministic semantic planner:
   - **Divergent architecture exploration:** generate meaningful alternatives
     grounded in goals, architecture and prior decisions.
   - **Convergent evaluation:** compare alternatives against constraints,
     dependencies, consequences, costs and reversibility.
   - **Adversarial review:** search for contradiction, accidental assumption,
     unmodeled consumer, invalid test evidence and owner non-goal conflict.
3. Return approved decisions, rejected options and newly learned consequences
   to authored records or a clearly attributed hypothesis register.
4. Preserve small-context mode when no consequential semantic query is needed.

**Verification:** Inspect actual agent output against source; test false-positive
impact links and counterevidence; ensure no automatic architectural authority,
owner-intent inference or unsupported release/merge recommendation.

**Exit:** At least one real architectural decision has materially benefited
from connected product + architecture + history knowledge rather than a
file-inventory summary.

## 10. Wave 5 — Multi-session stewardship and cumulative learning

**Objective:** Prove that knowledge **compounds** over a sequence of real
engineering episodes.

**Pilot choice:** Use an authorized repository with meaningful product/domain
work spanning several sessions. Prefer an existing active product over a newly
invented benchmark; do not consume the sealed Chess-Mentor Trial 002 mission
or confuse ordinary product construction with its independent trial.

**Episode sequence:**
1. Record governing intent, current baseline and existing decisions.
2. Complete valuable engineering work, capture what changed and which
   non-derivable rationale/lessons should persist.
3. Begin a later session with a genuinely fresh agent context and the same
   durable repository knowledge, **not** the previous chat transcript.
4. Ask an architectural or product question that reuses, challenges, or
   supersedes earlier knowledge.
5. Continue construction, compare outcome against actual sources and
   reconcile the knowledge store.
6. Repeat across enough consequential source changes to exercise stale
   relationships, alternative decisions and cross-session retrieval.

**Observations to preserve:**
- Was the earlier decision correctly recovered and attributed?
- Did it change a later architectural or product responsibility?
- Was a stale/contradicted statement recognized before acting?
- Did the agent avoid repeated owner questions or rediscovery?
- Did maintained knowledge introduce rework or wrong decisions?
- Which records were used, corrected, superseded, or never consulted?
- What was the cumulative maintenance/rebuild/retrieval cost?

A few paired, same-base episodes can test component causality; a longer
development sequence tests **longitudinal stewardship**. Do not demand that a
short single-fix benchmark establish a multi-month knowledge thesis.
Nevertheless, do not claim cumulative improvement merely because a graph
contains many records or a fresh agent correctly paraphrases them.

**Exit:** At least one later independent episode demonstrates correct reuse
or correction of consequential prior knowledge, with source-bound evidence
and an honest comparison to cheaper reconstruction when possible.

## 11. Wave 6 — Scale, transfer and specialized ontologies

**Objective:** Grow beyond a small pilot to multi-subsystem and multi-repository
reasoning without collapsing different authority domains.

Possible evolutions, **not automatic next tasks**:
- product/domain-specific semantic packs and richer relationship types;
- architectural trend, long-horizon dependency and temporal contradiction queries;
- multi-repository product capability ownership and interface constraints;
- retrieval acceleration, incremental reindex and compact query-context summaries;
- knowledge review/diff UI when owner/agent use warrants it;
- reusable lessons across multiple products with explicit applicability limits.

**Exit:** Transfer and maintenance behavior is observed, not merely inferred
from one repository's self-description. Retain the option to replace SQLite or
split authored/derived stores if the real workload requires it.

## 12. Engineering acceptance and product-value criteria

These dimensions must be reported independently.

| Dimension | Acceptable evidence | Claim limit |
| --- | --- | --- |
| Representation correctness | Schema/semantic reference tests, round-trip/migrations | Valid records, not truthful claims |
| Source fidelity | Exact Git/CI anchors, rerun extractors, independent source checks | Only observed properties at scoped revisions |
| Query integrity | Adversarial false-edge and incompleteness tests | No fabricated certainty |
| Maintenance sustainability | Real incremental rebuild, stale-link and reconciliation history | Bounded overhead on observed workloads |
| Architectural usefulness | An agent uses connected rationale to make or reject a consequential design | Local decision benefit, not general superiority |
| Longitudinal learning | Fresh episodes correctly reuse/revise consequential earlier knowledge | Supported at the observed horizon |
| Comparative benefit | Matched task/model/tool/authority conditions or sufficiently controlled real episodes | Only where causal isolation is valid |
| Owner experience | Less repeated explanation and better meaningful product progress | Must not be achieved by omitting necessary consent |

Failure to demonstrate immediate single-task speedup does not disqualify the
owner-selected long-term trajectory. Repeated stale-authority errors,
unbounded maintenance, or poor *longitudinal* usefulness would warrant a
Level-3 redesign or Level-4 thesis challenge.

## 13. Core risks and design responses

| Risk | Response |
| --- | --- |
| Canonizing a buggy implementation as product intent | Prescriptive/descriptive split, source/authority checks |
| Stale graph driving harmful code changes | Revision-scoped links, invalidation, query-visible staleness |
| Divergent duplicate knowledge sources | Git authority plus rebuildable index; do not write to two manual truths |
| Excessive ontology upkeep | Incremental mechanical extraction and demand-driven authored records |
| Agent hallucinating owner decisions | Explicit authority provenance and permission separation |
| Lost architecture rationale across sessions | Versioned decisions, rejected options and historical view |
| Overfitting to one repo or short benchmark | Longitudinal normal-use episodes, transfer later |
| Huge context usage | Targeted bounded queries + references, not full graph injection |
| Another coding/execution factory accidentally emerges | Keep active agent semantic owner, external executor control |
| Skill context/version drift | Exact installed-source identity and targeted loading when attribution matters |
| Over-conservatism blocks a worthy new capability | Selected product trajectory warrants progressive construction; local evidence guides design, not permission to have a vision |
| Security and privacy leaks through the graph | Local default; source permissions, no secret capture, scoped export |
| Knowledge hoarding | Retire unsupported/unused claims, preserve consequential rationale and history |

## 14. Construction order, interfaces and PR boundaries

Prefer reviewable PRs that produce usable, retained vertical slices. Indicative
workstream order, not fixed calendar estimates:

| Package | Likely touched areas | First useful output | Dependency |
| --- | --- | --- | --- |
| S0 Product thesis + plan | ADR 0031, product strategy, CONTEXT, grounding-plan reconciliation, STATUS | Authoritative selected direction | Owner choice — **this PR** |
| S1 Typed epistemic core | `semantic_architecture/models.py`, serializers, focused tests | Versioned knowledge claims and source-bound edges | S0 |
| S2 Source/authority ingestion | `semantic_architecture/probes.py`, source adapters, evidence checks | Rebuildable graph from real repo and accepted decisions | S1 |
| S3 Durable index + queries | Existing semantic CLI + new repository-scoped persistence adapter, query tests | Independent process can query product intent, architecture and rationale | S1–S2 |
| S4 Skill integration | Existing strategy, change-impact and reconciliation Skills + relevant examples | Agent consults and updates model during genuine work | S3 |
| S5 Long-horizon pilot | Authorized real target repo, narrow normal-use receipts | Evidence of reuse, correction and architectural decision value | S3–S4 |
| S6 Scalability/transfer | Scoped adapters, retrieval/UX/optimization as warranted | Multi-subsystem or cross-repository stewardship | S5 evidence |

**No mandatory new Skill in S1–S3.** Add or substantially revise a specialized
Skill only if a repeatable semantic responsibility and actual consumer need
emerge. Do not rename semantic CLI functions as Skills.

**No automatic construction from the table.** Select each bounded responsibility
against the current repo, authority and prior results. A failed package can
be revised, narrowed or replaced without abandoning the selected north star.

## 15. Decision and authority record

- **Owner's selected product destination:** Path 3, persistent semantic
  stewardship, with Path 2 as its active development/learning loop.
- **Level-4 disposition:** REVISE long-term purpose and prioritization;
  preserve ADR 0029 external system/authority boundary and ADR 0030
  as the Grounding Pack contract.
- **Level-3 implication:** Reconcile existing short-term task-support
  priorities against persistent knowledge architecture; prefer useful,
  independent product work over construction theater.
- **This change's authority:** documentation and planning, not coding,
  publishing, merging, deploying, credentials or billing.
- **Next valid build frontier:** S1 typed epistemic/source model with one
  consequential read/query consumer; then S2/S3 persistent reconstruction.
- **Current evidence:** Architectural intent is owner-selected; repository
  implementation, long-term learning and comparative advantage are **not
  yet established** by the documentation.

The goal is not to accumulate as many ontology rows as possible. The goal is
for **the next coding agent to have a more accurate, traceable, and useful
understanding of the product than the previous agent had**, and to be able
to explain how that accumulated knowledge changed what it built.


## 16. Repository first-visit semantic bootstrap — implementation extension

**Owner selection:** first-visit orientation plus a broad, bounded structural
skeleton; progressively deepened semantic knowledge, not a mandatory exhaustive
ontology. This extends S1-S6 without resetting accepted strategy or claiming
independent agent-learning qualification.

The implementation contracts, CLI, PR delivery slices, explicit deferments and
acceptance boundaries are in
[Repository Semantic Bootstrap](semantic-architecture/repository-bootstrap.md).

- RSB-0/1/2: read-only pinned orientation, optional tracked-source containment
  indexing and focused mechanical qualification.
- RSB-3/4/5: reuse reviewed S1-S4 semantic records, explicit contradictions,
  currentness audit and optional source-checked consultation in existing Skills.
- RSB-6: real fresh independent-session qualification after S5's original
  Episode B gate, without counting same-session simulations as independent.
- RSB-7: conditional transfer/domain adapters selected by real tasks and
  observed limitations, not automatic completeness targets.

No permission, merger/deployment authority or new autonomous controller is
derived from a knowledge record or repository onboarding. A repository can
still be developed directly when a local bounded responsibility is clear.
