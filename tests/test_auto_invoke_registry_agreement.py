"""Current/compatibility workflow auto-invocation boundary.

Active workflows must not advertise automatic downstream execution. Historical
compatibility workflows may retain auto-invocation metadata solely so old
records remain reconstructible; liveness keeps those entries out of current
selection/execution surfaces.
"""

import os
import unittest

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_COPIES = [
    (
        "skills/workflow-planner/references/workflow-registry.yaml",
        "skills/workflow-planner/references/workflow-liveness.yaml",
    ),
    (
        "src/sensemaking_skills/defaults/workflow-registry.yaml",
        "src/sensemaking_skills/defaults/workflow-liveness.yaml",
    ),
]


class TestAutoInvokeRegistryAgreement(unittest.TestCase):
    def _load(self, rel):
        with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _effective_liveness(self, workflow_id, overlay):
        return overlay.get("overrides", {}).get(
            workflow_id, overlay.get("default_liveness", "active")
        )

    def test_active_workflows_have_no_auto_execution_metadata(self):
        for registry_rel, liveness_rel in REGISTRY_COPIES:
            registry = self._load(registry_rel)
            overlay = self._load(liveness_rel)
            offenders = []
            for workflow in registry.get("workflows", []):
                if self._effective_liveness(workflow["id"], overlay) != "active":
                    continue
                if any(
                    key in workflow
                    for key in (
                        "auto_invoke_next_workflow",
                        "auto_invoke_source",
                        "auto_invoke_next_workflow_id",
                    )
                ):
                    offenders.append(workflow["id"])
            self.assertEqual(
                offenders,
                [],
                f"{registry_rel} active workflows must return recommendations to the active agent",
            )

    def test_retained_auto_invoke_metadata_is_compatibility_only(self):
        sets = []
        for registry_rel, liveness_rel in REGISTRY_COPIES:
            registry = self._load(registry_rel)
            overlay = self._load(liveness_rel)
            retained = {
                workflow["id"]
                for workflow in registry.get("workflows", [])
                if workflow.get("auto_invoke_next_workflow") is True
            }
            for workflow_id in retained:
                self.assertEqual(
                    self._effective_liveness(workflow_id, overlay),
                    "compatibility_only",
                    f"{workflow_id} may retain auto-invoke metadata only as compatibility history",
                )
            sets.append(retained)
        self.assertEqual(
            sets[0],
            sets[1],
            "registry copies must agree on retained compatibility auto-invoke identities",
        )

    def test_ui_diagnostic_historical_explicit_next_agrees(self):
        next_ids = []
        for registry_rel, _ in REGISTRY_COPIES:
            registry = self._load(registry_rel)
            workflow = next(
                workflow
                for workflow in registry.get("workflows", [])
                if workflow.get("id") == "ui-diagnostic-workflow"
            )
            next_ids.append(workflow.get("auto_invoke_next_workflow_id"))
        self.assertEqual(next_ids[0], next_ids[1])
        self.assertEqual(next_ids[0], "ui-implementation-workflow")


if __name__ == "__main__":
    unittest.main()
