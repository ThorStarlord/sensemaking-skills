# V1 FREEZE MANIFEST — SEMANTIC CONTROL CORE V1

```
SEMANTIC_CONTROL_CORE_V1_FROZEN = true
```

| Field | Value |
|---|---|
| Repository | `ThorStarlord/sensemaking-skills` |
| Represented `main` SHA | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` |
| Authorization canonical SHA | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` (no movement) |
| V1 branch | `research/semantic-control-core-v1` (from canonical `main`; not from PR #244) |
| V1 root | `experiments/semantic-control-core-v1/` |
| V0 reference head (read-only) | `f7b0d344640721249aaa14c5bbf8061523bd26b7` |
| Frozen at (UTC) | 2026-08-31T08:36:23Z |
| Hash algorithm | SHA-256 |

## Frozen V1 artifacts

| SHA-256 | Path | Lines |
|---|---|---|
| `a3da3be1bf2091bdb2cc6c212f87e7152d49f6d64e107135736e7053dcba82b6` | `00-SCOPE.md` | 75 |
| `6aad41a0117493da2ef54a2878e79c66f3db55da496302054570cbbdf943e74c` | `SEMANTIC-CONTROL-CORE.md` | 102 |
| `54e5a90dcfa7e967ee6ca329c733a4c635ffdc03f03ede8f4519ad74ddd06853` | `ON-DEMAND-PROJECTION-RECIPE.md` | 122 |

Frozen total: **299 lines, 3 files.**

## Produced AFTER freeze (not frozen; evaluation outputs)

- `COMPRESSION-EVALUATION.md` — V0 regression replay (10 cases) + 2 holdouts +
  1 current-state projection drill + staleness classification
- `SYNTHESIS.md` — 12 synthesis answers + `V1_ARCHITECTURE_DISPOSITION`
- `V1-FREEZE-MANIFEST.md` — this file

## Freeze rule (authorization Section 18)

After this point the frozen V1 core + recipe are **not modified** because
evaluation exposes a weakness. Weaknesses are recorded in
`COMPRESSION-EVALUATION.md` / `SYNTHESIS.md`. A later V2 may change the core.

## Machine-readability check

The three frozen artifacts are Markdown (tables + prose). No YAML in the frozen
set — deliberate, per authorization §32 and V0 finding E-9 (hand-authored
nested YAML was error-prone). `grep -nE '^\s*[A-Za-z0-9_-]+:\{' *.md` → no hits.

## Integrity re-check

```bash
cd experiments/semantic-control-core-v1
sha256sum -c <(sed -n '/^| `[0-9a-f]\{64\}`/p' V1-FREEZE-MANIFEST.md \
  | sed -E 's/^\| `([0-9a-f]{64})` \| `([^`]+)` \| [0-9]+ \|$/\1  \2/')
```
