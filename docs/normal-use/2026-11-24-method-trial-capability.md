# Predecision method trials (2026-11-24)

**Status:** intellectual-capability increment and one authentic design trial.
**Source baseline:** `8018f07c7792148bbfc3b77df38576327e4f7d41`.
**Implementation:** `67b3db447eaa5b336e17ed12ed85bb2ae767fad1`.
**Completed trial:** `ebf82c8cf2274ba597c316450314a3cc06c21cd0`.

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

This is a documented limitation in the SCL/Method Adaptation records. It is a
consumer gap, not a request for a new universal learning engine.

## 2. Delivered capability

`semantic method trial` uses existing `decision` and `observation` claims:

| Command | Behavior |
| --- | --- |
| `trial open` | Writes an `OPEN` decision with the question, selected method, assumptions, expected observation, optional prior lesson, tracked evidence and claim ceiling. The proposal must be reviewed and committed before the work. |
| `trial close` | Appends a separate `observation` linked by `closes_trial`, with the observed outcome, disposition, evidence and claim ceiling. It rejects duplicate result identifiers and does not rewrite the predecision decision. |
| `trial show` | Reconstructs the predecision commitment and the optional later result. `predecision_commitment_preserved` is true only when the pair is structurally present; `method_effect_established` remains false. |

No new claim kind, schema, controller or ranking surface was added. The
disposition is agent-authored; `CONFIRMED` means the expected observation was
seen, not that the method caused it.

## 3. Authentic use

The first trial addressed a real design decision for the capability itself:

- **Question:** should the method-trial capability add a list command, or is
  exact-ID show sufficient?
- **Method:** prefer the smallest consumer surface; use exact-ID show and the
  open proposal plus commit as the discovery path; add a list only if a real
  discovery failure is observed.
- **Assumptions:** the open proposal output names the trial decision id and
  path; a reviewer can commit it and show it by exact id; no list is needed for
  the bounded capability.
- **Expected observation:** the trial can be opened, committed, shown by exact
  id, and closed; no missing discovery path is observed; no list command is
  warranted.
- **Evidence:** the producer, CLI documentation and method-trial reference.

The trial decision was committed in `67b3db44` before the result. The open
view was inspected with `semantic method trial show` (`closed: false`). The
result was appended in `ebf82c8c` with disposition `CONFIRMED`; the closed view
reports `closed: true`, the predecision fields and the result, with
`method_effect_established: false`.

The observed result supported the method: the exact-ID show path was sufficient
and no list was built. This is a same-agent design decision, not an independent
method trial.

## 4. What the product provides versus the model

**Product:** source/revision validation, append-only decision/observation
pairing, duplicate-closure rejection, and a deterministic show surface.

**Model:** selected the method, stated the assumptions and expected
observation, performed the review, chose the disposition and wrote the
evidence. The product did not select the method or interpret the outcome.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Predecision decision and later observation pair | Observed through the real CLI and committed records |
| Exact source revisions and evidence preservation | Observed mechanically |
| Duplicate closure rejected | Observed |
| Method effect or causality | NOT ESTABLISHED |
| Independent later-agent use | NOT ESTABLISHED |
| Decision benefit or comparative benefit | NOT ESTABLISHED |
| Longitudinal development | NOT ESTABLISHED |

The first trial is self-referential: it decided a surface of the trial
capability itself. It demonstrates that the predecision/outcome machinery
works, not that a later agent uses it well.

## 6. Continuation

The next warranted use is an independent later agent applying a trial to a
real method choice with an observable expected result, then closing it with
evidence. No further producer, ranking, method selector or mandatory trial
stage is warranted without that use. A justified `NO_MODEL_CHANGE` remains a
valid outcome.
