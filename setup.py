#!/usr/bin/env python3
"""Setup configuration for sensemaking-skills package."""

import shutil
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

# Read the long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""


class build_py(_build_py):
    """Derive packaged runtime trees from canonical repository sources.

    The repository-root ``skills/`` and ``scripts/`` directories remain the
    SINGLE authoritative sources. Build-time copies make those exact bytes
    available to an installed wheel without introducing manually maintained
    duplicate Skill or validator implementations.
    """

    def run(self):
        super().run()
        repo_root = Path(__file__).resolve().parent

        skills_src = repo_root / "skills"
        if not skills_src.is_dir():
            raise RuntimeError(
                f"canonical skills/ tree not found at {skills_src}; refusing incomplete build"
            )

        # Existing P1-R distribution contract: ship the canonical Skill trees.
        skill_dest = Path(self.build_lib) / "sensemaking_skills" / "skill_trees"
        if skill_dest.exists():
            shutil.rmtree(skill_dest)
        shutil.copytree(skills_src, skill_dest)
        self.announce(f"packaged canonical skill trees into {skill_dest}", level=2)

        # P11 release-portability contract: derive a self-contained validator
        # runtime from the SAME canonical scripts/contracts used in checkout
        # development. The runtime mirrors the repository-relative paths that
        # the existing validators intentionally resolve through --repo-root.
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


setup(
    name="sensemaking-skills",
    version="0.3.0",
    description="Agent-native framework for repository diagnosis and workflow orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dimmi Andreus",
    author_email="dimmi.andreus1@gmail.com",
    url="https://github.com/ThorStarlord/sensemaking-skills",
    license="MIT",
    python_requires=">=3.11",
    packages=find_packages(where="src", include=["sensemaking_skills", "sensemaking_skills.*"]),
    package_dir={"": "src"},
    include_package_data=True,
    cmdclass={"build_py": build_py},
    install_requires=[
        "click>=8.1.0",
        "PyYAML>=6.0,<7.0",
        "jsonschema>=4.18,<5.0",
        "rfc8785>=0.1.4,<0.2",
    ],
    entry_points={
        "console_scripts": [
            "sensemaking-skills=sensemaking_skills.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="agent ai diagnosis workflow orchestration repository analysis",
    project_urls={
        "Bug Reports": "https://github.com/ThorStarlord/sensemaking-skills/issues",
        "Source": "https://github.com/ThorStarlord/sensemaking-skills",
        "Documentation": "https://github.com/ThorStarlord/sensemaking-skills#readme",
    },
)
