"""Phase 3 (#119): digest-vector tests for exploratory authorization snapshots.

The issuer binds two snapshot digests at mint time (task brief section 8):

- approval snapshot digest: SHA-256 over the RFC 8785 (JCS) canonical
  serialization of the complete parsed, validated campaign-approval
  document (``CampaignApproval.raw``), as produced by the Phase 2
  validator-owned YAML profile parser.
- configuration snapshot digest: SHA-256 over the JCS canonical
  serialization of the complete parsed, validated configuration-identity
  document (``ConfigurationIdentity.raw``) WITH ``configuration_id``
  included. Unlike ``compute_configuration_id`` (which excludes
  ``campaign_id`` and ``configuration_id`` by ADR 0023 section 10), the
  snapshot must bind campaign_id and configuration_id so a capability
  cannot be split across campaigns or across revisions of one document.

Digests are recomputed internally at mint; callers never supply trusted
digest values. Both digests are lowercase 64-character SHA-256 hex.

The pinned vectors below were independently computed with the maintained
rfc8785 adapter (``sensemaking_skills.campaign_validation.jcs``) over the
reference documents from ``campaign-approval.schema.md`` /
``configuration-identity.schema.md`` example sections, then hashed with
``hashlib.sha256``.
"""

from __future__ import annotations

import copy
import hashlib

import pytest

from sensemaking_skills.campaign_validation.jcs import canonicalize
from sensemaking_skills.exploratory_authorization.digests import (
    compute_approval_snapshot_digest,
    compute_configuration_snapshot_digest,
)

REFERENCE_APPROVAL_RAW = {
    "approval_schema_version": "1",
    "campaign_id": "EXP-0000-EXAMPLE",
    "policy_digest": "0000000000000000000000000000000000000000000000000000000000000000",
    "claimed_approver_identity": "example-owner-handle",
    "approval_provenance": {
        "mechanism": "signed_commit",
        "reference": "000000000000000000000000000000000000c0de",
    },
    "approval_statement": (
        "EXAMPLE ONLY. This illustrates the shape of a filled approval; it is "
        "not a real consent statement and authorizes nothing."
    ),
    "approved_at": "2026-01-01T00:00:00+00:00",
    "marker": "EXAMPLE_ONLY_NOT_AUTHORIZATION",
}

REFERENCE_CONFIGURATION_ID = (
    "1111111111111111111111111111111111111111111111111111111111111111"
)

REFERENCE_CONFIGURATION_RAW = {
    "configuration_schema_version": "1",
    "configuration_id": REFERENCE_CONFIGURATION_ID,
    "campaign_id": "EXP-0000-EXAMPLE",
    "framework_sha": "000000000000000000000000000000000000dead",
    "target_repository": "https://example.invalid/example-owner/example-target.git",
    "target_sha": "000000000000000000000000000000000000beef",
    "model_identifier": "example-model-identifier",
    "prompt_or_skill_revision": "v1",
    "validator_revision": "v1",
    "artifact_type": "repository_sensemaking_brief",
    "execution_parameters": {},
}

# Independently computed reference vectors (see module docstring).
PINNED_APPROVAL_SNAPSHOT_DIGEST = (
    "7e07e1aa8dae44333f6c40451d633b4681ad809f90ec26d4b93809c55c5b5119"
)
PINNED_CONFIGURATION_SNAPSHOT_DIGEST = (
    "5fd194737fcfa496941e2e7d6d43cb0a18df67f682d924a21e10945e44d2eef9"
)


def _independent_sha256(value: object) -> str:
    return hashlib.sha256(canonicalize(value).encode("ascii")).hexdigest()


def _configuration_snapshot(raw: dict, configuration_id: str) -> dict:
    snapshot = dict(raw)
    snapshot["configuration_id"] = configuration_id
    return snapshot


# ---------------------------------------------------------------------------
# Pinned vectors
# ---------------------------------------------------------------------------


def test_approval_snapshot_digest_matches_pinned_reference_vector():
    assert compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW) == (
        PINNED_APPROVAL_SNAPSHOT_DIGEST
    )


def test_configuration_snapshot_digest_matches_pinned_reference_vector():
    assert compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    ) == PINNED_CONFIGURATION_SNAPSHOT_DIGEST


# ---------------------------------------------------------------------------
# Algorithm shape: RFC 8785 JCS + SHA-256, lowercase 64-hex
# ---------------------------------------------------------------------------


def test_approval_snapshot_digest_is_sha256_over_jcs_canonical_form():
    expected = _independent_sha256(REFERENCE_APPROVAL_RAW)
    assert compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW) == expected


