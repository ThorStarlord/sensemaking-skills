"""Regression coverage for CI command parsing."""

from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "validation.yml"

# Spot-check members that must stay in the repository-contracts assertion
# suite: restructuring the CI file must not silently drop contract coverage.
REQUIRED_SUITE_MEMBERS = (
    "tests/test_repo_probes.py",
    "tests/test_cli.py",
    "tests/test_strategic_sensemaking_loop.py",
)


def test_core_assertion_command_is_not_yaml_folded() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["repository-contracts"]["steps"]
    command = next(step["run"] for step in steps
                   if step.get("name") == "Stable repository assertion suite")

    assert "python -m pytest" in command, \
        "the assertion suite step must invoke pytest explicitly"
    for member in REQUIRED_SUITE_MEMBERS:
        assert member in command, \
            f"{member} dropped from the repository-contracts assertion suite"
