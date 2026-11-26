# Change-scoped verification plan (2026-11-28)

**Status:** cumulative beneficiary work completed and partially exercised.
**Source baseline:** `ca597b2a6c80e76964f45630fe29e1a11c4c9e19`.
**Possibility synthesis:** `6acc0fe9163d40736d3603be5575a05457ad5b62`.

## 1. Retained beneficiary evidence

On 2026-11-25 a fresh-context consumer evaluating `knowledge_sources.py` found
that the then-current source relationships gave file-level test references but
not the test functions or methods that mention `build_knowledge_snapshot`. The
consumer had to inspect test bodies manually to expand a verification plan for
a change to that symbol. The resulting symbol context now reports six direct
test-function candidates, but no consumer turned a selected file/symbol into a
deduplicated test set, pytest command, authored verification view and explicit
gaps.

That record is the retained understanding this episode applies:
`docs/normal-use/2026-11-25-symbol-usage-context.md`.

## 2. Selected responsibility

For one committed Python file and top-level symbol, produce a bounded
verification plan that composes:

- authored verification records linked to the file path;
- direct test-function candidates for the symbol;
- guard-derived scenario candidates for the symbol;
- a deduplicated Python test-file set and suggested pytest command;
- explicit gaps and limits.

The plan does not execute tests, generate tests, claim coverage or establish
that a change is verified.

**Value hypothesis:** the plan reduces manual test-body inspection and missed
verification for a change-scoped engineering task.

## 3. Fresh-context entry

A `sensemaking-skills handoff` was generated for this repository at
`6acc0fe9`, with the installed `using-sensemaking` Skill path, the task
question and the retained normal-use record. The consumer was authorized to
modify this worktree, not to commit, push, merge or modify another repository.

**Observed entry:** the handoff discovered the repository source Skill at
`skills/using-sensemaking/SKILL.md` with
`currency: CURRENT_WITH_PACKAGE_SOURCE`. The consumer read the Skill manually
because the host exposed no native Skill tool. It reported that fallback
explicitly. It worked only in the target worktree, made no commits and did not
modify the knowledge pack, normal-use record or receipt.

## 4. Implementation and authentic use

**Delivered consumer:** a new
`semantic verification-plan --path FILE --symbol NAME` command, backed by
`run_verification_plan` and a pure `verification_plan.py` composition. It
merges targets from `context.verification_refs` with
`symbol_context.test_candidates`, keeps guard scenarios separate and
non-executable, reports authored records that do not map to a test file, and
emits explicit gaps. It does not run or generate tests.

**Observed plan for `knowledge_sources.py` / `build_knowledge_snapshot`:**
`target_ref` `6acc0fe9`; definition line 521; 5 authored verification records
(all file-scope), 6 direct test functions, 8 guard scenarios; 12 unique pytest
candidates (6 files + 6 function targets); 10 suggested targets after 2 function
targets were subsumed by file targets; 0 duplicate target merges.

Suggested test files:

- `tests/test_architecture_queries.py`
- `tests/test_architecture_vocabulary_v2.py`
- `tests/test_console_output_ascii_only.py`
- `tests/test_public_api_contract.py`
- `tests/test_semantic_knowledge.py`
- `tests/test_semantic_knowledge_self_repo.py`

Unsubsumed suggested functions include
`tests/test_repository_semantic_steward.py::test_stewardship_revision_lifecycle_and_currentness`
and
`tests/test_semantic_change_classification.py::test_missing_origin_fingerprint_is_not_assessed`.

The plan reports `FILE_LEVEL_ONLY`, `NO_EXECUTABLE_TEST`, `NOT_RUN` and
`NOT_ASSESSED` gaps. `tests_executed`, `test_analysis_established`,
`test_results_established`, `coverage_established`,
`semantic_truth_established` and `action_authorized` are all `false`.

**Static checks and hosted CI:** ruff, compileall, docs currentness, YAML parse
and `git diff --check` passed locally. A source-pinned hosted check exercises
this exact case, the non-Python refusal and the malformed-symbol refusal. Local
unit/synthetic tests are `NOT_RUN`; the hosted full suite remains the execution
evidence.

## 5. Cumulative contribution

**Recovered understanding:** the consumer read
`docs/normal-use/2026-11-25-symbol-usage-context.md`, the synthesis episode and
the newly authored possibility. It cited the prior manual test-body inspection
and the existing direct-reference limitation as the reason for the plan's
shape. It also recovered the current `context-for --include-source-relationships
--symbol` contract, authored `verification_refs`, and guard scenarios.

**What it changed:** the same symbol that previously required manual test-body
inspection now yields a deduplicated candidate set and a non-executed pytest
invocation in one command. The plan preserves the prior record's distinction
between file-level test references and function-level mentions: it exposes both,
marks file-level authored records, and reports function candidates subsumed by
a file candidate. It also reports its own gaps and non-claims rather than
silently treating the candidate set as coverage.

**What did not transfer:** the plan does not establish coverage, sufficiency,
collection, pass status or that the chosen tests exercise the symbol. The agent
still has to judge the candidate set and run the tests elsewhere. No timing or
comparative measurement was made, so the reduction in manual inspection is
observed as a workflow change, not a measured effort reduction.

## 6. Claim ceiling

| Level | Status |
| --- | --- |
| Functional consumer | OBSERVED |
| Authentic use on the recorded symbol | OBSERVED |
| Reduced manual inspection or changed verification set | PARTIAL — candidate collection is automated; no measured effort or decision change |
| Independent later-agent reuse | NOT ESTABLISHED |
| Comparative cognitive benefit | NOT ESTABLISHED |
| Longitudinal cognitive development | NOT ESTABLISHED |

## 7. Continuation

The next warranted use is an independent agent applying the plan to a real
change and recording whether it changed the selected or executed verification
set. Do not add execution, coverage inference, test generation or a broader
verification subsystem on this evidence alone. The free-text revisit condition
on the possibility remains `NOT_ASSESSED`; no semantic premise change was
manufactured.
