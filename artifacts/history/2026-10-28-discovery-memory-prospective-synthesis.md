# Prospective Synthesis: Discovery Memory for Target Repositories

**Kind:** reference case for the Prospective Reasoning Ontology (plan PR B); an analysis record, not a registered artifact contract yet (plan PR D will define `architectural_synthesis`)  
**Date:** 2026-10-28  
**Target repository:** `ThorStarlord/sensemaking-skills` (the portable Skill it ships); assessed at `main@b6cf50998467a42fa999b2cf3a52b7271d14ec6a`  
**Author:** active coding agent, under the owner's 2026-10-28 program plan  
**Authority:** none. Options, paths, consequences and the provisional preference below are hypotheses and an attributed agent judgment. Nothing here selects a Strategic Frontier item, authorizes construction, or changes the portable Skill.  
**Concepts:** [`docs/semantic-architecture/prospective-reasoning-ontology.md`](../../docs/semantic-architecture/prospective-reasoning-ontology.md)

## 1. Governing intent and scope

- **Question:** should Sensemaking retain the candidate responsibilities a repository-only discovery compared, in addition to the one it selects, and what would that unlock?
- **Governing sources:**
  - ADR 0031 decision 1: knowledge across tasks, agents, repositories and time.
  - ADR 0029: agent-owned semantic control; no automatic selection.
  - ADR 0030 (accepted): the target-repository Grounding Pack.
  - ADR 0032 (proposed): receipts.
  - `using-sensemaking`: repository-only discovery is read-only unless implementation authority is separately granted (`skills/using-sensemaking/SKILL.md:87`).
  - The owner's plans: PR J requires one explicitly authorized target repository for portable application.
- **Scope:** architecture and strategy of one portable capability. Not a Level-3 reopening of this repository's frontier: PATH-1 accretion is unaffected.

## 2. Target possibility

`poss:target-repository-discovery-memory` (Idea Library section 3.5; `.sensemaking/knowledge/possibilities.json`). The disposition history reads `EXPLORATORY` (agent, 2026-10-28).

**Motivating evidence:** `docs/agents/build-loop.md:58` records a 2026-10-27 discovery that anchored on prior component-level receipts. Its leading hypothesis is premature framing reinforced by receipt history. It is one owner-shared episode, not a rate.

## 3. Current architecture (observed at `b6cf509`)

| Element | Observation | Source |
| --- | --- | --- |
| Discovery comparison | Discovery compares "credible, materially distinct responses" and selects one; the comparison lives in the task report | `skills/using-sensemaking/references/portable-construction-loop-v1.md:78` |
| Session receipt | Records one `next.warranted_responsibility` (300-character cap); no field for the compared set | `skills/using-sensemaking/references/session-receipt-v1.md:31`, `:218` |
| Receipt role | "receipt != reviewed knowledge"; "Never paste reasoning"; final receipts are immutable | same file, `:23`, `:33`, `:59` |
| Receipt persistence | Without commit or host upload, a receipt is `working_tree_only` and lost with the checkout | same file, `:103` |
| Receipt consumer | `summarize-receipts.py` reports `next`, open questions and misses; it reads no other field | `scripts/summarize-receipts.py:96-128` |
| Receipt validator | No unknown-field rejection was found by inspection; a new field would be neither enforced nor surfaced | `scripts/validate-receipt.py` |
| Reviewed knowledge in targets | Updated "if the target has such a knowledge surface and the edit is authorized"; built demand-first | `portable-construction-loop-v1.md:310-312` |
| Possibility records | Encoding convention exists (`opportunity`, `poss:` id, disposition history) | `skills/repository-semantic-steward/references/knowledge-contract.md:40` |
| Recall of possibilities | Funnel section 4 recalls retained `poss:` records before breadth | `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md:172` |
| Grounding Pack | `.sensemaking/decisions/*.md` lines are indexed as `decision` claims; files have hard word budgets | `src/sensemaking_skills/semantic_architecture/knowledge_sources.py:175-181`; `docs/adr/0030-target-repository-grounding.md:16-17` |
| Strategic projections | `strategy history` and `strategy graph` project explicitly supplied strategic analyses | `src/sensemaking_skills/strategy_cli.py:629`, `:684` |
| Analysis is optional in discovery | A full Brief, ontology or strategic analysis is not a discovery prerequisite | `portable-construction-loop-v1.md`, repository-only entry |

## 4. Architecture options

Each option is a proposal; none of its proposed structure exists.

### `arch:git-reviewed-local-memory` (A): repository-local possibility records

