"""
PROTOTYPE (prototype/repo-sensemaker-vnext) -- not wired into validate-repo.py,
CI, or any canonical validator.

Formalizes the P4 ".venv correction" as a reusable, deterministic check:
"25 of the 30 .md files live under .venv/... This scan described the
broader tree, not the product surface" (P4 learning-v1.md). That correction
was made by hand, once. This tool makes the underlying comparison
(workspace total vs. git-tracked subset) mechanically repeatable for any
subdirectory, so future evidence-gathering doesn't have to rediscover it.

Usage:
    python scripts/prototype_tracked_vs_workspace_scan.py --repo-root . --subdir .
"""

import argparse
import os
import subprocess

DEFAULT_EXCLUDE_DIRS = {".git"}


def _walk_all_files(root):
    results = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDE_DIRS]
        for f in files:
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            results.append(rel)
    return results


def _git_tracked_files(repo_root, subdir):
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", subdir],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def compare_tracked_vs_workspace(repo_root, subdir="."):
    """Compare git-tracked files under `subdir` to everything physically
    present on disk under the same subdir.

    Returns a dict:
        tracked_count: int
        workspace_count: int  (everything on disk, tracked or not)
        untracked_count: int
        untracked_ratio: float (0.0-1.0; 0.0 if workspace_count is 0)
        untracked_top_level_dirs: sorted list of first-path-component dirs
            that contain ANY untracked file (candidate workspace-noise
            sources, e.g. ".venv", "node_modules") -- not a full listing,
            just enough to say where to look.
        is_git_repo: bool -- False means "tracked" has no meaning here;
            all counts describe the filesystem only.
    """
    abs_subdir = os.path.join(repo_root, subdir) if subdir != "." else repo_root
    # _walk_all_files returns paths relative to abs_subdir; re-root them
    # relative to repo_root (POSIX-style) so they compare directly against
    # `git ls-files`' output, which is always repo-root-relative.
    workspace_files = {
        f"{subdir.rstrip('/')}/{f}" if subdir != "." else f
        for f in _walk_all_files(abs_subdir)
    }

    tracked = _git_tracked_files(repo_root, subdir)
    if tracked is None:
        return {
            "is_git_repo": False,
            "tracked_count": 0,
            "workspace_count": len(workspace_files),
            "untracked_count": len(workspace_files),
            "untracked_ratio": 1.0 if workspace_files else 0.0,
            "untracked_top_level_dirs": sorted({
                f.split("/")[0] for f in workspace_files if "/" in f
            }),
        }

    tracked_set = set(tracked)
    untracked = workspace_files - tracked_set
    ratio = (len(untracked) / len(workspace_files)) if workspace_files else 0.0
    return {
        "is_git_repo": True,
        "tracked_count": len(tracked_set),
        "workspace_count": len(workspace_files),
        "untracked_count": len(untracked),
        "untracked_ratio": ratio,
        "untracked_top_level_dirs": sorted({
            f.split("/")[0] for f in untracked if "/" in f
        }),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--subdir", default=".")
    parser.add_argument(
        "--warn-ratio", type=float, default=0.3,
        help="Print a warning if untracked_ratio exceeds this (default 0.3).",
    )
    args = parser.parse_args(argv)

    result = compare_tracked_vs_workspace(args.repo_root, args.subdir)
    print(f"Subdirectory: {args.subdir}")
    print(f"Git repository: {result['is_git_repo']}")
    print(f"Tracked files: {result['tracked_count']}")
    print(f"Workspace files (on disk): {result['workspace_count']}")
    print(f"Untracked files: {result['untracked_count']}")
    print(f"Untracked ratio: {result['untracked_ratio']:.1%}")
    if result["untracked_top_level_dirs"]:
        print(f"Untracked top-level dirs: {', '.join(result['untracked_top_level_dirs'])}")

    if result["untracked_ratio"] > args.warn_ratio:
        print(
            f"\nWARNING: untracked ratio ({result['untracked_ratio']:.1%}) exceeds "
            f"{args.warn_ratio:.0%} -- evidence gathered against the raw workspace "
            "here likely describes local environment noise, not the tracked product "
            "(the P4 .venv pattern). Prefer `git ls-files`-scoped evidence."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
