"""Phase 3 (#119): real-executor provider-boundary proofs for the EXPLORATORY
lane.

The four-lane model is enforced where it can actually be violated: in the
REAL production executors in `scripts/skill_executor.py`, immediately
before the provider SDK call. This module exercises
`ClaudeAgentSdkSkillExecutor` with a spy provider substituted for the SDK
entrypoint, mirroring `test_gate_a_invocation_boundary.py`.

Invariants under test:

- An EXPLORATORY invocation without an exploratory capability never reaches
  the provider (EXPLORATORY_CAPABILITY_REQUIRED, zero calls).
- An EXPLORATORY invocation with a capability consumes it exactly once at
  the narrowest point, calls the provider exactly once with the bound
  model, and is permanently spent afterwards.
- A capability bound to different invocation facts (any of 13 drift
  categories) burns the capability and never calls the provider.
- The capability type is lane-specific: an exploratory capability can never
  satisfy a CANONICAL invocation, and a canonical AuthorizedInvocation can
  never satisfy an EXPLORATORY lane (each fails closed, zero calls).
- Mixed evidence (exploratory claims on an ordinary-classified path, or any
  non-campaign experiments path) maps to AMBIGUOUS and requires the
  canonical capability -- the exploratory capability does not run it.
- A provider exception after consumption burns the capability permanently.

NO REAL MODEL IS EVER INVOKED HERE. The spy replaces
`claude_agent_sdk.query` (via the name bound inside skill_executor) and
`anthropic.Anthropic`. Any attempt to reach a real provider would raise.
"""

from __future__ import annotations

import subprocess
import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402
import skill_executor as se  # noqa: E402
from gate_a_fixtures import build_valid_case  # noqa: E402

import exploratory_fixtures as ef  # noqa: E402
import sensemaking_skills.exploratory_authorization as ea  # noqa: E402

CAMPAIGN_ID = ef.TEST_CAMPAIGN_ID
CLASSIFICATION = "EXPLORATORY_NOT_CANONICAL_EVIDENCE"


# ===========================================================================
# Spy provider
# ===========================================================================


class SpyProvider:
    """Counts provider calls. Never contacts a network or a model."""

    def __init__(self):
        self.model_invocation_count = 0
        self.fallback_invocation_count = 0
        self.retry_invocation_count = 0
        self.models_requested: list = []
        #: When set, the provider call RAISES after being counted.
        self.raise_on_call = None

    def query(self, prompt=None, options=None):
        self.model_invocation_count += 1
        self.models_requested.append(getattr(options, "model", None))
        if getattr(options, "fallback_model", None):
            self.fallback_invocation_count += 1
        if self.raise_on_call is not None:
            raise self.raise_on_call

        async def _agen():
            if False:  # pragma: no cover - shapes the async generator
                yield None

        return _agen()

    def anthropic_client_factory(self, *a, **k):
        spy = self

        class _Messages:
            def create(self, model=None, **kwargs):
                spy.model_invocation_count += 1
                spy.models_requested.append(model)
                raise AssertionError(
                    "SpyProvider: a model call escaped the authorization boundary"
                )

        class _Client:
            messages = _Messages()

        return _Client()


@pytest.fixture
def spy(monkeypatch):
    s = SpyProvider()

    import claude_agent_sdk
    assert hasattr(claude_agent_sdk, "query"), (
        "claude_agent_sdk.query is the real invocation entrypoint; if this "
        "attribute moved, these tests are no longer patching the provider")
    monkeypatch.setattr(claude_agent_sdk, "query", s.query)

    try:
        import anthropic
        monkeypatch.setattr(anthropic, "Anthropic", s.anthropic_client_factory)
    except ImportError:
        pass

    return s


@pytest.fixture(autouse=True)
def _fresh_registry():
    """Each test starts from an empty process-local issuer registry."""
    ea.reset_exploratory_registry()
    yield


# ===========================================================================
# Helpers
# ===========================================================================


