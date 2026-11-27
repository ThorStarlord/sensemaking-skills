# P3 direction proposal v1 (for independent criticism)

Repository `ThorStarlord/sensemaking-skills`, `origin/main` at
`baaec6b92f87a00dbcefdbf865da04f86d5ce59f`. Author: the planner
(`claude-fable-5-2`). Status: a proposal. Nothing is built.

## Decision question

Is there a user outcome that Sensemaking Skills cannot yet deliver reliably
and that warrants a minimum construction now? If so, which one?

"No candidate justifies construction" is an acceptable answer.

## Proposed direction: pending-change commitment review

**Outcome.** An owner or a coding agent can review any unmerged line of work
in decisions, not diffs:

1. what the change would commit the product to: the decision, alternative,
   rule, invariant and contract records it adds, revises or removes, each with
   its authority (`owner`, `delegated`, ...) and disposition (`rejected`,
   `deferred`, ...);
2. which standing commitments its changed files touch;
3. where it changes behaviour while recording no commitment at all;
4. for several pending lines at once: records written by more than one of
   them, shared files, and textual conflicts.

**Beneficiary and moment.** The high-delegation owner at the merge decision,
and an agent before it designs work that overlaps something pending.

**Classification by the planner.** A new user-facing question about a new
subject (unmerged work) inside the current product thesis. It recombines
existing mechanisms. It is NOT claimed as a new product end.

## Evidence offered (verify each against the repository)

- E1. Seven pull requests are open. Earlier session notes say merge order is
  the owner's call. `git merge-tree` shows a textual conflict between the
  heads of PRs 795 and 796, and between PR 797 and `main`.
- E2. In `.sensemaking/knowledge/*.json` on `main`, decisions by
  `authority_kind` are: delegated 7, owner 2, policy 1, document 1. Three more
  delegated decisions sit in open PRs (796, 797, 801).
- E3. The archive's own top-ranked residual question is owner understanding
  and agency after an agent has authored the option space
  (`docs/explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md`,
  section 6, item 1), with the caution that it does not imply a dashboard.
- E4. `docs/normal-use/2026-11-10-frontier-04-semantic-continuity.md` found
  that record content duplicated PR text, so records changed no decision. Facts
  aggregated across pending PRs exist in no single PR text.
- E5. The head of PR 797 records `observation:no-query-receipt-after-2026-10-30`:
  a recording duty that depends on agent discipline lapsed. A projection
  derived from Git needs no extra agent duty beyond the records themselves.
- E6. A read-only probe over today's open PR heads (output below) shows:
  the per-PR commitment delta is small and readable; PR 795 changes the
  retrieval code and records no decision; record-level overlap across PRs adds
  nothing beyond Git today; the path-level "records citing changed files" list
  is noisy (22 to 85 claims) when a pack file or a large shared doc changes.

## Nearest existing surfaces

- `semantic knowledge-query --operation changes` with `change_classification`,
  between two revisions indexed in one database;
- `--operation workspace-impact` and `--operation context-for`;
- the `change-impact-analysis` Skill and its artifact;
- `journey delta` and `strategy compare` for strategic artifacts;
- the decision note in each PR description;
- `scripts/summarize-receipts.py` open questions; `owner-decision-capsule`.

## Novelty claim to test

Not found among the 59 DE/NX/RP labels, the seven GD families or the 19
`poss:` records (searched for in-flight, unmerged, concurrent, parallel,
merge order, delegated ledger, ratification). Closest neighbours: DE-B3
decision-language translation, DE-E3 design-judgment inheritance,
`poss:assumption-aware-opportunity-ecology`,
`poss:construction-time-possibility-reconciliation`.

## Minimum realization sketch (not a design commitment)

A read-only command that reads authored packs at the merge-base and at the
head from Git objects (no index, cache, checkout or network), reports the
record delta and the facts above as JSON and as owner-readable Markdown, and
makes no ranking, merge recommendation or semantic verdict.

## Weaknesses the planner already sees

- W1. It is a composition a capable agent can script in minutes.
- W2. Owner demand is inferred, not observed.
- W3. Its value depends on agents writing records in their PRs (three of five
  probed PRs did).
- W4. Path-level matching is noisy.
- W5. It could encourage record ceremony.
- W6. It may be coordination machinery the repository has said not to open
  without recurring pressure.
- W7. It may be recency anchoring: the planner hand-fenced three open PRs in
  the previous session.

## Alternatives the planner considered and declined

- A1. An independent-critic capability: guidance only; behaviour unverifiable.
- A2. Memory of abandoned work (closed, unmerged lines): no incident evidence;
  needs the GitHub API.
- A3. A worker-contract capability for cheaper models: risks becoming an
  execution factory; overlaps the Execution Interface.
- A4. A ledger of product claims against demonstrated evidence: exists as an
  inventory document.
- A5. Cost-aware planning memory in receipts: the receipt schema is under a
  proposed ADR and an open PR.
- A6. A cross-PR semantic overlap map as the main feature: the probe showed
  noise.
- A7. No construction.

## Probe output (planner's scratch script; open PR heads at 2026-11-10)

