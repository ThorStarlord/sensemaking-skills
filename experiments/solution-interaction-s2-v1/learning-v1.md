# S2 Learning v1

## Central S2 question

"On an authentic owner-originated repository question, does the refined
investigation-first / neutral-clarify-if-needed interaction produce useful,
grounded decision support with low owner cognitive burden?"

## Disposition (qualitative)

**MIXED.**

The interaction produced a genuinely useful discovery (the repository's
documentation/tracker no longer reflects the project's actual development
state) with very low owner burden and a clarification the owner judged
neutral — but the recommendation was built on stale documented state, repeated
already-completed work, and had **no material effect** on the owner's next
action. The failure is specific, diagnosed, and addressable; it does not
invalidate the interaction shape.

## Dispositions

- **CLARIFICATION_BEHAVIOR:** WRONG_QUESTION — neutral but not the
  highest-information question. The one-question budget was spent on
  milestone intent when the higher-information uncertainty was whether the
  repository's documented state was still current (owner: "The better one
  question would have asked whether the repository's milestone/tracker state
  still reflected reality").
- **OWNER_BURDEN:** LOW ("Very low burden"; owner suggested "reasonable
  burden" is the cleaner rating given the outcome was drift discovery).
- **GROUNDING:** MIXED ("Mostly grounded" — real evidence, intent respected,
  but stale documentation treated as authoritative current state).
- **INTENT_PRESERVATION:** GOOD — the owner's stated demo priority was
  respected; no prior decision was overridden or challenged.

## What the interaction did right

1. Investigation-first worked on an owner-originated question: the owner was
   never asked to perform repository information retrieval or intake work.
2. The docs-vs-trajectory divergence was surfaced and was judged by the owner
   to be the genuinely useful output ("exposing that the repository
   documentation/tracker does not accurately communicate the project's
   current development state").
3. The clarification was **neutral** — the S1 refinement held. The owner
   explicitly confirmed the options contained no embedded recommendation.
4. Owner burden stayed very low; the owner answered one question and seven
   POST items.

## What failed (the core S2 limitation)

**State-currency verification.** The synthesis treated the repository's
*recorded* state (completion-tracker "Tested" column empty; "Fresh-persistent
playthrough" unchecked; CONTEXT.md "rough draft technical validation build")
as the *current* state, and sequenced work on that basis. In reality:

- the script is finished;
- the owner has already playtested the game several times (including audio and
  in-game images);
- character image asset production is the current work.

The Phase 3/4 discipline was applied in one direction only: I correctly
refused to convert "unfinished technical state" into "product priority"
without intent, but I *did* convert "documented unfinished state" into
"current unfinished state" without verification. This is a CASE A violation
in reverse: the missing facts (has the game been playtested? is prose
finished?) were empirically checkable, and cheap probes existed in the
working tree itself — `game/saves/` contained 21 save files (evidence of real
play sessions), the working tree contained active asset-production artifacts
(new untracked repair scripts, an updated HUMAN_APPROVAL timestamp, a new
.agents skill), and the commit trajectory pointed at asset production. The
one-clarification budget should have been spent on the highest-information
uncertainty — state currency — before sequencing any work.

## S1 -> S2 comparison

| Dimension | S1 (agent-selected target) | S2 (owner-originated target) |
|---|---|---|
| Target origin | AGENT_SELECTED | OWNER_ORIGINATED (real current project) |
| Disposition | PROMISING | MIXED |
| Owner burden | low | LOW (confirmed) |
| Clarification | one helpful but somewhat leading question | one NEUTRAL question (neutrality confirmed) |
| Clarification information value | resolved the fork | neutral but WRONG highest-information question (state-currency) |
| Recommendation effect | useful | no material effect (repeated already-done work) |

1. **Did the interaction remain useful when the problem originated naturally
   from the owner?** Partly. Useful as a state-drift detector; not useful as a
   next-work recommender in this run.
2. **Was owner burden still low?** Yes — very low.
3. **Did autonomous investigation still do most of the cognitive work?** Yes;
   the owner supplied intent and POST answers only.
4. **Was a clarification required?** Yes — the docs/behavior divergence was
   real and intent-dependent.
5. **Was it genuinely neutral this time?** Yes — confirmed by the owner
   ("much more neutral than S1's").
6. **Did the agent correctly distinguish missing empirical evidence from
   missing owner intent?** NO — this is the main regression risk: an
   empirical question (is the documented state current?) was treated as
   settled, and an intent question was asked in its place.
7. **Would the owner want to use this naturally again outside an experiment?**
   "Maybe, with refinements" — investigation-first and low burden are liked;
   the refinement is to verify the state-currency boundary before sequencing.

## Strongest positive learning

The refined neutral-clarification rule works in the field: an owner-originated
case confirmed that a neutral, intent-gathering question is achievable and
accepted, and the investigation-first interaction retains its low-burden
property on a real project.

## Strongest limitation / failure

The agent's recommendation depended on unverified, stale repository claims
about current project state (playtesting, prose completeness), repeating work
the owner had already done. The one-question budget was spent on intent when
state-currency was the higher-information uncertainty — a CASE A
(empirical/probe-able) question misclassified as CASE B (intent).

## Refinement for the interaction (recorded, not implemented)

Before sequencing a recommendation, the investigation must verify that
documented/tracked state is current, using the cheapest available probes
(local artifacts such as saves and build outputs, working-tree activity,
recency-weighted git history, or — if still ambiguous — the single
clarification question aimed at state currency rather than intent). The
recommendation must explicitly separate "tracker-documented state" from
"verified state."

## Construction gate

**CONSTRUCTION_PLAUSIBLY_JUSTIFIED.**

One authentic reuse case is not proof, but: (a) the interaction again produced
value (drift discovery) at very low burden; (b) the neutral-clarification
refinement was field-confirmed; and (c) the failure is a single, diagnosed,
fixable behavior — state-currency verification — rather than a shape-level
defect. Construction should proceed only if the refined interaction includes
the state-currency check and a state/verification distinction in the
synthesis. This is a recommendation for a future owner decision, NOT
authorization to implement.

## Validation note (Phase 6)

Canonical standalone validation ran exactly once via
`scripts/validate-brief.py --target-repo <superhero-netorare-parody>`:
**failed** (17 `EVIDENCE_QUOTE_NOT_FOUND` logic errors — the same
placeholder-quote failure mode as S1: the runtime's quote-overwrite step from
issue #89 does not run in standalone execution; all file/line citations
resolved correctly against the target repository). Result preserved verbatim
in `validation-result-v1.json`. Not repaired, not rerun; validation is
execution evidence, not the S2 product-value outcome.
