"""Tests for the Phase 3 + Phase 4 provider boundary (Issue #120).

``invoke_exploratory_attempt`` is the single seam where a capability-backed
exploratory invocation crosses into the provider. These tests prove with a
spy provider:

* every denial path (no reservation, forged reservation, wrong campaign /
  configuration / attempt, expired, not live, spent capability) yields
  ZERO provider calls;
* on the success path the durable INVOKED transition is already visible in
  the ledger when the provider runs;
* a provider failure records PROVIDER_FAILED and burns the capability;
* an interruption (KeyboardInterrupt) leaves INVOKED-incomplete durable
  state, burns the capability, and is re-raised;
* a validation failure preserves both the raw output and the produced
  artifact;
* a retry is always a NEW attempt with a NEW reservation and a NEW
  capability -- never a reuse of the spent attempt.
"""

from datetime import timedelta
import sys
from pathlib import Path
import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import (
    _ANCHOR_NOW,
    TrustedReferenceProvenanceVerifier,
    build_request,
    build_valid_bundle,
    make_context,
    new_attempt_id,
)

from sensemaking_skills.campaign_accounting import (
    ProviderResponse,
    RESERVATION_ATTEMPT_MISMATCH,
    RESERVATION_CAMPAIGN_MISMATCH,
    RESERVATION_CONFIGURATION_MISMATCH,
    RESERVATION_EXPIRED,
    RESERVATION_NOT_GENUINE,
    RESERVATION_NOT_LIVE,
    RESERVATION_REQUIRED_BEFORE_INVOCATION,
    AttemptReservation,
    AttemptState,
    CampaignAccountingError,
    CampaignLedger,
    DurableReservationManager,
    AttemptOutcomeRecorder,
    ValidationOutcome,
    invoke_exploratory_attempt,
)
from sensemaking_skills.exploratory_authorization import (
    mint_exploratory_capability,
)

PASSING_VALIDATE = lambda raw: ValidationOutcome(  # noqa: E731
    passed=True,
    details={"validator": "test-ok"},
    artifact_content="# candidate artifact",
)


def _mint(bundle, attempt_id, now=_ANCHOR_NOW):
    request = build_request(
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
    )
    return mint_exploratory_capability(
        bundle,
        request,
        verifier=TrustedReferenceProvenanceVerifier(),
        now=now.isoformat(),
    )


def _reserve(tmp_path, bundle, attempt_id=None, now=_ANCHOR_NOW):
    attempt_id = attempt_id or new_attempt_id()
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=now,
    )
    return manager, reservation


class SpyProvider:
    """Provider test double: counts calls and can observe the ledger."""

    def __init__(self, tmp_path, bundle, attempt_id, raw=b"raw provider response"):
        self.tmp_path = Path(tmp_path)
        self.bundle = bundle
        self.attempt_id = attempt_id
        self.raw = raw
        self.calls = 0
        self.latest_states_at_call = []
        self.exception = None

    def __call__(self, *, permit, context, prompt) -> ProviderResponse:
        self.calls += 1
        ledger = CampaignLedger(
            self.tmp_path / self.bundle.policy.campaign_id,
            self.bundle.policy.campaign_id,
        )
        states = [
            e.event_type
            for e in ledger.read_events()
            if e.attempt_id == self.attempt_id
        ]
        self.latest_states_at_call.append(states[-1] if states else None)
        if self.exception is not None:
            raise self.exception
        return ProviderResponse(raw_output=self.raw)


def _ledger_states(tmp_path, bundle, attempt_id):
    ledger = CampaignLedger(
        Path(tmp_path) / bundle.policy.campaign_id, bundle.policy.campaign_id
    )
    return [
        e.event_type
        for e in ledger.read_events()
        if e.attempt_id == attempt_id
    ]


def _invoke(tmp_path, bundle, capability, reservation, provider, validate=PASSING_VALIDATE):
    return invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=Path(tmp_path),
        context=make_context(capability=capability),
        provider=provider,
        validate=validate,
        prompt="test prompt",
        now=_ANCHOR_NOW,
    )


# ---------------------------------------------------------------------------
# Denial paths: zero provider calls
# ---------------------------------------------------------------------------


def test_no_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, None, provider)
    assert exc_info.value.failure_code == RESERVATION_REQUIRED_BEFORE_INVOCATION
    assert provider.calls == 0


def test_forged_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    # A reservation-shaped object reconstructed via object.__new__: no seal.
    _, genuine = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    forged = object.__new__(AttemptReservation)
    for key, value in genuine.to_dict().items():
        object.__setattr__(forged, key, value)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, forged, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_GENUINE
    assert provider.calls == 0


