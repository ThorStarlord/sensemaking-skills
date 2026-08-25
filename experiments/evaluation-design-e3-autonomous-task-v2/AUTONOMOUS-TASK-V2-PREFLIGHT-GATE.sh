#!/usr/bin/env bash
# Autonomous Task v2 — Preflight Gate
#
# Status: DRAFT tooling for a DESIGN-ONLY task. This script performs
# mechanical checks that should pass before any pilot or main-study run is
# dispatched. It does NOT dispatch, run, or score a benchmark task, and it
# must never be invoked with that intent.
#
# Scope discipline: this script only reads repository/clone state and writes
# to the isolated output directory passed via --out-dir (default: a
# subdirectory of this script's own location). It never modifies tracked
# repository files.
#
# Usage:
#   AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh \
#     --clone-dir <path to standalone clone under test> \
#     --frozen-sha <expected frozen commit SHA> \
#     [--out-dir <path for preflight report + logs>] \
#     [--regime-dir <path containing the three REGIME-*.txt files>] \
#     [--sibling-allowlist <path to a file listing approved sibling names>] \
#     [--run-state-dir <path the dispatched run will write into>] \
#     [--task-bundle <path to the task-visible contract file for this run>] \
#     [--task-bundle-sha256 <expected sha256 of --task-bundle>] \
#     [--oracle-self-test-command <shell command that runs the oracle's own
#         self-test>] \
#     [--expected-oracle-self-test-sha <expected sha256 of that command's
#         stdout>]
#
# DISPATCH MODE vs. DESIGN-TIME MODE: added in Lock-Readiness Response 2
# §7 — a reviewer found that run-state-dir-is-fresh, oracle-self-test, and
# task-bundle-excludes-evaluator-artifacts were UNCONDITIONALLY
# UNVERIFIABLE, which (combined with UNVERIFIABLE blocking a zero exit)
# meant this script could never return 0 for a real dispatch invocation no
# matter what was supplied. The five arguments above let a real dispatch
# invocation supply concrete, checkable inputs so those three checks can
# become PASS/FAIL instead of only ever UNVERIFIABLE. Omitting an argument
# at design time (nothing to check yet) still yields UNVERIFIABLE for that
# specific check — the fail-closed default is unchanged, just no longer
# permanent.
#
# Added by the Pre-Lock Ambient-Environment Audit
# (AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md): checks 5b-5d below detect
# two exposure vectors that audit found undetected by the original script —
# (1) a local-filesystem git remote URL in the clone's .git/config, which
# reveals the path to whatever directory the clone was made from regardless
# of where the clone itself is later placed, and (2) an uncrowded-parent
# check so an unapproved sibling directory (this repo already has ~80
# pre-existing sibling directories/worktrees in its default parent
# directory, several with names suggestive of prior benchmark structure)
# cannot sit next to the clone unnoticed. Both checks are name-agnostic —
# they do not hardcode any specific sibling's name.
#
# Exit code 0 means every mechanically-checkable condition passed. Exit
# code 1 means at least one check failed or could not be verified. This
# script intentionally FAILS CLOSED: a condition it cannot check is reported
# as UNVERIFIABLE and counts as a non-pass, never silently skipped as a pass.

set -u
set -o pipefail

CLONE_DIR=""
FROZEN_SHA=""
OUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/preflight-runs"
REGIME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIBLING_ALLOWLIST=""
RUN_STATE_DIR=""
TASK_BUNDLE=""
TASK_BUNDLE_SHA256=""
ORACLE_SELF_TEST_COMMAND=""
EXPECTED_ORACLE_SELF_TEST_SHA=""

