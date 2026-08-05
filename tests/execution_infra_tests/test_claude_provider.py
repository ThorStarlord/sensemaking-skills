"""ClaudeProvider tests (Phase 6 correction, #122).

Proves the STRUCTURAL provider gate:

* no SDK import without a genuine, consumed, attempt-bound permit;
* the class is not subclassable (a subclass cannot override the gate);
* the bound configuration must equal the invocation context (model,
  target, framework, artifact);
* the SDK tool envelope is Read/Glob/Grep only, no settings sources, no
  MCP servers, cwd = target checkout;
* usage observations are extracted from ResultMessage objects;
* the provider performs no filesystem persistence.

A fake ``claude_agent_sdk`` module substitutes the real SDK; an import
blocker proves the SDK is never imported on denial paths.
"""

import sys
import types
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
    DurableReservationManager,
    invoke_exploratory_attempt,
)
from sensemaking_skills.campaign_accounting.models import ProviderResponse
from sensemaking_skills.exploratory_authorization import mint_exploratory_capability
from sensemaking_skills.exploratory_execution import (
    ALLOWED_SDK_TOOLS,
    ALLOWED_SETTING_SOURCES,
    ClaudeProvider,
    ProviderConfigMismatch,
    ProviderInvocationError,
    ProviderPermitDenied,
)


class _FakeOptions:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def _install_fake_sdk(monkeypatch, script):
    """Install a fake claude_agent_sdk whose query runs ``script``."""
    fake = types.ModuleType("claude_agent_sdk")
    calls = []

    async def fake_query(prompt, options):
        calls.append({"prompt": prompt, "options": options})
        for item in script(prompt, options):
            yield item

    fake.query = fake_query
    fake.ClaudeAgentOptions = _FakeOptions
    monkeypatch.setitem(sys.modules, "claude_agent_sdk", fake)
    return calls


def _block_sdk_imports(monkeypatch):
    """Make any claude_agent_sdk import raise a sentinel error."""
    class Blocker:
        def find_module(self, name, path=None):
            if name == "claude_agent_sdk" or name.startswith("claude_agent_sdk."):
                return self
            return None

        def load_module(self, name):
            raise ImportError("SDK IMPORT BLOCKED")
    monkeypatch.setitem(sys.modules, "claude_agent_sdk", None)
    return Blocker()


class _Message:
    def __init__(self, text=None, total_cost_usd=None, usage=None):
        self.text = text
        self.total_cost_usd = total_cost_usd
        self.usage = usage


class _Usage:
    def __init__(self, input_tokens=0, output_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


def _provider(**overrides):
    kwargs = dict(
        model="example-model-identifier",
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        framework_sha="000000000000000000000000000000000000dead",
        artifact_type="attempt_result",
        target_checkout=Path("/tmp/example-target"),
    )
    kwargs.update(overrides)
    return ClaudeProvider(**kwargs)


def _genuine_permit(tmp_path, bundle, attempt_id):
    """Drive an attempt to a consumed genuine permit and STOP at INVOKED
    (durable INVOKED -> issue -> consume), so the provider-under-test can
    be called with a live permit."""
    from sensemaking_skills.campaign_accounting import (
        AttemptOutcomeRecorder,
        consume_provider_permit,
        issue_provider_permit,
    )
    manager = DurableReservationManager(tmp_path)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    from exploratory_fixtures import build_request
    capability = mint_exploratory_capability(
        bundle,
        build_request(
            attempt_id=attempt_id,
            configuration_id=bundle.configuration.configuration_id,
        ),
        verifier=TrustedReferenceProvenanceVerifier(),
        now=_ANCHOR_NOW.isoformat(),
    )
    recorder = AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, attempt_id)
    recorder.record_raw_request(b"p", now=_ANCHOR_NOW)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    permit = issue_provider_permit(
        campaign_root=tmp_path,
        campaign_id=bundle.policy.campaign_id,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        now=_ANCHOR_NOW,
    )
    consume_provider_permit(permit, campaign_root=tmp_path)
    return permit, make_context(
        capability=capability, campaign_root=str(tmp_path)
    )


def test_provider_is_not_subclassable() -> None:
    with pytest.raises(TypeError):
        class Evil(ClaudeProvider):  # type: ignore[misc]
            def __call__(self, *, permit, context, prompt) -> ProviderResponse:
                return ProviderResponse(raw_output=b"attacker bytes")


def test_direct_call_without_permit_fails_before_sdk_import(monkeypatch) -> None:
    """A bare provider() call is refused with NO SDK import at all."""
    _block_sdk_imports(monkeypatch)
    provider = _provider()
    with pytest.raises(TypeError):
        provider()  # missing required keyword arguments


def test_call_with_forged_permit_fails_before_sdk_import(monkeypatch) -> None:
    _block_sdk_imports(monkeypatch)
    provider = _provider()
    with pytest.raises(ProviderPermitDenied):
        provider(
            permit=object(),  # not a ProviderPermit at all
            context=object(),
            prompt="p",
        )


