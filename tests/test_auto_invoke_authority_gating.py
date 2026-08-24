"""ADR 0026 authority-gating tests for the script runtime.

Prove that auto_invoke_next_workflow / recommended_workflow_id /
chosen_workflow_id / selected_workflow are compatibility metadata, NOT
execution authority (recommendation != selection != execution authorization;
knowable != authorized). The script runtime's Phase-7 auto-invocation consumer
must surface a candidate and NEVER spawn a child workflow absent a separate
explicit authority event.

Because no suitable explicit authority primitive exists in the product today,
_under ADR 0026_ the runtime FAILS CLOSED: it surfaces/logs the candidate and
does not spawn. These tests pin that behavior: a subprocess spawn attempt is
impossible and an observable candidate record is produced.
"""

import os
import sys
import unittest
import importlib.util

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


class TestAutoInvokeAuthorityGating(unittest.TestCase):
    """Script-runtime fail-closed auto-invocation behavior (ADR 0026)."""

    def _runner(self, workflow_id="fast-path-workflow", mode="autonomous_execution"):
        runner = OrchestrationRunner(
            workflow_id=workflow_id, mode=mode, repo_root=REPO_ROOT, executor="dry-run"
        )
        self.assertTrue(runner.workflow, f"workflow '{workflow_id}' not loaded: {runner.errors}")
        runner.session_id = "test-auth-0001"
        return runner

    def _assert_no_spawn(self, runner, candidate, source):
        """Run _surface_candidate_next_workflow and prove no subprocess spawn."""
        original_run_subprocess = workflow_runtime.run_subprocess

        def boom(*args, **kwargs):
            self.fail("FAIL: a subprocess child workflow was spawned (ADR 0026)")
        workflow_runtime.run_subprocess = boom
        try:
            code = runner._surface_candidate_next_workflow(candidate, source)
        finally:
            workflow_runtime.run_subprocess = original_run_subprocess
        self.assertEqual(code, 0, "fail-closed surfacing must return clean completion 0")

    def test_flag_alone_does_not_spawn(self):
        """auto_invoke_next_workflow: true alone must NOT cause a spawn (ADR 0026)."""
        # The runner loaded a workflow whose registry entry has
        # auto_invoke_next_workflow: true (fast-path-workflow). Surfacing a
        # candidate must never spawn, regardless of the flag.
        self._runner()
        # Even with the flag set, surfacing a candidate never spawns:
        self._assert_no_spawn(self._runner(), "product-implementation-workflow",
                              "workflow_orchestration_plan.recommended_workflow_id")

    def test_recommended_workflow_id_does_not_spawn(self):
        """A discoverable recommended_workflow_id must NOT cause a spawn."""
        self._assert_no_spawn(self._runner(), "product-implementation-workflow",
                              "workflow_orchestration_plan.recommended_workflow_id")

    def test_chosen_workflow_id_does_not_spawn(self):
        """A chosen_workflow_id must NOT cause a spawn."""
        self._assert_no_spawn(self._runner(), "product-implementation-workflow",
                              "workflow_orchestration_plan.chosen_workflow_id")

    def test_selected_workflow_does_not_spawn(self):
        """A selected_workflow must NOT cause a spawn."""
        self._assert_no_spawn(self._runner(), "product-implementation-workflow",
                              "workflow_orchestration_plan.selected_workflow")

    def test_explicit_next_id_ui_diagnostic_fails_closed(self):
        """The ui-diagnostic explicit next-id path must fail closed (ADR 0026).

        ui-diagnostic-workflow declares auto_invoke_next_workflow_id:
        ui-implementation-workflow. An explicit target is still NOT authority.
        """
        self._assert_no_spawn(self._runner("ui-diagnostic-workflow", "guided_execution"),
                              "ui-implementation-workflow", "ui_specification")

    def test_candidate_surfaced_with_reason_and_not_authorized_recorded(self):
        """Surfacing records candidate, source, reason, and 'execution not authorized'."""
        runner = self._runner()
        ledger_events = []
        original_log = runner._log_ledger_event

        def capture(event_data):
            ledger_events.append(event_data)
            return original_log(event_data)
        runner._log_ledger_event = capture

        code = runner._surface_candidate_next_workflow(
            "product-implementation-workflow", "workflow_orchestration_plan.recommended_workflow_id")
        self.assertEqual(code, 0)
        self.assertTrue(ledger_events, "expected a candidate-surfaced ledger event")
        ev = ledger_events[-1]
        self.assertEqual(ev.get("event"), "auto_invoke_candidate_surfaced")
        self.assertEqual(ev.get("candidate_workflow_id"), "product-implementation-workflow")
        self.assertEqual(ev.get("source_artifact"), "workflow_orchestration_plan.recommended_workflow_id")
        self.assertIs(ev.get("execution_authorized"), False)
        self.assertEqual(ev.get("reason"), "explicit authority event absent (ADR 0026)")

    def test_no_child_plan_written_on_surface(self):
        """Surfacing does NOT write/wire a child workflow execution plan."""
        runner = self._runner()
        plan_out_before = runner.plan_out
        # Mount a write trap on os.makedirs/open? The surfacing path must not
        # create a plan file (it returns without invoking workflow-runtime.py).
        # Simplest robust check: run_subprocess guard already covers the spawn;
        # also assert the run completes cleanly and no secondary plan path set.
        self.assertEqual(
            runner._surface_candidate_next_workflow(
                "product-implementation-workflow", "workflow_orchestration_plan"), 0)
        self.assertEqual(runner.plan_out, plan_out_before)


if __name__ == "__main__":
    unittest.main()
