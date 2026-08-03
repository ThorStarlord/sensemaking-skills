"""Tests for the artifact-root filesystem trust boundary adapter.

These exercise the narrow adapter in ``fs_adapter.py`` around Gate A's own
``canonicalize_path`` / ``resolve_containment`` (imported, never
reimplemented). They do not modify or import ``gate_a_authorization.py``'s
behavior in any way that could regress its own test suite -- see
``test_gate_a_regression_untouched.py``.
"""

from __future__ import annotations

import os
import sys

import pytest

from sensemaking_skills.campaign_validation import (
    ValidationContext,
    load_and_validate_configuration_from_root,
    load_and_validate_policy_from_root,
)
from sensemaking_skills.campaign_validation.fs_adapter import (
    ArtifactRootError,
    resolve_under_root,
)

from .fixtures import base_policy_doc, finalize_policy, finalize_configuration, base_configuration_doc
from .helpers import to_bytes


def test_resolve_under_root_accepts_contained_relative_path(tmp_path):
    (tmp_path / "policy.yaml").write_text("a: 1\n", encoding="utf-8")
    resolved = resolve_under_root("policy.yaml", str(tmp_path))
    assert resolved.name == "policy.yaml"


def test_resolve_under_root_rejects_lexical_escape(tmp_path):
    with pytest.raises(ArtifactRootError) as exc_info:
        resolve_under_root("../../etc/passwd", str(tmp_path))
    assert exc_info.value.code in ("CAMPAIGN_PATH_ESCAPE", "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION")


def test_resolve_under_root_rejects_absolute_path_outside_root(tmp_path):
    outside = tmp_path.parent / "outside-file.yaml"
    with pytest.raises(ArtifactRootError) as exc_info:
        resolve_under_root(str(outside), str(tmp_path))
    assert exc_info.value.code == "CAMPAIGN_PATH_ESCAPE"


@pytest.mark.skipif(sys.platform.startswith("win"), reason="symlink creation needs elevated privilege on Windows CI")
def test_resolve_under_root_rejects_symlink_escape(tmp_path):
    outside_dir = tmp_path.parent / "outside-dir-for-symlink-test"
    outside_dir.mkdir(exist_ok=True)
    (outside_dir / "secret.yaml").write_text("a: 1\n", encoding="utf-8")
    link = tmp_path / "escape-link"
    os.symlink(outside_dir, link, target_is_directory=True)
    with pytest.raises(ArtifactRootError) as exc_info:
        resolve_under_root("escape-link/secret.yaml", str(tmp_path))
    assert exc_info.value.code == "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION"


def test_root_separation_two_roots_do_not_cross_contaminate(tmp_path):
    root_a = tmp_path / "root_a"
    root_b = tmp_path / "root_b"
    root_a.mkdir()
    root_b.mkdir()
    (root_a / "policy.yaml").write_text("a: 1\n", encoding="utf-8")
    resolved = resolve_under_root("policy.yaml", str(root_a))
    assert str(resolved).startswith(str(root_a.resolve()))
    with pytest.raises(ArtifactRootError):
        # policy.yaml does not exist under root_b -- resolve_under_root itself
        # does not require existence, but a path escaping root_b lexically
        # (pointing back into root_a) must still fail.
        resolve_under_root(f"../root_a/policy.yaml", str(root_b))


def test_load_and_validate_policy_missing(tmp_path):
    ctx = ValidationContext(current_time="2026-06-01T00:00:00+00:00")
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml"], ctx)
    assert result.failure_code == "CAMPAIGN_POLICY_MISSING"


def test_load_and_validate_policy_duplicate_candidates_ambiguous(tmp_path):
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    (tmp_path / "policy-a.yaml").write_bytes(to_bytes(doc))
    (tmp_path / "policy-b.yaml").write_bytes(to_bytes(doc))
    ctx = ValidationContext(current_time="2026-06-01T00:00:00+00:00")
    result = load_and_validate_policy_from_root(
        str(tmp_path), ["policy-a.yaml", "policy-b.yaml"], ctx
    )
    assert result.failure_code == "CAMPAIGN_POLICY_IDENTITY_AMBIGUOUS"


def test_load_and_validate_policy_single_candidate_succeeds(tmp_path):
    doc = finalize_policy(base_policy_doc(["1" * 64]))
    (tmp_path / "policy.yaml").write_bytes(to_bytes(doc))
    ctx = ValidationContext(current_time="2026-06-01T00:00:00+00:00")
    result = load_and_validate_policy_from_root(str(tmp_path), ["policy.yaml", "missing.yaml"], ctx)
    assert result.valid


def test_load_and_validate_configuration_duplicate_candidates_ambiguous(tmp_path):
    config = finalize_configuration(base_configuration_doc())
    policy = finalize_policy(base_policy_doc([config["configuration_id"]]))
    (tmp_path / "config-a.yaml").write_bytes(to_bytes(config))
    (tmp_path / "config-b.yaml").write_bytes(to_bytes(config))
    result = load_and_validate_configuration_from_root(
        str(tmp_path), ["config-a.yaml", "config-b.yaml"], policy
    )
    assert result.failure_code == "CAMPAIGN_CONFIGURATION_IDENTITY_AMBIGUOUS"
