# SYNTHESIS — SEMANTIC CONTROL CORE V1

Architecture-development conclusion. **Not** product ratification, **not**
persistence ratification (authorization §26, §34).

---

## The 12 questions (authorization §33)

**1. How much of V0 was discarded?**
By line count, ~89% (2804 → 299 core). By file count, 16 → 3. Whole families
gone: STRUCTURAL (CALLS/DEPENDS_ON/CONTAINS), PRODUCT-capability enumeration,
the 9-row research-claim map, the full component register, PM/UI artifact-flow
rows, restated operating-flow prose, per-experiment claim ceilings, all embedded
SHAs/counts/file inventory.

**2. Which V0 value survived directly in the core?**
8 of the 10 mandated value cases (PR #243 ownership split, ADR 0010 path
ownership, routing policy-vs-impl divergence, `auto_invoke` authority, superseded
ADR / present-implementation distinction, deprecated-file-still-load-bearing,
research→product crossing, and the explicit statement of the raw-inspection
floor). Carried by: 7 authority-seam rows, a 6-entry lifecycle ledger, an 8-row
enforcement-gap register, 1 research→product edge.

**3. Which V0 value survived only through on-demand projection?**
`representation_sufficiency` cross-cutting blast-radius analysis (case 9) — the
core supplies the seed rows (A2, A6, §4) and the recipe scopes the search to 3
files. Consumer-level blast radius of registry mirror drift (case 7 / the drill).
Both were question-specific in V0 as well.

**4. Which useful V0 behavior was lost?**
None of the 10 mandated cases. `DEGRADED`/`LOST`/`MISLEADING` count = 0.
Discarded content was not used in any V0 retrospective or prospective reasoning
case, so its removal is compression, not loss. (Caveat: the V0 challenge set
itself is the yardstick; a value V0 never exercised cannot show up as lost here.)

**5. Did any compression create misleading architecture?**
No misleading *case*. One residual *risk*: a reader who consults the core and
does not invoke the recipe can over-read a **silent omission** (no row for X) as
"nothing to know about X." Two holdouts (ADR 0025 plan lifecycle; canonical
vocabulary) are exactly such omissions — both recover in one documented hop, but
only if the reader reaches recipe step A. The mitigation (core §5 + recipe step
A) is textual, not structural. This is the sharpest weakness of the thin-core
form.

**6. Which semantic row types were repeatedly useful?**
- **Authority-seam rows** — used in 8 of 10 cases + both holdouts + the drill.
  The DEFINES vs ENFORCES vs RUNTIME-OWNS split is the single highest-value
  element, exactly as V0 found.
- **Lifecycle-ledger rows** ("present ≠ authoritative") — cases 5, 6; the
  reason superseded/deprecated state stays legible.
- **Enforcement-gap rows** — cases 3, 6, 7; the `IMPL_AHEAD_OF_POLICY` /
  `MIRROR_DRIFT` tags did real work.
- **Research→product edge** — case 8; one row replaced a 9-row map.

**7. Which retained rows appear slow-changing enough to plausibly maintain?**
13 of 22 load-bearing rows are `S` (slow); 7 are `M` (decision-cadence, not
commit-cadence: A5, A6, A7, G4, G5, G6, research row); **0 are `F`**.
Compression preferentially kept slow-changing facts — the staleness hypothesis
from V0 is *addressed* by the core's construction, not merely asserted.

**8. Did the projection recipe materially outperform ordinary unstructured
rediscovery?**
Yes, in the one drill run: G5 named the exact seed and 3 targeted reads bounded
the mirror-drift blast radius; without the core row the same question is an
open-ended grep across `scripts/` + `src/`. n=1 drill + 2 holdouts — a
sanity-level signal, not a measured result.

**9. Did the two holdout cases generalize beyond the V0 challenge set?**
Yes. Both located the correct authority region for episodes outside the V0 set
in one documented hop, no misleading result. Both were deliberate probes of
core *omissions*, so the result also confirms the inclusion test is drawing a
defensible line. n=2, sanity check only.

