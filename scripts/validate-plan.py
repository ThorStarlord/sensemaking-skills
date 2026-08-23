"""Specialized Level 3 validator for workflow-orchestration-plan artifacts."""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import format_error, load_workflow_registry, load_artifact_contracts, load_skill_registry

# Stable error codes
WORKFLOW_NOT_FOUND = "WORKFLOW_NOT_FOUND"
EXECUTION_MODE_DENIED = "EXECUTION_MODE_DENIED"
INPUT_MISMATCH = "INPUT_MISMATCH"
STEP_COUNT_MISMATCH = "STEP_COUNT_MISMATCH"
STEP_SKILL_MISMATCH = "STEP_SKILL_MISMATCH"
STEP_TYPE_MISMATCH = "STEP_TYPE_MISMATCH"
GATE_MISMATCH = "GATE_MISMATCH"
INPUT_ARTIFACT_MISMATCH = "INPUT_ARTIFACT_MISMATCH"
OUTPUT_ARTIFACT_MISMATCH = "OUTPUT_ARTIFACT_MISMATCH"
ARTIFACT_NOT_CONTRACTED = "ARTIFACT_NOT_CONTRACTED"
GATE_BEHAVIOR_MISSING = "GATE_BEHAVIOR_MISSING"
SIMULATED_GATE_CLASH = "SIMULATED_GATE_CLASH"
STOP_CONDITIONS_EMPTY = "STOP_CONDITIONS_EMPTY"
SUBSET_NOT_CONTIGUOUS = "SUBSET_NOT_CONTIGUOUS"
SECTION_11_MALFORMED = "SECTION_11_MALFORMED"
ABSOLUTE_PATH_DETECTED = "ABSOLUTE_PATH_DETECTED"
HALLUCINATED_SKILL = "HALLUCINATED_SKILL"
MISSING_DECISION_FIELD = "MISSING_DECISION_FIELD"
INVALID_CONDITIONAL_BRANCH = "INVALID_CONDITIONAL_BRANCH"
CONFLICT_NOT_ESCALATED = "CONFLICT_NOT_ESCALATED"


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str  # e.g., workflow_orchestration_plan.primary_fog_type.missing_field
    error_type: str  # missing_field, unknown_value, semantic_conflict, type_error, logic_error
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str


class ValidationResult(TypedDict):
    """Complete validation result with metadata."""
    valid: bool
    artifact_id: str
    artifact_path: str
    validator: str
    errors: list[ValidationError]
    validation_timestamp: str


def _code_error(code: str, message: str, field: str | None = None) -> ValidationError:
    """Build a ValidationError whose message is prefixed with a stable error code.

    Kept as a distinct helper (rather than reusing the Phase-1 field-check dict
    literals above) because these checks report a fixed vocabulary of codes
    (WORKFLOW_NOT_FOUND, GATE_MISMATCH, ...) cross-referenced against the
    workflow/skill/artifact registries, not simple field presence.
    """
    return {
        "error_type": "logic_error",
        "field": field,
        "current_value": None,
        "message": f"{code}: {message}",
        "suggested_fixes": [],
        "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
    }


def _validate_conditional_step(step, repo_root=".") -> list[ValidationError]:
    """Validate a conditional workflow step (decision_field + if_true/if_false branches)."""
    errors: list[ValidationError] = []

    decision_field = step.get("decision_field")
    if not decision_field:
        errors.append(_code_error(MISSING_DECISION_FIELD, f"Step {step.get('id')} missing 'decision_field'"))
        return errors

    skill_reg = load_skill_registry(repo_root)
    if skill_reg is None:
        errors.append(_code_error(WORKFLOW_NOT_FOUND, "Failed to load skill-registry.yaml"))
        return errors

    valid_skills = set()
    for ecosystem in skill_reg.get("ecosystems", {}).values():
        for skill in ecosystem.get("skills", []):
            valid_skills.add(skill["id"])

    for branch_name in ("if_true", "if_false"):
        branch = step.get(branch_name)
        if not branch:
            continue
        branch_skill = branch.get("skill")
        if branch_skill and branch_skill not in valid_skills:
            errors.append(
                _code_error(HALLUCINATED_SKILL, f"Step {step.get('id')} {branch_name} branch references non-existent skill '{branch_skill}'")
            )
        if not (branch_skill or branch.get("next_step")):
            errors.append(
                _code_error(INVALID_CONDITIONAL_BRANCH, f"Step {step.get('id')} {branch_name} branch must have either 'skill' or 'next_step'")
            )

    return errors


