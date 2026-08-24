# Autonomous Task v2 — Re-Freeze Lock Record (PILOT_READY)

Status: SUPERSEDING LOCK RECORD for the pilot instrument. Produced by the
**E3 pilot preparation** responsibility (Phases 1-4). Supersedes the
historical construction freeze (`AUTONOMOUS-TASK-V2-LOCK-RECORD.md`, which
declared `PILOT LOCKED` against `0ffb564b` and is preserved unchanged as
provenance).

This record freezes the **pilot** instrument against the current product
freeze and concludes `PILOT_READY`. It does **not** dispatch any pilot cell,
does **not** run any main-study cell, and does not itself authorize the
main study.

## 1. Source identity (re-frozen)

```
repository: ThorStarlord/sensemaking-skills
old freeze: 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5
new freeze: a7b957d738f5e1c42b6dd06824c3e6029d816bcd  (current main)
```

Re-freeze rationale, comparability lost, validity gained, and the full
task/oracle re-validation record: **`RE-FREEZE-PROVENANCE.md`** (same
directory). Terminal task/oracle classifications:

- **T1 — `VALID_UNCHANGED`** (substrate drift holds; oracle base-independent)
- **T2 — `VALID_WITH_METADATA_UPDATE`** (`git diff` base re-pointed to `a7b957d`)
- **T3 — `VALID`** (seven-link recovery chain re-proven empirically at
  `a7b957d` during preparation)

## 2. Pilot instrument (re-frozen) hashes

All hashes are SHA-256 hex over raw UTF-8 bytes (LF, no BOM) per
`scripts/hash_utils.py`.

| file | task_sha256 | oracle_sha256 |
|---|---|---|
| T1 | `efb99507a4e49a24ac5b65dda262ca352cce58d8b23bf1da5bc32ea764decd70` | `f468c3f77dc902e728f9d677e1bb5bd639e9fca7ecef5326a9b9ead1bf8edbae` |
| T2 | `adaf43d75732a0ab1e14eb09f14c8478b04370fb8b91e0e23097d93319717e91` | `1376f5a1b4701d8acce987639d12e4339f35b1d14da91d2a34190460e45ff55c` |
| T3 | `fe2dc7ee028854283c56288adcd1eee9c23b4f1c71503e1d12da9e75a1a2b5e8` | `66e4498c51f8f9cc2586f6850c7504e70f2e5014f529882e5cb7b1007d2f75c9` |

```
pilot_manifest_sha256 = e640de278b1218ad20df7a5a0e20e5a63f5d63aeccdc2ccedc703f566597a8b6
(old freeze value = d6988ce3acd91bf361b6c63963760262620d089e59033a476238afabf9a7f317)
```

Regime prompts (unchanged by re-freeze; substrate-independent), hashes
verified against the design package and the historical lock record:

```
R0-ROBUST     sha256 = 5cab71b47464ddeb4e3537d26dd58540bd88249b6f44d319f46ca008c0585ea9
R1-LEAN       sha256 = 6a7147cdfb726fc6a2f216dd39fdf3335daad08447a98178b5ae7b2dd24f4861
R2-ESCALATION sha256 = ab94cc5480a8e4410bcc9df1f788f36f622625c277b8c917170caf8e568e3714
```

Bundle separation (regenerated from updated task/oracle files at the new
freeze; agent-visible content byte-identical to old freeze, evaluator-only
content reflects the updated oracle files):

```
agent-visible T1 sha256 = 33861682d93c8da480f5bfa3868a000933c77479039eb6284aad636b601b25fb
agent-visible T2 sha256 = 021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525
agent-visible T3 sha256 = 0dce1a825a4e7461c45177f9237892954ce799778a2c032c48a2c3bea90f0f86
evaluator-only T1 sha256 = f468c3f77dc902e728f9d677e1bb5bd639e9fca7ecef5326a9b9ead1bf8edbae
evaluator-only T2 sha256 = 1376f5a1b4701d8acce987639d12e4339f35b1d14da91d2a34190460e45ff55c
evaluator-only T3 sha256 = 66e4498c51f8f9cc2586f6850c7504e70f2e5014f529882e5cb7b1007d2f75c9
```

