"""PF-2 regression: recommended_workflow_id must not conflate "exists in the
Sensemaking toolchain" with "available as an execution vehicle in the analysed
target repository".

Goal A (evidence 0024): Auteur Run 1's brief set
`recommended_workflow_id: architectural-review-planning-workflow` -- a real,
liveness-active workflow in the toolchain `workflow-registry.yaml` -- for a
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
TEMPLATE_MD = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"
EXAMPLE_BRIEF = (
    REPO_ROOT / "tests" / "fixtures" / "validate-brief" / "valid"
    / "workflow-not-vendored-in-target-escalation.md"
)

_AVAILABILITY = re.compile(r"vendor|available (?:in|from)|target[- ]available|not .{0,40}available", re.I)
_TARGET = re.compile(r"target repositor|analy[sz]ed (?:target|repositor)|in the target", re.I)


def _boundary_rule_2() -> str:
    """The text of Boundary Rule 2 (the recommended_workflow_id grounding rule)
    in repo-sensemaker/SKILL.md -- located within the '## Boundary Rules'
    section, robust to the rule's bold-header wording."""
    text = SKILL_MD.read_text(encoding="utf-8")
    section = re.search(r"^##\s+Boundary Rules\s*$(.*?)(?=^##\s)", text, re.S | re.M)
    assert section, "'## Boundary Rules' section not found in repo-sensemaker/SKILL.md"
    body = section.group(1)
    m = re.search(r"^\s*2\.\s+.*?(?=^\s*3\.\s+)", body, re.S | re.M)
    assert m, "Boundary Rule 2 not found in the '## Boundary Rules' section"
    return m.group(0)


def _template_section_12() -> str:
    text = TEMPLATE_MD.read_text(encoding="utf-8")
    m = re.search(r"^##\s*12\.\s+Recommended workflow\s*$(.*?)(?=^##\s)", text, re.S | re.M)
    assert m, "Section 12 (Recommended workflow) not found in repo-analysis-template.md"
    return m.group(1)


# --------------------------------------------------------------------------- #
# Instruction surface: SKILL.md Boundary Rule 2
# --------------------------------------------------------------------------- #

def test_boundary_rule_2_still_grounds_on_the_toolchain_registry():
    """The existing registry-existence check must remain."""
    rule = _boundary_rule_2()
    assert "workflow-registry.yaml" in rule


def test_boundary_rule_2_distinguishes_toolchain_from_target_availability():
    """PF-2: the rule must tell the producer that a registry-valid workflow is not
    automatically an execution vehicle available from the analysed target."""
    rule = _boundary_rule_2()
    assert _AVAILABILITY.search(rule), (
        "Boundary Rule 2 does not mention workflow *availability* in the target "
        "(vendored / available-from-target). A registry-valid id is being treated "
        "as automatically executable from any target -- the PF-2 conflation."
    )
    assert _TARGET.search(rule), (
        "Boundary Rule 2 does not reference the analysed target repository when "
        "qualifying recommended_workflow_id provenance."
    )


def test_boundary_rule_2_routes_unavailable_workflow_to_truthful_null():
    """When a workflow exists in the toolchain but is not available from the
    target, the rule must direct the truthful no-match representation
    (null + escalation), not a bare registry id."""
    rule = _boundary_rule_2()
    assert "null" in rule and re.search(r"escalation_recommended", rule), (
        "Boundary Rule 2 must tie the not-available-in-target case to "
        "recommended_workflow_id: null + escalation_recommended: true."
    )
    # The null/escalation directive must be connected to availability, not only
    # to 'no semantically matching workflow'.
    tail = rule[rule.lower().find("registry") :]
    assert _AVAILABILITY.search(tail), (
        "the null/escalation directive is not connected to target availability"
    )


# --------------------------------------------------------------------------- #
# Instruction surface: template Section 12
# --------------------------------------------------------------------------- #

def test_template_section_12_qualifies_target_availability():
    body = _template_section_12()
    assert _AVAILABILITY.search(body), (
        "repo-analysis-template.md Section 12 still says only 'one candidate from "
        "workflow-registry.yaml' with no target-availability qualification."
    )


# --------------------------------------------------------------------------- #
# Worked example: truthful no-match because the workflow is not vendored/available
# --------------------------------------------------------------------------- #

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
    # names a real workflow as a conceptual pointer...
    assert "architectural-review-planning-workflow" in text
    # ...explicitly flagged as not available in / vendored by the target.
    assert _AVAILABILITY.search(text) and _TARGET.search(text)
