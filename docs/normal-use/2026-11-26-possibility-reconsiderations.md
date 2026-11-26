# Possibility reconsideration signals (2026-11-26)

**Status:** generative review capability, exercised on a real change and used to
reconsider a retained possibility.
**Source baseline before the capability:** `feeaecf95df58b675b29e9e8356dc921419e9cca`.
**Capability merge:** PR #976, `8c9ac0ce0e4f8e9964fb698b41500eb614eb74ee`.
**Real follow-up change:** `403b8d389a26fa59e8c1d4dce0aa0f2659c2e527`.

## 1. The cognitive-substance gap

A direct inspection of the authored knowledge pack found 21 opportunities.
Eleven had a `revisit_when`; ten had none. None of the eleven contained a
claim, file or symbol reference that a mechanical review could evaluate:

- `workspace-review-context --include-candidates` before this episode:
  `with_condition: 11`, `fired: 0`, `not_assessed: 11`, coverage `PARTIAL`.
- The same review after the capability and one authored condition:
  `with_condition: 12`, `fired: 1`, `not_assessed: 11`, coverage `PARTIAL`.

The limitation was not a missing retrieval mechanism. The conditions existed,
but they were prose that named no inspectable premise.

## 2. Delivered capability

`workspace-review-context --include-candidates` now adds
`candidate_reconsiderations`. An authored `revisit_when` may embed:

- `file:path/to/file`
- `claim:kind:identifier`
- `symbol:path/to/file.py#name`

The review evaluates only those references:

- `file:` matches committed changed paths, plus worktree path names when
  `--include-worktree` is used;
- `claim:` compares the normalized claim record at BASE and TARGET and checks
  whether its authority or evidence paths changed;
- `symbol:` reuses the existing source-level behavior comparison for one Python
  definition; a file unchanged between the revisions is `NO_MATCH` without
  running the comparison.

Each possibility receives `FIRED`, `NO_MATCH` or `NOT_ASSESSED` with per-ref
evidence. Surrounding prose is reported as `unstructured_text`, not interpreted.
Fired conditions are returned first, followed by no-match and not-assessed;
this is a review visibility order, not a value ranking.

## 3. Knowledge development

`poss:possibility-reconsideration-from-change` was updated from
`NOT_IMPLEMENTED` to `PARTIALLY_IMPLEMENTED`. Its realization basis now names the
review-context implementation and its limits. It gained a real structured
condition:

> A later change modifies the review-context condition evaluator or its
> consumer: `file:src/sensemaking_skills/semantic_architecture/possibility_revisit.py`
> or `file:src/sensemaking_skills/workspace_knowledge.py`. Also revisit when an
> independent agent uses a structured condition to reconsider a retained
> possibility.

This condition is grounded in the actual dependency, not a generated attribute.
Nine opportunities still have no condition and eleven still have unstructured
prose; neither gap was mechanically populated.

## 4. Authentic use and observed outcome

After PR #976 merged, a real follow-up optimization was made: skip the symbol
behavior comparison when the symbol's file is unchanged, and reuse the BASE
claim map when both revisions are equal. The change touched
`possibility_revisit.py`.

Review from `8c9ac0ce` (main with the structured condition) to `403b8d38`:

- `poss:possibility-reconsideration-from-change` → `FIRED`
  - `file:.../possibility_revisit.py` → `FIRED`, `CHANGED_PATH`
  - `file:.../workspace_knowledge.py` → `NO_MATCH`, `PATH_UNCHANGED`
  - prose remains visible as `unstructured_text`
- 11 other conditions remain `NOT_ASSESSED`
- coverage `PARTIAL`; `fired: 1`; no ranking, selection or automatic revival

The condition did what it was authored to do. The agent then inspected the
change and kept the possibility `PARTIALLY_IMPLEMENTED`: the optimization
improves the evaluator but does not establish semantic consequence or
independent use.

## 5. What this use does not show

The first fired condition was caused by a change to the evaluator itself. It
demonstrates the mechanism, not a real-world premise change. No condition yet
fires on an external product file, claim or symbol change. Eleven of twelve
authored conditions remain unassessable. A fired reference is a reconsideration
prompt, not a staleness verdict, decision, revival or authorization.

The capability also does not interpret the prose around references, infer that
a changed claim is semantically relevant, or compare runtime behavior. The
`symbol:` path is source-level only.

## 6. Product versus model

**Product:** commit-exact claim loading, structured-reference parsing, changed
path matching, normalized claim comparison, source-level symbol comparison and
explicit status/coverage reporting.

**Model:** selected the possibility, authored the condition, judged the fired
result, kept the realization partial and recorded the limitation. The product did
not decide that the possibility should be revived or that the change was
beneficial.

## 7. Claim ceiling

| Level | Status |
| --- | --- |
| Structured condition parsing and review surface | Observed |
| Real condition fires on a changed referenced file | Observed |
| Claim and symbol reference evaluation | Mechanically implemented; not yet used by authored conditions |
| Real external premise change | NOT OBSERVED |
| Reconsideration changed a decision or disposition | NOT OBSERVED |
| Independent later-agent reuse | NOT ESTABLISHED |
| Comparative cognitive benefit | NOT ESTABLISHED |
| Longitudinal development | NOT ESTABLISHED |

## 8. Continuation

The next warranted use is a condition grounded in an external dependency — a
product file, claim or symbol whose change is meaningful to the possibility —
and an observation of whether the fired signal changes the agent's
reconsideration. Until then, do not extend the grammar, add a general trigger
system, or mechanically populate the remaining conditions. The existing
prose-only conditions remain an honest `NOT_ASSESSED` gap.
