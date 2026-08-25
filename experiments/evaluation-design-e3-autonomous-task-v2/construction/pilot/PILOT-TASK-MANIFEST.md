# Autonomous Task v2 — Pilot Task Manifest

All three pilot task families are ADMISSIBLE. Each is disposable
instrument-calibration content — none may ever be promoted into a
Tranche-1/Tranche-2 main-study candidate.

| pilot_id | family | task file | task_sha256 | oracle file | oracle_sha256 |
|---|---|---|---|---|---|
| T1-PILOT | T1 | `T1-PILOT-TASK.md` | `efb99507a4e49a24ac5b65dda262ca352cce58d8b23bf1da5bc32ea764decd70` | `T1-PILOT-ORACLE.md` | `f468c3f77dc902e728f9d677e1bb5bd639e9fca7ecef5326a9b9ead1bf8edbae` |
| T2-PILOT | T2 | `T2-PILOT-TASK.md` | `adaf43d75732a0ab1e14eb09f14c8478b04370fb8b91e0e23097d93319717e91` | `T2-PILOT-ORACLE.md` | `1376f5a1b4701d8acce987639d12e4339f35b1d14da91d2a34190460e45ff55c` |
| T3-PILOT | T3 | `T3-PILOT-TASK.md` | `fe2dc7ee028854283c56288adcd1eee9c23b4f1c71503e1d12da9e75a1a2b5e8` | `T3-PILOT-ORACLE.md` | `66e4498c51f8f9cc2586f6850c7504e70f2e5014f529882e5cb7b1007d2f75c9` |

Hash algorithm: SHA-256, hex digest, raw UTF-8 file bytes (per
`scripts/hash_utils.py:sha256_file`).

## Correction record (before this manifest's final freeze)

The originally-frozen `T3-PILOT-ORACLE.md` (oracle_sha256
`64fb9f48499173be61f727fe74bd65188e149761389be5543233696d9491bcef`,
manifest hash `3042f496997c55f331b7dba288c789c6c1a33a2c6b6174041f5326232ba62b2f`)
had two real defects, both found by actually re-running the full end-to-end
recovery sequence a second time while investigating an independent
reviewer's finding on a Tranche-1 T3 HIGH candidate (Task 10), rather than
by re-reading the original oracle's own prose:

1. Checks 1-2 parsed `run_log_*.md` content via regex to confirm the FAILED
   status existed and was later resolved. In fact `--resume` must reuse the
   *same* `--log-dir` to find prior state at all, and `write_run_log()`
   writes to that same fixed path every invocation — so the run log is
   **overwritten in place**, not preserved as a historical record. After a
   real resume, the file that originally showed `FAILED` shows only the
   final `COMPLETED`/`VALIDATED` state; the original oracle's Check 1
   assertions would never find what they were looking for, and Check 2
   would fail outright (`run_log_*.md` does not exist at all in the
   ledger's own numbered directory when `--log-dir` points elsewhere) —
   meaning the original oracle would have **rejected a genuinely correct
   recovery**, the exact failure mode this whole review process exists to
   catch.
2. `RUN_DIRS = sorted((CLONE / "artifacts").glob("*-orchestration-run"))`
   silently picked up **pre-existing, real, committed dogfood-example**
   `artifacts/NN-orchestration-run/` directories that already ship with the
   frozen-SHA repo (for unrelated workflows like `fast-local-diagnostic`,
   `full-local-sensemaking`) instead of the agent's own attempts.

Both were found and fixed by rewriting the oracle to rely exclusively on
`run-ledger.jsonl` content (verified reliably isolated per invocation,
independent of `--log-dir`), filtered to only the directories whose
ledger's `run_started.workflow_id` matches `t3-pilot-recovery-workflow`.
The corrected oracle was re-verified against a fresh end-to-end run of the
real recovery sequence (fresh scratch clone, frozen SHA, genuine FAILED
attempt, genuine fix, genuine `--resume`) before this manifest was
finalized. See `T3-PILOT-ORACLE.md`'s "Empirically observed run mechanics"
section for the full mechanism this correction is based on.

This correction happened entirely within the pre-freeze construction phase
— no salt, ranking, or dispatch seed existed yet, and no candidate pool
construction depended on the old hash. It is recorded here rather than
silently overwritten so the lock record's chronology can show it honestly.

## Manifest hash

Computed via `sha256_manifest()` over the canonical JSON serialization
(sorted by `candidate_id`, sorted keys, no extraneous whitespace — see
`scripts/hash_utils.py:canonical_manifest_json`) of the three records
`{candidate_id, family, task_sha256, oracle_sha256}`:

```
pilot_manifest_sha256 = e640de278b1218ad20df7a5a0e20e5a63f5d63aeccdc2ccedc703f566597a8b6
```

## Re-freeze (a7b957d) — manifest regenerated

This manifest was regenerated when the pilot instrument was re-frozen from
the old construction freeze `0ffb564b` to current `main`
`a7b957d738f5e1c42b6dd06824c3e6029d816bcd`. Because every pilot task's
`frozen SHA` reference and every oracle's re-freeze provenance note changed,
all six task/oracle hashes above and therefore `pilot_manifest_sha256`
changed from the old-freeze freeze record:

```
old pilot_manifest_sha256 = d6988ce3acd91bf361b6c63963760262620d089e59033a476238afabf9a7f317
new pilot_manifest_sha256 = e640de278b1218ad20df7a5a0e20e5a63f5d63aeccdc2ccedc703f566597a8b6
```

Task/oracle **content validity** at the new freeze is individually recorded in
`../RE-FREEZE-PROVENANCE.md` (T1 `VALID_UNCHANGED`, T2 `VALID_WITH_METADATA_UPDATE`,
T3 `VALID` after an empirical seven-link re-run at `a7b957d`). The bundles were
re-extracted from the updated task/oracle files and re-audited for leakage
(0 findings): the agent-visible bundles are **byte-identical** to the old-freeze
freeze, and the evaluator-only bundles regenerated to match the updated oracle
files. No task or oracle semantic content was altered by the re-freeze — only
the freeze-base references and provenance notes.

## Freeze

Frozen at: re-frozen at preparation time; see `../RE-FREEZE-PROVENANCE.md`.
No further edits to `T1/T2/T3-PILOT-TASK.md` or `-ORACLE.md` content after
this hash was computed. Any future change to pilot content requires
recomputing and re-recording this hash, and invalidates any prior claim
that referenced the value above.
