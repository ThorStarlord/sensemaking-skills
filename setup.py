"""Setup configuration for Sensemaking Skills package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="sensemaking-skills",
    version="1.0.0",
    author="Dimmi Andreus",
    author_email="dimmi.andreus1@gmail.com",
    description="Artifact-driven diagnostic and orchestration skills for any repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimmi-andreus/sensemaking-skills",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=5.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "sensemaking-skills=sensemaking_skills.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
