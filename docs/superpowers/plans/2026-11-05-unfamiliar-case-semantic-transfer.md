# Unfamiliar-Case Semantic-Transfer Procedure (normal-use-first, revised)

> **Revision of the PR #768 plan.** The earlier version (git history at `5305c157`) required distinct genuine host sessions, source-occluded first passes and a five-axis gate for every observation. This version follows the [revised design](../specs/2026-11-05-unfamiliar-case-semantic-transfer-design.md). It treats those arrangements as optional diagnostics. This document is a procedure, not an execution record.

**Execution status:** `NOT_RUN`. This revision made no agent observation and no change to Sensemaking or Atlas.
**Current disposition:** `NO_FURTHER_INQUIRY` for the isolated unfamiliar-case run (spec section 8). The [first-use result](../../normal-use/2026-11-05-ontology-author-reader-first-use.md) remains `PARTIAL`.
**Baselines:** Sensemaking `origin/main` `5305c157` (PR #768 merge). Atlas `2b3556e47daa6110d01c045432e23bf4e041ba49`, as named in PR #768 and not re-verified in this revision. Re-pin at the start of any real execution. Do not substitute moving main.

## Global constraints

- The only claims this procedure can support are the three in spec section 1, each with its ceiling. Nothing here establishes product usefulness.
- An observation records what happened during the work; it does not itself change Sensemaking product code, schema, Skill, test or any Atlas file, and it does not restrict legitimate engineering work to create cleaner evidence. An ordinary engineering task may modify authorized repository files. A disposable, unmerged knowledge candidate may be created only inside an authorized authoring diagnostic (Task 2). Canonical knowledge and product authority change only through the normal knowledge review path.
- Operator notes and any answer-bearing material stay outside checkouts that agents work in, and out of prompts, *when a diagnostic depends on that exclusion*.
- Use an isolated environment when a CLI is needed. Do not modify the global CLI or installed Skills.
- Label any prompted reading as prompted. Keep negative and failed results.
- Construction rule for this repository phase: do not add or run local unit or synthetic evidence tests. State `NOT_RUN` where they would otherwise be cited.
- Mechanical validity is not semantic truth.
- Any Atlas work needs Atlas's own authority. This revision grants none.

## Task 0 - Decide what evidence the decision needs

1. Name the claim (A, B or C, spec section 1) and the decision it would inform. If no plausible result would change that decision, stop with `NO_FURTHER_INQUIRY`.
2. For a normal-use episode, confirm a real goal and record the selection rule before work starts. The goal is chosen for its product value, evidence, constraints and authorization, not for its usefulness as an evaluation case (spec section 3).
3. For a diagnostic (spec section 5), confirm its trigger. If the arrangement it needs is unavailable, record that diagnostic as `NOT_RUN` and carry on with normal use. Do not substitute a weaker arrangement and report it as the same test.

**Acceptance:** one line naming the claim, the decision and the selected evidence form.

## Task 1 - Normal-use episode (preferred)

1. Do the real task with ordinary context: repository instructions, installed Skills, sources and history. Do not add a wrapper question or hide repository context.
2. Consult retained knowledge where it bears on the work. Record the queries and record IDs actually used. If a record is cited as evidence, confirm that it resolves at the cited revision (exact-commit index and query, where available).
3. Check retained claims against their sources as ordinary practice. Record the sources opened and any correction made.
4. For each decision the knowledge touched, record the artifact that shows the effect (decision note, diff or report). Mark anything that rests only on the agent's account as such.
5. Verify the outcome in proportion to the target's policy. Name anything not run.
6. Write the observation note with the spec section 4 dimensions, including negatives, the selection rule and the ceiling.
7. Reconcile: retain, revise or reject the touched knowledge through the normal Steward path, or record `NO_MODEL_CHANGE`.

**Acceptance:** a note that separates observed artifacts from self-report, keeps the negative observations and states its ceiling. No score is produced.

## Task 2 - Authoring a new knowledge candidate (only when authoring is the work)

1. Write the smallest record set that supports the decision, using the existing vocabulary (`schema_version`, `claims`, `relations`). Do not invent predicates or schema versions to fit the claim.
2. Run the existing proposal check and record its output.
3. Commit on a disposable branch at one exact revision. Build the index outside the repository and confirm that search and explain return the candidate.
4. Leave the branch unmerged unless the normal knowledge review accepts it.

**Acceptance:** mechanical validity and exact-commit retrieval are recorded. Semantic fidelity is judged in Task 1 step 3 or in D-FID, not by the proposal check.

## Task 3 - Optional diagnostics (only when triggered)

**D-CONT, cross-session continuity (claim B):**

1. Start a genuinely new session or fresh agent. Record its identity, and the instructions and memory it inherited.
2. Give it the ordinary repository goal. Do not supply the earlier conclusion or an answer.
3. Record its retrieval trace and source reads, in order.
4. If its inherited context contained the answer, record that ceiling and do not count the result as continuity.

**D-REP, representation sufficiency:**

1. Give the reader only the retrieved records, with a knowledge-first request labelled as prompted.
2. Freeze the first account and the list of tool calls before any source is opened. Any earlier source read invalidates the account as representation evidence.
3. In a separate step, have it check the original sources and classify each material claim as `SUPPORTED`, `CONTRADICTED`, `UNSUPPORTED` or `NOT_ASSESSED`.

**D-FID, authoring fidelity:**

1. Use a reviewer that did not author the record.
2. Check each material claim at the exact revision. Record support, scope and missing nuance. Distinguish declared design, historical status, current behaviour and tests that were written but not run.
3. Report which claims were sampled. Give no verdict on unsampled claims.

**D-CAUSAL, causal or comparative attribution:** not executable from this procedure. It needs a separate, owner-warranted design with fixed outcomes and adjudication. Stop here.

**Acceptance:** each diagnostic run states its trigger, its arrangement and what it could not show.

## Task 4 - Adjudicate and reconcile

1. For each claim the work touched, state the ceiling the evidence supports.
2. Decide whether any model or guidance changes. Prefer `NO_MODEL_CHANGE`. A concrete change needs its own warranted responsibility.
3. Leave every prior result unchanged, including the `PARTIAL` first-use readout.

## Task 5 - Record and stop

1. If an episode or diagnostic was actually run, record a concise dated note under `docs/normal-use/`, with its real ceiling. Keep private transcripts and inherited memory out of the repository.
2. Stop when the decision is supported or no warranted responsibility remains. Do not rerun for a more favourable outcome.

## Current disposition (this revision)

- No episode or diagnostic was run. Disposition: `NO_FURTHER_INQUIRY` for the isolated unfamiliar-case run.
- Next responsibility: whichever engineering work product value, evidence, constraints and authorization select (spec section 3, responsibility selection). Retained knowledge may inform that choice but must not be the reason for it. Record a Task 1 note only if such work is done.
