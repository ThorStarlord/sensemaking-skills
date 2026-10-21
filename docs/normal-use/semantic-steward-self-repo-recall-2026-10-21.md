# Normal use: Repository Semantic Steward on Sensemaking Skills itself

**Date:** 2026-10-21
**Target repository:** `ThorStarlord/sensemaking-skills`
**Inspected committed baseline:** `main@c2b20176d3ef5b12086bfe236835a2abb155b078` (merged PR #558)
**Scope:** Source-checked RECALL and targeted construction/reconciliation of Skill guidance in the same repository; **not** an independent fresh-agent test, cross-repository transfer or release qualification.

## Actual responsibility and memory reuse

The active agent needed to answer how Sensemaking's main `using-sensemaking` Skill should use the specialized `repository-semantic-steward` **on Sensemaking itself**. Git-reviewed `.sensemaking/knowledge/stewardship.json` already contained `cap:semantic-queries`, `goal:longterm-stewardship`, `inv:source-boundary`, `component:knowledge-store`, `verification:knowledge-tests`, and their explicit relationships. This eliminated any need for a new BOOTSTRAP or general ontology redesign.

RECALL followed the reviewed authored records to their original sources: `docs/adr/0031-persistent-semantic-stewardship.md` for purpose/epistemic authority; `docs/semantic-architecture/persistent-knowledge-cli.md` for the source/index contract; `src/sensemaking_skills/semantic_architecture/knowledge_sources.py` for exact clean-source indexing; `src/sensemaking_skills/semantic_architecture/worktree_context.py` for read-only dirty-worktree disclosure; and `tests/test_semantic_knowledge_self_repo.py` for self-repository CLI smoke coverage. The file/test sources show the selected boundary; test existence is not a claim of passing on the new branch.

**Actual execution boundary:** This session accessed the authoritative GitHub source using the GitHub connector; it did **not** execute an installed `repository-semantic-steward` Skill or run `knowledge-query` locally against a built SQLite snapshot. The read-only source-first fallback described in `references/recall.md` was used. Exact-head CI on the follow-on PR is separate evidence of the CLI's already-implemented self-repo smoke test, not a manual CLI receipt for this session.

## Source mismatch found and corrected

The Steward entrypoint instructed agents to use a clean separate worktree when dirty and said its entire CLI example required a clean checkout. These descriptions conflated **source-pinned index construction** with **querying an already indexed revision**. The referenced source and tests explicitly support `knowledge-query --repo .` while the active checkout is dirty, with `workspace_context` marking unindexed source edits. The general `using-sensemaking` entrypoint also described the Steward mainly as a multi-session tool, obscuring ordinary same-repository use. `STATUS.md` still called the already merged PR #558 active.

Bounded changes: clarify the two Skill entrypoints and a self-repository CLI example; reconcile STATUS and the CLI documentation with merged PR facts; add a focused mechanical Skill/knowledge contract regression test. No new planner, runtime, semantic-search inference or construction campaign is authorized.

## RECONCILE disposition

**ADD one reusable, source-linked invariant** `inv:index-snapshot-vs-working-overlay` plus its `constrained_by` edge to `cap:semantic-queries`. This directly addresses the reusable mistaken assumption revealed in this development responsibility, without promoting current working-tree content into indexed authority. Other existing claims are **CONFIRM** at their source-existence/selected-strategy ceilings, not independently reverified runtime truths. No unrelated knowledge records were rewritten.

## Evidence and limits

- This is a repository-local, source-first self-application trace, not measured architectural decision improvement or longitudinal knowledge compounding.
- PR #558's [Product Validation](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/39535941094) and [Release Candidate Distribution](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/39535941107) passed at its recorded final feature head. They do not qualify this follow-on change; use its own exact-head PR checks.
- Missing indexed alternatives or `--expect-kind` coverage do not establish global absence or semantic completeness. Fresh independent-agent use and release gates remain deferred under the Construction Phase.
