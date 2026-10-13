"""PF-2 regression: recommended_workflow_id must not conflate "exists in the
Sensemaking toolchain" with "available as an execution vehicle in the analysed
target repository".

Goal A (evidence 0024): Auteur Run 1's brief set
`recommended_workflow_id: architectural-review-planning-workflow` -- a historical
conceptual pointer now retained as compatibility-only identity -- for a
target that does not vendor `workflow-planner`. The brief did not flag that the
recommended execution vehicle is unavailable from the target, pointing a naive
reader/executor at a dead end. Auteur Run 2 independently produced the truthful
`recommended_workflow_id: null` + `escalation_recommended: true` with an explicit
"no applicable workflow match" explanation. All three independent reviewers
flagged the Run 1 issue.

The repair is an instruction/qualification rule on the producer surfaces
(SKILL.md Boundary Rule 2 + the repo-analysis template) -- no new machine field,
no registry change, no routing code. These tests pin the rule and a worked
example of the truthful no-match-because-unavailable path.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
EXAMPLE_BRIEF = (
    REPO_ROOT / "tests" / "fixtures" / "validate-brief" / "valid"
    / "workflow-not-vendored-in-target-escalation.md"
)

_AVAILABILITY = re.compile(r"vendor|available (?:in|from)|target[- ]available|not .{0,40}available", re.I)
_TARGET = re.compile(r"target repositor|analy[sz]ed (?:target|repositor)|in the target", re.I)


def test_skill_grounds_recommended_workflow_id_on_the_toolchain_registry():
    """The producer surface must keep naming the field, the registry it is
    grounded on, and the escalation field used for the truthful no-match."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "recommended_workflow_id" in text
    assert "workflow-registry.yaml" in text
    assert "escalation_recommended" in text


def test_example_unavailable_workflow_brief_exists_and_is_valid():
    assert EXAMPLE_BRIEF.exists(), f"missing worked-example fixture: {EXAMPLE_BRIEF}"
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate-brief.py"),
         str(EXAMPLE_BRIEF), "--repo-root", str(REPO_ROOT)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"example brief must pass validate-brief.py:\n{proc.stdout}{proc.stderr}"


def test_example_unavailable_workflow_brief_shows_the_pattern():
    text = EXAMPLE_BRIEF.read_text(encoding="utf-8")
    assert re.search(r"recommended_workflow_id:\s*null", text)
    assert re.search(r"escalation_recommended:\s*true", text)
    # names the historical workflow identity only as a conceptual pointer...
    assert "architectural-review-planning-workflow" in text
    # ...explicitly flagged as not available in / vendored by the target.
    assert _AVAILABILITY.search(text) and _TARGET.search(text)
