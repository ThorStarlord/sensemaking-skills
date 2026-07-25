# ADR 0016: Evidence Policy for Repository Findings

**Status**: PROPOSED — draft for owner review, not yet accepted
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
Product-direction decision; confirm or amend before treating as Accepted.
