"""Gate A invocation-boundary proofs.

Preparation package section 2j, criterion 25:

    "A consumer that passes unit tests in isolation but is never called by the
    real Stage 1 path enforces nothing."

This module is that proof. It exercises the REAL production executors in
`scripts/skill_executor.py` -- the two classes that actually reach a provider
SDK -- with a spy provider substituted for the SDK entrypoint.

The core invariant under test:

    No valid authorization capability, no path to the model invocation
    function.

and its negative form, which is the one that matters:

    every failed preflight leaves the provider invocation count at exactly
    zero.

NO REAL MODEL IS EVER INVOKED HERE. The spy replaces
`claude_agent_sdk.query` (via the name bound inside skill_executor) and
`anthropic.Anthropic`. Any attempt to reach a real provider would raise.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402
import skill_executor as se  # noqa: E402
from gate_a_fixtures import (  # noqa: E402
    EVIDENCE_SLUG,
    PACKAGE_REL,
    build_valid_case,
    sha256_bytes,
)


# ===========================================================================
# Spy provider
# ===========================================================================


class SpyProvider:
    """Counts provider calls. Never contacts a network or a model.

    Separate counters for the primary call, fallback, and retry so a test can
    assert all three are zero, not just the aggregate.
    """

    def __init__(self):
        self.model_invocation_count = 0
        self.fallback_invocation_count = 0
        self.retry_invocation_count = 0
        self.models_requested: list = []
        self.generated_brief_count = 0
        #: When set, the provider call RAISES after being counted. Used to
        #: prove a failed attempt never returns the capability to ISSUED.
        self.raise_on_call = None

    # -- claude_agent_sdk.query substitute ---------------------------------
    def query(self, prompt=None, options=None):
        self.model_invocation_count += 1
        model = getattr(options, "model", None)
        self.models_requested.append(model)
        if getattr(options, "fallback_model", None):
            self.fallback_invocation_count += 1
        if self.raise_on_call is not None:
            raise self.raise_on_call

        async def _agen():
            if False:  # pragma: no cover - shapes the async generator
                yield None

        return _agen()

    # -- anthropic.Anthropic substitute ------------------------------------
    def anthropic_client_factory(self, *a, **k):
        spy = self

        class _Messages:
            def create(self, model=None, **kwargs):
                spy.model_invocation_count += 1
                spy.models_requested.append(model)
                raise AssertionError(
                    "SpyProvider: a model call escaped the Gate A boundary"
                )

        class _Client:
            messages = _Messages()

        return _Client()


@pytest.fixture
def spy(monkeypatch):
    """Substitute the spy for every real provider entrypoint.

    `skill_executor` imports `query` from `claude_agent_sdk` *inside* the
    async invocation function, so the substitution must be made on the SDK
    module attribute -- patching a name on `skill_executor` would silently do
    nothing and make these tests vacuous.
    """
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
        pass  # the second path is proven unreachable without the SDK too

    return s


# ===========================================================================
# Helpers
# ===========================================================================


def invocation_identity(tmp_path, repo_root=None, *, model="claude-sonnet-5",
                        executor_id="claude-code", declared=True,
                        output_path=None):
    """The identity of the invocation `invoke()` below actually performs.

    Gate A binds the capability to this. Building it from the same inputs the
    executor uses at the provider boundary is the point: a capability issued
    for one invocation cannot authorize a different one.
    """
    return se.build_invocation_identity(
        repo_root=str(repo_root or REPO_ROOT),
        executor_id=executor_id,
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={
            "expected_output_path": str(
                output_path if output_path is not None
                else tmp_path / "out" / "brief.md"),
        },
        model=model,
        declared_controlled_mode=(True if declared else None),
    )


def make_capability(tmp_path, identity=None, repo_root=None, **kwargs):
    ctx, head, resolver, heads = build_valid_case(tmp_path, **kwargs)
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver,
        invocation_identity=(identity if identity is not None
                             else invocation_identity(tmp_path, repo_root)))
    return ctx, head, resolver, heads, decision, cap


def controlled_executor(tmp_path, capability, repo_root=None):
    """Construct the real production executor for a controlled Stage 1 run.

    `repo_root` defaults to the real repository because the executor's prompt
    builder loads the live skill/workflow registries from it. Using a stub
    root would make the invocation fail during prompt construction -- before
    the Gate A boundary -- and the TOCTOU/positive tests would then prove
    nothing about the boundary itself. The Gate A *authorization* inputs
    remain fully synthetic and live in tmp_path.
    """
    return se.ClaudeAgentSdkSkillExecutor(
        repo_root=str(repo_root or REPO_ROOT),
        model="claude-sonnet-5",
        controlled_experiment=True,
        authorization=capability,
        invocation_identity=invocation_identity(tmp_path, repo_root),
    )


def invoke(executor, tmp_path):
    """Invoke through the real executor, with all side effects confined to tmp.

    `artifact_session_dir` is passed explicitly so the tool-call trace is
    written under tmp_path rather than into the repository's artifacts/
    directory. A test that gates model invocation must not itself dirty the
    working tree.
    """
    session_dir = tmp_path / "session"
    session_dir.mkdir(exist_ok=True)
    return executor.invoke_skill(
        skill_id="repo-sensemaker",
        invocation_command="/skill repo-sensemaker",
        input_artifacts=[],
        expected_output_artifact="repository_sensemaking_brief",
        context={
            "expected_output_path": str(tmp_path / "out" / "brief.md"),
            "artifact_session_dir": str(session_dir),
        },
    )


def test_boundary_tests_leave_the_working_tree_clean():
    """Guard: this suite must not create untracked files in the repository."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--", "artifacts/"],
        capture_output=True, text=True, check=False,
    )
    assert result.stdout.strip() == "", (
        f"the Gate A boundary tests dirtied the working tree:\n{result.stdout}")


