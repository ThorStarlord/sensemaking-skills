# Post-hoc retrospective — Controller A vs Controller B

```
WRITTEN:   2026-09-02 by the lead Campaign 2 controller (the context that was
           Controller A), AFTER Controller B completed its full strategic cycle
           and reached a legitimate terminal disposition. The owner instruction
           ("Controller A Relinquishment Rule") permits retrospective A/B
           comparison only at this point.
SCOPE:     this file does not edit any A-* or B-* checkpoint. It records what the
           two controllers' independent work reveals about the succession.
```

## Did the succession actually transfer semantic decision-making authority?

**Yes, at the honest evidence level the environment supports.**

- Controller B received **only** the verbatim bootstrap in `A-handoff.md`
  (worktree/branch + `CHARTER.md` + `CAMPAIGN-STATE.md` paths + "you are the
  active semantic controller" + reconstruct/reverify/independently-select/
  checkpoint-before-implementation). No mission text, task rationale, frontier,
  gaps, recommended task, or predecessor predictions crossed.
- B reconstructed the mission, authority, and three state planes from durable
  sources (`B-reconstruction-and-selection.md` Part 1, Q1–Q20).
- B **reverified 12 consequential durable-state claims** before acting
  (`B-*` Part 0). All were correct at the decision level; the only corrections
  were cosmetic (N-1: CI was also green on `358b5a2`, recorded for `431ec43`
  only; N-2: three unfilled `<...>` SHA placeholders). **No
  `HANDOFF_FACT_TRUST_FAILURE`** — verification-bearing continuation held.
- B **committed its reconstruction + selection checkpoint (`4ccbc70`) before any
  Task B implementation and before any predecessor semantic feedback.** The
  predecessor gave none until this file.
- B **partially rejected Controller A's recorded frontier**: it treated F-a..F-d
  as "LAST ASSESSED CANDIDATE", rejected F-d (staged-reveal minimality probe) as
  measurement-only, confirmed F-c (Goal A substrate) as `OWNER_DECISION_REQUIRED`
  and therefore not campaign work, and folded F-a/F-b in rather than adopting
  them as tasks.
- B **independently selected a different task** (the *machinery* half of the
  development-direction reconstruction surface) via its own five-alternative
  comparison (`B-*` Part 2, B-ALT-1..4) and its own Strategic Selection Gate
  (`B-*` Part 3).
- After the handoff commit, Controller A performed **only** the mechanical
  `Agent`-tool spawn and did not steer B. Acceptance condition 19 (succession
  integrity) holds.

## Where A and B agreed and disagreed

| Dimension | Controller A | Controller B |
|---|---|---|
| Highest-leverage boundary family | development-direction reconstruction surface | **same family**, but the *machinery* half (A did the human half) |
| Task shape | investigate + smallest human-surface change | substantive deterministic-machinery change (`scripts/` + regression tests) |
| Goal A (F-c) | flagged as `OWNER_DECISION_REQUIRED`, not campaign work | **confirmed** independently against Issue #255 |
| Comparative minimality (F-d / EC-1) | named as a frontier candidate | **rejected as Task B** (measurement, would leave the campaign with no substantive implementation) — preserved as an explicit ceiling |
| MG-6 (product vs campaign state) | named as F-b | partially resolved as a by-product (machinery-consistency = product; succession provenance = campaign-only) |
| Disposition | (did not assess — handed off first) | disposition **read** `CAMPAIGN_COMPLETE`; declined to *declare* it (owner-reserved) |

**Convergence with independent divergence.** B did not reproduce A's task, but
selected within the same capability family A had identified — and, notably, B's
task *completed the half A left unfinished* and *resolved a product-consistency
contradiction A's own change introduced* (Task A's prose "historical" headers
were invisible to the probe's path-only classifier, so the version-drift probe
kept flagging `roadmap.md`/`goal.md`). This is the strongest single piece of
evidence that the durable state carried a real, actionable frontier rather than
just A's opinion: a fresh controller, given only the bootstrap, found the same
boundary *and* found the gap A had not noticed.

## What this does and does not establish about succession

**Establishes:** a fresh **controller** (not merely a fresh worker) can
reconstruct, reverify, independently select against the predecessor's
assessment, checkpoint before feedback, and execute real engineering — the
`FRESH WORKER != FRESH CONTROLLER` distinction the owner instruction draws, and
the exact capability Campaign 1 explicitly did not establish.

**Does not establish:** strong isolation (same model family; Controller A's
process persisted and received B's report through the `Agent` call;
non-resumption was discipline, not environment enforcement —
`SUCCESSION_ISOLATION_UNVERIFIED` on that dimension); scale (one succession, one
repository, one day); or that the *specific* durable-state arrangement is
minimal (no smaller-state comparison was run).

## Contamination / integrity notes

- The A1 sub-probe (a tool inside Task A, not the succession) disclosed a `Grep`
  leak of ~30 lines of the excluded Campaign 2 directory; assessed immaterial
  (FO-3).
- Controller B's reconstruction is a **contaminated** test of Task A's *product*
  surface specifically: B was pointed at the campaign durable tree by the
  bootstrap, so it did not reconstruct "from the refreshed `STATUS.md` alone". A
  clean repo-only re-test of the refreshed surface was **not** run (it would
  need a fresh sub-context; B rejected B-ALT-1). This is a recorded ceiling, not
  a hidden gap.
- Both controllers ran in the same worktree (`H:/GithubRepositories/smk-campaign-2`),
  sequentially, each from a clean committed state. No predecessor working-tree
  leftovers crossed the handoff (pre-handoff invariant item 11).
