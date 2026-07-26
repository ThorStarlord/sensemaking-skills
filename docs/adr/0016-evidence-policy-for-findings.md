# ADR 0016: Evidence Policy for Repository Findings

**Status**: ACCEPTED (with a ratified addendum) — 2026-07-26 by explicit
owner decision (D5, D9) recorded in
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`
**Date**: 2026-07-25 (revised 2026-07-26)
**Provisionally addresses**: Issue #31

**2026-07-26 addendum, owner-ratified**: the auteur campaign (PR #73, #75,
#77, #78) directly exercised this ADR's mechanics live. The owner explicitly
approved:
- **D5**: the independent substantive evidence audit is **mandatory only for
  absence/unreachability/dead-code/safety/ghost-feature and other high-risk
  claims**, not for every brief — this resolves the "which claims require
  evidence" threshold this ADR's promotion condition named explicitly.
- **D9**: PR #78's `UNKNOWN_WEAKNESS_TYPE` failure is legitimate under the
  current (brittle) contract, not a model-reasoning failure, and not a
  successful external validation either. The trace evidence (completed
  Grep/Read contradiction searches against real `auteur` symbols) confirms
  PR #75's contradiction-search discipline held live, independent of the
  unrelated taxonomy failure that stopped the run.

The owner's approval also separately ratified **D6** (human review depth:
approval required for every final brief during the next phase) — recorded
here because D6 has no other existing ADR home (see the product-contract
review's Part 6 issue mapping), though it is not itself part of this ADR's
promotion condition.

The product-contract review (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md`,
Part 4) additionally identifies one new, currently-unimplemented deterministic
check worth considering — verifying a cited `quote` is actually a substring
of the target file at/near the cited line range — as a candidate direction,
**not itself ratified** and not implemented by this revision.

---

## Context

`repository_sensemaking_brief.md` and other findings artifacts need a
consistent, validator-enforceable evidence policy. Prior experience in this
repo (CLAUDE.md verification-discipline notes) already shows that an
over-strict evidence format (`Lx`-only citations) rejected valid output —
so this policy must be validated against what a real validator actually
consumes, not designed in the abstract.

## Decision

**Which claims require evidence**: Every claim that drives a routing
decision (fog-type classification, recommended workflow, weakest-boundary
identification) requires at least one evidence excerpt. Incidental
observations in prose do not.

**Shape**: A structured YAML evidence-excerpt list, already implemented in
`repository_sensemaking_brief.md`'s "Evidence excerpts" section:
```yaml
evidence_excerpts:
  - file: "path/relative/to/repo-root"
    lines: "10-20"          # optional: bare line range or bare number
    quote: "..."
    supports_claim: "..."
```
This is both human-readable (renders under a Markdown heading) and
machine-parseable (the YAML block).

**Path representation**: relative to repo root, forward slashes, matching
every existing validator's convention (`_resolve_run_log_path` etc.) — no
absolute paths, since sessions may run from different machines.

**Placement**: a dedicated "Evidence" / "Evidence excerpts" section, not
inline per-finding — matches the current brief structure and keeps the
validator's job (checking the section exists and has ≥1 entry) simple.

**Citation format**: accept both bare line numbers/ranges and `Lx`-style
citations (already relaxed per the CLAUDE.md-documented incident) — do not
regress to a single strict format.

## Consequences
- `validate-brief.py` should require the `evidence_excerpts` block for any
  claim that sets `primary_fog_type` or `recommended_workflow_id`.
- Feeds ADR 0015 (deterministic fields): `evidence_excerpts` is a
  deterministic field; the `quote`/narrative text inside it is not.

## Owner sign-off required
~~The mechanics below are already implemented and evidence-backed; owner
should confirm the "which claims require evidence" threshold before
promoting to Accepted.~~

**Given, 2026-07-26**: the owner ratified the threshold as D5 in
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`. Promoted to Accepted.

---

## Hypothesis

Claims that drive routing decisions require an attached evidence excerpt;
incidental prose does not; citation format accepts both bare line
numbers/ranges and `Lx`-style references.

## Supporting evidence

- PR #59 ("live Step-1 semantic validity proven", issue #58) specifically
  exercised the evidence-authority-hierarchy and evidence-citation-grammar
  path in a live `repo-sensemaker` run, and the resulting
  `repository_sensemaking_brief.md` passed `validate-brief.py` with real
  `evidence_excerpts` content — direct, repeated evidence the mechanics
  work against live model output, not just fixtures.
- PR #65's live Step-2 evidence cites the brief's evidence excerpts
  (weakest-boundary section) as the basis for `proposed_direction.md`'s
  content, showing the evidence chain is actually consumed downstream, not
  just produced and ignored.
- CLAUDE.md's verification-discipline section documents the `Lx`-only
  format having previously and concretely rejected valid bare-number
  citations — this is a real, already-corrected incident, not a
  hypothetical risk.

## Missing evidence

- No merged evidence demonstrates a validator actually *rejecting* a claim
  for missing evidence on a routing-relevant field (i.e., the negative case
  of this policy is untested in the live campaign) — PR #65's negative run
  tested a missing *input file*, not a missing evidence excerpt on a
  present claim.
- The specific threshold ("routing-relevant claims only, not incidental
  observations") is a judgment call about how much evidence is "enough,"
  which is a policy decision the evidence can support but not fully settle.

## Experiment or review trigger

Revisit if a future validator run shows a routing claim shipping without
evidence and passing validation anyway (a gap in enforcement), or if the
evidence-excerpts schema needs to change to support a new artifact type.

## Status rationale

**2026-07-26 update — promoted to Accepted.** Owner sign-off on the
enforcement threshold (D5) is now given, which was this ADR's stated
promotion condition. Preserved for record, the prior rationale:

**Provisional**: the shape (`evidence_excerpts` YAML block, dual citation
format, placement) is implemented and was exercised against live model
output in PR #59 and #65, going beyond a bare proposal. Held short of
Accepted because the enforcement boundary (which claims strictly require
evidence) had not been tested by a validator actually rejecting a
non-compliant claim, and owner sign-off on the threshold itself was
outstanding.
