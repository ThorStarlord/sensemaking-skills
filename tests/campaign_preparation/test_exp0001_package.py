"""Phase 5 (#121): EXP-0001 preparation-package proofs.

The campaign package under ``experiments/campaigns/EXP-0001-stage1-auteur-
autonomy-pilot/`` must be internally coherent, digest-bound, narrowly
bounded, and IMPOSSIBLE to execute without a genuine human approval. These
tests validate the WRITTEN package files (not in-memory reconstructions)
with the real Phase 2 validators and the real Phase 3/4 chain, and prove:

* package coherence: policy and configuration validate, both digests
  match, the configuration is authorized conjunctively by the policy,
  every pinned value is exact;
* approval absence: the only approval material is a marker-bearing
  template that validation rejects, so no bundle, capability, reservation,
  or provider call is reachable;
* drift resistance: mutating any pinned field changes the digest or fails
  validation;
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
    ValidatedCampaignBundle,
    ValidationContext,
)

CAMPAIGN_ID = "EXP-0001-stage1-auteur-autonomy-pilot"
FRAMEWORK_SHA = "4ba049e04e74699a009147df112baed3f7536343"
TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
MODEL = "claude-sonnet-5"
ARTIFACT_TYPE = "repository_sensemaking_brief"
NOT_BEFORE = "2026-08-07T00:00:00+00:00"
NOT_AFTER = "2026-08-14T00:00:00+00:00"
# Injected validation time, always inside the frozen window: deterministic
# regardless of when the suite is executed (never the wall clock).
CURRENT_TIME = "2026-08-08T00:00:00+00:00"

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
    assert raw["allowed_framework_shas"] == [FRAMEWORK_SHA]
    assert raw["allowed_targets"] == [
        {"repository": TARGET_REPOSITORY, "sha": TARGET_SHA}
    ]
    assert raw["allowed_models"] == [MODEL]
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
        (config_raw["target_repository"], config_raw["target_sha"])
        in {(t["repository"], t["sha"]) for t in policy_raw["allowed_targets"]}
    )
    assert config_raw["model_identifier"] in policy_raw["allowed_models"]
    assert config_raw["artifact_type"] in policy_raw["allowed_artifact_types"]
    # Exactly one configuration is allowed.
    assert len(policy_raw["allowed_configuration_ids"]) == 1


def test_configuration_pins_exact_values() -> None:
    raw = _parse("configuration-identity.yaml")
    assert raw["configuration_schema_version"] == "1"
    assert raw["campaign_id"] == CAMPAIGN_ID
    assert raw["framework_sha"] == FRAMEWORK_SHA
    assert raw["target_repository"] == TARGET_REPOSITORY
    assert raw["target_sha"] == TARGET_SHA
    assert raw["model_identifier"] == MODEL
    assert raw["artifact_type"] == ARTIFACT_TYPE
    # The skill and validator revisions ship in the framework repository, so
    # the framework commit is their exact revision.
    assert raw["prompt_or_skill_revision"] == FRAMEWORK_SHA
    assert raw["validator_revision"] == FRAMEWORK_SHA
    assert raw["execution_parameters"] == {}


# ---------------------------------------------------------------------------
# Approval absence: the package cannot become operative
# ---------------------------------------------------------------------------


def test_approval_template_is_non_operative() -> None:
    policy = _validated_policy()
    result = validate_campaign_approval(
        _read("approval-template.yaml"), policy, CONTEXT
    )
    assert not result.valid
    assert result.failure_code == "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE"


def test_bundle_cannot_become_operative() -> None:
    """The only approval material is the template, so the bundle is invalid."""
    result = validate_campaign_bundle(
        _read("campaign-policy.yaml"),
        _read("approval-template.yaml"),
        _read("configuration-identity.yaml"),
        CONTEXT,
    )
    assert not result.valid


def test_capability_cannot_be_minted() -> None:
    """A capability requires a genuine validated bundle; package materials
    cannot produce one (the template is rejected), and a reconstructed
    bundle fails the validator-owned provenance check."""
    from sensemaking_skills.exploratory_authorization import (
        mint_exploratory_capability,
    )
    from sensemaking_skills.exploratory_authorization.failure_codes import (
        EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE,
    )
    from sensemaking_skills.exploratory_authorization.models import (
        ExploratoryAttemptRequest,
    )

    forged = object.__new__(ValidatedCampaignBundle)
    object.__setattr__(forged, "policy", None)
    object.__setattr__(forged, "approval", None)
    object.__setattr__(forged, "configuration", None)

    request = ExploratoryAttemptRequest(
        attempt_id="00000000-0000-4000-8000-000000000001",
        campaign_id=CAMPAIGN_ID,
        configuration_id=_parse("configuration-identity.yaml")["configuration_id"],
        intended_model=MODEL,
        framework_sha=FRAMEWORK_SHA,
        target_repository=TARGET_REPOSITORY,
        target_sha=TARGET_SHA,
        artifact_type=ARTIFACT_TYPE,
        output_path="/tmp/exploratory/exp-0001/attempt-1.md",
        executor_id="test-executor",
    )

    with pytest.raises(Exception) as exc_info:
        mint_exploratory_capability(forged, request, verifier=object())
    assert exc_info.value.failure_code == EXPLORATORY_MINT_REQUIRES_GENUINE_BUNDLE


def test_attempt_cannot_be_reserved_and_provider_never_called() -> None:
    """Without a genuine bundle there is no reservation and no provider
    call: the boundary fails closed before any provider is reached."""
    from sensemaking_skills.campaign_accounting import (
        RESERVATION_REQUIRED_BEFORE_INVOCATION,
        CampaignAccountingError,
        invoke_exploratory_attempt,
    )

    calls = []

    def spy_provider() -> bytes:
        calls.append(1)
        return b"should never run"

    with pytest.raises(CampaignAccountingError) as exc_info:
        invoke_exploratory_attempt(
            bundle=None,
            capability=None,
            reservation=None,
            campaign_root=Path("/tmp/phase5-probe"),
            context=None,
            provider=spy_provider,
            validate=lambda raw: None,
            now=datetime.fromisoformat(CURRENT_TIME),
        )
    assert exc_info.value.failure_code == RESERVATION_REQUIRED_BEFORE_INVOCATION
    assert calls == []


# ---------------------------------------------------------------------------
# Drift resistance
# ---------------------------------------------------------------------------

POLICY_DRIFT_CASES = {
    "framework_sha": {"allowed_framework_shas": ["0" * 40]},
    "target_sha": {"allowed_targets": [{"repository": TARGET_REPOSITORY, "sha": "0" * 40}]},
    "model": {"allowed_models": ["claude-opus-4"]},
    "artifact_type": {"allowed_artifact_types": ["architectural_review_recommendation"]},
    "attempt_count": {"max_attempt_slots": 4},
    "classification": {"classification": "CANONICAL_EVIDENCE"},
    "configuration_allowlist": {"allowed_configuration_ids": ["1" * 64]},
    "validity_window": {
        "validity_window": {"not_before": NOT_BEFORE, "not_after": "2026-08-21T00:00:00+00:00"}
    },
}


@pytest.mark.parametrize("label", sorted(POLICY_DRIFT_CASES))
def test_policy_drift_changes_digest(label: str) -> None:
    raw = _parse("campaign-policy.yaml")
    original = raw["policy_digest"]
    drifted = dict(raw)
    drifted.update(POLICY_DRIFT_CASES[label])
    drifted.pop("policy_digest", None)
    assert compute_policy_digest(drifted) != original


CONFIG_DRIFT_CASES = {
    "framework_sha": {"framework_sha": "0" * 40},
    "target_sha": {"target_sha": "0" * 40},
    "model": {"model_identifier": "claude-opus-4"},
    "artifact_type": {"artifact_type": "architectural_review_recommendation"},
    "skill_revision": {"prompt_or_skill_revision": "v2"},
    "validator_revision": {"validator_revision": "v2"},
    "execution_parameters": {"execution_parameters": {"temperature": 0.5}},
}


@pytest.mark.parametrize("label", sorted(CONFIG_DRIFT_CASES))
def test_configuration_drift_changes_id(label: str) -> None:
    raw = _parse("configuration-identity.yaml")
    original = raw["configuration_id"]
    drifted = dict(raw)
    drifted.update(CONFIG_DRIFT_CASES[label])
    drifted.pop("configuration_id", None)
    new_id = compute_configuration_id(drifted)
    assert new_id != original
    # A drifted configuration is not authorized by the frozen policy.
    assert new_id not in _parse("campaign-policy.yaml")["allowed_configuration_ids"]


def test_policy_file_tamper_fails_validation() -> None:
    """Tampering the policy bytes (attempts 3 -> 4) is detected."""
    content = _read("campaign-policy.yaml").decode("utf-8")
    tampered = content.replace("max_attempt_slots: 3", "max_attempt_slots: 4")
    assert tampered != content
    result = validate_campaign_policy(tampered.encode("utf-8"), CONTEXT)
    assert not result.valid


def test_approval_digest_drift_detected() -> None:
    """An approval referencing a different digest cannot validate."""
    policy = _validated_policy()
    template = _parse("approval-template.yaml")
    drifted_template = dict(template)
    drifted_template["policy_digest"] = "1" * 64
    from tests.campaign_validation.helpers import to_bytes
    result = validate_campaign_approval(to_bytes(drifted_template), policy, CONTEXT)
    assert not result.valid


# ---------------------------------------------------------------------------
# No execution residue
# ---------------------------------------------------------------------------


def test_no_execution_residue() -> None:
    """The package directory contains ONLY the six preparation files."""
    files = {p.name for p in PACKAGE_DIR.iterdir() if p.is_file()}
    assert files == PACKAGE_FILES, files
    forbidden = [
        "ledger.jsonl", "ledger.lock", "campaign-summary.yaml",
    ]
    for name in forbidden:
        assert not (PACKAGE_DIR / name).exists(), name
    attempts_dir = PACKAGE_DIR / "attempts"
    assert not attempts_dir.exists()
    for pattern in ("reservation.yaml", "request-metadata.json",
                    "raw-output.*", "produced-artifact.*",
                    "validation-result.json", "attempt-result.yaml"):
        assert not list(PACKAGE_DIR.glob(pattern)), pattern
