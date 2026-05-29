"""
Test artifact-contract schemas for PM/engineering pipeline.

Validates that prd, issue_list, agent_brief, and code_patch have
required sections and machine fields as per INFRA-004.
"""

import yaml
import os
from pathlib import Path


def load_contracts():
    """Load artifact-contracts.yaml"""
    # Try main location first
    main_path = "workflow-orchestrator/references/artifact-contracts.yaml"
    if not os.path.exists(main_path):
        # Fall back to worktree location
        worktrees_dir = ".claude/worktrees"
        if os.path.exists(worktrees_dir):
            # Use first available worktree
            for worktree in os.listdir(worktrees_dir):
                path = f"{worktrees_dir}/{worktree}/skills/workflow-orchestrator/references/artifact-contracts.yaml"
                if os.path.exists(path):
                    main_path = path
                    break

    with open(main_path) as f:
        return yaml.safe_load(f)


def test_artifact_contracts_can_parse():
    """Test that artifact-contracts.yaml is valid YAML"""
    contracts = load_contracts()
    assert contracts is not None
    assert "artifacts" in contracts
    assert isinstance(contracts["artifacts"], list)


def test_prd_contract_exists():
    """Test that prd artifact contract exists"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    assert "prd" in artifacts


def test_prd_has_required_sections():
    """Test that prd contract specifies required_sections"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    prd = artifacts["prd"]

    assert "required_sections" in prd, "prd must have required_sections field"
    assert isinstance(prd["required_sections"], list)

    # Check for expected sections
    expected = ["executive_summary", "user_goal", "features", "acceptance_criteria"]
    for section in expected:
        assert section in prd["required_sections"], f"prd missing required section: {section}"


def test_prd_has_machine_fields():
    """Test that prd contract specifies required_machine_fields"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    prd = artifacts["prd"]

    assert "required_machine_fields" in prd, "prd must have required_machine_fields"
    assert isinstance(prd["required_machine_fields"], list)

    expected = ["prd_id", "date", "status", "source_intent_ref"]
    for field in expected:
        assert field in prd["required_machine_fields"], f"prd missing machine field: {field}"


def test_issue_list_contract_has_required_sections():
    """Test that issue_list contract specifies required_sections"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    issue_list = artifacts["issue_list"]

    assert "required_sections" in issue_list
    assert "issues_generated" in issue_list["required_sections"]


def test_issue_list_has_per_issue_schema():
    """Test that issue_list contract defines per-issue fields"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    issue_list = artifacts["issue_list"]

    assert "per_issue" in issue_list, "issue_list must define per_issue schema"
    expected_fields = ["issue_id", "title", "effort", "acceptance_criteria"]
    for field in expected_fields:
        assert field in issue_list["per_issue"], f"per_issue missing field: {field}"


def test_agent_brief_contract_complete():
    """Test that agent_brief contract is complete"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    brief = artifacts["agent_brief"]

    assert "required_sections" in brief
    assert "required_machine_fields" in brief
    assert "task" in brief["required_sections"]
    assert "parent_issue_id" in brief["required_machine_fields"]


def test_code_patch_contract_complete():
    """Test that code_patch contract is complete"""
    contracts = load_contracts()
    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    patch = artifacts["code_patch"]

    assert "required_sections" in patch
    assert "required_machine_fields" in patch
    assert "files_created" in patch["required_sections"]
    assert "parent_brief_id" in patch["required_machine_fields"]


if __name__ == "__main__":
    # Quick sanity check
    contracts = load_contracts()
    print(f"✓ Loaded {len(contracts['artifacts'])} artifacts")

    artifacts = {a["id"]: a for a in contracts["artifacts"]}
    for artifact_id in ["prd", "issue_list", "agent_brief", "code_patch"]:
        if artifact_id in artifacts:
            print(f"✓ Found {artifact_id}")
        else:
            print(f"✗ Missing {artifact_id}")
