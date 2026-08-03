"""Tests proving Gate A deterministically loads
``sensemaking_skills.path_containment`` from THIS checkout, never from a
conflicting ambient/pre-imported installation.

Each test spawns a real subprocess (never monkeypatches ``sys.modules`` in
this process, which would leak between tests) with a deliberately
conflicting fake ``sensemaking_skills`` package placed on ``PYTHONPATH``.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

_FAKE_INIT = ""
_FAKE_PATH_CONTAINMENT = '''
"""Fake, incompatible ambient path_containment module for testing."""


def canonicalize_path(value):
    raise RuntimeError("FAKE AMBIENT MODULE WAS USED")


def resolve_containment(value, root):
    raise RuntimeError("FAKE AMBIENT MODULE WAS USED")


def has_colon_component(canon):
    raise RuntimeError("FAKE AMBIENT MODULE WAS USED")


def anchor_output_path(value, root):
    raise RuntimeError("FAKE AMBIENT MODULE WAS USED")


class CanonicalPath:
    pass


GATE_A_OUTPUT_PATH_ALIAS_MISMATCH = "FAKE"
GATE_A_OUTPUT_PATH_AMBIGUOUS = "FAKE"
GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED = "FAKE"
GATE_A_OUTPUT_PATH_ESCAPE = "FAKE"
GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT = "FAKE"
GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED = "FAKE"
GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS = "FAKE"
GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE = "FAKE"
GATE_A_OUTPUT_PATH_UNANCHORABLE = "FAKE"
PHYSICAL_CONTAINMENT_FAILURE_CODES = frozenset()
'''


@pytest.fixture()
def fake_ambient_package(tmp_path):
    """Build a throwaway directory containing a fake, conflicting
    ``sensemaking_skills`` package, and return its path (for PYTHONPATH)."""
    pkg_dir = tmp_path / "fake_ambient" / "sensemaking_skills"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "__init__.py").write_text(_FAKE_INIT, encoding="utf-8")
    (pkg_dir / "path_containment.py").write_text(_FAKE_PATH_CONTAINMENT, encoding="utf-8")
    return tmp_path / "fake_ambient"


def _run(code: str, fake_ambient_dir: Path, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    import os

    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(fake_ambient_dir) + (os.pathsep + existing if existing else "")
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=30,
    )


def test_ambient_earlier_on_pythonpath_but_checkout_module_is_used(fake_ambient_package):
    """Case 1: fake ambient package appears earlier on PYTHONPATH, but is
    NOT pre-imported before Gate A -- the checkout-local module must win."""
    code = """
        import sys
        sys.path.insert(0, "scripts")
        import gate_a_authorization as ga
        assert ga.canonicalize_path.__module__ == "sensemaking_skills.path_containment"
        result = ga.canonicalize_path("a/b")
        assert result.parts == ("a", "b")
        print("CHECKOUT_MODULE_USED")
    """
    result = _run(code, fake_ambient_package)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CHECKOUT_MODULE_USED" in result.stdout


def test_ambient_preimported_before_gate_a_fails_closed(fake_ambient_package):
    """Case 2: the fake ambient package is imported BEFORE Gate A -- Gate A
    must fail closed (ImportError) rather than silently use it."""
    code = """
        import sys
        import sensemaking_skills.path_containment  # pre-import the AMBIENT (fake) one
        sys.path.insert(0, "scripts")
        try:
            import gate_a_authorization as ga
            print("NO_ERROR_RAISED")
        except ImportError as e:
            print("IMPORT_ERROR_RAISED:", str(e)[:80])
    """
    result = _run(code, fake_ambient_package)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "IMPORT_ERROR_RAISED" in result.stdout
    assert "NO_ERROR_RAISED" not in result.stdout


def test_loaded_module_path_is_beneath_active_checkout(fake_ambient_package):
    """The loaded path_containment module's __file__ must resolve beneath
    this exact checkout's src/sensemaking_skills/, not merely 'somewhere'."""
    code = """
        import sys
        from pathlib import Path
        sys.path.insert(0, "scripts")
        import gate_a_authorization as ga
        import sensemaking_skills.path_containment as pc
        expected_dir = (Path(".").resolve() / "src" / "sensemaking_skills")
        actual = Path(pc.__file__).resolve()
        assert actual == (expected_dir / "path_containment.py").resolve(), (actual, expected_dir)
        print("PATH_BENEATH_CHECKOUT_OK")
    """
    result = _run(code, fake_ambient_package)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PATH_BENEATH_CHECKOUT_OK" in result.stdout


def test_gate_a_behavior_unchanged_with_no_ambient_conflict():
    """No conflict present -- Gate A imports and behaves exactly as before."""
    code = """
        import sys
        sys.path.insert(0, "scripts")
        import gate_a_authorization as ga
        result = ga.canonicalize_path("a/b/c")
        assert result.parts == ("a", "b", "c")
        print("NORMAL_BEHAVIOR_OK")
    """
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NORMAL_BEHAVIOR_OK" in result.stdout


def test_installed_campaign_validation_does_not_depend_on_repository_checkout():
    """This correction to Gate A's loading must not make the (separate)
    campaign_validation package depend on a repository checkout -- it
    already imports sensemaking_skills.path_containment as a normal package
    import (see fs_adapter.py), which is unaffected by Gate A's
    checkout-local-only enforcement (that enforcement lives in
    scripts/gate_a_authorization.py, a script never shipped in the wheel)."""
    import ast
    import inspect

    from sensemaking_skills.campaign_validation import fs_adapter

    source = inspect.getsource(fs_adapter)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "spec_from_file_location":
            raise AssertionError("fs_adapter.py must not call importlib.util.spec_from_file_location")
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        for name in names:
            assert "gate_a_authorization" not in name, (
                f"fs_adapter.py must not import gate_a_authorization: {name!r}"
            )
