# Prospective decision rehearsal (2026-11-25)

**Status:** product-capability procedure and one authentic selection
rehearsal. No new executable consumer or record type was retained.
**Source baseline:** `a40ec5e5ed31ceba8b45539bbffa076710cbf614`.
**Implementation:** `1cc0bdcd43b0d539d4a2a9542862c6d7a3781047`.
**Fresh-review revision:** `cae8d2c60a01fc3e3b4b20a48ad4418e5d6f69e8`.

The capability is a bounded reasoning procedure: before selecting or building a
possibility because it is coherent, test whether it would change a real
beneficiary decision. It composes existing possibility, method, hypothesis and
trial capabilities. It does not predict success or prove benefit.

## 1. Observed limitation

Two read-only opportunity explorers examined strategic possibility
discovery and experience-driven adaptation against `a40ec5e5`.

Their material findings:

- the ratified domain-general goal had one direct authored candidate and nine
  one-hop descendants; the landscape was thin at the top goal;
- only 7 of 19 opportunity claims had a `value_hypothesis`, and only 9 had a
  `revisit_when`;
- `possibility contrast` marks assumption dependence, not a beneficiary
  decision delta;
- `method context` exposed only 2 of 13 lessons because only 2 authored a
  method; the method corpus is thin;
- recent views and retrieval additions often produced no observable change in
  the next decision (`docs/normal-use/2026-11-24-assumption-contrast-fresh-use.md`,
  `docs/normal-use/2026-11-23-goal-family-opportunity-discovery.md`);
- receipts are continuity state, not a searchable experience base; but both
  explorers concluded that another unified locator would still not establish
  applicability or decision value.

The binding limitation was therefore **not missing retrieval breadth**. It was
the absence of a concrete beneficiary decision delta and a later observation
that could distinguish a valuable possibility from a coherent view.

## 2. Selected capability

`skills/using-sensemaking/references/prospective-decision-rehearsal-v1.md`
defines the optional procedure:

1. recover the candidate's authored evidence and assumptions;
2. recover a real beneficiary episode and its current decision;
3. consult relevant method experience when it could change the rehearsal;
4. state the candidate decision and its observable delta;
5. state the expected observation, failure condition and added cost;
6. select, build, defer, reject or investigate; `NO_DELTA` is valid.

The procedure reuses `product-outline`, `possibility-ecology`, `method context`,
`hypothesis`, `experiment-design` and `method trial`. It adds no schema, CLI,
planner, automatic selector or mandatory stage. A concise note in an existing
normal-use record or PR decision note is enough when the decision matters.

## 3. Authentic rehearsal

| Candidate | Beneficiary episode | Current decision | Candidate decision | Expected observation | Disposition |
| --- | --- | --- | --- | --- | --- |
| A question-relevant precedent locator over receipts, normal-use notes and explorations | This fifth-episode selection; 128 receipts, 75 normal-use notes and 31 explorations available | Inspect prior work manually and ask two read-only explorers | Query the locator, then inspect its top candidates | A prior precedent not already visible changes the selection | **REJECT — `NO_DELTA`** |
| A short precedent/applicability check in the existing decision note | A reviewer choosing a local increment with retained method experience | Decision note names consulted knowledge, not whether it applied | Name precedent, source revision, conditions checked and apply/adapt/reject/ignore | A real decision note shows a precedent disposition that changes or confirms the choice | **DEFER** — no observed episode of a missed precedent; existing guidance is already extensive |
| A product-possibility outcome loop joining value hypotheses to later observed evidence | An agent selecting product possibilities across episodes | Possibilities carry value hypotheses but no outcome link | Review later evidence and revise/reaffirm/reject the value hypothesis | A selected possibility has a real later outcome that changes a future selection | **DEFER** — too few selected possibilities have observable outcomes now |
| Reconsideration from indexed change (`poss:possibility-reconsideration-from-change`) | The 2026-11-05 premise-qualification episode; current decision qualified the retrieval premise, kept PATH-1 and made no automatic reassessment | Two target-repository possibilities whose value hypotheses depend on later-session consultation remain unreassessed | Inspect the affected possibilities and append a qualified/reaffirmed assessment linked to the episode | A new dated assessment entry that changes a later selection | **DEFER — `NO_DELTA`**; the trigger is free-text `revisit_when`, no typed claim/source is cited, and `workspace-changes` returned supporting-source churn with no `poss:` change. Data/shape limitation, not rejection |

