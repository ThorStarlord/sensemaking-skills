"""Stable, frozen failure codes for campaign policy/approval/configuration validation.

Every code carries the ``CAMPAIGN_`` prefix. Independent failure categories
never collapse into a shared generic code (no bare ``INVALID`` or
``UNAUTHORIZED``). This mapping is the single source of truth; tests freeze
it (``tests/campaign_validation/test_failure_codes.py``).

First-failure precedence (checked in this order by ``validate_campaign_bundle``):

1. root / path safety (escape, symlink, filesystem errors)
2. source-profile / YAML parsing
3. schema / version validation
4. digest / identity integrity
5. approval binding / identity declaration
6. policy validity window
7. configuration / conjunctive allowlists
"""

from __future__ import annotations

from typing import Mapping

CAMPAIGN_FAILURE_CODES: Mapping[str, str] = {
    # --- filesystem / path trust boundary ---
    "CAMPAIGN_PATH_ESCAPE": "resolved path lexically or physically escapes the artifact root",
    "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION": "a symlink or reparse point redirects outside the artifact root",
    "CAMPAIGN_FILESYSTEM_ERROR": "an unexpected filesystem error occurred while reading an artifact",

    # --- policy loading / identity ---
    "CAMPAIGN_POLICY_MISSING": "no policy document found at the expected location",
    "CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID": "policy source violates the Two-Lane YAML Profile v1",
    "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED": "policy_schema_version is not a supported version",
    "CAMPAIGN_POLICY_SCHEMA_INVALID": "policy document does not satisfy the campaign-policy JSON Schema",
    "CAMPAIGN_POLICY_IDENTITY_AMBIGUOUS": "more than one policy record matches this campaign identity",
    "CAMPAIGN_POLICY_DIGEST_MALFORMED": "policy_digest is not a well-formed sha256 hex string",
    "CAMPAIGN_POLICY_DIGEST_MISMATCH": "recomputed policy_digest does not match the document's declared value",

    # --- approval loading / identity ---
    "CAMPAIGN_APPROVAL_MISSING": "no approval document found at the expected location",
    "CAMPAIGN_APPROVAL_SOURCE_PROFILE_INVALID": "approval source violates the Two-Lane YAML Profile v1",
    "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED": "approval_schema_version is not a supported version",
    "CAMPAIGN_APPROVAL_SCHEMA_INVALID": "approval document does not satisfy the campaign-approval JSON Schema",
    "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE": "approval carries the EXAMPLE_ONLY_NOT_AUTHORIZATION marker and can never be operative",
    "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT": "approval contains an unfilled human-placeholder token",
    "CAMPAIGN_APPROVAL_POLICY_MISMATCH": "approval's campaign_id or policy_digest does not match the policy being approved",
    "CAMPAIGN_APPROVER_UNAUTHORIZED": "claimed_approver_identity is not in the caller-supplied allowed approver set",
    "CAMPAIGN_APPROVAL_PROVENANCE_INVALID": "approval_provenance mechanism/reference is missing or structurally invalid",
    "CAMPAIGN_APPROVAL_AMBIGUOUS": "more than one operative approval matches this policy",

    # --- policy validity window / limits ---
    "CAMPAIGN_POLICY_NOT_YET_VALID": "current time is before validity_window.not_before",
    "CAMPAIGN_POLICY_EXPIRED": "current time is at or after validity_window.not_after",
    "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID": "validity_window is malformed or not_before is not before not_after",
    "CAMPAIGN_POLICY_LIMITS_INVALID": "one or more policy limit fields violate their documented bounds",

    # --- configuration identity / conjunctive checks ---
    "CAMPAIGN_CONFIGURATION_MISSING": "no configuration-identity document found at the expected location",
    "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID": "configuration document does not satisfy the configuration-identity JSON Schema",
    "CAMPAIGN_CONFIGURATION_ID_MALFORMED": "configuration_id is not a well-formed sha256 hex string",
    "CAMPAIGN_CONFIGURATION_ID_MISMATCH": "recomputed configuration_id does not match the document's declared value",
    "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED": "configuration_id is not a member of allowed_configuration_ids",
    "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED": "framework_sha is not a member of allowed_framework_shas",
    "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED": "target_repository/target_sha pair is not a member of allowed_targets",
    "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED": "model_identifier is not a member of allowed_models",
    "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED": "artifact_type is not a member of allowed_artifact_types",

    # --- catch-all ---
    "CAMPAIGN_INTERNAL_VALIDATION_ERROR": "an unexpected internal error occurred during validation",
}


def is_known_code(code: str) -> bool:
    return code in CAMPAIGN_FAILURE_CODES
