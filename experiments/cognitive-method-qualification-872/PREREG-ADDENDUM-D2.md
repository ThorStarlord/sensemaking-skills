# Addendum to PREREGISTRATION.md: D2 reuse episodes

**Status:** preregistered before any D2 subject episode. The commit that adds this file is the chronology record for D2.

## 1. Knowledge snapshot

D2 uses the knowledge store as updated after D1, at commit `15676632` (`knowledge(#872): narrow the safe-mode remedy after calibration C2; record D1 exposure`). The manifest is `manifests/D2.txt`. It includes `stewardship.json`, the cognitive-method record and the C2 calibration record, all at that commit.

The knowledge update was made by the orchestrator after D1 and includes its interpretation of C2. The new lesson is therefore not independent of its author. This is disclosed as a limit.

## 2. Arms

| Arm | Snapshot | Prompt addition | Runner arm name |
| --- | --- | --- | --- |
| Spontaneous treatment | `15676632` | the D1 availability sentence (consult if useful) | `treatment` |
| Instructed treatment | `15676632` | "Before you answer, read it and state which record, if any, you relied on." | `instructed` |
| Baseline | none | none | `baseline` |

- N = 3 per arm: `treatment` T1 to T3, `instructed` I1 to I3, `baseline` B1 to B3.
- The subject task is `prompts/D2.txt`, the rubric is `rubrics/D2-rubric.md` (S1 to S5), and the harness is the calibrated configuration in the main preregistration.
- Subjects are fresh sessions. The prompts do not name the orchestrator, the study author or any prior identity, so no identity or authority is inherited.

**Runner change, disclosed.** `runner/run_child.sh` gained an `instructed` branch. The `treatment` and `baseline` behavior is unchanged, and the D1 streams were produced by the earlier version of the same script.

## 3. Measures, reported separately

- **Exposure:** a Read or Grep on the knowledge directory before the final text, from stream ordering. For the instructed arm this is produced by the instruction, so it is reported as such.
- **Source check:** a Read of `docs/normal-use/2026-11-15-harness-calibration-c2.md` before the final text.
- **Reported use:** S5, which requires a named source and the finding that a safety flag alone let an outside file be read.
- **Configuration:** S1 to S4, which the subject could in principle meet from prior knowledge.

Exposure, source check and reported use are never inferred from one another.

## 4. Decision rules

- The S5 result for the baseline is structurally limited, because the finding is in no source the baseline can read. A baseline S5 of 1 is reported as an anomaly and checked against the transcript, and it is not counted as reuse.
- Reuse is claimed only where the trace shows a source-check read before the final text and S5 is 1.
- The result is reported in each direction, and no effect size is inferred from N = 3.
- The validity rules of the main preregistration apply. An invalid episode is rerun once, and both attempts are reported.

## 5. Claim ceiling

Three episodes per arm, one harness, one model identifier and one CLI version. A positive S5 shows that a fresh agent reported a source-checked finding in the stated configuration. It does not show cognitive benefit, transfer, or independence from the orchestrator who wrote the lesson.
