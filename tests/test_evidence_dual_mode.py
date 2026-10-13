"""
Test evidence rules dual-mode documentation (INFRA-001).
Verifies that the evidence-rules reference and repo-analysis template exist.
"""

import os


def test_evidence_rules_exists():
    """Test that evidence-rules.md documentation exists"""
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    assert os.path.exists(path), f"evidence-rules.md not found at {path}"


def test_repo_analysis_template_exists():
    """Test that repo-analysis-template.md exists"""
    path = "skills/repo-sensemaker/references/repo-analysis-template.md"
    assert os.path.exists(path), f"repo-analysis-template.md not found at {path}"