def test_dict_shaped_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    _, genuine = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    mapping = dict(genuine.to_dict())

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, mapping, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_GENUINE
    assert provider.calls == 0


def test_wrong_campaign_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    other_bundle = build_valid_bundle(campaign_id="EXP-9002-beta")
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    # The reservation belongs to a DIFFERENT campaign than the bundle and
    # capability being invoked.
    _, foreign_reservation = _reserve(tmp_path, other_bundle, attempt_id=attempt_id)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, foreign_reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_CAMPAIGN_MISMATCH
    assert provider.calls == 0


def test_wrong_configuration_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    # Same campaign, different validated configuration (different artifact type).
    other_bundle = build_valid_bundle(
        configuration_kwargs={"artifact_type": "repository_sensemaking_brief"}
    )
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    _, foreign_reservation = _reserve(tmp_path, other_bundle, attempt_id=attempt_id)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, foreign_reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_CONFIGURATION_MISMATCH
    assert provider.calls == 0


def test_capability_attempt_mismatch_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    capability_attempt = new_attempt_id()
    reservation_attempt = new_attempt_id()
    capability = _mint(bundle, capability_attempt)
    provider = SpyProvider(tmp_path, bundle, reservation_attempt)

    _, reservation = _reserve(tmp_path, bundle, attempt_id=reservation_attempt)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_ATTEMPT_MISMATCH
    assert provider.calls == 0


def test_expired_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    expired_now = _ANCHOR_NOW + timedelta(days=400)

    with pytest.raises(CampaignAccountingError) as exc_info:
        invoke_exploratory_attempt(
            bundle=bundle,
            capability=capability,
            reservation=reservation,
            campaign_root=Path(tmp_path),
            context=make_context(capability=capability),
            provider=provider,
            validate=PASSING_VALIDATE,
            prompt="test prompt",
            now=expired_now,
        )
    assert exc_info.value.failure_code == RESERVATION_EXPIRED
    assert provider.calls == 0


def test_terminal_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    manager, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    recorder = AttemptOutcomeRecorder(
        tmp_path, bundle.policy.campaign_id, attempt_id
    )
    recorder.record_pre_invocation_abort("aborted before invoke", now=_ANCHOR_NOW)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_LIVE
    assert provider.calls == 0


def test_already_invoked_reservation_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    manager, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    recorder = AttemptOutcomeRecorder(
        tmp_path, bundle.policy.campaign_id, attempt_id
    )
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_LIVE
    assert provider.calls == 0


def test_deleted_reservation_file_zero_provider_calls(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)

    manager, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)
    # Tampering: the durable reservation file disappears.
    res_file = (
        Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
        / "reservation.yaml"
    )
    res_file.unlink()

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_LIVE
    assert provider.calls == 0


# ---------------------------------------------------------------------------
# Success path
# ---------------------------------------------------------------------------


def test_success_invoked_durable_before_provider_call(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    result = _invoke(tmp_path, bundle, capability, reservation, provider)

    assert result.state == AttemptState.VALIDATION_PASSED.value
    assert provider.calls == 1
    # The provider observed the durable INVOKED transition before it ran.
    assert provider.latest_states_at_call == [AttemptState.INVOKED.value]
    assert _ledger_states(tmp_path, bundle, attempt_id) == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
        AttemptState.OUTPUT_CAPTURED.value,
        AttemptState.VALIDATION_PASSED.value,
    ]

    attempt_dir = Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "raw-output.bin").read_bytes() == b"raw provider response"
    assert (attempt_dir / "produced-artifact.md").read_text(
        encoding="utf-8"
    ) == "# candidate artifact"
    assert (attempt_dir / "validation-result.json").exists()
    assert (attempt_dir / "attempt-result.yaml").exists()
    raw_result = yaml.safe_load(
        (attempt_dir / "attempt-result.yaml").read_text(encoding="utf-8")
    )
    assert raw_result["state"] == "VALIDATION_PASSED"
    assert raw_result["raw_output_reference"].endswith("raw-output.bin")


