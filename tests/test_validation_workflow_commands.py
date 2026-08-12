"""Regression coverage for CI command parsing."""

from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "validation.yml"
EXPECTED_CORE_COMMAND = (
    "python -m pytest tests/test_repo_probes.py tests/test_probe_report_cli.py "
    "tests/test_probe_relationships.py tests/test_skill_distribution_probe.py "
    "tests/test_gate_relationship_findings.py tests/test_path_drift.py "
    "tests/test_cli.py -q"
)


def test_core_assertion_command_is_not_yaml_folded() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["core-assertions"]["steps"]
    command = next(step["run"] for step in steps
                   if step.get("name") == "Core assertion suite")

    assert command == EXPECTED_CORE_COMMAND
