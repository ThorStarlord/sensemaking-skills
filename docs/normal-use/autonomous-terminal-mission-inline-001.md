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