def _validate_plan_against_registries(plan_data: dict, repo_root: str = ".") -> list[ValidationError]:
    """Cross-reference plan machine fields against the workflow/skill/artifact registries.

    Ported from the pre-Phase-1 validator so that registry-grounded checks
    (workflow existence, step/gate/artifact alignment, escalation, stop
    conditions, etc.) still run in addition to the Phase-1 required-field
    checks in validate_plan(). Uses 'workflow_steps' (current contract field
    name) with a fallback to the legacy 'steps' key.
    """
    errors: list[ValidationError] = []

    workflow_reg = load_workflow_registry(repo_root)
    artifact_con = load_artifact_contracts(repo_root)
    skill_reg = load_skill_registry(repo_root)

    if workflow_reg is None or artifact_con is None or skill_reg is None:
        errors.append(_code_error(WORKFLOW_NOT_FOUND, "Failed to load one or more registries from workflow-planner references."))
        return errors

    chosen_id = plan_data.get("chosen_workflow_id")
    if not chosen_id:
        return errors  # Already reported as a missing_field by the Phase-1 check

    workflow = next((w for w in workflow_reg.get("workflows", []) if w["id"] == chosen_id), None)
    if not workflow:
        errors.append(_code_error(WORKFLOW_NOT_FOUND, f"chosen_workflow_id '{chosen_id}' not found in workflow-registry.yaml"))
        return errors

    # Path hygiene: no absolute paths anywhere in the machine-readable block
    yaml_dump = yaml.dump(plan_data)
    for pattern in (r"[a-zA-Z]:\\", r"/[Uu]sers/", r"/[Hh]ome/"):
        if re.search(pattern, yaml_dump):
            errors.append(_code_error(ABSOLUTE_PATH_DETECTED, f"Absolute path detected in YAML block (pattern: {pattern}). All paths must be relative."))

    # Execution mode
    exec_mode = plan_data.get("execution_mode")
    if exec_mode is not None and exec_mode not in workflow.get("allowed_execution_modes", []):
        errors.append(_code_error(EXECUTION_MODE_DENIED, f"execution_mode '{exec_mode}' not allowed for workflow '{chosen_id}'"))

    # Escalation
    escalation_recommended = plan_data.get("escalation_recommended", False)
    system_recommended = plan_data.get("system_recommended_workflow", "")
    if escalation_recommended and system_recommended != "full-fog-workflow":
        errors.append(
            _code_error(CONFLICT_NOT_ESCALATED,
                        f"escalation_recommended is true but system_recommended_workflow is '{system_recommended}', expected 'full-fog-workflow'")
        )

    # Initial inputs
    plan_inputs = plan_data.get("initial_inputs", [])
    reg_inputs = workflow.get("initial_inputs", [])
    if plan_inputs or reg_inputs:
        plan_input_ids = {i["id"] for i in plan_inputs}
        reg_input_ids = {i["id"] for i in reg_inputs}
        required_reg_input_ids = {
            i["id"] for i in reg_inputs if i.get("required", False)
        }
        # A plan must declare every REQUIRED registry input and must not
        # invent inputs; OPTIONAL registry inputs (required: false, e.g.
        # docs-contract-reconciliation's prior_evidence, issue #170) may be
        # omitted without failing validation.
        if required_reg_input_ids - plan_input_ids:
            errors.append(_code_error(
                INPUT_MISMATCH,
                f"initial_inputs mismatch: plan is missing required inputs "
                f"{sorted(required_reg_input_ids - plan_input_ids)}"))
        if plan_input_ids - reg_input_ids:
            errors.append(_code_error(
                INPUT_MISMATCH,
                f"initial_inputs mismatch: plan has unknown inputs "
                f"{sorted(plan_input_ids - reg_input_ids)}"))
        for i in plan_inputs:
            if "type" not in i or "required" not in i:
                errors.append(_code_error(INPUT_MISMATCH, f"Initial input '{i.get('id')}' missing 'type' or 'required' fields"))

    # Steps ('workflow_steps' is the current field name; 'steps' kept for back-compat)
    plan_steps = plan_data.get("workflow_steps")
    if plan_steps is None:
        plan_steps = plan_data.get("steps", [])
    if not isinstance(plan_steps, list):
        return errors  # Already reported as a type_error by the Phase-1 check

    reg_steps = workflow.get("steps", [])
    subset_run = plan_data.get("subset_run", False)

    if subset_run:
        if not plan_data.get("subset_reason"):
            errors.append(_code_error(SUBSET_NOT_CONTIGUOUS, "Missing 'subset_reason' for subset_run"))

        included_ids = plan_data.get("included_steps", [])
        excluded_data = plan_data.get("excluded_steps", [])
        excluded_ids = [s.get("id") for s in excluded_data]

        all_reg_ids = [s["id"] for s in reg_steps]
        all_plan_ids = set(included_ids) | set(excluded_ids)

        if set(all_reg_ids) != all_plan_ids:
            errors.append(_code_error(SUBSET_NOT_CONTIGUOUS, f"Subset mismatch: registry steps {all_reg_ids} not fully accounted for in plan ({all_plan_ids})"))

        if included_ids:
            try:
                first_idx = all_reg_ids.index(included_ids[0])
                last_idx = all_reg_ids.index(included_ids[-1])
                expected_subsequence = all_reg_ids[first_idx: last_idx + 1]
                if included_ids != expected_subsequence:
                    errors.append(_code_error(SUBSET_NOT_CONTIGUOUS, f"Non-contiguous subset: included_steps {included_ids} is not a contiguous sequence in workflow registry"))
            except ValueError as e:
                errors.append(_code_error(SUBSET_NOT_CONTIGUOUS, f"Step ID in included_steps not found in registry: {e}"))

        steps_to_validate = []
        for s_id in included_ids:
            p_step = next((s for s in plan_steps if s["id"] == s_id), None)
            r_step = next((s for s in reg_steps if s["id"] == s_id), None)
            if not p_step:
                errors.append(_code_error(SUBSET_NOT_CONTIGUOUS, f"Included step {s_id} missing from step list"))
            elif not r_step:
                errors.append(_code_error(WORKFLOW_NOT_FOUND, f"Included step {s_id} not found in registry"))
            else:
                steps_to_validate.append((p_step, r_step))
    else:
        if len(plan_steps) != len(reg_steps):
            errors.append(_code_error(STEP_COUNT_MISMATCH, f"Step count mismatch: plan has {len(plan_steps)}, registry expects {len(reg_steps)}"))
        steps_to_validate = list(zip(plan_steps, reg_steps))

    for p_step, r_step in steps_to_validate:
        s_id = p_step.get("id")
        if "status" not in p_step:
            errors.append(_code_error(SECTION_11_MALFORMED, f"Step {s_id} missing 'status'"))

        if p_step.get("conditional") and r_step.get("conditional"):
            errors.extend(_validate_conditional_step(p_step, repo_root))
            continue

        skill = p_step.get("skill")
        if skill != r_step.get("skill"):
            errors.append(_code_error(STEP_SKILL_MISMATCH, f"Step {s_id} skill mismatch: plan='{skill}', reg='{r_step.get('skill')}'"))

        s_type = p_step.get("step_type")
        if s_type != r_step.get("step_type"):
            errors.append(_code_error(STEP_TYPE_MISMATCH, f"Step {s_id} step_type mismatch: plan='{s_type}', reg='{r_step.get('step_type')}'"))

        gate = p_step.get("gate")
        if gate != r_step.get("gate"):
            errors.append(_code_error(GATE_MISMATCH, f"Step {s_id} gate mismatch: plan='{gate}', reg='{r_step.get('gate')}'"))

        p_in_src = p_step.get("input_source")
        r_in_src = r_step.get("input_source")
        if p_in_src != r_in_src:
            errors.append(_code_error(INPUT_ARTIFACT_MISMATCH, f"Step {s_id} input_source mismatch: plan='{p_in_src}', reg='{r_in_src}'"))

        p_in_art = p_step.get("input_artifact")
        r_in_art = r_step.get("input_artifact")
        if p_in_art != r_in_art:
            errors.append(_code_error(INPUT_ARTIFACT_MISMATCH, f"Step {s_id} input_artifact mismatch: plan='{p_in_art}', reg='{r_in_art}'"))

        p_out_art = p_step.get("output_artifact")
        r_out_art = r_step.get("output_artifact")
        if p_out_art != r_out_art:
            errors.append(_code_error(OUTPUT_ARTIFACT_MISMATCH, f"Step {s_id} output_artifact mismatch: plan='{p_out_art}', reg='{r_out_art}'"))

        if p_out_art:
            contract = next((a for a in artifact_con.get("artifacts", []) if a["id"] == p_out_art), None)
            if not contract:
                errors.append(_code_error(ARTIFACT_NOT_CONTRACTED, f"Step {s_id} output_artifact '{p_out_art}' not found in artifact-contracts.yaml"))
            else:
                skill_meta = None
                for ecosystem in skill_reg.get("ecosystems", {}).values():
                    skill_meta = next((s for s in ecosystem.get("skills", []) if s["id"] == skill), None)
                    if skill_meta:
                        break

                actual_producer = None
                if skill_meta and skill_meta.get("artifact") == p_out_art:
                    actual_producer = skill
                elif contract.get("produced_by") == skill:
                    actual_producer = skill

                if not actual_producer:
                    errors.append(_code_error(ARTIFACT_NOT_CONTRACTED, f"Step {s_id} skill '{skill}' is not contracted to produce '{p_out_art}'"))

    # Approval gates & behavior
    plan_gates = plan_data.get("approval_gates", [])
    step_gates = [s.get("gate") for s in plan_steps if s.get("gate")]
    if plan_gates != step_gates:
        errors.append(_code_error(GATE_MISMATCH, f"approval_gates mismatch: plan has {plan_gates}, steps have {step_gates}"))

    gate_behavior = plan_data.get("gate_behavior", {})
    for g in plan_gates:
        if g not in gate_behavior:
            errors.append(_code_error(GATE_BEHAVIOR_MISSING, f"Missing gate_behavior for gate '{g}'"))
        elif gate_behavior[g] == "simulated_for_research":
            for s in plan_steps:
                if s.get("gate") == g and s.get("approved_by_user") is True:
                    errors.append(_code_error(SIMULATED_GATE_CLASH, f"Gate clash: step {s.get('id')} claims 'approved_by_user: true' but gate '{g}' is simulated"))

    # Stop conditions
    stop_conds = plan_data.get("stop_conditions", [])
    if not stop_conds or not isinstance(stop_conds, list) or len(stop_conds) == 0:
        errors.append(_code_error(STOP_CONDITIONS_EMPTY, "stop_conditions missing or empty in Section 11/13"))

    return errors


