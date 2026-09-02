# Semantic Control Map — Persistence Trial Protocol

**Status:** EXPERIMENTAL. Authorized by owner decision 2026-08-31 (see the
prototype lineage below). This protocol governs `docs/semantic-control-map.md`
for the trial period only.

## Lineage (research evidence, not merged)

| Step | Where | Result |
|---|---|---|
| Rich representation V0 | PR #244 `research/detailed-repository-architecture-prototype-v0` | 16 files / 2804 lines; most richness unnecessary |
| Compression V1 | PR #245 `research/semantic-control-core-v1` | 3-file / 299-line core; `THIN_CORE_PLUS_PROJECTIONS_PRESERVES_VALUE` |
| Independent reconstruction | fresh agent, zero V0/V1 exposure | `SUBSTANTIALLY_CONVERGENT`; also found V1 under-coverage |
| Persistence prototype | PR #246 `research/semantic-control-core-persistence-v0` | merged 38-row map; ~63% mechanically refreshable; no new infra to maintain |
| **This trial** | this PR | run the map in-place under real repository activity, then decide `CORE_PERSISTENCE_RATIFIED` |

`CORE_PERSISTENCE_RATIFIED = false`. `PRODUCT_ARCHITECTURE_RATIFIED = false`.
No prototype PR (#244/#245/#246) is merged. This PR is a fresh minimal candidate
from `main`.

## Map authority (binding for the trial)

- The map is a **non-authoritative decision-support index**. Its header states
  this; that header must not be weakened.
- **Absence of a row = NOT ASSESSED.** Never "no issue", never "safe".
- On any conflict with an authoritative source (ADR, contract, validator,
  `CONTEXT.md`, runtime behavior, measured evidence), the **authoritative source
  wins and the map row is stale** — fix or delete the row.
- Nothing may depend on the map: no runtime contract, no validator requirement,
  no workflow route, no Skill assumption. (See "Reversibility".)

## Row maintenance

Each row carries `Deriv` = `MECH` / `JUDG` / `MIX`.

- **`MECH` rows are refreshed, not re-decided.** Refresh procedure (all existing
  machinery; no new code beyond the advisory probe check this PR adds):
  1. `python scripts/probe-repo.py` — ADR lifecycle + relationships (now
     including `stale_accepted_adr_candidate`).
  2. `diff` the two `workflow-registry.yaml`; `diff` the two
     `artifact-contracts.yaml`.
  3. `grep -n 'pytest' .github/workflows/validation.yml`;
     `git branch -a --contains <feat/enforcement-gate tip>`.
  4. `pytest -q tests/test_path_drift.py tests/test_cli.py`
     — record whether any red is a **known** environment-only red (see SE2:
     Windows cp1252 `UnicodeDecodeError`) or new. (Selector corrected
     2026-09-02: `tests/test_cli.py::test_cli_version` no longer resolves; the
     test is `TestCLIBasic::test_cli_version`.)
  5. `cat distribution-drift.yaml`.
  6. the ~10 per-row symbol/import/doc-name greps named in the rows.
- **`JUDG` rows** and the **`INTERP:` half of `MIX` rows** are reviewed **only
  when a trigger below plausibly touches them**, by a competent agent/human.
  Update `judgment:` to `affirmed | contested | superseded` with the date and
  the trigger. A row two reviewers disagree on stays `contested` and keeps both
  readings (SA1 is already `contested`).
- **Do not silently resolve a `contested` row.**

### Staleness triggers (event-driven, not calendar)

| Trigger | Rows to refresh |
|---|---|
| `docs/adr/` file added or its `**Status**` edited | SL1-SL3, SL9, SA1, SA4, SA5, SA7, SA11 |
| `.github/workflows/validation.yml` changed | SE1, SE2, SA13 |
| `feat/enforcement-gate` (or successor) merges | SE1, SE2, SA13, SA9 |
| either `workflow-registry.yaml` / either `artifact-contracts.yaml` edited | SA2, SA8, SA9, SE3, SE4, SE6, SL5 |
| `src/sensemaking_skills/reasoning/` or `warrant_gate.py` imports change | SA6, SR1, SL6 |
| `distribution-drift.yaml` regenerated | SE10 |
| `test_path_drift.py` / `test_cli.py` change red/green state | SE2, SA10, SA12 |
| a new `experiments/` thread wires an import into `scripts/` or `src/` | SR1-SR4, SR-neg |
| `STATUS.md` / `CONTEXT.md` product-scope language changes | SA11, SA1 |
| retirement-plan doc-reconciliation items get done | SL7, SL8 |

If none has fired since the last refresh, the map is current — no work.

## Map size is not fixed

- `MAP_EXPANSION_DEFAULT = NO` — do not add rows during the trial except to
  record a genuinely new consequential boundary of the four fact-kinds.
- `MAP_ROW_RETIREMENT_ALLOWED = true` — mark a row `candidate-for-removal` in
  the log if, across the trial, it is repeatedly: cheap to recover from one
  obvious source · never consulted · too volatile · misleading · no longer
  consequential.
- The 38 rows are a starting point, not a number to defend. (The count differs
  slightly from PR #246's prototype map because MIX rows were restructured into
  explicit `FACT:` / `INTERP:` form per owner instruction; this is a
  presentation change, not new content.)

## What to observe (keep it small — 4 observations)

Record everything in `docs/semantic-control-map-trial-log.md`.

### A. Trigger frequency
For each repo change that touches a trigger: the trigger, and the affected
rows. Learn whether the "slow" map really stays slow.

### B. Maintenance effort (actual time, not estimates)
For each refresh/review: `MECH refresh` minutes · `JUDG review` minutes ·
`MIX review` minutes · which rows.

### C. Consultation value
When **ordinary** engineering work consults the map (never manufacture a task
to use it): the task · row(s) consulted · did it — locate authority faster /
reveal a conflict / seed a useful projection / prevent a likely mistake / add
no value.

### D. Incorrect consultation / over-read (the most important metric)
Every case where someone: treats absence as safety · treats a row as more
authoritative than its source · fails to invoke the projection procedure when
needed · follows stale map information · mistakes a `JUDG`/`INTERP` reading for
a demonstrated fact.

## Termination

```
minimum_elapsed_time = 4 weeks
maximum_elapsed_time  = 8 weeks
```

Closure additionally requires **meaningful real activity** — enough that
maintenance and consultation behaviour were actually exercised:
- several `MECH` refresh events;
- at least a few real map consultations;
- at least one `JUDG`/`MIX`-relevant trigger.

At 8 weeks, close regardless. If activity was too low, classify the evidence
`INSUFFICIENT_ACTIVITY` rather than pretending it decided anything.

At closure, write a short trial report and set one of:
```
CORE_PERSISTENCE_RATIFIED = true
  | false
  | INSUFFICIENT_ACTIVITY
```

## Reversibility

This trial is fully reversible. If it fails or is inconclusive:
1. delete `docs/semantic-control-map.md`, `docs/semantic-control-map-trial.md`,
   `docs/semantic-control-map-trial-log.md`;
2. revert the `scripts/probe_relationships.py` `stale_accepted_adr_candidate`
   addition and `tests/test_stale_accepted_adr_probe.py` **unless** the probe
   check has by then shown independent value (e.g. it caught a real stale ADR
   status that got fixed);
3. keep the final trial report as durable research evidence.

Attestation for this PR:
- no runtime contract, validator, workflow, or Skill references or requires the
  map;
- the new probe finding is `requires_semantic_review: True` and is **not** in
  `scripts/gate_relationship_findings.py::BLOCKING_FINDING_TYPES` — it can never
  fail CI;
- no product / runtime / contract / PHB / ADR / `CONTEXT.md` behavior changed.
