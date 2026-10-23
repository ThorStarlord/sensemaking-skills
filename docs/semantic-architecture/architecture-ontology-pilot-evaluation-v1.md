# Architecture and Ontology Pilot Evaluation v1

**Status:** Phase 5 evidence for ADR 0033 (Proposed)
**Index:** committed HEAD `c3afebf`, 85 claims (23 architecture, 8 domain, and the existing records), built with `knowledge-build` from a clean checkout
**Pilot records:** `.sensemaking/knowledge/architecture.json`, `.sensemaking/knowledge/domain.json`

## What this evaluation measures, and what it does not

It measures whether each Phase 0 competency question can now be answered **by a bounded query** on the committed index, and whether the answer is correct as far as the reviewed records go.

It does **not** measure whether an agent makes a different decision. That is the reassessment trigger in ADR 0033, and it needs an independent session that is not in place. Nothing here is a benchmark or proof of benefit.

## Results per competency question

Verdict key: **answered** (query returns the needed fact), **partial** (answered with a gap the query exposes), **not answered** (no reviewed fact exists to return), **n/a** (question concerns a repository this pilot does not model).

| # | Question | Query used | Verdict | Evidence |
|---|---|---|---|---|
| Q1 | Owner of `scripts/validate-receipt.py` | `rules-for` | answered | owner `component:receipt-validator` |
| Q2 | Rules for an edit under `semantic_architecture/` | `rules-for` on `knowledge_store.py` | answered | `rule:stable-core-no-lab-imports` matched by path scope |
| Q3 | May a stable module import lab code? | `rules-for` + `knowledge-check-rules` | answered | rule present; checker reports 0 findings on this repo |
| Q4 | Campaign and Responsibility cardinality | `explain domain_concept:campaign` | answered, **hypothetical** | `relates_to`, `cardinality: 1:N`, status `hypothetical` |
| Q5 | Book vs Book Workspace | `term` | n/a | this repository has no Book concept |
| Q6 | Fog type vs weakness type | `term fog-type` | answered | `distinct_from` `domain_concept:weakness-type` and `epistemic-status` |
| Q7 | Receipt lifecycle transitions | `explain lifecycle_state:receipt-in-progress` | answered | `transitions_to` `receipt-final` |
| Q8 | Layer of the brief producer | `rules-for` on `skills/repo-sensemaker/SKILL.md` | **partial** | owner found, but **no layer** is recorded for the Skills |
| Q9 | Bounded context of "responsibility" | `term responsibility` and `explain` | **partial** | the term is found, but **no context link** exists; `bounded_context:workflow-control` is declared and unused |
| Q10 | Data flow brief → planner | `explain component:repo-sensemaker-skill` | answered | `flows_to` `component:workflow-planner-skill`, carries the contract |
| Q11 | Interface of a receipt | existing `contract` | answered (unchanged) | `contract:receipt-schema` |
| Q12 | Decision and rejected alternative | existing `decision` / `alternative` | answered (unchanged) | ADR-derived records |
| Q13 | Test protecting an invariant | existing `tested_by` | answered (unchanged) | `inv:index-snapshot-vs-working-overlay` |
| Q14 | Placement convention for validators | `rules-for` on `scripts/validate-brief.py` | answered | `rule:validators-placement` |
| Q15 | Meaning of `observed` | existing epistemic status | answered (unchanged) | model separates status from authority |

Summary: 9 answered (Q1–Q4, Q6, Q7, Q10, Q14 and the unchanged Q11–Q13, Q15 count as unchanged, not new), 2 partial (Q8, Q9), 1 n/a (Q5). Q4 is answered only as a hypothesis.

## Gaps the evaluation exposed

1. **No `tested_by` links for the validators.** `rules-for scripts/validate-brief.py` returns `tests: []` even though validator fixtures and tests exist. The pilot did not record them. This is a pilot omission, not a query defect, and it is the most useful gap to close first.
2. **No layer for the Skills.** `skills/**` components have no `belongs_to` edge, so the layer question returns nothing for them.
3. **No context link for domain concepts.** Bounded contexts are declared but no concept is linked to one.
4. **The pilot's cardinality is a hypothesis.** Nothing in the repository states it. It should be verified or removed; it is not evidence.

None of these gaps comes from the query logic. The answers are exactly as complete as the reviewed records.

## Warning-only checker on this repository

`knowledge-check-rules --repo . --target-ref c3afebf` reports **0 findings** and **0 not-assessed** items. This matches the existing `validate-contract-authority.py` result that stable modules import no lab code. The checker's ability to detect a violation is covered by the fixture tests (`tests/test_architecture_rule_checker.py`), not by this repository, which has no violation to find.

## Cross-check of the index against the source

- Version-2 documents index with `schema_version: 2`; the 21 pre-existing records are unchanged.
- The regression check on `main@86b132c` gave the same index digest with the old and new code (`00417827…`), so existing indexes are unaffected.
- `knowledge-proposal-check` accepts both pilot files, and rejects the same files if relabelled version 1 (covered by `test_architecture_vocabulary_v2.py`).

## Decision for the owner

Keep the pilot as it is and treat gaps 1–4 as follow-up work, or complete them before ADR 0033 is considered for acceptance? The evaluation recommends completing gap 1 and gap 4 before acceptance, since one leaves a rule unqueryable for tests and the other records an unverified claim as a pilot fact.

## Reassessment (ADR 0033 trigger)

The trigger is not yet testable. It requires an independent session that uses `rules-for` before an edit and records whether the result changed what it did. Until that exists, the claim ceiling is: the queries answer the competency questions on this repository's reviewed records; decision benefit is NOT ESTABLISHED.
