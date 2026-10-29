**Short answer:** Don't build coach support yet. Most of what the coach describes is already possible on one machine. What can't be done today is for the coach to assign practice, and to record a judgment on a student's hypothesis. Adding either one gives a new kind of actor power that the current rules leave out on purpose. Whether coaches are a segment CME wants at all is your call, and the repository's own rule for what comes next asks for evidence from real use first. I didn't change any code.

## What already works
- **Keeping students separate:** every stored item is tagged with one participant, and any read for a different participant is refused (`src/chess_mentor_engine/storage/store.py`). One coach can already run the existing local tutor for several students, each kept apart.
- **Reviewing hypotheses and progress:** the learner progress view (M44) and the review queue (M45) already show each student's hypotheses, evidence and transfer plans, one student at a time.

## What would be new, and where it collides with existing decisions
1. **Coach-assigned practice has nowhere to live.** ADR 0008 makes intervention selection (M9) a fixed rule. It picks an intervention only when exactly one applies, and otherwise returns "unclear" or "ineligible". The same ADR rejected letting anything choose freely at selection time. A human is only recorded as the author of content or of a mapping, never as the one who selects. So "the coach assigns X" needs its own record (attributed to the coach, pointing at existing registry interventions, and kept separate from the rule's own selection). Folding it into the rule would break that decision.
2. **A coach's judgment is a fourth kind of evidence.** The architecture keeps three things apart: objective chess facts, what the student reported, and the system's inference about the student (M7C). A coach agreeing or disagreeing with a hypothesis is none of these. It must not overwrite M7C, because the derived views (M36 and M44) are read-only.
3. **Consent covers the student's own review only.** Today's consent is the student agreeing to a review session that captures their answers. Nothing covers a third party seeing a student's hypotheses. The pilots' data-handling rules are also built around one participant.
4. **A view across students doesn't exist.** Every read model and report covers one participant. A roster is a new consumer and needs no new authority. This is the cheapest gap and the one least likely to be the real bottleneck.
5. **Going beyond one machine is outside the repository.** Hosted accounts, multiple coaches and privacy approval are listed as needing outside sign-off (`STATUS.md`).

## Decisions and earlier work that bear on it
- **Product discovery** targets individual players rated about 1400–1800 and lists the human coach as a competing category, not a customer. A coach-led product changes the segment and the buyer.
- **The first validation study** already has a researcher or coach write the analysis packet by hand. A coach in the loop fits that research design. That argues for using a coach as an observer before building anything for them.
- **The release gate** (build plan §9–10) says that only demonstrated need from real use should create the next package. Nothing from real use has been recorded since PR #98. Pilots 001 and 002 came back "Mixed", and pilots 003 and 004 were designed but never run. The parked labels (M35 operator exposure, M47 multi-session plan) shouldn't be pulled forward just because this request sounds close to them.

## Warranted next step
First, you decide (this is the open question in the session receipt):

| Option | What follows |
|---|---|
| **Coach as observer only** | Nothing new to build. The coach runs the existing local review, feedback and report commands for 2–3 students, and we record where it breaks down. |
| **Coach as a product segment or channel** | Reopens the product thesis. An ADR would need to define coach assessment, coach assignment and consent before any build. |
| **Decline for now** | Keep the single-player thesis and record this request as outside evidence only. |

I'd recommend the observer option. It costs no code and produces exactly the evidence the release gate asks for. It also tests whether the real bottleneck is a roster view, assignment, or consent before committing to any ADR.

The session receipt is at `.sensemaking/receipts/2026-10-29-multi-student-coach.session.yaml`. It parses as valid YAML, but the receipt validator script isn't installed here, so I couldn't run it. I haven't committed it because no Git permission was given, so it will be lost when this checkout is reclaimed unless you tell me to commit it. 
