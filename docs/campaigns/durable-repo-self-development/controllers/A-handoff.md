# Controller A — handoff to Controller B

```
CONTROLLER A -> CONTROLLER B.  Written 2026-09-02 by Controller A, immediately
before Controller B is instantiated. Immutable: not retro-edited. The one field
that is filled in after this commit (Controller B's checkpoint SHA) is recorded
in CAMPAIGN-STATE.md section 16, not by editing this file.
```

After this handoff, **Controller A is a FORMER controller.** Per the owner
instruction ("Controller A Relinquishment Rule"), Controller A will perform only
the mechanical action of instantiating Controller B and will not: tell B what
task to choose, summarize A's reasoning, rank boundaries, name a subsystem for B
to inspect first, restate A's frontier view, reinterpret campaign state for B,
critique or veto B's selection, or redirect B afterward. A does not regain
semantic campaign ownership. Any retrospective A/B comparison happens only after
B completes its cycle or reaches a legitimate terminal disposition.

---

## Pre-handoff repository invariant (owner instruction checklist)

| # | Requirement | Status |
|---|---|---|
| 1 | Task A complete to its legitimate boundary | YES — decision-changing uncertainty U-2 resolved with evidence (A1); the smallest warranted change implemented and committed; remaining work needs a fresh campaign warrant, not an extension of Task A. |
| 2 | Relevant validation run | YES — `validate-repo.py` exit 0; probe gate PASS (0 blocking); `test-validators.py` 78/78; core-assertions pytest 99 passed / 1 skipped. Exact-head CI: PR #269 (draft) triggered on `431ec43` — result recorded in CAMPAIGN-STATE.md section 15. |
| 3 | Campaign 2 semantic state updated | YES — `CAMPAIGN-STATE.md` v3 (Task A recorded; U-2 resolved; MG-7 status; FO-1..FO-4; CCO-1; Controller A post-Task-A frontier candidates F-a..F-d). |
| 4 | All intended surviving campaign changes committed | YES — bootstrap `3c55254`; A selection `a216293`; Task A `431ec43`. |
| 5 | Controller A cycle result committed | YES — Task A result is in `CAMPAIGN-STATE.md` section 8 + `controllers/A-task-A1-reconstruction-probe.md`. |
| 6 | Controller A handoff checkpoint created | YES — this file. |
| 7 | Exact handoff SHA recorded | The commit that adds this file (branch `campaign/durable-repo-self-development`); recorded in `CAMPAIGN-STATE.md` section 16 handoff trace. |
| 8 | Current `origin/main` fetched and recorded | `git fetch origin` 2026-09-02 → `origin/main` = `06a57d1d182a32684275d343a9248429feedbfe6` (unchanged since campaign start; no drift). |
| 9 | Candidate-vs-main state recorded | `CAMPAIGN-STATE.md` section 3. Candidate = campaign branch head; product-surface delta = `STATUS.md` / `roadmap.md` / `goal.md` / `CONTEXT.md`(+1 row); nothing merged. |
| 10 | Relevant PR / CI observations recorded | Draft PR **#269** (`campaign/durable-repo-self-development` → `main`, not for merge). CI on `431ec43` — see `CAMPAIGN-STATE.md` section 15. |
| 11 | Working tree clean | Verified `git status --porcelain` empty in `H:/GithubRepositories/smk-campaign-2` before instantiating Controller B. No intentional uncommitted state. |

## Handoff provenance

```
PREDECESSOR CONTROLLER ID:   Controller A — the coding-agent context that
                             received the owner instruction, ran the preflight,
                             committed the bootstrap, and executed Task A.
                             Model: claude-sonnet-5 (Claude Code harness).
SUCCESSOR CONTROLLER ID:     Controller B — a fresh `general-purpose` sub-agent
                             context spawned via the Claude Code `Agent` tool.
LAUNCH MECHANISM:            `Agent` tool, `subagent_type: general-purpose`,
                             run in the foreground, single call. The verbatim
                             prompt is reproduced below and is the ONLY
                             information B receives from A.
MODEL / AGENT TYPE:          claude-sonnet-5 (same model family as A; disclosed,
                             not claimed as full independence). Fresh context
                             window; no shared transcript.
CONTEXT-ISOLATION CLAIM:     Context isolation — HARNESS-REPORTED (the `Agent`
                             tool starts the sub-agent cold; it does not receive
                             A's conversation transcript or A's private/thinking
                             content). Bootstrap minimality, checkpoint
                             immutability, and non-resumption — CONTROLLER-
                             ASSERTED (discipline, not environment-enforced).
                             Predecessor PROCESS non-persistence — NOT
                             established: A's process continues and the `Agent`
                             call returns B's report to A. `SUCCESSION_ISOLATION_
                             UNVERIFIED` applies to that dimension (EC-2).
EXACT BOOTSTRAP TEXT:        see "Verbatim bootstrap given to Controller B" below.
FILES / PATHS DISCLOSED:     only: the repo worktree path + branch; the paths of
                             `CHARTER.md` and `CAMPAIGN-STATE.md`; that B is the
                             active semantic Campaign 2 controller. No mission
                             text, no task rationale, no frontier, no gaps, no
                             recommended task, no predecessor predictions.
REPOSITORY HANDOFF HEAD:     the commit that adds this file, on branch
                             `campaign/durable-repo-self-development`
                             (SHA in CAMPAIGN-STATE.md section 16).
CURRENT ORIGIN/MAIN HEAD:    06a57d1d182a32684275d343a9248429feedbfe6
WORKTREE / CHECKOUT IDENTITY: H:/GithubRepositories/smk-campaign-2, branch
                             campaign/durable-repo-self-development, working tree
                             clean at handoff. B works here and commits to this
                             branch.
GIT CAPABILITIES:            full (the sub-agent has Bash; git 2.51.0; branch,
                             commit, push to `origin` all available).
GITHUB CAPABILITIES:         full read + push + PR via `gh` (shared auth,
                             account ThorStarlord, scopes repo/workflow/read:org).
VALIDATION CAPABILITIES:     full — `python scripts/validate-repo.py`,
                             `scripts/test-validators.py`, the probe engine,
                             `python -m pytest`, all runnable (Python 3.14.3).
OUT-OF-BAND INFORMATION PROVIDED:  none beyond the verbatim bootstrap below.
START TIME:                  2026-09-02 (Campaign 2 day 1).
SUCCESSOR CHECKPOINT SHA:    to be recorded in CAMPAIGN-STATE.md section 16 after
                             Controller B commits its reconstruction + selection
                             checkpoint (before any Task B implementation).
PREDECESSOR ACCESS AFTER LAUNCH:  Controller A's process persists and receives
                             B's final report through the `Agent` call. A has
                             committed (this file) not to use that report to
                             steer B, and to treat any A/B comparison as
                             post-hoc only. This is the known isolation
                             limitation (EC-2).
KNOWN ISOLATION LIMITATIONS: (1) same model family; (2) predecessor process
                             persists; (3) checkpoint immutability and
                             non-resumption are discipline, not enforcement;
                             (4) B runs in A's worktree (clean, exact committed
                             state — no leftovers — but the same filesystem).
                             A stronger variant (owner launches B in a wholly
                             separate session) is available if the owner wants to
                             raise the evidence level.
```

