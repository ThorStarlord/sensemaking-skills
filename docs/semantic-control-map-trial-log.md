# Semantic Control Map — Trial Log

Fill during the trial. Protocol: `docs/semantic-control-map-trial.md`.
Map: `docs/semantic-control-map.md`.

```
trial_start_commit   = <commit that merged this PR>
trial_start_date     = <YYYY-MM-DD>
minimum_close_date   = trial_start_date + 4 weeks
maximum_close_date   = trial_start_date + 8 weeks
status               = OPEN
```

---

## A. Trigger events

| date | commit | trigger | affected rows | refreshed? |
|---|---|---|---|---|
| | | | | |

## B. Maintenance effort (actual minutes)

| date | activity (MECH refresh / JUDG review / MIX review) | rows | minutes | notes |
|---|---|---|---|---|
| | | | | |

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
