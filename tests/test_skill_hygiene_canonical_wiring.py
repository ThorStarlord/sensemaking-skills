"""
Regression tests for validate-skill-hygiene.py's canonical wiring
(Construction Slice 1).

Before this fix, checks 2 ("skill IDs cross-ref") and 3 ("artifact contracts
resolve") read workflow-orchestrator/references/{workflow-registry,
skill-registry,artifact-contracts}.yaml -- a legacy tree that no longer
carries workflow-registry.yaml or skill-registry.yaml at all. Both checks
had a branch that silently returned an EMPTY error list when the registry
failed to load, so the validator printed "PASSED" for checks it never
actually ran (S1's false-green finding).

Repointing the paths alone is not sufficient: the canonical
skill-registry.yaml nests skills under `ecosystems: {name: {skills: [...]}}`
rather than a flat `skills:` list, workflow steps reference a skill via the
`skill` key (not `skill_id`), and each skill declares a single `artifact`
field (not `input_artifact_ids`/`output_artifact_ids`). A naive repoint
would keep silently passing via empty iteration instead of a missing file.
"""

import importlib.util
import os
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

if "validate_skill_hygiene" in sys.modules:
    hygiene = sys.modules["validate_skill_hygiene"]
else:
    _spec = importlib.util.spec_from_file_location(
        "validate_skill_hygiene", os.path.join(SCRIPTS_DIR, "validate-skill-hygiene.py")
    )
    hygiene = importlib.util.module_from_spec(_spec)
    sys.modules["validate_skill_hygiene"] = hygiene
    _spec.loader.exec_module(hygiene)


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


@pytest.fixture
def canonical_repo(tmp_path, monkeypatch):
    """chdir into a tmp repo root with a minimal, valid canonical
    skills/workflow-planner/references/ tree."""
    refs = tmp_path / "skills" / "workflow-planner" / "references"
    _write(str(refs / "skill-registry.yaml"), """\
ecosystems:
  core:
    name: Core
    skills:
      - id: repo-sensemaker
        purpose: diagnose
        artifact: repository_sensemaking_brief
""")
    _write(str(refs / "workflow-registry.yaml"), """\
workflows:
  - id: fast-path-workflow
    steps:
      - id: 1
        skill: repo-sensemaker
""")
    _write(str(refs / "artifact-contracts.yaml"), """\
artifacts:
  - id: repository_sensemaking_brief
""")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_canonical_repo_has_no_xref_errors(canonical_repo):
    assert hygiene.check_skill_registry_xref() == []


def test_canonical_repo_has_no_artifact_errors(canonical_repo):
    assert hygiene.check_artifact_contracts() == []


def test_detects_workflow_step_referencing_missing_skill(canonical_repo):
    refs = canonical_repo / "skills" / "workflow-planner" / "references"
    _write(str(refs / "workflow-registry.yaml"), """\
workflows:
  - id: fast-path-workflow
    steps:
      - id: 1
        skill: does-not-exist
""")
    errors = hygiene.check_skill_registry_xref()
    assert any("MISSING_SKILL_ID" in e and "does-not-exist" in e for e in errors), errors


def test_detects_skill_referencing_missing_artifact_contract(canonical_repo):
    refs = canonical_repo / "skills" / "workflow-planner" / "references"
    _write(str(refs / "artifact-contracts.yaml"), "artifacts: []\n")
    errors = hygiene.check_artifact_contracts()
    assert any(
        "MISSING_ARTIFACT_CONTRACT" in e and "repository_sensemaking_brief" in e
        for e in errors
    ), errors


def test_missing_canonical_workflow_registry_is_a_hard_error_not_a_silent_pass(tmp_path, monkeypatch):
    """The core false-green bug: no skills/workflow-planner/references/ tree
    at all must produce a reported error, not a silently-empty error list."""
    monkeypatch.chdir(tmp_path)
    assert hygiene.check_skill_registry_xref() != []


def test_missing_canonical_artifact_contracts_is_a_hard_error_not_a_silent_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert hygiene.check_artifact_contracts() != []


def test_no_legacy_workflow_orchestrator_path_in_source():
    src = open(os.path.join(SCRIPTS_DIR, "validate-skill-hygiene.py"), encoding="utf-8").read()
    assert "workflow-orchestrator/references" not in src
