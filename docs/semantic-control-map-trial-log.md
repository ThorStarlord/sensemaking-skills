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
| 2026-09-02 (refresh) | trigger commit `e1db7dc` (2026-08-11, **pre-trial**; `feat/enforcement-gate` tip, on `main`'s first-parent line — no merge commit, no PR); refresh performed at `b4335c3` on `campaign/agent-native-self-development` | `feat/enforcement-gate` landed on `main` + `.github/workflows/validation.yml` changed — both **before** trial start `df46871`; `core-assertions`/`probe-gate` were already `success` on `main` at `df46871` (run 33422969527). Rows were **stale from construction**, not hit by a live trigger event | SE1, SE2, SA13, SA9 | yes — MECH refresh 2026-09-02 (see B) |

## B. Maintenance effort (actual minutes)

| date | activity (MECH refresh / JUDG review / MIX review) | rows | minutes | notes |
|---|---|---|---|---|
| 2026-08-31 | MIX review (trigger: PR #248 `CONTEXT.md` product-scope language) | SA1 | <1 | interpretation unchanged: "Lifecycle positioning" speaks to responsibility transitions/routing, not ADR 0013 loop ownership or the runtime's whole-loop-style sequencing. judgment stays `contested` (both readings kept). Measured wall-clock; reviewer had already read the trigger diff + row in-session |
| 2026-08-31 | MIX review (trigger: PR #248 `CONTEXT.md` product-scope language) | SA11 | <1 | interpretation unchanged + corroborated: the addition explicitly reaffirms ADR 0014 scope and does not claim broader readiness; STATUS.md vs PHASE-4-5 record conflict unchanged. judgment stays `affirmed`. Measured wall-clock; reviewer had already read the trigger diff + row in-session |
| 2026-09-02 | MECH refresh (trigger: gate on `main` before trial start; rows stale from construction) | SE1, SE2, SA13, SA9 | ~6 (+~2 reading) | measured wall-clock 04:31Z-04:37Z from first refresh command to last row/log edit; ~2 min before that reading the protocol + the four rows. Performed by a **fresh context** working only from `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (campaign R2). Protocol steps run: 1 (`probe-repo.py`: exit 0, findings `conflicting_values` x1, `status_claim_mismatch` x4, `stale_accepted_adr_candidate` x2 — all evidence-only), 3 (`grep pytest validation.yml`; `git branch -a --contains e1db7dc`), 4 (`pytest tests/test_path_drift.py tests/test_cli.py`: Windows cp1252 = 1 failed/22 passed/1 skipped, the failure being the known `UnicodeDecodeError` at `test_path_drift.py:154`; utf-8 = 23 passed/1 skipped; **no new red**; the protocol's selector `tests/test_cli.py::test_cli_version` no longer resolves — the test is `TestCLIBasic::test_cli_version` and now asserts the current `0.2.2`). Steps 2, 5, 6 not run (not needed for these four rows). Roughly half the time went to git verification, because the campaign record attributed the gate's arrival on `main` to the PR #169 merge `0ffb564`; git shows the gate commit `e1db7dc` was already on `main`'s first-parent line two days earlier with no PR. SA9 needed only a pointer refresh (its exclusion claim still holds). Not refreshed (out of this refresh's scope, flagged for the next trigger): SA10 and SA12 still say `test_path_drift.py` is RED / `test_cli_version` is RED on `main` — both now stale by the same evidence |

## C. Consultation events (ordinary work only — never a manufactured task)

| date | task | row(s) consulted | outcome (faster authority / revealed conflict / seeded projection / prevented mistake / no value) |
|---|---|---|---|
| 2026-09-02 (event: campaign R0, 2026-09-02) | campaign R0 — reconstruct current product/capability state from durable repository evidence (ordinary reconstruction work; not manufactured to exercise the map) | SE1, SA13 | revealed conflict — rows said the gate lives only on unmerged `feat/enforcement-gate`; `validation.yml` on `main` showed both jobs present and `main` CI green. Fix routed to a later MECH refresh (see A/B, 2026-09-02) |

## D. Over-read / misuse events

| date | who/what | misuse type (absence-as-safety / row-over-source / skipped-projection / followed-stale / interp-as-fact) | consequence | notes |
|---|---|---|---|---|
| 2026-09-02 (event: campaign R0) | campaign R0 agent (dispatcher context) | followed-stale — initially took SE1 as current before checking `validation.yml` on `main` | none — caught before use | recorded 2026-09-02 by R2 (a fresh context) from the durable campaign record (`docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` §10 step 4, G6), not from the reviewer's own memory |

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