```text

=== PR 795  merge-base 53b667c1  files 8
   existing records citing changed files: 22 claims {'alternative': 1, 'arch': 1, 'cap': 2, 'component': 5, 'conseq': 2, 'decision': 3, 'incident': 1, 'inv': 2, 'lesson': 2, 'poss': 2, 'verification': 1}; uncited changed paths: 2
   standing commitments touched: ['decision:granular-indexed-delta-classification', 'decision:index-from-temporary-worktree', 'decision:workspace-impact-path-overlap', 'inv:bounded-query-disclosure', 'inv:index-snapshot-vs-working-overlay']

=== PR 796  merge-base 53b667c1  files 12
   + alternative:authored-anchoring-only [alternative; authority=delegated]
   + alternative:capability-hop-into-context-categories [alternative; authority=delegated]
   + decision:relevance-candidates-separate-from-context [decision; authority=delegated]
   + observation:ownership-edit-stranded-store-verification [observation; authority=document]
   ~ lesson:source-anchored-context-reentry [lesson]
   existing records citing changed files: 35 claims {'alternative': 3, 'cap': 2, 'component': 6, 'contract': 1, 'decision': 4, 'goal': 1, 'incident': 3, 'inv': 3, 'lesson': 7, 'observation': 1, 'poss': 1, 'verification': 3}; uncited changed paths: 4
   standing commitments touched: ['contract:semantic-query-receipt', 'decision:granular-indexed-delta-classification', 'decision:index-from-temporary-worktree', 'decision:proposal-check-existence-only-endpoints', 'decision:workspace-impact-path-overlap', 'goal:longterm-stewardship', 'inv:bounded-query-disclosure', 'inv:index-sna

=== PR 797  merge-base 53b667c1  files 7
   + alternative:query-records-its-own-receipt-entry [alternative; authority=delegated]
   + alternative:retrieval-tallies-from-receipts [alternative; authority=delegated]
   + decision:reader-reports-query-recording-facts [decision; authority=delegated]
   + observation:no-query-receipt-after-2026-10-30 [observation; authority=document]
   existing records citing changed files: 80 claims {'alternative': 5, 'arch': 1, 'bounded_context': 2, 'component': 20, 'conseq': 1, 'contract': 5, 'decision': 5, 'layer': 5, 'lifecycle_state': 2, 'observation': 12, 'poss': 1, 'rule': 10, 'verification': 11}; uncited changed paths: 2
   standing commitments touched: ['contract:architectural-synthesis', 'contract:receipt-schema', 'contract:repository-sensemaking-brief', 'contract:semantic-query-receipt', 'contract:workflow-orchestration-plan', 'decision:committed-history-identifies-unrecorded-skill-copies', 'decision:comparison-level-guidance', 'decision:inst

=== PR 801  merge-base baaec6b9  files 7
   + alternative:ephemeral-index-per-query [alternative; authority=document]
   + alternative:implicit-index-in-knowledge-query [alternative; authority=document]
   + alternative:snapshot-from-git-objects [alternative; authority=document]
   + decision:workspace-query-derived-commit-index [decision; authority=delegated]
   ~ component:semantic-cli [component]
   existing records citing changed files: 85 claims {'alternative': 6, 'bounded_context': 2, 'cap': 1, 'component': 20, 'contract': 5, 'decision': 8, 'hyp': 1, 'inv': 1, 'layer': 5, 'lesson': 2, 'observation': 11, 'poss': 2, 'rule': 10, 'verification': 11}; uncited changed paths: 1
   standing commitments touched: ['contract:architectural-synthesis', 'contract:receipt-schema', 'contract:repository-sensemaking-brief', 'contract:semantic-query-receipt', 'contract:workflow-orchestration-plan', 'decision:committed-history-identifies-unrecorded-skill-copies', 'decision:comparison-level-guidance', 'decision:gran

=== PR 794  merge-base 53b667c1  files 3
   existing records citing changed files: 0 claims {}; uncited changed paths: 3
   standing commitments touched: []

=== pairwise
795 x 796: same files 4 ['docs/semantic-architecture/persistent-knowledge-cli.md', 'skills/repository-semantic-steward/references/recall.md', 'src/sensemaking_skills/semantic_architecture/knowledge_architecture.py', 'src/sensemaking_skills/semantic_architecture/knowledge_store.py']; records written by both []; shared cited recor
795 x 797: same files 0 []; records written by both []; shared cited records 5; textual conflict in []
795 x 801: same files 2 ['docs/semantic-architecture/persistent-knowledge-cli.md', 'skills/repository-semantic-steward/references/recall.md']; records written by both []; shared cited records 14; textual conflict in []
795 x 794: same files 0 []; records written by both []; shared cited records 0; textual conflict in []
796 x 797: same files 1 ['skills/repository-semantic-steward/references/query-receipt.md']; records written by both []; shared cited records 5; textual conflict in []
796 x 801: same files 2 ['docs/semantic-architecture/persistent-knowledge-cli.md', 'skills/repository-semantic-steward/references/recall.md']; records written by both []; shared cited records 14; textual conflict in []
796 x 794: same files 0 []; records written by both []; shared cited records 0; textual conflict in []
797 x 801: same files 1 ['.sensemaking/knowledge/architecture.json']; records written by both []; shared cited records 73; textual conflict in ['.sensemaking/knowledge/architecture.json']
797 x 794: same files 0 []; records written by both []; shared cited records 0; textual conflict in []
801 x 794: same files 0 []; records written by both []; shared cited records 0; textual conflict in []
```
