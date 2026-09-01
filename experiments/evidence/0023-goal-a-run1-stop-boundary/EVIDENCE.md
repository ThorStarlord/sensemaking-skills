# Evidence 0023 — Goal A / A1 Run-1 Stop Boundary (HARNESS_ENVIRONMENT_FAILURE)

**Status:** durable evidence record. Does not grant any episode execution
authorization on its own (Goal A execution requires a separate, fresh owner
authorization per `docs/research/goal-a-external-product-validation-protocol.md` §1).

## Purpose

Make durable the Goal A Run-1 stop boundary that was previously captured only in
local/untracked files. Per PR-reviewer disposition, concerns:
`docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` cited this
evidence as if it were repository evidence; it was not committed. This entry
gives that evidence a durable provenance chain and a live tracker issue.

## Provenance now on `main`

The four source files are committed under this evidence folder (byte-identical to
the prior local copies):

| file | SHA-256 |
|---|---|
| RUN1-STOP-BOUNDARY.md | `cc493eab60ba89dc9cd0942687334691200349ddebd5fa60fd898b6893d756b3` |
| PRE-RUN-PACKET.md | `afa498f1dd776d502945157aef79e5e28ba41b439d335ac246972e11b633f380` |
| GOAL-A-HARNESS-QUALIFICATION.md | `85ae2dffb89c39427a4aa99f835f7377411ef0c359e7bcdbeb4b47b842eb01bc` |
| GOAL-A-HARNESS-V3-QUALIFICATION.md | `5e076013ed2cec0a461ce9d622d0a936bbf30a752c8074686383a631d7af14c6` |

The prior untracked copies under `experiments/goal-a-auteur-target1/` remain
untracked and are superseded for citation purposes by these committed bytes.

## Substrate reality this preserves (beyond the Run-1 stop)

The Run-1 note (`RUN1-STOP-BOUNDARY.md`) records the immediate
`HARNESS_ENVIRONMENT_FAILURE`. The two harness-qualification files in this folder
record that the producer-write blocker is **one of three falsified execution
substrates** in this environment:

1. isolated task sub-agent, direct file write — **blocked** (Run 1; write dispatch
   did not grant the target, and a canary write was also blocked);
2. isolated task sub-agent, framed return — **`FRAMED_RETURN_NOT_LOSSLESS`** (the
   producer's final answer is not exposed as a clean hashable blob by the tool
   envelope; `LOSSLESS_ARTIFACT_CAPTURE_UNAVAILABLE`);
3. external OS process (`claude_agent_sdk` / `claude` CLI / `anthropic`) —
   **`EXTERNAL_RUNTIME_UNAVAILABLE`** (a genuinely separate process cannot
   authenticate: host-injected credentials flow over IPC and no independent API
   key is present).

The owner's surface rule (v3 directive) is that if v3 also fails, Goal A
execution stops **in this environment entirely** rather than designing Harness v4.
V3 did fail, so no Auteur producer run is consumed and Goal A is halted here
pending an owner decision (realistic options being an environment with an
independent credential/API key, or a different host).

**No repo code change fabricates a lossless frozen-artifact capture or an external
session credential; the remaining boundary is an owner/environment decision, not a
repo edit.**

## Verified top-level facts (from RUN1-STOP-BOUNDARY.md)

- `GOAL_A_AUTEUR_TARGET1_RESULT = RUN1_COMPLETED_STOP_RULE_TRIGGERED`
- Stop boundary = `HARNESS_ENVIRONMENT_FAILURE`
- Producer sub-agent P1 **could not persist its own frozen brief** to
  `experiments/goal-a-auteur-target1/run1_brief.md` (host write dispatch did not
  grant the target directory; `run1_brief.md` confirmed absent).
- Producer provenance side-channel: P1 read the pinned Auteur target from the
  un-pinned local object store `H:\GithubRepositories\auteur` at the same SHA
  rather than the pinned checkout path; content SHA identical but provenance
  differs.
- P1 could not re-run the probe engine (read-only shell); probe-derived numbers
  labeled documented-but-not-verified at the pinned revision.
- `RUN1_EPISODE_ADMISSIBILITY = HARNESS_ENVIRONMENT_FAILURE`; all evaluation
  axes `NOT_RUN` / `NOT_EVALUATED` / `NOT_APPLICABLE` because no frozen artifact
  was persisted.
- `AUTEUR_REPEATABILITY = NOT_APPLICABLE` (Run 2 not dispatched).
- This is a **harness/environment stop, not a product verdict**.

## Pins referenced in the packet

- TARGET_REPOSITORY = ThorStarlord/auteur ; TARGET_SHA = `a6f7ded7d01cfdd149c526a71e0c751af517e0b1`
- SENSEMAKING_SHA = `f83fd773f6b9adeb354790b3764cbcb2bd5acbf3`
- TASK_TEXT_SHA256 = `4C7574A0B4A90029A96A04A4A6D45A2F0865963A23AFCD9BFC20184C531CB65D`

## Substrate blockers this preserves (see live tracker)

1. **Producer artifact-finalization** — isolated producer sub-agent must be able
   to persist its own frozen brief to the exact session-scoped path (ADR 0010 /
   `expected_output_path` contract).
2. **Verifiable provenance / hermeticity** — pinned checkout path (not un-pinned
   object store) + ability to re-run the probe engine so probe-derived numbers
   are verified.

## Live tracker

A dedicated Goal A execution-substrate issue tracks the repair of these two
blockers and the preconditions for a compliant future Run 1.
