# Cognitive integration — canonical verification and next responsibility

**Scope:** continuation of PRs #998–1000 under ADR 0038, at
`main@6dd67a491cf8d7a12b0c8540bc436a2c2d39c5b9`. No Level-4 change, new controller or
independent cognitive qualification.

## Exact-source reconciliation

[Run 46071489716](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/46071489716)
checked the canonical SHA above. The corrected receipt passed validation;
the next step failed at the assertion that three particular sessions
were returned in closure context. The two requested historical sessions
were available. The assertion depended on the third session being the
automatically selected latest final receipt. The source of
`scripts/summarize-receipts.py` includes the latest timestamp candidate(s)
plus explicitly requested historical final sessions.
The tracked `2026-11-28-verification-plan.session.yaml` declares an
updated_at of 2026-11-28T00:00:00Z, later than the integration-correction
receipt's 2026-11-27T21:35:19Z. This is a declared ordering, not evidence
of actual future execution or semantic precedence.

The existing receipt guidance already distinguishes chronology from
relevance and describes repeatable `--closure-context`. Select the
exact historical receipt rather than treating latest as an identity.
Execution-only commit [b5b728d](https://github.com/ThorStarlord/sensemaking-skills/commit/b5b728d4e4592dae07161e753f1c0998259ce8f0)
requests all three named sessions and prints the returned identities and
unavailable set. It preserves the original assertions, source pin,
knowledge blob checks, receipt validation, semantic assertions and
read-only runner permissions. No product reader, timestamp, final
receipt, knowledge pack or validator was changed.

[Run 46082001619](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/46082001619),
job 140782863093, passed at the exact pinned canonical source. It printed:

- LATEST_CANDIDATE: 2026-11-28-verification-plan.
- CLOSURE_CONTEXT_SESSIONS: latest candidate plus 2026-11-19-precommit-review-construction,
  2026-11-19-method-v0-source-path-provenance, and
  2026-11-27-cognitive-integration-actual-use-correction.
- CLOSURE_CONTEXT_UNAVAILABLE: [].
- CANONICAL_CLOSURE_CONTEXT=PASS and ACTUAL_COMMITTED_RETRIEVAL=PASS.
- 820 claims, 897 relations; digest
  `ef5897189853d9fcdafb0599f96c14401785d84e120ef4c761c23b50434f037a`.
- Both integrated concept and capability projections untruncated;
  original method application disposition apply, related records complete,
  present applicability NOT_ESTABLISHED.

[Actual output artifact 15236689522](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/46082001619/artifacts/15236689522)
has bounded retention. Product Validation and Release Candidate
Distribution also passed for the pinned canonical SHA (runs 46071466954
and 46071466923). Local unit/synthetic tests NOT_RUN.
The original failed run remains visible. The execution branch is not a
product workflow and is not merged.

## Decision influence and intellectual organization

The prior equivalent-execution lesson and actual-use report supported
preserving the original gate while substituting the authorized narrow
execution context. The failed assertion warranted a targeted correction
rather than a receipt reader rewrite or a new integration projection.
The prior lesson itself was not changed. The actual verification
procedure was refined to specify identities, not chronological
assumptions. This is an attributable local procedural correction,
not independent comparative cognitive improvement or a new reviewed
method-adaptation claim. The existing guidance already covers explicit
selection; do not create a duplicate method lesson.

Recovery also exposed the separate [#979 verification-plan episode](https://github.com/ThorStarlord/sensemaking-skills/pull/979)
and its [normal-use record](../../docs/normal-use/2026-11-28-verification-plan.md).
That record reports fresh-context implementation and real-symbol use,
not independently attributable later use of the integrated cognitive
capability. Its source-backed candidate composition is available to a
later agent doing real change-scoped development; retain its own
no-execution/no-coverage and comparative-benefit limits. It is not a
replacement for the current independent qualification responsibility.

## Alternatives and disposition

- Re-run the unmodified failed workflow: repeats an unsupported latest
  identity assumption. Rejected.
- Change the product reader or retimestamp the final receipt: current
  reader behaves as documented and exact selection works. Rejected.
- Extend the construction-bridge projection, create another learning
  mechanism, or reopen #880: actual-use history defers the former
  without a bound consumer; the latter has no established exposure
  activation condition. No new evidence defeats those decisions.
- Close the exact canonical verification, correct the current next-step
  pointer, and retain a source-grounded handoff: selected. Makes the
  existing capabilities and actual limitations easier to recover without
  inventing another subsystem.

The [previous actual-use record](2026-11-27-cognitive-integration-actual-use.md)
and #996 detached replay are complete; do not reconstruct them as
unimplemented work. Level-3 direction reaffirmed. A genuinely later
authorized agent should recover the integrated context before deciding,
compare substantive development alternatives, select and execute a
valuable real responsibility, and reconsider the intellectual method
from the actual outcome. Retain adaptation, application, rejection or
justified unchanged practice with the existing contracts as warranted.
Use the verified first-use handoff and the relevant read-only queries
when useful; no mandatory new trial or synthetic task. Independent
later-agent execution remains an external dependency of the current
episode; no new independent actor was dispatched. Ordinary valuable
construction may continue independently when it has a real warranted
consumer and authority. No independent improvement, longitudinal
compounding, cross-domain transfer, or release is established.