Isolation classification (owner instruction "Handoff Provenance"):
`DEMONSTRATED ISOLATION` — none claimed. `HARNESS-REPORTED ISOLATION` — context
(no transcript, no private reasoning). `CONTROLLER-ASSERTED ISOLATION` —
bootstrap minimality, checkpoint immutability, non-resumption.
`UNVERIFIABLE / UNVERIFIED` — predecessor process non-persistence
(`SUCCESSION_ISOLATION_UNVERIFIED`).

---

## Verbatim bootstrap given to Controller B

The following is the exact and complete prompt passed to the fresh sub-agent.
Nothing else is provided.

```text
You are now the fresh independent semantic controller for Campaign 2 in the
sensemaking-skills repository ("Controller B"). You have a new context with no
access to the previous controller's conversation or private reasoning.

Work in this repository worktree:
  path:   H:/GithubRepositories/smk-campaign-2
  branch: campaign/durable-repo-self-development
The working tree is clean and is at the exact committed handoff state. Commit
your work to this branch. You may push to origin and inspect CI. `git`, `gh`
(GitHub, authenticated), `python`, `pytest`, and the repo's validators/probe
engine are all available.

The Campaign 2 charter is at:
  docs/campaigns/durable-repo-self-development/CHARTER.md
The durable Campaign 2 semantic state is at:
  docs/campaigns/durable-repo-self-development/CAMPAIGN-STATE.md
Other durable campaign records are in the same directory
(docs/campaigns/durable-repo-self-development/), including the preserved owner
instruction and the previous controller's checkpoints under controllers/.

Reconstruct, from those durable sources and from current repository / GitHub
evidence: the campaign mission; the authority available to you and the authority
reserved to the owner; the current integrated origin/main state; the Campaign 2
candidate (branch) state and which candidate changes are not on main; the
demonstrated product capabilities and demonstrated campaign capabilities; the
evidence ceilings; what the previous strategic cycle changed and why its task
had been selected; the material product gaps; and the current development
frontier.

Reverify consequential factual claims before acting on them — durable state may
contain stale or wrong facts. A previously recorded capability frontier, "last
assessed" candidate, or "next task" in the campaign state is historical
evidence, not a command; you own the next decision and may reject it.

Independently determine the next strategically warranted repository-level task,
comparing the plausible capability boundaries. Task B must materially advance a
campaign-relevant product capability, or produce evidence that materially
refines or invalidates the campaign's product-development architecture.

Before implementing anything, write and commit a controller-specific
reconstruction-and-selection checkpoint at
docs/campaigns/durable-repo-self-development/controllers/B-reconstruction-and-selection.md
(answer the 20 fresh-controller reconstruction questions and fill the mandatory
successor-checkpoint fields from the owner instruction; record its commit SHA).
Then execute Task B through bounded responsibilities, validate with the
strongest available referee, update the durable campaign state
(CAMPAIGN-STATE.md) and any warranted product surfaces, and write
docs/campaigns/durable-repo-self-development/controllers/B-cycle-result.md.

Do not merge any PR, accept an ADR, publish externally, change owner-reserved
decisions, or infer owner preference — classify anything like that as
OWNER_DECISION_REQUIRED. Follow the charter's constraints and stopping rules.

Report back: your reconstruction summary, the task you independently selected and
why, what you implemented, your validation results, the commit SHAs (checkpoint
+ work), and your assessment of what Campaign 2 has and has not established.
```
