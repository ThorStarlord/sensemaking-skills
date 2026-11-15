# D1 result summary (method choice, N = 3 per arm)

**Preregistration:** `PREREGISTRATION.md`, committed at `77f74be9`, before any subject episode.
**Snapshot:** knowledge at `d68b8513` (origin/main at the start of this work).
**Harness:** `runner/run_child.sh`, `--safe-mode --restricted`, tools `Read,Grep,Glob`, `claude-haiku-5-5`, Claude Code 2.1.266.
**Scoring:** each response relabelled with seed 20261115 and scored by a separate evaluator session. The label key was joined only after scoring.
**Raw data:** `transcripts/D1-*.jsonl` (subjects), `transcripts/eval-D1-D1-R*.jsonl` (evaluators), `results/summaries/D1-*.json`, `results/D1-D1-scores.json`.

## Validity

All six episodes were valid on the first attempt, so no rerun was needed. Each init record showed 16 bundled built-in skills, no user or plugin skills, no MCP servers, the tools allowlist, and no memory path. Each run completed in one turn.

## Results by arm

| Criterion | Treatment (T1 to T3) | Baseline (B1 to B3) |
| --- | --- | --- |
| K1 CHOICE_B | 3 of 3 | 3 of 3 |
| K2 AMBIENT_IDENTIFIED | 3 of 3 | 3 of 3 |
| K3 INSTRUCTION_MEMORY_SKILL_CONTROL | 3 of 3 | 3 of 3 |
| K4 READ_CONFINEMENT (borderline, see below) | 1 of 3 | 2 of 3 |
| K5 CHECKABLE_FALSIFIER | 3 of 3 | 3 of 3 |
| Read or Grep tool call on the knowledge directory | **0 of 3** | not applicable |

## What this shows, and what it does not

1. **Exposure without retrieval.** None of the three treatment subjects opened the knowledge directory, although the prompt named it and offered it for use. The stream has zero tool calls in all six episodes. The treatment therefore has no predecision encounter to report. #872's first requirement, encounter before the choice, is not met by this design.
2. **The task does not discriminate.** Every response chose B and identified ambient inheritance, and each one named flags such as `CLAUDE_CONFIG_DIR`, `--disable-slash-commands`, `--strict-mcp-config` and `--setting-sources`. The fixed-method baseline already has this knowledge. D1 cannot show whether the lesson changes a method choice, because the arms reach the same answer without it. This is a property of the task, and it is not a claim about the lesson.
3. **K4 is the weakest criterion.** The evaluator accepted `--add-dir` as an explicit read-scope control (B1, B3, and T2 with its `permissions.deny` note). That follows the rubric's wording, but these responses do not describe confinement in the sense the C2 finding requires. The criterion is reported as recorded, not interpreted.
4. **No applied-use or outcome measure exists in D1.** Applied use is the choice, which is at ceiling. Outcome support would need a returned task outcome, and D1 has none.

## Consequence for the preregistered rule

The #873 rule is satisfied: C2 and C3 passed, and every D1 episode was valid. The harness disposition is therefore HARNESS_READY for this configuration. D1's content result is reported as non-discriminating, with exposure 0 of 3 in the treatment arm.

D2 is designed differently. Its discriminating content is the C2 file-read finding, which no baseline subject can know from prior knowledge. Its arms add an instructed-exposure condition, so that exposure and use are measured separately. D2 is preregistered in an addendum before any D2 run.

## Claim ceiling

Three episodes per arm, in one harness, one model identifier and one CLI version. No cognitive benefit, no independent re-entry, and no comparison is established.