def test_call_with_unconsumed_genuine_permit_fails_before_sdk_import(
    tmp_path, monkeypatch
) -> None:
    """Even a GENUINE permit fails the provider gate if the registry does
    not show it consumed (the boundary always consumes before entry)."""
    _block_sdk_imports(monkeypatch)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    # Issue but do NOT consume: the gate must refuse.
    from sensemaking_skills.campaign_accounting import (
        AttemptOutcomeRecorder,
        issue_provider_permit,
    )
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    recorder = AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    permit = issue_provider_permit(
        campaign_root=tmp_path,
        campaign_id=bundle.policy.campaign_id,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        now=_ANCHOR_NOW,
    )
    from sensemaking_skills.exploratory_authorization.models import (
        ExploratoryInvocationContext,
    )
    context = ExploratoryInvocationContext(
        model="example-model-identifier",
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        framework_sha="000000000000000000000000000000000000dead",
        artifact_type="attempt_result",
        output_path="/tmp/x.md",
        campaign_id=bundle.policy.campaign_id,
        configuration_id=bundle.configuration.configuration_id,
        configuration_snapshot_digest="0" * 64,
        policy_digest="0" * 64,
        approval_digest="0" * 64,
        attempt_id=attempt_id,
        lane="EXPLORATORY",
        campaign_root=str(tmp_path),
    )
    provider = _provider()
    with pytest.raises(ProviderPermitDenied):
        provider(permit=permit, context=context, prompt="p")


def test_config_mismatch_fails_before_sdk_import(tmp_path, monkeypatch) -> None:
    """A provider built from a DIFFERENT configuration cannot reach the SDK
    even with a genuine permit: the runner's class check alone would be
    insufficient."""
    _block_sdk_imports(monkeypatch)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    permit, context = _genuine_permit(tmp_path, bundle, attempt_id)
    provider = _provider(model="claude-opus-4")  # wrong model
    with pytest.raises(ProviderConfigMismatch):
        provider(permit=permit, context=context, prompt="p")


def test_sdk_call_envelope_is_minimal_and_gated(tmp_path, monkeypatch) -> None:
    """With a genuine consumed permit and matching config, the SDK is
    reached with the minimal envelope: cwd = target checkout, Read/Glob/
    Grep only, no settings sources, no MCP servers."""
    calls = []

    def script(prompt, options):
        yield _Message(text="hello")

    calls = _install_fake_sdk(monkeypatch, script)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    permit, context = _genuine_permit(tmp_path, bundle, attempt_id)
    provider = _provider()
    response = provider(permit=permit, context=context, prompt="the prompt")

    assert response.raw_output == b"hello"
    assert len(calls) == 1
    options = calls[0]["options"]
    assert options.cwd == str(Path("/tmp/example-target"))
    assert options.model == "example-model-identifier"
    assert tuple(options.allowed_tools) == ("Read", "Glob", "Grep")
    assert ALLOWED_SDK_TOOLS == ("Read", "Glob", "Grep")
    assert "Write" not in options.allowed_tools
    assert options.setting_sources == list(ALLOWED_SETTING_SOURCES)
    assert options.setting_sources == []
    assert options.mcp_servers == {}
    assert options.skills == []
    assert calls[0]["prompt"] == "the prompt"


def test_result_message_usage_is_extracted(tmp_path, monkeypatch) -> None:
    def script(prompt, options):
        yield _Message(text="brief content")
        yield _Message(
            text=None,
            total_cost_usd=1.25,
            usage=_Usage(input_tokens=100, output_tokens=50),
        )

    calls = _install_fake_sdk(monkeypatch, script)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    permit, context = _genuine_permit(tmp_path, bundle, attempt_id)
    provider = _provider()
    response = provider(permit=permit, context=context, prompt="p")
    assert response.raw_output == b"brief content"
    assert response.tokens_observed == 150
    assert response.cost_observed == {"amount": 1.25, "currency": "USD"}


def test_empty_output_fails_closed(tmp_path, monkeypatch) -> None:
    def script(prompt, options):
        yield _Message(text=None)
        yield _Message(text="")

    _install_fake_sdk(monkeypatch, script)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    permit, context = _genuine_permit(tmp_path, bundle, attempt_id)
    provider = _provider()
    with pytest.raises(ProviderInvocationError):
        provider(permit=permit, context=context, prompt="p")


def test_provider_creates_no_files(tmp_path, monkeypatch) -> None:
    """The provider performs no artifact persistence: nothing is created
    outside the attempt directory by the provider itself."""
    def script(prompt, options):
        yield _Message(text="brief")

    _install_fake_sdk(monkeypatch, script)
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    permit, context = _genuine_permit(tmp_path, bundle, attempt_id)
    provider = _provider()
    provider(permit=permit, context=context, prompt="p")
    # No timestamped campaign-level raw file outside the attempt dirs
    # (raw-request.txt / raw-output.bin under attempts/ are recorded by the
    # durable boundary, which is the sole persistence authority).
    stray = [
        str(p)
        for p in Path(tmp_path).rglob("*")
        if p.name.startswith("raw-") and "attempts" not in p.parts
    ]
    assert stray == []
