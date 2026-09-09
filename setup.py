#!/usr/bin/env python3
"""Build hooks for the sensemaking-skills distribution.

All release metadata lives in ``pyproject.toml``.  This file exists only for
the custom build step that derives packaged Skill trees from the canonical
repository-root ``skills/`` directory.
"""

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    """Copy canonical repository Skill trees into the built Python package."""

    def run(self):
        super().run()
        src = Path(__file__).resolve().parent / "skills"
        if not src.is_dir():
            self.warn(f"skills/ not found at {src}; skill trees will not be packaged")
            return
        dest = Path(self.build_lib) / "sensemaking_skills" / "skill_trees"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        self.announce(f"packaged canonical skill trees into {dest}", level=2)


setup(cmdclass={"build_py": build_py})
