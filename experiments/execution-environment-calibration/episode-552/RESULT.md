# Episode 552-B result (one subject, non-comparative; corrected after review)

**Run:** `transcripts/ep552-b.jsonl`, sid `6d4b4807-…`, 05:02:43Z to 05:04:03Z. Fresh headless session. Model `claude-haiku-5-5` (the CLI printed `unrecognized_model` for this model; the served model is not independently verified). Claude Code 2.1.266. Cost $0.35. 15 tool calls. Exit 0, within the budget and timeout.

**Sandbox.** This episode ran on the attempt-5 **full-clone** sandbox at the pinned revision `b7ce9e69`. That sandbox exposed tags and commits beyond the pin (PREREG-AMENDMENT-5, 2a). The subject made **no `.git` reads** (verified: `grep` count 0 in the transcript). Its citations are therefore not affected by the beyond-pin exposure. The episode was **not rerun** on the corrected sandbox, because that would generate new evidence (PREREG-AMENDMENT-5, section 4).

**Network canary.** Not running during this episode. The subject's init tool list showed no Bash, WebFetch or WebSearch. The record's `net_hits: 0` is **not instrument-verified** and should be read as "not recorded".

**Prompt topic.** The episode prompt (`prompt.tmpl`) named the topic family ("source staleness") and pointed to ADR 0031 and `STATUS.md`. The subject's first reads followed that framing. Its choice of responsibility was not made from an open survey, so the source reads are not evidence of subject-initiated method use.

**Objective checks.** `results/ep552-b.check.json`, computed by `scripts/episode_check.py` from the transcript. The check runs before the orchestrator's judgement is recorded. The summary JSON already contains the report text, so the ordering is not independently proven.

## Objective checks (PREREG-EPISODE-552.md section 3)

| Measure | Result |
| --- | --- |
| 1. Knowledge calls before the final report | 1 `knowledge_query` search for "stale source span", made at call 11 of 15, after the subject had already identified the gap in its own text. It returned **0 claims**. |
| 2. Source reads before the final report | The script counts `Read` and `git_show_file`: **5 `Read` calls** (STATUS.md, ADR 0031, the plan, `knowledge_store.py`, `knowledge_sources.py`). Eight `Grep` calls, including over the tests, and one `Glob` call were not counted. Preregistered measure 2 (files the store cites) was **approximated**, not computed. |
| 3. Claim ids cited and present at the pin | **None cited.** The check reports false only because the set is empty. |
| 4. Commit cited and present | `b7ce9e69` present. |
| 4. Paths cited and present | 6 of 8 present. **2 failed:** `knowledge.py` and `knowledge_architecture.py`, cited by basename. Both exist at `src/sensemaking_skills/semantic_architecture/`. This is a path-form error, not a fabricated file. |
| Verdict token | `CHANGE_RECOMMENDED`. |

## Orchestrator verification of the verdict (non-blinded)

The claimed behaviour is real, and it is documented as intended.

- `audit_knowledge_sources` (`knowledge_store.py:630` to `691`) reports `source_changed` for every record whose cited file changed, because `_source_hashes` (`knowledge_sources.py:167`) hashes the whole file.
- The function's docstring says a changed byte "means evidence should be re-examined". Its explicit limits say "Changed source evidence requires inspection, not automatic invalidation" (`knowledge_store.py:762` to `766`).
- `docs/semantic-architecture/persistent-knowledge-cli.md:708` describes `knowledge-audit` as "intentionally conservative".
- The plan lists "stale source spans" as a detection (`docs/persistent-semantic-stewardship-plan.md:251`). Its verification, "a deliberately stale source link" (`:257`), is **already satisfied**: `tests/test_semantic_knowledge.py:393` to `400` changes a cited file and asserts `source_changed >= 2` and that `component:replay` appears in `affected_records`.

**Engineering classification: CANDIDATE_IMPROVEMENT, not DEFECT.** A per-line status would improve precision, following the existing `authored_record_audit` pattern (`knowledge_store.py:747`). Per-record classification already exists (`docs/semantic-architecture/persistent-knowledge-cli.md`, around lines 704 to 708, from PR #561), so the candidate is a per-line refinement of that, not a new capability. It would need separate evaluation: it changes the audit's output schema and needs its own tests. The report's own over-approximation note (moved lines would read as `text_differs`) is accurate. The report did not read the existing tests, so their effect on the proposal is not assessed here.

**Verdict:** the recommendation is source-grounded and bounded. It was not implemented, tested or pushed.

## What this episode does and does not show

- **Predecision retrieval did not occur in the preregistered sense.** The subject identified the gap from source reads (after call 9, its text said that "a span-level staleness check would be a gap"), and only then queried the knowledge store (call 11). The query returned nothing, and the report uses no claim id. Measure 1 is therefore not met.
- **Method influence was not observed.** Under the preregistered rule (PREREG-EPISODE-552.md section 4), no method-learning outcome follows: measure 1 is not met and measure 3 failed.
- **Source checking occurred** before the verdict: five `Read` calls, plus Greps. Their order and the topic framing are described above.
- **Citation integrity partly failed:** two basename paths.
- **Counterevidence:** the report names what it did not verify and a limit of its own proposal. That is not counterevidence to a recorded lesson. The #872 requirement "counterevidence elicited" stays unmet.
- **Method reuse, outcome support and comparative benefit: not observed.** One episode, one subject, no baseline, and no outcome measured beyond source checks.

## Against #872 and #874

- #872 requires an encounter that changes a consequential method choice, applied adaptation or rejection of a recorded lesson, counterevidence elicited, outcome support, a repeat sample and comparative benefit. None of these is met by this episode. **#872 stays open.**
- #874 needs a precommitted task family, a matched comparator and refuting conditions. **Not ready.**