**10. Did the current-state projection drill reveal a useful architecture
relation not encoded persistently?**
Yes: "`workflow-runtime.py` reads only the canonical `workflow-registry.yaml`;
`WorkflowRegistry` merges canonical over `src/defaults/`, so the mirror drift is
inert on this repo and only bites an external target with no local registry."
Useful, but consumer-level and code-cadence → **promotion recommended = NO**
(the slow-changing part, "the drift exists," is already G5).

**11. Is a dedicated thin semantic core still warranted?**
On this evidence, **yes** — with caveats. It preserved 8/10 high-value cases
directly at ~11% of the size, kept only slow/decision-cadence facts, and made
the raw-inspection floor explicit. Caveats: single repo (self); the same author
built V0 and V1 (not independent); "which facts belong in the core" carries
modeling judgment (grade the *inclusion* choices INTERPRETIVE even where each
row's content is DEMONSTRATED); silent-omission over-read risk is unmitigated
structurally.

**12. Is persistence now worth testing, or is the next responsibility something
else?**
Persistence testing is **plausibly warranted but not yet** — the missing
evidence is (a) independent construction: would a different agent draw the same
~22 rows? (b) normal-use: does the core get *consulted* and stay correct across
a few real engineering tasks without a maintenance burden spike? Those are the
next questions, not "wire it into a product doc."

---

## Failure-mode assessment (authorization §27 — not biased toward A)

| Mode | Verdict |
|---|---|
| A `COMPRESSION_PRESERVES_VALUE` | **partially supported** — tiny core preserved 8/10 directly; 1 via projection; 0 lost/misleading among mandated cases |
| B `RICH_CONTEXT_WAS_LOAD_BEARING` | **not supported** — no mandated value case required V0's discarded detail |
| C `CORE_TOO_STALE` | **not supported** — 0 fast-changing rows; construction preferentially kept slow facts |
| D `CORE_TOO_INTERPRETIVE` | **partially present** — each row's content is DEMONSTRATED, but the *selection* of ~22 rows is a contestable modeling judgment; an independent author might differ at the margins |
| E `PROJECTION_RECIPE_TOO_EXPENSIVE` | **not supported** on n=1 drill + 2 holdouts — each resolved in ≤3 targeted reads / 1 documented hop |
| F `NO_DEDICATED_CORE_NEEDED` | **not supported** — cases 3, 5, 6, 7, 8 assemble facts that `CONTEXT.md` + `AGW` + ordinary inspection leave scattered; the core's cross-source assembly is the value |

## Compression success criterion (authorization §21)

- A. most V0 high-value conclusions directly visible from the tiny core — **met** (8/10)
- B. question-specific detail recoverable via the recipe without a permanently
  rich representation — **met** (case 9, drill, both holdouts)
- C. materially reduced size/staleness burden — **met** (~11% size; 0 fast rows)
- D. no new misleading simplifications — **met for cases**; one residual
  silent-omission risk noted (Q5)

---

## Disposition

```
V1_ARCHITECTURE_DISPOSITION = THIN_CORE_PLUS_PROJECTIONS_PRESERVES_VALUE
```

Not `THIN_CORE_PRESERVES_VALUE`: the projection recipe was load-bearing for the
hardest V0 capability (blast-radius analysis) and for both holdouts — the core
alone is insufficient and is *designed* to be.

Not `RICHER_CORE_REQUIRED`: nothing among the mandated cases needed V0's
discarded richness.

Not `NO_DEDICATED_CORE_REQUIRED`: the cross-source authority/lifecycle/gap
assembly is value that existing canonical docs do not provide.

Confidence: **moderate**. Single repo = self; non-independent construction;
n=2 holdouts + n=1 drill; core-inclusion choices carry modeling judgment.

```
DEDICATED_THIN_CORE_STILL_WARRANTED   = true
PERSISTENCE_TEST_NOW_WARRANTED        = inconclusive  (leaning true — gated on
                                        independent-construction + normal-use
                                        consultation evidence, not on more
                                        prototype iteration)
PROJECTION_PROMOTION_RECOMMENDED      = false
```

## Next

Return to owner review of the frozen V1 core + this evaluation. Do **not** build
V2, wire the core into any product doc, implement persistence, or add
infrastructure. The next *evidence* question is independent reconstruction +
light normal-use consultation of the frozen core — not another compression pass.
