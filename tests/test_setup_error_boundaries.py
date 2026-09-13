from __future__ import annotations

import importlib.resources

import pytest

from sensemaking_skills import setup_skills


def test_unexpected_packaged_resource_failure_is_not_silently_swallowed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_unexpectedly(package):
        raise RuntimeError("resource provider failed")

    monkeypatch.setattr(importlib.resources, "files", fail_unexpectedly)

    with pytest.raises(RuntimeError, match="resource provider failed"):
        setup_skills.get_package_skills_dir()
