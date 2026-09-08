"""Filesystem layout for durable Sensemaking campaigns."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .errors import CampaignWorkspaceError


@dataclass(frozen=True)
class CampaignWorkspace:
    """Paths owned by one campaign.

    v0.3 deliberately requires a workspace outside the target repository when a
    target path is supplied.  Read-only repository sensemaking must not become a
    repository mutation merely because durable campaign state is enabled.
    """

    root: Path
    target_repo: Path | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", Path(self.root).expanduser().resolve())
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
    def artifacts_dir(self) -> Path:
        return self.root / "artifacts"

    @property
    def evidence_dir(self) -> Path:
        return self.root / "evidence"

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
