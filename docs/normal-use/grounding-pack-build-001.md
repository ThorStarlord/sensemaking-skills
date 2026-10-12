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

| Condition | Status |
| --- | --- |
| Pack merged | Not met (PR #166 open) |
| Owner intent review | Not met |
| Spot-check failure rate under 10% on a random sample of 10 | Not met (not sampled; 3 errors found in about a dozen checked citations) |
| Result note written | Met (this note) |

**Phase 2 status: PARTIAL.** The pack exists and the mechanical checks pass. It can't be called complete until the owner reviews it and a random spot-check is done.

## Notes for Phase 3

- The pack's value on this repo is unproven. The target's authority set is already extensive, and the pack's README sends agents to those files first, so the pack adds reading rather than replacing it.
- Any evaluation should use real historical tasks and state which knowledge was available at each baseline. Current pack content postdates most historical baselines, so replays leak to that extent.
