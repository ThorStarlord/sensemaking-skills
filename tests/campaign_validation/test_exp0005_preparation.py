"""Preparation proofs for the connector-native EXP-0005 successor campaign.

This suite runs inside the existing Phase 2 campaign-validation matrix so
canonical digest discovery and final package validation happen in GitHub
Actions. Preparation is lifecycle-scoped: the immutable campaign package must
contain no operative approval or attempt state. A synthetic receipt proves the
exact connector-native approval-reference form without creating real approval
state. A future results namespace is governed separately by the GitHub-durable
state validator and is not globally forbidden by this preparation proof.
"""

from pathlib import Path

from sensemaking_skills.campaign_validation import (
    compute_configuration_id,
    compute_policy_digest,
    parse_two_lane_yaml,
    validate_campaign_approval,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation.models import ValidationContext
from sensemaking_skills.campaign_validation.yaml_profile import dump_two_lane_yaml
from sensemaking_skills.exploratory_execution import extract_frontmatter

CAMPAIGN_ID = "EXP-0005-stage1-auteur-github-connector-pilot"
FRAMEWORK_SHA = "c9cb29d467eee82d1d9cc4d4fb89a184c26f27e7"
TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
EXECUTION_SURFACE = "github_connector"
PROBE_BACKEND = "github_connector_exact_sha_v1"
APPROVAL_REFERENCE_KIND = "agent_recorded_github_issue_comment"
APPROVAL_AUDIT_REPOSITORY = "ThorStarlord/sensemaking-skills"
APPROVAL_AUDIT_ISSUE_NUMBER = 201
NOT_BEFORE = "2026-08-18T19:00:00+00:00"
NOT_AFTER = "2026-08-25T19:00:00+00:00"
CURRENT_TIME = "2026-08-19T19:00:00+00:00"

ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "experiments" / "campaigns" / CAMPAIGN_ID
PACKAGE_FILES = {
    "campaign-policy.yaml",
    "campaign-policy.sha256",
    "configuration-identity.yaml",
    "approval-template.md",
    "scientific-questions.md",
    "README.md",
}
CONTEXT = ValidationContext(
    current_time=CURRENT_TIME,
    allowed_approver_identities=frozenset(),
)


def _read(name: str) -> bytes:
    return (PACKAGE_DIR / name).read_bytes()


def _parse(name: str) -> dict:
    return parse_two_lane_yaml(_read(name))


def test_exp0005_configuration_digest_is_frozen_by_canonical_implementation() -> None:
    config = _parse("configuration-identity.yaml")
    configuration_id = compute_configuration_id(config)
    assert config["configuration_id"] == configuration_id, (
        f"EXP0005_CONFIGURATION_ID={configuration_id}"
    )


def test_exp0005_policy_digest_is_frozen_by_canonical_implementation() -> None:
    policy = _parse("campaign-policy.yaml")
    policy_digest = compute_policy_digest(policy)
    assert policy["policy_digest"] == policy_digest, (
        f"EXP0005_POLICY_DIGEST={policy_digest}"
    )
    assert _read("campaign-policy.sha256").decode().strip() == policy_digest


def test_exp0005_policy_and_configuration_validate() -> None:
    policy_result = validate_campaign_policy(_read("campaign-policy.yaml"), CONTEXT)
    assert policy_result.valid, (
        f"{policy_result.failure_code}: {policy_result.detail}"
    )
    configuration_result = validate_configuration_identity(
        _read("configuration-identity.yaml"), policy_result.value
    )
    assert configuration_result.valid, (
        f"{configuration_result.failure_code}: {configuration_result.detail}"
    )


def test_exp0005_exact_pins_and_connector_native_contract_are_frozen() -> None:
    policy = _parse("campaign-policy.yaml")
    config = _parse("configuration-identity.yaml")

    assert policy["campaign_id"] == CAMPAIGN_ID == config["campaign_id"]
    assert policy["execution_mode"] == "coding_agent_native"
    assert policy["execution_surface"] == EXECUTION_SURFACE
    assert policy["external_provider_api_prohibited"] is True
    assert policy["allowed_models"] == []
    assert policy["allowed_framework_shas"] == [FRAMEWORK_SHA]
    assert policy["allowed_targets"] == [
        {"repository": TARGET_REPOSITORY, "sha": TARGET_SHA}
    ]
    assert policy["allowed_configuration_ids"] == [config["configuration_id"]]
    assert policy["max_attempt_slots"] == 3
    assert policy["max_provider_invocations"] == 3
    assert policy["max_attempts_per_configuration"] == 3
    assert policy["concurrency_ceiling"] == 1
    assert policy["validity_window"] == {
        "not_before": NOT_BEFORE,
        "not_after": NOT_AFTER,
    }
    assert policy["target_mutation_prohibited"] is True
    assert policy["fallback_prohibited"] is True
    assert policy["repair_prohibited"] is True
    assert policy["automatic_merge_prohibited"] is True

    assert config["framework_sha"] == FRAMEWORK_SHA
    assert config["target_repository"] == TARGET_REPOSITORY
    assert config["target_sha"] == TARGET_SHA
    assert config["model_identifier"] == EXECUTION_SURFACE
    assert config["prompt_or_skill_revision"] == FRAMEWORK_SHA
    assert config["validator_revision"] == FRAMEWORK_SHA
    assert config["artifact_type"] == "repository_sensemaking_brief"
    assert config["execution_parameters"] == {
        "durability_backend": "github_results_branch_v1",
        "validation_backend": "github_actions_exact_head",
        "invocation_boundary": "before_first_experiment_scoped_target_read",
        "target_access_mode": "github_connector_read_only",
        "probe_backend": PROBE_BACKEND,
        "approval_reference_kind": APPROVAL_REFERENCE_KIND,
        "approval_audit_repository": APPROVAL_AUDIT_REPOSITORY,
        "approval_audit_issue_number": APPROVAL_AUDIT_ISSUE_NUMBER,
    }


def test_exp0005_intended_connector_native_receipt_shape_validates_synthetically() -> None:
    policy_result = validate_campaign_policy(_read("campaign-policy.yaml"), CONTEXT)
    assert policy_result.valid
    policy = policy_result.value
    raw_policy = _parse("campaign-policy.yaml")
    reference = (
        "https://github.com/ThorStarlord/sensemaking-skills/issues/201"
        "#issuecomment-5330000001"
    )
    receipt = {
        "approval_schema_version": "1",
        "status": "approved",
        "campaign_id": CAMPAIGN_ID,
        "policy_digest": raw_policy["policy_digest"],
        "approval_source": "active_human_conversation",
        "approval_text": "approve",
        "approved_at": "2026-08-18T19:05:00+00:00",
        "maximum_attempts": 3,
        "concurrency": 1,
        "automatic_merge": "prohibited",
        "external_provider_api_prohibited": True,
        "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        "reference_kind": APPROVAL_REFERENCE_KIND,
        "reference": reference,
    }
    result = validate_campaign_approval(
        dump_two_lane_yaml(receipt).encode(), policy, CONTEXT
    )
    assert result.valid, (result.failure_code, result.detail)
    assert f"/{APPROVAL_AUDIT_REPOSITORY}/issues/{APPROVAL_AUDIT_ISSUE_NUMBER}" in reference


def test_exp0005_approval_template_is_nonoperative() -> None:
    frontmatter = extract_frontmatter(_read("approval-template.md"))
    assert frontmatter is not None
    template = parse_two_lane_yaml(frontmatter)
    assert template["campaign_id"] == CAMPAIGN_ID
    assert template["status"] == "<STATUS>"
    assert template["policy_digest"] == "<PRESENTED_DIGEST>"
    assert template["approved_at"] == "<APPROVED_AT>"
    assert template["approval_text"] == "approve"
    assert template["reference_kind"] == "<REFERENCE_KIND>"
    assert template["reference"] == "<AUDIT_REFERENCE>"

    policy_result = validate_campaign_policy(_read("campaign-policy.yaml"), CONTEXT)
    assert policy_result.valid
    result = validate_campaign_approval(frontmatter, policy_result.value, CONTEXT)
    assert not result.valid


def test_exp0005_preparation_package_contains_no_execution_state() -> None:
    assert {p.name for p in PACKAGE_DIR.iterdir()} == PACKAGE_FILES
    for name in ("approval.md", "approval.yaml", "ledger.jsonl", "ledger.lock"):
        assert not (PACKAGE_DIR / name).exists()
    assert not (PACKAGE_DIR / "attempts").exists()
