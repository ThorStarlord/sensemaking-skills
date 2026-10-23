# Architecture and Ontology Competency Check v1

**Status:** Phase 0 evidence for proposed ADR 0033 (`docs/adr/0033-architecture-and-ontology-vocabulary.md`)
**Purpose:** decide, before any vocabulary change, which architecture, ontology and design questions the current knowledge vocabulary cannot express. Questions marked **not expressible** are the primary extension gate; additional convenient predicates need an explicit independent rationale.
**Vocabulary tested:** `src/sensemaking_skills/semantic_architecture/knowledge.py` as of `main@86b132c` (18 claim kinds, 6 epistemic states, 8 authority kinds, 16 predicates).

## Verdict scale

- **expressible**: a claim kind or predicate with the right meaning exists and is validated.
- **awkward**: the meaning fits only in free text, or in the unchecked `attributes` mapping. Accepted by ingestion, validated by nothing, and not queried by any operation.
- **not expressible**: no kind or predicate carries the meaning.

Evidence for "awkward" is the code path, not the author's intent: `knowledge_store` accepts any `attributes` mapping (`knowledge.py`, `read_authored_claim`), and no retrieval operation reads it.

## The competency questions

Each question states the decision it serves (from the six purposes in the plan), the closest existing form, and the verdict.

| # | Question the coding agent needs answered | Decision served | Closest existing form | Verdict |
|---|---|---|---|---|
| Q1 | Which component owns the file `scripts/validate-brief.py`? | where code belongs | `component` with `implemented_by`; no path matching | awkward: `implemented_by` links a claim to a source file, but nothing answers "what applies to this path" |
| Q2 | Which architecture rules apply to an edit under `src/sensemaking_skills/semantic_architecture/`? | which rules apply | `invariant`, `constraint` as free text | not expressible: rules carry no scope and cannot be selected by path |
| Q3 | May a stable module import from the lab package? | which rules apply | `constraint` statement; `validate-contract-authority.py` enforces it outside the graph | not expressible: a dependency-direction rule has no typed form and no checkable target list |
| Q4 | What is the relationship between a Campaign and its Responsibilities: one or many? | ontology cardinality | none; `depends_on` is untyped | not expressible: no cardinality on any relation |
| Q5 | Is a Book distinct from a Book Workspace? | ontology: confusable terms | `domain_concept` statements only | awkward: no `distinct_from` or `synonym_of` predicate |
| Q6 | Is "fog type" the same concept as "weakness type"? | ontology: confusable terms | `domain_concept`, prose | awkward: same as Q5 |
| Q7 | Which lifecycle states can a receipt move through, and which transitions are legal? | ontology: lifecycle | none | not expressible: no state kind and no transition predicate |
| Q8 | Which layer does `repository_sensemaking_brief` belong to? | architecture: layers | `component` attributes only | not expressible: no layer kind and no membership predicate |
| Q9 | Which bounded context defines "responsibility" (Skill responsibility vs Campaign responsibility)? | ontology: bounded contexts | none | not expressible: no context kind |
| Q10 | What data flows from `repo-sensemaker` to `workflow-planner`? | architecture: data flow | `depends_on` (untyped), artifact contracts outside the graph | not expressible: no flow predicate; the contract lives in `artifact-contracts.yaml`, which the graph does not index |
| Q11 | Which component exposes the `semantic_query_receipt` contract? | architecture: interfaces | `contract` with `implemented_by` | expressible |
| Q12 | What was decided about the knowledge index revision rule, and what was rejected? | design: rationale | `decision` with `decided_by`; `alternative` with `references` | expressible |
| Q13 | Which test protects the invariant "index builds need a clean commit"? | design: verification | `invariant` with `tested_by` `verification` | expressible |
| Q14 | Which naming or placement convention applies to new validators? | design: conventions | none; `CLAUDE.md` prose | not expressible: conventions have no typed form and no path scope |
| Q15 | Is the `observed` status of a claim proof that the code still does what it says? | epistemic status | `epistemic_status` plus `authority_kind` | expressible (the model already separates these) |

## Tally

- expressible: 4 (Q11, Q12, Q13, Q15)
- awkward: 3 (Q1, Q5, Q6)
- not expressible: 8 (Q2, Q3, Q4, Q7, Q8, Q9, Q10, Q14)

## Gate outcome

The gate passes: eight questions are not expressible, and they group into five needs:

1. **Path-scoped rules** (Q2, Q3, Q14): a rule kind with a `rule_type` and an `applies_to` scope.
2. **Cardinality** (Q4): an `N:M`-capable relation with a required cardinality attribute, checked by ingestion.
3. **Lifecycle** (Q7): a state kind and a transition predicate.
4. **Layers and contexts** (Q8, Q9): membership predicates over new `layer` and `bounded_context` kinds.
5. **Data flow** (Q10): a `flows_to` predicate, checked against `artifact-contracts.yaml` in the authored-source verification adapter.

Q5 and Q6 are awkward, but cheap to fix with two predicates (`distinct_from`, `synonym_of`); they are included.

Q10 (data flow) is included as need 5. Indexing `artifact-contracts.yaml` would be an alternative, but the contract file already declares `produced_by` and `consumed_by`, so the graph only needs a typed predicate to reference it. **Decision for Phase 1: add `flows_to`, and cross-check it against the contract file in Phase 2.**

## What this document does not establish

- It does not show that these additions will change any agent decision. That is tested in Phase 5 of the plan.
- The verdicts are a single reviewer's judgment, checked against code, not a measured benchmark.
- Q1 can already be approximated by listing component paths in prose; the verdict reflects that a query cannot do it.

**Post-review clarification:** `external_system` was deferred because no competency failure justified it. `exposes` is retained to make the already-expressible Q11 component-to-contract relation explicit; this is a scoped convenience, not evidence of a new failure. See the corrected pilot evaluation for the actual answer ceiling.
