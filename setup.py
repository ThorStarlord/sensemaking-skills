#!/usr/bin/env python3
"""Setup configuration for sensemaking-skills package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="sensemaking-skills",
    version="0.2.0",
    description="Agent-native framework for repository diagnosis and workflow orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dimmi Andreus",
    author_email="dimmi.andreus1@gmail.com",
    url="https://github.com/ThorStarlord/sensemaking-skills",
    license="MIT",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["scripts.validate_brief", "scripts.validate_plan", "scripts.shadow_mode_runner"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
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
