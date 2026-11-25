# Predecision method trials (2026-11-24; repaired 2026-11-25)

**Status:** repaired workflow contract and one anchored, same-agent method
trial. The first trial remains an unanchored smoke test.
**Source baseline:** `64ef6310a9b6d384e51158861dcef5f6101f8d34` (PR #965).
**Anchoring producer:** `80bd0a7eac39910330a620e0bdb80958c76fe16b`.
**Decision-only commit:** `fc297357f4978d0bcde1413a9347f18a6a557467`.
**Enforcement:** `ce3e58c41faa7b40eecd2c0f61be976ae0be56f9`.
**Retained result:** `e8c6f0ad5e696a2deaf8e5500b4e544df7e3cf51`.

The capability is a predecision method commitment with a later observed result.
It does not prove that the method caused the result or that the method is
generally effective.

## 1. Current limitation

The existing method path had two useful halves:

- `semantic method context` retrieves reviewed lessons with procedure, scope,
  conditions, counterevidence and original outcome;
- `semantic method record` can materialize a post-episode observation and a
  conditional lesson, optionally linked to an authored decision.

The missing part was temporal and structural: the agent could record a method
episode after the outcome, but could not preserve what method it committed to
before the work, what observable result it expected, and which later result
belonged to that commitment. A later reader could not distinguish a
predecision method choice from a retrospective interpretation.

The first implementation in PR #965 added the record pair but left four
defects: it did not require a later descendant close, hard-coded
`predecision_commitment_preserved`, could silently miss a closing record in a
truncated explain envelope, and did not surface the result to method context.
Its first trial was also committed with the implementation it evaluated.

## 2. Delivered capability

`semantic method trial` uses existing `decision` and `observation` claims:

| Command | Behavior |
| --- | --- |
| `trial open` | Writes an `OPEN` decision with the question, selected method, assumptions, expected observation, optional prior lesson, tracked evidence and claim ceiling, a SHA-256 `trial_digest`, and evidence paths absent at the declared revision. The proposal must be reviewed and committed before the work. |
| `trial close` | Requires the exact `decision_commit` and a later descendant `source_revision`, verifies the decision digest, and appends a separate `observation` linked by `closes_trial`. It rejects a same-revision or non-descendant close, a second closing observation, a mismatched trial id/digest and an `ADAPTED` result without `method_after`. |
| `trial show` | Reconstructs the predecision commitment and the later result. It fails closed on a truncated explain envelope, multiple closing relations, or a closing record that does not match the trial. `predecision_commitment_preserved` is true only with matching decision/result digests and verified later Git ancestry; legacy trials report `NOT_ASSESSED`. |

No new claim kind, schema, controller or ranking surface was added. The
disposition is agent-authored; `CONFIRMED` means the expected observation was
seen, not that the method caused it. A lesson-informed close also writes
`trial_result_for` to the lesson, so `method context` shows the result beside
the trial decision.

## 3. Authentic use

The retained trial addressed a real repair decision:

- **Question:** should the repair enforce close chronology, decision-content
  anchoring and fail-closed inspection in the producer, rather than relying on
  documentation?
- **Method:** require the exact decision commit and later descendant revision,
  verify the content digest, reject a second closure, fail closed on a
  truncated envelope, and expose a lesson-informed result to method context.
- **Assumptions:** the decision carries a digest; the close can name the
  decision commit; Git ancestry is available locally; explain reports
  truncation explicitly.
- **Expected observation:** named commands reject a same-revision close, a
  non-descendant close, a duplicate close and a truncated show; the retained
  show reports matching digests and verified ancestry; the legacy trial reports
  `NOT_ASSESSED`; method context lists the result.

The decision was committed alone in `fc297357`, before the enforcement in
`ce3e58c4`. Observed results:

- `show` at the decision commit reported `closed: false`,
  `trial_digest_match: MATCH`, preservation false with reason `TRIAL_OPEN`.
- A close at the decision commit exited non-zero with "must be later"; a close
  at an ancestor revision exited non-zero with "must descend".
- `show --limit 1` exited non-zero because the explain envelope was truncated.
- The legacy `decision:method-trial-discovery-surface` reported
  `trial_digest_match: NOT_ASSESSED` and preservation false.
- On a disposable descendant of the enforcement revision, close succeeded,
  `show` reported `MATCH`/`MATCH`/`VERIFIED` and preservation true, and method
  context listed the result with `trial_result_for`.
- The retained result in `e8c6f0ad` repeats that pair; a duplicate close is
  rejected.

This is a same-agent implementation trial. It demonstrates the enforcement and
the anchored pair; it does not establish independent use or decision benefit.

## 4. What the product provides versus the model

**Product:** source/revision validation, digest anchoring, descendant-commit
enforcement, duplicate/ambiguous closure rejection, fail-closed truncation and
ancestry handling, and a deterministic show/context projection.

**Model:** selected the enforcement method, stated the assumptions and expected
observation, authored the episodes, performed the checks, chose the disposition
and interpreted the result. The product did not select the method or judge
whether the enforcement was the right engineering choice.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Predecision decision and later observation pair | Observed through the real CLI and committed records |
| Decision committed before the enforcement it trials | Observed in Git history |
| Later-descendant close enforced | Observed: same-revision and non-descendant closes rejected |
| Duplicate closure rejected | Observed |
| Content digest and result digest matched | Observed in the retained pair |
| Truncated show fails closed | Observed with `--limit 1` |
| Legacy unanchored trial reported `NOT_ASSESSED` | Observed |
| Method context lists the trial result | Observed with `trial_result_for` |
| Method effect or causality | NOT ESTABLISHED |
| Independent later-agent use | NOT ESTABLISHED |
| Decision benefit or comparative benefit | NOT ESTABLISHED |
| Longitudinal development | NOT ESTABLISHED |

The first trial is self-referential and lacks digest/decision-commit anchors; it
remains a compatibility fixture, not preservation evidence. The second trial is
still same-agent and concerns the enforcement mechanism itself.

## 6. Continuation

The next warranted use is an independent later agent applying a trial to a real
method choice with a falsifiable expected result, then closing it with
evidence. No further producer, ranking, method selector or mandatory trial
stage is warranted without that use. A justified `NO_MODEL_CHANGE` remains a
valid outcome.
