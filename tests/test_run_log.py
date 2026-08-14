"""Tests for workflow-runtime.py write_run_log() state determination logic."""

import os
import sys
import importlib.util
from unittest.mock import patch, MagicMock

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Reuse the already-loaded module if another test file loaded it first, so all test
# files share one module object (clobbering sys.modules breaks @patch in sibling files).
if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime",
        os.path.join(scripts_dir, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _make_runner(mode, steps=None, step_results=None):
    runner = OrchestrationRunner.__new__(OrchestrationRunner)
    runner.mode = mode
    runner.workflow_id = "test-wf"
    runner.session_id = "session-1"
    runner.log_dir = "/tmp/logs"
    runner.repo_root = "/tmp/repo"
    runner.workflow = {
        "id": "test-wf",
        "display_name": "Test Workflow",
        "steps": steps or [{"skill": "s1"}, {"skill": "s2"}],
    }
    runner.step_results = step_results or []
    runner.gate_decisions = []
    runner.errors = []
    runner.final_state = "not_started"
    runner.final_note = ""
    return runner


def _step(status, step_id="1", skill="s1"):
    return {
        "step_id": step_id,
        "skill": skill,
        "status": status,
        "gate": "review",
        "output_artifact": "test",
        "artifact_path": "artifacts/test.md",
        "validator_stack": [],
        "gate_result": "approved_by_user",
    }


def test_run_log_failed_state():
    runner = _make_runner("guided_execution", step_results=[
        _step("EXECUTED", "1"),
        _step("FAILED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "failed"
    assert "failed" in runner.final_note


def test_run_log_paused_state():
    runner = _make_runner("guided_execution", step_results=[
        _step("EXECUTED", "1"),
        _step("PAUSED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "paused"
    assert "Paused" in runner.final_note


def test_run_log_plan_only_planned():
    runner = _make_runner("plan_only", steps=[{"skill": "s1"}, {"skill": "s2"}], step_results=[
        _step("PLANNED", "1"),
        _step("PLANNED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "planned"


def test_run_log_prompt_chain_generated():
    runner = _make_runner("prompt_chain", steps=[{"skill": "s1"}, {"skill": "s2"}], step_results=[
        _step("PROMPT_GENERATED", "1"),
        _step("PROMPT_GENERATED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "prompt_chain_generated"

def test_run_log_completed():
    runner = _make_runner("guided_execution", steps=[{"skill": "s1"}, {"skill": "s2"}], step_results=[
        _step("APPROVED", "1"),
        _step("APPROVED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "completed"


def test_run_log_partial():
    runner = _make_runner("guided_execution", steps=[{"skill": "s1"}, {"skill": "s2"}, {"skill": "s3"}], step_results=[
        _step("APPROVED", "1"),
        _step("EXECUTED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "partial"
    assert "2/3" in runner.final_note


def test_run_log_prefers_failed_over_paused():
    runner = _make_runner("guided_execution", step_results=[
        _step("FAILED", "1"),
        _step("PAUSED", "2"),
    ])
    with patch("os.makedirs"), patch("builtins.open", MagicMock()):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    assert runner.final_state == "failed"


def test_run_log_runtime_strings():
    # 1. use_fixtures should write "fixture"
    runner = _make_runner("guided_execution", step_results=[_step("APPROVED", "1")])
    runner.use_fixtures = True
    runner.executor = "dry-run"
    
    mock_open = MagicMock()
    with patch("os.makedirs"), patch("builtins.open", mock_open):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    
    written_data = "".join(call.args[0] for call in mock_open.return_value.__enter__.return_value.write.call_args_list)
    assert "- **runtime**: fixture" in written_data

    # 2. plan_only should write "planning"
    runner = _make_runner("plan_only", step_results=[_step("PLANNED", "1")])
    runner.use_fixtures = False
    runner.executor = "dry-run"
    
    mock_open = MagicMock()
    with patch("os.makedirs"), patch("builtins.open", mock_open):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    
    written_data = "".join(call.args[0] for call in mock_open.return_value.__enter__.return_value.write.call_args_list)
    assert "- **runtime**: planning" in written_data

    # 3. guided_execution with dry-run should write "dry-run"
    runner = _make_runner("guided_execution", step_results=[_step("APPROVED", "1")])
    runner.use_fixtures = False
    runner.executor = "dry-run"
    
    mock_open = MagicMock()
    with patch("os.makedirs"), patch("builtins.open", mock_open):
        with patch("workflow_runtime._get_git_branch", return_value="main"):
            with patch("workflow_runtime._check_clean_git", return_value=(True, "")):
                runner.write_run_log()
    
    written_data = "".join(call.args[0] for call in mock_open.return_value.__enter__.return_value.write.call_args_list)
    assert "- **runtime**: dry-run" in written_data
