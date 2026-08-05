"""Materialized, sealed target checkout (Phase 6 correction, #122).

The provider must analyze the EXACT approved target revision, not a URL
and SHA embedded in prompt text. ``TargetCheckout.prepare`` materializes
the approved repository locally and proves, before any attempt is
reserved, that the checkout IS the approved target:

* the ``origin`` remote, normalized, equals the approved target repository;
* ``HEAD`` is exactly the approved target SHA;
* the index and working tree are clean;
* there are no untracked files (an untracked file could silently alter
  the analysis);
* there are no submodules and no ``.gitmodules`` file (submodule drift
  could silently change what the model reads).

Policy for existing directories: a checkout that already exists is reused
ONLY when it passes every check; otherwise the runner refuses. The
materializer never silently fetches, checks out, mutates, or "fixes" an
existing checkout -- the approved bytes must already be on disk, exactly.

The checkout is exposed to the provider as a read root. Real read-only
enforcement on Windows is limited (no reliable chmod), so the primary
confinement is mechanical: the provider's SDK tool envelope is
Read/Glob/Grep only -- there is no Write tool, no Bash tool, and no
filesystem-mutating capability inside the provider boundary. The runner
re-verifies checkout integrity immediately before every attempt.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .production_verifier import _norm_repo_url


class TargetCheckoutError(Exception):
    """The target checkout cannot be proven to be the approved target."""


class TargetCheckout:
    """A verified local checkout of the approved target repository."""

    def __init__(self, path: Path, target_repository: str, target_sha: str) -> None:
        self._path = Path(path)
        self._target_repository = target_repository
        self._target_sha = target_sha

    @property
    def path(self) -> Path:
        return self._path

    @property
    def target_repository(self) -> str:
        return self._target_repository

    @property
    def target_sha(self) -> str:
        return self._target_sha

    @classmethod
    def prepare(
        cls,
        *,
        target_repository: str,
        target_sha: str,
        work_root: Path,
        label: str = "target",
    ) -> TargetCheckout:
        """Materialize (or reuse a verified) checkout of the approved target.

        An absent checkout is CLONED fresh and then verified. An existing
        checkout is reused only if it passes every integrity check; any
        failure raises ``TargetCheckoutError`` -- never a silent fix.
        """
        path = Path(work_root) / label
        if path.exists():
            if not (path / ".git").exists():
                raise TargetCheckoutError(
                    f"target checkout path {path} exists but is not a git "
                    "repository; refusing to initialize over it"
                )
        else:
            result = subprocess.run(
                ["git", "clone", target_repository, str(path)],
                capture_output=True, text=True, timeout=900, check=False,
            )
            if result.returncode != 0:
                raise TargetCheckoutError(
                    f"cannot materialize target checkout: "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )
        checkout = cls(path, target_repository, target_sha)
        checkout.verify_integrity()
        return checkout

    # -- subprocess seam (tests stub these) --------------------------------
    def _run(self, args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self._path)] + args,
            capture_output=True, text=True, timeout=120, check=False,
        )

    def _origin_url(self) -> str:
        result = self._run(["remote", "get-url", "origin"])
        if result.returncode != 0:
            raise TargetCheckoutError(
                f"target checkout at {self._path} has no 'origin' remote"
            )
        return result.stdout.strip()

    def _head_sha(self) -> str:
        result = self._run(["rev-parse", "HEAD"])
        if result.returncode != 0:
            raise TargetCheckoutError(
                f"target checkout at {self._path} has no resolvable HEAD"
            )
        return result.stdout.strip()

    def _porcelain_status(self) -> str:
        result = self._run(["status", "--porcelain", "--untracked-files=all"])
        if result.returncode != 0:
            raise TargetCheckoutError(
                f"target checkout at {self._path}: cannot read git status"
            )
        return result.stdout.strip()

    def _submodule_status(self) -> str:
        result = self._run(["submodule", "status"])
        if result.returncode != 0:
            raise TargetCheckoutError(
                f"target checkout at {self._path}: cannot read submodule status"
            )
        return result.stdout.strip()

    def verify_integrity(self) -> None:
        """Re-verify every approved-target property. Raises on any drift.

        Called at materialization time and again immediately before each
        attempt, so a checkout mutated between attempts is refused.
        """
        if _norm_repo_url(self._origin_url()) != _norm_repo_url(
            self._target_repository
        ):
            raise TargetCheckoutError(
                f"target checkout origin {self._origin_url()!r} is not the "
                f"approved target repository {self._target_repository!r}"
            )
        head = self._head_sha()
        if head != self._target_sha:
            raise TargetCheckoutError(
                f"target checkout HEAD {head} is not the approved target "
                f"sha {self._target_sha}"
            )
        status = self._porcelain_status()
        if status:
            raise TargetCheckoutError(
                f"target checkout is not clean:\n{status}"
            )
        if (self._path / ".gitmodules").exists():
            raise TargetCheckoutError(
                "target checkout declares submodules (.gitmodules present); "
                "submodule drift could alter the analysis"
            )
        submodules = self._submodule_status()
        if submodules:
            raise TargetCheckoutError(
                f"target checkout has active submodules:\n{submodules}"
            )

    def seal_read_only(self) -> None:
        """Best-effort read-only sealing (POSIX).

        On Windows the mechanical confinement is the provider tool
        envelope (Read/Glob/Grep only); chmod is not reliable there.
        """
        if os.name == "nt":
            return
        for root, dirs, files in os.walk(self._path):
            if ".git" in dirs:
                dirs.remove(".git")
            for name in files:
                try:
                    os.chmod(Path(root) / name, 0o444)
                except OSError:
                    pass
            for name in dirs:
                try:
                    os.chmod(Path(root) / name, 0o555)
                except OSError:
                    pass
