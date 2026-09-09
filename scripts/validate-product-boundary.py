#!/usr/bin/env python3
"""Fail closed when product packaging and the retained research lab re-couple."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_PACKAGE_GLOBS = {
    "sensemaking_skills.campaign_accounting*",
    "sensemaking_skills.campaign_validation*",
    "sensemaking_skills.exploratory_authorization*",
    "sensemaking_skills.exploratory_execution*",
}
LAB_DEPENDENCIES = {"jsonschema", "rfc8785"}


def _dependency_name(spec: str) -> str:
    return re.split(r"[<>=!~\[; ]", spec, maxsplit=1)[0].strip().lower()


def validate() -> list[str]:
    errors: list[str] = []

    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)
    project = pyproject.get("project", {})
    if not isinstance(project.get("version"), str) or not project["version"]:
        errors.append("pyproject.toml [project].version must be the release authority")

    dependency_names = {
        _dependency_name(item) for item in project.get("dependencies", [])
        if isinstance(item, str)
    }
    leaked = sorted(dependency_names & LAB_DEPENDENCIES)
    if leaked:
        errors.append(f"lab-only dependencies leaked into product runtime: {leaked}")

    find = pyproject.get("tool", {}).get("setuptools", {}).get("packages", {}).get("find", {})
    excludes = set(find.get("exclude", []))
    missing_excludes = sorted(LAB_PACKAGE_GLOBS - excludes)
    if missing_excludes:
        errors.append(f"lab packages are not excluded from wheel discovery: {missing_excludes}")

    setup_path = ROOT / "setup.py"
    tree = ast.parse(setup_path.read_text(encoding="utf-8"), filename=str(setup_path))
    setup_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "setup"
    ]
    if len(setup_calls) != 1:
        errors.append("setup.py must contain exactly one setup() build-hook call")
    else:
        keywords = {kw.arg for kw in setup_calls[0].keywords if kw.arg is not None}
        if keywords != {"cmdclass"}:
            errors.append(f"setup.py may define only cmdclass, found metadata keys: {sorted(keywords)}")

    package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package_json.get("private") is not True:
        errors.append("package.json must be private repository tooling metadata")
    if "version" in package_json:
        errors.append("package.json must not declare the Python product version")
    if package_json.get("devDependencies"):
        errors.append("package.json must not model Python dependencies as npm devDependencies")

    init_text = (ROOT / "src" / "sensemaking_skills" / "__init__.py").read_text(encoding="utf-8")
    if re.search(r"__version__\s*=\s*['\"]", init_text):
        errors.append("__init__.py must derive __version__ from installed distribution metadata without a literal fallback declaration")

    tracked = subprocess.run(
        ["git", "ls-files", "src/sensemaking_skills.egg-info"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if tracked.returncode == 0 and tracked.stdout.strip():
        errors.append("generated src/sensemaking_skills.egg-info metadata must not be tracked")

    core_workflow = (ROOT / ".github" / "workflows" / "validation.yml").read_text(encoding="utf-8")
    for forbidden in (
        "phase3-exploratory-authorization",
        "phase4-campaign-ledger",
        "phase4-windows-path-confinement",
        "phase5-exp0001-preparation",
        "phase6-execution-boundary",
    ):
        if forbidden in core_workflow:
            errors.append(f"lab job {forbidden!r} leaked into product validation workflow")

    lab_workflow = (ROOT / ".github" / "workflows" / "lab-validation.yml").read_text(encoding="utf-8")
    if "workflow_dispatch" not in lab_workflow:
        errors.append("lab workflow must remain explicitly dispatchable")
    if "requirements-lab.txt" not in lab_workflow:
        errors.append("lab workflow must install the source-only lab dependency manifest")
    if '--ignore-glob="tests/campaign_validation/test_installed_wheel_*.py"' not in lab_workflow:
        errors.append("lab workflow must leave installed-wheel qualification to Product Validation")

    worktree_entries = subprocess.run(
        ["git", "ls-files", "--stage", "--", ".claude/worktrees"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if worktree_entries.returncode != 0:
        errors.append("unable to inspect tracked .claude/worktrees entries")
    elif any(line.startswith("160000 ") for line in worktree_entries.stdout.splitlines()):
        errors.append("ephemeral .claude/worktrees gitlinks must not be tracked")
    ignored_paths = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    if ".claude/worktrees/" not in ignored_paths:
        errors.append(".gitignore must exclude ephemeral .claude/worktrees/")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("PRODUCT_LAB_BOUNDARY_INVALID")
        for error in errors:
            print(f" - {error}")
        return 1
    print("PRODUCT_LAB_BOUNDARY_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
