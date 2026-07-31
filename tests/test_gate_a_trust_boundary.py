"""Gate A trust-boundary regression proofs (issue #108 independent review).

An independent adversarial review of PR #109 REPRODUCED three authorization
bypasses against the first design:

1. ``controlled_experiment`` was a caller-controlled opt-out defaulting to
   ``False``. Omitting one CLI flag reached the provider with no authorization
   at all; constructing a gated executor and then assigning
   ``.controlled_experiment = False`` reached the provider with the capability
   left unconsumed and reusable.
2. ``AuthorizedInvocation`` could be duplicated by ``copy.copy``,
   ``copy.deepcopy``, and a pickle round-trip. One authorization produced nine
   successful consumptions in the reproduction.
3. ``consume()`` was check-then-set with no lock. Eight threads racing one
   single-use capability produced eight successes.

This module is the regression suite for the redesign. Every test here fails on
the pre-remediation head. Nothing here invokes a model, writes a real
authorization artifact, or touches ``experiments/``.

Design under test
-----------------
- Gate A requirement is DERIVED from an immutable ``InvocationIdentity``, not
  read from a mutable boolean.
- The capability object is a handle; authorization lives in a process-local
  issuer registry keyed by a random capability ID.
- Consumption is an atomic ISSUED -> CONSUMING -> CONSUMED transition taken
  under a lock BEFORE expensive revalidation.
- Any consumption attempt burns the issuance. There is no retry.
"""

from __future__ import annotations

import copy
import pickle
import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402
import skill_executor as se  # noqa: E402
import gate_a_fixtures as F  # noqa: E402


ARTIFACT = F.ARTIFACT_TYPE
MODEL = F.EXACT_MODEL


def mint(tmp_path, **kwargs):
    decision, cap, ctx, git_head, identity = F.mint_capability(
        tmp_path, repo_root=tmp_path / "framework", **kwargs)
    assert cap is not None, f"fixture failed to issue: {decision.failure_code}"
    return decision, cap, ctx, git_head, identity


# ===========================================================================
# A. Classification: the security decision is derived, not declared
# ===========================================================================


def test_controlled_stage1_is_recognized_without_any_declared_flag():
    """Bypass 1, root cause. The flag is gone from the decision entirely."""
    identity = se.build_invocation_identity(
        repo_root="/repo",
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path":
                 f"/repo/experiments/evidence/{F.EVIDENCE_SLUG}/brief.md"},
        model=MODEL,
        declared_controlled_mode=None,  # the flag was never passed
    )
    mode, signals = ga.classify_invocation(identity)
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1
    assert ga.requires_gate_a(mode) is True
    assert "output_in_controlled_evidence_namespace" in signals


@pytest.mark.parametrize("declared", [False, None, 0, ""])
def test_falsy_declared_mode_cannot_downgrade_controlled_stage1(declared):
    """Omitted / False / None / falsy-string all still require Gate A."""
    identity = se.build_invocation_identity(
        repo_root="/repo",
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={
            "expected_output_path":
                f"/repo/experiments/evidence/{F.EVIDENCE_SLUG}/brief.md",
            "evidence_number": F.EVIDENCE_NUMBER,
            "evidence_slug": F.EVIDENCE_SLUG,
        },
        model=MODEL,
        declared_controlled_mode=(declared or None),
    )
    mode, _ = ga.classify_invocation(identity)
    assert ga.requires_gate_a(mode) is True


def test_declared_false_conflicting_with_structure_is_ambiguous_not_ordinary():
    """Never allow `False` to override structural controlled-Stage-1 signals."""
    identity = ga.InvocationIdentity.build(
        workflow_id="stage-1", workflow_stage="stage-1",
        artifact_type="something_else",
        output_path="/repo/artifacts/x.md",
        target_repository=ga.CONTRACT_TARGET_REPOSITORY,
        requested_model=MODEL,
        executor_id="claude-code",
        declared_controlled_mode=False,
    )
    mode, signals = ga.classify_invocation(identity)
    assert mode is ga.ExecutionMode.AMBIGUOUS
    assert "declared_mode_conflict" in signals
    assert ga.requires_gate_a(mode) is True