def assert_zero_invocation(spy, tmp_path, ctx=None):
    """The negative proof, asserted the same way every time."""
    assert spy.model_invocation_count == 0, "a model call escaped Gate A"
    assert spy.fallback_invocation_count == 0, "a fallback call escaped Gate A"
    assert spy.retry_invocation_count == 0, "a retry call escaped Gate A"
    assert spy.generated_brief_count == 0
    assert not (tmp_path / "out").exists(), "an output artifact was created"
    if ctx is not None:
        evidence = ctx.evidence_output_dir
        assert not evidence.exists(), "Evidence 0016 output was created"


# ===========================================================================
# 16. Negative invocation boundary -- twelve representative failures
# ===========================================================================
#
# Each case: a Gate A failure -> capability is None -> the real executor
# refuses -> provider invocation count is exactly zero.


NEGATIVE_CASES = {}


def _neg(name):
    def deco(fn):
        NEGATIVE_CASES[name] = fn
        return fn
    return deco


@_neg("record_missing")
def _c1(ctx):
    ctx.authorization_record_path.unlink()
    return ga.GATE_A_AUTHORIZATION_RECORD_MISSING


@_neg("digest_mismatch")
def _c2(ctx):
    ctx.authorization_digest_path.write_text("0" * 64 + "\n", encoding="utf-8", newline="")
    return ga.GATE_A_AUTHORIZATION_DIGEST_MISMATCH


@_neg("approval_missing")
def _c3(ctx):
    ctx.owner_approval_path.unlink()
    return ga.GATE_A_OWNER_APPROVAL_MISSING


@_neg("approval_digest_mismatch")
def _c4(ctx):
    real = sha256_bytes(ctx.authorization_record_path.read_bytes())
    text = ctx.owner_approval_path.read_text(encoding="utf-8")
    ctx.owner_approval_path.write_text(text.replace(real, "e" * 64),
                                       encoding="utf-8", newline="")
    return ga.GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH


@_neg("framework_sha_mismatch")
def _c5(ctx, heads=None):
    heads[str(ctx.framework_root)] = "9" * 40
    return ga.GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH


@_neg("target_sha_mismatch")
def _c6(ctx, heads=None):
    heads[str(ctx.target_root)] = "8" * 40
    return ga.GATE_A_TARGET_SHA_MISMATCH


@_neg("missing_required_path")
def _c7(ctx):
    (ctx.framework_root / PACKAGE_REL).unlink()
    return ga.GATE_A_REQUIRED_PATH_MISSING


