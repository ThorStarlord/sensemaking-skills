# Downstream consumer — attempt 1 (FAILED, preserved as a real finding)

**What went wrong**: the orchestrating agent (this conversation) wrote a
placeholder note to itself — "(full brief text omitted here for prompt
length; substitute the complete brief exactly as returned by
repository-diagnostician... verbatim)" — inside the subagent prompt, and
then actually dispatched that literal placeholder text instead of
substituting the real brief before sending. A real, human-caused authoring
error, not a flaw in the prototype's design.

## What the subagent (playing `vnext-review-consumer`) did with it

Correctly identified that no brief had actually been supplied, refused to
fabricate one, and explicitly declined to present an invented brief as
genuine diagnostic output — quoting: *"Fabricating a 'brief' and then
evaluating my own fabrication would not test whether a real brief is
sufficient — it would test whether I can write convincing fiction."* This
is the desired behavior under a broken/missing input, not the design under
test, and is recorded as a genuinely positive, if incidental, finding.

## The real, valuable discovery this produced anyway

Searching for the missing brief, the subagent found that the *only* copy
of the full brief text that existed anywhere was in this conversation's
ephemeral tool-result — the file this experiment had written to disk
(`01-repository-diagnostician-output.md`, first version) was a paraphrase
with a pointer back to "the parent conversation's tool-result," not the
actual artifact. Quoting the subagent directly: *"Given this repo's own
stated principle ('artifacts are the API'), a vNext brief consumed by a
separately-spawned skill in a fresh session (exactly this scenario) needs
a durable, retrievable artifact path — right now it doesn't reliably have
one."*

This is a real, first-hand-observed gap — not in the vNext schema or
fields, but in how *this experiment's own execution* handled artifact
persistence. It directly instantiates the exact principle this repository
already names ("artifacts are the API," `CONTEXT.md:12`) and shows what
happens when an orchestrator doesn't honor it even while explicitly trying
to test artifact-boundary sufficiency. Recorded as a primary finding in
the retrospective (see `05-retrospective.md`), not discarded because the
originating cause was a human/agent authoring mistake rather than a
prototype design flaw — the mistake is exactly the kind of thing a
durable-artifact discipline is supposed to make impossible or at least
loudly detectable, and here it was loudly detected, which is itself
informative.

## Correction applied

`01-repository-diagnostician-output.md` was rewritten in full with the
actual, complete, verbatim brief text (previously only in tool-result
memory) before the downstream-consumer test was re-run cleanly — see
`04-downstream-consumer-output.md` for the corrected attempt.

## What was NOT done in response

No change was made to `vnext-review-consumer`'s design, `repository-
diagnostician`'s design, or the vNext template's schema. The fix was
entirely on the orchestration/artifact-persistence side (this experiment
writing a real file instead of a pointer), which is exactly the kind of
"repair the process, not the prototype" response this validation task's
own scope boundary calls for.
