# Historical Replay Study (synthetic, 2026-10-12)

**Evidence class:** SYNTHETIC. Simulated coding-agent replays of merged historical tasks. Not human-player evidence and not a claim about the game.
**Target:** `ThorStarlord/React_incremental_game_prototype`. Tasks: PR #151 (baseline `767d080`) and PR #162 (baseline `9626f9a`).

## Setup and its limits

- Each arm is a standalone one-commit repository built from `git archive` of the baseline, so the arm's git history contains no future commits.
- Pack arm: the pack from `claude/grounding-pack-phase2` (written from current `main`). Its content postdates both baselines, so it leaks. Measured: 1 of 8 cited paths is missing at `767d080` (`specification/Technical/FeatureCompleteResult.md`). The pack's status wording also describes later state. At `9626f9a`, no cited path is missing, but the wording still postdates the baseline.
- **Isolation failure:** both arms shared one `node_modules` (symlinked). The no-pack T2 agent saw a stack frame pointing into the pack workspace, so a shared Jest/source-map cache crossed the arms. Any later run needs a separate install per arm.
- The filesystem was not isolated from the main clone, so agents could in principle have read future commits. They were instructed not to, and their reports do not show it, but this was not enforced.
- Single run per arm per task. Tasks were fully specified.

## Results (graded by diff against requirements, not against the merged diff)

| Task / arm | Correct vs requirement | Owner questions | Verification | Tool calls (approx) | Notes |
| --- | --- | --- | --- | --- | --- |
| T1 pack | Yes (1.15 -> 0.15 plus regression) | 0 | Focused test pass; broader run found 1 failing test, not checked against baseline | ~19 | Pack used; no decision changed |
| T1 no pack | Yes (same change) | 0 | Focused test pass only | ~12 | n/a |
| T2 pack | Yes (act wrapping; 0 act warnings after; 43 before) | 0 | Tests pass; tsc clean | ~14 | Pack used; no decision changed |
| T2 no pack | Yes; wrapped some calls that did not warn (scope decision, not required) | 0 | Tests pass; act warnings 42 vs 43 before (unexplained, reported as found) | ~13 | n/a |

Diffs were checked directly: T1 both arms changed `public/data/traits.json` and added one test; T2 both arms changed the same two test files with 10 added `act` calls.

## What this shows

- **No measurable difference.** Both arms were correct on both tasks. The pack changed no decision. The pack arm ran slightly more verification and used slightly more calls, but the sample is too small to attribute that to the pack.
- **The tasks could not discriminate.** Both were fully specified and had no owner-decision point, so an agent with or without a pack had nothing to ask. A useful test needs a task where the pack would change the decision (a recorded owner answer that applies), and a task where declining is correct.
- **No declining case was run.** The replay set had none, so the study can't tell caution from productive action, as the critique noted.
- **Leakage and shared-cache contamination are real** and invalidate a clean comparison for these runs.

## Conclusion

Phase 3 is **inconclusive**. Neither arm's correctness differed, and the design can't yet test the pack's hypothesis. The two replays are useful as a harness check, not as evidence for or against the pack. Next step if pursued: a historical task with a recorded owner decision that applies to it, a warranted-decline case, separate installs per arm, and a baseline-only pack.

# Auteur assessment (step 4)

Auteur (`ThorStarlord/auteur`, read-only shallow clone at `cd3d847`) has explicit product intent in `MISSION.md`: named users, in-scope and out-of-scope lists, and owner-confirmed exclusions. Its core documents total about 10.7k words, plus 680 Markdown files (233 in `docs/research/`). Its status is gated on external evidence (`STATUS.md`, issue #310 for the next evidence surface), not on a missing product definition.

Classification against the three outcomes:
1. **Better retrieval of existing knowledge** is the main need. The intent exists but is spread across a large document set.
2. **Missing intent or decision history** is not the main gap: the mission and exclusions are stated. Some decision history may be missing, but that is unverified.
3. **Sufficient knowledge, limits elsewhere** is the best fit: the next step is external product evidence, which no document can supply.

Recommendation: do **not** build a Grounding Pack for Auteur. A pack would duplicate `MISSION.md`. If anything is built, it's a one-page entry index pointing to the mission and status, not a pack.

# Fresh-session usability test (synthetic, 2026-10-12, after PR #166 merged at `2331dd1`)

**Evidence class:** SYNTHETIC. One fresh agent, one onboarding question (how Copy Essence generation works, and what a new Trait effect would require). Read-only. No control arm, so no attribution to the pack is possible.

- **Answered from code, without asking:** the rate function, the per-Copy formula, the files that apply it, and the authority rule for named runtime effects.
- **Questions it still needed a human for:** stacking rule (additive or multiplicative), whether this request is in Campaign One scope at all, whether a new effect should be Copy-only or a permanent player effect, and balance numbers. The pack answered only the balance question ("none set"). The other three were design or scope decisions that no document records.
- **Contradictions it found in the repo:** effect naming calls the multiplier "multiplicative" while the code sums it additively. Design docs say "qualifying" Copies contribute, but the rate counts any Copy at maturity 100 or more. `ESSENCE_GENERATION_BONUS` is documented as current but has no reader. One component shadows a shared constant.
- **Pack coverage:** no entry on the Essence rate or Trait effects. `decisions/` holds two records, so it could not answer the stacking, scope, or target questions.

**Reading:** the pack added little beyond the code for the mechanics. Its value for this task would have been decision records for stacking, scope, and target. Those are missing, and the test shows the code and docs disagree in places. The next useful step is an owner decision on those three questions, recorded as `[owner: date]` lines, rather than more pack content.