Leakage audit (re-run after regeneration): **0 findings** — no oracle
sentence (>8 words) appears verbatim in any agent-visible file.

## 3. Dispatch state (re-frozen pilot)

The pilot dispatch seed is **unchanged** (it is cryptographic random bytes,
content-independent, and only orders the 9 `(task, regime)` cells, whose
identities are intact across the re-freeze):

```
seed_pilot_dispatch = 0ab5cab61c1703f51f583d2ca527c9c3
```

Canonical 9-cell pilot order produced by the frozen seed interpretation
(Python `random.Random(int(seed,16))` + `shuffle`, per the pre-dispatch
addendum):

```
order  cell
1      T3 x R2
2      T3 x R1
3      T1 x R2
4      T3 x R0
5      T1 x R0
6      T2 x R2
7      T2 x R0
8      T2 x R1
9      T1 x R1
```

Each cell is a fresh standalone clone at `a7b957d` + fresh isolated agent
session; task-visible contract identical across regimes for a given task.

## 4. Preflight (re-run at the new freeze)

The canonical `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` is bash-only. This
preparation host (Windows) has no `bash` and the Docker daemon was not
running, so the `.sh` gate could not be invoked byte-for-byte. It was
**transcribed natively** (same checks, Python/git) against a fresh standalone
clone at `a7b957d`:

- clone-is-git-repo: PASS
- clone-head-matches-frozen-sha: PASS (`a7b957d...`)
- clone-working-tree-clean: PASS
- clone-is-standalone-not-worktree: PASS
- no-known-sibling-experiment-dirs: PASS
- clone-no-alternate-object-store: PASS
- clone-common-dir-is-self: PASS
- regime-file-present R0/R1/R2: PASS (hashes match §2)
- clone-remote-has-no-local-path: FAIL **on the scratch clone only** — its
  origin is a local `file://H:\...` path used to create the scratch clone for
  verification. A real dispatch clone must be created via a network-style
  remote (or have its origin stripped/redirected) **before** preflight; the
  gate correctly blocks a local-path remote. This is an execution-harness
  requirement, not an instrument defect.

**Execution-session requirement:** before dispatching any cell, run the
canonical `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` on a bash-capable harness
against the fresh clone at `a7b957d`, with a network-style (or removed)
origin, and require `PASS=17 FAIL=0 UNVERIFIABLE<=0` (excluding the ENV_LIMIT
disclosure line, which is always reported and is not a failure).

## 5. Main-study pools (unchanged historical)

The Tranche-1/Tranche-2 candidate pools, salts, rankings, samples, and
`seed_tranche1/`/`seed_tranche2`_dispatch` seeds are **carried unchanged at
their old-freeze frozen state**. They are historical construction content and
were **not** re-validated against `a7b957d` here.

Re-freezing the **main-study** pools against `a7b957d`, re-creating their
salts/rankings/seeds if any candidate content changes, and re-running their
preflight is the responsibility of the **separate main-study preparation
responsibility** that must follow a successful pilot. This lock record does
not assert the main-study pools are valid at the new freeze.

## 6. Terminal status

```
PREPARATION_READY     = PILOT_READY
pilot cells dispatched = 0
old lock status kept   = PILOT_LOCKED (historical, frozen at 0ffb564b)
```

The pilot instrument is frozen against `a7b957d` and ready for dispatch by a
fresh execution session. The execution session's responsibility is to consume
this immutable package and run the nine cells exactly as specified (see the
handoff in `RE-FREEZE-PROVENANCE.md` §7 and the owner's declared
chain: preparation -> PILOT_READY -> fresh execution session -> pilot ->
PILOT_VALID / PILOT_NEEDS_REPAIR / PRODUCT_FAILURE_EXPOSED / INCONCLUSIVE).
