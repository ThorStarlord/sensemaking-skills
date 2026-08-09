# S1 — Clarification (single high-information owner question, frozen before asking)

record: clarification-v1
frozen_at: 2026-08-08 (after Phase 2 investigation, before the question was presented)
question_count: exactly ONE (protocol constraint)

## Why a question is asked at all

Phase 3 test applied to the investigation's Phase-3 input:

1. Can repository evidence resolve the recommendation sufficiently? Partially —
   the investigation establishes from repository evidence that the "four
   infrastructure gaps" were implemented and committed (May 28 "infra:
   Stabilize") but mis-wired: deliverables landed in legacy root copies
   (repo-sensemaker/references/, workflow-orchestrator/references/) that
   agents never load, the canonical skills/ trees were never updated, and
   validate-skill-hygiene.py silently skips its two substantive checks
   (missing registry paths -> early return). That part is evidence-resolved.
2. Remaining uncertainty that matters: the DIRECTION choice itself —
   interaction design (S1-class) vs. contract cleanup vs. both vs. neither.
   Classification: OWNER_INTENT (strategic priority; the repository's own
   records — P2-P4 — ratify interaction design but are the owner's own
   recorded decisions, which the owner alone can update).
3. Counterfactual test: "If the owner answered the opposite way, would the
   engineering recommendation materially change?" YES — branch (b) makes the
   wiring reconciliation the focus and defers interaction design; branch (a)
   makes interaction design the focus with reconciliation as fast-follow.
   Materially different recommended work.

Therefore: CASE B applies. Exactly one high-information question is asked.
No second question will be asked even if the answer leaves residual
uncertainty (recorded as learning instead).

## The frozen question (presented to the owner verbatim)

"For the next engineering focus, what is your intent?
(a) interaction design first (S1-class), with the four-gap wiring
    reconciliation as a fast-follow [recommendation the evidence supports];
(b) the four-gap wiring reconciliation first, then interaction design;
(c) both in parallel;
(d) neither — a different direction."

(For the ask presentation, option (a) carries the evidence recommendation
and the alternatives are exposed neutrally.)

## Why this is the highest-information question

- Only the owner can answer it (strategic priority; not derivable from the
  repository).
- The answer materially changes the recommended next work (counterfactual
  YES).
- It resolves a major decision branch in one answer (direction + sequencing).
- It is easy to answer (four discrete branches, no essay required).
- It avoids asking for anything the agent can retrieve itself.