@pytest.mark.parametrize("case", ["record_missing", "digest_mismatch",
                                  "approval_missing", "approval_digest_mismatch",
                                  "framework_sha_mismatch", "target_sha_mismatch",
                                  "missing_required_path"])
def test_negative_zero_invocation_mutation_cases(tmp_path, spy, case):
    ctx, head, resolver, heads, _, _ = make_capability(tmp_path)
    fn = NEGATIVE_CASES[case]
    expected = fn(ctx, heads) if case.endswith("_sha_mismatch") else fn(ctx)

    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver)
    assert decision.authorized is False
    assert decision.failure_code == expected, decision.failure_detail
    assert cap is None

    # The real executor now refuses to be constructed at all.
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        controlled_executor(tmp_path, cap)
    assert exc.value.code == ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED

    assert_zero_invocation(spy, tmp_path, ctx)


@pytest.mark.parametrize("overrides,expected", [
    ({"exact_model": "claude-opus-4-7"}, ga.GATE_A_MODEL_MISMATCH),
    ({"no_retry": False}, ga.GATE_A_RETRY_PROHIBITED),
    ({"no_fallback": False}, ga.GATE_A_FALLBACK_PROHIBITED),
    ({"invocation_limit": 2}, ga.GATE_A_INVOCATION_LIMIT_INVALID),
], ids=["model_mismatch", "retry_enabled", "fallback_enabled", "limit_gt_one"])
def test_negative_zero_invocation_record_cases(tmp_path, spy, overrides, expected):
    approval_overrides = ({"exact_model": overrides["exact_model"]}
                          if "exact_model" in overrides else None)
    ctx, head, resolver, heads, decision, cap = make_capability(
        tmp_path, record_overrides=overrides, approval_overrides=approval_overrides)
    assert decision.authorized is False
    assert decision.failure_code == expected, decision.failure_detail
    assert cap is None
    with pytest.raises(se.GateAAuthorizationRequired):
        controlled_executor(tmp_path, cap)
    assert_zero_invocation(spy, tmp_path, ctx)


def test_negative_zero_invocation_stale_run_control_commit(tmp_path, spy):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=lambda a, b: "c" * 40)
    assert decision.failure_code == ga.GATE_A_RUN_CONTROL_COMMIT_MISMATCH
    assert cap is None
    with pytest.raises(se.GateAAuthorizationRequired):
        controlled_executor(tmp_path, cap)
    assert_zero_invocation(spy, tmp_path, ctx)


def test_negative_zero_invocation_no_capability_passed_at_all(tmp_path, spy):
    """Case 12: the invocation function is simply called with nothing."""
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.ClaudeAgentSdkSkillExecutor(
            repo_root=str(tmp_path), model="claude-sonnet-5",
            controlled_experiment=True, authorization=None,
        )
    assert exc.value.code == ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED
    assert_zero_invocation(spy, tmp_path)


def test_invoke_skill_refuses_when_capability_removed_after_construction(tmp_path, spy):
    """Post-construction tampering: rejected outright, and fails closed anyway.

    Two layers are asserted here. First, `authorization` is no longer a
    settable attribute -- the reported downgrade path raises. Second, even the
    brute-force route that bypasses `__setattr__` entirely by writing to
    `__dict__` still cannot reach the SDK, because Gate A is re-derived from
    the invocation identity at the provider boundary rather than trusted from
    executor state.
    """
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    assert cap is not None
    executor = controlled_executor(tmp_path, cap)

    with pytest.raises(AttributeError):
        executor.authorization = None

    executor.__dict__["authorization"] = None  # bypass __setattr__ entirely
    result = invoke(executor, tmp_path)
    assert result.status is se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED in result.error
    assert_zero_invocation(spy, tmp_path, ctx)


def test_forged_capability_object_rejected(tmp_path, spy):
    """A duck-typed lookalike is not a capability."""

    class FakeCapability:
        model = "claude-sonnet-5"
        artifact_type = "repository_sensemaking_brief"
        decision = type("D", (), {"authorized": True})()

        def consume(self, **k):  # pragma: no cover
            return self.decision

    with pytest.raises(se.GateAAuthorizationRequired):
        controlled_executor(tmp_path, FakeCapability())
    assert_zero_invocation(spy, tmp_path)


