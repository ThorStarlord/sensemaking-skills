# Repository Grounding Direction (2026-10)

**Status:** owner-directed direction (2026-10-12); analysis record  
**Authority:** owner agreed to the recommendations below. Changing the Level-4
product thesis still goes through `docs/product-thesis-revision.md`; see Phase 0
of [`../repository-grounding-plan.md`](../repository-grounding-plan.md).  
**Execution plan:** [`../repository-grounding-plan.md`](../repository-grounding-plan.md)

## 1. Question

Should Sensemaking pursue full autonomy and full delegation by having agents
build detailed documentation of the repository they work on (a "repo ontology"
and product definition), instead of building more testing and validation
machinery? Does detailed repository and product knowledge make implementation
follow naturally?

Two outside analyses were reviewed. One argued for "compressed domain
grounding" (a product contract, an invariant ledger, and a technical blueprint)
and warned about documentation theater. The other kept full autonomy as the
goal, separated autonomy from authority, and argued for continuously updated
understanding instead of complete understanding before acting.

## 2. What the repository showed (2026-10-12, `main@1396b56`)

- **No artifact describes the target repository.** The main repo-facing
  artifact, `repository_sensemaking_brief`, requires `primary_fog_type`,
  `evidence`, and `recommended_workflow`
  (`skills/workflow-planner/references/artifact-contracts.yaml`). It is a
  one-time routing diagnosis. Nothing stores the target repo's entities,
  invariants, intent, non-goals, or past decisions for the next session.
- **The existing ontology describes Sensemaking itself.** `CONTEXT.md` (about
  4.6k words) defines fog types, warrants, gates, and control levels.
- **Documentation volume already exists, pointed inward.** `docs/` held 501
  Markdown files, about 714k words. Of about 240 commits since 2026-09-01, 132
  were `docs:` commits, mostly about Sensemaking's own state.
- **Context goes to process first.** `using-sensemaking` (about 6.3k words) and
  `repo-sensemaker` (about 4.6k words) put roughly 11k words of procedure in
  front of an agent before it reads any target-repo code.
- **Evidence is consistent with "context, not procedure, is the bottleneck".**
  The normal-use re-measure recorded 18 read-only episodes with 0 clearly
  Skill-favorable tasks (see PR #536 and `STATUS.md`). That does not prove net
  harm, but it is what this hypothesis predicts.
- **Full autonomy was never formally dropped.** `docs/product-strategy.md`
  names the high-delegation builder as the primary user, and
  `skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`
  honors "FULL AUTONOMY". In practice, the larger body of gates and lifecycle
  distinctions makes agents stop often.

## 3. Assessment of the core argument

**Holds:** for a capable coding agent, knowledge specific to the repository is
the main limit on non-trivial work.

**Does not hold, as stated:**

1. *"A detailed enough ontology and product definition makes the
   implementation follow."* A spec that contains every implementation detail
   is the implementation, written in a language that cannot be run or tested.
   Useful context is less detailed than code and constrains the right things:
   what must stay true, what is not wanted, what was tried and rejected. It
   narrows the solution space; it does not choose the solution.
2. *"Give the model the context and it knows what to do."* Context describes
   what **is**. The task is the gap between that and what **should be**, and
   the should-be lives with the owner and users, not in the code. An agent with
   perfect repo knowledge and no intent invents work, which
   `docs/product-strategy.md` already lists as a failure mode.

## 4. Rule for what to record

Record only what an agent cannot recover from the code. Turn whatever can be
checked into a check (a test, a type, a lint rule).

| Worth recording (not in the code) | Not worth recording (derivable; goes stale) |
| --- | --- |
| Intent, users, non-goals | Module lists, class taxonomies |
| Why decisions went one way; rejected alternatives | File-by-file descriptions |
| Invariants the code does not enforce | Restated function signatures |
| Known traps ("this broke before because...") | Architecture prose recoverable with grep |
| Work in flight; areas that are off-limits | Directory trees |

The model to copy is already in this repository: the "Verification discipline"
section of `CLAUDE.md` (about 370 words). Each rule exists because it caused a
real bug, it is dense, and an agent cannot derive it from the code.

## 5. Assessment of the two outside analyses

**Compressed domain grounding analysis**

- Right: documentation theater, prose going stale, the big-design-up-front
  comparison, a dense format for invariants, non-goals mattering more than
  goals.
- Wrong: it asked for "un-falsifiable boundaries"; boundaries should be
  *falsifiable*, and its own YAML example works because every line can be
  checked against code. "Superhuman at general programming" is overstated.
  "Confirm the blueprint, then ship without another question" needs one
  exception: if implementation contradicts the blueprint, update the blueprint.
- Risk: three new artifact types on top of about 50 skills; its directive is
  likely to become another plan document rather than a change in behavior.

**Continuous grounding analysis**

- Right: autonomy is separate from authority; product intent, repository
  reality, and system consequences are different kinds of knowledge; tests are
  executable knowledge (keep tests that protect product behavior, drop tests
  that only check framework-artifact shape); understanding and implementation
  feed each other; the useful comparison is direct agent vs. agent with a
  context pack vs. full Sensemaking.
- Weak: it missed that existing artifacts all describe Sensemaking itself. It
  defended "full autonomy is already permitted" on paper without addressing
  practice. It ended by recommending another investigation.

## 6. Full vs. mixed autonomy

The useful question is which decisions the agent can settle with what it
knows. Agreeing to "mixed" autonomy described the agent's current knowledge,
not a principle. Full autonomy is reached as owner knowledge moves into
artifacts.

**The ratchet:** every question the agent must ask the owner becomes a
permanent line in the target repo's intent/decision record, so it is never
asked again. Progress toward full delegation is then measurable as owner
questions per task over time.

## 7. Direction

1. Sensemaking's main output for a target repository becomes a small,
   maintained **Grounding Pack**: domain language, decision records, invariants
   and traps, and an intent file. Every line cites code or tests, cites an owner
   decision, or is marked as a hypothesis.
2. Process guidance shrinks to the few judgments that change behavior; the
   freed context goes to the target repo's pack.
3. The hypothesis is tested by real use on a real target repository, counting
   owner questions and rework, not by building new evaluation machinery.

The step-by-step plan is in
[`../repository-grounding-plan.md`](../repository-grounding-plan.md).
