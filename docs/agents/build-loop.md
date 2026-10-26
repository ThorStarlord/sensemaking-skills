# Build Loop: Choosing and Building an Increment

How a coding agent selects, builds and closes one increment of work in this
repository. `CLAUDE.md` carries the short trigger; this page carries the detail.
It adds no runtime, Skill or artifact type. It applies the existing control law
in `CONTEXT.md` ("lower levels may execute decisions delegated from higher
levels, but they may not silently redefine commitments owned by the higher
level") to a single increment.

Each increment has three steps:

```text
ARCHITECT  ->  decision note  ->  BUILDER  ->  PR + evidence  ->  CLOSE
(what, why,     (the handoff)     (how)                          (readout)
 which slice)
```

The decision note is the API between the architect and builder steps, in the
same sense that artifacts are the API between Skills.

## 1. Architect step

### Read, in this order

1. **Last readout.** Did the previous increment get used? What did CI say?
   What did its STATUS entry ask the next agent to observe?
2. **Compass.** Orientation, not a gate:
   - `CONTEXT.md` "Current product definition";
   - `docs/product-strategy.md` §1 (purpose and outcome);
   - `docs/adr/0029-current-product-boundary.md` (in scope / out of scope);
   - `docs/persistent-semantic-stewardship-plan.md` §12 (value criteria) and
     §14 (construction order);
   - `STATUS.md` "Current next step" and open owner questions.

   Root `roadmap.md` is historical and superseded; do not use it.
3. **Model state.** What the reviewed knowledge in `.sensemaking/knowledge/`
   holds and lacks, compared with the kinds the schema accepts
   (`src/sensemaking_skills/semantic_architecture/knowledge.py`).
4. **Constraints.** Authority limits and owner-reserved decisions.

Do not read the whole source-of-truth map in `CONTEXT.md`. Read further only
where the candidate touches it.

### Then

1. **Diverge.** List five to eight candidates from different lenses: compass
   gaps, roadmap packages, user journeys, knowledge-model gaps, defects, debt.
   One line each.
2. **Converge.** Score candidates against these criteria, written down before
   choosing:
   - which goal in product strategy §1 it serves;
   - which §14 package it advances;
   - which §12 dimension it improves;
   - reversibility;
   - size (a complete vertical slice, not a partial one);
   - whether an owner decision gates it.
3. **Challenge the pick.** Name the strongest alternative and what would make
   the pick wrong. Ask whether it is simply the easiest thing to verify.
4. **Design the slice.** Files and contracts touched (use the Steward's
   `context-for` RECALL, and `change-impact-analysis` for wide changes), what
   is out of scope, what done looks like, and what to observe after merge.

### Output: the decision note

Put it in the PR description's "Why this increment" section. The session
receipt may point to the PR; reasoning does not belong in the receipt.

```text
Increment:    one sentence
Serves:       goal (product strategy §1), package (§14), dimension (§12)
Rejected:     2-3 alternatives, one line each on why not
Slice:        files and contracts touched; explicitly out of scope
Done when:    acceptance criteria
Verify:       exact checks before merge
Probe:        what use after merge would show it mattered
Owner input:  none | the question
```

- If no `Serves` line can be filled with a citation, do not build the
  candidate as a roadmap increment. It may still be done as labelled
  maintenance.
- If `Owner input` is not `none`, stop and ask, or use
  `owner-decision-capsule`. Goals, non-goals and authority are never inferred
  from code.

### Depth scales with reversibility

| Change | Architect depth |
| --- | --- |
| Reversible and small (code fix, doc correction) | A ten-line note |
| Durable commitment (schema kinds, reviewed knowledge agents will trust, public contracts) | A fuller pass; possibly an ADR or an owner decision capsule |

## 2. Builder step

- **Input:** the decision note, plus `context-for` on each file in the slice.
- **Stay in scope.** Keep the diff to the note's files and contracts. Small
  adjustments to how are fine; changes to what or why are not.
- **Kick back.** If the slice proves bigger, a contract does not exist, or the
  premise is false, stop and return to the architect step with the finding.
- **Park discoveries.** Out-of-scope findings become candidates for the next
  architect step, not part of this diff.
- **Verify as declared.** Follow `CLAUDE.md` "Local verification scope" and
  the PR rules there. State plainly what did not run.
- **Output:** a PR whose description is the decision note plus the evidence.

## 3. Close

- Add a `STATUS.md` entry for the increment, including its probe question.
- Reconcile reviewed knowledge only when the change made a claim false or
  created consequential, reusable knowledge.
- The next architect step starts by reading this readout.

## Failure modes this guards against

| Failure | Guard |
| --- | --- |
| Building whatever is easiest to verify | Criteria written before choosing; `Serves` must cite |
| Analysis that never ends in building | The architect step's only output is the note |
| Builder redesigning silently | Diff compared with the note's slice in review |
| Probe never read | Readout is the first input of the next architect step |
| Agent inventing owner intent | Goals and authority are questions, not assumptions |