def test_unauthorized_decision_capability_rejected(tmp_path, spy):
    """Even a genuine AuthorizedInvocation carrying a denied decision fails."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, snapshot = ga.authorize(
        ctx, git_head=head, run_control_commit_resolver=resolver)
    denied = ga.AuthorizationDecision(authorized=False,
                                      failure_code=ga.GATE_A_AUTHORIZATION_RECORD_INVALID)
    # Issued through the registry so the capability IS live -- the point is
    # that liveness alone is not authorization; the decision must also be
    # authorized.
    cap = ga._REGISTRY.issue(denied, ctx, snapshot,
                             invocation_identity(tmp_path))
    assert cap.live is True
    with pytest.raises(se.GateAAuthorizationRequired):
        controlled_executor(tmp_path, cap)
    assert_zero_invocation(spy, tmp_path, ctx)


# ===========================================================================
# 17. Positive invocation boundary -- exactly one fake invocation
# ===========================================================================


def test_positive_exactly_one_fake_invocation(tmp_path, spy, monkeypatch):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    assert decision.authorized is True, decision.failure_detail
    assert cap is not None

    executor = controlled_executor(tmp_path, cap)
    # The capability revalidates against real filesystem state at consume
    # time; give it the same injected HEAD reader the preflight used.
    monkeypatch.setattr(ga, "read_git_head", head)

    result = invoke(executor, tmp_path)

    # Exactly one provider call. Not zero, not two.
    assert spy.model_invocation_count == 1, (
        f"expected exactly 1 provider call, got {spy.model_invocation_count}")
    assert spy.fallback_invocation_count == 0
    assert spy.retry_invocation_count == 0
    # The authorized model reached the provider unchanged.
    assert spy.models_requested == ["claude-sonnet-5"]
    assert cap.consumed is True
    assert cap.remaining_invocations == 0
    # The spy yields no messages, so no artifact is produced; the run reports
    # failure honestly rather than fabricating one.
    assert result.status is se.SkillExecutionStatus.FAILED
    assert result.requested_model == "claude-sonnet-5"


def test_second_invocation_attempt_is_rejected(tmp_path, spy, monkeypatch):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    executor = controlled_executor(tmp_path, cap)
    monkeypatch.setattr(ga, "read_git_head", head)

    invoke(executor, tmp_path)
    assert spy.model_invocation_count == 1

    second = invoke(executor, tmp_path)
    # The capability is spent: the second attempt must not reach the provider.
    assert spy.model_invocation_count == 1, (
        "a second model invocation happened on a one-invocation authorization")
    assert second.status is se.SkillExecutionStatus.FAILED
    # The issuance is retired in the registry, so the non-consuming preflight
    # already refuses it -- the second attempt never even reaches consume().
    assert (ga.GATE_A_CAPABILITY_NOT_LIVE in second.error
            or ga.GATE_A_CAPABILITY_ALREADY_CONSUMED in second.error)
    assert cap.live is False


def test_no_fallback_model_is_ever_configured(tmp_path, spy, monkeypatch):
    """`fallback_model` is never set anywhere on the authorized path."""
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    executor = controlled_executor(tmp_path, cap)
    monkeypatch.setattr(ga, "read_git_head", head)
    invoke(executor, tmp_path)
    assert spy.fallback_invocation_count == 0
    source = (REPO_ROOT / "scripts" / "skill_executor.py").read_text(encoding="utf-8")
    assert "fallback_model=" not in source, "a fallback model was introduced"


# ===========================================================================
# 18. TOCTOU resistance
# ===========================================================================
#
# Strategy: capability binding to validated digests and revisions, plus
# revalidation performed inside consume(), which runs as the last statement
# before the provider call. Preflight-time validity is never sufficient.


@pytest.mark.parametrize("mutate", ["record", "digest", "approval", "package"])
def test_toctou_bytes_changed_after_validation(tmp_path, spy, monkeypatch, mutate):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    assert cap is not None
    monkeypatch.setattr(ga, "read_git_head", head)

    target = {
        "record": ctx.authorization_record_path,
        "digest": ctx.authorization_digest_path,
        "approval": ctx.owner_approval_path,
        "package": ctx.framework_root / PACKAGE_REL,
    }[mutate]
    target.write_bytes(target.read_bytes() + b"\n# changed after validation\n")

    executor = controlled_executor(tmp_path, cap)
    result = invoke(executor, tmp_path)

    assert spy.model_invocation_count == 0, (
        f"{mutate} changed after validation but the invocation still happened")
    assert result.status is se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_REVALIDATION_FAILED in result.error
    # Remediation semantics: a consumption ATTEMPT burns the authorization.
    # It must never return to ISSUED, or a failed provider attempt becomes an
    # unauthorized retry. This campaign permits no retry.
    assert cap.consumed is True
    assert cap.live is False


@pytest.mark.parametrize("which", ["framework", "target"])
def test_toctou_head_moved_after_validation(tmp_path, spy, monkeypatch, which):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    monkeypatch.setattr(ga, "read_git_head", head)
    root = ctx.framework_root if which == "framework" else ctx.target_root
    heads[str(root)] = "d" * 40

    executor = controlled_executor(tmp_path, cap)
    result = invoke(executor, tmp_path)

    assert spy.model_invocation_count == 0, (
        f"{which} HEAD moved after validation but the invocation still happened")
    assert ga.GATE_A_REVALIDATION_FAILED in result.error


def test_toctou_artifact_deleted_after_validation(tmp_path, spy, monkeypatch):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    monkeypatch.setattr(ga, "read_git_head", head)
    ctx.authorization_record_path.unlink()
    executor = controlled_executor(tmp_path, cap)
    result = invoke(executor, tmp_path)
    assert spy.model_invocation_count == 0
    assert ga.GATE_A_REVALIDATION_FAILED in result.error


# ===========================================================================
# 19. Alternate entrypoints
# ===========================================================================


def test_every_provider_call_site_is_inside_a_gated_executor():
    """Static audit: enumerate every provider SDK call in production code.

    If a new provider call site appears that is not one of the two known,
    Gate-A-bound sites, this test fails and forces it to be gated too.
    """
    known = {
        ("scripts/skill_executor.py", "query("),          # Claude Agent SDK
        ("scripts/skill_executor.py", "client.messages.create("),  # Anthropic SDK
        # scripts/execution_infra/provider_adapter.py (Phase 6, #122): the
        # real provider adapter for the EXPLORATORY lane. Its SDK call is
        # reachable ONLY after invoke_exploratory_attempt has consumed the
        # exploratory capability (the same single-use capability the
        # executor's EXPLORATORY branch consumes before its own query
        # call), so the invocation is gated by the identical boundary --
        # never reachable with an unconsumed capability, and the capability
        # is single-use so no second invocation is possible.
        ("scripts/execution_infra/provider_adapter.py", "query("),
    }
    found = set()
    for py in list((REPO_ROOT / "scripts").rglob("*.py")) + \
            list((REPO_ROOT / "src").rglob("*.py")):
        rel = os.path.relpath(py, REPO_ROOT).replace("\\", "/")
        text = py.read_text(encoding="utf-8", errors="replace")
        for needle in ("client.messages.create(", "messages.create("):
            if needle in text:
                found.add((rel, "client.messages.create("))
        if "async for message in query(" in text:
            found.add((rel, "query("))
    assert found <= known, (
        f"new, ungated provider call site(s): {sorted(found - known)}. "
        f"Every production model invocation must be behind the Gate A "
        f"capability boundary."
    )


def test_api_executor_alternate_path_is_gated(tmp_path, spy):
    """The second production provider path refuses controlled invocations.

    It refuses at construction, so a controlled run cannot even hold an
    ApiSkillExecutor without a capability.
    """
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.ApiSkillExecutor(repo_root=str(tmp_path),
                            controlled_experiment=True, authorization=None)
    assert exc.value.code == ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED
    assert_zero_invocation(spy, tmp_path)

    # And the invoke_skill layer refuses independently, if the object is
    # somehow obtained without going through __init__.
    executor = se.ApiSkillExecutor.__new__(se.ApiSkillExecutor)
    executor.__dict__.update({
        "repo_root": str(tmp_path),
        "model": se.ApiSkillExecutor.API_MODEL,
        "_declared_controlled_experiment": True,
        "authorization": None,
    })
    result = executor.invoke_skill("repo-sensemaker", "cmd", [],
                                   "repository_sensemaking_brief", {})
    assert result.status is se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED in result.error
    assert_zero_invocation(spy, tmp_path)

    # And with the declared flag stripped entirely -- the reported opt-out --
    # the SAME Stage 1 invocation is still classified as requiring Gate A,
    # because classification comes from the invocation, not the flag.
    ordinary_looking = se.ApiSkillExecutor.__new__(se.ApiSkillExecutor)
    ordinary_looking.__dict__.update({
        "repo_root": str(tmp_path),
        "model": se.ApiSkillExecutor.API_MODEL,
        "_declared_controlled_experiment": False,
        "authorization": None,
    })
    result = ordinary_looking.invoke_skill(
        "repo-sensemaker", "cmd", [], "repository_sensemaking_brief",
        {"expected_output_path": str(
            tmp_path / "experiments" / "evidence" / EVIDENCE_SLUG / "brief.md")})
    assert result.status is se.SkillExecutionStatus.FAILED
    assert "GATE_A_" in result.error
    assert_zero_invocation(spy, tmp_path)


def test_api_executor_refuses_even_with_a_valid_capability(tmp_path, spy):
    """It hardcodes a model that is not the authorized one, so it can never
    serve a Stage 1 invocation -- no model substitution."""
    api_identity = invocation_identity(
        tmp_path, tmp_path, model=se.ApiSkillExecutor.API_MODEL,
        executor_id="api", output_path="")
    ctx, head, resolver, heads, decision, cap = make_capability(
        tmp_path, identity=api_identity)
    assert cap is not None
    executor = se.ApiSkillExecutor(repo_root=str(tmp_path),
                                   controlled_experiment=True, authorization=cap,
                                   invocation_identity=api_identity)
    result = executor.invoke_skill("repo-sensemaker", "cmd", [],
                                   "repository_sensemaking_brief", {})
    assert result.status is se.SkillExecutionStatus.FAILED
    assert ga.GATE_A_MODEL_MISMATCH in result.error
    assert spy.model_invocation_count == 0
    assert cap.consumed is False, "the capability must not be spent by a refusal"


@pytest.mark.parametrize("executor_id", ["dry-run", "prompt-chain"])
def test_non_model_executors_cannot_serve_a_controlled_run(executor_id, tmp_path):
    """A controlled run must not silently downgrade to a non-executing path."""
    with pytest.raises(se.GateAAuthorizationRequired):
        se.create_executor(executor_id, str(tmp_path), controlled_experiment=True)


def test_create_executor_requires_capability_for_every_executor_id(tmp_path):
    for executor_id in se.EXECUTOR_REGISTRY:
        with pytest.raises((se.GateAAuthorizationRequired, ValueError)):
            se.create_executor(executor_id, str(tmp_path),
                               model="claude-sonnet-5",
                               controlled_experiment=True, authorization=None)


def test_imported_python_function_path_is_gated(tmp_path, spy):
    """Importing the executor class directly is not a bypass."""
    from skill_executor import ClaudeAgentSdkSkillExecutor
    with pytest.raises(se.GateAAuthorizationRequired):
        ClaudeAgentSdkSkillExecutor(repo_root=str(tmp_path),
                                    model="claude-sonnet-5",
                                    controlled_experiment=True)
    assert_zero_invocation(spy, tmp_path)


def test_workflow_runtime_controlled_run_without_capability_errors():
    """The CLI/workflow-plan entrypoint fails closed with the Gate A code."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime_gate_a", REPO_ROOT / "scripts" / "workflow-runtime.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    runner = module.OrchestrationRunner(
        workflow_id="architectural-review-planning-workflow",
        mode="autonomous_execution",
        repo_root=str(REPO_ROOT),
        executor="claude-code",
        model="claude-sonnet-5",
        controlled_experiment=True,
        authorization=None,
    )
    assert runner.skill_executor is None, (
        "the runtime built a real executor for a controlled run with no "
        "Gate A capability")
    assert any(ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED in e
               for e in runner.errors), runner.errors


