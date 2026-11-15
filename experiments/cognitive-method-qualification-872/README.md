# Cognitive-method qualification episodes (#872 under the harness of #873)

Independent-episode qualification for methodological lessons (#861, #862 original requirements), run under the harness configuration that the calibration in `docs/normal-use/2026-11-15-harness-calibration-c2.md` tested.

- `PREREGISTRATION.md`: the question, frozen harness, arms, task, rubric, validity rules and decision rules. Committed before any subject episode.
- `prompts/`: subject task texts (D1, D2).
- `rubrics/`: blind evaluation criteria.
- `manifests/`: which repository files form the knowledge snapshot for each task.
- `runner/`: `run_child.sh` (subject episode), `run_eval.sh` and `evaluate_blind.sh` (blind evaluation), and `score.py` (summaries, blinding, collection, unblinding).
- `calibration/`: C3 planted evaluator inputs and expected vectors. C2 transcripts are in `calibration/C2-transcripts/`.
- `transcripts/`: raw stream-json for every subject and evaluator session, and `index.txt` with session ids.
- `results/`: summaries, blind scores and unblinded scores.

The runner needs `SCRATCH` set to a directory outside the repository. Fixtures are built there.

Claim ceiling: these episodes test whether a fresh agent encounters, source-checks and reuses a lesson. They do not measure cognitive benefit, and they are not a comparison (#874).
