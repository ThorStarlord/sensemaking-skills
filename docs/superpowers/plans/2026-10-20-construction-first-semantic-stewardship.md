# Construction-First Semantic Stewardship Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking. **Execution selection for this project: native execution in the current agent context, with local tests and incremental commits; no fresh-context subagents are required during construction.**

**Goal:** Make Sensemaking's existing source-linked knowledge practically useful during ordinary coding in the current workspace: expose honest working-tree freshness, improve targeted recall, disclose gaps in retrieved decision context, and retain consequential lessons through normal commits.

**Architecture:** Extend the existing Click semantic CLI and SQLite-backed `query_knowledge` function in backward-compatible slices. Keep authored knowledge in reviewed Git JSON, indexes rebuildable outside the repository, and interpretation/authority with the active coding agent. No new planner, ontology service, mandatory workflow, agent executor, schema version or retrieval infrastructure is introduced.

**Tech Stack:** Python >=3.11, Click, sqlite3, Git CLI, pytest, repository Markdown and JSON.

**Spec:** `docs/adr/0031-persistent-semantic-stewardship.md`, `docs/persistent-semantic-stewardship-plan.md`, `docs/semantic-architecture/persistent-knowledge-cli.md`, `skills/repository-semantic-steward/SKILL.md` and `skills/repository-semantic-steward/references/recall.md`. This plan incorporates the owner's October 20, 2026 construction-mode correction.

**Source inspected for planning:** `main@76742d4a72daf4334621d657fa27bc9de13b60ba` (October 19). Rebase/inspect current source at execution; exact line ranges below are navigation aids, not authority to overwrite newer work.

## Global Constraints

- **Construction now.** Use the current working tree, current agent context, ordinary source inspection, local red/green tests, incremental commits and practical feature dogfooding. No mandatory clean-room evaluation, blinded comparison, fresh coding-agent handoff, synthetic benchmark or owner questionnaire during feature development.
- **Release later.** Preserve independent-agent, portability and comparative claim ceilings as **NOT ESTABLISHED**, with qualification deferred to an explicitly initiated release gate. Do not mark Issues #552/#554 passed merely because code and same-session tests work.
- **Preserve source truth.** `knowledge-build` still indexes only a clean, exact committed HEAD; **do not relax this**. A dirty current checkout may query an existing committed index and run `knowledge-proposal-check`, but all uncommitted bytes remain an unindexed overlay. Never force an extra clean worktree or agent session to implement features; commit at a natural slice boundary before rebuilding.
- **Preserve authority.** Authored knowledge, lexical matches, path containment, successful tests and graph edges never grant owner intent or permission to merge, deploy, release or rewrite ADRs. ADR 0029 and ADR 0031 remain authoritative.
- **Compatibility.** Existing `knowledge-query` calls, JSON keys, SQLite schema version 1, authored `.sensemaking/knowledge/*.json` and query defaults must remain valid. New options and output fields are additive.
- **Proportionality.** Fix observed retrieval friction first. No LLM search, embeddings, ontology v2, universal TypeScript/SQL adapter, duplicate artifact/decision store, automatic relevance adjudication or new orchestration layer.
- **Verification.** Run focused tests before each implementation commit; complete the local full suite plus existing docs/contract validators at the end. Hosted CI is useful when available but is not an independent-agent experiment or a prerequisite to a local construction commit.
- **Scope.** Only `ThorStarlord/sensemaking-skills`. Auteur observations provide motivating examples; do not modify Auteur or Dark Factory as part of this plan.
- **Terminal boundary.** The plan permits normal repository implementation and commits; it does not implicitly authorize merging a PR, publishing a release, modifying GitHub branch rules, billing, credentials or other protected external actions.
- **Windows compatibility.** Do not introduce Unicode-only console strings into this repository's Windows-sensitive output path. Structured JSON can escape Unicode safely.

## Review Focus