def test_configuration_snapshot_digest_is_sha256_over_jcs_canonical_form():
    snapshot = _configuration_snapshot(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    expected = _independent_sha256(snapshot)
    assert compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    ) == expected


def test_approval_snapshot_digest_is_lowercase_64_hex():
    digest = compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW)
    assert len(digest) == 64
    assert digest == digest.lower()
    int(digest, 16)


def test_configuration_snapshot_digest_is_lowercase_64_hex():
    digest = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert len(digest) == 64
    assert digest == digest.lower()
    int(digest, 16)


def test_approval_snapshot_digest_is_deterministic():
    first = compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW)
    second = compute_approval_snapshot_digest(dict(REFERENCE_APPROVAL_RAW))
    assert first == second


def test_configuration_snapshot_digest_is_deterministic():
    first = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    second = compute_configuration_snapshot_digest(
        dict(REFERENCE_CONFIGURATION_RAW), REFERENCE_CONFIGURATION_ID
    )
    assert first == second


# ---------------------------------------------------------------------------
# Field sensitivity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate",
    [
        lambda raw: raw.update({"claimed_approver_identity": "another-handle"}),
        lambda raw: raw.update({"approved_at": "2026-02-01T00:00:00+00:00"}),
        lambda raw: raw["approval_provenance"].update(
            {"reference": "000000000000000000000000000000000000f00d"}
        ),
        lambda raw: raw["approval_provenance"].update({"mechanism": "github_review_approval"}),
        lambda raw: raw.update({"approval_statement": "I approve this campaign."}),
        lambda raw: raw.update({"policy_digest": "9999999999999999999999999999999999999999999999999999999999999999"}),
        lambda raw: raw.pop("marker"),
    ],
    ids=[
        "approver",
        "approved_at",
        "provenance_reference",
        "provenance_mechanism",
        "statement",
        "policy_digest",
        "marker",
    ],
)
def test_approval_snapshot_digest_binds_every_document_field(mutate):
    mutated = copy.deepcopy(REFERENCE_APPROVAL_RAW)
    mutate(mutated)
    assert compute_approval_snapshot_digest(mutated) != (
        compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW)
    )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda raw: raw.update({"framework_sha": "0000000000000000000000000000000000000bad"}),
        lambda raw: raw.update({"target_sha": "000000000000000000000000000000000000f00d"}),
        lambda raw: raw.update({"model_identifier": "other-model"}),
        lambda raw: raw.update({"artifact_type": "other_artifact"}),
        lambda raw: raw.update({"execution_parameters": {"temperature": 0.2}}),
        lambda raw: raw.update({"prompt_or_skill_revision": "v2"}),
        lambda raw: raw.update({"validator_revision": "v2"}),
    ],
    ids=[
        "framework_sha",
        "target_sha",
        "model_identifier",
        "artifact_type",
        "execution_parameters",
        "prompt_or_skill_revision",
        "validator_revision",
    ],
)
def test_configuration_snapshot_digest_binds_every_normative_field(mutate):
    mutated = copy.deepcopy(REFERENCE_CONFIGURATION_RAW)
    mutate(mutated)
    baseline = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert compute_configuration_snapshot_digest(
        mutated, REFERENCE_CONFIGURATION_ID
    ) != baseline


def test_configuration_snapshot_digest_binds_campaign_id():
    mutated = dict(REFERENCE_CONFIGURATION_RAW)
    mutated["campaign_id"] = "EXP-0001-OTHER"
    baseline = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert compute_configuration_snapshot_digest(
        mutated, REFERENCE_CONFIGURATION_ID
    ) != baseline


def test_configuration_snapshot_digest_binds_configuration_id():
    other_id = "2222222222222222222222222222222222222222222222222222222222222222"
    baseline = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, other_id
    ) != baseline


def test_configuration_snapshot_digest_differs_from_configuration_id():
    snapshot = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert snapshot != REFERENCE_CONFIGURATION_ID


def test_approval_snapshot_digest_differs_from_policy_digest():
    approval = compute_approval_snapshot_digest(REFERENCE_APPROVAL_RAW)
    assert approval != REFERENCE_APPROVAL_RAW["policy_digest"]


def test_configuration_snapshot_digest_is_not_the_bare_jcs_of_raw_without_id():
    # The snapshot must NOT be the digest of the document without an explicit
    # configuration_id: the ID is a computed field and could drift silently.
    bare = _independent_sha256({
        key: value for key, value in REFERENCE_CONFIGURATION_RAW.items()
        if key != "configuration_id"
    })
    snapshot = compute_configuration_snapshot_digest(
        REFERENCE_CONFIGURATION_RAW, REFERENCE_CONFIGURATION_ID
    )
    assert snapshot != bare
