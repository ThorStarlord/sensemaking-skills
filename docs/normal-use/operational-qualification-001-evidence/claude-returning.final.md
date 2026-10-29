**Should CME do this? Not as a product pivot yet.** Whether to serve coaches is your decision. The repository can't settle it, and the evidence says to answer that question before building anything for coaches. I didn't change any product code.

## What the coach would need versus what exists

- **Several students.** Mostly there already. All stored records belong to a single student, and the store refuses links between students' records (`storage/store.py:118-125`). So several students already fit in one local store as separate student IDs. What's missing is any way to list or compare students, and any notion of a coach in the store.
- **Reviewing a student's hypotheses and progress.** This is blocked by the same two gaps the earlier analysis found:
 - Nothing turns a student's review sessions into the learning hypotheses (M7) that every progress view needs. The next-session planner (M40) refuses a student who has none (`next_session.py:543`).
 - Most learner records aren't saved by any command; they only exist as Python functions.

 So for a real student there is nothing yet for a coach to review.
- **A coach writing or confirming hypotheses.** This fits the current rules. Hypotheses can already be marked as written by a human, a model or the system (`learning/hypothesis_model.py`). A coach confirming hypotheses is essentially the "operator-confirmed" answer to the question still open from the first analysis (Q-2): who may create a student's hypotheses.
- **A coach assigning practice.** This is the real conflict. Today the system picks practice automatically and conservatively: only when a hypothesis has been seen repeating and exactly one registered exercise applies (ADR 0008, decisions 5–6). The CLI is also explicitly barred from selecting or assigning practice (ADR 0011). A coach overriding that pick would be a new kind of authority and needs its own decision record, not just a screen. A safe alternative within today's rules is to record the coach's judgment as human input about which exercise fits, and leave the automatic pick unchanged.
- **Hosting, logins, privacy.** Real use across several students on different devices needs accounts, separation between users and privacy approval. `STATUS.md` keeps all of that outside the repository's authority.

## Decisions and earlier ideas that bear on it

- **Who the product is for.** Product discovery picks a self-directed online player rated about 1400–1800. The human coach appears only as an alternative the product is compared against (`product-discovery.md:126`). Making the coach the user changes who the product is for.
- **The earlier coach idea.** The first analysis kept "coach-mediated product" as a "what if" only, marked as needing your decision, and judged the related path premature.
- **Current product rule.** `CONTEXT.md` says the next evidence comes from real repeated local use, and rules out hosted products or new learner-intelligence layers before that.
- **Manual testing already has a coach role.** The research protocol already names "a researcher or coach" as the person who prepares the manual analysis (`product-discovery.md:264`).

## Recommended next step

1. **Your decision.** Is a coach (a) who the product is for, (b) an optional local operator on top of the player product, or (c) out of scope for now? If (a) or (b): may coaches write or confirm hypotheses, and may a coach's assignment replace the automatic practice pick or only add a note to it? Answering this also settles Q-2.
2. **No-code step now.** This coach and their students are exactly the real-user evidence the project lacks; it currently has one participant. Have the coach run the existing manual analysis packets for 2–3 students. That tests whether the diagnoses are useful to a coach before any multi-student code exists.
3. **Only if the answer is (b), and after the setup work recommended earlier (PATH-1/T1).** Design the step that turns sessions into hypotheses (T2) so that hypothesis confirmation is the coach's act. Keep one local store with one ID per student, and record coach assignments as human input rather than as the automatic pick.

I wrote a session receipt at `.sensemaking/receipts/2026-10-29-coach-multi-student-question.session.yaml`. It's in the working tree only (not committed or pushed, since I had no authority to), so later sessions won't see it unless you commit it. 
