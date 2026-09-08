"""File-backed campaign workspace primitives.

This package persists campaign-semantic artifacts without taking semantic control
away from the active coding agent.  The agent decides what repository evidence
means; this package only preserves, validates, and reconstructs durable state.
"""

from .errors import (
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignNotInitializedError,
    CampaignWorkspaceError,
)
from .store import CampaignStore
from .workspace import CampaignWorkspace

__all__ = [
    "CampaignAlreadyExistsError",
    "CampaignIdentityError",
    "CampaignNotInitializedError",
    "CampaignStore",
    "CampaignWorkspace",
    "CampaignWorkspaceError",
]
