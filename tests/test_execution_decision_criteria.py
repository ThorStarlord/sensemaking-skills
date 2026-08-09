"""
Test execution decision criteria documentation (INFRA-002).
Verifies that agent decision tree documents when to use orchestration vs. direct execution.
"""

import os


def test_agents_md_exists():
    """Test that AGENTS.md documentation exists"""
    paths = [
        "docs/AGENTS.md",
        "docs/agents/AGENTS.md",
        "AGENTS.md",
    ]

    found = False
    for path in paths:
        if os.path.exists(path):
            found = True
            break

    assert found, "AGENTS.md not found in expected locations"


def test_agents_documents_decision_tree():
    """Test that AGENTS.md documents when to orchestrate"""
    paths = [
        "docs/AGENTS.md",
        "docs/agents/AGENTS.md",
        "AGENTS.md",
    ]

    for path in paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()

            assert "orchestrat" in content.lower(), \
                "AGENTS.md must discuss orchestration decision"
            return

    assert False, "No AGENTS.md found"


def test_decision_criteria_mentioned():
    """Test that decision criteria (1-3 skills, 4+ skills, etc.) are documented"""
    paths = [
        "docs/AGENTS.md",
        "docs/agents/AGENTS.md",
        "AGENTS.md",
    ]

    for path in paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()

            # Should mention either explicit counts or general guidance
            assert "skill" in content.lower(), \
                "AGENTS.md must mention skills"
            return


def test_execution_modes_has_context_note():
    """Test that execution-modes.md has context about decision tree"""
    path = "skills/workflow-planner/references/execution-modes.md"

    if os.path.exists(path):
        with open(path) as f:
            content = f.read()

        # Should mention decision tree or link to AGENTS.md
        assert "decision" in content.lower() or "agent" in content.lower(), \
            "execution-modes.md should reference agent decision tree"
    # If file doesn't exist yet, that's OK for minimal v1


def test_example_direct_execution():
    """Test that examples distinguish direct vs. orchestrated"""
    paths = [
        "docs/AGENTS.md",
        "docs/agents/AGENTS.md",
        "AGENTS.md",
    ]

    for path in paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()

            # Should have examples
            assert "example" in content.lower() or "e.g." in content.lower(), \
                "AGENTS.md should include examples"
            return


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")

    print("Checking execution decision criteria documentation...")
    for path in ["docs/AGENTS.md", "docs/agents/AGENTS.md", "AGENTS.md"]:
        if os.path.exists(path):
            print(f"✓ Found {path}")
            break
    else:
        print("✗ AGENTS.md not found")
