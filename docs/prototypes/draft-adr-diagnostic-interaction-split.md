# DRAFT ADR SKETCH — Separate owner-interaction from repository diagnosis

**Status: DRAFT, prototype material only. Not submitted, not numbered, not
part of the `docs/adr/` sequence. No existing ADR governs `repo-sensemaker`'s
internal packaging, so this would be a new draft ADR, not an amendment.**

## Problem this sketch responds to

On `main`, `repo-sensemaker`'s `SKILL.md` observably mixes two
responsibilities in one file: Stage 1 intent-extraction/conflict-detection
(interaction-adjacent) and evidence-gathering/weakest-boundary
classification (diagnosis). This is directly readable in the file, not an
inference.

## What this sketch proposes (Option A, one of at least three candidates)

```text
repo-sensemaker           = owner-facing interaction layer
repository-diagnostician  = non-interactive diagnostic core
```

Implemented as a working prototype on this branch:
[`skills/repository-diagnostician/`](../../skills/repository-diagnostician/SKILL.md)
(new, diagnosis-only) and a restructured
[`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md)
(interaction-only on this branch; unchanged, diagnostic-only on `main`).

## Alternatives this sketch does not rule out

- **Option B**: a generic `sensemaking-interaction` skill above
  `repo-sensemaker`, reusable if other sensemaking capabilities
  (`product-sensemaker`, `incident-sensemaker`, ...) eventually want the
  same investigate-first/clarify-if-needed shape.
- **Option C**: one `repo-sensemaker` Skill, internally decomposed (compact
  control plane + `references/` subprocedures) — the pattern this skill
  already uses for `weakness-types.md`/`evidence-rules.md`, extended rather
  than split into a second Skill package.

This sketch does not claim Option A is correct — only that it is now
concrete enough to evaluate against B and C, per the stated purpose of this
prototype branch.

## Evidence for and against

**For a split existing somewhere:** the responsibility mixture is directly
observable in `main`'s `SKILL.md`, independent of any experiment's sample
size.

**Against concluding Option A specifically is correct:** whether the
runtime ever needs to invoke diagnosis without interaction (or vice versa)
is the concrete test that would decide between A/B/C, and this prototype
does not exercise the real `workflow-runtime.py` orchestration path — the
skills here are invoked directly by name, not through
`skill-registry.yaml`/`workflow-registry.yaml`. That question remains open.

## What this sketch does NOT propose

- Does not modify `main`'s `repo-sensemaker/SKILL.md`.
- Does not register `repository-diagnostician` in the canonical
  `skill-registry.yaml` or any `workflow-registry.yaml` workflow.
- Does not claim this packaging is validated by real orchestrated use —
  only that it now exists to look at.

## Reversibility

High — deleting `skills/repository-diagnostician/` and restoring `main`'s
`repo-sensemaker/SKILL.md` fully reverses this, since nothing canonical
references the new skill.

## Owner action, if pursued

Decide A vs. B vs. C based on whether a real next use case needs
diagnosis and interaction independently invocable — per the assumption
ledger's A-01 entry — then file as a real, numbered ADR.
