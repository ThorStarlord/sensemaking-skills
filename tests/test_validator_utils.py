"""Tests for shared validator utility functions."""

import os
from pathlib import Path

from scripts._validator_utils import (
    format_error,
    load_artifact_contracts,
    load_skill_registry,
    load_weakness_types,
    load_workflow_registry,
    load_yaml,
    resolve_repo_root,
)


def test_format_error_returns_code_colon_message():
    result = format_error("TEST_CODE", "Something went wrong.")
    assert result == "TEST_CODE: Something went wrong."


def test_load_yaml_returns_dict_for_valid_yaml(tmp_path: Path):
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text("key: value\nnumber: 42\n")
    result = load_yaml(str(yaml_file))
    assert result == {"key": "value", "number": 42}


def test_load_yaml_returns_none_for_missing_file(tmp_path: Path):
    result = load_yaml(str(tmp_path / "nonexistent.yaml"))
    assert result is None


def test_resolve_repo_root_uses_given_when_absolute(tmp_path: Path):
    result = resolve_repo_root(str(tmp_path), str(tmp_path / "scripts"))
    assert result == str(tmp_path)


def test_resolve_repo_root_joins_relative_with_script_dir(tmp_path: Path):
    script_dir = str(tmp_path / "scripts")
    result = resolve_repo_root("..", script_dir)
    assert os.path.normpath(result) == os.path.normpath(str(tmp_path))


def test_load_weakness_types_parses_bolded_terms(tmp_path: Path):
    types_dir = tmp_path / "skills" / "repo-sensemaker" / "references"
    types_dir.mkdir(parents=True)
    types_file = types_dir / "weakness-types.md"
    types_file.write_text(
        "Recognized types:\n"
        "- **Vocabulary Drift**\n"
        "- **Contract Mismatch**\n"
        "- **Ghost Features**\n"
    )
    result = load_weakness_types(str(tmp_path))
    assert result == ["Vocabulary Drift", "Contract Mismatch", "Ghost Features"]


def test_load_weakness_types_returns_empty_for_missing_file(tmp_path: Path):
    result = load_weakness_types(str(tmp_path))
    assert result == []


def test_load_workflow_registry_loads_yaml(tmp_path: Path):
    ref_dir = tmp_path / "skills" / "workflow-orchestrator" / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "workflow-registry.yaml").write_text("workflows:\n  - id: test\n")
    result = load_workflow_registry(str(tmp_path))
    assert result == {"workflows": [{"id": "test"}]}


def test_load_workflow_registry_returns_none_for_missing(tmp_path: Path):
    result = load_workflow_registry(str(tmp_path))
    assert result is None


def test_load_artifact_contracts_loads_yaml(tmp_path: Path):
    ref_dir = tmp_path / "skills" / "workflow-orchestrator" / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "artifact-contracts.yaml").write_text("artifacts:\n  - id: brief\n")
    result = load_artifact_contracts(str(tmp_path))
    assert result == {"artifacts": [{"id": "brief"}]}


def test_load_artifact_contracts_returns_none_for_missing(tmp_path: Path):
    result = load_artifact_contracts(str(tmp_path))
    assert result is None


def test_load_skill_registry_loads_yaml(tmp_path: Path):
    ref_dir = tmp_path / "skills" / "workflow-orchestrator" / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "skill-registry.yaml").write_text("skills:\n  - id: test-skill\n")
    result = load_skill_registry(str(tmp_path))
    assert result == {"skills": [{"id": "test-skill"}]}


def test_load_skill_registry_returns_none_for_missing(tmp_path: Path):
    result = load_skill_registry(str(tmp_path))
    assert result is None