1. **Dirty working tree:** querying an already indexed HEAD from an actively edited workspace must succeed while visibly warning that uncommitted changes were not indexed; never silently equate local bytes to recorded evidence. Pin in Task 2.
2. **Different current HEAD:** a historical index requested from a newer checkout must remain queryable but explicitly be labeled as historical, not current. Pin in Task 2.
3. **Query limits:** category omission caused by `--limit` must be distinguishable from a category not encountered in the bounded neighborhood; no completeness inference. Pin in Task 4.
4. **Retrieval false negatives and false positives:** explicit multi-phrase search must remain literal and deterministic, disclose total hits/truncation and never infer synonyms or authority. Pin in Task 3.
5. **Compatibility and CLI errors:** existing flags/output remain stable; invalid option combinations or unknown claim kinds fail clearly, without partial writes or false-success output. Pin in Tasks 2–4 and full-suite verification.

## File / Responsibility Map

| Surface | Exact files | Responsibility |
| --- | --- | --- |
| Current operational strategy | `STATUS.md`, `docs/persistent-semantic-stewardship-plan.md`, `docs/semantic-architecture/repository-bootstrap.md` | Describe construction as current work without rewriting historical experiments or inventing a release PASS |
| Worktree observation | **Create** `src/sensemaking_skills/semantic_architecture/worktree_context.py`, **create** `tests/test_semantic_worktree_context.py` | Read Git working-state metadata without treating it as indexed evidence |
| Query CLI wiring | `src/sensemaking_skills/semantic_cli.py` | Add opt-in `--repo`, `--term` and `--expect-kind` to the existing `knowledge-query` command |
| Query semantics | `src/sensemaking_skills/semantic_architecture/knowledge_store.py`, `tests/test_semantic_knowledge.py` | Explicit term retrieval, bounded-coverage metadata and accurate truncation |
| Real CLI integration | `tests/test_repository_bootstrap.py`, `tests/test_repository_semantic_steward.py` | Exercise old/new CLI invocation and safe draft-to-committed-knowledge flow |
| Agent consumption | `skills/repository-semantic-steward/references/recall.md`, `skills/repository-semantic-steward/references/reconciliation.md`, `docs/semantic-architecture/persistent-knowledge-cli.md` | Teach in-context working-tree consultation, explicit alternate-path checks and selective same-session learning |
| Durable learning | `.sensemaking/knowledge/stewardship.json` **only if a genuinely reusable lesson is found** | Preserve a sourced, reviewed distinction; no knowledge-count target |

---

### Task 1: Reconcile Current Construction Posture

**Files**
- Modify: `STATUS.md` (current Level-3 frontier, selected responsibility, next-step and execution-vehicle sections; preserve historical ledger entries).
- Modify: `docs/persistent-semantic-stewardship-plan.md` (candidate-era header, RSB/RSS state and qualification vs construction boundary).
- Modify: `docs/semantic-architecture/repository-bootstrap.md` (implementation status, exact release evidence limits).
- Test: existing `tests/test_strategic_state_validation.py` and documentation validators; **do not add brittle tests asserting transient wording**.

**Interfaces**
- Consumes: ADR 0031, PRs #550/#553/#555/#551/#556/#557 merged on main and open Issues #552/#554.
- Produces: one internally consistent Level-3 construction responsibility: improve active-workspace knowledge use and decision coverage with retained, locally verified code.