- **Target structure:** authorized discovery retains each consequential compared candidate as a `poss:` opportunity record in the target's `.sensemaking/knowledge/`. The record carries a disposition (selected or declined, with reason), `revisit_when`, its origin (the session receipt) and cited source files.
- **Reuses:** the knowledge contract's possibility convention, steward RECONCILE, funnel recall, `workspace-impact` reconsideration, and the index when present. JSON is readable without it.
- **Proposed change:** guidance in the portable loop's repository-only entry. No schema change.
- **Requires:** knowledge-edit and commit authority in the target; the target owner's acceptance of a `.sensemaking/knowledge/` surface.
- **Invariants:** candidates are hypotheses, not a backlog; no import from other repositories; the receipt still records the session.

### `arch:receipt-based-memory` (B): extended session receipt

- **Target structure:** an optional `considered_candidates` list in the session receipt (identity, responsibility, selected or declined, reason, `revisit_when`), reported by the receipt reader.
- **Reuses:** receipts, which every `using-sensemaking` session creates; the reader and validator.
- **Proposed change:** the receipt schema, validator and reader, under proposed ADR 0032.
- **Requires:** commit authority for persistence.
- **Conflicts with the receipt's role:** facts and pointers, not reasoning; 300-character caps; immutable once final; not indexed, so no `changes` or `workspace-impact` reconsideration by candidate identity.

### `arch:strategic-artifact-projection` (C): projection from strategic analyses (counterfactual)

- **Target structure:** no new records. Prior candidates are projected from strategic analyses' frontier candidates and paths with `strategy history` and `strategy graph`.
- **Reuses:** existing projections.
- **Requires:** discovery to produce strategic analyses. It usually does not, because they are optional.
- **Expected loss:** every candidate compared in ordinary discovery. This is the same finding as the declined `poss:possibilities-projected-from-analyses`, now applied to discovery.

### `arch:grounding-pack-decision-log` (D): Grounding Pack decision lines

- **Target structure:** declined candidates become provenance-tagged lines (`[delegated: date]`) in the target's `.sensemaking/decisions/`, which the index already ingests as `decision` claims.
- **Reuses:** ADR 0030's pack, question ratchet, budgets and indexing.
- **Requires:** write authority.
- **Tension:** word budgets limit how many candidates fit; a declined candidate becomes a `decision` claim, which fits "not chosen because" but carries no typed disposition, `revisit_when` or relationships. It is owner-legible.

## 5. Strategic paths (analysis-local)

| Path | Future capability state | Uses | Main dependency |
| --- | --- | --- | --- |
| PATH-1, local-first | Authorized discovery sessions leave typed candidate records that later discovery recalls | Option A | Write authority in targets; ASSUMPTION-1-like reuse |
| PATH-2, receipt-first | Every committed receipt carries its compared set; records decided later | Option B | ADR 0032 acceptance; receipt-role change |
| PATH-3, wait for loss | Unchanged until a discovery demonstrably loses a consequential alternative | none | A detectable loss event |

These are trajectories, not tasks. A full `strategic_repository_analysis` is not warranted: the choice changes one portable capability, not this repository's frontier.

## 6. Preliminary comparison (attributed: agent, 2026-10-28)

| Lens | A local records | B receipts | C projection | D decision lines |
| --- | --- | --- | --- | --- |
| Fidelity (identity, reason, assumptions, relations) | High | Medium: capped text, no relations | Low: most candidates absent | Medium: prose, no typed disposition |
| Reconsideration support | `workspace-impact`, `changes`, funnel recall | None by candidate identity | Strategy drift only | Index claims; no `revisit_when` |
| Fit with existing contracts | Uses an existing convention | Conflicts with receipt role | Consistent but incomplete | Consistent; strains budgets |
| Footprint in target repositories | New surface where absent | None beyond receipts | None | Pack files |
| Owner legibility | JSON; library optional | Low | Existing artifacts | High |
| Construction cost | Guidance only | Schema, validator, reader | None | Guidance only |

**Path comparison:**
- **PATH-3** is cheapest, but the 2026-10-27 episode is already partial evidence of the failure it waits for.
- **PATH-2** is cheap to start but changes a proposed contract against its stated role.
- **PATH-1** reuses existing mechanisms.

**Provisional preference:** `arch:git-reviewed-local-memory` via PATH-1. Status: PROVISIONAL, attributed to the agent, no authority.

## 7. Post-convergence consequence exploration of the provisional preference