while [ $# -gt 0 ]; do
  case "$1" in
    --clone-dir) CLONE_DIR="$2"; shift 2 ;;
    --frozen-sha) FROZEN_SHA="$2"; shift 2 ;;
    --out-dir) OUT_DIR="$2"; shift 2 ;;
    --regime-dir) REGIME_DIR="$2"; shift 2 ;;
    --sibling-allowlist) SIBLING_ALLOWLIST="$2"; shift 2 ;;
    --run-state-dir) RUN_STATE_DIR="$2"; shift 2 ;;
    --task-bundle) TASK_BUNDLE="$2"; shift 2 ;;
    --task-bundle-sha256) TASK_BUNDLE_SHA256="$2"; shift 2 ;;
    --oracle-self-test-command) ORACLE_SELF_TEST_COMMAND="$2"; shift 2 ;;
    --expected-oracle-self-test-sha) EXPECTED_ORACLE_SELF_TEST_SHA="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$CLONE_DIR" ] || [ -z "$FROZEN_SHA" ]; then
  echo "Usage: $0 --clone-dir <path> --frozen-sha <sha> [--out-dir <path>] [--regime-dir <path>]" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
REPORT="$OUT_DIR/preflight-report-$(date -u +%Y%m%dT%H%M%SZ).txt"

PASS_COUNT=0
FAIL_COUNT=0
UNVERIFIABLE_COUNT=0

record() {
  # record <STATUS> <check-name> <detail>
  local status="$1" name="$2" detail="$3"
  printf '%-14s %-40s %s\n' "$status" "$name" "$detail" | tee -a "$REPORT"
  case "$status" in
    PASS) PASS_COUNT=$((PASS_COUNT + 1)) ;;
    FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)) ;;
    UNVERIFIABLE) UNVERIFIABLE_COUNT=$((UNVERIFIABLE_COUNT + 1)) ;;
    # ENV_LIMIT is deliberately NOT counted toward PASS/FAIL/UNVERIFIABLE:
    # it discloses a condition this script cannot control (execution-
    # environment sandboxing) rather than judging the clone itself. It must
    # never be silently omitted — see ambient-scope-runtime-enforcement below.
  esac
}

echo "Autonomous Task v2 preflight — $(date -u +%FT%TZ)" | tee "$REPORT"
echo "clone_dir=$CLONE_DIR frozen_sha=$FROZEN_SHA" | tee -a "$REPORT"
echo "---" | tee -a "$REPORT"

# 1. Clone exists and is a git repository.
if [ -d "$CLONE_DIR/.git" ] || git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  record PASS "clone-is-git-repo" "$CLONE_DIR"
else
  record FAIL "clone-is-git-repo" "$CLONE_DIR is not a git working tree"
fi

# 2. Clone HEAD matches the frozen SHA exactly (not merely an ancestor —
#    a benchmark run must sit AT the frozen revision, not somewhere past it).
if git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  ACTUAL_SHA="$(git -C "$CLONE_DIR" rev-parse HEAD 2>/dev/null || echo "")"
  if [ "$ACTUAL_SHA" = "$FROZEN_SHA" ]; then
    record PASS "clone-head-matches-frozen-sha" "$ACTUAL_SHA"
  else
    record FAIL "clone-head-matches-frozen-sha" "HEAD=$ACTUAL_SHA expected=$FROZEN_SHA"
  fi
else
  record UNVERIFIABLE "clone-head-matches-frozen-sha" "clone not accessible as a git repo"
fi

# 3. No tracked modifications in the clone (clean working tree).
if git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  DIRTY="$(git -C "$CLONE_DIR" status --porcelain 2>/dev/null)"
  if [ -z "$DIRTY" ]; then
    record PASS "clone-working-tree-clean" "no tracked modifications"
  else
    record FAIL "clone-working-tree-clean" "$(echo "$DIRTY" | wc -l) dirty entries"
  fi
else
  record UNVERIFIABLE "clone-working-tree-clean" "clone not accessible as a git repo"
fi

# 4. Clone is standalone — not a worktree sharing .git with another checkout.
#    This is a heuristic, not a proof: it only checks whether .git is a
#    linked-worktree pointer file rather than a real directory. It cannot
#    rule out two independent full clones sharing a filesystem-level cache.
if [ -f "$CLONE_DIR/.git" ]; then
  record FAIL "clone-is-standalone-not-worktree" ".git is a worktree pointer file, not a full clone"
elif [ -d "$CLONE_DIR/.git" ]; then
  record PASS "clone-is-standalone-not-worktree" ".git is a real directory"
