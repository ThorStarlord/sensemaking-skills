"""Unit tests for the decentralized run ledger and handoff utilities.

Tests create-artifact.py, record-step.py, and finalize-run.py.
"""

import os
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock
import yaml
import datetime

# Setup scripts path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import importlib.util

def import_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(scripts_dir, filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

create_artifact = import_script("create_artifact", "create-artifact.py")
record_step = import_script("record_step", "record-step.py")
finalize_run = import_script("finalize_run", "finalize-run.py")


class TestLedgerSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo_root = self.tmp
        
        # Setup mock directories for artifact-contracts.yaml
        self.planner_ref_dir = os.path.join(self.repo_root, "skills", "workflow-planner", "references")
        os.makedirs(self.planner_ref_dir, exist_ok=True)
        
        # Setup dummy artifact contracts
        self.contracts = {
            "artifacts": [
                {
                    "id": "mock_artifact_1",
                    "path": "artifacts/mock_artifact_1.md",
                    "produced_by": "mock-skill",
                    "required_sections": ["overview", "details"],
                    "required_machine_fields": ["artifact_id", "source_intent_ref", "created_at"]
                },
                {
                    "id": "mock_artifact_2",
                    "path": "artifacts/mock_artifact_2.md",
                    "produced_by": "mock-skill",
                    "required_sections": ["summary"],
                    "required_machine_fields": ["artifact_id", "source_intent_ref", "status"]
                }
            ]
        }
        self.contracts_path = os.path.join(self.planner_ref_dir, "artifact-contracts.yaml")
        with open(self.contracts_path, "w", encoding="utf-8") as f:
            yaml.dump(self.contracts, f)

        # Setup mock skill references for template loading
        self.skill_ref_dir = os.path.join(self.repo_root, "skills", "mock-skill", "references")
        os.makedirs(self.skill_ref_dir, exist_ok=True)
        self.template_path = os.path.join(self.skill_ref_dir, "mock-artifact-1-template.md")
        with open(self.template_path, "w", encoding="utf-8") as f:
            f.write("# Mock Artifact 1 Title\n\n## Overview\nTemplate overview content.\n\n## Details\nTemplate details content.\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # 1. Test create-artifact.py
    def test_create_artifact_from_template(self):
        out_path = os.path.join(self.tmp, "artifacts", "mock_artifact_1.md")
        test_argv = [
            "create-artifact.py",
            "--artifact-id", "mock_artifact_1",
            "--path", out_path,
            "--intent-ref", "user_intent_ref.md",
            "--repo-root", self.repo_root
        ]
        with patch("sys.argv", test_argv):
            exit_code = create_artifact.main()
            self.assertEqual(exit_code, 0)
            
        self.assertTrue(os.path.exists(out_path))
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verify content matches template
        self.assertIn("# Mock Artifact 1 Title", content)
        self.assertIn("Template overview content.", content)
        
        # Verify YAML block injection
        yaml_blocks = re_get_yaml_blocks(content)
        self.assertEqual(len(yaml_blocks), 1)
        meta = yaml_blocks[0]
        self.assertEqual(meta.get("artifact_id"), "mock_artifact_1")
        self.assertEqual(meta.get("source_intent_ref"), "user_intent_ref.md")
        self.assertIn("created_at", meta)

    def test_create_artifact_skeleton_fallback(self):
        out_path = os.path.join(self.tmp, "artifacts", "mock_artifact_2.md")
        test_argv = [
            "create-artifact.py",
            "--artifact-id", "mock_artifact_2",
            "--path", out_path,
            "--intent-ref", "user_intent_ref.md",
            "--repo-root", self.repo_root
        ]
        # No template is provided for mock_artifact_2, so it should fallback to skeleton
        with patch("sys.argv", test_argv):
            exit_code = create_artifact.main()
            self.assertEqual(exit_code, 0)
            
        self.assertTrue(os.path.exists(out_path))
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verify generated skeleton sections
        self.assertIn("# Mock Artifact 2", content)
        self.assertIn("## Summary", content)
        
        # Verify YAML block injection
        yaml_blocks = re_get_yaml_blocks(content)
        self.assertEqual(len(yaml_blocks), 1)
        meta = yaml_blocks[0]
        self.assertEqual(meta.get("artifact_id"), "mock_artifact_2")
        self.assertEqual(meta.get("source_intent_ref"), "user_intent_ref.md")
        self.assertEqual(meta.get("status"), "draft")

    # 2. Test record-step.py
    def test_record_step_lifecycle(self):
        ledger_path = os.path.join(self.tmp, "runs", "run_ledger.yaml")
        input_file = os.path.join(self.tmp, "input_doc.txt")
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("Input file content for hashing")
            
        # Call start command
        start_argv = [
            "record-step.py",
            "--repo-root", self.repo_root,
            "--ledger-path", ledger_path,
            "--step-id", "step-1-analysis",
            "start",
            "--run-id", "test-run-123",
            "--skill-id", "analyzer-skill",
            "--input-artifacts", input_file,
            "--git-commit", "git-sha-test-abc",
            "--workflow-id", "test-workflow",
            "--mode", "guided_execution"
        ]
        with patch("sys.argv", start_argv):
            exit_code = record_step.main()
            self.assertEqual(exit_code, 0)
            
        self.assertTrue(os.path.exists(ledger_path))
        ledger = load_yaml_file(ledger_path)
        
        # Check run_metadata initialization
        meta = ledger.get("run_metadata", {})
        self.assertEqual(meta.get("run_id"), "test-run-123")
        self.assertEqual(meta.get("git_commit"), "git-sha-test-abc")
        self.assertEqual(meta.get("workflow_id"), "test-workflow")
        self.assertEqual(meta.get("mode"), "guided_execution")
        self.assertEqual(meta.get("status"), "started")
        
        # Check step status
        steps = ledger.get("steps", [])
        self.assertEqual(len(steps), 1)
        step = steps[0]
        self.assertEqual(step.get("step_id"), "step-1-analysis")
        self.assertEqual(step.get("skill_id"), "analyzer-skill")
        self.assertEqual(step.get("status"), "started")
        self.assertEqual(len(step.get("inputs", [])), 1)
        self.assertEqual(step["inputs"][0]["path"], "input_doc.txt")
        self.assertIsNotNone(step["inputs"][0]["hash"])
        self.assertNotEqual(step["inputs"][0]["hash"], "file_not_found")

        # Simulate producing output and calling complete command
        output_file = os.path.join(self.tmp, "output_doc.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Output file content for hashing")
            
        complete_argv = [
            "record-step.py",
            "--repo-root", self.repo_root,
            "--ledger-path", ledger_path,
            "--step-id", "step-1-analysis",
            "complete",
            "--output-artifact", output_file,
            "--validator-command", "python scripts/validate-artifact.py mock_artifact_1 output_doc.txt",
            "--validator-exit-code", "0",
            "--status", "passed",
            "--gate-status", "approved"
        ]
        with patch("sys.argv", complete_argv):
            exit_code = record_step.main()
            self.assertEqual(exit_code, 0)
            
        # Reload and check updated step complete facts
        ledger = load_yaml_file(ledger_path)
        step = ledger["steps"][0]
        self.assertEqual(step.get("status"), "passed")
        self.assertEqual(step.get("gate_status"), "approved")
        self.assertEqual(step.get("validator_exit_code"), 0)
        self.assertEqual(step.get("validator_command"), "python scripts/validate-artifact.py mock_artifact_1 output_doc.txt")
        self.assertEqual(len(step.get("outputs", [])), 1)
        self.assertEqual(step["outputs"][0]["path"], "output_doc.txt")
        self.assertIsNotNone(step["outputs"][0]["hash"])
        self.assertNotEqual(step["outputs"][0]["hash"], "file_not_found")

    # 3. Test finalize-run.py
    def test_finalize_run_completion_status(self):
        ledger_path = os.path.join(self.tmp, "run_ledger.yaml")
        
        # Scenario A: All steps passed
        ledger_data = {
            "run_metadata": {
                "run_id": "run-abc",
                "status": "started"
            },
            "steps": [
                {"step_id": "s1", "status": "passed"},
                {"step_id": "s2", "status": "skipped"}
            ]
        }
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f)
            
        finalize_argv = ["finalize-run.py", "--ledger-path", ledger_path, "--repo-root", self.repo_root]
        with patch("sys.argv", finalize_argv):
            exit_code = finalize_run.main()
            self.assertEqual(exit_code, 0)
            
        ledger = load_yaml_file(ledger_path)
        self.assertEqual(ledger["run_metadata"]["status"], "completed")
        self.assertIn("timestamp_end", ledger["run_metadata"])

        # Scenario B: One step failed
        ledger_data["steps"][1]["status"] = "failed"
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f)
            
        with patch("sys.argv", finalize_argv):
            exit_code = finalize_run.main()
            self.assertEqual(exit_code, 0)
            
        ledger = load_yaml_file(ledger_path)
        self.assertEqual(ledger["run_metadata"]["status"], "failed")

        # Scenario C: Step in progress/started
        ledger_data["steps"][1]["status"] = "started"
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f)
            
        with patch("sys.argv", finalize_argv):
            exit_code = finalize_run.main()
            self.assertEqual(exit_code, 0)
            
        ledger = load_yaml_file(ledger_path)
        self.assertEqual(ledger["run_metadata"]["status"], "partial")

    def test_finalize_run_mode_coverage_integration(self):
        ledger_path = os.path.join(self.tmp, "run_ledger.yaml")
        ledger_data = {
            "run_metadata": {
                "run_id": "run-xyz-987",
                "workflow_id": "fast-local-diagnostic",
                "mode": "guided_execution",
                "status": "started"
            },
            "steps": [
                {
                    "step_id": "step1",
                    "status": "passed",
                    "validator_command": "python scripts/validate-artifact.py repository_sensemaking_brief brief.md",
                    "gate_status": "approved"
                },
                {
                    "step_id": "step2",
                    "status": "passed",
                    "validator_command": "python scripts/validate-brief.py brief.md",
                    "gate_status": "approved"
                }
            ]
        }
        with open(ledger_path, "w", encoding="utf-8") as f:
            yaml.dump(ledger_data, f)
            
        # Create a mock mode-coverage.yaml
        coverage_dir = os.path.join(self.repo_root, "docs")
        os.makedirs(coverage_dir, exist_ok=True)
        coverage_path = os.path.join(coverage_dir, "mode-coverage.yaml")
        
        initial_coverage = {
            "mode_coverage": [],
            "system_tools": [],
            "orchestration_runner": {}
        }
        with open(coverage_path, "w", encoding="utf-8") as f:
            yaml.dump(initial_coverage, f)
            
        finalize_argv = [
            "finalize-run.py",
            "--ledger-path", ledger_path,
            "--repo-root", self.repo_root,
            "--update-mode-coverage"
        ]
        with patch("sys.argv", finalize_argv):
            exit_code = finalize_run.main()
            self.assertEqual(exit_code, 0)
            
        # Verify mode-coverage.yaml was updated correctly
        coverage = load_yaml_file(coverage_path)
        
        # Verify entry in mode_coverage list
        self.assertEqual(len(coverage["mode_coverage"]), 1)
        entry = coverage["mode_coverage"][0]
        self.assertEqual(entry["workflow_id"], "fast-local-diagnostic")
        self.assertEqual(entry["mode"], "guided_execution")
        self.assertEqual(entry["steps_completed"], 2)
        self.assertEqual(entry["steps_total"], 2)
        
        # Verify validators list matches (validate-artifact.py and validate-brief.py parsed correctly)
        expected_validators = ["level_1: validate-repo.py", "level_2: validate-artifact.py", "level_3: validate-brief.py"]
        for val in expected_validators:
            self.assertIn(val, entry["validators_exercised"])
            
        # Verify gates info
        self.assertTrue(entry["gates_exercised"])
        self.assertEqual(entry["gates_note"], "2 approved, 0 denied")
        
        # Verify system_tools update
        runner_tool = next((t for t in coverage["system_tools"] if t.get("tool") == "orchestration-runner.py"), None)
        self.assertIsNotNone(runner_tool)
        self.assertIn("fast-local-diagnostic (guided_execution)", runner_tool["workflows_executed"])
        self.assertEqual(runner_tool["last_session"], "run-xyz-987")
        
        # Verify orchestration_runner overall sections
        runner_sec = coverage["orchestration_runner"]
        self.assertEqual(runner_sec["total_workflow_families"], 1)
        self.assertIn("fast-local-diagnostic", runner_sec["workflow_families_proven"])


def re_get_yaml_blocks(content: str) -> list:
    import re
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    return [yaml.safe_load(b) for b in blocks]


def load_yaml_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    unittest.main()
