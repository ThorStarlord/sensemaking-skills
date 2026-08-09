# Composition assessment — honest, not celebratory

## The falsification question, answered directly

*"If the same agent ends up reading all the repository files anyway while
wearing both hats, and the two-Skill separation adds ceremony without
changing reasoning quality, Option C gets stronger."*

**At the artifact level: the separation held.** Checking each downstream
document against what it actually cites:
- `02-repo-sensemaker-interaction-synthesis.md` cites zero repository
  evidence directly — every citation is either the brief's own fields or
  the prior conversation's recorded owner statements. It does not re-grep,
  re-read a test file, or re-derive a finding.
- `03-vnext-review-consumer-output.md` cites zero repository evidence
  directly either — every claim traces to `analysis_vnext` fields or the
  `proposed_direction` text. It does not re-open `test_field_contract_agreement.py`
  or re-check which CI job runs what.

So the brief functioned as a real boundary in this run: downstream
reasoning stayed inside it rather than reaching back into the repository.

## The honest limitation this test cannot remove

**I am one continuous agent that authored all three documents with full
memory of the whole investigation.** The clean citation boundary above is
consistent with "the brief was genuinely sufficient" — but it's *equally*
consistent with "I already knew everything and simply didn't need to
re-derive it, regardless of what document I was writing." This test cannot
distinguish those two explanations. A test that could would need the
consumer step authored by something that had *only* the brief as input —
a fresh context, or a genuinely separate invocation — not a continuation
of the same session that produced the brief.

**This is not a small caveat.** It's the specific thing self-administered,
single-session composition tests structurally cannot establish, and it's
exactly the gap between "STATIC ARCHITECTURE PROTOTYPE" and "LIVE
INTERACTION PROTOTYPE" flagged two turns before this one. This test moves
partway across that gap (real artifacts, real citation-boundary discipline
observed) but does not close it.

## Where the split showed real (if modest) value

The three documents ask genuinely different questions, not the same
question three times:
- Brief: *what does the repository establish?*
- Interaction synthesis: *what does prior owner context already answer,
  and does it still cover what's now known?*
- Consumer output: *does this specific proposal make sense given both?*

Writing these as separate documents made each question individually
checkable in a way a single combined document attempting all three at once
likely would not have been — Step 4 of the interaction synthesis (the
"reuse old intent for its original scope, but flag new findings as
uncovered by it" move) is a genuinely distinct piece of reasoning that
would have been easy to blur into the evidence-gathering or the
proposal-evaluation if all three lived in one place.

## Where ceremony showed, honestly, in the other direction

Writing `vnext-review-consumer`'s "does not re-diagnose the repository"
boundary rule cost something — it's a restated discipline reminder that a
single continuous document narrating one train of thought would not have
needed, because there'd be no separate "hat" to accidentally violate. This
is small, real evidence toward Option C (one skill, internally separated,
no restated boundary rules between sections) rather than Option A.

## One concrete new finding this run produced that prose discussion hadn't

The `domain` field's behavior needed a judgment call the design discussion
never surfaced: when does a second `domain` value (here, `docs` alongside
`architecture`) represent a genuinely separate decision-making lens
(P4's product-vs-architecture split, where the consumer should withhold
judgment) versus a domain label that's technically accurate but doesn't
actually require withholding anything (here, `docs` = "the registry file
the architectural fix touches," not a competing authority)? The consumer
had to decide this in the moment (`03`, field check 3) rather than follow
a rule that already existed. That's exactly the kind of thing construction
reveals that discussion didn't — and it's now recorded as a real
open question for `domain`'s design, not resolved by this test.

## Verdict on Option A vs. C, calibrated to what this actually shows

**Modest positive evidence for the intermediate artifact's value** (the
brief functioned as a real boundary, citation discipline held).
**Inconclusive on the packaging question** (two deployable Skills vs. one
internally separated) — this test never exercised invocation mechanics;
everything here was authored in one continuous session, which is closer to
Option C's actual runtime shape (one agent, internally organized) than to
Option A's (two independently invocable units) regardless of how the
documents were labeled. If anything, this test is weak evidence that the
*documents* should stay separate (Option A's artifact-boundary idea) while
remaining silent on whether the *Skills* need to be separate too (Option
A's packaging idea) — those are not the same claim, and this run is the
first time that distinction became visible.

**Recommendation**: do not collapse to Option C on the strength of this
result — the evidence doesn't support that either. Keep Option A as the
working hypothesis; the specific thing worth testing next isn't more
prototype construction, it's whether a genuinely separate invocation
(fresh context reading only the brief) reproduces this run's clean
citation boundary. That's real-use evidence, not more code.
