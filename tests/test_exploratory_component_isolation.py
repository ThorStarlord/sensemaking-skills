"""Phase 3 (#119): canonical-path import isolation for ``skill_executor``.

The established minimal Gate A environment installs pytest, pyyaml, click
and the Claude SDK -- but deliberately NOT the Phase 2/3 package or its
declared dependencies (rfc8785, jsonschema). Phase 3 originally imported
``sensemaking_skills.exploratory_authorization`` eagerly at module load,
which broke every canonical executor import there (ModuleNotFoundError:
rfc8785, observed in CI run 30867804098 on PR #126).

These tests pin the corrected architecture:

* ``skill_executor`` imports successfully when rfc8785 is unavailable.
* The ORDINARY and CANONICAL paths never import the exploratory package or
  its dependencies (proven by ``sys.modules`` inspection in a fresh
  interpreter).
* A canonical denial still produces the existing canonical Gate A code,
  never an import error.
* An actual EXPLORATORY invocation loads the exploratory module normally in
  the complete package environment.
* An EXPLORATORY invocation with the component unavailable fails closed
  with exactly one stable code
  (``EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE``) and zero provider
  calls -- never a downgrade to ORDINARY/CANONICAL, never a raw
  ModuleNotFoundError as the authorization result.
* No caller-controlled lane declaration can downgrade an identity that is
  structurally exploratory, and mixed canonical/exploratory evidence stays
  AMBIGUOUS on the existing fail-closed canonical path.

Everything runs in SUBPROCESSES with ``rfc8785`` deliberately unavailable
(simulated by poisoning ``sys.modules`` in a fresh interpreter), so the
tests never depend on deleting modules from the main pytest interpreter.
The existing positive exploratory test-double, reuse, field-drift, expiry
and concurrency suites (test_exploratory_provider_boundary.py,
test_exploratory_capability_lifecycle.py) are unchanged and remain the
proof of exactly-once invocation for the real executor path.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
SRC = REPO_ROOT / "src"

EXPLORATORY_COMPONENT_UNAVAILABLE = "EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE"

#: True only when the subprocess interpreter (this interpreter) can actually
#: load the exploratory package -- i.e. we are NOT inside the minimal Gate A
#: environment. The complete-environment test needs rfc8785 importable in
#: the subprocess, which inherits this interpreter.
_HAVE_RFC8785 = importlib.util.find_spec("rfc8785") is not None

_FORBIDDEN_MODULES = (
    "sensemaking_skills.exploratory_authorization",
    "sensemaking_skills.campaign_validation",
    "rfc8785",
)

_FRAMEWORK = "C:/phase3-tests/example-repo"

_MINIMAL_SETUP = f"""\
import sys
sys.modules["rfc8785"] = None
sys.path.insert(0, {str(SCRIPTS)!r})
import gate_a_authorization as ga
import skill_executor as se
"""

_COMPLETE_SETUP = f"""\
import sys
sys.path.insert(0, {str(SCRIPTS)!r})
sys.path.insert(0, {str(SRC)!r})
import gate_a_authorization as ga
import skill_executor as se
"""


def _identity_snippet(output_path: str, *, controlled: bool = False) -> str:
    controlled_kw = (
        "\n    declared_controlled_mode=True," if controlled else ""
    )
    return f"""\
identity = ga.InvocationIdentity.build(
    workflow_id="phase3-test-workflow",
    workflow_stage="stage-3",
    artifact_type="attempt_result",
    output_path=r"{output_path}",
    framework_root=r"{_FRAMEWORK}",
    target_repository="https://example.invalid/example-owner/example-target.git",
    target_sha="000000000000000000000000000000000000beef",
    requested_model="example-model-identifier",
    executor_id="test-executor",{controlled_kw}
)
"""


_ORDINARY_IDENTITY = _identity_snippet(f"{_FRAMEWORK}/artifacts/brief.md")
_CAMPAIGN_IDENTITY = _identity_snippet(
    f"{_FRAMEWORK}/experiments/campaigns/EXP-0001-alpha/attempts/attempt-1.md")
_CONTROLLED_CAMPAIGN_IDENTITY = _identity_snippet(
    f"{_FRAMEWORK}/experiments/campaigns/EXP-0001-alpha/attempts/attempt-1.md",
    controlled=True)
_EVIDENCE_IDENTITY = _identity_snippet(
    f"{_FRAMEWORK}/experiments/evidence/0016-sensemaking/summary.md")

_DECLARED = """\
declared = ga.DeclaredExploratory(
    campaign_id="EXP-0001-alpha",
    classification="EXPLORATORY_NOT_CANONICAL_EVIDENCE",
    attempt_id="a1b2c3d4-e5f6-4789-8abc-def012345678",
    configuration_id="1" * 64,
)
"""

_FORBIDDEN_CHECK = f"""\
forbidden_present = [
    m for m in {_FORBIDDEN_MODULES!r}
    if sys.modules.get(m) is not None
]
"""


def _run(code: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, timeout=120,
        cwd=str(REPO_ROOT), env=env,
    )


def _assert_ok(result: subprocess.CompletedProcess, sentinel: str):
    assert result.returncode == 0, result.stdout + result.stderr
    assert sentinel in result.stdout, result.stdout + result.stderr


def test_skill_executor_imports_successfully_without_rfc8785():
    code = _MINIMAL_SETUP + _FORBIDDEN_CHECK + """\
