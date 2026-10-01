# Orphaned documents (archived 2026-09-30)

Stage 1 of the owner-ratified "simplify hard" program
(`artifacts/owner_decision_capsule.md`, Option B, Stage 1 only).

These documents were moved here because **no tracked file referenced them** — not
a test, manifest, CI config, skill, evidence record, or other document. Zero
inbound references was verified by scanning all tracked text files
(`git ls-files`) for each file's basename before moving. Moving them breaks no
citation.

They are **archived, not deleted**: every byte is preserved here, and the whole
move is a single reversible commit (`git mv`, no content changes). Nothing was
edited.

## How to restore one

```bash
git mv docs/archive/orphaned-2026-09-30/<name> docs/<name>
```

## Scope and method

- Candidates came from a read-only usage survey of `docs/` (495 markdown files):
  40 zero-inbound docs, excluding the current-activity families
  `docs/normal-use/**` and `docs/triage/**`.
- Historical/evidence docs that ARE cited by immutable experiment manifests or
  qualification evidence were **not** moved (that is why, e.g., most of
  `docs/superpowers/plans/*` stays in place — only the unreferenced ones moved).
- Off-limits and untouched: artifact contracts, validators with real consumers,
  anything pinned by `release-v1.0.yaml` or the qualification evidence, and the
  `docs/PHASE-*` / `STAGE-*` / `IMPLEMENTATION-*` set previously decided to stay.

## Contents by family

- `campaign-*.md` — superseded campaign notes/reports.
- `superpowers/plans/*.md` — unreferenced dated plans.
- `candidate/*`, `stress-test-2026-08-10/*` — dated candidate/stress-test records.
- `semantic-architecture/phase-9-handoff.md`, `phase-10/episode-*.md` — phase records.
- `research/path-*.md`, `research/exp0003-*.md` — unreferenced research notes.
- `experiments/schemas/two-lane-v1/phase-*-implementation.md` — unreferenced design records.
- `PHASE-1-GOLDEN-PATH.md`, `STRATEGIC-*.md`, `strategic-state-*.md`,
  `change-impact-sensemaking-v1.md`, `cross-repository-execution-projection-v1.md`,
  `github-provenance-publication-v1.md`, `adaptive-guidance-product-reconciliation-v0.md`,
  `practical-agent-architecture-v0-handoff.md`, `semantic-usefulness-evaluation-v1.0.md`,
  `product-management/dogfood/preflights/.../PRECHECK.md` — unreferenced records.

Restoring any file is one command; if a doc turns out to be wanted, restore it
and link it from `docs/README.md` so it is no longer orphaned.
