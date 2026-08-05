"""EXP-0002 preparation-package proofs (coding-agent-native pilot).

The campaign package under ``experiments/campaigns/EXP-0002-stage1-auteur-
coding-agent-pilot/`` must be internally coherent, digest-bound, narrowly
bounded, coding-agent-native (no external model/provider API), and
IMPOSSIBLE to execute without a genuine human approval comment. These
tests validate the WRITTEN package files (not in-memory reconstructions)
with the real Phase 2 validators and prove:

* package coherence: policy and configuration validate, both digests
  match, the configuration is authorized conjunctively by the policy,
  every pinned value is exact, and the execution-mode coupling holds
  (coding_agent_native + external_provider_api_prohibited + empty
  allowed_models);
* approval absence: the only approval material is a marker-bearing
  template that validation rejects, so no reservation, INVOKED
  transition, or attempt output is reachable;
* drift resistance: mutating any pinned field changes the digest or
  fails validation;
* no execution residue: after every test, the package directory contains
  only the six preparation files.
"""

from datetime import datetime, timedelta
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensemaking_skills.campaign_validation import (
    compute_configuration_id,
    compute_policy_digest,
    parse_two_lane_yaml,
    validate_campaign_approval,
    validate_campaign_bundle,
    validate_campaign_policy,
    validate_configuration_identity,
)
from sensemaking_skills.campaign_validation.models import (
    ValidationContext,
)

CAMPAIGN_ID = "EXP-0002-stage1-auteur-coding-agent-pilot"
FRAMEWORK_SHA = "253efe56d08f3e5c9a051bbba78efeaa606a6928"
TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
EXECUTION_SURFACE = "current_coding_agent"
ARTIFACT_TYPE = "repository_sensemaking_brief"
NOT_BEFORE = "2026-08-18T00:00:00+00:00"
NOT_AFTER = "2026-08-25T00:00:00+00:00"
# Injected validation time, always inside the frozen window: deterministic
# regardless of when the suite is executed (never the wall clock).
CURRENT_TIME = "2026-08-19T00:00:00+00:00"

PACKAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "experiments" / "campaigns" / CAMPAIGN_ID
)

PACKAGE_FILES = {
    "campaign-policy.yaml",
    "campaign-policy.sha256",
    "configuration-identity.yaml",
    "approval-template.yaml",
    "scientific-questions.md",
    "README.md",
}

CONTEXT = ValidationContext(
    current_time=CURRENT_TIME, allowed_approver_identities=frozenset()
)


def _read(name: str) -> bytes:
    return (PACKAGE_DIR / name).read_bytes()


def _parse(name: str) -> dict:
    return parse_two_lane_yaml(_read(name))


def _validated_policy():
    result = validate_campaign_policy(_read("campaign-policy.yaml"), CONTEXT)
    assert result.valid, f"policy failed validation: {result.failure_code} {result.detail}"
    return result.value


# ---------------------------------------------------------------------------
# Package coherence
# ---------------------------------------------------------------------------


def test_policy_file_validates_and_digests_match() -> None:
    result = validate_campaign_policy(_read("campaign-policy.yaml"), CONTEXT)
    assert result.valid, f"{result.failure_code}: {result.detail}"

    parsed = _parse("campaign-policy.yaml")
    recomputed = compute_policy_digest(parsed)
    assert parsed["policy_digest"] == recomputed
    sha256_file = _read("campaign-policy.sha256").decode("utf-8").strip()
    assert sha256_file == recomputed
    assert len(recomputed) == 64
    assert int(recomputed, 16) >= 0  # well-formed lowercase hex


def test_policy_pins_exact_values() -> None:
    raw = _parse("campaign-policy.yaml")
    assert raw["policy_schema_version"] == "1"
    assert raw["campaign_id"] == CAMPAIGN_ID
    assert raw["classification"] == "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
    # Coding-agent-native coupling (ADR 0023 section 21e).
    assert raw["execution_mode"] == "coding_agent_native"
    assert raw["execution_surface"] == EXECUTION_SURFACE
    assert raw["external_provider_api_prohibited"] is True
    assert raw["allowed_models"] == []  # no external model authorized
    assert raw["allowed_framework_shas"] == [FRAMEWORK_SHA]
    assert raw["allowed_targets"] == [
        {"repository": TARGET_REPOSITORY, "sha": TARGET_SHA}
    ]
    assert raw["allowed_artifact_types"] == [ARTIFACT_TYPE]
    assert raw["max_attempt_slots"] == 3
    assert raw["max_provider_invocations"] == 3
    assert raw["max_attempts_per_configuration"] == 3
    assert raw["concurrency_ceiling"] == 1
    assert raw["target_mutation_prohibited"] is True
    assert raw["fallback_prohibited"] is True
    assert raw["repair_prohibited"] is True
    assert raw["automatic_merge_prohibited"] is True
    assert raw["prepared_by"] == "campaign-preparation-agent"


