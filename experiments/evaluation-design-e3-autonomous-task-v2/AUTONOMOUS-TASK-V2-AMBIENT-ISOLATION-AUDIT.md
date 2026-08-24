# Autonomous Task v2 — Pre-Lock Ambient-Environment Audit

Status: DRAFT. Narrow, metadata-only audit. No sibling worktree's file
contents were opened, read, grepped, or diffed at any point in this audit —
every finding below comes from `git worktree list`/`git worktree list
--porcelain` (which reads administrative metadata the current repository
already stores about registered worktrees, not their working-tree contents),
from directory-name enumeration (`ls`, names only), and from one throwaway
standalone clone this audit created and destroyed itself (never a sibling's
existing clone). No commit logs, branch histories, reports, or evaluator
artifacts belonging to any sibling worktree were inspected.

This audit does not change the Autonomous Task v2 design. It found one real,
previously-undetected preflight gap and fixed it narrowly (§5); it did not
alter any task family, hypothesis, regime, or sample-size decision.

## 1. Metadata-only inventory

`git worktree list --porcelain` run from `H:/GithubRepositories/sensemaking-skills`
returned 24 entries. All 24 (including the primary working directory) are
registered under the same git common directory,
`H:/GithubRepositories/sensemaking-skills/.git` — this is structural, not a
matter of interpretation: `git worktree list` can only enumerate worktrees
that are registered in the current repository's own `.git/worktrees/` admin
area, so every entry it returns shares that common directory by definition.

| Path | Branch / state | HEAD SHA (first 8) |
|---|---|---|
| `H:/GithubRepositories/sensemaking-skills` (primary) | `main` | `1458f921` |
| `C:/.../reasonix/worktrees/.../3b9623566a/...` | `reasonix/delivery-20260812-220949-...` | `63350d47` |
| `C:/.../reasonix/worktrees/.../3d6b702e68/...` | `reasonix/delivery-20260812-235250-...` | `63350d47` |
| `C:/.../reasonix/worktrees/.../9530761a09/...` | `reasonix/delivery-20260812-221522-...` | `63350d47` |
| `C:/.../reasonix/worktrees/.../bbc3e8d5e9/...` | `reasonix/delivery-20260812-235545-...` | `63350d47` |
| `C:/.../reasonix/worktrees/.../cca0f7a03a/...` | `evidence/0017-auteur-repo-sensemaking-brief-repair` | `9bc83605` |
| `C:/.../Temp/opencode/pr111-continuation` | `run-control/0016-authorization-record-continuation` | `9e503c04` (prunable — gitdir points to non-existent location) |
| `C:/.../Temp/opencode/pr125-review-base` | detached | `5c1612ac` (prunable) |
| `C:/.../Temp/opencode/pr125-review-head` | detached | `a0c0c833` (prunable) |
| `H:/GithubRepositories/sensemaking-skills-1br2` | `experiment/autonomous-evolution-1br2-0ffb564` | `2df9f49a` |
| `H:/GithubRepositories/sensemaking-skills-1r2` | `experiment/autonomous-evolution-1r2-0ffb564` | `8120901c` |
| `H:/GithubRepositories/sensemaking-skills-ab-dogfood` | `experiment/ab-dogfood` | `8adf5d75` |
| `H:/GithubRepositories/sensemaking-skills-acceptance` | `impl/architectural-review-acceptance-infrastructure` | `944e7523` |
| `H:/GithubRepositories/sensemaking-skills-e1` | `experiments/evaluation-design-e1-v1` | `70fb50a4` |
| `H:/GithubRepositories/sensemaking-skills-e2` | `experiments/evaluation-design-e2-v1` | `9d444a3c` |
| `H:/GithubRepositories/sensemaking-skills-exp0002-results` | `experiment/exp-0002-results` | `d82ae512` |
| `H:/GithubRepositories/sensemaking-skills-exp1` | `experiment/autonomous-evolution-exp1-0ffb564` | `884cf543` |
| `H:/GithubRepositories/sensemaking-skills-exp1b` | `experiment/autonomous-evolution-exp1b-0ffb564` | `ef7a70ba` |
| `H:/GithubRepositories/sensemaking-skills-framework` | detached | `50daa17a` |
| `H:/GithubRepositories/sensemaking-skills-taskc` | `experiments/post-hardening-decision-probe-v1` | `1f33605d` |
| `H:/GithubRepositories/sensemaking-skills-taskd` | `experiments/post-hardening-adjudication-probe-v1` | `6f532aae` |
| `H:/investigation-worktree` | detached | `adbf7058` |
| `H:/scratch-step2-negative/target` | detached | `087cf85f` |
| `H:/scratch-step2-positive/target` | detached | `087cf85f` |

Four branch names contain the literal string `0ffb564` — the frozen SHA this
design uses as its base — confirming (at the metadata level only; contents
not inspected) that this commit was already used as a base for other,
separately-named experiment work before this design pass began.