| Id | Predicted effect (conditional) | Category | Assumptions | Mechanism | Counterevidence or uncertainty | Would change the decision if |
| --- | --- | --- | --- | --- | --- | --- |
| `conseq:candidate-recall-in-later-discovery` | Later discovery recalls declined candidates and their reasons instead of re-deriving or anchoring on `next` | benefit | Later sessions consult `.sensemaking/knowledge/` (ASSUMPTION-1 analogue) | Funnel section 4 recall; using-sensemaking source table lists reviewed knowledge | Not tested in any independent session | Sessions ignore the records |
| `conseq:persistence-requires-write-authority` | Under default read-only discovery, A persists nothing; neither does B | constraint | Observed premise: discovery is read-only by default; uncommitted receipts are lost | `SKILL.md:87`; `session-receipt-v1.md:103` | Observed, not hypothesized, for both options | Already changes it (section 8) |
| `conseq:target-maintenance-burden` | Stale candidate records accumulate in repositories whose owners rarely use Sensemaking | risk | Low later use in some targets | Records without later RECONCILE | Mitigated by `revisit_when` and `workspace-impact`; unmeasured | Burden observed in a real target |
| `conseq:citation-noise` | Broad evidence citations make every related edit flag candidate records | risk | Records cite libraries or broad documents | File-level matching (observed lesson, query receipt QY-11) | Knowledge contract now says cite the origin | Noise recurs despite the rule |
| `conseq:knowledge-surface-bootstrap` | Targets without `.sensemaking/knowledge/` need one created on demand, which their owners may resist | constraint | Owners accept the directory | Portable loop's demand-first rule | No target observation yet | An owner refuses the surface |
| `conseq:prospective-decision-memory-reuse` | The same record surface could also hold architecture options, consequences and preferences in target repositories | opportunity | Option and consequence encodings work with existing kinds (plan PR C tests this) | Shared encoding conventions | Coincides with plan PR J's intent | Encoding loses decisive meaning |

**Stop:** a further layer (for example, cross-target aggregation) would not change the choice between A to D under current authority, so depth stops here.

## 8. Feedback: `REVISE_PREFERENCE` (narrowed)

`conseq:persistence-requires-write-authority` does not separate A from B, but it changes where A has value. In the default read-only mode, no option retains anything. The task report already compares alternatives in prose (`portable-construction-loop-v1.md:78`).

The preference is revised to:

> Prefer A **only in sessions that hold knowledge-edit and commit authority in the target**. Read-only discovery keeps its compared candidates in the report, as today.

A remains preferred over B for the reasons in section 6. B is retained as the lighter alternative if ADR 0032 is accepted with a candidate field. C and D are declined for this purpose: C loses ordinary-discovery candidates, and D's budgets and missing typed disposition fail the fidelity lens.

## 9. New possibility derived

`poss:repository-local-prospective-decision-memory`:
- **Proposed future:** a target repository's authorized knowledge surface retains not only discovery candidates but also architecture options, consequence hypotheses and preferences from its own reasoning, so later sessions there reconstruct why one structure or path was preferred.
- **Derived from:** `conseq:prospective-decision-memory-reuse`.
- **Status:** hypothetical. It is broader than `poss:target-repository-discovery-memory`, and it coincides with the outcome plan PR J intends, so it is recorded as the possibility that PR J would advance, not as an independent proposal.
- **Retention:** recorded in the Idea Library and reviewed knowledge with plan PR C.

## 10. Smallest warranted responsibility (candidate, not authorized)

The candidate guidance change, in the portable loop's repository-only entry:

> When the session holds knowledge-edit and commit authority in the target, retain consequential declined candidates as `poss:` records under the knowledge contract; otherwise keep them in the report.

It changes guidance only, adds no authority, and is a candidate for plan PR H. Whether to build it is a later selection.

## 11. Reconsideration conditions

- ADR 0032 is accepted and adds or invites a candidate field (reopens B).
- An independent discovery session ignores retained candidate records (challenges `conseq:candidate-recall-in-later-discovery`).
- A target owner rejects the `.sensemaking/knowledge/` surface (challenges A's footprint).
- Maintenance burden or citation noise is observed in a real target.

## 12. Unresolved questions

- How often do real discovery sessions hold knowledge-edit and commit authority? This determines A's practical reach and is unknown.
- Which explicitly authorized target repository plan PR J would use. That is an owner choice.

## 13. Authority and claim boundaries

```text
provisional preference != selection != authorization
consequence hypothesis != observed effect
proposed structure     != existing component
reference case         != evidence of cross-session benefit
```

`implementation_authority_established_by_artifact: false`; `semantic_truth_established: false`.

## 14. Evidence

All sources are cited inline in sections 2 to 7, at `main@b6cf509`. The only observed premise inside the consequence table is `conseq:persistence-requires-write-authority`. Every other consequence is hypothesized.