def test_missing_identity_is_ambiguous_and_gated():
    mode, signals = ga.classify_invocation(None)
    assert mode is ga.ExecutionMode.AMBIGUOUS
    assert signals == ("identity_missing",)
    assert ga.requires_gate_a(mode) is True


@pytest.mark.parametrize("output", [
    "/repo/experiments/evidence/0016-stage1-auteur-post-remediation-controlled-attempt/brief.md",
    "/repo/experiments/evidence/0099-some-other-campaign/brief.md",
    "/repo/experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/x.md",
])
def test_any_evidence_namespace_output_is_gated(output):
    """Fail closed: an evidence namespace is a controlled namespace."""
    identity = ga.InvocationIdentity.build(
        artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
        workflow_stage="stage-1", output_path=output,
        executor_id="claude-code")
    mode, _ = ga.classify_invocation(identity)
    assert ga.requires_gate_a(mode) is True


def test_evidence_identity_is_parsed_from_the_output_path():
    """A caller that omits the evidence fields does not thereby escape."""
    identity = se.build_invocation_identity(
        repo_root="/repo", executor_id="claude-code", skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path":
                 f"/repo/experiments/evidence/{F.EVIDENCE_SLUG}/brief.md"},
        model=MODEL)
    assert identity.evidence_number == "0016"
    assert identity.evidence_slug == F.EVIDENCE_SLUG


# ---- the honest ordinary-development boundary -----------------------------


@pytest.mark.parametrize("identity_kwargs", [
    # non-Stage-1 skill
    dict(skill_id="workflow-planner", artifact_type="workflow_orchestration_plan",
         output="/repo/artifacts/plan.md", model="claude-haiku-4-5"),
    # Stage 1 skill, non-evidence output, non-campaign target/model
    dict(skill_id="repo-sensemaker", artifact_type="repository_sensemaking_brief",
         output="/repo/artifacts/brief.md", model="claude-haiku-4-5"),
    # non-controlled artifact type
    dict(skill_id="problem-framer", artifact_type="problem_frame",
         output="/repo/artifacts/frame.md", model="claude-haiku-4-5"),
])
def test_genuinely_ordinary_development_stays_ungated(identity_kwargs):
    """Positive proof that this redesign did not gate normal local work."""
    identity = se.build_invocation_identity(
        repo_root="/repo", executor_id="claude-code",
        skill_id=identity_kwargs["skill_id"],
        expected_output_artifact=identity_kwargs["artifact_type"],
        context={"expected_output_path": identity_kwargs["output"]},
        model=identity_kwargs["model"])
    mode, signals = ga.classify_invocation(identity)
    assert mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT, signals
    assert ga.requires_gate_a(mode) is False
    # and it needs no capability
    assert se.require_authorization_capability(
        None, identity=identity, model=identity_kwargs["model"],
        executor_name="test") is ga.ExecutionMode.ORDINARY_DEVELOPMENT


def test_relabelling_controlled_stage1_as_ordinary_does_not_work():
    """Negative twin of the test above."""
    identity = se.build_invocation_identity(
        repo_root="/repo", executor_id="claude-code", skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path":
                 f"/repo/experiments/evidence/{F.EVIDENCE_SLUG}/brief.md"},
        model=MODEL, declared_controlled_mode=None)
    with pytest.raises(se.GateAAuthorizationRequired):
        se.require_authorization_capability(
            None, identity=identity, model=MODEL, executor_name="test")


# ===========================================================================
# B. Post-construction mutation attacks (the exact reported bypass)
# ===========================================================================


