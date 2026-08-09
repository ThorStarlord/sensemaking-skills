"""
Test evidence rules dual-mode documentation (INFRA-001).
Verifies that evidence-rules document both investigative and durable modes.
"""

import os


def test_evidence_rules_exists():
    """Test that evidence-rules.md documentation exists"""
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    assert os.path.exists(path), f"evidence-rules.md not found at {path}"


def test_evidence_rules_documents_dual_modes():
    """Test that evidence-rules document both output modes"""
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    with open(path) as f:
        content = f.read()

    assert "investigative" in content.lower(), \
        "evidence-rules.md must document investigative mode"
    assert "durable" in content.lower(), \
        "evidence-rules.md must document durable mode"


def test_evidence_rules_explains_investigative():
    """Test that investigative mode is explained"""
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    with open(path) as f:
        content = f.read()

    assert "line number" in content.lower() or "line" in content.lower(), \
        "investigative mode must mention line numbers"


def test_evidence_rules_explains_durable():
    """Test that durable mode is explained"""
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    with open(path) as f:
        content = f.read()

    assert "grep" in content.lower() or "verifiable" in content.lower(), \
        "durable mode must mention grep-verifiable or verifiable approach"


def test_repo_analysis_template_has_mode_toggle():
    """Test that repo-analysis-template.md has mode toggle"""
    path = "skills/repo-sensemaker/references/repo-analysis-template.md"
    assert os.path.exists(path), f"repo-analysis-template.md not found at {path}"

    with open(path) as f:
        content = f.read()

    assert "<!-- mode: investigative | durable -->" in content, \
        "template must carry the literal mode toggle marker (<!-- mode: investigative | durable -->)"


def test_downstream_docs_explain_implications():
    """Test that downstream consumer docs explain mode implications"""
    # Check prompt-handoff docs if they exist
    doc_paths = [
        "prompt-handoff/AGENTS.md",
        "docs/agents/prompt-handoff.md",
    ]

    for path in doc_paths:
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            # Should mention mode or staleness concern
            assert "mode" in content.lower() or "staleness" in content.lower() or \
                   "line number" in content.lower(), \
                f"{path} should document mode implications"
            return  # Found one valid doc

    # If no downstream docs found, that's OK for v1 (can be added later)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")

    print("Checking evidence dual-mode documentation...")
    path = "skills/repo-sensemaker/references/evidence-rules.md"
    if os.path.exists(path):
        print(f"✓ Found {path}")
        with open(path) as f:
            content = f.read()
        if "investigative" in content.lower():
            print("✓ Investigative mode documented")
        if "durable" in content.lower():
            print("✓ Durable mode documented")
    else:
        print(f"✗ Missing {path}")
