"""Campaign workspace and lifecycle errors."""

from __future__ import annotations

from typing import Iterable


class CampaignWorkspaceError(RuntimeError):
    """Base error for durable campaign workspace operations."""


class CampaignAlreadyExistsError(CampaignWorkspaceError):
    """Raised when initialization would overwrite an existing workspace."""


class CampaignNotInitializedError(CampaignWorkspaceError):
    """Raised when a workspace operation requires initialized state."""


class CampaignIdentityError(CampaignWorkspaceError):
    """Raised when campaign-scoped artifacts disagree on campaign identity."""


class CampaignTransactionError(CampaignWorkspaceError):
    """Raised when a durable lifecycle transaction cannot be prepared/applied."""


class CampaignIntegrityError(CampaignWorkspaceError):
    """Raised when persisted campaign artifacts cannot reconstruct coherently."""

    def __init__(self, message: str, *, diagnostic_codes: Iterable[str] = ()):
        self.diagnostic_codes = tuple(diagnostic_codes)
        suffix = (
            f" [{', '.join(self.diagnostic_codes)}]"
            if self.diagnostic_codes
            else ""
        )
        super().__init__(f"{message}{suffix}")
