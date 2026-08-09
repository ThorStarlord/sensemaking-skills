# repo-sensemaker interaction-layer synthesis — composition test

## Step 1: recover known intent

Before invoking `repository-diagnostician`, the prior session's actual
recorded owner statements are the known intent:
- "the stale runtime `fog_type` alias is the leading candidate for the
  next small contract-correctness repair" (prior turn, this repository).
- "record — not automatically fix — the newly exposed hygiene/vocabulary/
  CI debt" (same prior turn).
- "the fog_type runtime alias... I would wait until #163 lands before
  starting that" (same prior turn).

This is real, not fabricated — both statements are quoted verbatim from
this repository's own conversation history, not invented for this test.

## Step 2: read the returned brief

`owner_intent_state.status: thin` (not `sufficient`, not
`blocking_unknown`). The brief's own `unresolved` field asks whether the
prior "record, don't fix" guidance still holds now that three MORE
instances of the same drift class are confirmed.

## Step 3: would a different answer be decision-changing?

Yes — per S1's rule, this passes the test. "Fix fog_type alone, defer the
rest" vs. "fix all four together" vs. "fix all four AND add CI
enforcement" are three materially different scopes of work.

## Step 4: is there already a real, applicable answer, or does this need a new question?

**This is the interesting case.** The prior recorded intent already
answers the *scope* half of the question (fog_type alone, wait for #163) —
but it was recorded *before* the other three drift instances were known to
exist. Re-asking from scratch would ignore real prior context; silently
assuming the old answer still covers three additional, not-yet-seen
findings would risk exactly the "invented owner preference" failure this
whole prototype exists to prevent.

**Resolution**: treat the prior recorded answer as *provisionally still
applicable* to its own original scope (fog_type alone, wait for #163), but
explicitly flag the three NEW findings as **not yet covered** by that
prior answer, rather than silently bundling or silently deferring them.
This is a middle path between "ask a redundant question" and "invent an
answer to a question that was never actually asked."

## Recommendation

1. **Proceed** with the fog_type alias as the next micro-repair, once #163
   merges — directly supported by prior recorded intent, no new question
   needed for this part.
2. **Do not bundle** the three newly-found canonical-vocabulary.yaml gaps
   or the CI-enforcement question into that repair — they are real,
   `is_demonstrated_weakness: true`, but were not part of what "record, not
   fix" was originally said about.
3. **Flag explicitly** (this document) that the three new findings and the
   CI-enforcement question remain open and were not resolved by reusing
   old context — a genuinely new clarifying question, not fabricated, not
   asked here because it's not blocking this step's recommendation.

`recommended_workflow_id`: none — this is a repair, not a workflow-routable
change; matches the brief's `domain` not including `product`.
