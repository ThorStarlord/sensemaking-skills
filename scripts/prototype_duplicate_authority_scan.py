"""
PROTOTYPE (prototype/repo-sensemaker-vnext) -- not wired into validate-repo.py,
CI, or any canonical validator. Demonstration of one item from the "expanded
evidence acquisition" roadmap category: a deterministic, mechanically-decidable
scan for candidate duplicate-authority files (same basename + same relative
suffix path under two different root prefixes).

This directly operationalizes a pattern that mattered twice in this project's
own history: the workflow-orchestrator/ vs skills/workflow-planner/ contract
fork (S1), and the two-parallel-implementation finding in P4. The script only
surfaces candidates -- it does not decide which copy is canonical or whether
a collision is meaningful. That interpretation is repository-diagnostician's
job (mechanically decidable -> script; semantic significance -> model
reasoning), per this repo's own evidence-acquisition principle.

Provenance: prefers `git ls-files` (tracked repository state) when repo_root
is a git repository, falling back to a filesystem walk otherwise. This
matters -- P4's own investigation ("Documentation-count reconciliation")
found that an earlier evidence pass had scanned the working tree including
an untracked .venv/, inflating file counts with workspace noise that was
never part of the tracked product. Scanning "the filesystem" and scanning
"the tracked repository" are different evidence sources with different
trustworthiness, and every result this tool reports says which one it used.

Usage:
    python scripts/prototype_duplicate_authority_scan.py --repo-root .
"""

import argparse
import os
import subprocess
from collections import defaultdict

DEFAULT_EXCLUDE_DIRS = {
    ".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
    ".github", ".claude", "worktrees", "examples", "build", "dist",
    ".reasonix",
}
DEFAULT_EXCLUDE_SUFFIXES = {".pyc"}


def _walk_filesystem(repo_root, exclude_dirs):
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


def _git_ls_files(repo_root):
    """Return tracked file paths (relative, POSIX-style) via `git ls-files`,
    or None if repo_root is not a git repository / git is unavailable.
    Never raises -- absence of git tracking info is a fallback trigger, not
    an error, since this tool must also work in a plain directory."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return paths if paths else None


def find_evidence_files(repo_root, exclude_dirs=None):
    """Return (paths, provenance) where provenance is "git_tracked" (from
    `git ls-files`, the trustworthy case -- matches what's actually part of
    the product per this repo's own tracked-vs-workspace distinction) or
    "filesystem_fallback" (repo_root is not a git repo; results may include
    untracked/workspace files and should be treated as weaker evidence).
    """
    exclude_dirs = exclude_dirs or DEFAULT_EXCLUDE_DIRS

    tracked = _git_ls_files(repo_root)
    if tracked is not None:
        filtered = [
            p for p in tracked
            if not any(part in exclude_dirs for part in p.split("/"))
            and os.path.splitext(p)[1] not in DEFAULT_EXCLUDE_SUFFIXES
        ]
        return filtered, "git_tracked"

    return _walk_filesystem(repo_root, exclude_dirs), "filesystem_fallback"


def find_duplicate_authority_candidates(repo_root, min_suffix_parts=2):
    """Group evidence files by their last `min_suffix_parts` path components
    (e.g. "references/artifact-contracts.yaml"). Any group with more than
    one distinct top-level prefix is a candidate duplicate-authority pair.

    Returns: (candidates, provenance) where candidates is
    {suffix: [rel_path, ...]} for suffixes with 2+ distinct top-level
    prefixes (i.e. genuinely different directory trees, not e.g. two
    sibling skills that legitimately each have their own
    references/weakness-types.md by design -- that distinction is left to
    the caller/model, not decided here), and provenance is "git_tracked" or
    "filesystem_fallback" (see find_evidence_files).
    """
    paths, provenance = find_evidence_files(repo_root)

    by_suffix = defaultdict(list)
    for rel in paths:
        parts = rel.split("/")
        if len(parts) < min_suffix_parts:
            continue
        suffix = "/".join(parts[-min_suffix_parts:])
        by_suffix[suffix].append(rel)

    candidates = {}
    for suffix, suffix_paths in by_suffix.items():
        if len(suffix_paths) < 2:
            continue
        top_prefixes = {p.split("/")[0] for p in suffix_paths}
        if len(top_prefixes) >= 2:
            candidates[suffix] = sorted(suffix_paths)
    return candidates, provenance


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--min-suffix-parts", type=int, default=2,
        help="Number of trailing path components to group by (default 2, "
             "e.g. 'references/foo.md').",
    )
    args = parser.parse_args(argv)

    candidates, provenance = find_duplicate_authority_candidates(
        args.repo_root, args.min_suffix_parts
    )
    provenance_note = (
        "git-tracked repository state"
        if provenance == "git_tracked"
        else "filesystem walk (not a git repo, or git unavailable) -- "
             "may include untracked/workspace files, treat as weaker evidence"
    )
    print(f"Evidence source: {provenance_note}\n")

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
