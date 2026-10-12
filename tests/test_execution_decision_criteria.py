"""
Test execution decision criteria documentation (INFRA-002).
Verifies that the agent decision-tree documentation (AGENTS.md) exists.
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