assert not forbidden_present, forbidden_present
print("IMPORT_OK")
"""
    _assert_ok(_run(code), "IMPORT_OK")


def test_ordinary_path_imports_no_exploratory_dependencies():
    code = _MINIMAL_SETUP + _ORDINARY_IDENTITY + _FORBIDDEN_CHECK + """\
lane, mode = se.require_invocation_authorization(
    None, None, identity=identity, model="example-model-identifier",
    executor_name="isolation-test")
assert lane == se.LANE_ORDINARY, lane
assert mode is se.ExecutionMode.ORDINARY_DEVELOPMENT, mode
assert not forbidden_present, forbidden_present
print("ORDINARY_OK")
"""
    _assert_ok(_run(code), "ORDINARY_OK")


def test_canonical_path_imports_no_exploratory_dependencies():
    code = _MINIMAL_SETUP + _CONTROLLED_CAMPAIGN_IDENTITY + _DECLARED + _FORBIDDEN_CHECK + """\
try:
    se.require_invocation_authorization(
        None, None, identity=identity, model="example-model-identifier",
        executor_name="isolation-test", declared=declared)
    raise AssertionError("expected a canonical Gate A denial")
except se.GateAAuthorizationRequired as exc:
    assert exc.code.startswith("GATE_A_"), exc.code
assert not forbidden_present, forbidden_present
print("CANONICAL_OK")
"""
    _assert_ok(_run(code), "CANONICAL_OK")


def test_canonical_denial_uses_existing_gate_a_code_not_import_error():
    code = _MINIMAL_SETUP + _CONTROLLED_CAMPAIGN_IDENTITY + _DECLARED + f"""\
try:
    se.require_invocation_authorization(
        None, None, identity=identity, model="example-model-identifier",
        executor_name="isolation-test", declared=declared)
    raise AssertionError("expected a canonical Gate A denial")
except se.ExploratoryAuthorizationRequired:
    raise AssertionError("the exploratory class must not be raised for a canonical lane")
except se.GateAAuthorizationRequired as exc:
    assert exc.code.startswith("GATE_A_"), exc.code
    assert exc.code != {EXPLORATORY_COMPONENT_UNAVAILABLE!r}, exc.code
print("CANONICAL_DENIAL_OK")
"""
    _assert_ok(_run(code), "CANONICAL_DENIAL_OK")


@pytest.mark.skipif(
    not _HAVE_RFC8785,
    reason="requires the complete package environment (rfc8785 importable)",
)
def test_exploratory_path_loads_module_in_complete_environment():
    code = _COMPLETE_SETUP + _CAMPAIGN_IDENTITY + _DECLARED + """\
try:
    se.require_invocation_authorization(
        None, None, identity=identity, model="example-model-identifier",
        executor_name="isolation-test", declared=declared)
    raise AssertionError("expected EXPLORATORY_CAPABILITY_REQUIRED")
except se.ExploratoryAuthorizationRequired as exc:
    assert exc.code == "EXPLORATORY_CAPABILITY_REQUIRED", exc.code
assert "sensemaking_skills.exploratory_authorization" in sys.modules
print("COMPLETE_ENV_OK")
"""
    _assert_ok(_run(code), "COMPLETE_ENV_OK")


def test_exploratory_component_unavailable_fails_closed_with_exact_code():
    code = _MINIMAL_SETUP + _CAMPAIGN_IDENTITY + _DECLARED + _FORBIDDEN_CHECK + f"""\