def test_capability_spent_after_success(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    _invoke(tmp_path, bundle, capability, reservation, provider)
    assert capability.consumed is True


# ---------------------------------------------------------------------------
# Provider failure
# ---------------------------------------------------------------------------


def test_provider_failure_records_and_burns(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    provider.exception = RuntimeError("provider exploded")
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    with pytest.raises(RuntimeError, match="provider exploded"):
        _invoke(tmp_path, bundle, capability, reservation, provider)

    assert provider.calls == 1
    assert _ledger_states(tmp_path, bundle, attempt_id) == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
        AttemptState.PROVIDER_FAILED.value,
    ]
    # The spent capability can never authorize anything again.
    assert capability.consumed is True
    attempt_dir = Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
    raw_result = yaml.safe_load(
        (attempt_dir / "attempt-result.yaml").read_text(encoding="utf-8")
    )
    assert raw_result["state"] == "PROVIDER_FAILED"
    assert raw_result["provider_invoked_at"] is not None


def test_no_hidden_retry_after_provider_failure(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    provider.exception = RuntimeError("boom")
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    with pytest.raises(RuntimeError):
        _invoke(tmp_path, bundle, capability, reservation, provider)

    # Re-running the SAME attempt must fail before the provider is reached.
    provider.exception = None
    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider)
    assert exc_info.value.failure_code == RESERVATION_NOT_LIVE
    assert provider.calls == 1  # still exactly one provider call ever


def test_retry_is_a_new_attempt(tmp_path: Path) -> None:
    """A retry is a new reservation, a new attempt ID, a new budget charge."""
    bundle = build_valid_bundle()
    first_id = new_attempt_id()
    capability1 = _mint(bundle, first_id)
    provider1 = SpyProvider(tmp_path, bundle, first_id)
    provider1.exception = RuntimeError("boom")
    _, reservation1 = _reserve(tmp_path, bundle, attempt_id=first_id)
    with pytest.raises(RuntimeError):
        _invoke(tmp_path, bundle, capability1, reservation1, provider1)

    second_id = new_attempt_id()
    capability2 = _mint(bundle, second_id)
    provider2 = SpyProvider(tmp_path, bundle, second_id)
    _, reservation2 = _reserve(tmp_path, bundle, attempt_id=second_id)
    result = _invoke(tmp_path, bundle, capability2, reservation2, provider2)

    assert result.state == AttemptState.VALIDATION_PASSED.value
    assert result.attempt_id == second_id
    assert first_id != second_id
    # Both attempts remain visible; both consumed an attempt slot.
    assert _ledger_states(tmp_path, bundle, first_id)[-1] == AttemptState.PROVIDER_FAILED.value
    assert _ledger_states(tmp_path, bundle, second_id)[-1] == AttemptState.VALIDATION_PASSED.value


# ---------------------------------------------------------------------------
# Interruption handling (Phase 3 follow-up #2)
# ---------------------------------------------------------------------------


def test_keyboard_interrupt_leaves_invoked_durable(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    provider.exception = KeyboardInterrupt()
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    with pytest.raises(KeyboardInterrupt):
        _invoke(tmp_path, bundle, capability, reservation, provider)

    # The interruption is re-raised, but the attempt is durably visible as
    # INVOKED-incomplete: spent, never retried, never erased.
    assert _ledger_states(tmp_path, bundle, attempt_id) == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
    ]
    assert capability.consumed is True
    attempt_dir = Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
    # No OUTPUT_CAPTURED event, no fabricated result file.
    assert not (attempt_dir / "attempt-result.yaml").exists()
    assert not (attempt_dir / "raw-output.bin").exists()


def test_system_exit_leaves_invoked_durable(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    provider.exception = SystemExit(3)
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    with pytest.raises(SystemExit):
        _invoke(tmp_path, bundle, capability, reservation, provider)

    assert _ledger_states(tmp_path, bundle, attempt_id) == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
    ]
    assert capability.consumed is True


# ---------------------------------------------------------------------------
# Validation failure preserves evidence
# ---------------------------------------------------------------------------


def test_validation_failure_preserves_raw_and_artifact(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = SpyProvider(tmp_path, bundle, attempt_id)
    _, reservation = _reserve(tmp_path, bundle, attempt_id=attempt_id)

    def failing_validate(raw):
        assert raw == b"raw provider response"
        return ValidationOutcome(
            passed=False,
            details={"validator": "schema mismatch at line 3"},
            artifact_content="# broken candidate",
        )

    result = _invoke(
        tmp_path, bundle, capability, reservation, provider, validate=failing_validate
    )

    assert result.state == AttemptState.VALIDATION_FAILED.value
    assert result.validation_outcome["passed"] is False
    attempt_dir = Path(tmp_path) / bundle.policy.campaign_id / "attempts" / attempt_id
    # The raw provider output survives the validation failure untouched.
    assert (attempt_dir / "raw-output.bin").read_bytes() == b"raw provider response"
    # The produced artifact is preserved for inspection alongside it.
    assert (attempt_dir / "produced-artifact.md").read_text(
        encoding="utf-8"
    ) == "# broken candidate"
    assert _ledger_states(tmp_path, bundle, attempt_id)[-1] == (
        AttemptState.VALIDATION_FAILED.value
    )
