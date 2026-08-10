# Round 2 — targeted revision verification (2026-08-10)

Per explicit owner instruction: three narrow revisions applied (drop `discovery_confidence`; clarify `uncertainty.source`'s `repository_evidence`/`empirical` discriminant; revise `architectural-review` Boundary Rule 6 to remove the Section 6/15 scoping ambiguity). No packaging change, no new fields, no new validators, no new governance mechanisms, no ADR promotion, no merge. Full diff: commit `c09faef`. Only Cases 3, 4, and 5 rerun — not the full six-case round.

## Case 3 rerun — `repository_evidence` vs. `empirical`, clarified

**Before**: classified the target question (`repository_evidence`) correctly, but reasoning was an implicit judgment call — defensible, but not traceable to any explicit rule text, and structurally similar to Case 1's question (classified `empirical`) with no stated discriminant explaining the difference.

**After**: same classification (`repository_evidence`) — this was never actually the wrong answer, so it should not have changed. What changed is *how it got there*: the subagent explicitly quoted SKILL.md's new discriminant text verbatim, including the worked example ("'Has this ever caused a real failure in production' is `repository_evidence` if run logs/traces already exist to search... `empirical` if nothing has ever been run") and applied it directly to the brief's own Section 7 language ("no search... has been performed" — an unperformed *lookup*, not an unperformed *experiment*).

**Consequence**: the apparent Case-1-vs-Case-3 inconsistency dissolves under the clarified rule rather than being patched over. Case 1's question ("does the script still execute") requires a *new* execution — nothing existing can answer it — genuinely `empirical` under the same rule. Case 3's question ("has this drift ever caused a failure") requires searching records that may already exist from past runs — genuinely `repository_evidence`. They were never in conflict once the real discriminant (existing vs. new evidence) replaces the surface-level "has/does X" tense that made them look alike. The rerun did not need to produce a *different* answer to count as success — it needed to produce the *same* answer for a *citable* reason, which it did.

## Case 4 rerun — `discovery_confidence` removal, behavior check

See `case4-round2-output.md` for the full subagent transcript.

**On the narrow question asked** ("does removing `discovery_confidence` cost anything?"): no — its absence is a complete non-event in this run's reasoning, exactly as round 1 predicted.

**But honestly reported, not smoothed over: the verdict itself changed**, from `pursue_narrowed` (round 1) to `pursue` (round 2) — driven by the separately-revised Boundary Rule 6, not by the field removal. Round 2's subagent judged that fixing one of three unranked candidates "bypasses" the ranking question rather than partially resolving it, landing in the revised rule's "unrelated, disclose but don't narrow" branch instead of its "partial cut, narrow" branch. This is a harder case than Case 5 (no explicit relatedness disclaimer in the brief text to lean on), and the subagent's reasoning was coherent and well-compensated (explicit flags that candidate (b) has stronger urgency evidence than (a) and risks silent deprioritization) — but it is a real, substantive verdict change on identical proposal content, and is reported as such rather than folded into "no regression."

## Case 5 rerun — Boundary Rule 6, unambiguous verdict

See `case5-round2-output.md` for the full subagent transcript. Directly asked, the subagent answered without hedging: "No — one clear path, not multiple defensible readings" — round 1's specific finding (two equally-faithful readings of one rule producing different verdicts on identical input) does not reproduce here. It also self-reported an honest limit: this case was easy partly because the brief's own text explicitly disclaimed relatedness; a brief without that disclaimer (like Case 4's rerun, encountered in this same round) still requires real judgment. The revision fixed the specific textual ambiguity it targeted, not the general need for judgment in harder cases.

## Summary

| Case | Narrow question asked | Answer | Notable side effect |
|---|---|---|---|
| 3 | Does the clarified repository_evidence/empirical rule explain the original inconsistency? | Yes — same classification, now traceable to explicit, quoted rule text instead of an implicit call | None |
| 4 | Does dropping discovery_confidence cost any behavior? | No — complete non-event | Verdict changed (`pursue_narrowed` → `pursue`), caused by the Boundary Rule 6 revision, not the field drop — reported plainly, not hidden |
| 5 | Does the Boundary Rule 6 revision remove the specific ambiguity found? | Yes — explicitly confirmed, no competing reading found | Subagent self-reported this case was easy partly due to an explicit disclaimer in the brief; harder cases (like 4) still need judgment |

No case failed outright. No further architecture change made in response to these results, per the owner's explicit instruction to report and stop rather than expand further.
