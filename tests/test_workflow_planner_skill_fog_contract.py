"""Regression guard for issue #229.

The workflow-planner SKILL previously drifted from the ratified model:
- it listed `integration_fog` as a fifth canonical fog type (the active enum
  holds exactly four: product_fog, ui_fog, docs_fog, architecture_fog);
- it presented fog->workflow selection as automatic runtime routing and as
  execution authority, and named `recommended_workflow_id` as the plan's
  required workflow-selection field.

Under the ratified boundary the plan's authoritative workflow-selection field
is `chosen_workflow_id`; `recommended_workflow_id` belongs to the repository
sensemaking brief as a planning recommendation. No pre-existing test reads
skills/workflow-planner/SKILL.md for these semantics, so this guard locks the
corrected contract in.
"""

import os
import re
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL_MD = os.path.join(REPO_ROOT, "skills", "workflow-planner", "SKILL.md")

CANONICAL_FOG_TYPES = {
    "product_fog",
    "ui_fog",
    "docs_fog",
    "architecture_fog",
}


class TestWorkflowPlannerSkillFogContract(unittest.TestCase):
    def setUp(self):
        with open(SKILL_MD, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_skill_lists_only_four_canonical_fog_types(self):
        # The CRITICAL sentence must declare exactly the four canonical fog
        # types and never teach `integration_fog` as canonical.
        m = re.search(r"four canonical fog types are ([^\.\n]+)", self.content)
        self.assertIsNotNone(
            m, "SKILL.md must declare the four canonical fog types explicitly"
        )
        declared = {
            tok.strip()
            for tok in m.group(1).replace("`", "").split(",")
            if tok.strip()
        }
        self.assertEqual(
            declared, CANONICAL_FOG_TYPES,
            "The four-fog list in SKILL.md must match the ratified canonical set",
        )
        # The fog->workflow mapping must not teach integration_fog as a routable
        # fog type (it must not appear in the selection-mapping lines).
        mapping_section = self.content.split("Workflow selection mapping", 1)[1]
        mapping_head = mapping_section.split("\n\n", 1)[0]
        self.assertNotIn(
            "integration_fog",
            mapping_head,
            "integration_fog must not be taught as a routable/selectable fog type",
        )

    def test_plan_required_workflow_selection_field_is_chosen_workflow_id(self):
        # Issue #229: recommended_workflow_id belongs to the brief; the plan's
        # authoritative workflow-selection field is chosen_workflow_id.
        self.assertIn(
            "chosen_workflow_id",
            self.content,
            "The plan must teach chosen_workflow_id as its workflow-selection field",
        )
        m = re.search(
            r"Section 11: Machine-readable plan\*+ YAML block containing "
            r"`?([a-z_]+)`?",
            self.content,
        )
        self.assertIsNotNone(
            m, "SKILL.md must name the Section 11 required field explicitly"
        )
        self.assertEqual(
            m.group(1),
            "chosen_workflow_id",
            "Section 11's required field must be chosen_workflow_id, not "
            "recommended_workflow_id",
        )

    def test_fog_to_workflow_mapping_is_recommendation_not_authority(self):
        # The mapping must be framed as a planning recommendation / selection
        # aid, not automatic execution authority.
        self.assertIn(
            "planning recommendation / selection aid",
            self.content,
            "fog->workflow mapping must be framed as a recommendation",
        )
        self.assertIn(
            "A recommendation is not execution authorization",
            self.content,
            "the skill must state that a recommendation is not execution authorization",
        )

    def test_plan_output_contract_points_to_chosen_workflow_id_not_auto_invoke(self):
        # The plan's machine-readable output must not direct the runtime to
        # auto-invoke via recommended_workflow_id.
        self.assertNotIn(
            "auto-invoke next",
            self.content,
            "the skill must not teach auto-invocation via recommended_workflow_id",
        )


if __name__ == "__main__":
    unittest.main()
