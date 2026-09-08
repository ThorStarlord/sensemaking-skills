"""File-backed campaign workspace and deterministic lifecycle primitives.

The active coding agent retains semantic control: it decides what evidence
means and supplies lifecycle decisions. This package validates and persists the
durable structural consequences of those decisions.
"""

from .admission import (
    ArtifactAdmission,
    ArtifactAdmissionContractError,
)
from .artifacts import (
    ArtifactAdmissionResult,
    ArtifactAdmissionService,
)
from .errors import (
    ArtifactValidationRejectedError,
    ArtifactValidatorError,
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignIntegrityError,
    CampaignNotInitializedError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .service import (
    CampaignDiagnostic,
    CampaignService,
    CampaignSnapshot,
    CampaignValidationResult,
)
from .store import CampaignStore
from .workspace import CampaignWorkspace

__all__ = [
    "ArtifactAdmission",
    "ArtifactAdmissionContractError",
    "ArtifactAdmissionResult",
    "ArtifactAdmissionService",
    "ArtifactValidationRejectedError",
    "ArtifactValidatorError",
    "CampaignAlreadyExistsError",
    "CampaignDiagnostic",
    "CampaignIdentityError",
    "CampaignIntegrityError",
    "CampaignNotInitializedError",
    "CampaignService",
    "CampaignSnapshot",
    "CampaignStore",
    "CampaignTransactionError",
    "CampaignValidationResult",
    "CampaignWorkspace",
    "CampaignWorkspaceError",
]
