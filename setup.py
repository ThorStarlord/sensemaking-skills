#!/usr/bin/env python3
"""Build hooks for the sensemaking-skills distribution.

All release metadata lives in ``pyproject.toml``. This file exists only for the
custom build step that derives packaged runtime trees from canonical repository
sources.
"""

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    """Derive packaged Skill and validator runtimes from canonical sources."""

    def run(self):
        super().run()
        repo_root = Path(__file__).resolve().parent

        skills_src = repo_root / "skills"
        if not skills_src.is_dir():
            raise RuntimeError(
                f"canonical skills/ tree not found at {skills_src}; refusing incomplete build"
            )

        skill_dest = Path(self.build_lib) / "sensemaking_skills" / "skill_trees"
        if skill_dest.exists():
            shutil.rmtree(skill_dest)
        shutil.copytree(skills_src, skill_dest)
        self.announce(f"packaged canonical skill trees into {skill_dest}", level=2)

        scripts_src = repo_root / "scripts"
        vocabulary_src = repo_root / "docs" / "canonical-vocabulary.yaml"
        if not scripts_src.is_dir():
            raise RuntimeError(
                f"canonical scripts/ tree not found at {scripts_src}; refusing incomplete build"
            )
        if not vocabulary_src.is_file():
            raise RuntimeError(
                "canonical vocabulary not found at "
                f"{vocabulary_src}; refusing incomplete validator runtime"
            )

        runtime_dest = Path(self.build_lib) / "sensemaking_skills" / "validator_runtime"
        if runtime_dest.exists():
            shutil.rmtree(runtime_dest)
        shutil.copytree(scripts_src, runtime_dest / "scripts")
        shutil.copytree(skills_src, runtime_dest / "skills")
        (runtime_dest / "docs").mkdir(parents=True, exist_ok=True)
        shutil.copy2(vocabulary_src, runtime_dest / "docs" / vocabulary_src.name)
        self.announce(
            f"packaged canonical validator runtime into {runtime_dest}", level=2
        )


setup(cmdclass={"build_py": build_py})
