"""Deterministic contract tests: repo-sensemaker template <-> validate-brief.py.

Proves that skills/repo-sensemaker/references/repo-analysis-template.md, the
authoritative contract (skills/workflow-planner/references/artifact-contracts.yaml),
and scripts/validate-brief.py all agree on the shape of the `evidence` field.

Uses the real `validate-brief.py` CLI (subprocess) rather than reimplementing
its parsing logic.
"""

import json
import os
import re
import subprocess
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATE_BRIEF = os.path.join(REPO_ROOT, "scripts", "validate-brief.py")
TEMPLATE_PATH = os.path.join(
    REPO_ROOT, "skills", "repo-sensemaker", "references", "repo-analysis-template.md"
)
CONTRACTS_PATH = os.path.join(
    REPO_ROOT, "skills", "workflow-planner", "references", "artifact-contracts.yaml"
)
CANONICAL_FIXTURE = os.path.join(
    REPO_ROOT, "tests", "fixtures", "repo-sensemaker-template-canonical.md"
)


def run_validate_brief(path: str) -> dict:
    result = subprocess.run(
        [sys.executable, VALIDATE_BRIEF, path, "--json"],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def load_contract_entry() -> dict:
    with open(CONTRACTS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for artifact in data["artifacts"]:
        if artifact["id"] == "repository_sensemaking_brief":
            return artifact
    raise AssertionError("repository_sensemaking_brief not declared in artifact-contracts.yaml")


def first_yaml_block_under_section_13(content: str) -> dict:
    """Mirror validate-brief.py's own extraction: the first yaml fence after '## 13.'."""
    match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert match, (
        "Template's '## 13. Machine-readable handoff' section must be followed "
        "immediately by a single yaml fence (no intervening subheading text), "
        "matching what validate-brief.py's parser actually looks for."
    )
    return yaml.safe_load(match.group(1))


def complete_example_yaml_block(content: str) -> dict:
    """The '### Complete Example' section's own yaml fence, specifically --
    not "whichever yaml fence happens to be last in the file". The template
    may legitimately contain yaml fences after Complete Example (e.g.
    Section 15's own field-shape documentation), so anchoring by heading,
    not position, is what actually proves this section's identity.
    """
    match = re.search(
        r"### Complete Example\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert match, "Template must have a '### Complete Example' heading followed by a yaml fence."
    return yaml.safe_load(match.group(1))


def write_tmp(tmp_path, name: str, content: str) -> str:
    path = os.path.join(tmp_path, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# 1 & 2: producer template requires `evidence` in the canonical shape, matching contract naming/nesting
def test_template_first_yaml_block_declares_evidence_as_list():
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        content = f.read()
    data = first_yaml_block_under_section_13(content)
    assert "evidence" in data, (
        "Template's parsed machine-readable block must declare 'evidence' "
        "(not only 'evidence_excerpts')."
    )
    assert isinstance(data["evidence"], list)


def test_contract_declares_evidence_as_required_machine_field():
    entry = load_contract_entry()
    assert "evidence" in entry["required_machine_fields"]
    assert "evidence" in entry["required_sections"]


# 3: canonical valid example (Complete Example) matches the same required shape
def test_template_complete_example_matches_canonical_fixture_shape():
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        content = f.read()
    complete_example = complete_example_yaml_block(content)
    assert isinstance(complete_example["evidence"], list)
    assert len(complete_example["evidence"]) > 0
    entry = load_contract_entry()
    for field in entry["required_machine_fields"]:
        assert field in complete_example, f"Complete Example is missing required field '{field}'"


# 4: canonical valid example passes validate-brief.py
def test_canonical_fixture_passes_validator():
    result = run_validate_brief(CANONICAL_FIXTURE)
    assert result["valid"] is True, result["errors"]
    assert result["errors"] == []


# 5: missing evidence fails
def test_missing_evidence_fails(tmp_path):
    content = """# Missing evidence

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
recommended_workflow_id: product-implementation-workflow
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
"""
    path = write_tmp(tmp_path, "missing-evidence.md", content)
    result = run_validate_brief(path)
    assert result["valid"] is False
    assert any(e["error_id"].endswith("evidence.missing_field") for e in result["errors"])


# 6: empty evidence -> documented as logic_error (fails), per validate-brief.py's contract
def test_empty_evidence_fails_as_logic_error(tmp_path):
    content = """# Empty evidence

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence: []
recommended_workflow_id: product-implementation-workflow
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
"""
    path = write_tmp(tmp_path, "empty-evidence.md", content)
    result = run_validate_brief(path)
    assert result["valid"] is False
    assert any(e["error_id"].endswith("evidence.logic_error") for e in result["errors"])


# 7: malformed evidence (wrong type) fails
def test_malformed_evidence_type_fails(tmp_path):
    content = """# Malformed evidence

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence: "README.md: not a list"
recommended_workflow_id: product-implementation-workflow
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
"""
    path = write_tmp(tmp_path, "malformed-evidence.md", content)
    result = run_validate_brief(path)
    assert result["valid"] is False
    assert any(e["error_id"].endswith("evidence.type_error") for e in result["errors"])


# 8: renamed/stale evidence field (evidence_excerpts only, no `evidence`) fails
def test_stale_evidence_excerpts_field_name_fails(tmp_path):
    content = """# Stale field name only

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: product_fog
evidence_excerpts:
  - file: README.md
    lines: L1-L5
    quote: "..."
    supports_claim: "..."
recommended_workflow_id: product-implementation-workflow
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
"""
    path = write_tmp(tmp_path, "stale-field-name.md", content)
    result = run_validate_brief(path)
    assert result["valid"] is False
    assert any(e["error_id"].endswith("evidence.missing_field") for e in result["errors"])


# 9: existing valid fixtures still pass
#
# NOTE: tests/fixtures/validate-brief/valid/valid-brief.md and
# valid-brief-bare-lines.md are excluded here: they were already failing
# validate-brief.py's primary_fog_type/evidence checks on main before this
# change (pre-existing fixture drift, unrelated to the template fix) —
# confirmed via `git stash` + direct validator run. Only fixtures that
# actually pass on main are asserted as non-regressions.
def test_existing_valid_fixtures_still_pass():
    for rel in [
        os.path.join("tests", "fixtures", "brief-valid.md"),
    ]:
        path = os.path.join(REPO_ROOT, rel)
        result = run_validate_brief(path)
        assert result["valid"] is True, f"{rel} regressed: {result['errors']}"


# 10: unrelated validators are unaffected (validate-artifact.py generic check, unrelated artifact id)
def test_unrelated_validator_unaffected():
    result = subprocess.run(
        [
            sys.executable,
            os.path.join(REPO_ROOT, "scripts", "validate-artifact.py"),
            "issue_list",
            os.path.join(REPO_ROOT, "tests", "fixtures", "brief-valid.md"),
        ],
        capture_output=True,
        text=True,
    )
    # issue_list contract has no bearing on the repo-sensemaker template change;
    # this must run without crashing due to our edit (content may fail its own checks).
    assert "Traceback" not in result.stderr
