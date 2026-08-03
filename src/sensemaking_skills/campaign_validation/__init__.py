"""Fail-closed validation for Two-Lane v1 campaign policy/approval/configuration
documents (ADR 0023, Issue #118 -- program Issue #116, Phase 2).

Public API:

* ``parse_two_lane_yaml(source_bytes)`` -- Two-Lane YAML Profile v1 parser.
* ``compute_policy_digest(policy)`` / ``compute_configuration_id(configuration)``
  -- RFC 8785 (JCS) digests.
* ``validate_campaign_policy(...)`` / ``validate_campaign_approval(...)`` /
  ``validate_configuration_identity(...)`` / ``validate_campaign_bundle(...)``
  -- fail-closed validators returning ``ValidationResult``.

This package validates DATA. It never returns, and does not import, a
provider-facing invocation capability. See ``validators.py`` module
docstring and the PR description for the full Phase 2 / Phase 3 boundary
statement.
"""

from .digests import compute_configuration_id, compute_policy_digest
from .failure_codes import CAMPAIGN_FAILURE_CODES
from .models import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidatedCampaignBundle,
    ValidationContext,
    ValidationDiagnostic,
    ValidationResult,
)
from .validators import (
    load_and_validate_approval_from_root,
    load_and_validate_configuration_from_root,
    load_and_validate_policy_from_root,
    validate_campaign_approval,
    validate_campaign_bundle,
    validate_campaign_policy,
    validate_configuration_identity,
)
from .yaml_profile import TwoLaneYamlError, parse_two_lane_yaml

__all__ = [
    "parse_two_lane_yaml",
    "TwoLaneYamlError",
    "compute_policy_digest",
    "compute_configuration_id",
    "validate_campaign_policy",
    "validate_campaign_approval",
    "validate_configuration_identity",
    "validate_campaign_bundle",
    "load_and_validate_policy_from_root",
    "load_and_validate_approval_from_root",
    "load_and_validate_configuration_from_root",
    "CampaignPolicy",
    "CampaignApproval",
    "ConfigurationIdentity",
    "ValidatedCampaignBundle",
    "ValidationContext",
    "ValidationDiagnostic",
    "ValidationResult",
    "CAMPAIGN_FAILURE_CODES",
]