def campaign_output_path(campaign_id: str = CAMPAIGN_ID,
                         attempt: str = "attempt-1.md") -> str:
    return str(REPO_ROOT / "experiments" / "campaigns" / campaign_id
               / "attempts" / attempt)


def mint_capability(tmp_path, **request_overrides):
    bundle = ef.build_valid_bundle()
    request = ef.build_request(
        configuration_id=bundle.configuration.configuration_id,
        output_path=campaign_output_path(), **request_overrides)
    return ea.mint_exploratory_capability(
        bundle, request, verifier=ef.TrustedReferenceProvenanceVerifier(),
        now=ef.TEST_VALIDATION_TIME)


def exploratory_executor(tmp_path, capability, *, model=ef.TEST_MODEL):
    return se.ClaudeAgentSdkSkillExecutor(
        repo_root=str(REPO_ROOT),
        model=model,
        controlled_experiment=False,
        authorization=None,
        exploratory_capability=capability,
        invocation_identity=None,
    )


def invocation_context(capability, tmp_path, **overrides):
    b = capability.binding
    ctx = {
        "workflow_id": "phase3-test-workflow",
        "expected_output_path": b.bound_output_path,
        "artifact_session_dir": str(tmp_path / "session"),
        "artifact_type": "attempt_result",
        "workflow_stage": "stage-2",
        "campaign_id": b.campaign_id,
        "classification": CLASSIFICATION,
        "attempt_id": b.attempt_id,
        "configuration_id": b.configuration_id,
        "configuration_snapshot_digest": b.configuration_snapshot_digest,
        "policy_digest": b.policy_digest,
        "approval_digest": b.approval_digest,
        "execution_framework_sha": b.framework_sha,
        "target_repository": b.target_repository,
        "target_sha": b.target_sha,
    }
    ctx.update(overrides)
    return ctx


def invoke(executor, ctx):
    return executor.invoke_skill(
        skill_id="repo-sensemaker",
        invocation_command="/skill repo-sensemaker",
        input_artifacts=[],
        expected_output_artifact="attempt_result",
        context=ctx,
    )


def assert_zero_invocation(spy, capability):
    assert spy.model_invocation_count == 0, "a model call escaped the boundary"
    assert spy.fallback_invocation_count == 0, "a fallback call escaped the boundary"
    assert spy.retry_invocation_count == 0, "a retry call escaped the boundary"
    assert not Path(capability.binding.bound_output_path).exists(), (
        "an output artifact was created")


