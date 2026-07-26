# ADR 0016: Evidence Policy for Repository Findings

**Status**: PROVISIONAL — the citation-format and evidence-attachment
mechanics are already implemented and exercised live; the "which claims
require evidence" threshold is still a policy choice pending owner sign-off
**Date**: 2026-07-25
**Resolves**: Issue #31

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
The mechanics below are already implemented and evidence-backed; owner
should confirm the "which claims require evidence" threshold before
promoting to Accepted.

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

**Provisional**: the shape (`evidence_excerpts` YAML block, dual citation
format, placement) is implemented and was exercised against live model
output in PR #59 and #65, going beyond a bare proposal. Held short of
Accepted because the enforcement boundary (which claims strictly require
evidence) has not been tested by a validator actually rejecting a
non-compliant claim, and owner sign-off on the threshold itself is
outstanding.
