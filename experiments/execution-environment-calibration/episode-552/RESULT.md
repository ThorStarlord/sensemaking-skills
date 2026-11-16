# Episode 552-B result (one subject, non-comparative)

**Run:** `transcripts/ep552-b.jsonl` (fresh headless session, sandbox at the pinned revision `b7ce9e69`), model `claude-haiku-5-5`, Claude Code 2.1.266, cost $0.35, 15 tool calls, exit 0, within the budget and timeout.
**Objective checks:** `results/ep552-b.check.json` (computed by `scripts/episode_check.py` before the orchestrator read the report's content). **Orchestrator judgement** is labelled and is not blinded.
**Network canary:** not running during this episode (it was stopped at the end of the battery). The subject's tool list was rechecked (no Bash, WebFetch or WebSearch), but the net-hit count is **not instrument-verified** for this run.

## Objective checks (PREREG-EPISODE-552.md section 3)

| Measure | Result |
| --- | --- |
| 1. Knowledge calls before the final report | 1 (`knowledge_query` search for "stale source span", returned **0 claims**) |
| 2. Source reads before the final report | 5 (Read and Grep of ADR 0031, the plan, `knowledge_store.py`, `knowledge_sources.py`, tests) |
| 3. Claim ids cited and present at the pin | **None cited**. The check reports false only because the set is empty |
| 4. Commit cited and present | `b7ce9e69…` present |
| 4. Paths cited and present | 6 of 8 present. **2 failed:** `knowledge.py` and `knowledge_architecture.py` were cited by basename. Both exist at `src/sensemaking_skills/semantic_architecture/` |
| Verdict tokens | `CHANGE_RECOMMENDED` |

## Orchestrator verification of the verdict (non-blinded)

The claimed defect is real. `audit_knowledge_sources` (`knowledge_store.py:630` to `691`) reports `source_changed` for any record whose cited file changed. `_source_hashes` resolves a `file:<path>:line:<N>` reference to the whole file, which is what the report says. The plan (`docs/persistent-semantic-stewardship-plan.md:251`, `257`) lists "stale source spans" and "a deliberately stale source link" as required detections, and the report quotes this accurately. The proposed bounded change is a per-record line-text comparison. The report states its over-approximation (moved lines read as `text_differs`). Existing tests assert `source_changed` counts (`tests/test_semantic_knowledge.py:390` to `429`). The report did not read them, so the recommendation's effect on them is not assessed here.

**Verdict:** CHANGE_RECOMMENDED is source-grounded and bounded. It was not implemented, and nothing was tested or pushed.

## What this episode does and does not show

- **Predecision retrieval occurred** (1 call), **but it returned nothing**. The report says so and does not use any claim id. The decision rests on direct source reads, so **recorded knowledge did not change the decision**.
- **Source checking occurred** before the verdict (5 reads).
- **Citation integrity partly failed:** two basename paths. This is a path-form error, not a fabricated file.
- **Counterevidence:** the report names what it did not verify and one over-approximation of its own proposal.
- **Method reuse, outcome support and comparative benefit: not observed.** One episode, one subject, no baseline, no outcome measured beyond source checks.

## Against #872 and #874

- #872 requires an encounter that changes a consequential method choice, applied adaptation or rejection of a recorded lesson, counterevidence elicited, outcome support, a repeat sample and comparative benefit. Only the first is partly met (retrieval before the decision), and it did not change the decision. **#872 stays open.**
- #874 needs a precommitted task family, a matched comparator and refuting conditions. **Not ready.**