else
  record UNVERIFIABLE "clone-is-standalone-not-worktree" "could not inspect .git"
fi

# 5. Sibling-experiment leakage — checkable only within this repo's own
#    ambient filesystem conventions (experiments/, artifacts/), and only as
#    a heuristic: absence of known sibling directory names inside the clone.
#    This does NOT prove filesystem isolation; see NOT TECHNICALLY CLOSED
#    note at the bottom of this script.
if [ -d "$CLONE_DIR" ]; then
  LEAK_HITS="$(find "$CLONE_DIR/experiments" -maxdepth 1 -iname "*autonomous-task-v2*" 2>/dev/null)"
  if [ -z "$LEAK_HITS" ]; then
    record PASS "no-known-sibling-experiment-dirs" "none found under $CLONE_DIR/experiments"
  else
    record FAIL "no-known-sibling-experiment-dirs" "$LEAK_HITS"
  fi
else
  record UNVERIFIABLE "no-known-sibling-experiment-dirs" "clone dir not found"
fi

# 5b. Clone's git remote(s) must not point at a local filesystem path.
#     A clone made via `git clone <local-path>` retains that path in
#     .git/config regardless of where the clone is later moved to, and an
#     agent with ordinary read access to its own .git/config can follow it
#     straight to whatever directory (and siblings) the clone came from.
#     Demonstrated finding, not a hypothetical: see
#     AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md §2b.
if git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  REMOTE_URLS="$(git -C "$CLONE_DIR" remote -v 2>/dev/null | awk '{print $2}' | sort -u)"
  LOCAL_PATH_REMOTES=""
  if [ -n "$REMOTE_URLS" ]; then
    while IFS= read -r url; do
      case "$url" in
        http://*|https://*|ssh://*|git://*|*@*:*) : ;; # network-style, OK
        "") : ;;
        *) LOCAL_PATH_REMOTES="$LOCAL_PATH_REMOTES $url" ;;
      esac
    done <<EOF
$REMOTE_URLS
EOF
  fi
  if [ -z "$LOCAL_PATH_REMOTES" ]; then
    record PASS "clone-remote-has-no-local-path" "no local-filesystem-path remotes configured"
  else
    record FAIL "clone-remote-has-no-local-path" "local-path remote(s) found:$LOCAL_PATH_REMOTES"
  fi
else
  record UNVERIFIABLE "clone-remote-has-no-local-path" "clone not accessible as a git repo"
fi

# 5c. Clone's own `git worktree list` must show exactly one entry (itself).
#     Catches both "this is actually a `git worktree add`, not a real
#     clone" and any other way the clone ended up administratively linked
#     to a shared .git. A real standalone clone always passes this; a
#     linked worktree never does.
if git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  WT_COUNT="$(git -C "$CLONE_DIR" worktree list 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$WT_COUNT" = "1" ]; then
    record PASS "clone-worktree-list-shows-self-only" "1 entry"
  else
    record FAIL "clone-worktree-list-shows-self-only" "$WT_COUNT entries — clone is administratively linked to other worktrees"
  fi
else
  record UNVERIFIABLE "clone-worktree-list-shows-self-only" "clone not accessible as a git repo"
fi

# 5d. Clone's immediate parent directory must contain nothing besides the
#     clone itself, unless every extra entry is on an explicit allowlist.
#     Generic and name-agnostic by design: it does not need to know any
#     specific sibling's name to flag an unapproved neighbor. See
#     AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md §2a for why this
#     matters (the default parent directory in this repository's own
#     environment currently has on the order of 80 other entries in it).
if [ -d "$CLONE_DIR" ]; then
  PARENT_DIR="$(dirname "$CLONE_DIR")"
  CLONE_BASENAME="$(basename "$CLONE_DIR")"
  # find -mindepth 1 -maxdepth 1 (not `ls -1`, which silently skips
  # dotfiles/dot-directories and would let a hidden sibling evade this
  # check entirely -- fixed per Lock-Readiness Response 2 §7).
  EXTRA_ENTRIES="$(find "$PARENT_DIR" -mindepth 1 -maxdepth 1 -exec basename {} \; 2>/dev/null | grep -v -x -F "$CLONE_BASENAME")"
  if [ -n "$SIBLING_ALLOWLIST" ] && [ -f "$SIBLING_ALLOWLIST" ]; then
    UNAPPROVED=""
    while IFS= read -r entry; do
      [ -z "$entry" ] && continue
      if ! grep -q -x -F "$entry" "$SIBLING_ALLOWLIST" 2>/dev/null; then
        UNAPPROVED="$UNAPPROVED $entry"
      fi
    done <<EOF
