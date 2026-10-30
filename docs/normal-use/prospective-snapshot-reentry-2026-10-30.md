# Prospective re-entry: using a prior indexed snapshot

## Decision

After the discovery-memory change merged at
`921cbb64ef0a37c70117f260c7da29b0b54585a4`, the next real choice was whether
to rebuild the index immediately before checking the merged work or use the
existing `7050dd84869bceeeef6e8add460cd1fde89a46d1` snapshot with current
workspace and source checks. This is a second, distinct application of retained
architectural reasoning, not an independent session or a benchmark.

The retained `inv:index-snapshot-vs-working-overlay`,
`decision:index-from-temporary-worktree` and
`decision:workspace-impact-path-overlap` made the available mechanisms and
their limits explicit. The context for `knowledge_sources.py` also returned the
previous alternatives `alternative:dirty-tree-byte-audit` and
`alternative:shared-clone-checkout`; the separate `worktree_context.py` path
had ownership and decisions `NOT_ASSESSED`. That gap is not a claim that the
component has no owner or decision.

## Comparison and consequences

1. **Reuse the pinned snapshot, inspect workspace and originals.** This makes
   the old graph available immediately, but only as committed-revision data;
   changed and uncited paths still need inspection.
2. **Build the current clean revision, or use the existing temporary checkout
   option for a dirty workspace.** This gives a current committed snapshot, at
   build cost; it still cannot index an uncommitted overlay or establish semantic
   truth. It is warranted when the updated graph itself must be queried.
3. **Treat dirty bytes as an exact-source index.** The earlier rejected
   dirty-tree audit alternative would undermine source identity and was not
   chosen. The temporary-checkout option preserves the clean-source boundary.

For the present check, option 1 was sufficient. The actual old-ref query with
`--repo .` returned `head_matches_indexed_ref: false`, a clean worktree and
`uncommitted_changes_not_indexed: false`; it did not present the snapshot as
current. `workspace-impact` reported one changed, uncited file and zero
affected reviewed records. Git comparison showed that file was this episode's
normal-use report; current source inspection confirmed the workspace-context
and path-overlap mechanics. An uncited file is a coverage gap, not proof of no
semantic effect; its contents were inspected for this decision. The query
excludes submodule working-tree state and disables configured external filters.

Conditional consequences reinforce that choice: forcing an index rebuild for
every continuation could spend time while leaving dirty-overlay semantics
unresolved; always trusting an old index could miss changed knowledge. The
existing combination of pinned retrieval, disclosed mismatch, path-level
reinspection and clean or temporary rebuild when needed addresses this bounded
case. If the changed path or its sources had altered the applicable knowledge,
source reconciliation and a current committed index would become relevant.
No new consumer behavior or authored record is warranted by this observation.

## Evidence and limits

At the earlier indexed commit, the agent queried `explain` on the invariant,
`context-for` on the two implementation paths and `workspace-impact` with the
merged checkout as `--repo .`. It inspected
`docs/semantic-architecture/persistent-knowledge-cli.md`,
`src/sensemaking_skills/semantic_architecture/worktree_context.py`,
`src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py`, and the
Git diff. The retrieval shaped the comparison by preserving the rejected dirty
audit and temporary-checkout alternative; it does not demonstrate that an
independent agent would make a better choice. Native Skill invocation and
comparative or longitudinal benefit remain unassessed.
