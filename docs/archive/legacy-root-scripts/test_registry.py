#!/usr/bin/env python
"""Test script for WorkflowRegistry functionality."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sensemaking_skills.registry import WorkflowRegistry
from sensemaking_skills.config import ConfigManager, SkillsConfig

def test_registry_loading():
    """Test that registry loads defaults successfully."""
    print("Test 1: Loading registry with defaults...")

    # Get the project root
    repo_root = Path(__file__).parent

    try:
        registry = WorkflowRegistry(repo_root)
        print(f"  [PASS] Registry loaded successfully")
        print(f"  [INFO] Loaded {registry.workflow_count()} workflows")
        return registry
    except Exception as e:
        print(f"  [FAIL] Failed to load registry: {e}")
        return None

def test_get_workflow(registry):
    """Test getting a specific workflow."""
    print("\nTest 2: Getting a specific workflow...")

    try:
        workflow = registry.get_workflow("fast-path-workflow")
        if workflow:
            print(f"  [PASS] Found workflow: {workflow.get('display_name')}")
            return True
        else:
            print(f"  [FAIL] Workflow 'fast-path-workflow' not found")
            return False
    except Exception as e:
        print(f"  [FAIL] Error getting workflow: {e}")
        return False

def test_list_workflows(registry):
    """Test listing all workflows."""
    print("\nTest 3: Listing all workflows...")

    try:
        workflows = registry.list_workflows()
        print(f"  [PASS] Found {len(workflows)} workflows")
        for wid in workflows[:3]:
            print(f"    - {wid}")
        if len(workflows) > 3:
            print(f"    ... and {len(workflows) - 3} more")
        return True
    except Exception as e:
        print(f"  [FAIL] Error listing workflows: {e}")
        return False

def test_auto_invocation(registry):
    """Test checking auto-invocation."""
    print("\nTest 4: Checking auto-invocation...")

    try:
        has_auto = registry.has_auto_invocation("fast-path-workflow")
        print(f"  [PASS] fast-path-workflow auto_invoke_next_workflow: {has_auto}")

        next_workflow = registry.get_recommended_next_workflow("fast-path-workflow")
        print(f"  [INFO] Recommended next workflow: {next_workflow}")
        return True
    except Exception as e:
        print(f"  [FAIL] Error checking auto-invocation: {e}")
        return False

def test_config_manager(registry):
    """Test that SkillsConfig properly initializes with registry."""
    print("\nTest 5: SkillsConfig integration...")

    try:
        # Create a SkillsConfig directly with a registry
        project_root = Path(__file__).parent
        config_dict = {
            "project_root": str(project_root),
            "artifacts_dir": "artifacts",
            "context_file": "CONTEXT.md",
            "skills_dir": "skills",
            "workflows_dir": "workflows",
            "adr_dir": "docs/adr",
        }

        # Create SkillsConfig with the registry
        config = SkillsConfig(config_dict, registry)

        if hasattr(config, 'workflow_registry'):
            print(f"  [PASS] SkillsConfig has workflow_registry attribute")
            print(f"  [INFO] Registry has {config.workflow_registry.workflow_count()} workflows")
            return True
        else:
            print(f"  [FAIL] SkillsConfig missing workflow_registry attribute")
            return False
    except Exception as e:
        print(f"  [FAIL] Error with SkillsConfig: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("WorkflowRegistry Tests")
    print("=" * 60)

    registry = test_registry_loading()
    if not registry:
        print("\nCannot continue without registry loaded")
        return False

    results = [
        test_get_workflow(registry),
        test_list_workflows(registry),
        test_auto_invocation(registry),
        test_config_manager(registry),
    ]

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