def _executor(tmp_path, cap, identity, repo_root):
    cls = se.ClaudeAgentSdkSkillExecutor
    orig = cls._check_dependencies
    cls._check_dependencies = lambda self: (True, [])
    try:
        return cls(repo_root=str(repo_root), model=MODEL,
                   controlled_experiment=True, authorization=cap,
                   invocation_identity=identity)
    finally:
        cls._check_dependencies = orig


@pytest.mark.parametrize("attr,value", [
    ("controlled_experiment", False),
    ("_declared_controlled_experiment", False),
    ("authorization", None),
    ("model", "claude-haiku-4-5"),
    ("_invocation_identity", None),
    ("repo_root", "/elsewhere"),
])
def test_security_relevant_attributes_reject_reassignment(tmp_path, attr, value):
    _, cap, ctx, head, identity = mint(tmp_path)
    ex = _executor(tmp_path, cap, identity, tmp_path / "framework")
    with pytest.raises(AttributeError):
        setattr(ex, attr, value)


def test_post_construction_downgrade_does_not_change_classification(tmp_path):
    """The reported bypass, end to end, including a raw __dict__ poke.

    Even after every mode-related attribute is overwritten by writing straight
    into __dict__ (bypassing __setattr__), the invocation is still classified
    as controlled, because classification is re-derived from the call.
    """
    _, cap, ctx, head, identity = mint(tmp_path)
    fw = tmp_path / "framework"
    ex = _executor(tmp_path, cap, identity, fw)

    ex.__dict__["_declared_controlled_experiment"] = False
    ex.__dict__["_invocation_identity"] = F.ordinary_identity(fw)

    actual = ex._actual_identity(
        "repo-sensemaker",
        F.controlled_output_path(fw),
        F.controlled_context(ctx.target_root))
    mode, signals = ga.classify_invocation(actual)
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, signals
    assert ga.requires_gate_a(mode) is True
    assert cap.live is True, "no capability was spent by a mutation attempt"


def test_controlled_experiment_has_no_setter(tmp_path):
    """It is informational metadata now, not an authorization switch."""
    _, cap, ctx, head, identity = mint(tmp_path)
    ex = _executor(tmp_path, cap, identity, tmp_path / "framework")
    assert ex.controlled_experiment is True
    with pytest.raises(AttributeError):
        ex.controlled_experiment = False
    assert ex.controlled_experiment is True


# ===========================================================================
# C. Cloning and forgery (bypass 2)
# ===========================================================================


def test_shallow_copy_is_refused(tmp_path):
    _, cap, *_ = mint(tmp_path)
    with pytest.raises(TypeError, match="COPY_PROHIBITED"):
        copy.copy(cap)


def test_deep_copy_is_refused(tmp_path):
    _, cap, *_ = mint(tmp_path)
    with pytest.raises(TypeError, match="COPY_PROHIBITED"):
        copy.deepcopy(cap)


@pytest.mark.parametrize("protocol", list(range(pickle.HIGHEST_PROTOCOL + 1)))
def test_every_pickle_protocol_is_refused(tmp_path, protocol):
    _, cap, *_ = mint(tmp_path)
    with pytest.raises(TypeError, match="SERIALIZATION_PROHIBITED"):
        pickle.dumps(cap, protocol)


def test_optional_third_party_serializers_are_refused(tmp_path):
    _, cap, *_ = mint(tmp_path)
    refused = 0
    for name in ("cloudpickle", "dill"):
        try:
            mod = __import__(name)
        except ImportError:
            continue
        with pytest.raises(TypeError):
            mod.dumps(cap)
        refused += 1
    if refused == 0:
        pytest.skip("neither cloudpickle nor dill is installed")


def test_getstate_and_setstate_are_refused(tmp_path):
    _, cap, *_ = mint(tmp_path)
    with pytest.raises(TypeError):
        cap.__getstate__()
    with pytest.raises(TypeError):
        cap.__setstate__({})


def test_subclassing_is_refused():
    with pytest.raises(TypeError, match="COPY_PROHIBITED"):
        type("Evil", (ga.AuthorizedInvocation,), {})


