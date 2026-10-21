# RECONCILE / AUDIT — Living memory from engineering evidence

## Trigger

Consequential new evidence about product intent, accepted design, important implementation, tests, migration, failure analysis or incidents. A corrected test assumption or a task blocked by an overlooked architectural alternative can justify a durable lesson **without changing product code**. Minor edits and unsurprising confirmations with no reusable consequence use NO_MODEL_CHANGE.

## Procedure

1. Pin the prior indexed revision and current Git HEAD. **Continue in the active checkout and context**, including while it is dirty. Inspect changed code and existing knowledge through `knowledge-query --repo .`; the workspace metadata says whether the index is historical or local changes are unindexed. `--operation workspace-impact --repo .` lists the reviewed indexed records whose cited source files changed since the indexed revision (committed or not), separating an edited record definition from changed evidence; treat the list as re-inspection candidates, and changed code that no record cites as a possible coverage gap, not as unaffected knowledge. A dirty checkout is never a committed source revision.
2. Do not create a clean-room development session just to proceed. After an ordinary code/knowledge commit, at the naturally clean current HEAD, compare source fingerprints with `semantic knowledge-audit --indexed-ref OLD_SHA --current-ref HEAD_SHA`. Source drift does not automatically invalidate historical decisions.
3. If both snapshots are indexed, use `knowledge-query --operation changes --base-ref OLD --target-ref NEW` to inspect recorded set differences. This is not proof of actual semantic consequences.
4. Follow changed evidence **and consequential newly understood evidence** to claims/relations, verify original affected code and tests, and check documented product/architecture authority. Do not assume only changed source files can teach something worth retaining.
5. Choose a disposition per consequential affected claim:
   - **CONFIRM:** current evidence supports the existing interpretation.
   - **REVISE:** correct an unsupported or mistaken interpretation.
   - **SUPERSEDE:** retain historical context and record the replacement.
   - **ADD:** introduce a meaningful new concept, relationship, decision or lesson.
   - **CONTEST:** preserve contradictory sources as unresolved.
   - **NO_MODEL_CHANGE:** no durable change is justified.

   Distinguish *no existing claim was falsified* from *nothing reusable was learned*. Before selecting NO_MODEL_CHANGE after a repaired test, incorrect blocker inference or architecture rediscovery, ask whether a future agent would plausibly repeat the mistake without one source-linked invariant, decision link or lesson. Use **ADD** only if the distinction is stable, decision-relevant, source-supported and not already represented. A successful no-change run is not a quota failure.
6. Edit only the relevant reviewed Git-authored knowledge files and source documents. If a record's interpretation is disputed, never silently change its historical assertion to disguise the conflict.
7. In the active dirty checkout run `semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/NAME.json --json` to preflight reviewed draft records. Run relevant local code tests; commit source and knowledge in the repository's normal feature-branch workflow. No fresh-context handoff is required after every commit.
8. At the resulting **naturally clean committed SHA**, rebuild the index outside the repo, check currentness and preserve older snapshots. Exact committed indexing requires clean bytes; dirty-worktree querying and feature construction do not.
9. Report affected domains, corrections, remains-unknown evidence, tests actually run, and where future agents should look for the reasoning.

## Memory hygiene

- Separate lexical imports and path containment from semantic dependencies.
- Avoid endless duplicate incident lessons and obsolete active claims.
- Reuse stable identifiers for the same entity through versions, but use distinct identifiers for genuinely different concepts.
- Distinguish a historical decision that was valid then from an error in the original interpretation.
- Never infer a successful verification because a test file exists or a PR mentions a green check.
- Use explicit source-revision identities for third-party issues/PRs when evidence matters.
- If concurrent work changes the same authored pack, reconcile Git conflicts through source inspection rather than overwriting another agent's knowledge.

AUDIT returns currentness/coverage findings without mutating the record; reconciliation is a separate meaning judgment.