For candidate A, the relevant prior work was already available: the
[2026-11-13 construction-versus-product-outcomes retrospective](../explorations/2026-11-13-construction-vs-product-outcomes-retrospective.md)
and the
[2026-11-17 opportunity landscape](../explorations/2026-11-17-cognitive-construction-opportunity-landscape.md)
were surfaced by the opportunity explorers and were already committed. The
locator added a second path to the same evidence, while its prototype required
one `git show` per artifact and was not materially faster than direct
inspection. The beneficiary decision did not change; the candidate was
rejected.

An untracked 12 KB prototype (`precedent_context.py`) was removed before this
record was committed. No executable consumer was merged.

## 4. Fresh-context review and revision

A separate fresh-context reviewer applied the procedure to
`poss:possibility-reconsideration-from-change` without a predetermined result.
It selected a real 2026-11-05 premise-qualification episode, inspected the two
target-repository possibilities, ran `workspace-changes` between `a40ec5e5` and
its then-current head, and found:

- the decisive `revisit_when` values are free text, not typed claim/source
  references;
- no typed claim or source in the two possibilities matched the 2026-11-05
  premise;
- `workspace-changes` reported supporting-source fingerprint churn and no
  `poss:` claim change;
- the candidate's trigger therefore could not fire in that episode.

It returned `DEFER` with `NO_DELTA` as a **data/shape limitation**, not a
rejection of the idea. It also judged the procedure useful as a stop rule but
partly ceremonial as an evidence procedure: the decisive work was reading the
idea library, counting the free-text conditions, reading the episode, and
running `workspace-changes`, which the first version did not name.

The revision adds a **mechanism-to-data check** after candidate recovery: run
the existing consumer on a real revision pair and record whether the trigger
fields are populated and matchable. If not, stop with `NO_DELTA`/`DEFER` as a
data/shape limitation. This directly addresses the fresh reviewer's finding.

## 5. Why this is a capability, not a plan

The procedure was exercised on real candidates and changed a real selection:
it rejected the precedent locator and deferred two premature loops. It leaves a
portable method that a later agent can apply to another candidate, and it makes
`NO_DELTA` a legitimate product outcome rather than a failure. The retained
artifacts are the procedure and this source-linked rehearsal, not a new record
schema or a roadmap.

## 6. Product versus model

**Product:** possibility and method consumers, authored candidate evidence,
receipts, normal-use records, existing hypothesis/experiment/trial carriers,
and the new procedure reference.

**Model:** reconstructed the beneficiary episodes, compared current and
candidate decisions, judged that the locator added no decision delta, deferred
the other candidates, and selected the procedure itself. The product did not
choose the dispositions.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 7. Claim ceiling

| Level | Status |
| --- | --- |
| Procedure documented and applied to real candidates | Observed |
| Rejection of the precedent locator | Observed decision in this episode |
| Deferral of the other two candidates | Observed |
| Fresh-context use of the procedure | Observed; same-session review, not longitudinal independence |
| Later independent use of the procedure | NOT ASSESSED |
| Changed beneficiary outcome or comparative benefit | NOT ESTABLISHED |
| Longitudinal cognitive development | NOT ESTABLISHED |

## 8. Continuation

The next warranted use is an independent later agent applying the rehearsal to
a candidate that has a real beneficiary episode and a plausible observable
delta, then recording whether the candidate was selected or rejected. No new
CLI, locator, outcome schema or mandatory stage is warranted without that use.
A later `NO_DELTA` remains a successful stop.
