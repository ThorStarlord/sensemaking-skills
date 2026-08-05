"""Provider permit tests (Phase 6 correction, #122).

The provider permit is the STRUCTURAL gate: no permit issuance before the
durable INVOKED transition; no genuine permit without the on-disk registry
record; no consumption twice; no provider-side usability for forged,
unconsumed, or stale permits. No SDK import or provider call ever happens
in these tests.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from exploratory_fixtures import (
    _ANCHOR_NOW,
    TrustedReferenceProvenanceVerifier,
    build_valid_bundle,
    make_context,
    new_attempt_id,
)

from sensemaking_skills.campaign_accounting import (
    CampaignAccountingError,
    DurableReservationManager,
    ProviderPermit,
    consume_provider_permit,
    invoke_exploratory_attempt,
    is_genuine_provider_permit,
    issue_provider_permit,
)
from sensemaking_skills.campaign_accounting.models import ProviderResponse
from sensemaking_skills.exploratory_authorization import mint_exploratory_capability


class NoopProvider:
    def __call__(self, *, permit, context, prompt) -> ProviderResponse:
        return ProviderResponse(raw_output=b"raw")


def _reserve_and_mint(tmp_path, bundle, attempt_id):
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    capability = mint_exploratory_capability(
        bundle,
        _request(bundle, attempt_id),
        verifier=TrustedReferenceProvenanceVerifier(),
        now=_ANCHOR_NOW.isoformat(),
    )
    return reservation, capability


def _request(bundle, attempt_id):
    from exploratory_fixtures import build_request
    return build_request(
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
    )


def test_permit_is_not_publicly_constructible() -> None:
    with pytest.raises(TypeError):
        ProviderPermit(  # type: ignore[call-arg]
            permit_id="0" * 64,
            attempt_id="a1b2c3d4-e5f6-4789-8abc-def012345678",
            campaign_id="EXP-9001-alpha",
            configuration_id="0" * 64,
            issued_at=_ANCHOR_NOW.isoformat(),
        )


def test_permit_requires_durable_invoked_before_issuance(tmp_path) -> None:
    """A permit can never be issued while the attempt is still RESERVED."""
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    _reserve_and_mint(tmp_path, bundle, attempt_id)

    with pytest.raises(CampaignAccountingError) as exc:
        issue_provider_permit(
            campaign_root=tmp_path,
            campaign_id=bundle.policy.campaign_id,
            attempt_id=attempt_id,
            configuration_id=bundle.configuration.configuration_id,
            now=_ANCHOR_NOW,
        )
    assert exc.value.failure_code == "PROVIDER_PERMIT_NOT_ISSUED"
    # No provider call, no state change.
    ledger = _ledger_states(tmp_path, bundle, attempt_id)
    assert ledger == ["RESERVED"]


def test_boundary_issues_and_consumes_permit_before_provider(tmp_path) -> None:
    """The full boundary: INVOKED durable -> permit issued -> permit
    consumed -> provider entered. The provider observes a genuine consumed
    permit bound to its attempt."""
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    reservation, capability = _reserve_and_mint(tmp_path, bundle, attempt_id)

    observed = {}

    class Observer:
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            observed["permit"] = permit
            observed["attempt"] = context.attempt_id
            observed["prompt"] = prompt
            # Liveness at the provider boundary: ledger still INVOKED.
            observed["genuine_at_call"] = is_genuine_provider_permit(
                permit, campaign_root=Path(tmp_path)
            )
            return ProviderResponse(raw_output=b"raw")

    invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=Path(tmp_path),
        context=make_context(capability=capability),
        provider=Observer(),
        validate=_passing_validate,
        prompt="the exact prompt",
        now=_ANCHOR_NOW,
    )
    permit = observed["permit"]
    assert observed["attempt"] == attempt_id
    assert observed["prompt"] == "the exact prompt"
    # The provider-side gate passes for the genuine consumed permit while
    # the attempt is INVOKED...
    assert observed["genuine_at_call"] is True
    # ...and the spent permit is dead once the attempt completes (the
    # ledger moved past INVOKED).
    assert is_genuine_provider_permit(permit, campaign_root=tmp_path) is False
    # The permit file exists in the attempt directory with consumed: true.
    permit_file = (
        tmp_path / bundle.policy.campaign_id / "attempts" / attempt_id
        / "provider-permit.yaml"
    )
    assert permit_file.is_file()
    import yaml
    on_disk = yaml.safe_load(permit_file.read_text(encoding="utf-8"))
    assert on_disk["consumed"] is True
    assert on_disk["attempt_id"] == attempt_id


def test_consumed_permit_cannot_be_consumed_twice(tmp_path) -> None:
    """The boundary consumes the permit before provider entry; a second
    consume of the same genuine permit must fail (one-shot)."""
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    captured = {}

    class DoubleConsume:
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            captured["code"] = None
            try:
                consume_provider_permit(permit, campaign_root=Path(tmp_path))
            except CampaignAccountingError as exc:
                captured["code"] = exc.failure_code
            return ProviderResponse(raw_output=b"raw")

    reservation, capability = _reserve_and_mint(tmp_path, bundle, attempt_id)
    invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=Path(tmp_path),
        context=make_context(capability=capability),
        provider=DoubleConsume(),
        validate=_passing_validate,
        prompt="p",
        now=_ANCHOR_NOW,
    )
    assert captured["code"] == "PROVIDER_PERMIT_ALREADY_CONSUMED"


def _stale_permit_from_disk(tmp_path, bundle, attempt_id):
    """Reconstruct a permit object WITHOUT the closure sentinel: it must
    fail the genuine check at consume time."""
    return object.__new__(ProviderPermit)


def test_forged_permit_is_never_genuine(tmp_path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    reservation, capability = _reserve_and_mint(tmp_path, bundle, attempt_id)
    invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=Path(tmp_path),
        context=make_context(capability=capability),
        provider=NoopProvider(),
        validate=_passing_validate,
        prompt="p",
        now=_ANCHOR_NOW,
    )
    # A sentinel-less reconstruction is not genuine.
    forged = _stale_permit_from_disk(tmp_path, bundle, attempt_id)
    assert is_genuine_provider_permit(forged, campaign_root=tmp_path) is False


def test_permit_is_bound_to_the_exact_attempt(tmp_path) -> None:
    """A permit minted for attempt A is not usable for attempt B."""
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    captured = {}

    class WrongAttempt:
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            from sensemaking_skills.campaign_accounting import (
                require_usable_provider_permit,
            )
            try:
                require_usable_provider_permit(
                    permit,
                    campaign_root=Path(tmp_path),
                    attempt_id="b2b2c3d4-e5f6-4789-8abc-def012345678",
                    campaign_id=bundle.policy.campaign_id,
                    configuration_id=bundle.configuration.configuration_id,
                )
                captured["code"] = None
            except CampaignAccountingError as exc:
                captured["code"] = exc.failure_code
            return ProviderResponse(raw_output=b"raw")

    reservation, capability = _reserve_and_mint(tmp_path, bundle, attempt_id)
    invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=Path(tmp_path),
        context=make_context(capability=capability),
        provider=WrongAttempt(),
        validate=_passing_validate,
        prompt="p",
        now=_ANCHOR_NOW,
    )
    assert captured["code"] == "PROVIDER_PERMIT_ATTEMPT_MISMATCH"


def _passing_validate(raw: bytes):
    from sensemaking_skills.campaign_accounting import ValidationOutcome
    return ValidationOutcome(passed=True, details={}, artifact_content="# ok")


def _ledger_states(tmp_path, bundle, attempt_id):
    from sensemaking_skills.campaign_accounting import CampaignLedger
    ledger = CampaignLedger(
        Path(tmp_path) / bundle.policy.campaign_id, bundle.policy.campaign_id
    )
    return [
        e.event_type
        for e in ledger.read_events()
        if e.attempt_id == attempt_id
    ]
