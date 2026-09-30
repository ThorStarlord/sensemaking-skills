# Strategic Sensemaking trial program — cross-episode review and verdict

Section 12 review over `strategic-sensemaking-trial-002/003/004.md` (read-only
episodes on Pydantic, Jellyfin, and AION Workflow Core), 2026-09-29.

**This is an agent recommendation, not a ratified decision.** The investment
verdict is owner-reserved (issue #497). Per the guide section 14, this is not a
score, benchmark, or control/treatment study.

## Claim ceiling (read this before the verdict)

- **Single arm.** No episode ran a without-skill control. The "what would you
  have done without the skill" field is each subagent's own low-confidence
  guess, not measured counterfactual behavior.
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
  (a TODO, a coverage bump, the README roadmap milestone). All three
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

## Verdict (recommendation to the owner)

The evidence supports **keep investing, but simplify** rather than "simplify
only" or "stop":

- **Keep investing.** In 3/3 read-only episodes the control layer changed the
  selected responsibility away from scope-inventing implementation and toward the
  correct blocking question (owner/authority, external boundary, or a
  presupposed capability). That is the specific failure the skill exists to
  prevent, and it recurred across three very different repositories.
- **Simplify (do not add).** The one recurring cost is disproportionate breadth
  enumeration. The warranted change is emphasis, not machinery: scale
  breadth/depth to repository size and stop enumerating opportunity themes once
  the frame is stable. Consistent with the guide's own "lightest surface that can
  change the decision."
- **Do not stop, and do not formalize.** There is no stable, mechanically
  expressible failure boundary yet, and no repeated manual burden that a new
  artifact or policy layer would remove. Adding one now would violate the guide's
  escalation rule (section 13) and its non-goals (section 14).

## What would change this verdict

- A control arm showing agents reach the same responsibility without the skill
  would weaken the "keep investing" half.
- Write-authority episodes showing the skill either under-builds (excess inquiry
  where a cheap reversible build was warranted) or over-builds would test the
  unmeasured half of the doctrine.
- More episodes on genuinely construction-eligible tasks, not read-only ones.

## Program limits recorded

- Read-only only; counterfactuals self-reported; n=3; reviewer not independent
  of the skill's design. These bound the verdict to "recommendation," which is
  why the investment decision remains owner-reserved in issue #497.
