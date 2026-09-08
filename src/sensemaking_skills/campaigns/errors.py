"""Campaign workspace, lifecycle, and artifact-admission errors."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


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


class ArtifactValidationRejectedError(CampaignWorkspaceError):
    """Raised when the canonical validator runs successfully and rejects an artifact."""

    def __init__(self, validation_result: Mapping[str, Any]):
        self.validation_result = dict(validation_result)
        artifact_id = self.validation_result.get("artifact_id", "unknown")
        errors = self.validation_result.get("errors", [])
        super().__init__(
            f"canonical artifact validation rejected {artifact_id!r} "
            f"with {len(errors) if isinstance(errors, list) else 'unknown'} error(s)"
        )


class ArtifactValidatorError(CampaignWorkspaceError):
    """Raised when the canonical validation boundary cannot be executed or trusted."""
