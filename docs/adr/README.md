# Architecture Decision Records — Status Lifecycle

This directory holds ADRs for this repository. The ADR probe
(`scripts/probe_relationships.py`, part of the Probe Engine) reads the
`**Status**` line of every `docs/adr/NNN-*.md` and emits findings for
unrecognized or missing statuses and for status-claim mismatches; the status
vocabulary below is the canonical convention it validates against. This file
exists to define the convention so authors and reviewers use the same
vocabulary.

## Statuses

- **PROPOSED**: a candidate decision awaiting owner acceptance and/or
  evidence. Not yet operative.
- **PROVISIONAL**: implemented and evidence-supported, but awaiting a stated
  promotion condition (e.g. owner ratification or external validation)
  before it becomes the operative decision. Not yet Accepted — still write
  as pending, not settled.
- **ACCEPTED**: the operative repository decision. Only an Accepted ADR
  should use `Resolves: Issue #NN` in its header; Proposed and Provisional
  ADRs use `Proposes resolution for:` / `Provisionally addresses:` instead
  (see existing ADRs for examples).
- **SUPERSEDED** / **REJECTED**: reserved for ADRs later replaced or turned
  down, if that need arises. Not otherwise defined further here.

A Provisional ADR's "Status rationale" section should state an explicit,
checkable promotion condition — not just "more evidence needed."
