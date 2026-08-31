# 12 — V0 SYNTHESIS (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Architecture-development conclusion. **Not** a production ratification
(authorization Section 27). Answers the 10 required questions, then the
direction disposition.

---

## 1. Did rich explicit architecture produce observable decision value?

**Yes, but unevenly and concentrated.** The value was real in a minority of
places and mostly-repackaging in the majority.

- **Real decision value** (code A/C/G in `OBSERVATIONS`): cross-cutting impact
  analysis for a single contract field (`09` Q6), the "policy decided vs
  implemented" divergence ranking (`09` Q5, `11` RC#5), the deprecated-file /
  contradictory-ownership finding (`11` RC#6), and the "exactly one research
  thread touches product" answer (`09` Q4). These are cases where assembling
  the answer from raw sources is either slow *or* error-prone-by-omission.
- **Repackaging** (code F, not B): most of `01`, `02`, `04`, and `07` restate
  content already present in `CONTEXT.md` + `AGW` + `artifact-contracts.yaml` +
  the research agenda, just typed and cross-linked. Useful as an index; not a
  discovery.

## 2. Where exactly did it help?

| Location | Help type |
|---|---|
| `05` authority seams, POLICY-vs-IMPL column | ranked the impl/policy divergences; named the split-authority facts |
| `06` §2/§4 | surfaced the deprecated-file-is-canonical contradiction and the registry drift + missing parity check |
| `09` Q6 | assembled the ~9-node blast radius of a `representation_sufficiency` change across 4 relationship families |
| `07` "canonical relevance" column | isolated RC-1 as the only research→product edge |
| `03` lifecycle edges | kept superseded ADRs (0017-0021, 0018) from reading as live |
| `11` RC#2/#4/#5/#6 | authority/lifecycle boundaries were DIRECTLY_VISIBLE |

## 3. Where did it merely repackage information an agent can cheaply recover?

- Component enumeration (`02`) below the "load-bearing pair" level.
- Producer/consumer rows for the PM/UI sub-pipeline (`04`) — verbatim from
  `artifact-contracts.yaml`.
- The end-to-end flow diagram (`01`) — `AGW` section 1 already has it.
- Research-claim ceilings (`07`) — every claim already carries a written "what
  this does NOT claim" section; V0 re-indexed, did not reveal.
- `does_not_own` lines for low-salience skills — near-tautological.

## 4. Where did it mislead or become stale/ambiguous?

- **`11` RC#7 (partial MISLEADING):** V0 shows the reconciliation fan-in as a
  *resolved* contract without foregrounding that cross-run prior-report identity
  is still `CONVENTION`. A reader could over-read "resolved."
- **Component granularity** is `INTERPRETIVE` — putting `CONTEXT.md` and a
  probe script at the same "component" level is a defensible-but-contestable
  modeling choice a reviewer could reject.
- **Staleness vector:** V0 embeds specific ADR statuses, SHAs, and counts. The
  6 commits between the authorization SHA and `ba8968c` already show how fast
  the research surface moves; a persisted V0 would need those cells refreshed
  or it would mislead within weeks.

## 5. Which relationship families were load-bearing?

Ranked by observed use across `09` + `11`:

1. **AUTHORITY** (GOVERNS / DEFINES_CONTRACT_FOR / ENFORCES_CONTRACT_FOR /
   OWNS) — used in every prospective view and 5 of 7 challenges. The
   DEFINES vs ENFORCES vs RUNTIME-OWNS distinction is the single most valuable
   thing V0 encodes.
2. **LIFECYCLE** (SUPERSEDES / HISTORICAL_ONLY / DEPRECATES) — kept
   superseded/deprecated state legible; directly answered RC#5, RC#6.
3. **VALIDATION** (ENFORCES / "declared but unenforced") — surfaced the
   no-enforcement rows and the split-enforcement risk.
4. **ARTIFACT** (PRODUCES / CONSUMES / TRANSFORMS) — needed for impact
   analysis (Q6) and fan-in (RC#7), but mostly recoverable from the contract
   file directly.
5. **RESEARCH** (LIMITS_CLAIM / DOES_NOT_ESTABLISH / canonical-relevance) —
   valuable for Q4 only; elsewhere it re-indexes existing discipline.

Weak: **STRUCTURAL** (CALLS / DEPENDS_ON / CONTAINS) — lowest use; a plain
import/dependency graph or `grep` recovers these as cheaply.

## 6. Which representation was expensive but low-value?

- Full component enumeration with `does_not_own` for every skill.
- The PM/UI artifact-flow rows.
- STRUCTURAL edges generally.
- Restating the operating flow as prose+diagram in `01`.

## 7. Which representation seems useful almost all the time?

- The **authority seam table** with DEFINES / ENFORCES / RUNTIME-OWNS /
  WINS-ON-CONFLICT / POLICY-vs-IMPL columns.
- **Lifecycle status** on ADRs / capabilities / registries (active vs
  superseded vs deprecated vs research-only).
- The **"declared contract with no/weak enforcement"** list.
- **Epistemic grading** of each assertion (cheap, disciplining).

## 8. Which representation seems useful only for particular questions?

- **Cross-cutting artifact-impact tracing** — extremely valuable for "what
  breaks if I change field X" (Q6), near-useless otherwise. An **on-demand
  projection**, not a standing document.
- **Research-claim map** — valuable when the question is "which experiment
  established what / is it still live" (Q4, RC-8 meta-finding); otherwise the
  per-claim "what this does NOT claim" prose already suffices.
- **Full component register** — useful for onboarding orientation; stale fast.

## 9. Smallest plausible high-value architecture suggested by V0

A **thin persistent core** of roughly:

1. **Authority-seam register** — one row per consequential fact: DEFINES /
   ENFORCES / RUNTIME-OWNS / WINS-ON-CONFLICT / POLICY-vs-IMPL. ~12-15 rows.
2. **Lifecycle ledger** — ADRs / capabilities / registries with status +
   supersession edges. Mostly derivable from the ADR probe; the value-add is
   the *capability* and *registry* rows the probe doesn't cover.
3. **Declared-but-unenforced list** — contracts with no or weak mechanical
   enforcement, and multiply-enforced contracts.
4. **Research→product edge list** — only the edges where a research conclusion
   reaches a runtime path (currently: one).

Everything else (component enumeration, structural edges, artifact-flow rows,
full research-claim map, the narrative overview) is either cheaply recoverable
on demand or better generated as a **projection for a specific question** than
maintained.

Estimated persistent size: **~1 page of tables**, not 12 files.

## 10. Most plausible architecture direction

```
ARCHITECTURE_DIRECTION_DISPOSITION = THIN_PERSISTENT_CORE_PLUS_ON_DEMAND_DETAIL
```

**Reasoning:**
- The value clustered in 4 small, slow-changing, high-consequence structures
  (authority seams, lifecycle, unenforced-contract list, research→product
  edges) — Q7's "useful almost all the time" set. That argues for a *thin
  persistent core*.
- The one genuinely hard-to-recover capability (cross-cutting impact analysis,
  Q6) is question-specific and best produced **on demand** against current
  repository state, not maintained — a persisted version would be the fastest
  cell to go stale (finding #4).
- `ALWAYS_RICH` is contradicted by findings #1/#3/#6: most of V0 was
  repackaging and it decays fast. It also collides with the repo's own
  `harden only where pressured` principle and the PHB meta-finding (0/3 FULL
  spikes changed a decision).
- `NO_DEDICATED_RICH_REPRESENTATION` is contradicted by RC#6 and Q6, where V0
  surfaced a real contradiction and a real omission risk that the current prose
  (`CONTEXT.md` + `AGW`) does not.
- `CONDITIONAL_RICH` is close, but V0's evidence says the *core* (authority +
  lifecycle + enforcement gaps) is worth holding **persistently and cheaply**,
  while the *rich detail* is worth generating **only when a specific decision
  needs it** — which is precisely THIN_PERSISTENT_CORE_PLUS_ON_DEMAND_DETAIL,
  not "sometimes build the whole rich thing."

**Confidence:** moderate. Single repo (self), retrospective + prospective use
by one agent, no independent evaluation, no normal-use episode. This is an
architecture-development signal, not a validated result.

---

## Bridge to a possible V1 (NOT authorized here — authorization Section 28)

If the owner authorizes a next step, the compression target is:
`05-AUTHORITY-MAP.md` (seam table only) + a lifecycle/enforcement-gap table
derived where possible from the existing ADR + relationship probes + the
one-line research→product edge list. Drop `01`, most of `02`, the PM/UI half of
`04`, and the STRUCTURAL family. Treat `03` cross-cutting queries and `09` Q6
as an **on-demand projection generator**, not a file.

Do **not** build persistence, invalidation, a graph runtime, or PHB integration
without a separate owner decision.
