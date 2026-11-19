"""Name the code that is executing, for ``--version``.

The package version string stays the same across many commits, so it cannot
tell two revisions apart. An editable install from a checkout that lags behind,
or a tool installed from an older commit, then runs older code with no visible
sign. This module reports where the imported package lives and, when it can,
the commit those files come from.

A commit is named only when it names the executing bytes: a Git checkout whose
package directory has no uncommitted or untracked change, or an installed
distribution whose PEP 610 ``direct_url.json`` records a VCS commit. Otherwise
no commit is named; it is never inferred. Git reads disable fsmonitor, external
filters and repository hooks.
"""
from __future__ import annotations

import json
import re
from importlib import metadata
from pathlib import Path

_DISTRIBUTION = "sensemaking-skills"
_COMMIT = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


def _checkout_line(package_dir: Path) -> str | None:
    """Describe a package directory that is tracked source in a Git checkout."""
    from .semantic_architecture.worktree_context import guarded_git_text

    try:
        # A package under an untracked or ignored directory (a virtualenv inside a
        # project checkout, for example) is not that checkout's source.
        if not guarded_git_text(package_dir, "ls-files", "-z", "--", "__init__.py").strip("\x00"):
            return None
        status = guarded_git_text(
            package_dir, "status", "--porcelain=v1", "--untracked-files=all",
            "--ignore-submodules=all", "-z", "--", ".",
        )
        head = guarded_git_text(package_dir, "rev-parse", "--verify", "HEAD").strip()
    except (ValueError, OSError):
        return None
    if not _COMMIT.fullmatch(head):
        return None
    if status.strip("\x00"):
        return (
            "code commit: none named (Git checkout at HEAD "
            f"{head} has uncommitted or untracked changes in the package directory)"
        )
    return f"code commit: {head} (Git checkout, package directory unchanged)"


def _installed_vcs_line(package_dir: Path) -> str | None:
    """Describe an installed distribution whose installer recorded a VCS commit."""
    try:
        dist = metadata.distribution(_DISTRIBUTION)
        located = Path(str(dist.locate_file("sensemaking_skills/__init__.py"))).resolve()
        if located != (package_dir / "__init__.py").resolve():
            return None  # the imported code is not this distribution's installed copy
        raw = dist.read_text("direct_url.json")
        info = json.loads(raw) if raw else None
    except (metadata.PackageNotFoundError, OSError, ValueError):
        return None
    vcs = info.get("vcs_info") if isinstance(info, dict) else None
    commit = vcs.get("commit_id") if isinstance(vcs, dict) else None
    if not isinstance(commit, str) or not _COMMIT.fullmatch(commit):
        return None
    return f"code commit: {commit} (recorded by the installer; later edits are not detected)"


def code_provenance_lines(package_dir: Path | None = None) -> list[str]:
    """Return ASCII-safe lines naming the executing package and, if known, its commit."""
    package_dir = (package_dir or Path(__file__).parent).resolve()
    commit_line = (
        _checkout_line(package_dir)
        or _installed_vcs_line(package_dir)
        or "code commit: none named (no clean Git checkout or installer VCS record)"
    )
    location = str(package_dir).encode("ascii", "backslashreplace").decode("ascii")
    return [f"code: {location}", commit_line]
