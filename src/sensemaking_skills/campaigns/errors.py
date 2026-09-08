"""Campaign workspace errors."""


class CampaignWorkspaceError(RuntimeError):
    """Base error for durable campaign workspace operations."""


class CampaignAlreadyExistsError(CampaignWorkspaceError):
    """Raised when initialization would overwrite an existing workspace."""


class CampaignNotInitializedError(CampaignWorkspaceError):
    """Raised when a workspace operation requires initialized state."""


class CampaignIdentityError(CampaignWorkspaceError):
    """Raised when campaign-scoped artifacts disagree on campaign identity."""