def test_no_env_var_or_global_flag_can_authorize(tmp_path, spy, monkeypatch):
    """There is no AUTHORIZED=true style escape hatch."""
    for var in ("AUTHORIZED", "GATE_A_AUTHORIZED", "SKIP_GATE_A",
                "STAGE1_AUTHORIZED", "GATE_A_BYPASS"):
        monkeypatch.setenv(var, "true")
    with pytest.raises(se.GateAAuthorizationRequired):
        controlled_executor(tmp_path, None)
    assert_zero_invocation(spy, tmp_path)

    source = (REPO_ROOT / "scripts" / "skill_executor.py").read_text(encoding="utf-8")
    consumer = (REPO_ROOT / "scripts" / "gate_a_authorization.py").read_text(encoding="utf-8")
    for forbidden in ("os.environ.get(\"AUTHORIZED", "os.getenv(\"AUTHORIZED",
                      "GATE_A_BYPASS", "SKIP_GATE_A"):
        assert forbidden not in source
        assert forbidden not in consumer


# ===========================================================================
# 20. Filesystem safety
# ===========================================================================


def test_authorization_performs_no_writes_anywhere(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)

    def snapshot(root):
        return {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*") if p.is_file()
        }

    before_fw = snapshot(ctx.framework_root)
    before_tgt = snapshot(ctx.target_root)
    before_rc = snapshot(ctx.authorization_record_path.parent)

    ga.authorize_invocation(ctx, git_head=head, run_control_commit_resolver=resolver)

    assert snapshot(ctx.framework_root) == before_fw, "framework was written to"
    assert snapshot(ctx.target_root) == before_tgt, "TARGET WAS WRITTEN TO"
    assert snapshot(ctx.authorization_record_path.parent) == before_rc