**Physical location relative to a naive/default experiment parent**: 14 of
the 24 entries live directly inside `H:/GithubRepositories/`, immediately
adjacent to the primary repository itself. This is the single most important
fact for §2 below — any new clone placed as a further sibling inside that
same directory (the path a person would reach for without thinking twice
about it) is co-located with all fourteen.

## 2. Exposure test from a proposed experiment location

Two exposure vectors were tested, both metadata/path-level only.

### 2a. Plain directory-name enumeration of the default parent

`ls -1 H:/GithubRepositories/` (names only, no file opened) returned **over
80 entries**, including — beyond the 14 `sensemaking-skills-*` worktrees
already identified via git metadata — directory and log-file **names** that
are, on their face, strongly suggestive of prior benchmark/experiment
structure and outcomes without opening a single one of them: `auteur-
benchmark-base`, `auteur-benchmark-blindrepo`, `auteur-benchmark-launch`,
`auteur-benchmark-records`, `auteur-benchmark-run3`, `auteur-evolution`,
`auteur-evolution-v2`, `auteur-evolution-v2b`, `auteur-evolution-v2r`,
`v2.1-pilot-run`, `v2.1-r1-run`, `v2.1-r2-run`, `sensemaking-skills-task-v0`,
`sensemaking-skills-v2`, `sensemaking-skills-v2r2`, `exp-0002-logs`,
`exp-0002-target`, `run3.log`, `run4-negative.log`, `run5-negative.log`,
`run6-negative.log`, `sessions-issue-39-live-run`, `sessions-issue-39-negative`,
`mutation-audit-tmp`. Names such as `v2.1-r1-run` / `v2.1-r2-run` and
`run4-negative.log` are directly suggestive of a regime-labeled run
structure and pass/fail outcome pattern — this is name-level information,
not content, but it is exactly the kind of task-construction or expected-
outcome clue the protocol's `REFERENCE_SOLUTION_LEAKAGE` and
`CROSS_RUN_LEAKAGE` failure modes exist to prevent, and it is visible from
one `ls` call, no special access required. **None of these were opened.**

### 2b. Local-clone git-config breadcrumb (new finding, not previously identified)

A throwaway standalone clone was created via `git clone <local path>` into
the isolated session scratchpad (a location with no relationship to
`H:/GithubRepositories/` and no existing siblings) to test the initial
pass's assumption that "a standalone clone, unlike a worktree, is
disconnected from the origin's admin metadata."

- Confirmed true for git's own worktree-registration metadata: `git
  worktree list`, run from inside the fresh clone, returned exactly one
  entry — itself. None of the 24 siblings above are reachable through git's
  worktree machinery from a real clone. This is a genuine, structural
  difference from the `git worktree add` method this audit's own earlier
  frozen-SHA calibration step (Hardening Pass 1) used — that worktree, while
  it existed, WAS part of the shared metadata surface; it has since been
  removed.
- **New finding**: the clone's `.git/config`, however, retained
  `url = H:/GithubRepositories/sensemaking-skills` under `[remote "origin"]`
  — a literal, readable path back to the directory containing all 14
  co-located siblings and the ~80-entry gallery in §2a. Any agent with
  ordinary filesystem read access to its own clone's `.git/config` (an
  unremarkable, expected operation — the harness this audit itself ran under
  has exactly this level of access) could read this one line and then `ls`
  the parent it names, regardless of where the clone itself is physically
  located. **Relocating the clone alone does not close this vector** — the
  breadcrumb travels with the clone.
- Verified the fix: `git remote remove origin` on the throwaway clone
  reduced its `.git/config` to zero `url` lines (confirmed by direct
  inspection of that count, not by assumption). This is a real,
  demonstrated mitigation, not merely a proposed one.
- Also verified: an isolated parent directory (the session scratchpad) shows
  no experiment-relevant names — its only entries were the clone this audit
  created itself and, one level up, opaque per-session UUID directories that
  carry no semantic information about this experiment. This confirms
  relocation genuinely closes the §2a vector specifically, even though it
  does not, by itself, close the §2b vector.

The throwaway clone was deleted at the end of this test; nothing from it
persists.

## 3. Classification

**`AMBIENT_SIBLINGS_EXPOSED_AND_NOT_TECHNICALLY_CLOSED`** — for the
default/naive setup (a local-path `git clone` placed inside
`H:/GithubRepositories/`, run under a filesystem-unsandboxed agent harness,
which is the category of harness this audit itself ran under). This is not
a worst-case hypothetical: it is the setup a person would reach for without
deliberate effort, and it fails on *two independent* vectors (§2a path
exposure, §2b config breadcrumb), not one.

A corrected setup — clone into a genuinely isolated parent directory **and**
strip the `origin` remote immediately after cloning — was demonstrated in
§2b to close both vectors *at the filesystem/metadata level available to
this audit's tools*. However, per the user's own framing, this audit cannot
certify true isolation merely because a careful configuration avoids the
two vectors it happened to test: a general-purpose agent harness (again,
the category this audit itself used) generally has unrestricted absolute-
path filesystem access, meaning nothing stops a benchmark agent from simply
navigating to `H:/GithubRepositories/` directly if it ever has reason to
explore outward from its assigned clone — the corrected setup removes the
*breadcrumbs pointing there*, it does not make the path itself
unreachable. Whether the path is reachable at all is a property of the
execution environment/sandbox, not of the clone's configuration, and this
audit has no visibility into what sandboxing (if any) the actual future
benchmark-agent harness will provide.

Overall status carried forward unchanged from the M4 precedent named in the
original design brief: **`MITIGATED, AUDITABLE, NOT TECHNICALLY CLOSED`.**
The corrected clone setup is a real, demonstrated mitigation (not merely
aspirational) and the two vectors found are now specifically named and
auditable — but neither this audit nor the preflight script it updates can
prove the benchmark agent's filesystem access is actually bounded to its
assigned clone.

## 4. Preflight coverage review

`AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`, as written before this audit, did
**not** detect either vector. Its only sibling-related check (#5,
`no-known-sibling-experiment-dirs`) searched for a single hardcoded name
pattern (`*autonomous-task-v2*`) inside `$CLONE_DIR/experiments/` — it
checked for self-leakage of this specific experiment's own past runs, not
for exposure of *unrelated* prior experiments, and it never inspected the
clone's parent directory or its `.git/config` at all. This is a real,
previously-undetected gap, not a restatement of a known limitation — fixed
below rather than left as a finding only.

## 5. Preflight update (narrow, mechanical, name-agnostic)

Three checks were added to `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`, all
generic (no hardcoded sibling names, so they do not depend on ever having
seen this specific gallery of directories again):

1. **`clone-remote-has-no-local-path`**: fails if any configured git remote
   URL for the clone resolves to a local filesystem path rather than a
   network URL (`http(s)://`, `ssh://`, `git://`, or a `git@host:` scp-style
   address) — catches the §2b breadcrumb generically, for any local-path
   remote, not just this repository's own path.
