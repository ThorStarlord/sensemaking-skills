# Normal use: Steward RECALL -> workspace-impact construction -> RECONCILE

**Date:** 2026-10-21
**Target repository:** `ThorStarlord/sensemaking-skills`
**Indexed baseline:** `main@62a6920a94242a36a0da58a860ecf2683fc1493f` (merged PR #559)
**CLI used:** `sensemaking-skills 1.0.0rc5.dev0` installed in an isolated `uv tool run` environment from `git+https://github.com/ThorStarlord/sensemaking-skills.git@62a6920a...`, Python 3.14, `click==8.3.1`, `PyYAML==6.0.3`. The global `sensemaking-skills` on `PATH` was an older build without `--term`, `--expect-kind` or `--repo`, which is exactly the case the Steward's "verify and pin the CLI" section describes.
**Scope:** same-session construction in the active checkout; **not** an independent fresh-agent test, cross-repository transfer or release qualification.

## Execution receipts

- The `repository-semantic-steward` Skill was copied into the Claude Code user Skill root from the pinned package tree (identical to the repository tree modulo line endings). The harness did not list it until later in the session; it was then invoked through the Skill tool. `using-sensemaking` was invoked from its existing installed copy.
- `knowledge-orient` and `knowledge-build --include-repository-structure` ran at the clean baseline: 533 claims / 493 relations, digest `001af864...`, SQLite stored outside the checkout.
- RECALL used `explain` on `goal:longterm-stewardship`, `cap:semantic-queries` (with `--expect-kind alternative --expect-kind verification`), `inv:index-snapshot-vs-working-overlay` and `inv:source-boundary`; `why` on `decision:incremental-bootstrap`; a multi-`--term` search; and `contradictions` (no explicit contradictions recorded; NOT ASSESSED beyond that).

## What RECALL changed in the engineering decision

The retrieved records were followed to `knowledge_store.py`, `knowledge_sources.py`, `worktree_context.py`, `reconciliation.md` and the CLI contract. Two facts constrained the selection:

1. `inv:index-snapshot-vs-working-overlay` and `verified_tracked_sources` mean `knowledge-audit` (byte-level drift) is deliberately unavailable while the checkout is dirty.
2. RECONCILE step 1 tells the agent to "inspect changed code and existing knowledge through `knowledge-query --repo .`", but `workspace_context` only reports counts. Nothing mapped "files I edited" to "reviewed records citing them" during active work; the agent had to grep JSON by hand.

The selected responsibility was therefore a read-only `workspace-impact` query operation. The invariant ruled out the tempting alternative of making `knowledge-audit` accept a dirty tree (hashing uncommitted bytes would present the overlay as compared evidence). The design keeps the overlay unread: it matches **path names** from `git diff --no-renames <indexed_ref>` plus untracked paths against each indexed record's `source_sha256` keys.

`bounded_coverage` for `cap:semantic-queries` also reported `alternative` as NOT ASSESSED in its neighborhood: no rejected design alternative had been recorded anywhere in the stewardship pack.

## What the new operation reported on its own change

Run from the dirty implementation checkout against the baseline index, `workspace-impact` listed five reviewed records whose cited files changed (`component:knowledge-store`, `inv:bounded-query-disclosure`, `inv:index-snapshot-vs-working-overlay`, `rel:query-implemented`, `rel:query-snapshot-overlay-boundary`) and counted eight mechanical path matches separately.

It also exposed a coverage gap: `knowledge_retrieval.py` (search, coverage and now overlap logic) and `semantic_cli.py` (the query interface) changed, yet no reviewed record cited either file. Without the operation, an empty result for those files could have been read as "no knowledge affected".

## RECONCILE dispositions

- `component:knowledge-store`: **REVISE** evidence scope to include `knowledge_retrieval.py`, which the store imports for search, coverage and workspace overlap. Statement unchanged.
- `inv:bounded-query-disclosure`: **CONFIRM**. The new operation reports `affected_record_total` and `truncated`.
- `inv:index-snapshot-vs-working-overlay`: **CONFIRM**. The operation reads no overlay bytes (`overlay_indexed=false`); its tests are added as evidence.
- **ADD** `decision:workspace-impact-path-overlap`, `alternative:dirty-tree-byte-audit` (rejected) and `lesson:uncited-change-is-coverage-gap`, with explicit relations.
- Other records: **NO_MODEL_CHANGE**.

## Limits

Same-session use and local tests establish implementation behavior at the tested revision only. Whether a later independent agent uses `workspace-impact` or the new lesson is NOT TESTED (Issue #552 remains release-stage qualification). Path overlap cannot see semantic effects on records whose evidence lives in uncited files.