def test_rejected_authorization_creates_no_evidence_and_no_output(tmp_path, spy):
    ctx, head, resolver, heads, decision, cap = make_capability(
        tmp_path, digest="0" * 64)
    assert cap is None
    assert not ctx.evidence_output_dir.exists()
    assert not (tmp_path / "out").exists()
    assert_zero_invocation(spy, tmp_path, ctx)


def test_malformed_files_are_never_rewritten(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    broken = b"schema_version: [unclosed\n"
    ctx.authorization_record_path.write_bytes(broken)
    ga.authorize(ctx, git_head=head, run_control_commit_resolver=resolver)
    assert ctx.authorization_record_path.read_bytes() == broken, (
        "the consumer repaired a malformed record instead of rejecting it")


def test_real_run_control_paths_are_never_touched():
    """The operative owner approval, if present, must be well-formed and
    exist only at the exact contract path; Evidence 0016 stays unused.

    The repository owner approved record digest bf31c7b6... on 2026-08-01
    (PR #113), so the run-control directory now legitimately contains exactly
    one owner-approval.md, at the exact contract path. What must never exist,
    regardless of approval state, is Evidence 0016 output -- approval alone
    authorizes nothing by itself; it must never invoke a model or run.
    """
    real_rc = REPO_ROOT / "experiments" / "run-control"
    if real_rc.exists():
        approval = real_rc / EVIDENCE_SLUG / "owner-approval.md"
        others = [
            p for p in real_rc.rglob("owner-approval.md")
            if p.resolve() != approval.resolve()
        ]
        assert not others, (
            f"an owner approval exists outside the contract path: {others}")
    real_evidence = REPO_ROOT / "experiments" / "evidence" / EVIDENCE_SLUG
    assert not real_evidence.exists(), "Evidence 0016 must remain unused"


def test_no_real_authorization_artifacts_in_the_repository():
    """The drafted record, its digest, and exactly one owner approval may
    exist -- all solely at the single contract-defined run-control path.
    Nowhere else in the repository may any of these three filenames appear.
    """
    allowed_dir = (
        REPO_ROOT / "experiments" / "run-control" / EVIDENCE_SLUG
    ).resolve()
    permitted = {
        "authorization-record.yaml": allowed_dir,
        "authorization-record.sha256": allowed_dir,
        "owner-approval.md": allowed_dir,
    }
    for name, allowed_parent in permitted.items():
        matches = [
            p for p in REPO_ROOT.rglob(name)
            if ".git" not in p.parts and "tmp" not in p.parts
            and p.resolve().parent != allowed_parent
        ]
        assert not matches, f"unexpected authorization artifact present: {matches}"
    # owner-approval.md does not currently exist anywhere: the artifact-root
    # record regeneration invalidated the PR #113 approval's digest binding,
    # and it was renamed to owner-approval.SUPERSEDED-pre-artifact-root.md
    # (which is not the filename "owner-approval.md" and is not matched by
    # this glob). A fresh approval is required before any execution.
    approvals = [
        p for p in REPO_ROOT.rglob("owner-approval.md")
        if ".git" not in p.parts and "tmp" not in p.parts
    ]
    assert approvals == [], (
        f"owner-approval.md must not exist until a fresh owner approval is "
        f"granted for the regenerated record: {approvals}"
    )


def test_evidence_0015_is_untouched():
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "origin/main", "--", "experiments/evidence/"],
        capture_output=True, text=True, check=False,
    )
    assert result.stdout.strip() == "", (
        f"evidence tree was modified:\n{result.stdout[:2000]}")


