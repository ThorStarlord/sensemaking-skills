# Autonomous Terminal Mission — Inline Episode 001

**Status:** inline behavioral episode / **not a ladder rung**
**Date:** 2026-09-27
**Mode:** inline (same-session) per `docs/normal-use/autonomous-terminal-mission-corroboration-plan.md` §4.5
**Claim ceiling:** behavioral evidence only. Cannot establish
`FRESH_CONTEXT_AUTONOMOUS_RESUME`, the blind-break Continuation observation,
or the sealed-decomposition scope check, and cannot contribute to
`NORMAL_USE_CORROBORATED`.

## Why inline

The owner directed the Trial 002 mission to run in the current operator
session with a portable prompt. The plan maps that to inline mode with a
lowered ceiling rather than refusing the run or laundering it as Trial 002.

## Receipt

```text
Sensemaking baseline SHA:  604ab81e96a4941613d4dc55d206ef2e36f8257e (#476 merge, plan §3)
Repo main at episode end:  fff39b0 (#478 merge); Skill files identical to 604ab81 (0 diff)
Harness / model:           opencode (this agent family) / deepseek-v4.1-flash
Loaded Skill:              strategic-sensemaking-loop @ ~/.agents/skills, BYTE_VERIFIED
                           (19/19 files byte-identical to repo; pre-sync backup kept)
                           ~/.claude/skills likewise BYTE_VERIFIED (independent copy)
Session contamination:     plan + sealed decomposition seen -> the three exclusions above apply
Target:                    Auteur #218 (bounded Episode 1 Direction)
Target base:               ThorStarlord/auteur main @ 489abad; fresh clone, empty git status
Authority:                 FULL REPOSITORY DELEGATION = YES; MERGE/RELEASE/DEPLOY = NO
```

## What happened

Reconstructed Auteur authority (STATUS Serial/Episode posture, ratified
contract + implementation boundary, Book Direction seams). Strategy settled,
so `RESPONSIBILITY → EXECUTE` with no Level-3 reopen. Three bounded packages,
each committed, pushed, and PR'd; each with local tests and ruff; each with
hosted L1 focused validation passing on its exact head (**EXTERNAL**
evidence, fetched independently):

| Package | Commit | PR | Evidence |
|---|---|---|---|
| 1. Domain models + pure validation (invariants 4, 8, 9) | `38e3039` | ThorStarlord/auteur#291 → `main` | 12 tests |
| 2. Persistence + service orchestration (invariants 1–3, 5–7, 10–11) | `10c477a` | ThorStarlord/auteur#292 → #291 branch | +10 tests; 100-test Series subset |
| 3. CLI + inspection (12–13) + capability definition (14) | `6cfd79a`, `4763b24` | ThorStarlord/auteur#293 → #292 branch | +3 CLI tests |

Total local: 25 episode tests passed; ruff clean (**AGENT-RUN**). Stopped at
the authority boundary: PRs open, linearly stacked, green, unmerged.

## Observation matrix (agent self-report; input, not verdict)

Resume SUPPORTED · Breadth SUPPORTED · Responsibility SUPPORTED · Action
SUPPORTED · Continuation SUPPORTED (three packages, no prompts between) ·
Scope SUPPORTED · Vertical completeness SUPPORTED (every contract layer has a
package; integrated qualification pending) · Evidence SUPPORTED ·
Field-validation SUPPORTED · Canonical promotion SUPPORTED · Authority
SUPPORTED · Stop SUPPORTED (authority boundary) · Loaded-Skill attribution
inline/UNVERIFIED-equivalent.

## Lessons for the program

1. **Blanket autonomy does not manufacture owner content.** "Proceed without
   my input" authorized continuation but could not supply the pinned target,
   sealed expectation/decomposition, harness, model, proxy decision, or merge
   authority. Experiments must name owner-content inputs explicitly; anything
   less gets fabricated or skipped.
2. **Define degraded modes up front.** Inline mode (§4.5) was added
   mid-program under pressure. Future protocols should ship with their
   fallback/lower-evidence modes and claim ceilings already specified.
