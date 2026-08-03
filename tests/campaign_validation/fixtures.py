"""Shared fixture builders for campaign-validation tests.

Every identity used here is an unmistakable, non-operative placeholder
(``example-*``, ``EXP-0001-example``, ``https://example.invalid/...``).
Nothing here is a real campaign, approval, or configuration; nothing under
``experiments/`` is created or touched.
"""

from __future__ import annotations

import copy

from sensemaking_skills.campaign_validation import (
    compute_configuration_id,
    compute_policy_digest,
)

from .helpers import to_bytes

FRAMEWORK_SHA = "a" * 40
TARGET_SHA = "b" * 40
TARGET_REPO = "https://example.invalid/example-owner/example-target.git"
MODEL = "example-model-identifier"
ARTIFACT_TYPE = "repository_sensemaking_brief"
AUTHORIZED_APPROVER = "example-authorized-owner"


def base_configuration_doc() -> dict:
    return {
        "configuration_schema_version": "1",
        "configuration_id": "0" * 64,
        "campaign_id": "EXP-0001-example",
        "framework_sha": FRAMEWORK_SHA,
        "target_repository": TARGET_REPO,
        "target_sha": TARGET_SHA,
        "model_identifier": MODEL,
        "prompt_or_skill_revision": "example-skill@v1",
        "validator_revision": "example-validator@v1",
        "artifact_type": ARTIFACT_TYPE,
        "execution_parameters": {
            "max_tokens_hint": 4096,
            "tool_allowlist": ["read_repository"],
        },
    }


def finalize_configuration(doc: dict) -> dict:
    doc = copy.deepcopy(doc)
    doc["configuration_id"] = compute_configuration_id(doc)
    return doc


def base_policy_doc(allowed_configuration_ids: list[str]) -> dict:
    return {
        "policy_schema_version": "1",
        "campaign_id": "EXP-0001-example",
        "policy_digest": "0" * 64,
        "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        "allowed_framework_shas": [FRAMEWORK_SHA],
        "allowed_targets": [{"repository": TARGET_REPO, "sha": TARGET_SHA}],
        "allowed_models": [MODEL],
        "allowed_artifact_types": [ARTIFACT_TYPE],
        "allowed_configuration_ids": sorted(allowed_configuration_ids),
        "max_attempt_slots": 5,
        "max_provider_invocations": 5,
        "max_attempts_per_configuration": 2,
        "concurrency_ceiling": 1,
        "token_ceiling": None,
        "cost_ceiling": None,
        "validity_window": {
            "not_before": "2026-01-01T00:00:00+00:00",
            "not_after": "2027-01-08T00:00:00+00:00",
        },
        "target_mutation_prohibited": True,
        "fallback_prohibited": True,
        "repair_prohibited": True,
        "automatic_merge_prohibited": True,
        "preservation_requirements": "Every reservation and attempt result is preserved.",
        "logging_requirements": "Every provider invocation is logged.",
        "prepared_by": "campaign-operator-agent",
        "prepared_at": "2026-01-01T00:00:00+00:00",
    }


def finalize_policy(doc: dict) -> dict:
    doc = copy.deepcopy(doc)
    doc["policy_digest"] = compute_policy_digest(doc)
    return doc


def base_approval_doc(policy: dict) -> dict:
    return {
        "approval_schema_version": "1",
        "campaign_id": policy["campaign_id"],
        "policy_digest": policy["policy_digest"],
        "claimed_approver_identity": AUTHORIZED_APPROVER,
        "approval_provenance": {
            "mechanism": "signed_commit",
            "reference": "c" * 40,
        },
        "approval_statement": "I approve this exploratory campaign policy.",
        "approved_at": "2026-01-02T00:00:00+00:00",
    }


def build_valid_bundle():
    """Return (policy_doc, approval_doc, configuration_doc) all mutually consistent."""
    config_doc = finalize_configuration(base_configuration_doc())
    policy_doc = finalize_policy(base_policy_doc([config_doc["configuration_id"]]))
    approval_doc = base_approval_doc(policy_doc)
    return policy_doc, approval_doc, config_doc


def build_valid_bundle_bytes():
    policy_doc, approval_doc, config_doc = build_valid_bundle()
    return to_bytes(policy_doc), to_bytes(approval_doc), to_bytes(config_doc)
