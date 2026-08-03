"""Characterization tests for the ``canonicalize_path`` / ``resolve_containment``
path-containment primitives, written BEFORE extracting them into a shared,
importable ``sensemaking_skills.path_containment`` module used by both
``scripts/gate_a_authorization.py`` and the campaign-validation package.

Purpose: lock in exact current behavior for a representative battery of
inputs so the extraction can be proven byte-for-byte non-regressive. The
extraction itself is done by literally moving the function/class/constant
bodies unmodified into the new shared module and having
``gate_a_authorization.py`` import (re-export) them -- not by
reimplementing them -- so post-extraction, ``gate_a_authorization.<name> is
sensemaking_skills.path_containment.<name>`` holds for every extracted name.
That identity is checked directly below and is strictly stronger evidence
of non-regression than behavioral equivalence alone, but the behavioral
battery is kept too, since identity alone would not catch a case where the
*wrong* object was imported.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent / ".." / "scripts"))
sys.path.insert(0, str((Path(__file__).resolve().parent / ".." / "scripts").resolve()))

import gate_a_authorization as ga  # noqa: E402


CANONICALIZE_CASES = [
    (None, "", "", False, ()),
    ("", "", "", False, ()),
    ("a/b/c", "", "a/b/c", False, ("a", "b", "c")),
    ("/a/b", "", "/a/b", True, ("a", "b")),
    ("C:\\a\\b", "C", "C:/a/b", True, ("a", "b")),
    ("a/./b", "", "a/b", False, ("a", "b")),
    ("a//b", "", "a/b", False, ("a", "b")),
    ("../a", "", "../a", False, ("..", "a")),
    ("a/../b", "", "b", False, ("b",)),
    ("/../a", "", "/a", True, ("a",)),
]


@pytest.mark.parametrize("value,drive,lexical,is_absolute,parts", CANONICALIZE_CASES)
def test_canonicalize_path_characterization(value, drive, lexical, is_absolute, parts):
    canon = ga.canonicalize_path(value)
    assert canon.drive == drive
    assert canon.is_absolute == is_absolute
    assert canon.parts == parts


def test_has_colon_component_characterization():
    assert ga.has_colon_component(ga.canonicalize_path("dir:stream/x"))
    assert not ga.has_colon_component(ga.canonicalize_path("C:\\dir\\x"))


def test_resolve_containment_characterization(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    (root / "sub").mkdir()

    resolved, failure = ga.resolve_containment("sub/output.md", str(root))
    assert failure is None
    assert resolved is not None
    assert str(resolved).startswith(str(root.resolve()))

    # A plain LEXICAL escape with no symlink involved intentionally resolves
    # with failure=None here -- resolve_containment's own docstring/comment
    # calls this "ordinary development writing elsewhere"; it is the
    # caller's job to additionally reject a resolved path outside the root
    # if strict containment is required (this is exactly what
    # campaign_validation's fs_adapter.resolve_under_root does on top of
    # this primitive). Only a SYMLINK-mediated escape (anchored path looked
    # contained, but physical resolution landed outside root) sets a
    # failure code here.
    resolved_escape, failure_escape = ga.resolve_containment("../outside.md", str(root))
    assert failure_escape is None
    assert resolved_escape is not None
    assert not str(resolved_escape).startswith(str(root.resolve()))


def test_resolve_containment_none_and_empty_are_no_ops(tmp_path):
    assert ga.resolve_containment(None, str(tmp_path)) == (None, None)
    assert ga.resolve_containment("", str(tmp_path)) == (None, None)


def test_anchor_output_path_characterization(tmp_path):
    anchored, failure = ga.anchor_output_path("sub/x.md", str(tmp_path))
    assert failure is None
    assert str(anchored) == str(tmp_path / "sub" / "x.md")


# --- Post-extraction identity proof ----------------------------------------
# These assert that gate_a_authorization's names ARE (object identity, not
# just behavioral equivalence) the shared module's names, once the
# extraction lands. If the shared module does not exist yet, these are
# skipped rather than failed, so this file is valid both immediately before
# and immediately after the extraction commit.

try:
    from sensemaking_skills import path_containment as _shared
except ImportError:
    _shared = None


@pytest.mark.skipif(_shared is None, reason="path_containment shared module not yet extracted")
@pytest.mark.parametrize("name", [
    "canonicalize_path", "has_colon_component", "anchor_output_path",
    "CanonicalPath",
    "GATE_A_OUTPUT_PATH_ESCAPE", "GATE_A_OUTPUT_PATH_AMBIGUOUS",
    "GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE",
    "GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED",
    "GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS",
    "GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT",
    "GATE_A_OUTPUT_PATH_ALIAS_MISMATCH", "GATE_A_OUTPUT_PATH_UNANCHORABLE",
    "GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED",
])
def test_gate_a_reexports_shared_module_object_identically(name):
    assert getattr(ga, name) is getattr(_shared, name), (
        f"gate_a_authorization.{name} must be the SAME object as "
        f"path_containment.{name} (re-export, not reimplementation)"
    )


@pytest.mark.skipif(_shared is None, reason="path_containment shared module not yet extracted")
def test_gate_a_resolve_containment_delegates_without_reimplementation(tmp_path):
    """``gate_a_authorization.resolve_containment`` is kept as a real ``def``
    (not a plain import alias) only because
    ``tests/test_gate_a_physical_containment.py`` does a source-level
    inspection expecting ``def resolve_containment(`` to appear literally in
    this file. It must still be a one-line delegation, not a second
    implementation: prove behavioral equivalence directly against the
    shared module for a representative case, and prove the wrapper's own
    body is trivial (no containment logic duplicated in it).
    """
    root = tmp_path / "root"
    root.mkdir()
    for candidate in ("sub/output.md", "../escape.md", None, ""):
        assert ga.resolve_containment(candidate, str(root)) == \
            _shared.resolve_containment(candidate, str(root))

    import ast
    import inspect
    import textwrap

    source = textwrap.dedent(inspect.getsource(ga.resolve_containment))
    func_node = ast.parse(source).body[0]
    body = func_node.body
    # Strip a leading docstring Expr node if present.
    if body and isinstance(body[0], ast.Expr) and isinstance(
            getattr(body[0], "value", None), (ast.Constant,)):
        body = body[1:]
    # A trivial delegating wrapper is exactly one statement: the pass-through
    # return call -- proving no containment logic is duplicated here.
    assert len(body) == 1
    assert isinstance(body[0], ast.Return)
    assert ast.unparse(body[0].value).startswith("_path_containment.resolve_containment(")