$EXTRA_ENTRIES
EOF
    EXTRA_ENTRIES="$UNAPPROVED"
  fi
  EXTRA_ENTRIES="$(echo "$EXTRA_ENTRIES" | sed '/^[[:space:]]*$/d')"
  if [ -z "$EXTRA_ENTRIES" ]; then
    record PASS "clone-parent-directory-is-uncrowded" "no unapproved entries in $PARENT_DIR"
  else
    ENTRY_COUNT="$(echo "$EXTRA_ENTRIES" | wc -l | tr -d ' ')"
    record FAIL "clone-parent-directory-is-uncrowded" "$ENTRY_COUNT unapproved entries in $PARENT_DIR"
  fi
else
  record UNVERIFIABLE "clone-parent-directory-is-uncrowded" "clone dir not found"
fi

# 5e. Clone must not have an alternate-object-store reference (created by
#     `git clone --shared` / `--reference`), which would make the clone
#     depend on, and be able to reveal the path to, its source repository's
#     object store even after the origin remote is stripped (check 5b).
if [ -d "$CLONE_DIR" ]; then
  GIT_DIR="$(git -C "$CLONE_DIR" rev-parse --git-dir 2>/dev/null)"
  if [ -n "$GIT_DIR" ]; then
    case "$GIT_DIR" in
      /*|?:*) ALT_PATH="$GIT_DIR/objects/info/alternates" ;;
      *) ALT_PATH="$CLONE_DIR/$GIT_DIR/objects/info/alternates" ;;
    esac
    if [ -f "$ALT_PATH" ]; then
      record FAIL "clone-no-alternate-object-store" "found: $ALT_PATH (contents not read; presence alone is disqualifying)"
    else
      record PASS "clone-no-alternate-object-store" "no alternates file present"
    fi
  else
    record UNVERIFIABLE "clone-no-alternate-object-store" "could not resolve git-dir"
  fi
else
  record UNVERIFIABLE "clone-no-alternate-object-store" "clone dir not found"
fi

# 5f. Clone's git-common-dir must resolve to the clone's own .git — a
#     strictly more general replacement for check 4's file-vs-directory
#     heuristic: this catches linked worktrees, external `commondir` files,
#     and any other mechanism that would point the clone's git metadata
#     back at a shared location, by construction rather than by
#     enumerating known cases. Added per
#     AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md §Issue 3.
if git -C "$CLONE_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  COMMON_DIR="$(git -C "$CLONE_DIR" rev-parse --git-common-dir 2>/dev/null)"
  case "$COMMON_DIR" in
    /*|?:*) COMMON_DIR_ABS="$COMMON_DIR" ;;
    *) COMMON_DIR_ABS="$CLONE_DIR/$COMMON_DIR" ;;
  esac
  COMMON_DIR_NORM="$(cd "$COMMON_DIR_ABS" 2>/dev/null && pwd)"
  EXPECTED_NORM="$(cd "$CLONE_DIR/.git" 2>/dev/null && pwd)"
  if [ -n "$COMMON_DIR_NORM" ] && [ "$COMMON_DIR_NORM" = "$EXPECTED_NORM" ]; then
    record PASS "clone-common-dir-is-self" "$COMMON_DIR_NORM"
  else
    record FAIL "clone-common-dir-is-self" "common-dir=$COMMON_DIR_NORM expected=$EXPECTED_NORM (clone is administratively linked elsewhere)"
  fi
else
  record UNVERIFIABLE "clone-common-dir-is-self" "clone not accessible as a git repo"
fi

# 6. Regime prompt files present and hashed (for regime_prompt_hash telemetry).
for regime in R0-ROBUST R1-LEAN R2-ESCALATION; do
  f="$REGIME_DIR/AUTONOMOUS-TASK-V2-REGIME-${regime}.txt"
  if [ -f "$f" ]; then
    h="$(sha256sum "$f" 2>/dev/null | awk '{print $1}')"
    record PASS "regime-file-present:$regime" "sha256=$h"
  else
    record FAIL "regime-file-present:$regime" "missing: $f"
  fi
done

# 7. Telemetry destination writable.
if touch "$OUT_DIR/.write-test" 2>/dev/null; then
  rm -f "$OUT_DIR/.write-test"
  record PASS "telemetry-destination-writable" "$OUT_DIR"
else
  record FAIL "telemetry-destination-writable" "$OUT_DIR"
fi

# 8. Run-state directory freshness. DISPATCH MODE (--run-state-dir given):
#    real check -- PASS iff the directory is absent or empty, FAIL if it
#    already contains entries (stale state from a prior run). DESIGN-TIME
#    MODE (no argument): UNVERIFIABLE, honestly, since there is nothing yet
#    to check.
if [ -n "$RUN_STATE_DIR" ]; then
  if [ ! -e "$RUN_STATE_DIR" ]; then
    record PASS "run-state-dir-is-fresh" "$RUN_STATE_DIR does not exist yet (fresh)"
  elif [ -d "$RUN_STATE_DIR" ] && [ -z "$(find "$RUN_STATE_DIR" -mindepth 1 -maxdepth 1 2>/dev/null)" ]; then
    record PASS "run-state-dir-is-fresh" "$RUN_STATE_DIR exists and is empty"
  else
    record FAIL "run-state-dir-is-fresh" "$RUN_STATE_DIR already contains entries -- stale state from a prior run"
  fi
else
  record UNVERIFIABLE "run-state-dir-is-fresh" "no --run-state-dir supplied -- design-time invocation, nothing yet to check; supply --run-state-dir at real dispatch time"
fi

# 9. Oracle self-test. DISPATCH MODE (both --oracle-self-test-command and
#    --expected-oracle-self-test-sha given): runs the command, hashes its
#    stdout, compares against the expected hash. DESIGN-TIME MODE: no
#    oracle exists yet at design time (main-study instances are explicitly
#    not constructed by this design pass) -- UNVERIFIABLE, honestly.
if [ -n "$ORACLE_SELF_TEST_COMMAND" ] && [ -n "$EXPECTED_ORACLE_SELF_TEST_SHA" ]; then
  ACTUAL_ORACLE_SHA="$(eval "$ORACLE_SELF_TEST_COMMAND" 2>/dev/null | sha256sum | awk '{print $1}')"
  if [ "$ACTUAL_ORACLE_SHA" = "$EXPECTED_ORACLE_SELF_TEST_SHA" ]; then
    record PASS "oracle-self-test" "self-test output matches expected sha256=$ACTUAL_ORACLE_SHA"
  else
    record FAIL "oracle-self-test" "self-test output sha256=$ACTUAL_ORACLE_SHA expected=$EXPECTED_ORACLE_SELF_TEST_SHA"
  fi
else
  record UNVERIFIABLE "oracle-self-test" "no --oracle-self-test-command/--expected-oracle-self-test-sha supplied -- design-time invocation; supply both at real dispatch time once a task instance's oracle exists"
fi

# 10. Task bundle matches its frozen hash. RENAMED from
#     task-bundle-excludes-evaluator-artifacts (Lock-Readiness Response 3
#     §10 item 6 -- a reviewer correctly pointed out that name overclaimed:
#     a bundle contaminated with evaluator-only content BEFORE the hash was
#     taken would still match its own (contaminated) hash. This check only
#     proves the bundle has not changed SINCE the hash was recorded — it
#     does NOT prove the bundle was clean when the hash was taken. A
#     separate, one-time pre-lock bundle-separation audit (a human/process
#     review confirming the agent-visible bundle actually excludes
#     evaluator-only content) is a required prerequisite BEFORE this hash is
#     taken; this script cannot perform that audit itself. DISPATCH MODE
#     (both --task-bundle and --task-bundle-sha256 given): real hash-match
#     check. DESIGN-TIME MODE: no task bundle exists yet -- UNVERIFIABLE,
#     honestly.
if [ -n "$TASK_BUNDLE" ] && [ -n "$TASK_BUNDLE_SHA256" ]; then
  if [ -f "$TASK_BUNDLE" ]; then
    ACTUAL_BUNDLE_SHA="$(sha256sum "$TASK_BUNDLE" 2>/dev/null | awk '{print $1}')"
    if [ "$ACTUAL_BUNDLE_SHA" = "$TASK_BUNDLE_SHA256" ]; then
      record PASS "task-bundle-matches-frozen-hash" "task bundle sha256 matches expected: $ACTUAL_BUNDLE_SHA"
    else
      record FAIL "task-bundle-matches-frozen-hash" "task bundle sha256=$ACTUAL_BUNDLE_SHA expected=$TASK_BUNDLE_SHA256 -- bundle differs from its frozen, recorded form"
    fi
  else
    record FAIL "task-bundle-matches-frozen-hash" "--task-bundle path does not exist: $TASK_BUNDLE"
  fi
else
  record UNVERIFIABLE "task-bundle-matches-frozen-hash" "no --task-bundle/--task-bundle-sha256 supplied -- design-time invocation, no task bundle exists yet; supply both at real dispatch time"
fi

# 11. Ambient-scope runtime enforcement — always reported, never silently
#     omitted. Checks 5b-5d above verify the clone's configuration and
#     immediate surroundings AT PREFLIGHT TIME. None of them, individually
#     or together, prove the live agent harness's filesystem access is
#     actually bounded to the clone root DURING the run — that is a
#     property of container/sandbox-level isolation this script has no
#     power to inspect or enforce. Reporting a clean PASS on 5b-5d as if it
#     meant "isolation confirmed" would be exactly the false-green failure
#     the ambient-isolation audit warned against.
record ENV_LIMIT "ambient-scope-runtime-enforcement" "AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED — this script cannot verify or enforce that the executing agent's filesystem access is bounded to \$CLONE_DIR during the run; verify via the harness/sandbox layer, not this script"

echo "---" | tee -a "$REPORT"
echo "PASS=$PASS_COUNT FAIL=$FAIL_COUNT UNVERIFIABLE=$UNVERIFIABLE_COUNT" | tee -a "$REPORT"
echo "Report written to: $REPORT" | tee -a "$REPORT"

# NOT TECHNICALLY CLOSED: this script mitigates and audits several isolation
# risks but does not prove full filesystem isolation (per M4 in the supplied
# prior-work provenance, and per AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md
# which found two concrete, previously-undetected exposure vectors and added
# checks 5b-5d above to catch them). Checks 4 and 5 remain heuristics. A FAIL
# or UNVERIFIABLE result on any check MUST BLOCK DISPATCH UNCONDITIONALLY —
# there is no waiver path. (A "human waiver" escape hatch was removed here
# per Lock-Readiness Response 3 §10 item 7: a fail-closed dispatch gate
# should not offer one, and the one honest, permanent limitation this
# script cannot close is already correctly carried by the always-reported
# ENV_LIMIT line below, which is a disclosure, not something a checkbox can
# dismiss.) Resolve the underlying condition, or reduce scope (e.g. drop a
# family via the frozen fallback), never wave a FAIL/UNVERIFIABLE through.
# The ENV_LIMIT line (check 11) is not a failure and does not block dispatch
# by itself — it is a permanent disclosure, present in every run of this
# script, that no combination of PASS results above amounts to a proof of
# runtime filesystem sandboxing.

if [ "$FAIL_COUNT" -gt 0 ] || [ "$UNVERIFIABLE_COUNT" -gt 0 ]; then
  exit 1
fi
exit 0
