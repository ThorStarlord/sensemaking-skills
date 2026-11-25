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
   - `expected_observation`: what observable result would count for or against
     the method;
   - `prior_lesson_id` if a reviewed lesson is being applied;
   - tracked `evidence_refs` and a `claim_ceiling`.
3. **Open and commit the trial before doing the work.**
   ```bash
   sensemaking-skills semantic method trial open --repo . \
     --episode artifacts/history/<trial>.json \
     --output .sensemaking/knowledge/method-trial-<id>.json --json
   ```
   Review the proposal and commit it. The decision is the predecision record.
4. **Do the work.** Collect the evidence named in the expected observation.
5. **Author the close episode.** Record the actual outcome, a disposition
   (`CONFIRMED`, `ADAPTED`, `REJECTED`, `NO_CHANGE` or `INCONCLUSIVE`), tracked
   evidence and a claim ceiling.
   ```bash
   sensemaking-skills semantic method trial close --repo . \
     --episode artifacts/history/<trial>-result.json \
     --output .sensemaking/knowledge/method-trial-<id>-result.json --json
   ```
   Commit the result proposal.
6. **Inspect the pair.**
   ```bash
   sensemaking-skills semantic method trial show --repo . --ref HEAD \
     --trial decision:method-trial-<id> --json
   ```
   The output shows the predecision method, assumptions and expected
   observation beside the later result. `method_effect_established` remains
   false.
7. **Reconcile only if warranted.** If the result supports a reusable
   adaptation, use the existing method-record producer. A one-off trial and a
   justified `NO_MODEL_CHANGE` are valid.

## Failure modes

- **Retrospective trial:** opening after the outcome is not a predecision
  record.
- **Unfalsifiable expectation:** "it works better" is not an observable
  result.
- **Disposition without evidence:** do not close a trial on a feeling.
- **Causal overclaim:** `CONFIRMED` means the expected observation was seen,
  not that the method caused it.
- **Trial inflation:** not every task needs a trial; trivial work should
  proceed directly.
- **Shared-policy promotion:** a successful trial does not rewrite Skills or
  common policy automatically.

## Evidence ceiling

A trial establishes that an agent authored a predecision commitment and a
later observed result at pinned revisions. It does not establish that the
method was applicable, that the observation is complete, that the method
caused the outcome, or that another agent would benefit. Those remain separate
claims and, where comparative, separate qualification.
