"""Orchestrator — imports OrchestrationRunner from the canonical runtime module.

This module re-exports the shared types and classes that both workflow-runner-agent
and workflow-runtime use. The actual OrchestrationRunner class lives in
workflow-runtime.py (the canonical source), and this module imports it to avoid
code duplication between the two runners.

Usage:
    from _orchestrator import OrchestrationRunner, KNOWN_MODES, list_workflows, ...
"""

import sys
import os as _os
import importlib.util as _importlib_util

_scripts_dir = _os.path.dirname(_os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# Load workflow-runtime.py via importlib since the hyphen prevents a normal import.
_spec = _importlib_util.spec_from_file_location(
    "workflow_runtime",
    _os.path.join(_scripts_dir, "workflow-runtime.py"),
)
_wr = _importlib_util.module_from_spec(_spec)
_spec.loader.exec_module(_wr)

# Re-export everything for thin runners
OrchestrationRunner = _wr.OrchestrationRunner
KNOWN_MODES = _wr.KNOWN_MODES
GATE_RESULTS = _wr.GATE_RESULTS
STATE_LADDER = _wr.STATE_LADDER
MODE_CEILINGS = _wr.MODE_CEILINGS
list_workflows = _wr.list_workflows
WORKFLOW_NOT_FOUND = _wr.WORKFLOW_NOT_FOUND
WORKFLOW_INVALID = _wr.WORKFLOW_INVALID
MODE_NOT_ALLOWED = _wr.MODE_NOT_ALLOWED
MISSING_INPUT = _wr.MISSING_INPUT
VALIDATOR_FAILED = _wr.VALIDATOR_FAILED
GATE_DENIED = _wr.GATE_DENIED
GATE_TIMEOUT = _wr.GATE_TIMEOUT
STEP_FAILED = _wr.STEP_FAILED
PREFLIGHT_FAILED = _wr.PREFLIGHT_FAILED
ARTIFACT_NOT_FOUND = _wr.ARTIFACT_NOT_FOUND

__all__ = [
    "OrchestrationRunner",
    "KNOWN_MODES",
    "GATE_RESULTS",
    "STATE_LADDER",
    "MODE_CEILINGS",
    "list_workflows",
    "WORKFLOW_NOT_FOUND",
    "WORKFLOW_INVALID",
    "MODE_NOT_ALLOWED",
    "MISSING_INPUT",
    "VALIDATOR_FAILED",
    "GATE_DENIED",
    "GATE_TIMEOUT",
    "STEP_FAILED",
    "PREFLIGHT_FAILED",
    "ARTIFACT_NOT_FOUND",
]
