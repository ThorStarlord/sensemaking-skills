"""Unit tests for the decentralized run ledger and validate-and-record wrapper.

Tests scripts/run-ledger.py, scripts/validate-and-record.py, and scripts/create-artifact.py.
"""

import os
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock
import json
import yaml
import subprocess

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

run_ledger = import_script("run_ledger", "run-ledger.py")
create_artifact = import_script("create_artifact", "create-artifact.py")
validate_and_record = import_script("validate_and_record", "validate-and-record.py")


class TestRunLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo_root = self.tmp
        self.ledger_path = os.path.join(self.tmp, "artifacts", "test-run", "run-ledger.jsonl")
        
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
                }
            ]
        }
        self.contracts_path = os.path.join(self.planner_ref_dir, "artifact-contracts.yaml")
        with open(self.contracts_path, "w", encoding="utf-8") as f:
            yaml.dump(self.contracts, f)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read_ledger(self):
        events = []
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line.strip()))
        return events

    def test_start_run(self):
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "start-run",
            "--run-id", "run-123",
            "--workflow", "fast-local-diagnostic",
            "--mode", "yolo_execution"
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        events = self.read_ledger()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "run_started")
        self.assertEqual(events[0]["run_id"], "run-123")
        self.assertEqual(events[0]["workflow_id"], "fast-local-diagnostic")
        self.assertEqual(events[0]["mode"], "yolo_execution")
        self.assertIn("git_commit", events[0])

    def test_start_step_and_hashing(self):
        # Create a dummy input file
        input_path = os.path.join(self.tmp, "input.md")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write("Some input context")
            
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "start-step",
            "--step-id", "01",
            "--skill-id", "problem-framer",
            "--inputs", input_path
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        events = self.read_ledger()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "step_started")
        self.assertEqual(events[0]["step_id"], "01")
        self.assertEqual(events[0]["skill_id"], "problem-framer")
        self.assertEqual(len(events[0]["inputs"]), 1)
        self.assertEqual(events[0]["inputs"][0]["path"], "input.md")
        self.assertEqual(len(events[0]["inputs"][0]["hash"]), 64)  # Valid SHA-256

    def test_record_artifact(self):
        art_path = os.path.join(self.tmp, "art.md")
        with open(art_path, "w", encoding="utf-8") as f:
            f.write("Output artifact content")
            
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "record-artifact",
            "--step-id", "01",
            "--artifact-id", "mock_artifact_1",
            "--path", art_path
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        events = self.read_ledger()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "artifact_created")
        self.assertEqual(events[0]["step_id"], "01")
        self.assertEqual(events[0]["artifact_id"], "mock_artifact_1")
        self.assertEqual(events[0]["path"], "art.md")
        self.assertEqual(len(events[0]["hash"]), 64)

    def test_record_validation(self):
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "record-validation",
            "--step-id", "01",
            "--artifact-id", "mock_artifact_1",
            "--command", "python scripts/validate-output.py mock_artifact_1 art.md",
            "--exit-code", "0",
            "--status", "passed"
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        events = self.read_ledger()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "validation_completed")
        self.assertEqual(events[0]["step_id"], "01")
        self.assertEqual(events[0]["artifact_id"], "mock_artifact_1")
        self.assertEqual(events[0]["exit_code"], 0)
        self.assertEqual(events[0]["status"], "passed")

    def test_complete_step(self):
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "complete-step",
            "--step-id", "01",
            "--status", "completed",
            "--gate-status", "approved"
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        events = self.read_ledger()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "step_completed")
        self.assertEqual(events[0]["step_id"], "01")
        self.assertEqual(events[0]["status"], "completed")
        self.assertEqual(events[0]["gate_status"], "approved")

    def test_finalize_run_mode_coverage(self):
        # Create a mock docs/mode-coverage.yaml
        docs_dir = os.path.join(self.repo_root, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        coverage_path = os.path.join(docs_dir, "mode-coverage.yaml")
        
        initial_coverage = {
            "mode_coverage": [],
            "system_tools": [],
            "orchestration_runner": {}
        }
        with open(coverage_path, "w", encoding="utf-8") as f:
            yaml.dump(initial_coverage, f)
            
        # Write dummy ledger events to ledger path
        events = [
            {"event": "run_started", "run_id": "run-xyz", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "abc1234", "timestamp": "2026-05-22T20:00:00Z"},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": "2026-05-22T20:01:00Z"},
            {"event": "artifact_created", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "path": "artifacts/run-xyz/01-brief.md", "hash": "abc", "timestamp": "2026-05-22T20:01:30Z"},
            {"event": "validation_completed", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "validator_command": "python scripts/validate-brief.py brief.md", "exit_code": 0, "status": "passed", "timestamp": "2026-05-22T20:02:00Z"},
            {"event": "step_completed", "step_id": "01", "status": "completed", "gate_status": "approved", "timestamp": "2026-05-22T20:02:30Z"}
        ]
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e) + "\n")
                
        argv = [
            "run-ledger.py",
            "--repo-root", self.repo_root,
            "--ledger-path", self.ledger_path,
            "finalize-run",
            "--update-mode-coverage"
        ]
        with patch("sys.argv", argv):
            exit_code = run_ledger.main()
            self.assertEqual(exit_code, 0)
            
        with open(coverage_path, "r", encoding="utf-8") as f:
            coverage = yaml.safe_load(f)
            
        self.assertEqual(len(coverage["mode_coverage"]), 1)
        entry = coverage["mode_coverage"][0]
        self.assertEqual(entry["workflow_id"], "fast-local-diagnostic")
        self.assertEqual(entry["mode"], "guided_execution")
        self.assertEqual(entry["steps_completed"], 1)
        self.assertEqual(entry["steps_total"], 1)
        self.assertIn("level_3: validate-brief.py", entry["validators_exercised"])

    def test_validate_and_record(self):
        # Create a dummy artifact file
        art_path = os.path.join(self.tmp, "art.md")
        with open(art_path, "w", encoding="utf-8") as f:
            f.write("Output artifact content")
            
        # We need a validator mock or validate-output.py wrapper mock
        # Let's mock subprocess.run in validate-and-record selectively
        original_run = subprocess.run
        def mock_run_side_effect(cmd, *args, **kwargs):
            if len(cmd) > 1 and "validate-output.py" in str(cmd[1]):
                return MagicMock(returncode=0, stdout="Validation Passed", stderr="")
            return original_run(cmd, *args, **kwargs)

        with patch("subprocess.run", side_effect=mock_run_side_effect):
            argv = [
                "validate-and-record.py",
                "--repo-root", self.repo_root,
                "--ledger-path", self.ledger_path,
                "--step-id", "01",
                "--artifact-id", "mock_artifact_1",
                "--path", art_path
            ]
            with patch("sys.argv", argv):
                exit_code = validate_and_record.main()
                self.assertEqual(exit_code, 0)
                
        events = self.read_ledger()
        # Should record: 1) artifact_created, 2) validation_completed
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["event"], "artifact_created")
        self.assertEqual(events[1]["event"], "validation_completed")
        self.assertEqual(events[1]["exit_code"], 0)
        self.assertEqual(events[1]["status"], "passed")


if __name__ == "__main__":
    unittest.main()
