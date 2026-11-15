# Preregistration: method-choice episodes for #872 under the calibrated harness (#873)

**Status:** preregistered before any D1 subject episode. The commit that adds this file is the chronology record. Each later result cites that commit.

## 1. Question

Does a reviewed, source-checkable methodological lesson, made available to a fresh agent before a consequential method choice, change the method the agent chooses? Does a later fresh agent reuse the lesson after checking its source?

These are narrow behavioral questions. They are not cognitive benefit (#874), and they are not a claim about the study's wider effect or transfer.

## 2. Harness (frozen)

The calibration is in `docs/normal-use/2026-11-15-harness-calibration-c2.md` (C2, C3). Every subject episode uses `runner/run_child.sh`, which fixes:

- `claude -p --session-id <fresh> --safe-mode --restricted --model claude-haiku-5-5 --output-format stream-json --verbose --max-budget-usd 0.40`
- tools `Read,Grep,Glob`, passed as both `--tools` and `--allowedTools`
- a fresh empty working directory per episode, with no resume
- an environment wrapper that removes inherited `CLAUDE*` and `ANTHROPIC*` variables, except `ANTHROPIC_BASE_URL`

The arms differ in exactly two places: the treatment arm has `--add-dir` pointing at a knowledge snapshot taken from git with the manifest, and its prompt has one availability sentence. Nothing else differs.

## 3. Arms

- **Treatment (experience available):** the reviewed knowledge snapshot in `manifests/D1.txt`, at `d68b8513`. This snapshot is the knowledge as it stood before this study. It does not contain the C2 finding.
- **Baseline (fixed method):** no knowledge directory and no availability sentence.

Both arms run the same prompt, `prompts/D1.txt`.

## 4. Subject task D1 (method choice)

Full text: `prompts/D1.txt`. Subjects choose among three options for running two arms as isolated agent contexts: A (Agent-tool subagents), B (separate headless processes), C (one interactive session reused). They then state isolation, controls, contamination and a falsifier.

## 5. Evaluation (blind)

Rubric: `rubrics/D1-rubric.md`, criteria K1 to K5.

- K1 CHOICE_B: the choice is B.
- K2 AMBIENT_IDENTIFIED: the response says A or C lets an arm inherit ambient context.
- K3 INSTRUCTION_MEMORY_SKILL_CONTROL: for B, a named setting that excludes instructions, memory and Skills, with the exclusion stated.
- K4 READ_CONFINEMENT: a named mechanism confining reads, treated as a separate requirement. The current knowledge snapshot does not contain the C2 finding, so this criterion is expected to be low in both arms. The expectation is recorded here, before any run, so the result is not reinterpreted afterwards.
- K5 CHECKABLE_FALSIFIER: a named observable that a reviewer could check.

Each subject response is relabelled R1 to Rn in a seeded random order. The key is held in the scratch directory, outside the repository. Each response is scored in a separate evaluator session (`runner/run_eval.sh`, no tools, same safe and restricted flags). The key is joined to arms only after scoring.

## 6. Design and decision rules

- N = 3 per arm for D1, so 6 subject episodes: `T1`–`T3` (treatment) and `B1`–`B3` (baseline).
- Primary descriptive measures, reported by arm: K1 (choice B) and K2 (ambient identified).
- Exposure measure, reported separately: whether the treatment subject issued a Read on the knowledge directory before its final text. This comes from the stream ordering in `results/summaries/`. Exposure is not applied use.
- Applied use is K1 and K2 by arm. Outcome support is not measured in D1, because D1 has no returned task outcome.
- N = 3 cannot establish an effect. A difference or a lack of one is reported as observed, with no inferred effect size.

**Validity rules, fixed before the run:**

- An episode is INVALID if its stream lacks an init or result record, if its init record shows MCP servers or user skills, or if its exit code indicates a configuration error. An invalid episode is rerun once, and both attempts are reported.
- A treatment episode that never reads the knowledge directory is reported as exposure without retrieval.

**#873 disposition rule, fixed before the run:** #873 moves to HARNESS READY for this configuration if C2 and C3 pass (they do) and every D1 episode is valid after at most one rerun. Otherwise #873 stays NOT_ADMISSIBLE, and the reason is recorded.

## 7. Limits

- The orchestrator wrote this preregistration and the rubric, and it knows the expected outcome. The evaluator is blind to arms and holds no treatment information.
- The subjects are Haiku 5.5 in a single harness. The task is a method-choice prompt, not engineering work.
- The model identifier warning in C2 applies to every run.

## 8. D2 (reuse)

D2 (`prompts/D2.txt`, `rubrics/D2-rubric.md`) is not preregistered here. It will be preregistered in a dated addendum committed before any D2 run. D2 will use knowledge updated after D1, and that update is itself a separate commit.
