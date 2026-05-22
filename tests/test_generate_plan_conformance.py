"""The runtime's generate_plan() must produce a contract-conformant
workflow_orchestration_plan (ADR 0010 / runtime-canonical plan authoring).

Before this was enforced, generate_plan() emitted ~4 of 11 required sections and
omitted 5 of 21 machine fields, so the runtime's own plan failed both
validate-artifact.py and validate-plan.py. The step-5 workflow-planner SDK then
clobbered it with non-conformant output. These tests lock the runtime's plan to
the full contract for both a conditional workflow and a simple one.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import importlib.util
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
scripts_dir = os.path.join(REPO_ROOT, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(scripts_dir, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _run(validator, artifact_id, plan_path):
    """Run a validator script; return (ok, combined_output)."""
    if validator == "validate-artifact.py":
        cmd = [sys.executable, os.path.join(scripts_dir, validator), artifact_id, plan_path, "--repo-root", REPO_ROOT]
    else:
        cmd = [sys.executable, os.path.join(scripts_dir, validator), plan_path, "--repo-root", REPO_ROOT]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, (res.stdout + res.stderr)


class TestGeneratePlanConformance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _generate(self, workflow_id, mode="guided_execution"):
        runner = OrchestrationRunner(
            workflow_id=workflow_id, mode=mode, repo_root=REPO_ROOT, executor="dry-run"
        )
        # Fail fast if the workflow didn't load (keeps the assertion meaningful).
        self.assertTrue(runner.workflow, f"workflow '{workflow_id}' not loaded: {runner.errors}")
        runner.session_id = "test-session-0001"
        runner.plan_out = os.path.join(self.tmp, f"plan_{workflow_id}.md")
        runner.generate_plan()
        return runner.plan_out

    def _assert_conformant(self, workflow_id):
        plan_path = self._generate(workflow_id)
        ok_generic, out_generic = _run("validate-artifact.py", "workflow_orchestration_plan", plan_path)
        self.assertTrue(ok_generic, f"validate-artifact.py failed for {workflow_id}:\n{out_generic}")
        ok_plan, out_plan = _run("validate-plan.py", "workflow_orchestration_plan", plan_path)
        self.assertTrue(ok_plan, f"validate-plan.py failed for {workflow_id}:\n{out_plan}")

    def test_conditional_workflow_plan_is_conformant(self):
        """full-local-sensemaking has a conditional step (3-conditional)."""
        self._assert_conformant("full-local-sensemaking")

    def test_simple_workflow_plan_is_conformant(self):
        """fast-local-diagnostic is a simple 2-step workflow (no conditional)."""
        self._assert_conformant("fast-local-diagnostic")


if __name__ == "__main__":
    unittest.main()
