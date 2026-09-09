from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess


ROOT = Path(__file__).parents[1]


def _validator_module():
    path = ROOT / "scripts" / "validate-product-boundary.py"
    spec = importlib.util.spec_from_file_location("validate_product_boundary", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_product_lab_boundary_contract_is_valid():
    validator = _validator_module()
    assert validator.validate() == []


def test_historical_combined_workflow_is_retained_outside_actions_directory():
    archived = ROOT / "docs" / "archive" / "ci" / "validator-ecosystem-pre-core-lab-split.yml"
    assert archived.is_file()
    text = archived.read_text(encoding="utf-8")
    assert "phase3-exploratory-authorization:" in text
    assert "phase4-campaign-ledger:" in text
    assert "phase6-execution-boundary:" in text


def test_release_fallback_is_not_a_literal_version_authority():
    package_init = (ROOT / "src" / "sensemaking_skills" / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert '__version__ = "0+unknown"' not in package_init
    assert "__version__ = _distribution_version()" in package_init


def test_lab_installed_wheel_checks_remain_product_owned():
    lab_workflow = (ROOT / ".github" / "workflows" / "lab-validation.yml").read_text(
        encoding="utf-8"
    )
    assert '--ignore-glob="tests/campaign_validation/test_installed_wheel_*.py"' in lab_workflow


def test_ephemeral_claude_worktree_gitlinks_are_not_tracked():
    tracked = subprocess.run(
        ["git", "ls-files", "--stage", "--", ".claude/worktrees"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert tracked.returncode == 0, tracked.stderr
    assert not any(line.startswith("160000 ") for line in tracked.stdout.splitlines())
    assert ".claude/worktrees/" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
