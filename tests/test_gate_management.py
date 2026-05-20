"""Tests for workflow-runtime.py _manage_gate() across all 5 execution modes."""

import os
import sys
import importlib.util

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

spec = importlib.util.spec_from_file_location(
    "workflow_runtime",
    os.path.join(scripts_dir, "workflow-runtime.py")
)
workflow_runtime = importlib.util.module_from_spec(spec)
sys.modules["workflow_runtime"] = workflow_runtime
spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _make_runner(mode, gate_decision=None):
    runner = OrchestrationRunner.__new__(OrchestrationRunner)
    runner.mode = mode
    runner.gate_decision = gate_decision
    runner.gate_decisions = []
    runner.errors = []
    return runner


def test_plan_only_gate_not_applicable():
    runner = _make_runner("plan_only")
    result = runner._manage_gate("review", 1, "test-skill")
    assert result == "not_applicable"
    assert runner.gate_decisions[-1]["result"] == "not_applicable"
    assert runner.gate_decisions[-1]["mode"] == "plan_only"


def test_prompt_chain_gate_not_applicable():
    runner = _make_runner("prompt_chain")
    result = runner._manage_gate("review", 2, "test-skill")
    assert result == "not_applicable"
    assert runner.gate_decisions[-1]["result"] == "not_applicable"


def test_yolo_gate_bypassed():
    runner = _make_runner("yolo_execution")
    result = runner._manage_gate("review", 3, "test-skill")
    assert result == "bypassed"
    assert runner.gate_decisions[-1]["result"] == "bypassed"


def test_autonomous_gate_automated_approval():
    runner = _make_runner("autonomous_execution")
    result = runner._manage_gate("review", 4, "test-skill")
    assert result == "automated_approval"
    assert runner.gate_decisions[-1]["approved_by"] == "automated_gate"


def test_guided_gate_auto_approve():
    runner = _make_runner("guided_execution", "auto-approve")
    result = runner._manage_gate("review", 5, "test-skill")
    assert result == "approved_by_user"
    assert runner.gate_decisions[-1]["approved_by"] == "auto_gate"


def test_guided_gate_auto_deny():
    runner = _make_runner("guided_execution", "auto-deny")
    result = runner._manage_gate("review", 6, "test-skill")
    assert result == "denied_by_user"
    assert runner.gate_decisions[-1]["reason"] == "auto_denied_by_flag"


def test_guided_gate_no_tty_no_flag_returns_timed_out():
    import unittest.mock as mock
    runner = _make_runner("guided_execution")
    with mock.patch("sys.stdin.isatty", return_value=False):
        result = runner._manage_gate("review", 7, "test-skill")
    assert result == "timed_out"
    assert len(runner.errors) == 1
    assert "GATE_AUTO_FAILED" in runner.errors[0]
    assert "--gate-decision" in runner.errors[0]


def test_unknown_mode_defaults_to_not_applicable():
    """KNOWN_MODES.get(unknown, {}) returns {}; .get('gates', 'none') defaults to 'none'."""
    runner = _make_runner("nonexistent_mode")
    result = runner._manage_gate("review", 8, "test-skill")
    assert result == "not_applicable"


def test_gate_decision_records_step_and_gate_name():
    runner = _make_runner("yolo_execution")
    runner._manage_gate("my_gate", 99, "some-skill")
    entry = runner.gate_decisions[-1]
    assert entry["step"] == 99
    assert entry["gate"] == "my_gate"
    assert entry["mode"] == "yolo_execution"


def test_timestamp_is_iso_format():
    import re
    runner = _make_runner("yolo_execution")
    runner._manage_gate("review", 1, "test-skill")
    ts = runner.gate_decisions[-1]["timestamp"]
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", ts)


def test_gate_decision_mutates_gate_decisions_list():
    runner = _make_runner("plan_only")
    assert len(runner.gate_decisions) == 0
    runner._manage_gate("review", 1, "test-skill")
    assert len(runner.gate_decisions) == 1
    runner._manage_gate("deploy", 2, "other-skill")
    assert len(runner.gate_decisions) == 2
