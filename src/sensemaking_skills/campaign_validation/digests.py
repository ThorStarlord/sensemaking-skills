"""Deterministic digest computation (ADR 0023 sections 10a and 10c).

Digest functions accept only already-parsed, validated JSON-compatible
mapping values (never raw YAML text), select the exact hashed field set for
that digest, serialize via RFC 8785 (``jcs.canonicalize_bytes``), and hash
the resulting UTF-8 bytes with SHA-256. No trailing newline is included. The
input mapping is never mutated.
"""

from __future__ import annotations

import hashlib

from . import jcs

__all__ = ["compute_policy_digest", "compute_configuration_id"]

# Exact hashed field set for the policy digest: every required normative
# policy field (ADR 0023 section 9a) except `policy_digest` itself.
POLICY_DIGEST_FIELDS = (
    "policy_schema_version",
    "campaign_id",
    "classification",
    "allowed_framework_shas",
    "allowed_targets",
    "allowed_models",
    "allowed_artifact_types",
    "allowed_configuration_ids",
    "max_attempt_slots",
    "max_provider_invocations",
    "max_attempts_per_configuration",
    "concurrency_ceiling",
    "token_ceiling",
    "cost_ceiling",
    "validity_window",
    "target_mutation_prohibited",
    "fallback_prohibited",
    "repair_prohibited",
    "automatic_merge_prohibited",
    "preservation_requirements",
    "logging_requirements",
    "prepared_by",
    "prepared_at",
)

# Optional normative policy fields (Lane A beta amendment, ADR 0023
# section 21e): included in the digest WHEN PRESENT, so a declared
# execution mode / surface / external-API prohibition is digest-bound.
# Absence hashes nothing (the field simply is not part of the declared
# envelope), which keeps pre-amendment policies digest-stable.
POLICY_DIGEST_OPTIONAL_FIELDS = (
    "execution_mode",
    "execution_surface",
    "external_provider_api_prohibited",
)

# Exact hashed field set for the configuration ID (ADR 0023 section 10c),
# verbatim -- excludes `configuration_id` itself and `campaign_id`.
CONFIGURATION_ID_FIELDS = (
    "configuration_schema_version",
    "framework_sha",
    "target_repository",
    "target_sha",
    "model_identifier",
    "prompt_or_skill_revision",
    "validator_revision",
    "artifact_type",
    "execution_parameters",
)


def _project(
    document: dict, fields: tuple[str, ...], optional: tuple[str, ...] = ()
) -> dict:
    missing = [f for f in fields if f not in document]
    if missing:
        raise KeyError(f"missing required field(s) for digest: {missing}")
    projected = {field: document[field] for field in fields}
    for field in optional:
        if field in document:
            projected[field] = document[field]
    return projected


def compute_policy_digest(policy: dict) -> str:
    """Compute ``policy_digest`` for a parsed campaign policy document.

    ``policy`` must be the restricted JSON-compatible mapping produced by
    ``parse_two_lane_yaml`` (or an equivalent already-validated mapping) --
    never raw YAML text. Unknown fields are not silently included: only the
    exact fields in ``POLICY_DIGEST_FIELDS`` (plus any declared
    ``POLICY_DIGEST_OPTIONAL_FIELDS``) are hashed.
    """
    projected = _project(
        policy, POLICY_DIGEST_FIELDS, POLICY_DIGEST_OPTIONAL_FIELDS
    )
    payload = jcs.canonicalize_bytes(projected)
    return hashlib.sha256(payload).hexdigest()


def compute_configuration_id(configuration: dict) -> str:
    """Compute ``configuration_id`` for a parsed configuration-identity document.

    Excludes ``configuration_id`` itself and ``campaign_id`` (ADR 0023
    section 10c).
    """
    projected = _project(configuration, CONFIGURATION_ID_FIELDS)
    payload = jcs.canonicalize_bytes(projected)
    return hashlib.sha256(payload).hexdigest()