def test_capability_is_immutable(tmp_path):
    _, cap, *_ = mint(tmp_path)
    with pytest.raises(AttributeError, match="IMMUTABLE"):
        cap._capability_id = "z" * 64
    with pytest.raises(AttributeError, match="IMMUTABLE"):
        del cap._capability_id
    with pytest.raises(AttributeError):
        cap.brand_new_attribute = 1  # __slots__


def test_forged_capability_id_is_not_live(tmp_path):
    """Python privacy is not the claim. Registry membership is."""
    forged = object.__new__(ga.AuthorizedInvocation)
    object.__setattr__(forged, "_capability_id", "f" * 64)
    assert forged.live is False
    with pytest.raises(ga.GateAError, match="NOT_LIVE"):
        forged.consume(model=MODEL, artifact_type=ARTIFACT)


def test_reconstructed_object_with_a_real_id_shares_one_issuance(tmp_path):
    """Bypass 2, the strong form: even a perfect reflection-built duplicate
    cannot produce a second authorization, because both objects point at the
    SAME single registry entry."""
    _, cap, ctx, head, identity = mint(tmp_path)
    dup = object.__new__(ga.AuthorizedInvocation)
    object.__setattr__(dup, "_capability_id", cap.capability_id)

    successes = 0
    for obj in (dup, cap):
        try:
            obj.consume(model=MODEL, artifact_type=ARTIFACT,
                        git_head=head, actual_identity=identity)
            successes += 1
        except ga.GateAError:
            pass
    assert successes == 1, "one authorization must yield one consumption"
    assert cap.live is False
    assert dup.live is False


def test_duplicate_across_executor_instances_yields_one_consumption(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)
    dup = object.__new__(ga.AuthorizedInvocation)
    object.__setattr__(dup, "_capability_id", cap.capability_id)
    fw = tmp_path / "framework"
    ex_a = _executor(tmp_path, cap, identity, fw)
    ex_b = _executor(tmp_path, dup, identity, fw)
    successes = 0
    for ex in (ex_a, ex_b):
        try:
            ex.authorization.consume(model=MODEL, artifact_type=ARTIFACT,
                                     git_head=head, actual_identity=identity)
            successes += 1
        except ga.GateAError:
            pass
    assert successes == 1


# ===========================================================================
# D. Identity binding
# ===========================================================================


def test_consuming_for_a_different_invocation_is_refused(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)
    fw = tmp_path / "framework"
    other = F.controlled_identity(
        fw, target_root=ctx.target_root,
        output_path=f"{fw}/experiments/evidence/{F.EVIDENCE_SLUG}/other.md")
    with pytest.raises(ga.GateAError, match="INVOCATION_IDENTITY_MISMATCH"):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=other)
    assert cap.live is False, "the mismatched attempt still burns the issuance"


def test_identity_digest_ignores_the_informational_flag():
    """Two identities differing only in declared mode are the same invocation."""
    base = dict(workflow_id="w", workflow_stage="stage-1",
                artifact_type=ARTIFACT, output_path="/o", executor_id="claude-code")
    a = ga.InvocationIdentity.build(declared_controlled_mode=True, **base)
    b = ga.InvocationIdentity.build(declared_controlled_mode=False, **base)
    assert a.digest() == b.digest()


def test_identity_is_frozen():
    identity = ga.InvocationIdentity.build(artifact_type=ARTIFACT)
    with pytest.raises(Exception):
        identity.artifact_type = "something_else"


# ===========================================================================
# E. Atomic concurrency (bypass 3)
# ===========================================================================