try:
    se.require_invocation_authorization(
        None, None, identity=identity, model="example-model-identifier",
        executor_name="isolation-test", declared=declared)
    raise AssertionError("expected EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE")
except se.ExploratoryAuthorizationRequired as exc:
    assert exc.code == {EXPLORATORY_COMPONENT_UNAVAILABLE!r}, exc.code
except ImportError as exc:
    raise AssertionError("a raw ImportError escaped as the authorization result") from exc
assert not forbidden_present, forbidden_present
print("FAIL_CLOSED_OK")
"""
    _assert_ok(_run(code), "FAIL_CLOSED_OK")


def test_executor_level_exploratory_invocation_fails_closed_zero_provider_calls():
    repo_root = str(REPO_ROOT).replace("\\", "/")
    campaign_path = (
        f"{repo_root}/experiments/campaigns/EXP-0001-alpha/attempts/attempt-1.md")
    code = _MINIMAL_SETUP + f"""\
se.query = lambda *a, **k: (_ for _ in ()).throw(AssertionError("PROVIDER_CALLED"))
executor = se.ClaudeAgentSdkSkillExecutor(
    repo_root={repo_root!r},
    model="example-model-identifier",
    controlled_experiment=False,
    authorization=None,
    exploratory_capability=None,
    invocation_identity=None,
)
ctx = {{
    "workflow_id": "phase3-test-workflow",
    "expected_output_path": {campaign_path!r},
    "artifact_session_dir": {f"{repo_root}/.phase3-session"!r},
    "artifact_type": "attempt_result",
    "workflow_stage": "stage-2",
    "target_repository": {f"{repo_root}/experiments/campaigns/EXP-0001-alpha"!r},
    "target_sha": "000000000000000000000000000000000000beef",
    "campaign_id": "EXP-0001-alpha",
    "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
    "attempt_id": "a1b2c3d4-e5f6-4789-8abc-def012345678",
    "configuration_id": "1" * 64,
}}
result = executor.invoke_skill(
    skill_id="repo-sensemaker",
    invocation_command="/skill repo-sensemaker",
    input_artifacts=[],
    expected_output_artifact="attempt_result",
    context=ctx,
)
assert result.status == se.SkillExecutionStatus.FAILED, result
assert {EXPLORATORY_COMPONENT_UNAVAILABLE!r} in result.error, result.error
print("EXECUTOR_FAIL_CLOSED_OK")
"""
    _assert_ok(_run(code), "EXECUTOR_FAIL_CLOSED_OK")


def test_exploratory_identity_never_downgraded_to_ordinary_by_any_declaration():
    code = _MINIMAL_SETUP + _CAMPAIGN_IDENTITY + _DECLARED + """\
for variant in (None, declared):
    lane, _ = ga.derive_authorization_lane(identity, variant)
    assert lane in (se.LANE_EXPLORATORY, se.LANE_AMBIGUOUS), (
        f"declaration {variant!r} downgraded an exploratory identity to {lane}")
    assert lane != se.LANE_ORDINARY
malformed = ga.DeclaredExploratory(
    campaign_id="EXP-X", classification="", attempt_id="", configuration_id="")
lane, _ = ga.derive_authorization_lane(identity, malformed)
assert lane == se.LANE_AMBIGUOUS, lane
print("NEVER_ORDINARY_OK")
"""
    _assert_ok(_run(code), "NEVER_ORDINARY_OK")


def test_mixed_canonical_exploratory_identity_stays_ambiguous_without_import():
    code = _MINIMAL_SETUP + _EVIDENCE_IDENTITY + _DECLARED + _FORBIDDEN_CHECK + """\
lane, signals = ga.derive_authorization_lane(identity, declared)
assert lane == se.LANE_AMBIGUOUS, lane
try:
    se.require_invocation_authorization(
        None, None, identity=identity, model="example-model-identifier",
        executor_name="isolation-test", declared=declared)
    raise AssertionError("expected a canonical Gate A denial")
except se.GateAAuthorizationRequired as exc:
    assert exc.code.startswith("GATE_A_"), exc.code
assert not forbidden_present, forbidden_present
print("MIXED_AMBIGUOUS_OK")
"""
    _assert_ok(_run(code), "MIXED_AMBIGUOUS_OK")
