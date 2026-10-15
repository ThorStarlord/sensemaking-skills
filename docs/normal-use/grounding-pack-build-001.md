# Grounding Pack Build 001 (Phase 2 result note)

**Evidence class:** repository work and agent review. Not human evidence.
**Target:** `ThorStarlord/React_incremental_game_prototype`, base `main@55fb384`.
**Pack location:** branch `claude/grounding-pack-phase2` on PR #166 (target repo), head at the time of writing is recorded in that PR, not here.

## What was built

A thin pack at `.sensemaking/`: `README.md`, `intent.md`, `context.md`, `invariants.md`, and two decision records. The pack links to the existing authority set (`AGENTS.md`, `CLAUDE.md`, `STATUS.md`, `specification/`) and adds only what those documents do not state directly.

## Measured

- Words: `intent.md` 308, `context.md` 165, `invariants.md` 105 (within budgets of 800 / 800 / 600); README and two decision records together make the pack 897 words in total (decision records within the 250 each budget).
- Tag-bearing lines: 37 (bullets and decision lines). Primary tags: `policy` 28, `delegated` 3, `test` 2, `hypothesis` 1, `code` 1, `owner` 0.
- Owner-confirmed lines: **0**. The owner has not reviewed the pack. Delegated choices are tagged `[delegated: 2026-10-12]`, not `[owner]`.
- Time to build: not measured.

## Spot-check (against the plan's exit criterion)

The plan asked for 10 randomly chosen tagged lines checked against their cited files. That has **not** been done as a random sample. What was done:

- every cited path was confirmed to exist;
- about a dozen citations were checked against their content.

Of the citations checked by content, **three were wrong** and were fixed:
1. two rules cited to `AGENTS.md` that live in `CLAUDE.md` (fixed in `a7f6ee8`);
2. a "no tuning targets" rule cited to the wrong file, and its wording was overstated (fixed in `eb2c279`, found by the synthetic stress test).

Treat the random-sample spot-check as **not yet passed**.

## Owner corrections

None. No owner review has happened.

## Exit conditions

The table below records the **pre-waiver** evidence checkpoint. The later
owner directive below supersedes the merge/intent states but **does not**
convert the failed sample into a pass.

| Condition | Status |
| --- | --- |
| Pack merged | Not met (PR #166 open) |
| Owner intent review | Not met |
| Spot-check failure rate under 10% on a random sample of 10 | Not met (not sampled; 3 errors found in about a dozen checked citations) |
| Result note written | Met (this note) |

**Phase 2 final disposition (2026-10-12): COMPLETE BY OWNER DIRECTIVE WITH WAIVER; quality threshold NOT PASSED.** The table above is a pre-waiver snapshot. The later owner-approved `intent.md`, accepted citation corrections, and merge of target PR #166 close Phase 2 administratively; the fresh spot-check needed correction on 20% of sampled lines versus a 10% ceiling. This acceptance must not be relabeled as a validation pass or comparative Grounding Pack effectiveness.

## Notes for Phase 3

- The pack's value on this repo is unproven. The target's authority set is already extensive, and the pack's README sends agents to those files first, so the pack adds reading rather than replacing it.
- Any evaluation should use real historical tasks and state which knowledge was available at each baseline. Current pack content postdates most historical baselines, so replays leak to that extent.

## Owner directive (2026-10-12)

- `intent.md` approved by the owner, with external playtesting DEFERRED / TBD (no assigned owner or date).
- The fresh 10-line spot-check is waived. It was not passed: the sample as run had 20% of lines needing correction, against the 10% threshold. The corrections in `6a7fe8b` are accepted. Record this as a waiver, not as a pass.
- The pack was merged to `main` on the owner's directive once CI passed on the final head.
