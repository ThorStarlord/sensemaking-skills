"""
PROTOTYPE (prototype/repo-sensemaker-vnext) -- not wired into validate-repo.py,
CI, or any canonical validator. Demonstration of one item from the "expanded
evidence acquisition" roadmap category: a deterministic, mechanically-decidable
scan for candidate duplicate-authority files (same basename + same relative
suffix path under two different root prefixes in the tracked tree).

This directly operationalizes a pattern that mattered twice in this project's
own history: the workflow-orchestrator/ vs skills/workflow-planner/ contract
fork (S1), and the two-parallel-implementation finding in P4. The script only
surfaces candidates -- it does not decide which copy is canonical or whether
a collision is meaningful. That interpretation is repository-diagnostician's
job (mechanically decidable -> script; semantic significance -> model
reasoning), per this repo's own evidence-acquisition principle.

Usage:
    python scripts/prototype_duplicate_authority_scan.py --repo-root .
"""

import argparse
import os
from collections import defaultdict

DEFAULT_EXCLUDE_DIRS = {
    ".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
    ".github", ".claude", "worktrees", "examples", "build", "dist",
    ".reasonix",
}
DEFAULT_EXCLUDE_SUFFIXES = {".pyc"}


def find_tracked_files(repo_root, exclude_dirs=None):
    """Walk repo_root, returning relative POSIX-style paths, skipping
    excluded directories. Deliberately filesystem-based, not git-based --
    this is meant to run against any directory (including a worktree),
    not require a git context."""
    exclude_dirs = exclude_dirs or DEFAULT_EXCLUDE_DIRS
    results = []
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if os.path.splitext(f)[1] in DEFAULT_EXCLUDE_SUFFIXES:
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, repo_root).replace(os.sep, "/")
            results.append(rel)
    return results


def find_duplicate_authority_candidates(repo_root, min_suffix_parts=2):
    """Group tracked files by their last `min_suffix_parts` path components
    (e.g. "references/artifact-contracts.yaml"). Any group with more than
    one distinct top-level prefix is a candidate duplicate-authority pair.

    Returns: {suffix: [rel_path, ...]} for suffixes with 2+ distinct
    top-level prefixes (i.e. genuinely different directory trees, not
    e.g. two sibling skills that legitimately each have their own
    references/weakness-types.md by design -- that distinction is left to
    the caller/model, not decided here).
    """
    by_suffix = defaultdict(list)
    for rel in find_tracked_files(repo_root):
        parts = rel.split("/")
        if len(parts) < min_suffix_parts:
            continue
        suffix = "/".join(parts[-min_suffix_parts:])
        by_suffix[suffix].append(rel)

    candidates = {}
    for suffix, paths in by_suffix.items():
        if len(paths) < 2:
            continue
        top_prefixes = {p.split("/")[0] for p in paths}
        if len(top_prefixes) >= 2:
            candidates[suffix] = sorted(paths)
    return candidates


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--min-suffix-parts", type=int, default=2,
        help="Number of trailing path components to group by (default 2, "
             "e.g. 'references/foo.md').",
    )
    args = parser.parse_args(argv)

    candidates = find_duplicate_authority_candidates(
        args.repo_root, args.min_suffix_parts
    )
    if not candidates:
        print("No candidate duplicate-authority files found.")
        return 0

    print(f"{len(candidates)} candidate duplicate-authority suffix(es) found:\n")
    for suffix, paths in sorted(candidates.items()):
        print(f"  {suffix}")
        for p in paths:
            print(f"    - {p}")
    print(
        "\nThese are candidates only -- same basename in two different "
        "directory trees, nothing more. Whether this represents real "
        "duplicate authority (vs. two skills legitimately having their own "
        "same-named reference file) is a semantic judgment, not made here."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
