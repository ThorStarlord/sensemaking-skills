# Semantic stewardship S5 — Episode A: bounded knowledge-query integrity

**Status:** actual product repair proposed on `feat/s5-knowledge-query-integrity-episode-a`; exact-head qualification pending until hosted checks report; **independent-session S5 outcome NOT TESTED**.  
**Scope:** `ThorStarlord/sensemaking-skills` only, under owner-selected ADR 0031 and the existing S5 roadmap.  
**Before-source identity:** `main@3a20bd80737b5df247791e4ff86256c0b4f54b83` (merged PR #541); both Product Validation and Release Candidate Distribution passed on that prior baseline.  
**Participants:** one active implementation agent in one conversation context. No second coding agent has consumed this record; a fresh Python subprocess is not an independent coding agent.

## Real engineering problem observed before construction

Direct inspection of the source at the above commit, specifically
`src/sensemaking_skills/semantic_architecture/knowledge_store.py`, found two
source-verifiable query-contract defects:

1. `history` and `changes` slice their results according to `limit`, but
   `truncated` was calculated only from the unused top-level
   `found_claims`/`found_relations` lists. That could advertise
   `truncated: false` after omitting revisions or change identifiers.
2. `impact` updated the selected vertex set twice per loop iteration, so the
   second direction could visit vertices introduced by the first. A requested
   `depth=1` could therefore traverse more than one declared edge.

These are **representation/selection failures**, not evidence that a specific
coding agent made a wrong decision or that every past query is invalid.

## Delegated architectural decision and value

Implement the smallest backward-compatible repair in the existing query
function, with no new schema version, control runtime or ontology:

- Interpret `depth` as a maximum of exactly one explicit graph edge per
  frontier expansion in either direction; retain `impact` as candidate
  connectivity, not causal dependency.
- Mark `truncated=true` whenever **any** returned section omits entries,
  including `claim_history` and the six `changes` delta categories.
- Expose `history_total_entries` and `delta_total_counts` so a later
  consumer can explain the incompleteness instead of guessing. Preserve
  existing delta/history payload shapes and Git-ancestry disclaimers.
- Add adversarial tests for the two-hop leakage case, small-limit history,
  multi-claim changes, and full-limit complete results.

This is a concrete product improvement regardless of whether future S5
comparative benefit is demonstrated. The non-derivable lesson is that **result
completeness is itself source/evidence context**, not merely output
presentation; making a bounded result appear complete can silently reverse
the epistemic meaning of absence.

## Evidence / current result ceiling

- Source inspection at the *before* SHA establishes the vulnerable code paths
  and the warranted repair. It does not substitute for a pre-fix test run.
- The candidate implementation and regression tests are in the PR branch.
  Their exact-head CI result is to be attached to the PR before any claim of
  qualified implementation; the prior `main` green workflows do not qualify
  this change.
- A Git-reviewed typed record in
  `.sensemaking/knowledge/stewardship.json` retains this episode's bounded
  decision, incident and lesson. These are source-linked retrospective claims,
  not elevated owner intent or automatic verified facts.
- No fresh independent coding-agent consultation, architectural decision,
  comparison to direct source inspection, end-user observation, merge, release,
  external-target checkout or cross-repository transfer was performed here.

## Episode B — genuine independent-context continuation, NOT executed

A separate coding-agent session must start **without this chat transcript,
prior assistant reasoning or hidden carryover**. The operator may supply only
the repository URL, a pinned revision, an ordinary product objective, existing
repository documents and the CLI/installation instructions that a normal
developer would have. A successful fresh *interpreter* test must not be
substituted for a fresh *coding agent*.

The next executor should:

1. Pin its own exact source SHA, installed Skill/package identity, access scope
   and permitted actions; examine ADR 0031 and the relevant product state.
2. From a clean checked-out source, rebuild the local SQLite index outside
   the repository, query `search` for `query`, `lesson` and
   `incomplete`, then `explain`/`impact` the exact found claim IDs;
   source-check the returned docs, implementation and tests. Capture the
   actual command/JSON outputs, not just a narrative claim of consultation.
3. Establish whether the earlier bounded-query lesson is relevant to a
   **new** consequential, valuable development problem (for example, a query
   consumer or evidence/drift presentation defect found by independent
   inspection). Choose the next action from current evidence rather than
   executing a prescribed feature or inventing a new ontology.
4. Where a real construction responsibility is warranted, implement and
   qualify it. Independently record whether historical knowledge altered,
   prevented or corrected a material architecture decision compared with
   ordinary code/ADR reconstruction. Do not count merely quoting a claim.
5. If any cited source changed, inspect the exact old/new bytes and use
   `semantic knowledge-audit` before relying on that old claim. Reconcile
   changed or rejected authored knowledge through Git-reviewed source and
   preserve historical rationale. Do not silently overwrite owner intent.
6. Return an exact SHA, independent session/executor identity, PR or code
   outcome, knowledge query output, source checks, decision effect,
   omission/maintenance cost and an honest disposition: `CONSEQUENTIAL_REUSE`,
   `CORRECTED_OR_REJECTED`, `NO_BENEFIT`, `UNEXECUTED` or `INVALID`.
   These labels are observation summaries, not a new runtime enum.

A later independent Episode C can introduce a separate source/architecture
change, repeat with fresh context and check for staleness or contradiction.
The source history should remain queryable even when a newer correction
supersedes a lesson. A useful case of rejecting stale knowledge is just as
important as a correct reuse case.

## Evidence needed before claiming S5 or entering S6

An S5 success requires a later independent coding agent to **use, correct,
or reject consequential earlier knowledge** while completing a real task and
to show the decision impact with exact source/revision evidence. A simple
retrieval response, mock subagent, same-chat restart, synthetic fixture, or
additional green mechanical test is NOT an S5 success. Compare to cheaper
direct-source reconstruction where possible; avoid a causal advantage claim
without adequate isolation. If repeated retrieval is misleading, too costly,
or unused, adapt the model rather than promoting the thesis.

Only after meaningful S5 observation may a separately scoped S6 pilot test a
second authorized product/repository, independently pinned sources, different
domain/language structure and cross-namespace/authority isolation. S6 is
**not started** by this Episode A record.

**Authority:** This record is a normal-use product observation and selected
bounded implementation rationale. It does not approve merges, release,
deployment, new executor access or Level-4 thesis revisions.
