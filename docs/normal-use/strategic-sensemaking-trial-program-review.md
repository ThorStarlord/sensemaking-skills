# Strategic Sensemaking trial program — cross-episode review and verdict

Section 12 review over `strategic-sensemaking-trial-002/003/004.md` (read-only
episodes on Pydantic, Jellyfin, and AION Workflow Core), 2026-09-29
(ratified 2026-09-30).

**Ratified by the owner on 2026-09-30.** Source:
`artifacts/owner_decision_capsule.md` (`OWNER-DECISION-SIMPLIFY-001`); decision:
Option B (staged program), Stage 1 only, verdict "simplify hard" (originally
tracked in #497, closed; remaining decisions in #506). This is not a score,
benchmark, or control/treatment study (guide section 14).

## Claim ceiling (read this before the verdict)

- **Two arms (skill vs clean no-skill control), but n=3, read-only, same
  reviewer.** The first pass had no control; the control arm was added afterward
  (see "Control arm (added 2026-09-29)" below). The "what would you have done
  without the skill" field is each subagent's own low-confidence guess, not
  measured counterfactual behavior.
- **Executor.** Each episode was run by an independent read-only subagent (not
  the guide's author), but the reviewer writing this verdict is not fully
  independent of the skill's design.
- **Boundary coverage.** All three episodes were read-only, so this program says
  nothing about build/inquiry discipline once write authority is granted.
- **n = 3**, deliberately small (guide section 12: a large dataset is not the
  goal).
- Trial 001 (`autonomous-terminal-mission-trial-001.md`) is prior evidence and is
  not re-interpreted here.

## Cross-episode questions (guide section 12)

| Question | Observation |
| --- | --- |
| Did breadth find alternatives the prompt did not expose? | Yes, all three. 002/003 surfaced the owner/authority and external-maintainer boundaries; 004 surfaced an unwired validation/retry gap that the visible roadmap did not expose. |
| Were candidates semantic compressions, not renamed observations? | Mostly genuine. 004 enumerated six themes where one was decision-changing; the adapters/CLI themes were closer to renamed observations. |
| Was depth concentrated on finalists? | Two of three yes. 004 read essentially the whole (small) repo — over-depth relative to size. |
| Does resume skip settled analysis / reopen on real invalidation? | Not applicable — single episodes, no resume path exercised. |
| Was unnecessary inquiry rare in construction-eligible cases? | Not applicable — no episode was construction-eligible (read-only authority). This is the program's main coverage gap. |
| Did Goal Fitness catch milestone inversion without blocking legitimate qualification? | Yes. 004 distinguished the v0.2 schema milestone from the capability it presupposes (enforced validation) *and* explicitly flagged overcorrection risk. 002/003 caught completion-layer mismatches (owner decision / external maintainer acceptance). |
| Are failures concentrated in one domain? | The one recurring friction — over-broad breadth enumeration — appeared across heterogeneous repositories (Python library, C# server, tiny Python library), so it is not domain-specific. No correctness failures occurred. |

## Recurring signal

- **The dominant baseline failure mode the skill prevented was the same in all
  three episodes:** first-visible-problem capture — treating a vague "advance"
  objective as a license to start implementing the first plausible item
  (a TODO, a coverage bump, the README roadmap milestone). All three (skill arm)
  self-reported counterfactuals describe that behavior; all three instead
  surfaced the correct blocking question.
- **Two of three correctly refused to invent scope** and escalated on an
  owner/authority boundary that repository evidence cannot resolve.
- **One of three produced a substantive capability finding** (AION: validation
  is collected but never enforced; architecture.md claims retry hooks that do
  not exist) by challenging the visible milestone rather than executing it.
- **The recurring cost is breadth over-enumeration:** overhead was judged
  "marginally high but defensible" (002), "slightly heavy" (003), and
  "marginally over-proportional" (004). The ceremony that did not pay for itself
  was enumerating several opportunity themes when one was decision-changing —
  worst at the smallest repo.

## Control arm (added 2026-09-29 — the decisive comparison)

Each skill episode's counterfactual was a self-report ("without the skill I would
have captured the first visible problem"). To test that, the same three tasks
were run in **clean, fresh contexts that never loaded the skill** (the prompt
explicitly excluded any skill/SKILL.md/sensemaking material). Records:
`strategic-sensemaking-control-002/003/004.md`. Judged on artifacts
(responsibility chosen, scope avoided), not self-reports.

Pre-registered bar (owner): ratify "keep investing but simplify" only if the
control arm shows the skill changed the outcome in the skill's favor on **at
least two of three**; otherwise the honest verdict is **"simplify hard."**

| Task | Skill arm chose | Control arm chose | Direction |
| --- | --- | --- | --- |
| 002 Pydantic | ESCALATE on ownership/authority; no mutation | Restore verifiability (env mismatch) + request the work queue; incidental `.venv` slip, self-corrected | **Mixed / near-tie** |
| 003 Jellyfin | ESCALATE on the external-maintainer boundary | Bounded, evidence-grounded verification of the hottest recent refactor, with a proposed regression test | **Control-favorable** |
| 004 AION | CHALLENGE the visible milestone; surface the unwired-validation gap | Implement the visible documented milestone (v0.2 schema validation) | **Skill-favorable** |

Read honestly: the skill won the milestone-challenge case (004) and did not
invent scope anywhere; but the control **also avoided scope invention in all
three**, produced a *better* responsibility in 003 (the skill over-escalated
there), and matched the skill in 002. The skill's central claimed benefit —
preventing first-visible-problem capture — materialized in **one of three**,
not the two the bar required. The only other skill-favorable signal is authority
discipline in 002 (the control, not the skill, breached read-only).

## Verdict (ratified by the owner, 2026-09-30)

**Ratified.** Owner decision packet: `artifacts/owner_decision_capsule.md`
(`OWNER-DECISION-SIMPLIFY-001`). The owner selected **Option B (staged program),
authorized for Stage 1 only** (documentation-volume reduction); Stage 2 and
Stage 3 are withheld until Stage 1 passes its suite-green check. RC3 / PyPI /
1.0.0 remain held until the simplification decision completes.

Apply the pre-registered rule: **the control arm did not confirm the skill's
advantage at the ≥2/3 bar**, so the honest verdict is **simplify hard**, not
"keep investing but simplify."

- **Simplify hard.** The doctrine's core ceremony cost (breadth/depth over-
  processing) is real and recurring, while its headline benefit (preventing
  scope-inventing first-visible-problem capture) was demonstrated on 1/3 tasks
  against a control that avoided that failure on its own. Reduce the ceremony
  substantially. The single clearer skill-favorable signal is a secondary one —
  authority-boundary discipline (the control alone mutated) — not the headline
  claim.
- **Do not stop.** There is one genuine skill win (004, milestone inversion) and
  a real authority-discipline signal; and the skill never made an outcome worse
  than the control in the sense of inventing scope.
- **Do not formalize.** Still no stable, mechanically expressible failure
  boundary, and no repeated manual burden a new artifact or policy layer would
  remove (guide sections 13-14).

This revision changes the earlier agent-authored draft verdict. The owner has
since **ratified "simplify hard"** and chosen Option B, Stage 1 only
(`artifacts/owner_decision_capsule.md`).

**Re-measure (3 episodes per arm per task):**
`strategic-sensemaking-remeasure-2026-09-30.md` — reinforces "simplify hard"
(0 clear skill-favorable tasks; below the ≥2/3 bar). The pre-ratification verdict
stands and is not reopened by the added episodes.

## What would change this verdict

- Write-authority episodes showing whether the skill under-builds (excess inquiry
  where a cheap reversible build was warranted) or over-builds would test the
  unmeasured half of the doctrine.
- More episodes on genuinely construction-eligible tasks, not read-only ones.
- A second control arm on a set where the control is likelier to over-act (e.g.
  tasks that look like obvious local fixes), to test whether the skill's
  milestone-capture prevention generalizes beyond AION.

## Program limits recorded

- Read-only only; counterfactuals self-reported; n=3; the treatment and control
  arms were run by the same reviewer's subagents (not an independent lab). These
  limits still apply; the verdict is ratified (2026-09-30) and the remaining
  decisions are tracked in issue #506.
- The control arm 002 agent incidentally created a `.venv` (then removed it) — a
  read-only slip, recorded, and a point in the skill's favor on authority
  discipline rather than against it.
