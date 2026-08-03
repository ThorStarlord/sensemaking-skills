"""Installed-wheel smoke test.

Builds the package as an actual wheel, installs it into a throwaway venv
alongside its runtime dependencies, and exercises the public API from a
working directory that has neither ``docs/`` nor ``scripts/`` available --
proving the package does not silently depend on
``Path(__file__).parents[...] / "docs"`` / ``"scripts"`` / a sibling
repository-root layout at runtime (it must load its JSON schemas via
``importlib.resources`` and its path-containment helpers via a normal
package import, not a repository-relative filesystem walk).

This test is slow (builds a wheel and a venv) and touches the network only
to resolve already-pinned dependency versions from the configured index
(no external network calls are made by the package itself). It is marked
so it can be skipped in fast local iteration; CI should still run it.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
import venv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_installed_wheel_works_outside_repository_checkout(tmp_path):
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", str(REPO_ROOT), "--no-deps",
         "--wheel-dir", str(wheel_dir)],
        capture_output=True, text=True, timeout=300,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, f"expected exactly one wheel, got {wheels}"

    venv.create(venv_dir, with_pip=True)
    venv_python = venv_dir / ("Scripts/python.exe" if sys.platform.startswith("win")
                               else "bin/python")

    install = subprocess.run(
        [str(venv_python), "-m", "pip", "install", str(wheels[0]),
         "PyYAML>=6.0,<7.0", "jsonschema>=4.18,<5.0", "rfc8785>=0.1.4,<0.2"],
        capture_output=True, text=True, timeout=300,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    script = textwrap.dedent("""
        import os
        assert not os.path.isdir("docs"), "docs/ must not be visible to this smoke test"
        assert not os.path.isdir("scripts"), "scripts/ must not be visible to this smoke test"

        import sensemaking_skills.campaign_validation as cv
        from sensemaking_skills import path_containment as pc

        # Schemas load as packaged resources.
        from sensemaking_skills.campaign_validation import schema_validation
        assert schema_validation.policy_schema_errors({}) != []

        # Path-containment helpers load and work.
        canon = pc.canonicalize_path("a/b/c")
        assert canon.parts == ("a", "b", "c")

        print("WHEEL_SMOKE_OK")
    """)
    run = subprocess.run(
        [str(venv_python), "-c", script],
        capture_output=True, text=True, timeout=60, cwd=str(work_dir),
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert "WHEEL_SMOKE_OK" in run.stdout