- [ ] **Step 1: Inspect and write down the discrepancy** between the current status header and the later sections that still say `CURRENT CONSTRUCTION RESPONSIBILITY = NONE` and `NORMAL_USE_VALIDATION`. Verify the latest Git/PR state, so prior candidate-era prose is not copied as new truth.
- [ ] **Step 2: Reconcile the current Level-3 sections.** State `CONSTRUCTION` as the operating phase and this plan as the bounded responsibility. Treat previous `NO_CHANGE/NORMAL_USE_HANDOFF` as historical control-model disposition; do not rewrite its historical source evidence.
- [ ] **Step 3: Clarify the test split.** Ordinary local tests, in-session real-repository use and commits happen now. Fresh-context trials (#552), bootstrap transfer (#554), and clean-room comparative claims remain release-stage qualifications, not feature-construction gates. Retain their open/unproven state.
- [ ] **Step 4: Run existing documentation checks.** Commands:
  - `python scripts/validate-docs-currentness.py --repo-root .`
  - `python -m pytest tests/test_strategic_state_validation.py tests/test_current_documentation.py -q`
  - `git diff --check`
  Expected: exit 0. If a historical wording-pinned test rejects current reality, inspect its actual consumer and repair the smallest stale expectation without disabling meaningful source/authority checks.
- [ ] **Step 5: Commit:** `git add STATUS.md docs/persistent-semantic-stewardship-plan.md docs/semantic-architecture/repository-bootstrap.md && git commit -m "docs: align semantic stewardship with construction phase"`.

### Task 2: Make Indexed Recall Truthful in a Dirty Current Workspace

**Files**
- Create: `src/sensemaking_skills/semantic_architecture/worktree_context.py`.
- Create: `tests/test_semantic_worktree_context.py`.
- Modify: `src/sensemaking_skills/semantic_cli.py` (`knowledge-query` options at approximately lines 164–191).
- Test: `tests/test_repository_bootstrap.py` for CLI compatibility.

**Interfaces**
- Produces: `inspect_worktree_context(repo_root: Path, indexed_ref: str) -> dict[str, object]` (read-only).
- Produces an **optional**, additive `workspace_context` object on `semantic knowledge-query --repo PATH`; the indexed query itself still reads only the chosen revision in SQLite.
- Required payload keys: `current_head`, `indexed_ref`, `head_matches_indexed_ref`, `worktree_clean`, `modified_tracked_count`, `untracked_count`, `uncommitted_changes_not_indexed`, `source_alignment_not_semantic_truth` (= true). Do not output file contents.
- Consumes: existing `query_knowledge(db_path, repository=..., target_ref=..., ...)` and a local Git working tree.

- [ ] **Step 1: Write failing tests** `test_dirty_current_workspace_query_reports_unindexed_changes`, `test_historical_index_from_new_head_is_labeled_historical`, `test_clean_matching_head_reports_no_unindexed_changes`, and `test_existing_query_without_repo_preserves_payload`. Use temporary Git repositories, exact commits, and the existing snapshot/index fixtures.
- [ ] **Step 2: Run** `python -m pytest tests/test_semantic_worktree_context.py -q`. Expected: RED before the helper/CLI option exists.
- [ ] **Step 3: Implement the read-only Git observer.** Use `git rev-parse HEAD`, tracked modified/staged paths, and untracked path counts with bounded subprocess timeouts. Support standard `.git` directories and linked Git worktree gitfiles. Refuse non-repositories clearly; never execute target code, read file contents, mutate Git, create a clean worktree, or pretend a dirty overlay is committed evidence.
- [ ] **Step 4: Wire `--repo PATH` to `knowledge-query`.** When omitted, preserve the existing result shape exactly. When supplied, append `workspace_context` after a successful normal query. If HEAD differs, mark the indexed revision historical; when dirty, label the uncommitted overlay unassessed rather than refusing the query.
- [ ] **Step 5: Run** `python -m pytest tests/test_semantic_worktree_context.py tests/test_repository_bootstrap.py -q`. Expected: GREEN.
- [ ] **Step 6: Commit:** `git add src/sensemaking_skills/semantic_architecture/worktree_context.py src/sensemaking_skills/semantic_cli.py tests/test_semantic_worktree_context.py tests/test_repository_bootstrap.py && git commit -m "feat(semantic): disclose active worktree context in knowledge queries"`.

### Task 3: Provide Bounded Multi-Phrase Recall Without Semantic Search

**Files**
- Modify: `src/sensemaking_skills/semantic_architecture/knowledge_store.py` (`query_knowledge`, currently near line 155).
- Modify: `src/sensemaking_skills/semantic_cli.py`.
- Modify: `tests/test_semantic_knowledge.py`.

**Interfaces**
- Extend `query_knowledge(..., search_terms: tuple[str, ...] = ()) -> dict` (existing parameters retained).
- Extend CLI `semantic knowledge-query --operation search --term PHRASE --term PHRASE`.
- An explicitly supplied list of 1–8 nonempty phrases (each at most 80 Unicode code points) is a case-folded **literal OR** search in claim ID or statement, not tokenization, embeddings or semantic inference.
- Disallow combining `--term` with `--subject`, and disallow `--term` for non-search operations. With no `--term`, existing literal `--subject` behavior remains unchanged.
- Return additive `search_mode` ("literal" or "explicit_terms_any") and `search_hit_total`; rank multi-phrase hits deterministically by number of matching input phrases descending, then claim ID ascending. Apply existing `--limit` and `truncated` correctly.

- [ ] **Step 1: Write RED tests** `test_explicit_search_terms_return_union_in_stable_relevance_order`, `test_search_term_limit_reports_total_and_truncation`, `test_literal_search_remains_backward_compatible`, `test_invalid_term_operation_or_mixed_subject_fails`. Reuse existing committed fixture and query paths.
- [ ] **Step 2: Run** `python -m pytest tests/test_semantic_knowledge.py -q`. Expected: new tests RED; prior tests remain valid.
- [ ] **Step 3: Implement the minimal query and CLI extension.** Never silently split an arbitrary English question or claim the result set covers architectural alternatives. Search still operates only over indexed statement/ID fields at the selected source revision.
- [ ] **Step 4: Run** `python -m pytest tests/test_semantic_knowledge.py tests/test_semantic_cli.py -q`. Expected: GREEN with stable default behavior.
- [ ] **Step 5: Commit:** `git add src/sensemaking_skills/semantic_architecture/knowledge_store.py src/sensemaking_skills/semantic_cli.py tests/test_semantic_knowledge.py && git commit -m "feat(semantic): support explicit multi-phrase recall"`.

### Task 4: Expose Decision-Context Coverage Limits Without Pretending Completeness

**Files**
- Modify: `src/sensemaking_skills/semantic_architecture/knowledge_store.py`.
- Modify: `src/sensemaking_skills/semantic_cli.py`.
- Modify: `tests/test_semantic_knowledge.py`.

**Interfaces**
- Extend `query_knowledge(..., expected_kinds: tuple[str, ...] = ()) -> dict` (in addition to Task 3's optional search terms).
- Extend CLI `semantic knowledge-query --operation explain|why --subject CLAIM_ID --expect-kind alternative --expect-kind verification`.
- Validate expected kinds against `CLAIM_KINDS` in `knowledge.py`. The option only applies to `explain` and `why`.
- Return an additive `bounded_coverage` object with `requested_kinds`, `present_in_returned_claims`, `present_but_omitted_by_limit`, `not_assessed_in_neighborhood` and `semantic_completeness_established: false`.
- Interpret "not assessed" only for **the bounded, explicitly declared one-hop neighborhood**; do not infer that a fact, alternative, test or dependency is absent from repository reality or even from other unlinked indexed claims.
- Preserve the raw claim and relation arrays, current limits, original source refs, and false authority flags.

- [ ] **Step 1: Write RED tests** `test_expected_kind_present_in_neighborhood`, `test_unlinked_alternative_is_not_assessed_not_absent`, `test_expected_kind_omitted_by_limit_is_disclosed`, `test_unknown_kind_and_wrong_operation_fail` and `test_no_expect_kind_keeps_old_query_shape`.
- [ ] **Step 2: Run** `python -m pytest tests/test_semantic_knowledge.py -q`. Expected: new tests RED.
- [ ] **Step 3: Implement metadata from the full pre-truncation neighborhood** before slicing claims/relations to the requested output limit. Never create fabricated "missing" nodes, assign an evidence score, infer automatic closure, or make `why` apply to non-decision claims.
- [ ] **Step 4: Run** `python -m pytest tests/test_semantic_knowledge.py tests/test_semantic_knowledge_self_repo.py -q`. Expected: GREEN.
- [ ] **Step 5: Commit:** `git add src/sensemaking_skills/semantic_architecture/knowledge_store.py src/sensemaking_skills/semantic_cli.py tests/test_semantic_knowledge.py && git commit -m "feat(semantic): disclose bounded decision-context coverage"`.

### Task 5: Teach the Existing Steward to Use the New Surfaces During Construction

**Files**
- Modify: `skills/repository-semantic-steward/references/recall.md`.
- Modify: `skills/repository-semantic-steward/references/reconciliation.md`.
- Modify: `docs/semantic-architecture/persistent-knowledge-cli.md`.
- Modify: `tests/test_repository_semantic_steward.py` for a realistic CLI/use regression (not a prose-string gate).
- Optional, conditional: `.sensemaking/knowledge/stewardship.json` if implementation revealed a source-checked durable lesson not already represented.

**Interfaces**
- Consumes: Tasks 2–4 CLI behavior.
- Produces: a lightweight same-context usage recipe, not a new artifact schema, mandatory BOOTSTRAP step, background indexer or Skill router.

- [ ] **Step 1: Add a failing realistic usage test** that builds a committed fixture snapshot, performs a knowledge query with `--repo` while the repo is dirty, retrieves multiple explicit terms, and asks for explicit alternatives/verification coverage. Assert revision honesty, query limits and non-authority rather than arbitrary documentation phrases.
- [ ] **Step 2: Run** `python -m pytest tests/test_repository_semantic_steward.py -q`. Expected: RED if the exact CLI combination is not yet wired correctly.
- [ ] **Step 3: Update RECALL.** Use existing committed knowledge opportunistically from the current dirty tree; consult the original changed local code independently; search with one short literal or explicit `--term` phrases; request coverage only for kinds that matter to the current decision; inspect unassessed alternative implementations before declaring a blocker. Reuse the documented Auteur host-agent-first omission as a **bounded example**, not a new user requirement.
- [ ] **Step 4: Update RECONCILE.** Author and preflight knowledge proposals in the same dirty checkout with `knowledge-proposal-check`; commit source/knowledge when tests pass; rebuild and audit at the resulting clean committed SHA. Retain history; `NO_MODEL_CHANGE` is valid when no new reusable knowledge exists.
- [ ] **Step 5: Update the CLI guide**, including a working Windows-friendly example and exact-HEAD/index limitations. No claim that a query returned verified semantic truth or demonstrated independent-agent benefit.
- [ ] **Step 6: Run** `python -m pytest tests/test_repository_semantic_steward.py tests/test_semantic_knowledge.py tests/test_repository_bootstrap.py -q`, `python scripts/validate-skill-hygiene.py` and `git diff --check`. Expected: exit 0.
- [ ] **Step 7: Commit:** `git add skills/repository-semantic-steward/references/recall.md skills/repository-semantic-steward/references/reconciliation.md docs/semantic-architecture/persistent-knowledge-cli.md tests/test_repository_semantic_steward.py`, plus any separately inspected/verified authored knowledge, then `git commit -m "docs(steward): integrate in-session recall and learning"`.

### Task 6: Use the Constructed Slice in This Repository and Close the Local Development Loop

**Files**
- Test: `tests/test_semantic_knowledge.py`, `tests/test_semantic_worktree_context.py`, `tests/test_repository_semantic_steward.py`, `tests/test_repository_bootstrap.py`, the entire repository test suite and current docs/contract validators.
- Modify `STATUS.md` **only if needed** to reflect what actually integrated in the feature branch; preserve integration-vs-branch qualification distinction.
- Modify `.sensemaking/knowledge/stewardship.json` **only when warranted** by a consequential, non-derivable lesson.

**Interfaces**
- Consumes: all five prior tasks.
- Produces: tested committed code, reproducible normal-use CLI receipts, explicit known limitations, and a small reviewable feature PR; no release-stage or comparative conclusion.

- [ ] **Step 1: Before active edits or after a natural local commit, build a normal committed-source index** outside the checkout: `sensemaking-skills semantic knowledge-build --repo . --repository ThorStarlord/sensemaking-skills --target-ref HEAD_SHA --db PATH_OUTSIDE_REPO --json`. Resolve `HEAD_SHA` to the actual 40-character `git rev-parse HEAD`; never pass the literal token.
- [ ] **Step 2: While editing the current workspace, use the existing index without requiring clean worktree:** call `knowledge-query --repo . --operation explain --subject cap:semantic-queries --expect-kind alternative --expect-kind verification` against the committed `HEAD_SHA`. Verify the returned `workspace_context` visibly labels any unindexed dirty changes and unknown coverage.
- [ ] **Step 3: Exercise actual targeted retrieval** with multiple explicit search terms for the repository's real query-integrity lesson. Inspect the cited current source/tests and confirm what the system does **not** establish. This is a normal developer dogfood check, not an independent-agent trial or a synthetic success claim.
- [ ] **Step 4: When genuine new reusable knowledge is found, edit only the affected JSON claims/relations, check with `semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/stewardship.json --json` while dirty, run tests, and commit. Otherwise record `NO_MODEL_CHANGE` in the PR narrative and do not add filler records.
- [ ] **Step 5: Run the complete local product validation** (adjust environment dependencies only as needed for the supported Python 3.11+ installation):
  - `python -m pytest tests/ -q`
  - `python scripts/validate-docs-currentness.py --repo-root .`
  - `python scripts/validate-skill-hygiene.py`
  - `python scripts/validate-release-contract.py --repo-root .`
  - `python scripts/validate-contract-authority.py --repo-root .`
  - `git diff --check`
  Expected: exit 0. If an unrelated baseline defect exists, reproduce it against the same test invocation and report separately; never call a failing suite "passed".
- [ ] **Step 6: Commit any legitimate final fixes** with narrowly scoped paths and meaningful messages. Do not overwrite unrelated workspace changes; do not force a detached or synthetic fresh agent session.
- [ ] **Step 7: On the now-clean committed HEAD, rebuild the local index outside the repo and compare the prior indexed SHA to the new SHA** using `knowledge-query --operation changes` and any relevant `knowledge-audit`. Preserve that indexing order is not Git ancestry proof.
- [ ] **Step 8: Create/update a normal reviewable feature PR** summarizing which code paths changed, tests actually executed, source/currentness caveats, known gaps and practical outcome. Do not merge or release under this plan alone. Clean-room/independent portability testing is a later explicit release responsibility.

## Construction Completion Definition

Feature construction can be declared **locally complete** when:
1. Dirty-workspace recall reports its committed-index/working-overlay boundary without refusing ordinary queries.
2. Default old search and explain calls remain backward compatible; explicit multi-phrase search and bounded requested-kind coverage behave deterministically and report omissions.
3. Real code and source references, not semantic index text alone, govern conclusions about alternatives, constraints and actual behavior.
4. Focused tests plus the full local suite and touched contract/docs validators pass, or any external limitation is explicitly disclosed without a false PASS.
5. Changes are committed in reviewable slices and a proposed PR points to actual source/test evidence.
6. No independent-context, transfer, release-readiness, comparative superiority or owner-authority claim is manufactured from development results.

**Out of scope for this construction plan:** run of Issue #552 Episode B; RSB-6/#554 independent qualifier; sealed Trial 002/002R/#515; CI-gated final release; standalone semantic-search infrastructure; ontology-v2/schema migration; automatic graph-knowledge synthesis; cross-repository transfer; Dark Factory runtime integration; merge/protected GitHub administration.

## Execution Order, Stops and Decision Trace

**Order:** Task 1 documentation coherence -> Task 2 dirty-workspace truth -> Task 3 explicit search fallback -> Task 4 bounded decision coverage -> Task 5 agent consumption -> Task 6 same-session construction verification and commits.

**Most conservative alternative rejected:** do more synthetic/fresh-agent evaluation before writing useful code. This would not advance the selected product capability during the explicitly owner-selected construction phase.

**Most aggressive alternative rejected:** build a broad semantic assistant, full ontology ingester, embeddings and autonomous decision engine. Current evidence supports smaller, backward-compatible improvements and does not warrant another semantic controller.

**Stop only for:** a hard scope/authority boundary, a genuine unsupported source assumption that changes the implementation contract, a persistent test failure requiring a different responsibility, or successful local completion. Do not stop merely because an independent evaluator is unavailable.

**Release handoff (future):** after the feature set is stable and the owner starts release qualification, re-evaluate clean-room source reconstruction, independent agent utility, portability and comparisons under their existing separate issues. This handoff is a later gate, **not** a condition for the construction commits above.