def _race(cap, head, identity, n_threads, objects=None):
    """Deterministic race: every thread blocks on a barrier inside consume(),
    after the atomic transition point, so the window is real and not timing
    luck. No sleeps."""
    barrier = threading.Barrier(n_threads)
    provider_calls = []
    successes = []
    failures = []
    lock = threading.Lock()
    objs = objects or [cap] * n_threads

    def hook():
        # Runs inside consume(), immediately AFTER the ISSUED->CONSUMING
        # transition. If the transition were not atomic, every thread would be
        # sitting here having passed the check.
        try:
            barrier.wait(timeout=5)
        except threading.BrokenBarrierError:
            pass

    def worker(obj):
        try:
            obj.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                        actual_identity=identity, _before_revalidation=hook)
            with lock:
                provider_calls.append(1)
                successes.append(1)
        except BaseException as exc:  # noqa: BLE001
            with lock:
                failures.append(str(exc).split(":")[0])

    threads = [threading.Thread(target=worker, args=(o,)) for o in objs]
    for t in threads:
        t.start()
    # the loser threads never reach the barrier, so release the winner
    barrier.abort()
    for t in threads:
        t.join(timeout=10)
    return successes, failures, provider_calls


@pytest.mark.parametrize("n_threads", [2, 8])
def test_concurrent_consumption_permits_exactly_one(tmp_path, n_threads):
    """The exact reported 8-thread scenario, plus the 2-thread minimum."""
    _, cap, ctx, head, identity = mint(tmp_path)
    successes, failures, provider_calls = _race(cap, head, identity, n_threads)
    assert len(successes) == 1, (
        f"{len(successes)} threads consumed one single-use authorization")
    assert len(provider_calls) <= 1
    assert len(failures) == n_threads - 1
    assert set(failures) <= {ga.GATE_A_CAPABILITY_CONCURRENT_CONSUMPTION,
                             ga.GATE_A_CAPABILITY_ALREADY_CONSUMED,
                             ga.GATE_A_CAPABILITY_CONSUMPTION_FAILED}
    assert cap.live is False


def test_concurrent_consumption_with_forged_duplicates(tmp_path):
    """Duplicates racing the original still total exactly one consumption."""
    _, cap, ctx, head, identity = mint(tmp_path)
    objs = [cap, cap]
    for _ in range(6):
        dup = object.__new__(ga.AuthorizedInvocation)
        object.__setattr__(dup, "_capability_id", cap.capability_id)
        objs.append(dup)
    successes, failures, provider_calls = _race(cap, head, identity, 8, objects=objs)
    assert len(successes) == 1
    assert len(provider_calls) <= 1
    assert cap.live is False


def test_losing_callers_fail_deterministically(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)
    successes, failures, _ = _race(cap, head, identity, 8)
    assert all(code.startswith("GATE_A_") for code in failures), failures


def test_sequential_second_consumption_is_refused(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)
    cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                actual_identity=identity)
    with pytest.raises(ga.GateAError, match="ALREADY_CONSUMED"):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)


# ===========================================================================
# F. Burn semantics: failure, cancellation, provider error
# ===========================================================================


def test_revalidation_failure_burns_the_capability(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)
    ctx.authorization_record_path.write_bytes(b"tampered\n")
    with pytest.raises(ga.GateAError, match="REVALIDATION_FAILED"):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)
    assert cap.live is False
    with pytest.raises(ga.GateAError, match="CONSUMPTION_FAILED"):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)


def test_cancellation_during_revalidation_burns_the_capability(tmp_path):
    """A cancelled consumption must never become an unauthorized retry."""
    _, cap, ctx, head, identity = mint(tmp_path)

    class _Cancelled(BaseException):
        pass

    def cancel():
        raise _Cancelled("task cancelled mid-consumption")

    with pytest.raises(_Cancelled):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity, _before_revalidation=cancel)
    assert cap.live is False
    with pytest.raises(ga.GateAError, match="CONSUMPTION_FAILED"):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)


def test_keyboard_interrupt_during_revalidation_burns_the_capability(tmp_path):
    _, cap, ctx, head, identity = mint(tmp_path)

    def boom(_root):
        raise KeyboardInterrupt("interrupted")

    with pytest.raises(KeyboardInterrupt):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=boom,
                    actual_identity=identity)
    assert cap.live is False


