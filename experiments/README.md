# Experiments

This directory records protocol calibration and evidentiary runs of the
sensemaking-skills orchestration runtime (`scripts/workflow-runtime.py`).

Not every run in this directory is product evidence. See `ledger.md` for the
classification of each run (protocol calibration vs. live golden-path proof)
and `hypotheses.md` for what each run was trying to establish.

## Note on run 0001

A prior calibration run (0001) is known to exist, committed on a different
agent's isolated branch, and is not necessarily present in this worktree. Per
the task that created this directory, its content is not fabricated here.
Based on available context: run 0001 used `--mode plan_only` with a
`dry-run`/deterministic executor, and therefore invoked no skills. It is
protocol calibration only (confirms the CLI accepts a given invocation shape)
and must NOT be counted as live proof, golden-path proof, product evidence,
or evidence for ADR 0018/0021.

This ledger starts its authoritative record at run 0002.
