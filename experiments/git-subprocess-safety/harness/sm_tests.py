"""Exact Sensemaking Git-reading operations, each on a fresh canary repository. Records canary firings."""
import json, subprocess, sys
from pathlib import Path

import os
HERE = Path(os.environ["GITSAFETY_SCRATCH"])  # fixtures go here, never inside the repository
MAKE = Path(__file__).resolve().parent / "make_repo.py"
SRC = Path(__file__).resolve().parents[2] / "src"  # the worktree under test
BOOT = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = ['sensemaking-skills'] + sys.argv[2:]; from sensemaking_skills.cli import main; main()")
D, M, DB = HERE / "d-sm", HERE / "m-sm", HERE / "db"
REPO_ID = "gs-test"
results = {}


def fixture(mode="filter", proposal=False):
    subprocess.run([sys.executable, str(MAKE), str(D), str(M), mode], check=True, capture_output=True)
    if proposal:
        (D / ".sensemaking" / "knowledge").mkdir(parents=True, exist_ok=True)
        (D / ".sensemaking" / "knowledge" / "proposal.json").write_text("{}\n", encoding="utf-8")
    DB.mkdir(exist_ok=True)
    for stale in DB.glob("*.db"):
        stale.unlink()
    return subprocess.run(["git", "-C", str(D), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def run(label, args):
    for p in list(M.iterdir()) if M.exists() else []:
        p.unlink()
    proc = subprocess.run([sys.executable, "-c", BOOT, str(SRC), *args], capture_output=True, text=True,
                          timeout=300, cwd=str(HERE))
    fired = sorted(p.name for p in M.iterdir()) if M.exists() else []
    lines = proc.stderr.strip().splitlines()
    err = lines[-1][:150] if lines else ""
    results[label] = {"exit": proc.returncode, "canaries_fired": fired, "last_stderr": err}
    print(f"{label:26s} exit={proc.returncode:<3} fired={fired} | {err[:110]}", flush=True)


# 1. Active-checkout build (dirty-check neutralised in worktree_context).
head = fixture("filter")
run("knowledge_build_active", ["semantic", "knowledge-build", "--repo", str(D), "--repository", REPO_ID,
    "--target-ref", head, "--db", str(DB / "active.db"), "--json"])
# 2. Temporary-checkout build on a filter-attributed repo (refused after checkout; filters disabled).
head = fixture("filter")
run("knowledge_build_temp_filter", ["semantic", "knowledge-build", "--repo", str(D), "--repository", REPO_ID,
    "--target-ref", head, "--db", str(DB / "temp.db"), "--temporary-checkout", "--json"])
# 3. Temporary-checkout build, no filter attributes, then audit and query on that index.
head = fixture("nofilter")
run("knowledge_build_temp_nofilter", ["semantic", "knowledge-build", "--repo", str(D), "--repository", REPO_ID,
    "--target-ref", head, "--db", str(DB / "temp.db"), "--temporary-checkout", "--json"])
run("knowledge_audit_temp", ["semantic", "knowledge-audit", "--db", str(DB / "temp.db"), "--repo", str(D),
    "--repository", REPO_ID, "--indexed-ref", head, "--current-ref", head, "--temporary-checkout", "--json"])
run("knowledge_query_repo", ["semantic", "knowledge-query", "--db", str(DB / "temp.db"), "--repository", REPO_ID,
    "--target-ref", head, "--operation", "snapshot", "--repo", str(D), "--json"])
# 4. Unguarded status callers.
head = fixture("filter")
run("impact_preview", ["semantic", "impact-preview", "--repo", str(D), "--target-ref", head,
    "--subject", "notes", "--json"])
head = fixture("filter", proposal=True)
run("proposal_check", ["semantic", "knowledge-proposal-check", "--repo", str(D),
    "--proposal", str(D / ".sensemaking" / "knowledge" / "proposal.json"), "--json"])
head = fixture("filter")
run("release_audit", ["release", "audit", "--repo-root", str(D), "--json"])
(HERE / "sm_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print("saved", HERE / "sm_results.json")