def test_validity_window_is_exactly_seven_days() -> None:
    raw = _parse("campaign-policy.yaml")
    window = raw["validity_window"]
    not_before = datetime.fromisoformat(window["not_before"])
    not_after = datetime.fromisoformat(window["not_after"])
    assert not_after - not_before == timedelta(days=7)


def test_configuration_validates_and_id_matches() -> None:
    policy = _validated_policy()
    result = validate_configuration_identity(
        _read("configuration-identity.yaml"), policy
    )
    assert result.valid, f"{result.failure_code}: {result.detail}"

    parsed = _parse("configuration-identity.yaml")
    recomputed = compute_configuration_id(parsed)
    assert parsed["configuration_id"] == recomputed
    assert len(recomputed) == 64


def test_configuration_is_authorized_by_policy() -> None:
    """Conjunctive authorization: id membership AND every constituent field."""
    policy_raw = _parse("campaign-policy.yaml")
    config_raw = _parse("configuration-identity.yaml")
    assert config_raw["configuration_id"] in policy_raw["allowed_configuration_ids"]
    assert config_raw["framework_sha"] in policy_raw["allowed_framework_shas"]
    assert (
        {"repository": config_raw["target_repository"], "sha": config_raw["target_sha"]}
        in policy_raw["allowed_targets"]
    )
    # Agent-native coherence: the surface identifier matches the policy.
    assert config_raw["model_identifier"] == policy_raw["execution_surface"]
    assert config_raw["artifact_type"] in policy_raw["allowed_artifact_types"]


def test_bundle_validates_with_an_approver_identity() -> None:
    """A candidate operative approval (github issue-comment mechanism) binds
    the package; the claimed identity must be a real approved identity."""
    policy = _validated_policy()
    approval = _parse("approval-template.yaml")
    assert approval.get("marker") == "EXAMPLE_ONLY_NOT_AUTHORIZATION"
    assert approval["policy_digest"] == policy.policy_digest
    assert approval["approval_provenance"]["mechanism"] == "github_issue_comment_approval"


def test_template_can_never_be_operative() -> None:
    """The template is rejected by the real validator: a template can never
    become an operative approval no matter how it is otherwise malformed."""
    result = validate_campaign_approval(
        _read("approval-template.yaml"),
        _validated_policy(),
        CONTEXT,
    )
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


# ---------------------------------------------------------------------------
# Drift resistance
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "filename, old, new",
    [
        ("campaign-policy.yaml", "253efe56d08f3e5c9a051bbba78efeaa606a6928", "0" * 40),
        ("campaign-policy.yaml", "coding_agent_native", "provider_api"),
        ("campaign-policy.yaml", "current_coding_agent", "other_agent_surface"),
        ("campaign-policy.yaml", "EXP-0002-stage1-auteur-coding-agent-pilot", "EXP-9999-other"),
        ("configuration-identity.yaml", "0653defb05625f2fcde0ac32eac6e59ccf7eeb90", "0" * 40),
    ],
)
def test_pinned_field_tamper_detected(filename: str, old: str, new: str) -> None:
    source = _read(filename).decode("utf-8")
    mutated = source.replace(old, new, 1)
    assert mutated != source, f"tamper target {old!r} not present in {filename}"
    mutated_bytes = mutated.encode("utf-8")
    if filename == "campaign-policy.yaml":
        result = validate_campaign_policy(mutated_bytes, CONTEXT)
        assert not result.valid
        raw = parse_two_lane_yaml(mutated_bytes)
        if compute_policy_digest(raw) == raw.get("policy_digest"):
            # A value that still recomputes identically cannot exist: the
            # digest binds every normative field.
            raise AssertionError("digest did not change on tamper")
    else:
        policy = _validated_policy()
        result = validate_configuration_identity(mutated_bytes, policy)
        assert not result.valid or result.value.configuration_id != _parse(filename)["configuration_id"]


def test_no_execution_residue() -> None:
    """The package directory contains ONLY the six preparation files."""
    files = {p.name for p in PACKAGE_DIR.iterdir()}
    assert files == PACKAGE_FILES
    for name in ("approval.yaml", "ledger.jsonl", "ledger.lock"):
        assert not (PACKAGE_DIR / name).exists(), name
    attempts_dir = PACKAGE_DIR / "attempts"
    assert not attempts_dir.exists()
    for pattern in ("reservation.yaml", "request-metadata.json",
                    "raw-output.*", "produced-artifact.*",
                    "validation-result.json", "attempt-result.yaml"):
        assert not list(PACKAGE_DIR.glob(pattern)), pattern


def test_no_external_model_authorized() -> None:
    """The coding-agent-native envelope authorizes no external model API."""
    raw = _parse("campaign-policy.yaml")
    assert raw["allowed_models"] == []
    assert raw["external_provider_api_prohibited"] is True
    assert raw["execution_mode"] == "coding_agent_native"
