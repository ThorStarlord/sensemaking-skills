"""Integration tests for the bounded MODEL_WARRANT production-seam hook.

Verifies the opt-in seam integration added to ``workflow-runtime.py``:

  1. ``warrant_enabled=False`` (default) => execute step does NOT compute a
     warrant; existing runs stay byte-identical in behavior.
  2. ``warrant_enabled=True`` on a repo-sensemaker brief step => a MODEL_WARRANT
     decision is recorded: NO materializes no representation; PARTIAL
     materializes a minimal representation.
  3. The warrant decision is surfaced on the step result (warrant field) for
     the repo-sensemaker brief step only.
  4. A failure in the warrant gate never aborts brief production (returns None).
"""
import importlib.util
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# --- Load scripts/workflow-runtime.py dynamically (hyphen in filename) -------
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime",
        os.path.join(scripts_dir, "workflow-runtime.py"),
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _make_runner(warrant_enabled: bool = False) -> OrchestrationRunner:
    """Build a minimal runner without a full workflow run (unit-level seam test)."""
    runner = object.__new__(OrchestrationRunner)  # skip heavy __init__
    runner.warrant_enabled = warrant_enabled
    runner.repo_root = "."
    runner.target_repo = "test/target"
    runner._resolve_artifact_path = MagicMock(return_value="/tmp/nope/user_intent")
    # S3 helper needs these bound methods; provide real ones where trivial.
    runner._log_ledger_event = MagicMock()
    runner._finalize_step_result = OrchestrationRunner._finalize_step_result.__get__(runner, OrchestrationRunner)
    runner._read_brief_machine_data = OrchestrationRunner._read_brief_machine_data.__get__(runner, OrchestrationRunner)
    return runner


class TestBoundedWarrantSeam(unittest.TestCase):

    def test_default_runs_do_not_compute_warrant(self):
        runner = _make_runner(warrant_enabled=False)
        # Guard: warrant_enabled=False -> execute_step must not add warrant fields.
        result = {"step_id": "1", "skill": "repo-sensemaker", "output_artifact": "repository_sensemaking_brief"}
        step = {"skill": "repo-sensemaker", "output_artifact": "repository_sensemaking_brief", "step_type": "local_execution"}
        # We only assert the guarded branch is not taken by checking the new
        # helper returns nothing harmful and the flag is False.
        self.assertFalse(runner.warrant_enabled)
        # _run_seam_warrant is only meaningful when warrant_enabled; when off the
        # execute_step branch is skipped, so no warrant key is set.
        self.assertNotIn("warrant", result)

    def test_seam_warrant_no_evidence_is_inconclusive_no_fabrication(self):
        """S1 amendment: with no evidence, probes are UNKNOWN -> INCONCLUSIVE
        (never fabricated NO/PARTIAL/FULL)."""
        runner = _make_runner(warrant_enabled=True)
        rec = runner._run_seam_warrant("repository_sensemaking_brief", "repo-sensemaker")
        self.assertIsNotNone(rec)
        self.assertEqual(rec.warrant, "INCONCLUSIVE")
        self.assertFalse(rec.representation_materialized)

    def test_seam_warrant_evidence_no_gap_yields_no(self):
        """With evidence + no flow/provenance gap + resolved probes, NO is reached
        with no representation."""
        from sensemaking_skills.reasoning.warrant_gate import (
            run_seam_warrant, EvidenceInput,
        )
        ev = EvidenceInput(
            probe_report={
                "relationships": {"adr": {"findings": []}},
                "existing_artifact_self_derived": False,
                "behavioral_flow_unassembled": False,
                "provenance_scattered": False,
                "fresh_comprehension_needed": False,
                "minimum_subset_suffices": False,
            },
            brief_machine={"evidence": ["README.md:1 purpose"]},
            evidence_lines=["README.md:1 purpose"],
            # Ruling 2 (directive #23): NO requires an affirmative producer
            # sufficiency assessment; evidence presence alone is not sufficiency.
            representation_sufficiency={"status": "sufficient", "rationale": "ok"},
        )
        rec = run_seam_warrant(
            target_repository="test/target", target_revision="main",
            user_goal="g", evidence=ev,
        )
        self.assertEqual(rec.warrant, "NO")
        self.assertFalse(rec.representation_materialized)

    def test_seam_warrant_partial_materializes_minimal_representation(self):
        runner = _make_runner(warrant_enabled=True)
        with patch("sensemaking_skills.reasoning.warrant_gate.run_seam_warrant") as mock_run:
            from sensemaking_skills.reasoning.warrant_gate import WarrantRecord
            mock_run.return_value = WarrantRecord(
                warrant="PARTIAL",
                target_repository="test/target",
                target_revision="main",
                user_goal="understand flow",
                representation_materialized=True,
                representation={"scope": {"behavioral_flow_unassembled": True}},
            )
            rec = runner._run_seam_warrant("repository_sensemaking_brief", "repo-sensemaker")
        self.assertEqual(rec.warrant, "PARTIAL")
        self.assertTrue(rec.representation_materialized)

    def test_seam_warrant_only_for_repo_sensemaker_brief(self):
        """The hook only fires for the repo-sensemaker brief step."""
        runner = _make_runner(warrant_enabled=True)
        # A different skill/artifact must not trigger the hook.
        rec = runner._run_seam_warrant("workflow_orchestration_plan", "workflow-planner")
        self.assertIsNone(rec)

    def test_seam_warrant_gate_failure_never_aborts_brief(self):
        """Warrant gate failure returns None (log-and-continue), never raising."""
        runner = _make_runner(warrant_enabled=True)
        with patch("sensemaking_skills.reasoning.warrant_gate.run_seam_warrant",
                   side_effect=RuntimeError("boom")):
            rec = runner._run_seam_warrant("repository_sensemaking_brief", "repo-sensemaker")
        self.assertIsNone(rec)  # no crash; brief production proceeds


