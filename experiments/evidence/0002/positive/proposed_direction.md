# Proposed Direction

## summary

We want to strengthen confidence that the orchestration runtime's live
execution path (skill invocation, artifact production, validation, and gating)
actually works end-to-end, not just in structural/unit tests, because a past
completion claim (issue #39) turned out not to be independently verifiable
from repository history.

## proposed_response

Run the real `architectural-review-planning-workflow` against a disposable
target repository using the live `claude-code` executor in
`guided_execution` mode, preserve every artifact and log the run produces
(intent, brief, proposed direction, recommendation, run log, validator
output, exit codes), and also run a negative-path invocation that omits
`proposed_direction.md` to confirm the input contract is enforced with an
explicit failure rather than a silent one. Commit the preserved evidence to
the repository so future audits do not have to trust a free-text summary.

## success_criteria

- The positive-path run produces a validated brief and a validated
  recommendation, both committed as artifacts alongside their run log.
- The negative-path run fails explicitly at input resolution (no
  architectural-review invocation, no recommendation produced) and this is
  captured in a preserved run log.
- The disposable target repository is left unmodified by both runs.
- The evidence is reviewable in a PR, not summarized only in a comment.
