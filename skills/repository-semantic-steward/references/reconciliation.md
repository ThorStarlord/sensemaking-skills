# RECONCILE / AUDIT — Living memory from engineering evidence

## Trigger

A consequential change to product intent, accepted design, important implementation, tests, migration, failure analysis or incident evidence. Minor edits with no durable knowledge consequence use NO_MODEL_CHANGE.

## Procedure

1. Pin old and current repository revisions. Read the changed-source set and relevant prior claims. A dirty active checkout may be inspected but is not a committed revision.
2. Compare source fingerprints using `semantic knowledge-audit` on a clean checkout of the **current** commit, with `--indexed-ref` set to the old indexed SHA and `--current-ref` to HEAD.
3. If both snapshots are indexed, use `knowledge-query --operation changes --base-ref OLD --target-ref NEW` to inspect recorded set differences. This is not proof of actual semantic consequences.
4. Follow changed evidence to claims/relations, verify original affected code and tests, and check documented product/architecture authority.
5. Choose a disposition per consequential affected claim:
   - **CONFIRM:** current evidence supports the existing interpretation.
   - **REVISE:** correct an unsupported or mistaken interpretation.
   - **SUPERSEDE:** retain historical context and record the replacement.
   - **ADD:** introduce a meaningful new concept, relationship, decision or lesson.
   - **CONTEST:** preserve contradictory sources as unresolved.
   - **NO_MODEL_CHANGE:** no durable change is justified.
6. Edit only the relevant reviewed Git-authored knowledge files and source documents. If a record's interpretation is disputed, never silently change its historical assertion to disguise the conflict.
7. Check structured record integrity, cited paths and epistemic states. Publish the changes through the repository's normal branch/review workflow.
8. At the resulting clean committed SHA, rebuild the index outside the repo, check currentness, and preserve older indexed snapshots for history queries.
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
