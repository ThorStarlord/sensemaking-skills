# Fresh evaluation: assumption-contrast candidate (2026-11-24)

**Status:** fresh-context evaluation and correction. **Base:** `6fd3d765`.
**Fresh evaluation revision:** `bafa004b35b6f933d249608e9d0b9670ca015419` (cherry-picked into this branch as `03c3c7cb`).
**Subject:** `poss:assumption-contrast-inquiry` and the new
`semantic possibility contrast` operation.

This record preserves a negative result. The contrast operation was useful as
an auditable view, but the fresh agent judged the new candidate too narrow and
overlapping with `poss:assumption-aware-opportunity-ecology`. The candidate was
narrowed rather than retained as a distinct substantial direction.

## 1. Fresh task

The fresh agent was asked to evaluate whether the new candidate was:

- a distinct, sufficiently warranted direction;
- a duplicate or too-narrow variant of an existing candidate;
- in need of revision or rejection.

It was not told the parent's preferred answer. It recovered the goal, the new
candidate, the existing candidates and the contrast procedure from the
repository.

## 2. Scenarios and observed contrast

It authored five scenarios:

| Scenario | Assertion |
| --- | --- |
| `base` | none |
| `no-cross-episode-recurrence` | negate `hyp:cross-episode-synthesis-recurs` |
| `no-later-session-consult` | negate `hyp:later-sessions-consult-knowledge` |
| `held-cross-episode` | hold `hyp:cross-episode-synthesis-recurs` |
| `no-agent-semantic-control` | negate `con:agent-owns-semantic-control` |

At `goal:compounding-product-knowledge` the contrast returned 6 candidates and
3 assumptions:

| Scenario | Affected | Unaffected | Unassessed |
| --- | ---: | ---: | ---: |
| `base` | 0 | 5 | 1 |
| `no-cross-episode-recurrence` | 4 | 1 | 1 |
| `no-later-session-consult` | 2 | 3 | 1 |
| `held-cross-episode` | 0 | 5 | 1 |
| `no-agent-semantic-control` | 2 | 3 | 1 |

The only `NOT_ASSESSED` candidate in that ecology was
`poss:assumption-aware-opportunity-ecology` — the candidate whose statement is
itself about assumptions. Shared assumptions were reported with missing direct
relations, and four candidates had partial one-hop relationship coverage.

## 3. Fresh judgment

**Primary judgment:** a too-narrow variant of
`poss:assumption-aware-opportunity-ecology`, not a distinct sufficiently
warranted `SUBSTANTIAL` direction. Revise or fold it; do not reject outright.

Strongest evidence for distinctness:

- the new candidate names a diagnostic negation move, while the existing
  candidate is framed around generative family exploration;
- the operation and procedure are real, not merely a proposal;
- the contrast surfaced a plausible pairing with
  `poss:goal-family-construction-bridge` through
  `con:agent-owns-semantic-control` (a pre-bridge premise check) that the
  fresh agent said it would likely have missed.

Strongest evidence against:

- the existing candidate already covers shared premises and
  assumption-dependent futures;
- a prior decision (`decision:possibility-ecology-projection`) treated a
  similar read-only projection as a decision, explicitly not the full
  assumption-aware ecology;
- the 2026-11-05 normal-use record warned that re-presenting this benefit as
  new is restated or an implementation mechanism;
- the contrast is set projection over already-visible one-hop data; it adds a
  view, not new semantic information;
- the candidate's `hyp:cross-episode-synthesis-recurs` assumption is not
  clearly load-bearing for within-episode premise checking;
- `SUBSTANTIAL` ambition is overstated for a read-only view plus optional
  guidance;
- no independent use, decision influence or comparative benefit exists.

**Did the contrast change its view?** It confirmed the concern rather than
dispelling it. It made the existing candidate's zero authored assumptions
immediately visible and surfaced one plausible pairing, but it did not expose a
decision-changing assumption or an unrepresented direction that the ecology
view could not have supported.

## 4. Functional defect found and fixed

With `--limit 2`, the contrast silently analyzed 2 of 6 candidates while the
underlying ecology query disclosed `candidate_omitted: 4`. The fresh agent fixed
the omission in `bafa004b`:

- propagate `candidate_omitted` and `descendant_candidate_omitted` into the
  contrast coverage;
- add an explicit limit saying the scenario results are partial when candidates
  were omitted;
- document that `held` is only a conflict check, not a classification change.

This is a real defect in the new capability and was integrated.

## 5. Parent response

The parent accepted the fresh judgment and did not preserve the original
framing:

- the candidate was narrowed to `INCREMENTAL` ambition, an evaluation variant
  within the assumption-aware ecology rather than a distinct substantial
  direction;
- the non-load-bearing `hyp:cross-episode-synthesis-recurs` assumption was
  removed;
- a `NARROWED` disposition was recorded with the fresh evaluation as source;
- the contrast operation and portable procedure remain, because they are real
  functional support even if the candidate is not a new product direction;
- the candidate remains hypothetical; no realization, selection or
  authorization is claimed.

The operation was not deleted. Its value is as a bounded evaluation view and
procedure, not as a new generative capability.

## 6. Evidence ceiling

Same-agent source inspection and real CLI output at one revision. The fresh
agent authored the scenarios and interpreted them; the parent integrated the
result. This is an authentic fresh-context evaluation, not independent
longitudinal qualification, comparative benefit or proof that the contrast
improved a decision.
