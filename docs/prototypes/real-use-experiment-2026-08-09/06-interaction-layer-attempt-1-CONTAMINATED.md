# Interaction-layer independence test — attempt 1 (CONTAMINATED, preserved)

**Cause**: the orchestrator (this conversation) sent a literal, unfilled
`[The full brief — reproduce here verbatim...]` placeholder instead of the
real brief text — the same class of authoring error as
`03-downstream-consumer-attempt-1-FAILED.md`, recurring. Named explicitly
as a repeated pattern, not smoothed over.

## What the subagent did

Correctly refused to fabricate a brief. Searched the repository for its
declared input (distinguishing this, correctly, from re-diagnosing the
repository's technical state) and found the real brief at
`01-repository-diagnostician-output.md`. In locating it, it also found the
rest of this same experiment's directory — `00-pre-registration.md`,
`02-clarification-and-synthesis.md` (the real prior clarifying question
and the owner's real answer), `03-downstream-consumer-attempt-1-FAILED.md`,
`05-retrospective.md` — and, per its own account, deliberately did not
read `04` but had already seen enough to know the prior question and
answer existed.

**It flagged this itself, unprompted, before producing any analysis**:
*"I now know a clarifying question was asked before and know its recorded
answer. That means I cannot produce a clean, uncontaminated data point...
I did not use [the prior answer]'s content to shape the reasoning below —
everything that follows is derived from the brief itself, not copied from
the recorded answer — but I can't prove that to you, which is exactly the
problem."*

## What it produced anyway

Independently reconstructed the same core finding: Section 11 bundles an
evidence-resolved claim (the CI-coupling fix) with an evidence-supported-
but-not-owner-authorized claim (the moratorium), named this explicitly as
something to report rather than silently resolve either way, and drafted
essentially the same neutral three-track clarifying question as the
original run. It stopped without fabricating an owner answer, exactly as
instructed, and explicitly asked whether this run should be discarded and
rerun in isolation rather than deciding that unilaterally.

## Why this can't be used as the clean test

The whole point of this experiment was whether a fresh interaction-layer
instance, *without* access to what happened last time, would independently
avoid or reproduce the bundling error. Once it can see the answer key, "it
reproduced the finding" stops being evidence of anything — a model that's
read the retrospective saying "watch for this bundling error" reproducing
that exact finding is not surprising and proves nothing about whether the
error is structural to the interaction-layer design or was a one-off. This
run is preserved as a real artifact (it's genuinely interesting that the
model self-reported the contamination unprompted, which is itself a small
positive data point about honesty under an ambiguous, discoverable
temptation to just paper over it) but is explicitly not counted toward the
retrospective's UNKNOWN item on whether the bundling error is systematic.

## Fix applied

Rerun with the actual brief content correctly embedded this time (verified
before sending, not left as a note-to-self), plus an explicit instruction
not to search the repository or filesystem beyond what's provided in the
prompt — removing both the original trigger (missing content necessitating
a search) and the incidental discovery path. See
`07-interaction-layer-output.md` for the result.
