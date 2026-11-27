# Method Trial v1

**Status:** optional agent-facing workflow. It preserves a predecision method
commitment and a later observed result using existing `decision` and
`observation` claims. It does not select a method, prove causation or promote
a lesson.

## When to use

Use a trial when:

- a consequential task requires a method or approach choice;
- a retained lesson or explicit procedure could inform that choice;
- the agent can state an observable result that would count for or against
  using it;
- the predecision commitment and later outcome need to be distinguishable.

Do not use a trial for a trivial task, a purely local edit, or a decision whose
method and outcome are already fixed. A trial is not a mandatory reflection
stage.

```text
predecision commitment != proof the method caused the outcome
disposition            != causal attribution
trial                  != independent validation or qualification
observed result        != a new shared method
```

## Procedure

1. **Retrieve relevant experience if it exists.**
   ```bash
   sensemaking-skills semantic method context --repo . --ref HEAD \
     --question "<current method question>" --json
   ```
   Inspect the lesson's procedure, conditions, counterevidence and original
   outcome. A miss is `NOT_ASSESSED`, not a reason to stop.
2. **Author the open episode before the work.** Include:
   - `trial_id` (lowercase slug);
   - `actor`, exact `source_revision`, `origin_date`;
   - `question`: the method decision, not the implementation task;
   - `method`: the approach being tried;
   - `assumptions`: what must hold for the trial to be meaningful;
   - `expected_observation`: a result that named commands, tests or artifacts
     can show;
   - `prior_lesson_id` if a reviewed lesson is being applied;
   - tracked `evidence_refs` and a `claim_ceiling`.
3. **Open and commit the decision before the work it trials.**
   ```bash
   sensemaking-skills semantic method trial open --repo . \
     --episode artifacts/history/<trial>.json \
     --output .sensemaking/knowledge/method-trial-<id>.json --json
   ```
   Review the proposal and commit the decision and episode. Do not put the
   implementation in that commit; otherwise the record only precedes the
   result, not the work. The decision carries a `trial_digest` and discloses
   any evidence path that did not exist at `source_revision`.
4. **Do the work.** Collect the evidence named in the expected observation.
5. **Author the close episode.** Record:
   - `decision_commit`: the commit that introduced the trial decision and must
     still contain the same anchored decision;
   - `source_revision`: a later descendant commit;
   - `observed_outcome`, tracked evidence and a claim ceiling;
   - `disposition`;
   - `method_after` when the disposition is `ADAPTED`.
   ```bash
   sensemaking-skills semantic method trial close --repo . \
     --episode artifacts/history/<trial>-result.json \
     --output .sensemaking/knowledge/method-trial-<id>-result.json --json
   ```
   The producer rejects a close at the decision commit, a non-descendant
   revision, a mismatched trial digest, a second closing observation and an
   `ADAPTED` result without `method_after`. Commit the result proposal.
6. **Inspect the pair.**
   ```bash
   sensemaking-skills semantic method trial show --repo . --ref HEAD \
     --trial decision:method-trial-<id> --json
   ```
   `show` refuses a truncated explain envelope; raise `--limit` (default 50)
   rather than treating missing records as absence. It also refuses ambiguous
   or mismatched closure. `predecision_commitment_preserved` is true only when
   the decision digest matches, the result digest matches and Git ancestry
   confirms a later descendant. Legacy trials without anchors report
   `NOT_ASSESSED` and `false`. `method_effect_established` remains false.
7. **Reconcile only if warranted.** If the result supports a reusable
   adaptation, use the existing method-record producer. A one-off trial and a
   justified `NO_MODEL_CHANGE` are valid.

## Dispositions

| Value | Meaning |
| --- | --- |
| `CONFIRMED` | The named expected observation was seen. It does not confirm the method's general effectiveness. |
| `ADAPTED` | The method was changed during the work; `method_after` records what replaced it. |
| `REJECTED` | The method was abandoned because the expected observation was not seen or contrary evidence appeared; say which. |
| `NO_CHANGE` | The trial completed and no method change is warranted. |
| `INCONCLUSIVE` | Evidence is insufficient, confounded or incomplete; no method judgment. |

These values describe the trial, not a promoted lesson. They are not the same
vocabulary as `method record`'s `develop|adapt|apply|reject|no_change`; a
trial result becomes a reusable method only through that separate producer.

When a trial names a prior lesson, closing the trial also writes a
`trial_result_for` relation from the result to that lesson. `method context`
then shows the result as a later record beside the decision, so a future
retrieval does not stop at the predecision half.

### Recover a precedent without its exact ID

When a later consequential decision could benefit from prior trial
experience, `semantic method context --repo . --ref HEAD --question QUESTION
--include-trials --json` adds a separate `trial_precedents` family. The
question matches reviewed trial decisions lexically, independent of whether
a trial links to a lesson. Each candidate uses the existing exact-ID
projection; incomplete or invalid projections are explicitly unassessed,
not open trials. Unanchored legacy results retain their original limits.

For a future-capability or responsibility choice, the same family can be
requested with `workspace-query --operation product-outline` or
`--operation possibility-ecology`, `--method-question QUESTION` and
`--include-method-trials`. Both portions are pinned to the resolved source
revision. The agent decides if the earlier question, procedure, assumptions
and observation matter to the present composition. Neither discovery nor
closure establishes applicability or improved cognition.

## Failure modes

- **Retrospective trial:** opening after the outcome is not a predecision
  record.
- **Decision committed with its implementation:** the decision then precedes
  only the result. Commit the decision alone.
- **Same-revision close:** closing at the decision commit is rejected; a later
  descendant is required.
- **Unanchored legacy trial:** a trial without `trial_digest`/`decision_commit`
  is reported `NOT_ASSESSED`, not treated as preserved.
- **Truncated inspection:** a truncated `show` is an error, not evidence that
  the trial is open or unclosed.
- **Self-fulfilling expectation:** an expected observation that can only be
  confirmed by the act of closing does not test the method.
- **Disposition without evidence:** do not close a trial on a feeling.
- **Causal overclaim:** `CONFIRMED` means the expected observation was seen,
  not that the method caused it.
- **Trial inflation:** not every task needs a trial; trivial work should
  proceed directly.
- **Shared-policy promotion:** a successful trial does not rewrite Skills or
  common policy automatically.

## Evidence ceiling

A trial establishes that an agent authored a predecision commitment and a
later observed result at pinned revisions, with the decision content anchored
against later edits. It does not establish that the method was applicable,
that the observation is complete, that the method caused the outcome, or that
another agent would benefit. Those remain separate claims and, where
comparative, separate qualification.
