"""Guardrail: machine-field names read by the runtime must exist in the contracts.

This test exists because of a real bug: the auto-invocation routing code read the
machine field `fog_type` (to validate workflow alignment) and `recommended_workflow_id`
(to pick the next workflow), but `fog_type` is declared in NO artifact contract and the
orchestration plan declares `chosen_workflow_id` / `selected_workflow` instead. The
validation silently no-op'd and routing could silently fail.

The repo's founding principle is "artifacts are the API between skills". Field names are
part of that API. This test enforces it at the code boundary: every candidate machine
field the runtime is willing to read must be declared as a required or recommended
machine field on at least one artifact in artifact-contracts.yaml.

If you add a new field-read alias to the runtime, add it to a contract too (or this
fails). If you rename a contract field, update the runtime alias list (or this fails).
"""

import os
import sys
import importlib.util

# Add scripts directory to sys.path so scripts can import _validator_utils
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from _validator_utils import load_artifact_contracts  # noqa: E402

# Load scripts/workflow-runtime.py dynamically due to the hyphen in the filename.
# Reuse the already-loaded module if a sibling test file loaded it first; clobbering
# sys.modules["workflow_runtime"] gives test files divergent module objects and breaks
# @patch("workflow_runtime.<x>") across files.
if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    _spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(SCRIPTS_DIR, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(_spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    _spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _declared_machine_fields() -> set[str]:
    """Collect every machine field name declared across all artifact contracts."""
    contracts = load_artifact_contracts(REPO_ROOT)
    assert contracts, "artifact-contracts.yaml could not be loaded"
    declared: set[str] = set()
    for artifact in contracts.get("artifacts", []):
        declared.update(artifact.get("required_machine_fields", []) or [])
        declared.update(artifact.get("recommended_machine_fields", []) or [])
    assert declared, "no machine fields declared in any artifact contract"
    return declared


def test_workflow_id_field_aliases_exist_in_contracts():
    """Every workflow-id field the runtime reads must be a declared contract field.

    Guards against the regression where the runtime read `recommended_workflow_id`
    but the orchestration plan only declared `chosen_workflow_id`/`selected_workflow`.
    """
    declared = _declared_machine_fields()
    missing = [f for f in OrchestrationRunner._WORKFLOW_ID_FIELDS if f not in declared]
    assert not missing, (
        f"Runtime reads workflow-id fields not declared in any artifact contract: {missing}. "
        f"Either add them to a contract's machine fields or remove them from "
        f"OrchestrationRunner._WORKFLOW_ID_FIELDS. Declared fields: {sorted(declared)}"
    )


def test_fog_type_field_aliases_exist_in_contracts():
    """Every fog-type field the runtime reads must be a declared contract field.

    Guards against the original bug: the runtime read `fog_type`, which exists in no
    contract (the brief declares `primary_fog_type` / `user_implied_fog_type`).
    """
    declared = _declared_machine_fields()
    missing = [f for f in OrchestrationRunner._FOG_TYPE_FIELDS if f not in declared]
    assert not missing, (
        f"Runtime reads fog-type fields not declared in any artifact contract: {missing}. "
        f"Either add them to a contract's machine fields or remove them from "
        f"OrchestrationRunner._FOG_TYPE_FIELDS. Declared fields: {sorted(declared)}"
    )


def test_candidate_field_lists_are_nonempty():
    """Sanity: the runtime must declare at least one candidate for each routing concept."""
    assert OrchestrationRunner._WORKFLOW_ID_FIELDS, "no workflow-id field candidates defined"
    assert OrchestrationRunner._FOG_TYPE_FIELDS, "no fog-type field candidates defined"