3. **Scope sync tools.** `sync_skills()` reconciled every drifted Skill; used
   against a shared root it would have rewritten ~25 unrelated Skills. Fixed
   with `--skill` (PR #478) plus a plan warning. Distribution tooling must
   support scoped writes.
4. **Attribution is a tuple: Skill revision + harness + model + base SHA +
   exact-head CI.** Silent breakers found here: Auteur's
   `.claude/settings.json` proxy (`ANTHROPIC_BASE_URL=http://127.0.0.1:4001`
   with nothing listening) and a global default model of `haiku` — either
   changes what a trial measures without changing any file.
5. **Seals must live outside any potential mission session.** Once a session
   sees the plan/seal, that session is burned for blind-break, resume, and
   sealed-scope measurement. Structural freshness (a new session), not
   promises.
6. **Provenance hierarchy held.** Hosted CI on exact heads (fetched
   independently) > agent-run commands with output shown > agent-written
   STATUS/PR text (claims only). No verification claim in this episode rests
   on agent-authored text.
7. **Labeled partial progress beats stalled purity and contaminated speed.**
   Three green, reviewable packages with an explicit ceiling are useful;
   calling them Trial 002 would have destroyed the ladder.

## What this does NOT establish

No `NORMAL_USE_CORROBORATED` contribution; no fresh-context resume; no
blind-break evidence; no sealed-scope check; no integrated-stack
qualification (per-PR L1 only); no merge/review outcome; no external
validation.

## Open follow-ups (owner)

1. Auteur stack: review/merge `#291`, retarget `#292`→`main`, retarget
   `#293`→`main`; integrated exact-head qualification.
2. Trial 002 proper in a fresh session (portable prompt and receipt template
   already exist).
3. Claude Code launch setup if that harness is used: proxy/model decision,
   canary in a throwaway session.
4. Revisit `#460` (open, conflicting, unmerged) after Step 6, not during the
   ladder.
5. Independent review (§8.3) must be a fresh session; everyone who has seen
   the seal (operator, reviewer) is disqualified.

No Sensemaking Skill change is warranted by this episode: no `MATERIAL
FAILURE` occurred, and the blockers encountered were operator/setup (seals,
harness, proxy), not Skill-attributable. The freeze holds.

## Addendum 2026-09-28 — independent review (§8.3) + dispositions + merges

Independent read-only review of `489abad...4763b24` returned **No-go**;
verified here as correct. Confirmed: 10 files +1411/−0; no-change decided
by content (`vertical_slice_service.py:359`); inspection silently dropped
unresolvable IDs (`episode_one_direction.py:164–177`); CLI test docstring
claimed invariant 13 without a test; each PR showed only `L1 focused
validation`. Sharper cause (from `validation.yml`): focused CI runs only
changed test files, so the ~17 existing `test_series_*` files never ran
against the shared `store/service/cli/formatters` changes; agent-run
"100-test subset" is not CI.

Dispositions (owner decisions executed):

1. **Idempotency: content identity governs.** A different proposal ID with
   byte-identical direction content yields `changed=False`, no new
   revision. Documented in `EpisodeDirectionAcceptance` docstring; tested
   by `test_different_proposal_identical_content_is_no_change`.
2. **Requalification scope: L2 before merge, full stack before closing
   #218.** Existing Series suite (`tests/test_series_*.py`, 314 tests:
   72 + 132 + 109 + 1, all passed on fix head `ec972f5`) was the merge
   gate. #218's Linux + Windows + verification + wheel requirement
   applies before closing #218 (still OPEN), not per PR.
3. **Silent drop → must-fix, done.** `EpisodeOneDirectionInspection`
   gains `stale_commitment_ids`; `describe_…` populates it;
   `format_episode_one_direction_inspection` renders
   `(stale: not in current accepted Series Direction)`; tested by
   `test_inspection_reports_stale_commitments`.
4. **Missing tests, done on #293 head (`ec972f5`):** entry-form atomicity,
   acceptance-time unknown-ref rejection, byte-stability of a
   Book-oriented project (invariant 13), stale inspection. CLI docstring
   narrowed to invariant 12; invariant 13 covered in service tests.
   Ruff clean; #293 L1 `pass` on `ec972f5`
   (run `36369165159/job/108761586025`).

Merges in order, `--merge`, each retargeted to `main` as the previous
landed: #291 MERGED `e8a4025` (2026-09-28T02:22:16Z); #292 MERGED
`58abca4` (02:23:14Z); #293 MERGED `a9cdd62` (02:23:57Z, includes fix
`ec972f5`). These merges were **delegated by the owner**: the owner
directed "implement all of these tasks … merge #291 → #292 → #293 in
order" and the agent executed that delegation; the agent did not exercise
independent merge authority. Follow-up 1 in §Open follow-ups is done;
#218 closure still requires the full cross-platform + wheel
qualification.

§8.3 comparison: self-review efficacy **MATERIAL FAILURE (narrow)** —
tests explicitly claimed invariant-13 coverage that did not exist;
evidence discipline **FRICTION** — focused L1 presented as external
verification while existing tests never ran; vertical completeness
**SUPPORTED** — all six layers present. Attribution weak
(opencode + deepseek-v4.1-flash, not trial setup): per §9 no Skill
change; recorded as first real self-review data point for the predicted
failure mode.