2. **`clone-worktree-list-shows-self-only`**: fails unless `git -C
   $CLONE_DIR worktree list` returns exactly one entry — catches both the
   "used `git worktree add` instead of a real clone" mistake and any other
   way the clone might end up administratively linked to a shared `.git`.
3. **`clone-parent-directory-is-uncrowded`**: fails if the clone's immediate
   parent directory contains any entry besides the clone itself, UNLESS an
   explicit allowlist file (`--sibling-allowlist <path>`, one name per line)
   is provided and every extra entry appears on it. This is the generic,
   allowlist-based rule the review asked for in place of a hardcoded-name
   search — it does not need to know what `auteur-benchmark-run3` or
   `v2.1-r1-run` are named to flag an unapproved neighbor.

A fourth, explicitly honest line was added rather than a fourth check:
`ambient-scope-runtime-enforcement` is always reported
**`AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED`** — the script states plainly
that it can verify the clone's own configuration and immediate surroundings
at preflight time, but cannot verify or enforce that the live agent
harness's filesystem access is actually bounded to the clone root during
the run itself; that requires container/sandbox-level isolation outside a
bash script's power, and claiming otherwise would be exactly the "green
paint over an open door" failure mode the review warned against.

The script was smoke-tested against the corrected clone configuration
(isolated parent, origin remote stripped) and against the original
uncorrected configuration (adjacent to the primary repo, remote intact) to
confirm it passes the former's three new checks and fails the latter's,
before being left in its final state.

## 6. Report

- **Metadata-only inventory**: 24 registered worktrees, all sharing this
  repository's git common directory; 14 physically adjacent to the primary
  repo under `H:/GithubRepositories/`; 4 branch names literally contain the
  frozen SHA `0ffb564`, confirming (at the metadata level) that this commit
  was already a base for other, separately-named experiment work.
- **Exposure classification**: `AMBIENT_SIBLINGS_EXPOSED_AND_NOT_
  TECHNICALLY_CLOSED` for the default/naive setup, on two independent
  vectors (parent-directory name enumeration; local-clone git-config
  remote-URL breadcrumb). A corrected setup (isolated parent + stripped
  remote) was demonstrated to close both vectors at the filesystem/metadata
  level, but true isolation still depends on execution-environment
  sandboxing this audit cannot verify.
- **Preflight detection**: did not detect either vector before this audit;
  now does, via three new generic, non-hardcoded-name checks, plus an
  honest `AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` status line that is
  always reported rather than silently omitted.
- **Changes made**: `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` updated (§5). No
  task family, hypothesis, regime text, sample size, or acceptance rule was
  touched — this audit's scope stayed exactly as narrow as instructed.
- **Design status: remains READY FOR HUMAN DRAFT REVIEW.** This audit
  surfaced a real, previously-undetected preflight gap and fixed it
  narrowly; it did not surface a defect in the experimental design itself
  that would require reopening the protocol, task-construction rules, or
  hypotheses. The residual risk — that no bash-level preflight can prove
  runtime filesystem sandboxing — is recorded as exactly the kind of
  environment-level fact this repository's own prior-work provenance (the
  M4 lesson) says should be resolved, or explicitly accepted with its
  status named, during human review, not silently assumed away.
