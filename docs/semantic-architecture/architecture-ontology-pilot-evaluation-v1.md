# Architecture and Ontology Pilot Evaluation v2 — Corrected

**Status:** evidence review for ADR 0033 (PROPOSED), based on the remediation branch of PR #565.
**Original competency source:** `docs/semantic-architecture/architecture-ontology-competency-v1.md`.
**Measurement ceiling:** current source/contract inspection and focused tests, NOT an independent coding-agent behavioral evaluation.

## Method

The original Phase 0 questions (Q1–Q15) are frozen. A query retrieving a matching record is not automatically an answer. Each verdict considers: exact entity identity, cited evidence, semantic relationship, epistemic status, rule/graph coverage and decision relevance.

- **Answered:** the modeled entity/relationship is supported by the original source for the question's scope.
- **Partial:** some relevant information is modeled, but the decisive detail is hypothetical, incomplete or unsupported.
- **Not answered:** the original question has no sufficiently evidenced answer.
- **N/A:** the question is about a different repository's domain; it is not scored as success.
- Mechanical validation, current-source inspection and actual agent decision improvement are separate claims.

## Frozen-question results

| Q | Original question, abbreviated | Verdict | Evidence and remaining limits |
|---|---|---|---|
| Q1 | Owner of a validator file | **Answered** | Explicit `component:brief-validator` / `component:receipt-validator` `owned_paths`, not a citation-derived owner; source file must still be inspected when consequential. |
| Q2 | Rules for a semantic-architecture edit | **Answered** | Path-scoped stable-core dependency rule is returned; full architectural compliance is not inferred. |
| Q3 | Can stable code import source-only lab modules? | **Answered (normative)** | `release-v1.0.yaml` excludes four packages; rule checker reports static findings and its assessment limitations, not runtime proof. |
| Q4 | Campaign-to-Responsibility cardinality | **Partial** | `rel:campaign-responsibility-cardinality` is a `1:N` **hypothesis**, not an established contract. |
| Q5 | Book vs Book Workspace | **N/A** | This is an Auteur question. The current repository cannot establish that external distinction. |
| Q6 | Fog type vs weakness type | **Answered** | Canonical vocabulary and weakness-type sources support their `distinct_from` relationship. |
| Q7 | Receipt lifecycle transitions | **Answered** | `session-receipt-v1.md` specifies `in_progress` -> `final`; no broader transition state machine is asserted. |
| Q8 | Layer of `repository_sensemaking_brief` | **Not answered** | `layer:skills` describes the producing Skill, **not** the artifact. No authoritative artifact-layer classification established. |
| Q9 | Bounded context of Skill vs Campaign responsibility | **Partial** | `bounded_context:workflow-control` gives a useful context; the pilot does not fully disambiguate responsibility subtypes. |
| Q10 | Data flow brief -> workflow planner | **Answered** | Authored `flows_to` carries `repository_sensemaking_brief`; the loader checks producer and consumer against `artifact-contracts.yaml`. |
| Q11 | Component exposing `semantic_query_receipt` | **Answered** | `component:repository-semantic-steward-skill` `exposes` `contract:semantic-query-receipt`; the manifest names the producer. |
| Q12 | Index revision decision and rejected alternative | **Answered** | Existing decision/alternative records preserve that source-grounded historical distinction. |
| Q13 | Test protecting clean-commit index invariant | **Answered** | `inv:index-snapshot-vs-working-overlay` explicitly links to `verification:clean-index-tests`; test existence is not a claim that every run passed. |
| Q14 | Placement convention for new validators | **Partial** | `rule:validators-placement` is now **hypothetical**. Existing filenames do not establish a universal mandatory placement policy. |
| Q15 | Does `observed` establish current truth? | **Answered** | The model distinguishes epistemic status from verified authority/current source; observation is not a durable guarantee. |

**Corrected tally: 10 answered, 3 partial, 1 not answered, 1 N/A (15 total).** Q3's answer concerns the package-boundary contract, not the checker proving runtime compliance. Q4 and Q14 deliberately remain hypothetical.

## Finding-specific repairs

1. **Citation/ownership conflation:** `rules-for` uses explicit v2 `owned_paths`, not `evidence_refs`, and discloses multiple declared owners.
2. **Scope inconsistency:** repository-relative path globs remain in rule metadata; graph `applies_to` edges cover components, layers and bounded contexts through reviewed membership.
3. **Incomplete rule checker:** all authored architecture rules receive `ASSESSED`, `PARTIALLY_ASSESSED`, or `NOT_ASSESSED` outcomes. Unsupported rule kinds, syntax errors and source-only package mismatch are disclosed. Static import analysis is not runtime dependency proof.
4. **Contract-free flow:** a cited Sensemaking artifact manifest is parsed and compared with the authored producer, consumer and carried artifact ID. Other repositories are not required to adopt this manifest format.
5. **Entity substitution and unjustified convention:** Q8 remains unanswered; Q11 uses the exact receipt artifact; validator placement is an explicit hypothesis.
6. **Score inflation:** success is based on the original questions and their evidence, not merely nonempty query responses.

## What the checker does not establish

The checker evaluates statically resolvable Python imports and literal import calls for dependency-direction rules. It cannot fully prove dynamic/runtime dependencies, all architectural invariants, or non-Python placement/naming conventions. `rule_assessments` and `not_assessed` show the difference between zero findings and sufficient scope. It remains warning-only.

## Compatibility and currency

Schema v2 is an additive **authored-document** format; the SQLite store schema remains v1. Historical v1 documents continue to load, and prior exact-revision digests remain pinned to their original commits. This revised evaluation is not itself a fresh index build: build the final committed HEAD and record observed counts in CI or the release receipt. Do not copy historical pilot counts into a claim about the newer revision.

## Practical qualification

See `architecture-ontology-normal-use-qualification-v1.md` for concrete source-inspected editing cases and bounded test evidence. Independent agent behavior and incremental value are **NOT ESTABLISHED**; neither clean CI nor complete record retrieval can establish them.

**ADR 0033 remains PROPOSED.** Its acceptance and integration are separate from implementation and mechanical verification.
