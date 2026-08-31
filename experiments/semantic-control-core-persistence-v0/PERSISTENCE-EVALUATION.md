# PERSISTENCE EVALUATION — SEMANTIC CONTROL CORE PERSISTENCE PROTOTYPE v0

## 1. Does the merged map reconcile?

| Check | Result |
|---|---|
| Row count | 38 (A:13, E:10, L:10, R:5) — vs V1's 22 + agent B's 32. Merge deduped ~16 shared boundaries, kept V1's 1 unique (SE8), added ~12 from B, folded ~4 B rows (C6→SL7/SL8, C2→SE7/SL, A5→SA2, D2 detail→SR2). |
| Grade distribution | 36 rows carry `D` as primary; 2 cells explicitly `I` (SA1, SA6 impl/policy). 0 `H`. |
| Change-rate | SLOW 30 · MEDIUM 7 · FAST 1 (SE10 vendored drift). Consistent with V1's corrected staleness finding (compression preferentially keeps slow facts). |
| Derivation | MECH ~24 (63%) · JUDG ~7 (18%) · MIX ~7 (18%). |
| Arithmetic | 13+10+10+5 = 38 ✓ ; 24+7+7 = 38 ✓ (V1's accounting-erratum lesson applied — counts reconcile). |
| One row per concern | held; SA2 carries brief-contract concentration **and** structure authority as one concern with two evidence pointers, not two rows. |

**Reconciles.** The merge did not reintroduce V0-style enumeration: still no
call graphs, no file inventories, no producer/consumer tables. Every added row
is one of the four fact-kinds.

## 2. What the derived/judgment split tells us about persistence

- **~63% of the map is `MECH`** — refreshable by `probe-repo.py` +
  `probe_relationships.py` + two `diff`s + two `pytest` selections +
  `distribution-drift.yaml` + ~10 greps. All machinery **already exists**; no
  new code is required to keep those rows current, only a short runbook
  (`MAINTENANCE.md` §1).
- **The entire Lifecycle section (10 rows) is `MECH`** — ADR statuses, stale
  file headers, retired-runner shims, and the ~30 historical PHASE files are all
  grep/diff facts. This is the cheapest and highest-value part of the map to
  persist: it is exactly the "physical presence ≠ authority" information a
  dependency graph never surfaces, and it is nearly free to keep correct.
- **~18% is `JUDG`** — ~7 rows of architectural interpretation
  (SA1, SA4, SE8, SE9, SR3, plus the judgment halves of SA6/SA8). This is the
  real maintenance liability. It is **under** the `MAINTENANCE.md` §4.2
  safety threshold (25%), but only just, and the merge *added* judgment load
  (B's boundaries brought SR3; V1 already had SA1/SA4/SE8/SE9).
- **The judgment rows are also the contested ones** — V1 vs agent B disagreed
  on SA1 (control-loop policy-vs-impl) and on SA8's decidedness. That is the
  `CORE_TOO_INTERPRETIVE` risk localized: it lives in ~7 named rows, not spread
  through the whole map. Persistence can quarantine it (mark `contested`, keep
  both readings) rather than being blocked by it.

## 3. What makes persistence unsafe (from `MAINTENANCE.md` §4, assessed now)

| Condition | Status at `ba8968c` |
|---|---|
| `MECH` refresh cannot run cheaply | **watch** — `test_path_drift.py` is RED on `main` (SE2) and `test_cli.py::test_cli_version` is a known-wrong assertion (SA12); the refresh *works* but step 4 currently returns known reds. Not a blocker, but the runbook must distinguish "expected red" from "new red". |
| `JUDG` > 25% of map | **no** — currently ~18%, but with little headroom. |
| `JUDG` rows churn | **unknown** — no time series. SA1 already has two divergent readings at a single point in time. |
| Map consulted instead of the recipe (silent-omission over-read) | **unmitigated structurally** — same finding as `SYNTHESIS.md` Q5. `MAINTENANCE.md` §4.4 requires a structural header treatment ("absence of a row = not yet assessed"); this prototype specifies it but a persisted artifact must actually carry and surface it. |
| No owner ratification of persistence | **correct** — none exists; this stays an `experiments/` prototype. |

**Two of five conditions are "watch/unknown", none is a hard "unsafe".**

## 4. Maintenance-cost estimate

- `MECH` refresh: ~10–20 min per triggering change, a few times per active
  month (`MAINTENANCE.md` §5). Dominated by `probe-repo.py` runtime.
- `JUDG` + `MIX` overlay: ~14 rows; reviewed only on plausible triggers;
  ~5–15 min per affected row.
- The honest bottom line: **the mechanical 63% is cheap enough to persist
  today. The judgment 37% (JUDG+MIX) is ~14 rows whose sustained review burden
  is the open question** — and that question is answerable only by real use
  over time, not by another prototype.

## 5. Disposition

```
PERSISTENCE_PROTOTYPE_RESULT          = COMPLETE
MERGED_MAP_RECONCILES                 = true
MECHANICALLY_DERIVABLE_FRACTION       = ~0.63  (entire lifecycle section)
IRREDUCIBLE_JUDGMENT_FRACTION         = ~0.18  (7 named rows, quarantinable)
MIXED_FRACTION                        = ~0.18
NEW_INFRASTRUCTURE_REQUIRED_TO_MAINTAIN = false  (reuses probe engine + diff + pytest + greps)
PERSISTENCE_SAFETY                    = NO_HARD_BLOCKER  (2 of 5 conditions "watch/unknown")

CORE_PERSISTENCE_RATIFIED            = false   (owner decision; not taken here)
CANONICAL_PLACEMENT_MADE             = false   (map stays under experiments/)
PRODUCT_ARCHITECTURE_RATIFIED        = false
```

### Recommended next step (for owner)

A **bounded, time-boxed persistence trial**, not another prototype:

1. Place the merged map at `docs/semantic-control-map.md` **with** the
   structural "absence = not yet assessed" header treatment (`MAINTENANCE.md`
   §4.4).
2. Wire the `MECH` refresh runbook into the existing Probe Engine output (no new
   system — extend `probe_relationships.py`'s findings with the stale-Accepted-ADR
   check from `MAINTENANCE.md` §1).
3. Over ~4–8 weeks of ordinary repo activity, record: how often triggers fire,
   actual `MECH` refresh time, how often `JUDG` rows are touched and whether any
   flips, and whether anyone reads the map or over-reads its omissions.
4. Then decide `CORE_PERSISTENCE_RATIFIED`.

The distinctive remaining uncertainty is now narrow and concrete:
**is ~14 rows of periodically-reviewed architectural judgment a burden this
project will actually sustain, and does the map get consulted correctly?**
Only elapsed real use answers it.

### What NOT to do

No database / graph store / daemon / watcher / invalidation / query engine.
No new Skill or workflow. Do not expand the map past the four fact-kinds. Do not
merge V0/V1/this prototype into product docs before the persistence trial
reports. Do not run more repositories or another synthetic suite.
