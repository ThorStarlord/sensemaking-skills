"""Preparation proofs for the GitHub-durable EXP-0003 successor campaign.

This suite intentionally runs inside the existing Phase 2 campaign-validation
matrix so canonical digest computation and package validation happen in GitHub
Actions. Preparation must never create operative approval or attempt state in
the immutable preparation package. Results-branch lifecycle state is validated
separately by the GitHub-durable state contract.
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
from sensemaking_skills.exploratory_execution import extract_frontmatter

CAMPAIGN_ID = "EXP-0003-stage1-auteur-github-connector-pilot"
FRAMEWORK_SHA = "5704a2614222cd1705e0bf7e5174d1418c5d6240"
TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
EXECUTION_SURFACE = "github_connector"
NOT_BEFORE = "2026-08-18T12:00:00+00:00"
NOT_AFTER = "2026-08-25T12:00:00+00:00"
CURRENT_TIME = "2026-08-19T12:00:00+00:00"

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


def test_exp0003_digests_are_frozen_by_canonical_implementation() -> None:
    config = _parse("configuration-identity.yaml")
    configuration_id = compute_configuration_id(config)
    assert config["configuration_id"] == configuration_id, (
        f"EXP0003_CONFIGURATION_ID={configuration_id}"
    )

    policy = _parse("campaign-policy.yaml")
    policy_digest = compute_policy_digest(policy)
    assert policy["policy_digest"] == policy_digest, (
        f"EXP0003_POLICY_DIGEST={policy_digest}"
    )
    assert _read("campaign-policy.sha256").decode().strip() == policy_digest


def test_exp0003_policy_and_configuration_validate() -> None:
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


def test_exp0003_exact_pins_and_connector_native_coupling() -> None:
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
    }


def test_exp0003_approval_template_is_nonoperative() -> None:
    frontmatter = extract_frontmatter(_read("approval-template.md"))
    assert frontmatter is not None
    template = parse_two_lane_yaml(frontmatter)
    assert template["campaign_id"] == CAMPAIGN_ID
    assert template["policy_digest"] == "<PRESENTED_DIGEST>"
    assert template["approved_at"] == "<APPROVED_AT>"
    assert template["approval_text"] == "approve"

    policy = _parse("campaign-policy.yaml")
    result = validate_campaign_approval(frontmatter, policy, CONTEXT)
    assert not result.valid


def test_exp0003_preparation_package_contains_no_execution_state() -> None:
    assert {p.name for p in PACKAGE_DIR.iterdir()} == PACKAGE_FILES
    for name in ("approval.md", "approval.yaml", "ledger.jsonl", "ledger.lock"):
        assert not (PACKAGE_DIR / name).exists()
    assert not (PACKAGE_DIR / "attempts").exists()
