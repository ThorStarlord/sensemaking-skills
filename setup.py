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
    """Derive packaged skill trees from the canonical repo-root ``skills/``.

    The repository-root ``skills/`` directory is the SINGLE authoritative
    source of the SKILL.md trees (repo-sensemaker, workflow-planner, ...).
    This build step copies them into the built package as
    ``sensemaking_skills/skill_trees/`` so the wheel actually contains them
    (Task P1-R: the shipped 0.2.1 wheel contained zero SKILL.md files). The
    packaged copy is derived at build time -- never a second manually
    maintained copy.
    """

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


setup(
    name="sensemaking-skills",
    version="0.2.2",
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
