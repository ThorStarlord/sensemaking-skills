# Task P1 — Real Repository Decision-Sharpening Probe (v1)

experiment_type: product_interaction
task: Task P1 — Real Repository Decision-Sharpening Probe
status: in_progress
created_at: 2026-08-07T18:33:03Z

## Question being investigated

> Does `repo-sensemaker` help the owner make a better engineering decision on a
> real repository, on an ordinary invocation?

This is a **product / interaction experiment**, not an evaluation experiment.
The unit of value is the decision before -> investigate -> decision after
comparison, not taxonomy/fog/weakness-label accuracy. No weakness-label
accuracy, `decision_delta`, or any replacement scorer is used.

## Frozen product state

- **Repository being investigated**: `sensemaking-skills` (this repository,
  current checkout on experiment branch `experiments/product-interaction-p1-v1`).
- **Repository SHA (frozen)**: `b58038984f54fa13305aa951a7cbb6767e7ddcc9`
  (current `origin/main`, fetched 2026-08-07).
- **sensemaking-skills SHA / skill version used**:
  `skills/repo-sensemaker/SKILL.md` at the frozen SHA above — the canonical
  in-repository copy (164-line variant containing the corrected Execution
  Protocol and the "Runtime-owned artifact skeleton (issue #55)" section).
  The skill has no explicit numeric version; version identity = file path +
  SHA.
- **User question given to repo-sensemaker**:
  > Understand this repository and tell me what engineering work would create
  > the most value next.
- **Execution mode**: standalone agent-native invocation (no orchestration
  runtime, no skeleton). The complete Repository Sensemaking Brief artifact is
  authored directly per the skill, then validated once with
  `python scripts/validate-brief.py <artifact> --target-repo <repo> --repo-root <root>`.
- **Attempts**: exactly one invocation. No repairs, no ensembles, no
  follow-up attempts, no re-runs until a preferred result.

## Branch base correction (setup note)

The original P1 instruction said "fresh experiment branch from current main".
`main` (local) and `origin/main` differ; this experiment branch
`experiments/product-interaction-p1-v1` was created from **current
`origin/main` @ b580389**, per explicit owner correction. The previously
checked-out `hardening/repository-sensemaking-v1` branch @ a259bce is the
**closed REVISE candidate** and was deliberately left unmerged — it is NOT the
canonical product and was not used as the base. The initial P1 branch (created
from the hardening branch) was deleted before any work was committed.

## Execution surface actually selected (and why)

A normal user following `GETTING_STARTED.md` (origin/main) recommended
agent-native path invokes the **in-repository copy**
(`skills/repo-sensemaker/SKILL.md`), not an installed copy. The probe therefore
executes that in-repo copy at the frozen SHA.

Three distinct implementations were found during setup (not resolved):

| Copy | Location | Lines | Notes |
|---|---|---|---|
| Global installed | `C:\Users\Admin\.agents\skills\repo-sensemaker\SKILL.md` | 119 | Stale — Execution Protocol still says "Call `scripts/create-artifact.py` to resolve the output path" (pre-ADR-0010 behavior). What `/repo-sensemaker` slash command resolves to on this machine. |
| Canonical in-repo (selected) | `skills/repo-sensemaker/SKILL.md` @ b580389 | 164 | Corrected protocol: never call `create-artifact.py`; use `expected_output_path` verbatim (ADR 0010, issue #40). Includes issue #55 runtime skeleton guidance. |
| Hardening branch (not canonical) | `skills/repo-sensemaker/SKILL.md` @ a259bce | 452 | Closed REVISE candidate, deliberately unmerged. |

**Product evidence (recorded, NOT fixed before PRE)**: the global installed
copy lags the canonical in-repo copy — a user who installed via
`pip install sensemaking-skills; sensemaking-skills setup-skills` would invoke
the stale 119-line version teaching the pre-ADR-0010 path-resolution behavior.
This distribution/install lag is a potentially important product finding to be
evaluated after the probe, not before. No file was modified to resolve it.

## Frozen constraints

- Do NOT modify the target repository or `repo-sensemaker` during the probe.
- Do NOT run repairs, ensembles, or follow-up attempts.
- Do NOT resolve the installed-copy mismatch before PRE is recorded.
- Do NOT use weakness-label accuracy, `decision_delta`, or any replacement
  scorer.
- Investigation is read-only; no implementation.
- After the learning record, STOP. Do not implement the recommendation and do
  not modify `repo-sensemaker`.

## Artifact set (this directory)

- `charter-v1.md` — this file (frozen product state).
- `owner-pre-v1.md` — owner's pre-investigation position, recorded verbatim and
  frozen BEFORE investigation.
- `repo-sensemaker-investigation-v1.md` — what repo-sensemaker actually
  discovered (full investigation record / sensemaking brief).
- `owner-synthesis-v1.md` — the compact human-facing synthesis shown to the
  owner (recommended next work; strongest evidence; alternatives including do
  nothing; important uncertainty; decision-changing evidence).
- `owner-post-v1.md` — owner's decision after reading the synthesis.
- `learning-v1.md` — qualitative PRE vs POST comparison and whether the
  interaction is useful enough to repeat.

## Stop condition

Record `learning-v1.md`, then stop. No implementation, no repo-sensemaker
modification, no P2 design unless the learning record justifies asking for one.
