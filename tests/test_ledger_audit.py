"""Unit tests for the ledger audit-run command in workflow-runtime.py.

Tests that audit-run detects tampering, sequence anomalies, validation failures,
and hash mismatches.
"""

import os
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch
import json
import datetime
import importlib.util

# Setup scripts path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

def import_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(scripts_dir, filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    workflow_runtime = import_script("workflow_runtime", "workflow-runtime.py")



class TestLedgerAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo_root = self.tmp
        self.ledger_path = os.path.join(self.tmp, "artifacts", "test-run", "run-ledger.jsonl")
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        
        # Create some default inputs and artifacts to work with
        self.input_relative = "artifacts/00-user-intent.md"
        self.input_abs = os.path.join(self.repo_root, self.input_relative)
        os.makedirs(os.path.dirname(self.input_abs), exist_ok=True)
        with open(self.input_abs, "w", encoding="utf-8") as f:
            f.write("Test Input intent content")

        self.input_hash = workflow_runtime._compute_file_hash(self.input_abs)

        self.artifact_relative = "artifacts/test-run/01-brief.md"
        self.artifact_abs = os.path.join(self.repo_root, self.artifact_relative)
        os.makedirs(os.path.dirname(self.artifact_abs), exist_ok=True)
        with open(self.artifact_abs, "w", encoding="utf-8") as f:
            f.write("Test brief content")

        self.artifact_hash = workflow_runtime._compute_file_hash(self.artifact_abs)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_ledger(self, events):
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e) + "\n")

    def run_audit(self):
        # We can construct argparse args to pass to handle_audit_run
        class Args:
            ledger_path = self.ledger_path
            repo_root = self.repo_root
        return workflow_runtime.handle_audit_run(Args())

    def test_valid_ledger_passes(self):
        t1 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + "Z"
        t2 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=4)).isoformat() + "Z"
        t3 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=3)).isoformat() + "Z"
        t4 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=2)).isoformat() + "Z"
        t5 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=1)).isoformat() + "Z"

        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [{"path": self.input_relative, "hash": self.input_hash}], "timestamp": t2},
            {"event": "artifact_created", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "path": self.artifact_relative, "hash": self.artifact_hash, "timestamp": t3},
            {"event": "validation_completed", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "validator_command": "python scripts/validate-brief.py brief.md", "exit_code": 0, "status": "passed", "timestamp": t4},
            {"event": "step_completed", "step_id": "01", "status": "completed", "gate_status": "approved", "timestamp": t5},
            {"event": "run_completed", "run_id": "run-123", "status": "completed", "timestamp": t5}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 0)

    def test_missing_first_event_fails(self):
        t2 = datetime.datetime.utcnow().isoformat() + "Z"
        events = [
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t2}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_git_commit_invalid_format_fails(self):
        t1 = datetime.datetime.utcnow().isoformat() + "Z"
        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "invalid_sha", "timestamp": t1}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_duplicate_step_started_fails(self):
        t1 = datetime.datetime.utcnow().isoformat() + "Z"
        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t1}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_missing_input_file_fails(self):
        t1 = datetime.datetime.utcnow().isoformat() + "Z"
        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [{"path": "non-existent-input.md", "hash": "abc"}], "timestamp": t1}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_input_hash_mismatch_fails(self):
        t1 = datetime.datetime.utcnow().isoformat() + "Z"
        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [{"path": self.input_relative, "hash": "wrong_hash"}], "timestamp": t1}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_artifact_hash_mismatch_fails(self):
        t1 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + "Z"
        t2 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=4)).isoformat() + "Z"
        t3 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=3)).isoformat() + "Z"

        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t2},
            {"event": "artifact_created", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "path": self.artifact_relative, "hash": "wrong_hash", "timestamp": t3}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_chronological_causality_violation_fails(self):
        t1 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + "Z"
        t2 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=2)).isoformat() + "Z" # start late
        t3 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=3)).isoformat() + "Z" # complete early!

        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t2},
            {"event": "step_completed", "step_id": "01", "status": "completed", "gate_status": "approved", "timestamp": t3}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_step_completed_without_validation_fails(self):
        t1 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + "Z"
        t2 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=4)).isoformat() + "Z"
        t3 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=3)).isoformat() + "Z"

        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t2},
            {"event": "step_completed", "step_id": "01", "status": "completed", "gate_status": "approved", "timestamp": t3}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)

    def test_step_completed_validation_failed_fails(self):
        t1 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + "Z"
        t2 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=4)).isoformat() + "Z"
        t3 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=3)).isoformat() + "Z"
        t4 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=2)).isoformat() + "Z"
        t5 = (datetime.datetime.utcnow() - datetime.timedelta(minutes=1)).isoformat() + "Z"

        events = [
            {"event": "run_started", "run_id": "run-123", "workflow_id": "fast-local-diagnostic", "mode": "guided_execution", "git_commit": "a" * 40, "timestamp": t1},
            {"event": "step_started", "step_id": "01", "skill_id": "repo-sensemaker", "inputs": [], "timestamp": t2},
            {"event": "artifact_created", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "path": self.artifact_relative, "hash": self.artifact_hash, "timestamp": t3},
            {"event": "validation_completed", "step_id": "01", "artifact_id": "repository_sensemaking_brief", "validator_command": "python scripts/validate-brief.py brief.md", "exit_code": 1, "status": "failed", "timestamp": t4},
            {"event": "step_completed", "step_id": "01", "status": "completed", "gate_status": "approved", "timestamp": t5}
        ]
        self.write_ledger(events)
        self.assertEqual(self.run_audit(), 1)


if __name__ == "__main__":
    unittest.main()
