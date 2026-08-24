"""Registry-copy agreement test for auto_invoke_next_workflow semantics (ADR 0026).

Both the runtime-loaded registry
(skills/workflow-planner/references/workflow-registry.yaml) and the packaged
defaults copy (src/sensemaking_skills/defaults/workflow-registry.yaml) must
encode auto_invoke_next_workflow as COMPATIBILITY / HISTORICAL TRANSITION
METADATA, NOT execution authority, and both must agree on the set of workflows
that declare it.
"""

import os
import unittest

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COPIES = [
    "skills/workflow-planner/references/workflow-registry.yaml",
    "src/sensemaking_skills/defaults/workflow-registry.yaml",
]


class TestAutoInvokeRegistryAgreement(unittest.TestCase):
    """Prove both registry copies agree on compatibility-only auto_invoke semantics."""

    def _load(self, rel):
        with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_both_copies_declare_auto_invoke_compatibility_metadata(self):
        """Both copies carry an explicit ADR 0026 compatibility-only declaration."""
        for rel in COPIES:
            with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
                text = f.read()
            self.assertIn("COMPATIBILITY / HISTORICAL TRANSITION METADATA", text,
                          f"{rel} must mark auto_invoke_next_workflow as compatibility metadata")
            self.assertIn("NOT grant execution authority", text,
                          f"{rel} must state auto_invoke_next_workflow is NOT execution authority")

    def test_both_copies_agree_on_auto_invoke_workflow_set(self):
        """Both copies list the same workflows with auto_invoke_next_workflow: true."""
        sets = []
        for rel in COPIES:
            reg = self._load(rel)
            w = {wf["id"] for wf in reg.get("workflows", [])
                 if wf.get("auto_invoke_next_workflow") is True}
            sets.append(w)
        self.assertEqual(sets[0], sets[1],
                         "registry copies must agree on which workflows declare auto-invoke")

    def test_both_copies_agree_on_ui_diagnostic_explicit_next(self):
        """ui-diagnostic-workflow declares the same auto_invoke_next_workflow_id in both."""
        next_ids = []
        for rel in COPIES:
            reg = self._load(rel)
            wf = next(w for w in reg.get("workflows", [])
                      if w.get("id") == "ui-diagnostic-workflow")
            next_ids.append(wf.get("auto_invoke_next_workflow_id"))
        self.assertEqual(next_ids[0], next_ids[1], "ui-diagnostic explicit next id must agree")
        self.assertEqual(next_ids[0], "ui-implementation-workflow")


if __name__ == "__main__":
    unittest.main()