def validate_plan(plan_path: str, repo_root: str = ".") -> list[ValidationError]:
    """Validate a workflow orchestration plan and return structured errors.

    Returns a list of ValidationError dicts. Empty list means validation passed.

    Phase 1 scope: Validate required fields only:
    - artifact_id
    - primary_fog_type
    - chosen_workflow_id
    - routing_decision_method
    - workflow_steps (non-empty array)
    - created_at
    """
    errors: list[ValidationError] = []

    # Check file exists
    if not os.path.exists(plan_path):
        errors.append({
            "error_type": "missing_field",
            "field": "artifact",
            "current_value": None,
            "message": f"Plan file not found: {plan_path}",
            "suggested_fixes": [f"Ensure plan exists at: {plan_path}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    with open(plan_path, encoding="utf-8") as f:
        content = f.read()

    # Extract machine-readable handoff YAML
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        # Try to find Section 11 as fallback for backward compatibility
        handoff_match = re.search(
            r"## 11\. Machine-readable plan\s+```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL | re.IGNORECASE,
        )

    if not handoff_match:
        errors.append({
            "error_type": "missing_field",
            "field": "machine_readable_handoff",
            "current_value": None,
            "message": "SECTION_11_MALFORMED: Machine-readable handoff YAML block not found in plan artifact "
                        "(expected a ```yaml fence under Section 13 or Section 11).",
            "suggested_fixes": [
                "Add Section 13 with a ```yaml block containing plan metadata",
                "Or add Section 11 with a ```yaml block for backward compatibility"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    try:
        plan_data = yaml.safe_load(handoff_match.group(1))
    except Exception as e:
        errors.append({
            "error_type": "type_error",
            "field": "machine_readable_handoff",
            "current_value": None,
            "message": f"SECTION_11_MALFORMED: Failed to parse YAML block: {str(e)}",
            "suggested_fixes": ["Ensure YAML syntax is correct", "Check indentation and formatting"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    if not isinstance(plan_data, dict):
        errors.append({
            "error_type": "type_error",
            "field": "machine_readable_handoff",
            "current_value": type(plan_data).__name__,
            "message": f"SECTION_11_MALFORMED: YAML block should be a dictionary, got {type(plan_data).__name__}",
            "suggested_fixes": ["Ensure YAML block contains key-value pairs, not a list"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    # --- artifact_id / status sanity (registry-era checks, kept alongside Phase 1 fields) ---
    if plan_data.get("artifact_id") not in (None, "workflow_orchestration_plan"):
        errors.append(_code_error(
            SECTION_11_MALFORMED,
            f"artifact_id mismatch: expected 'workflow_orchestration_plan', got '{plan_data.get('artifact_id')}'",
            field="artifact_id",
        ))
    if "artifact_id" not in plan_data:
        errors.append(_code_error(SECTION_11_MALFORMED, "Missing 'artifact_id' in machine-readable block", field="artifact_id"))
    if "status" not in plan_data:
        errors.append(_code_error(SECTION_11_MALFORMED, "Missing 'status' in machine-readable block", field="status"))

    # --- PHASE 1 REQUIRED FIELD CHECKS ---
    # Check primary_fog_type
    if "primary_fog_type" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.primary_fog_type.missing_field",
            "error_type": "missing_field",
            "field": "primary_fog_type",
            "current_value": None,
            "message": "Required field 'primary_fog_type' is missing.",
            "suggested_fixes": [
                "Add primary_fog_type: product_fog",
                "Add primary_fog_type: ui_fog",
                "Add primary_fog_type: docs_fog",
                "Add primary_fog_type: architecture_fog"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        fog_type = plan_data.get("primary_fog_type")
        allowed_fog_types = ["product_fog", "ui_fog", "docs_fog", "architecture_fog"]
        if fog_type not in allowed_fog_types:
            errors.append({
                "error_id": "workflow_orchestration_plan.primary_fog_type.unknown_value",
                "error_type": "unknown_value",
                "field": "primary_fog_type",
                "current_value": fog_type,
                "message": f"Field 'primary_fog_type' has value '{fog_type}', which is not recognized.",
                "suggested_fixes": [f"Change to: primary_fog_type: {ft}" for ft in allowed_fog_types],
                "reference": "docs/adr/0007-soft-context-routing.md"
            })

    # Check chosen_workflow_id
    if "chosen_workflow_id" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.chosen_workflow_id.missing_field",
            "error_type": "missing_field",
            "field": "chosen_workflow_id",
            "current_value": None,
            "message": "WORKFLOW_NOT_FOUND: Required field 'chosen_workflow_id' is missing.",
            "suggested_fixes": [
                "Add chosen_workflow_id: product-implementation-workflow",
                "Add chosen_workflow_id: ui-implementation-workflow",
                "Add chosen_workflow_id: docs-implementation-workflow",
                "Add chosen_workflow_id: architecture-implementation-workflow"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        workflow_id = plan_data.get("chosen_workflow_id")
        workflow_reg = load_workflow_registry(repo_root)
        if workflow_reg is not None:
            valid_ids = {w["id"] for w in workflow_reg.get("workflows", [])}
            if workflow_id not in valid_ids:
                errors.append({
                    "error_id": "workflow_orchestration_plan.chosen_workflow_id.unknown_value",
                    "error_type": "unknown_value",
                    "field": "chosen_workflow_id",
                    "current_value": workflow_id,
                    "message": f"WORKFLOW_NOT_FOUND: Workflow ID '{workflow_id}' not found in registry.",
                    "suggested_fixes": [
                        "Check available workflows in workflow-registry.yaml",
                        "Ensure workflow ID matches exactly (case-sensitive)"
                    ],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                })

    # Check routing_decision_method
    if "routing_decision_method" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.routing_decision_method.missing_field",
            "error_type": "missing_field",
            "field": "routing_decision_method",
            "current_value": None,
            "message": "Required field 'routing_decision_method' is missing.",
            "suggested_fixes": [
                "Add routing_decision_method: automated",
                "Add routing_decision_method: manual_override",
                "Add routing_decision_method: context_based"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })

    # Check workflow_steps (should be non-empty array)
    if "workflow_steps" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.workflow_steps.missing_field",
            "error_type": "missing_field",
            "field": "workflow_steps",
            "current_value": None,
            "message": "Required field 'workflow_steps' is missing.",
            "suggested_fixes": [
                "Add workflow_steps as an array of step objects",
                "Each step should have: step_id, skill, input_artifact, output_artifact, gate, description"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
    else:
        workflow_steps = plan_data.get("workflow_steps")
        if not isinstance(workflow_steps, list):
            errors.append({
                "error_id": "workflow_orchestration_plan.workflow_steps.type_error",
                "error_type": "type_error",
                "field": "workflow_steps",
                "current_value": workflow_steps,
                "message": f"Field 'workflow_steps' should be an array, but got {type(workflow_steps).__name__}.",
                "suggested_fixes": ["Convert workflow_steps to an array of step objects"],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        elif len(workflow_steps) == 0:
            errors.append({
                "error_id": "workflow_orchestration_plan.workflow_steps.logic_error",
                "error_type": "logic_error",
                "field": "workflow_steps",
                "current_value": [],
                "message": "workflow_steps array is empty. At least one workflow step is required.",
                "suggested_fixes": [
                    "Add at least one step to workflow_steps",
                    "Each step should have: step_id, skill, input_artifact, output_artifact, gate, description"
                ],
                "reference": "docs/adr/0003-artifact-composition-pattern.md"
            })

    # Check created_at
    if "created_at" not in plan_data:
        errors.append({
            "error_id": "workflow_orchestration_plan.created_at.missing_field",
            "error_type": "missing_field",
            "field": "created_at",
            "current_value": None,
            "message": "Required field 'created_at' is missing.",
            "suggested_fixes": [
                "Add created_at with ISO 8601 timestamp (e.g., 2026-05-25T10:30:00Z)"
            ],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })

    # --- SEMANTIC CONFLICT CHECK: primary_fog_type vs chosen_workflow_id ---
    # Mapping of fog types to expected workflow IDs
    fog_to_workflow = {
        "product_fog": "product-implementation-workflow",
        "ui_fog": "ui-implementation-workflow",
        "docs_fog": "docs-implementation-workflow",
        "architecture_fog": "architecture-implementation-workflow",
    }

    fog_type = plan_data.get("primary_fog_type")
    workflow_id = plan_data.get("chosen_workflow_id")
    routing_method = plan_data.get("routing_decision_method")

    # An explicit, intentional fog/workflow divergence is permitted when the routing
    # decision was an explicit override. The canonical vocabulary value is
    # `user_explicit_override` (docs/canonical-vocabulary.yaml); the legacy `manual_override`
    # alias is still recognized for compatibility but is NOT part of the canonical
    # vocabulary (validate-artifact.py enforces the canonical values). See #232.
    explicit_override = isinstance(routing_method, str) and routing_method in (
        "user_explicit_override", "manual_override",
    )

    # Only check alignment if both fields are present and valid
    if fog_type in fog_to_workflow and workflow_id:
        expected_workflow = fog_to_workflow[fog_type]
        escalation_override = isinstance(routing_method, str) and routing_method.startswith("escalation_recommended")
        if workflow_id != expected_workflow and not explicit_override and not escalation_override:
            errors.append({
                "error_id": "workflow_orchestration_plan.chosen_workflow_id.semantic_conflict",
                "error_type": "semantic_conflict",
                "field": "chosen_workflow_id",
                "current_value": workflow_id,
                "message": f"Workflow '{workflow_id}' does not align with primary_fog_type '{fog_type}'. "
                           f"Expected '{expected_workflow}' unless routing_decision_method is an explicit override "
                           f"(user_explicit_override).",
                "suggested_fixes": [
                    f"Change chosen_workflow_id to: {expected_workflow}",
                    "Or set routing_decision_method to: user_explicit_override (if this is an intentional explicit "
                    "fog/workflow divergence).",
                ],
                "reference": "docs/adr/0007-soft-context-routing.md"
            })

    # --- REGISTRY CROSS-REFERENCE CHECKS ---
    # Only run once artifact_id/chosen_workflow_id survived the Phase-1 checks above,
    # otherwise these would just re-report the same missing-field errors differently.
    if plan_data.get("chosen_workflow_id"):
        errors.extend(_validate_plan_against_registries(plan_data, repo_root))

    return errors


def validation_result_to_json(
    plan_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema."""
    result: ValidationResult = {
        "valid": len(errors) == 0,
        "artifact_id": "workflow_orchestration_plan",
        "artifact_path": os.path.abspath(plan_path),
        "validator": "validate-plan.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for workflow orchestration plan.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the plan .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            WORKFLOW_NOT_FOUND,
            EXECUTION_MODE_DENIED,
            INPUT_MISMATCH,
            STEP_COUNT_MISMATCH,
            STEP_SKILL_MISMATCH,
            STEP_TYPE_MISMATCH,
            GATE_MISMATCH,
            INPUT_ARTIFACT_MISMATCH,
            OUTPUT_ARTIFACT_MISMATCH,
            ARTIFACT_NOT_CONTRACTED,
            GATE_BEHAVIOR_MISSING,
            SIMULATED_GATE_CLASH,
            STOP_CONDITIONS_EMPTY,
            SUBSET_NOT_CONTIGUOUS,
            SECTION_11_MALFORMED,
            ABSOLUTE_PATH_DETECTED,
            HALLUCINATED_SKILL,
            MISSING_DECISION_FIELD,
            INVALID_CONDITIONAL_BRANCH,
            CONFLICT_NOT_ESCALATED,
        ]
        print("Stable error codes for plan validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_plan(args.artifact_path, args.repo_root)

    if args.json:
        print(validation_result_to_json(args.artifact_path, errors))
        return 0 if len(errors) == 0 else 1
    else:
        # Legacy prose output for backward compatibility
        if errors:
            for error in errors:
                error_type = error.get("error_type", "unknown")
                field = error.get("field", "")
                message = error.get("message", "")
                print(f"ERROR [{error_type}] {field}: {message}")
            return 1
        else:
            print("Plan validation passed! All required fields are present and valid.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
