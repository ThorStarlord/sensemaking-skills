# Experiment ledger

| Run  | Mode         | Executor      | Classification              | Counts as live/product proof? |
|------|--------------|---------------|------------------------------|--------------------------------|
| 0001 | plan_only    | dry-run       | protocol calibration — non-executing dry run | NO |
| 0002 | guided_execution | claude-code (live) | live attempt — Step 1 (repo-sensemaker) executed live but failed validation in both positive and negative attempts; Step 2 never reached | STEP 1 FAILED — real live skill invocation, but no golden-path proof (see `runs/0002-live-golden-path-proof.md`) |

Run 0001 is not present in this worktree (committed on a different agent's
branch) and is recorded here from context only, not fabricated detail. It
invoked no skills (`plan_only` + dry-run), so it does not count as live proof,
golden-path proof, product evidence, or evidence for ADR 0018/0021.

Run 0002's classification and result are recorded in
`runs/0002-live-golden-path-proof.md` and the Phase 8 verdict of the task that
produced it.
