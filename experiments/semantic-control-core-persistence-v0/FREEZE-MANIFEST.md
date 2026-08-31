# FREEZE MANIFEST — SEMANTIC CONTROL CORE PERSISTENCE PROTOTYPE v0

```
SEMANTIC_CONTROL_CORE_PERSISTENCE_V0_FROZEN = true
```

| Field | Value |
|---|---|
| Repository | `ThorStarlord/sensemaking-skills` |
| Represented `main` SHA | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` (unchanged since V0/V1) |
| Branch | `research/semantic-control-core-persistence-v0` (from canonical `main`; not from PR #244 / #245) |
| Root | `experiments/semantic-control-core-persistence-v0/` |
| V1 reference | branch `research/semantic-control-core-v1`, draft PR #245 |
| Independent-reconstruction reference | agent B, 32 rows, zero V0/V1 exposure (`H:/GithubRepositories/smk-indep-recon-out/independent-semantic-control-representation.md`) |
| Frozen at (UTC) | 2026-08-31T17:15:59Z |
| Hash | SHA-256 |

## Frozen artifacts

| SHA-256 | Path | Lines |
|---|---|---|
| `854fb88ed733dd60235fe5fae8a0ee844e18f91bf1ae63cbbdc4b8e17f9e50b8` | `00-SCOPE.md` | 80 |
| `4ba271ffb142c44be0cf287436017053c693645f70cac075905b047780f74b87` | `SEMANTIC-CONTROL-MAP.md` | 91 |
| `d768927f70a44c3ea078bfc6b86307afdcad6397d21fe3face1cf21b8f0cbb3e` | `MAINTENANCE.md` | 129 |
| `28d67fac29dd7d1edeefc81dd118ad462dd4d0b4dd1958b0b2539b708a25bd37` | `PERSISTENCE-EVALUATION.md` | 105 |

Frozen total: **405 lines, 4 files.** (V0 = 2804 / V1 core = 299 / this = 405
including the merged 38-row map + full maintenance runbook + evaluation.)

## Freeze rule

After this point these 4 files are not modified because later review finds a
weakness. Weaknesses go to a separate note or a `v1`. `FREEZE-MANIFEST.md`
itself may be appended to for errata (as V1's was).

## Boundary attestation

- All Markdown (tables + prose). No YAML in the frozen set;
  `grep -nE '^\s*[A-Za-z0-9_-]+:\{' *.md` → no hits.
- No file outside `experiments/semantic-control-core-persistence-v0/` changed on
  this branch.
- Frozen V0 (`experiments/detailed-repository-architecture-v0/`) and frozen V1
  core files not present on this branch and not touched.
- No product / runtime / validator / probe / contract / PHB / ADR / test change.
- No `docs/` file created or edited.

## Integrity re-check

```bash
cd experiments/semantic-control-core-persistence-v0
sha256sum -c <(sed -n '/^| `[0-9a-f]\{64\}`/p' FREEZE-MANIFEST.md \
  | sed -E 's/^\| `([0-9a-f]{64})` \| `([^`]+)` \| [0-9]+ \|$/\1  \2/')
```
