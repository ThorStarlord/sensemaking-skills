# Normal-use trial program: staged, not yet executed (2026-09-29)

Status: **staged**. No episode has been run. This records the Step 4
prerequisites that are resolvable from repository/allowed evidence and the
boundary that is not.

## What Step 4 requires

Per `strategic-sensemaking-observation-guide.md` (section 11 template, section
12 cross-episode review):

1. Pick 2-3 real, bounded tasks in repositories other than this one.
2. Before each trial, confirm the harness loaded the current
   `using-sensemaking` revision (section 10, "Loaded-Skill identity").
3. Record each episode with the section 11 template.
4. After 3 episodes, write the section 12 cross-episode verdict on whether to
   keep investing in the control layer, simplify it, or stop.

## Prerequisite check (done)

`python scripts/probe_skill_distribution.py --no-write` (installed root
`~/.agents/skills`):

- `using-sensemaking` and `strategic-sensemaking-loop`: **synchronized** — the
  control-layer bootstrap the episodes evaluate is current. Trial 001's
  attribution loss (stale `using-sensemaking`) does not apply to the current
  installation.
- 15 downstream Skills are stale (e.g. `repo-sensemaker` installed 199 vs repo
  429 lines; `strategic-repository-analysis` 402 vs 669; `workflow-planner`
  134 vs 147; `to-prd`, `pricing`, `discovery`, `hypothesis`, ...), 4 missing,
  3 line-ending-only.
- Consequence: control-layer attribution is sound, but any observation about
  downstream Skill execution is weakened until the harness is synchronized
  (`--sync` or `setup-skills --force`). Lower the claim ceiling and preserve
  the mismatch per the guide.

## Decision on the stale Skills (delegated, 2026-09-29)

**Do not synchronize the global harness for the trials. Record the caveat per
episode instead.**

Rationale:

- The two Skills that gate the control-layer question — `using-sensemaking` and
  `strategic-sensemaking-loop` — are already current, so the primary attribution
  the trials need is sound.
- The stale set is 15 drifted + 4 missing downstream Skills. Synchronizing
  mutates the machine-global `~/.agents/skills` (and, if distributed, the other
  agents' folders), affecting work outside this repository for a secondary
  attribution gain.
- The guide explicitly permits a real episode with imperfect attribution:
  "Lower the claim ceiling and preserve the mismatch" (section 10).

If full downstream attribution is later required, the contained action is a
single sync of the drifted + missing Skills, on this machine's `.agents` only,
followed by re-running `probe_skill_distribution.py --no-write` — not a blanket
sync of all 51.

## Boundary (why this is not executed here)

Selecting the 2-3 real bounded tasks and running the episodes is a strategic,
owner-involved act, not a repository step:

- The tasks must be real work in other repositories (the candidate set is the
  owner's active repositories, many of them worktrees of one project).
- Episodes may mutate those repositories; that is separate authority the
  stabilization program does not carry.
- Section 12's verdict is an investment decision about the control layer and
  is reserved to the owner.

Fabricating episode records would violate the "do not invent evidence" rule
and produce a verdict with no grounding.

## Ready-to-run protocol

For each selected task:

1. `python scripts/probe_skill_distribution.py --no-write` and record the
   loaded `using-sensemaking` identity (and `--sync --no-write` only if a
   trial specifically needs current downstream Skills).
2. Run the episode with the `using-sensemaking` / strategic-sensemaking-loop
   Skill available; capture the section 11 fields.
3. File the episode under `docs/normal-use/` (e.g.
   `strategic-sensemaking-trial-00N.md`).
4. After three episodes, write the section 12 cross-episode review and the
   investment verdict.
