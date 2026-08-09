# DRAFT ADR AMENDMENT SKETCH — Consequential boundary without forced weakness

**Status: DRAFT, prototype material only. Not submitted, not numbered, not
part of the `docs/adr/` sequence. Not an amendment until the owner reviews
and files it as one.**

**Would amend:** ADR 0015 (Deterministic versus Model-Variable Artifact
Fields) — specifically the ratified D2/D3/D4 classification of
`weakness_type` as required-but-non-blocking, controlled-vocabulary.

## Problem this sketch responds to

P4's diagnosis (two parallel implementations of the same product, no
canonical surface declared) had to be filed under `Contract Mismatch`
because [repo-analysis-template.md](../../skills/repo-sensemaker/references/repo-analysis-template.md)
requires a `**Weakness type:**` line whenever Section 6 is filled in.
Nothing about P4's finding was actually a *demonstrated defect* — it was an
unresolved strategic choice. Forcing a weakness label onto it distorts the
brief's truthfulness.

## What this sketch proposes (for owner review, not enacted)

Do not add a new enum value (e.g. `weakness_type: none`) — per the source
review's own reasoning against Option D3-C ("relocates brittleness rather
than removing it"), adding a sentinel *inside* a taxonomy of defect
*mechanisms* contaminates that taxonomy with a non-mechanism value.

Instead: make `weakness_type`'s existing non-blocking absence
(already ratified, D2) mean something explicit when paired with a new
`is_demonstrated_weakness: false` flag (prototyped in
`analysis_vnext.consequential_boundary.is_demonstrated_weakness` — see
[the vNext template](../../skills/repository-diagnostician/references/brief-vnext-template.md)) —
i.e., don't change what `weakness_type` accepts; change what its absence is
allowed to *mean* when a companion field says the absence is deliberate.

## Evidence for this sketch

- P4's brief, filed under `Contract Mismatch` for a non-defect finding
  (owner-reviewed, recorded in `experiments/product-interaction-p4-v1/learning-v1.md`).
- ADR 0015's own D3 addendum already establishes precedent for adding a
  narrow, well-justified field-level fix in response to one concrete
  failure (`weakness_type` itself, in response to PR #78) — this sketch
  proposes the same kind of narrow fix, not a taxonomy redesign.

## What this sketch does NOT propose

- Does not change `validate-brief.py`'s current behavior on `main` or in
  PR #163. This prototype's `analysis_vnext` block is read by nothing
  canonical.
- Does not claim ADR 0015 is wrong — D2/D3/D4 remain correct for the
  "demonstrated weakness" case this sketch doesn't touch.
- Does not introduce `weakness_type: none` or any other new enum member.

## Reversibility

High. This is a documentation/schema-addendum sketch with a working
prototype demonstration behind it, not a code change to any canonical
validator.

## Owner action, if pursued

File as a real ADR 0015 addendum draft, following the same
owner-decision-package process that ratified D2/D3/D4, before any canonical
validator changes.
