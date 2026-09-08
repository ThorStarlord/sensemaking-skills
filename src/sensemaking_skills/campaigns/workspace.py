"""Filesystem layout for durable Sensemaking campaigns."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .errors import CampaignWorkspaceError


@dataclass(frozen=True)
class CampaignWorkspace:
    """Paths owned by one campaign.

    v0.3 deliberately requires a workspace outside the target repository when a
    target path is supplied. Read-only repository sensemaking must not become a
    repository mutation merely because durable campaign state is enabled.

    ``requested_root`` preserves the lexical path the caller supplied (made
    absolute without resolving filesystem aliases). ``root`` is the physically
    resolved path used for storage and containment checks. Keeping both prevents
    a dangling symlink at the requested path from disappearing during
    normalization and then being mistaken for an unused workspace location.
    """

    root: Path
    target_repo: Path | None = None
    requested_root: Path = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        requested_root = Path(os.path.abspath(Path(self.root).expanduser()))
        object.__setattr__(self, "requested_root", requested_root)
        object.__setattr__(self, "root", requested_root.resolve())
        if self.target_repo is not None:
            object.__setattr__(
                self,
                "target_repo",
                Path(self.target_repo).expanduser().resolve(),
            )

    @property
    def state_path(self) -> Path:
        return self.root / "campaign-state.yaml"

    @property
    def policy_path(self) -> Path:
        return self.root / "campaign-policy.yaml"

    @property
    def handoff_path(self) -> Path:
        return self.root / "campaign-handoff.yaml"

    @property
    def trace_path(self) -> Path:
        return self.root / "trace.yaml"

    @property
    def transitions_dir(self) -> Path:
        return self.root / "transitions"

    @property
    def transactions_dir(self) -> Path:
        """Private durable journal for P2 lifecycle commits/recovery."""
        return self.root / ".transactions"

    @property
    def artifacts_dir(self) -> Path:
        return self.root / "artifacts"

    @property
    def evidence_dir(self) -> Path:
        return self.root / "evidence"

    @property
    def admissions_dir(self) -> Path:
        """Return the P4 receipt directory, migrating P1-P3 workspaces safely.

        P1-P3 campaign workspaces predate ``admissions/``. Once an initialized
        campaign is opened by P4+, creating this one empty structural directory
        is a deterministic compatibility migration; it grants no evidence
        status by itself. Existing symlink/non-directory entries fail closed.
        """
        path = self.root / "admissions"
        if os.path.lexists(path):
            if path.is_symlink() or not path.is_dir():
                raise CampaignWorkspaceError(
                    "campaign admissions path must be a real directory: "
                    f"{path}"
                )
            return path
        if self.state_path.is_file():
            path.mkdir()
        return path

    def assert_isolated_from_target(self) -> None:
        """Fail closed if campaign state would live inside the target repo."""
        if self.target_repo is None:
            return
        try:
            self.root.relative_to(self.target_repo)
        except ValueError:
            return
        raise CampaignWorkspaceError(
            "campaign workspace must be outside the target repository; "
            f"workspace={self.root} target={self.target_repo}"
        )