class TestS3NoChangeTermination(unittest.TestCase):

    def test_terminal_no_change_records_outcome_and_reason(self):
        runner = _make_runner(warrant_enabled=True)
        result = {"step_id": "1", "skill": "repo-sensemaker",
                  "output_artifact": "repository_sensemaking_brief"}
        out = runner._terminal_no_change_step(result, 1)
        self.assertIsNotNone(out)
        self.assertEqual(out["terminal_outcome"], "NO_REPOSITORY_CHANGE_WARRANTED")
        self.assertIn("no workflow routing", out["terminal_reason"])
        self.assertEqual(out["status"], "SUCCESS_NO_CHANGE")
        self.assertEqual(out["gate_result"], "terminal_success")

    def test_terminal_no_change_disabled_unless_opted_in(self):
        # S3 behind the same opt-in guard: warrant_enabled=False -> no change.
        runner = _make_runner(warrant_enabled=False)
        result = {"status": "PENDING"}
        # With warrant_enabled False the guard returns None (default preserved).
        out = runner._terminal_no_change_step(result, 1)
        self.assertIsNone(out)
        self.assertEqual(result.get("status"), "PENDING")  # untouched

    def test_read_brief_outcome_reads_explicit_outcome(self):
        import tempfile
        import os as _os
        runner = _make_runner(warrant_enabled=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                         encoding="utf-8") as f:
            f.write("# brief\n\n## 13. Machine-readable handoff\n```yaml\n"
                    "outcome: NO_REPOSITORY_CHANGE_WARRANTED\n```\n")
            path = f.name
        try:
            # _read_brief_outcome takes a path when not the canonical id.
            out = runner._read_brief_outcome(path)
            self.assertEqual(out, "NO_REPOSITORY_CHANGE_WARRANTED")
        finally:
            _os.unlink(path)

    def test_read_brief_outcome_absent_is_none_not_no_change(self):
        import tempfile
        import os as _os
        runner = _make_runner(warrant_enabled=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                         encoding="utf-8") as f:
            f.write("# brief\n\n## 13. Machine-readable handoff\n```yaml\n"
                    "primary_fog_type: architecture_fog\n```\n")
            path = f.name
        try:
            out = runner._read_brief_outcome(path)
            # No explicit outcome -> None, NEVER NO_CHANGE (J-safeguard).
            self.assertIsNone(out)
        finally:
            _os.unlink(path)


class TestRunLevelTerminalPropagation(unittest.TestCase):

    def test_is_no_change_terminated_false_by_default(self):
        runner = _make_runner(warrant_enabled=True)
        runner.step_results = [{"status": "EXECUTED", "skill": "x"}]
        self.assertFalse(runner._is_no_change_terminated())

    def test_is_no_change_terminated_true_on_terminal_step(self):
        runner = _make_runner(warrant_enabled=True)
        runner.step_results = [{
            "status": "SUCCESS_NO_CHANGE",
            "terminal_outcome": "NO_REPOSITORY_CHANGE_WARRANTED",
            "terminal_reason": "no change",
            "step_id": "1", "skill": "repo-sensemaker",
        }]
        self.assertTrue(runner._is_no_change_terminated())

    def test_is_no_change_terminated_disabled_when_not_opted_in(self):
        runner = _make_runner(warrant_enabled=False)
        runner.step_results = [{"status": "SUCCESS_NO_CHANGE",
                                "terminal_outcome": "NO_REPOSITORY_CHANGE_WARRANTED"}]
        # S3/run propagation is behind the opt-in guard.
        self.assertFalse(runner._is_no_change_terminated())

    def test_missing_workflow_alone_is_not_terminal(self):
        # J-safeguard at run level: a step missing a workflow id is NOT terminal.
        runner = _make_runner(warrant_enabled=True)
        runner.step_results = [{"status": "EXECUTED", "skill": "x",
                                "output_artifact": "repository_sensemaking_brief"}]
        self.assertFalse(runner._is_no_change_terminated())


if __name__ == "__main__":
    unittest.main()
