# Persistent Semantic Knowledge — first-use qualification record

**Scope:** This repository's owner-selected ADR 0031 knowledge product, source-bound
first slice on PR #550 (stacked on strategy PR #549).
**Evidence:** exact committed source plus GitHub hosted CI; no real-user study,
independent model session, external target checkout or longitudinal outcome claim.

**Post-merge currentness (2026-10-15):** Strategy PR #549 merged as
`3ca44d0433d048ecbe5e75772b6d4f35266d41b6`; knowledge PR #550
merged as `28258413a11dd72d28f5c02f0e3abbd51dc5c55c`. The subsequent
five-PR integration reached `main@3a20bd80737b5df247791e4ff86256c0b4f54b83`;
its [Product Validation](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/38822699678)
(seven passing jobs) and
[Release Candidate Distribution](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/38822699683)
passed. The original text below retains its candidate-era evidence limits.
[Episode A](semantic-stewardship-episode-a-2026-10-15.md) is a distinct,
later knowledge-query repair and **not** proof of independent-agent learning.

## What now exists

The code uses the existing Semantic Architecture package without creating a new
semantic controller, Campaign contract or custom coding-agent runtime.

- S1: Typed source-bound claims, explicit edges, provenance, epistemic states,
  authorization boundaries, record/schema validation.
- S2: Exact clean-Git source inspection for tagged Grounding Pack claims, ADR
  title/status + bounded literal rationale excerpts, reviewed authored JSON,
  opt-in mechanical Python import observations, source SHA-256 fingerprints.
- S3: Local SQLite index outside the checkout; multi-revision persistence,
  rebuild-on-same-commit determinism, source-drift audit, search/explain/why/
  impact/contradictions/history/changes queries and bounded results.
- S4: Existing Skills mention optional semantic queries for architectural
  exploration, consequence analysis and durable knowledge reconciliation.
- S5 mechanical prerequisites: exact-head self-repository worktree smoke and
  a second *Python process* fetching persisted knowledge. Neither implies a
  second coding agent nor that the agent used history to make a better decision.
- S6 early safeguards: repository-namespaced index records, bounded optional
  import observation, no cross-repository authority merger. Real semantic
  transfer across independent products is NOT TESTED.

The reviewed, real example at
[.sensemaking/knowledge/stewardship.json](../../.sensemaking/knowledge/stewardship.json)
connects the actual ADR 0031 goal, a capability in the implementation,
a source-authority invariant, actual code and test surfaces, historical ADR 0030
grounding quality evidence, and source-cited edges. These are **declared** links:
they are inspectable but do not prove architecture completeness or benefit.

## Real-repository query to inspect

From a clean checkout at the PR's exact HEAD, in an environment with the
installed package, run:

    REF="$(git rev-parse HEAD)"
    sensemaking-skills semantic knowledge-build --repo . \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$REF" --db /tmp/sensemaking-knowledge.sqlite --json

    sensemaking-skills semantic knowledge-query \
      --db /tmp/sensemaking-knowledge.sqlite \
      --repository "ThorStarlord/sensemaking-skills" --target-ref "$REF" \
      --operation why --subject "adr:0031" --json

    sensemaking-skills semantic knowledge-query \
      --db /tmp/sensemaking-knowledge.sqlite \
      --repository "ThorStarlord/sensemaking-skills" --target-ref "$REF" \
      --operation impact --subject "cap:semantic-queries" --json

The exact-head self-worktree integration test actually calls this builder and
queries the index using repository sources, without depending on this chat.

## Evidence boundaries and continuation

- A passing test validates mechanics and selected sources, not whether ADR
  decisions are wise, whether the ontology is comprehensive, or whether
  retaining a relationship improves a later architectural decision.
- A clean worktree cannot be assumed for user projects; a dirty checkout
  produces a refusal rather than indexing unbound bytes as a committed SHA.
- A historical record is evidence at its original source revision. Run
  knowledge-audit in a new clean checkout to inspect changed/missing cited
  files. Changed bytes require reassessment, **not automatic revocation**.
- Prescriptive authority stays with approved product/owner/ADR records.
  Authored semantic JSON must not claim verified authority merely by asserting
  an owner tag. Skills and the active agent interpret source evidence.
- There is **no longitudinal independent-agent PASS**. The only legitimate
  next step for S5 is later genuine construction by distinct agents/sessions
  that correctly reuse, reject or update a consequential earlier decision.
- Cross-product/domain adapter expansion (S6) is a meaningful future
  implementation task when a real target exposes a missing representation.
  Adding arbitrary ontology families now would not complete that evidence.

**Disposition:** S1-S4 candidate implementation under normal PR qualification,
S5/S6 broader product outcomes **NOT ESTABLISHED**. Do not convert this record
into mandatory ontology indexing for routine tasks or claim a finished
autonomous knowledge-compounding platform.
