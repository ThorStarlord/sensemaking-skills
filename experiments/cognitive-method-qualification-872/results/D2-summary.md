# D2 result summary (configuration task, reuse of the calibrated finding, N = 3 per arm)

**Preregistration:** `PREREGISTRATION.md` (commit `77f74be9`) and `PREREG-ADDENDUM-D2.md` (commit `06417c4c`), committed before any D2 subject episode.
**Knowledge snapshot for the treatment arms:** commit `15676632`, after the calibration-driven update.
**Harness:** `runner/run_child.sh`, `--safe-mode --restricted`, tools `Read,Grep,Glob`, `claude-haiku-5-5`, Claude Code 2.1.266.
**Scoring:** blind relabelling with seed 20261116, one separate evaluator session per response, key joined after scoring.
**Raw data:** `transcripts/D2-*.jsonl`, `transcripts/eval-D2-D2-R*.jsonl`, `results/summaries/D2-*.json`, `results/D2-D2-scores.json`.

## Validity

All nine episodes were valid on the first attempt. Each had a successful result, 16 bundled built-in skills, no MCP servers, and the tools allowlist. Restricted mode refused eight out-of-directory calls, all in baseline episodes and in T2, and those refusals are part of the recorded trace. No episode needed a rerun.

## Results by arm

| Criterion | Spontaneous treatment (T1 to T3) | Instructed treatment (I1 to I3) | Baseline (B1 to B3) |
| --- | --- | --- | --- |
| S1 SAFE_MODE | 3 of 3 | 3 of 3 | 3 of 3 |
| S2 READ_CONFINEMENT (borderline, see below) | 1 of 3 | 3 of 3 | 1 of 3 |
| S3 TOOL_ALLOWLIST | 3 of 3 | 3 of 3 | 3 of 3 |
| S4 RESIDUAL_NAMED | 3 of 3 | 3 of 3 | 3 of 3 |
| S5 SOURCE_CHECKED_FINDING | 1 of 3 | 3 of 3 | 0 of 3 |
| Calibration record content read before the final text | 1 of 3 (T1) | 3 of 3 | not possible (no access) |

Exposure, separately from the content read:

- **T1:** read the knowledge store and the calibration record before answering, and that record content is the source of its S5 statement.
- **T2:** listed the knowledge directory by file name, which shows that the names were visible. It read no content and did not make an S5 statement.
- **T3:** never touched the knowledge directory.

## What this shows, and what it does not

1. **The calibrated finding is reused, but only where it was read.** Every S5 = 1 response read the calibration record content before answering, and every response that did not read it scored 0 on S5. The four reuse cases (T1, I1, I2, I3) state the finding in their own words, for example "`--safe-mode` alone let `Read` open a file outside the working directory" (I2) and "X10a showed `--safe-mode` alone read a file outside cwd" (I1). The baseline cannot reach the finding, and it scored 0 as expected.
2. **Spontaneous retrieval was low.** One of three spontaneous treatment subjects read the content, one listed the names, and one did not look. The instructed arm read the content in three of three episodes, but that is produced by the instruction, so it measures use after exposure, not spontaneous encounter.
3. **S2 is borderline.** Baseline B3's S2 = 1 rests on the phrase "Read is scoped to the working directory", which the evaluator accepted as read confinement. Its other flags do not show a named mechanism, and the baseline had no access to the finding. The S2 result is reported as recorded, not interpreted.
4. **S5 is the discriminating criterion.** It requires a named source and the specific finding. It is the criterion the baseline cannot meet, so a baseline result of 0 is expected and carries no evidential weight.

## Information-channel check

Restricted mode worked as designed. Glob, Grep and Read calls outside each episode's cwd or add-dir were refused in the four episodes that attempted them (B1, B2, B3 and T2), and the refusal messages named the outside directory. Those messages show that the study's scratch folder exists, but they expose no file contents. A baseline subject never read a file that belonged to another arm.

## What the reuse does not show

- **Outcome support:** D2 does not measure a returned task outcome. The rubric scores what the subject reported, not whether the chosen configuration performed as claimed in a run.
- **Comparative benefit:** not measured, and not claimed. N = 3 per arm cannot support an effect estimate, and the arms differ in exposure by design.
- **Independence from the orchestrator:** the subjects are fresh sessions with no orchestrator identity in their prompts. The lesson and its narrowing were written by the orchestrator after D1, which is a limit on the reuse claim, and it is disclosed in the addendum.
- **Counterevidence:** the prompts did not ask for counterevidence, so the subjects did not consider it. #872's bullet on counterevidence stays open.

## Claim ceiling

Three episodes per arm, one harness, one model identifier, and one CLI version. The result supports a bounded statement: in this configuration, a fresh agent that reads a source-checked calibration record reports its finding and applies it, and a fresh agent that does not read the record cannot. It does not support any statement about cognitive benefit.
