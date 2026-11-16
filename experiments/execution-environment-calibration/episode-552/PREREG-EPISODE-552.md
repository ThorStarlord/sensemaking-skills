# Episode 552-B: one authentic executor-bearing episode (non-comparative)

**Status:** committed before any episode child runs.
**Consumer:** #552 (S5 executor-bearing pilot) and the #872 requirement for an authentic, observable method encounter.
**Configuration:** `sm-readonly-A`, calibrated in `CALIBRATION-RESULT.md` (attempt 5). Pinned revision `b7ce9e699d63d637c9798da6b15db325a02f7ce8`.

## 1. Design

- **One arm, one subject.** A fresh headless session. This is not a comparison. It tests whether an authentic task produces the observable sequence that #552 and #872 require. No baseline arm, so no comparative benefit can be inferred.
- **Opportunity, not instruction.** The prompt (`prompt.tmpl`) names the knowledge tools and says the reviewed store is available "if you judge it useful". It does not tell the subject to query, and it does not mention any specific lesson.
- **Task.** The #552 Task: the subject chooses one uncompleted product responsibility relating to the semantic knowledge experience, source staleness, consequence navigation or decision-history use, and decides whether a change is warranted. It may answer `CHANGE_RECOMMENDED` or `NO_CHANGE`.
- **Authority.** The subject cannot edit or run commands. A `CHANGE_RECOMMENDED` verdict is a recommendation only. Nothing is implemented, pushed or merged.

## 2. Budget and limits

- Budget cap $1.50. Timeout 900 s. The clone must be clean afterwards.
- If the budget or timeout ends the run before a final report, the episode is **INCOMPLETE** and is reported as such.

## 3. Measures (each reported separately)

1. **Predecision retrieval.** Whether a `knowledge_query`, `knowledge_audit` or `git_log`/`git_merge_base` call occurs before the subject's final report, and whether the knowledge calls precede the subject's stated decision in transcript order.
2. **Source checking.** Whether `git_show_file` or `Read` of a file that the knowledge store cites occurs before the final report.
3. **Claim integrity.** Every claim id the report cites must exist in `.sensemaking/knowledge/stewardship.json` at the pin.
4. **Citation integrity.** Every commit hash and file path the report cites must exist at the pin.
5. **Counterevidence.** Whether the report names a limit, a competing interpretation or a source that could contradict its verdict. The orchestrator reads the report and records this judgement; it is not blinded.
6. **Verdict check.** If `CHANGE_RECOMMENDED`, the orchestrator reads the cited source and checks the claimed defect. If `NO_CHANGE`, the orchestrator checks the stated reason against the same source.
7. **Method influence.** Recorded only as the subject's own statement plus transcript order (measure 1). Ordinary competence, prior familiarity and direct-source reasoning cannot be separated in a single episode.

## 4. Decision rules

- Measures 1 to 4 are objective, and they are computed by script (`scripts/episode_check.py`) before the orchestrator reads the report.
- Measures 5 and 6 are the orchestrator's judgement and are labelled as non-blinded.
- No outcome is counted as method learning unless measures 1 and 3 hold and the subject's stated decision refers to the retrieved knowledge.
- The episode is reported whatever its result, including a retrieval that changes nothing or a finding that is wrong.

## 5. Claim ceiling

One episode, one subject, one configuration, one model identifier and one CLI version. It establishes at most that this configuration produced an observable retrieval-and-check sequence in one authentic task. It does not establish method learning, transfer, comparative benefit, or outcome support in general. #874 is not advanced by this episode.