def test_boundary_tests_leave_the_working_tree_clean():
    """Guard: this suite must not create untracked files in the repository."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain",
         "--", "artifacts/", "experiments/campaigns/"],
        capture_output=True, text=True, check=False,
    )
    assert result.stdout.strip() == "", (
        f"the exploratory boundary tests dirtied the working tree:\n"
        f"{result.stdout}")


# ===========================================================================
# Positive proof: exactly one invocation, exactly one consumption
# ===========================================================================


def test_exploratory_invocation_consumes_and_invokes_provider_exactly_once(
        tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    result = invoke(executor, invocation_context(cap, tmp_path))

    assert result.status == se.SkillExecutionStatus.FAILED  # honest: no artifact
    assert spy.model_invocation_count == 1
    assert spy.models_requested == [ef.TEST_MODEL]
    assert spy.fallback_invocation_count == 0
    assert spy.retry_invocation_count == 0
    assert cap.consumed is True
    assert not Path(cap.binding.bound_output_path).exists()


def test_exploratory_capability_is_spent_after_first_invocation(tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    ctx = invocation_context(cap, tmp_path)

    first = invoke(executor, ctx)
    assert spy.model_invocation_count == 1

    second = invoke(executor, ctx)
    assert second.status == se.SkillExecutionStatus.FAILED
    assert ea.EXPLORATORY_CAPABILITY_ALREADY_CONSUMED in second.error
    assert spy.model_invocation_count == 1, (
        "a spent capability authorized a second provider call")


# ===========================================================================
# Negative proofs: every rejection leaves the provider untouched
# ===========================================================================


def test_exploratory_invocation_without_capability_never_calls_provider(
        tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, None)
    result = invoke(executor, invocation_context(cap, tmp_path))

    assert result.status == se.SkillExecutionStatus.FAILED
    assert ea.EXPLORATORY_CAPABILITY_REQUIRED in result.error
    assert_zero_invocation(spy, cap)


def test_exploratory_capability_cannot_satisfy_canonical_gate(tmp_path, spy):
    cap = mint_capability(tmp_path)
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.ClaudeAgentSdkSkillExecutor(
            repo_root=str(REPO_ROOT),
            model=ef.TEST_MODEL,
            controlled_experiment=True,
            exploratory_capability=cap,
        )
    assert exc.value.code == ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED
    assert spy.model_invocation_count == 0


def test_canonical_capability_cannot_satisfy_exploratory_lane(tmp_path, spy):
    canonical = make_canonical_capability(tmp_path)
    executor = exploratory_executor(tmp_path, canonical)
    ctx = invocation_context(mint_capability(tmp_path), tmp_path)
    result = invoke(executor, ctx)

    assert result.status == se.SkillExecutionStatus.FAILED
    assert ea.EXPLORATORY_CAPABILITY_WRONG_TYPE in result.error
    assert spy.model_invocation_count == 0


def test_exploratory_capability_rejected_on_non_campaign_experiments_path(
        tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    ctx = invocation_context(cap, tmp_path, expected_output_path=(
        str(REPO_ROOT / "experiments" / "scratch" / "notes.md")))
    result = invoke(executor, ctx)

    assert result.status == se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS in result.error
    assert cap.consumed is False
    assert_zero_invocation(spy, cap)


def test_exploratory_capability_rejected_on_evidence_namespace(tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    ctx = invocation_context(cap, tmp_path, expected_output_path=(
        str(REPO_ROOT / "experiments" / "evidence" / "0016-sensemaking"
            / "artifacts" / "summary.md")))
    result = invoke(executor, ctx)

    assert result.status == se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS in result.error
    assert cap.consumed is False
    assert_zero_invocation(spy, cap)


def test_mixed_exploratory_declaration_on_ordinary_path_is_ambiguous(
        tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    ctx = invocation_context(cap, tmp_path, expected_output_path=(
        str(REPO_ROOT / "artifacts" / "brief.md")))
    result = invoke(executor, ctx)

    assert result.status == se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS in result.error
    assert cap.consumed is False
    assert_zero_invocation(spy, cap)


def test_ordinary_invocation_ignores_exploratory_capability(tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    session_dir = tmp_path / "session"
    session_dir.mkdir(exist_ok=True)
    result = invoke(executor, {
        "expected_output_path": str(REPO_ROOT / "artifacts" / "brief.md"),
        "artifact_session_dir": str(session_dir),
        "artifact_type": "attempt_result",
        "workflow_stage": "stage-2",
    })

    assert spy.model_invocation_count == 1
    assert spy.models_requested == [ef.TEST_MODEL]
    assert cap.consumed is False, (
        "an ORDINARY invocation must not consult the exploratory capability")


# ===========================================================================
# Drift: a capability bound to other invocation facts is burned, provider
# untouched
# ===========================================================================

DRIFT_CASES = {
    "model": (
        {},
        {"model": "example-model-other"},
        ea.EXPLORATORY_BINDING_MODEL_MISMATCH,
    ),
    "target_repository": (
        {"target_repository": "https://example.invalid/other-owner/other.git"},
        {},
        ea.EXPLORATORY_BINDING_TARGET_REPOSITORY_MISMATCH,
    ),
    "target_sha": (
        {"target_sha": "a" * 40},
        {},
        ea.EXPLORATORY_BINDING_TARGET_SHA_MISMATCH,
    ),
    "framework_sha": (
        {"execution_framework_sha": "b" * 40},
        {},
        ea.EXPLORATORY_BINDING_FRAMEWORK_SHA_MISMATCH,
    ),
    "artifact_type": (
        {"artifact_type": "session_log"},
        {},
        ea.EXPLORATORY_BINDING_ARTIFACT_TYPE_MISMATCH,
    ),
    "configuration_id": (
        {"configuration_id": "2" * 64},
        {},
        ea.EXPLORATORY_BINDING_CONFIGURATION_ID_MISMATCH,
    ),
    "configuration_snapshot_digest": (
        {"configuration_snapshot_digest": "3" * 64},
        {},
        ea.EXPLORATORY_BINDING_CONFIGURATION_SNAPSHOT_MISMATCH,
    ),
    "policy_digest": (
        {"policy_digest": "4" * 64},
        {},
        ea.EXPLORATORY_BINDING_POLICY_DIGEST_MISMATCH,
    ),
    "approval_digest": (
        {"approval_digest": "5" * 64},
        {},
        ea.EXPLORATORY_BINDING_APPROVAL_DIGEST_MISMATCH,
    ),
    "attempt_id": (
        {"attempt_id": str(uuid.uuid4())},
        {},
        ea.EXPLORATORY_BINDING_ATTEMPT_ID_MISMATCH,
    ),
    "campaign_id": (
        {"campaign_id": "EXP-9002-alpha",
         "expected_output_path": campaign_output_path("EXP-9002-alpha")},
        {},
        ea.EXPLORATORY_BINDING_CAMPAIGN_ID_MISMATCH,
    ),
    "output_path": (
        {"expected_output_path": campaign_output_path(attempt="attempt-2.md")},
        {},
        ea.EXPLORATORY_BINDING_OUTPUT_PATH_MISMATCH,
    ),
}


@pytest.mark.parametrize(
    "case",
    list(DRIFT_CASES),
    ids=list(DRIFT_CASES),
)
def test_drift_category_burns_capability_and_never_calls_provider(
        tmp_path, spy, case):
    ctx_overrides, executor_overrides, expected_code = DRIFT_CASES[case]
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap, **executor_overrides)
    ctx = invocation_context(cap, tmp_path, **ctx_overrides)
    result = invoke(executor, ctx)

    assert result.status == se.SkillExecutionStatus.FAILED
    assert expected_code in result.error, result.error
    assert cap.consumed is True, (
        f"a drifted invocation must burn the capability (case: {case})")
    assert_zero_invocation(spy, cap)


def test_declared_controlled_mode_cannot_be_overridden_by_capability(
        tmp_path, spy):
    cap = mint_capability(tmp_path)
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.ClaudeAgentSdkSkillExecutor(
            repo_root=str(REPO_ROOT),
            model=ef.TEST_MODEL,
            controlled_experiment=True,
            exploratory_capability=cap,
        )
    assert exc.value.code == ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED
    assert spy.model_invocation_count == 0


# ===========================================================================
# Provider failure: a spent capability stays permanently spent
# ===========================================================================


def test_provider_exception_burns_capability(tmp_path, spy):
    cap = mint_capability(tmp_path)
    executor = exploratory_executor(tmp_path, cap)
    ctx = invocation_context(cap, tmp_path)

    spy.raise_on_call = RuntimeError("provider down")
    first = invoke(executor, ctx)
    assert first.status == se.SkillExecutionStatus.FAILED
    assert spy.model_invocation_count == 1
    assert cap.consumed is True

    spy.raise_on_call = None
    second = invoke(executor, ctx)
    assert second.status == se.SkillExecutionStatus.FAILED
    assert ea.EXPLORATORY_CAPABILITY_CONSUMPTION_FAILED in second.error
    assert spy.model_invocation_count == 1, (
        "a burned capability authorized a second provider call")


# ===========================================================================
# Canonical capability construction (mirrors test_gate_a_invocation_boundary)
# ===========================================================================


def make_canonical_capability(tmp_path):
    ctx, head, resolver, heads = build_valid_case(tmp_path)
    identity = se.build_invocation_identity(
        repo_root=str(REPO_ROOT),
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path": str(tmp_path / "out" / "brief.md")},
        model=ef.TEST_MODEL,
        declared_controlled_mode=True,
    )
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver,
        invocation_identity=identity,
    )
    assert decision.authorized is True, decision.failure_detail
    return cap
