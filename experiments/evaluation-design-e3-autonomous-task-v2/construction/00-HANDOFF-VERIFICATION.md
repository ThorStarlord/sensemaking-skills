# Autonomous Task v2 — Phase 0: Handoff Verification

Status: HANDOFF VERIFIED
Session: Candidate Construction and Pilot Lock (new phase; design-review phase is CLOSED)
Date: 2026-08-19
Workspace: isolated worktree `worktree-autonomous-task-v2-candidate-construction`
(created via native EnterWorktree, branched fresh from `origin/main`)

## 1. Input design status

The 17-file design-review package at
`experiments/evaluation-design-e3-autonomous-task-v2/` is the normative input
to this phase.

Every individual artifact's own `Status:` header still reads `DRAFT`, and the
literal, unqualified phrase "READY FOR PILOT LOCK" does not appear as an
achieved status inside those 17 files — the package's own self-assessment
after `LOCK-READINESS-RESPONSE.md` was `READY FOR PILOT LOCK-CANDIDATE
REVIEW`, and `LOCK-READINESS-RESPONSE-4.md` (the file addressing the
reviewer's third line-by-line pass) explicitly defers final authorization:
"Final lock authorization remains with the reviewer's own re-inspection of
the corrected bundle" (`LOCK-READINESS-RESPONSE-4.md:116-118`).

This is a real provenance gap in the *files*, not a design gap. The missing
fact is the final reviewer re-inspection, which happened out-of-band (in the
review conversation, not written back into these files) after Response 4.
The owner has confirmed that re-inspection took place and returned:

    READY FOR PILOT LOCK

This is recorded here as the out-of-band handoff fact this phase proceeds
from. The historical `DRAFT` headers and the trajectory of `CHANGES REQUIRED
BEFORE PILOT LOCK` verdicts in `DESIGN-REVIEW.md` are left unmodified — they
correctly describe the documents' state at the time they were written. This
note supplies the missing later event rather than rewriting history.

Recorded:

    INPUT_DESIGN_STATUS = READY_FOR_PILOT_LOCK

Distinction preserved per owner instruction: `READY FOR PILOT LOCK !=
PILOT LOCKED`. No candidate content, oracle commitments, manifests, salts,
rankings, dispatch seeds, or pilot runs exist yet — those are what this phase
constructs. The experiment may not be called `PILOT LOCKED` until Phases 1-14
below are actually completed and a real lock record exists.

## 2. Frozen repository identity

    repository:   ThorStarlord/sensemaking-skills
    frozen SHA:   0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5

Verified mechanically in this working copy:

- `git cat-file -t 0ffb564b...` → `commit` (object exists).
- `git log --oneline -1 0ffb564b...` → `0ffb564 Merge pull request #169 from
  ThorStarlord/integration/ssk-0017-evidence`.
- `git merge-base --is-ancestor 0ffb564b... HEAD` → true, both in the
  original local checkout (HEAD `1458f92`) and in this isolated worktree
  (HEAD `c909295`, branched fresh from `origin/main`, which has since
  advanced further — e.g. merged PR #216/#217 — beyond either point). The
  frozen SHA remains a verified ancestor in both cases.

Consequence for construction: candidate task text, fixtures, and oracle specs
are authored against the repository **as it existed at the frozen SHA**,
read via `git show 0ffb564b:<path>`, not against the current working tree —
HEAD has since touched exactly the three named substrate files (see below)
plus unrelated work in other areas of the repository. The actual pilot/main
dispatch will always use a fresh standalone clone pinned to this exact SHA
(enforced by the preflight gate's `clone-head-matches-frozen-sha` check), so
drift in this authoring working tree past that SHA does not affect
construction validity as long as content is sourced from the frozen commit.

Per this session's isolation boundary, no other paths under this
repository's other worktrees/branches (e.g. the Path 4 domain-transfer work
visible in recent `origin/main` history) have been or will be inspected —
only the frozen-SHA content of the three named substrate files and the
17-file design package are read.

This working tree (used only for reading frozen-SHA content and authoring
new construction artifacts under `construction/`) is not itself the dispatch
clone and is not required to be clean for that reason.

## 3. Substrate verification at the frozen SHA

The design package names three concrete substrates. All three confirmed
present, at the frozen SHA, with the properties the package relies on:

**T1 — mechanism-routing ambiguity (`workflow-registry.yaml` duplication)**

- `skills/workflow-planner/references/workflow-registry.yaml` (979 lines at
  frozen SHA) vs. `src/sensemaking_skills/defaults/workflow-registry.yaml`
  (885 lines at frozen SHA) — genuinely different content. The `skills/`
  copy contains an `architecture-implementation-workflow` entry (57 lines)
  that the `defaults/` copy lacks entirely. Real, verified drift between the
  two consumers (`scripts/workflow-planner.py` /
  `scripts/_validator_utils.py` vs. `src/sensemaking_skills/registry.py`'s
  `WorkflowRegistry`).

**T2 — semantic state transformation (`artifact-contracts.yaml`)**

- `skills/workflow-planner/references/artifact-contracts.yaml` exists at the
  frozen SHA (687 lines).
- `tests/test_field_contract_agreement.py` exists at the frozen SHA (92
  lines) — the authoritative semantic validator the T2 oracle can invoke.

**T3 — operational recovery (`workflow-runtime.py` `--resume`)**

- `scripts/workflow-runtime.py` at the frozen SHA contains
  `_resumable_terminal_statuses()` (line 1916), `_find_resume_state()` (line
  1951), and the `resume_skip` construction/consumption logic (lines
  2594-2606) that the seven-link recovery chain depends on.

## 4. Mechanical checks

- `bash -n experiments/evaluation-design-e3-autonomous-task-v2/AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`
  → syntax OK.
- R1/R2 shared execution-discipline block: confirmed byte-identical (items
  1-10 of `AUTONOMOUS-TASK-V2-REGIME-R1-LEAN.txt` lines 3-64 vs.
  `AUTONOMOUS-TASK-V2-REGIME-R2-ESCALATION.txt` lines 3-64), matching the
  package's own recorded SHA-256 `a19c6c2c...0cde4c` for both
  (`LOCK-READINESS-RESPONSE-4.md` §1).

## 5. Exit criterion

    HANDOFF VERIFIED

Candidate construction (Phase 1 onward) may proceed.
