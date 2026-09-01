# Semantic Control Map — Trial Log

Fill during the trial. Protocol: `docs/semantic-control-map-trial.md`.
Map: `docs/semantic-control-map.md`.

```
trial_start_commit   = df46871c140cff64755cb3865df26354913d09c1 (merge of PR #247, trial/semantic-control-map)
trial_start_date     = 2026-08-31
minimum_close_date   = 2026-09-28 (trial_start_date + 4 weeks)
maximum_close_date   = 2026-10-26 (trial_start_date + 8 weeks)
status               = OPEN
```

---

## A. Trigger events

| date | commit | trigger | affected rows | refreshed? |
|---|---|---|---|---|
| 2026-08-31 | 4a4fdb2 (PR #248 merge; head 2470ab2) | `STATUS.md` / `CONTEXT.md` product-scope language changes — `CONTEXT.md` "Lifecycle positioning" added; explicitly reaffirms ADR 0014 scope ("does not broaden product scope") | SA1, SA11 | yes — MIX review 2026-08-31 (see B) |

## B. Maintenance effort (actual minutes)

| date | activity (MECH refresh / JUDG review / MIX review) | rows | minutes | notes |
|---|---|---|---|---|
| 2026-08-31 | MIX review (trigger: PR #248 `CONTEXT.md` product-scope language) | SA1 | <1 | interpretation unchanged: "Lifecycle positioning" speaks to responsibility transitions/routing, not ADR 0013 loop ownership or the runtime's whole-loop-style sequencing. judgment stays `contested` (both readings kept). Measured wall-clock; reviewer had already read the trigger diff + row in-session |
| 2026-08-31 | MIX review (trigger: PR #248 `CONTEXT.md` product-scope language) | SA11 | <1 | interpretation unchanged + corroborated: the addition explicitly reaffirms ADR 0014 scope and does not claim broader readiness; STATUS.md vs PHASE-4-5 record conflict unchanged. judgment stays `affirmed`. Measured wall-clock; reviewer had already read the trigger diff + row in-session |

## C. Consultation events (ordinary work only — never a manufactured task)

| date | task | row(s) consulted | outcome (faster authority / revealed conflict / seeded projection / prevented mistake / no value) |
|---|---|---|---|
| | | | |

## D. Over-read / misuse events

| date | who/what | misuse type (absence-as-safety / row-over-source / skipped-projection / followed-stale / interp-as-fact) | consequence | notes |
|---|---|---|---|---|
| | | | | |

## Row lifecycle notes (retirement / expansion candidates)

| date | row | proposal (candidate-for-removal / new-row) | reason |
|---|---|---|---|
| | | | |

## `stale_accepted_adr_candidate` probe — independent value tracking

At this snapshot the check flags: ADR 0013 → ADR 0012 ("now superceded by
skill-led model"); ADR 0025 → ADR 0005 ("Accepted, historical"). Record whether
any flagged ADR's `**Status**` line is subsequently corrected (evidence the
check has value independent of the map).

| date | flagged pair | action taken |
|---|---|---|
| | | |

---

## Closure

```
close_date            =
elapsed_weeks         =
meaningful_activity   = yes | no   (several MECH refreshes + a few real consultations + >=1 JUDG/MIX trigger)
CORE_PERSISTENCE_RATIFIED = true | false | INSUFFICIENT_ACTIVITY
```

### Trial report (write at closure)

- trigger frequency observed vs the "slow map" expectation:
- actual maintenance effort (MECH vs JUDG/MIX):
- judgment churn (did any JUDG/INTERP reading flip? which?):
- real consultation value (or absence):
- over-read / misuse incidents and severity:
- rows retired / added:
- disposition rationale:
- if failed/inconclusive: rollback done? probe check kept or reverted?
