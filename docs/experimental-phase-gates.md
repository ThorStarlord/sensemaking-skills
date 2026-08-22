# Experimental Phase Gates

Reusable methodology for experiments that compare agent execution regimes on
frozen, pre-committed tasks. Distilled from the Autonomous Task v2 series;
see `experiments/evaluation-design-e3-autonomous-task-v2/AUTONOMOUS-TASK-V2-
PROCESS-LEARNINGS.md` for the study-specific retrospective.

Status: REUSABLE GUIDANCE (non-normative for any specific experiment).

## Core idea

Readiness is layered. Passing one gate does not imply the next. In particular,
a design being *frozen* never implies the execution runtime can *instantiate*
it as a measuring instrument. Treat design readiness, construction readiness,
lock readiness, harness readiness, pilot readiness, and main-study readiness as
separate gates, each with its own evidence.

## Gates

### DESIGN READY

- construct defined (what is being measured, precisely).
- falsification conditions defined (what observation would force abandoning a
  claim).
- negative outcomes are allowed outputs, not failures.
- decision rules preregistered (before evidence).

### CONSTRUCTION READY

- real substrate exists (the behavior being measured is actually reachable in
  the repository/source).
- task/oracle contract can be instantiated against real repository state.
- evaluator independence is possible (an independent consumer can reject the
  producer's output).

### LOCK READY

- all candidate content exists and is qualified.
- all semantic commitments are frozen (oracle semantics, not just text).
- all randomization degrees of freedom are specified — including any
  seed→outcome mapping, not merely the seed value.

### LOCKED

- hashes recorded for every normative artifact.
- chronology auditable (e.g., commit-before-select: manifests before
  salts/rankings).
- selection randomness generated only after commitment.
- a mismatch means STOP, never silent recompute of the recorded hash.

### HARNESS READY

- execution environment reproduces the frozen conditions (same SHA, same task
  contract, same regime prompt, same model/config).
- required telemetry is actually observable (measurement capability, not just
  execution capability).
- isolation demonstrated (fresh clone, fresh agent session, no cross-run
  leakage).
- responder/escalation transport works (and the responder is oracle-blind).
- non-evidentiary calibration passes — using a throwaway task that is NOT one
  of the real cells and can never enter the evidence set.

### PILOT READY

- no unresolved instrument defect.
- dispatch order mechanically determined (fully specified seed→shuffle).

### MAIN STUDY READY

- pilot adjudicated according to preregistered rules (valid / family-dropped /
  instrument-invalid / not-admissible).
- family retention/drop rules applied mechanically from frozen mappings.
- selected tasks derived solely from frozen rules (no post-hoc selection).

## Post-lock ambiguity rule

If a frozen instruction admits multiple reasonable implementations that can
change experimental behavior, do not choose one silently.

- If no evidence-bearing run has occurred: resolve it through a transparent
  pre-dispatch addendum that preserves all previously frozen experimental
  choices.
- If evidence already exists: treat the ambiguity as an instrument-validity
  problem rather than retroactively repairing the experiment.

## Execution vs. measurement readiness

Before executing a regime-comparison experiment, answer all three separately:

```
Can the runtime perform the task?
Can the runtime enforce the experimental treatment?
Can the runtime observe every measurement required for adjudication?
```

"Can we spawn agents?" alone is insufficient. If a required measurement is not
observable, that is a harness admissibility finding — never a fabricated
estimate, and never grounds for weakening the measurement to fit the runtime.

## Calibration is non-evidentiary

Harness/runner testing must never consume one of the real experimental cells.
Use a throwaway calibration task and prove:

```
required telemetry populated
agent/evaluator separation holds
fresh state holds (no cross-run leakage)
no ambient leakage occurred
R2/escalation transport calibration works
```

Only then declare the harness ready and unlock the real cells.

## Diminishing-return rule for review

Review within a single layer while new findings can still materially change:
validity, selection, scoring, execution, or interpretation. When remaining
findings are primarily editorial, exercise the next layer instead of adding
another prose review.

Justification for any new check: **What concrete false conclusion could pass
without this check?** If unanswerable, do not add the check.