def test_a_provider_error_after_consumption_does_not_restore_the_capability(tmp_path):
    """Consumption completes BEFORE the provider call, on purpose: a provider
    failure must not hand back a reusable authorization."""
    _, cap, ctx, head, identity = mint(tmp_path)
    cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                actual_identity=identity)
    try:
        raise RuntimeError("provider exploded")
    except RuntimeError:
        pass
    assert cap.live is False
    with pytest.raises(ga.GateAError):
        cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)


# ===========================================================================
# G. Registry invariants
# ===========================================================================


def test_capability_ids_are_random_and_unique(tmp_path):
    ids = set()
    for i in range(5):
        _, cap, *_ = mint(tmp_path / f"case{i}")
        assert len(cap.capability_id) == 64
        int(cap.capability_id, 16)  # hex
        ids.add(cap.capability_id)
    assert len(ids) == 5


def test_failed_gate_a_issues_nothing(tmp_path):
    before = ga._REGISTRY.live_count()
    ctx, head, resolver, _ = F.build_valid_case(tmp_path, digest="0" * 64)
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver)
    assert decision.authorized is False
    assert cap is None
    assert ga._REGISTRY.live_count() == before


def test_all_new_failure_codes_are_registered():
    for code in (
        "GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS",
        "GATE_A_INVOCATION_IDENTITY_MISMATCH",
        "GATE_A_CAPABILITY_COPY_PROHIBITED",
        "GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED",
        "GATE_A_CAPABILITY_NOT_LIVE",
        "GATE_A_CAPABILITY_CONCURRENT_CONSUMPTION",
        "GATE_A_CAPABILITY_CONSUMPTION_FAILED",
        "GATE_A_CAPABILITY_IMMUTABLE",
    ):
        assert code in ga.ALL_FAILURE_CODES
        assert getattr(ga, code) == code


def test_preflight_rejects_a_spent_capability_before_any_consumption(tmp_path):
    """The NON-CONSUMING preflight must reject a retired issuance on its own.

    This targets `require_authorization_capability`'s registry liveness check
    specifically. Asserting the exact GATE_A_CAPABILITY_NOT_LIVE code matters:
    if the preflight check is deleted, consume() would still refuse, but with a
    different code and only after prompt construction -- so a test that accepts
    either code would not notice the check disappearing.
    """
    _, cap, ctx, head, identity = mint(tmp_path)
    cap.consume(model=MODEL, artifact_type=ARTIFACT, git_head=head,
                actual_identity=identity)
    assert cap.live is False

    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.require_authorization_capability(
            cap, identity=identity, model=MODEL, executor_name="preflight-test")
    assert exc.value.code == ga.GATE_A_CAPABILITY_NOT_LIVE


def test_preflight_rejects_a_forged_capability_before_any_consumption(tmp_path):
    """Same check, forged-ID form: never issued means never live."""
    _, cap, ctx, head, identity = mint(tmp_path)
    forged = object.__new__(ga.AuthorizedInvocation)
    object.__setattr__(forged, "_capability_id", "a" * 64)
    with pytest.raises(se.GateAAuthorizationRequired) as exc:
        se.require_authorization_capability(
            forged, identity=identity, model=MODEL, executor_name="preflight-test")
    assert exc.value.code == ga.GATE_A_CAPABILITY_NOT_LIVE


def test_denials_never_leak_the_capability_id(tmp_path):
    """The ID is an opaque handle; it must not appear in operator-facing text."""
    _, cap, ctx, head, identity = mint(tmp_path)
    try:
        cap.consume(model="wrong-model", artifact_type=ARTIFACT, git_head=head,
                    actual_identity=identity)
    except ga.GateAError as exc:
        assert cap.capability_id not in str(exc)
        str(exc).encode("ascii")
    else:  # pragma: no cover
        pytest.fail("wrong model was accepted")