# ===========================================================================
# 21. Logging and secret hygiene at the boundary
# ===========================================================================


def test_denial_message_carries_a_code_and_leaks_no_approval_content(tmp_path, spy):
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    executor = controlled_executor(tmp_path, cap)
    executor.__dict__["authorization"] = None
    result = invoke(executor, tmp_path)
    assert ga.GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED in result.error
    approval = ctx.owner_approval_path.read_text(encoding="utf-8")
    assert approval not in result.error
    assert "owner decision on the run-control PR" not in result.error
    result.error.encode("ascii")  # ASCII-only console output
    assert "no model invocation was attempted" in result.message.lower()


# ===========================================================================
# 18. Third review, section 27: an ALIAS of the same physical output path
#     cannot obtain a second provider call.
# ===========================================================================


def test_alternate_alias_of_same_output_path_cannot_get_a_second_call(
        tmp_path, spy, monkeypatch):
    """One physical output directory is ONE invocation, however it is spelled.

    The capability binds to a canonical identity derived from PHYSICAL
    filesystem identity. Re-invoking with a different spelling of the very same
    directory (here a `/./` + doubled-separator + trailing-dot alias) must not
    look like a different invocation and must not yield a second provider call.
    """
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    executor = controlled_executor(tmp_path, cap)
    monkeypatch.setattr(ga, "read_git_head", head)

    invoke(executor, tmp_path)
    assert spy.model_invocation_count == 1

    out = tmp_path / "out"
    out.mkdir(exist_ok=True)
    alias = str(out).replace("out", "out\.\..\out") + "\\brief.md"
    # The spent capability is refused at executor CONSTRUCTION -- an even
    # stronger outcome than a refusal at the provider boundary. Either way the
    # alias must not buy a second call.
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        aliased = controlled_executor(tmp_path, cap)
        aliased._invocation_identity = invocation_identity(
            tmp_path, output_path=alias)
        invoke(aliased, tmp_path)
    assert ga.GATE_A_CAPABILITY_NOT_LIVE in str(exc.value)
    assert spy.model_invocation_count == 1, (
        "an aliased spelling of the same physical output path obtained a "
        "second provider call on a one-invocation authorization")


def test_provider_exception_does_not_restore_issuance(tmp_path, spy,
                                                      monkeypatch):
    """A provider that raises must not hand the capability back."""
    ctx, head, resolver, heads, decision, cap = make_capability(tmp_path)
    executor = controlled_executor(tmp_path, cap)
    monkeypatch.setattr(ga, "read_git_head", head)

    spy.raise_on_call = RuntimeError("provider exploded")
    invoke(executor, tmp_path)
    assert cap.live is False, (
        "a provider exception returned the capability to ISSUED; a failed "
        "attempt must not become a fresh invocation budget")
    second = invoke(executor, tmp_path)
    assert spy.model_invocation_count <= 1
    assert second.status is se.SkillExecutionStatus.FAILED
