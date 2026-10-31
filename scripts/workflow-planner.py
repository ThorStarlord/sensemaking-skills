#!/usr/bin/env python3
"""Workflow Planner: Convert diagnostic brief into orchestration plan.

Reads a repository_sensemaking_brief and produces a workflow_orchestration_plan
by mapping fog_type to implementation workflow and extracting workflow steps.

The plan separates three facts. Liveness (ADR 0027) decides whether the workflow
is selectable. Installation availability decides whether its required Skills are
present in an explicitly supplied installed Skill root. Execution status combines
the two and is never execution authorization. Without an explicit installed root,
installation is reported as unknown, and the workflow is not presented as
executable now.
"""

import argparse
import json
import os
import sys
import yaml
from datetime import datetime, timezone
from typing import TypedDict, Any, Optional

from _validator_utils import (
    load_workflow_availability,
    load_workflow_registry,
    resolve_installed_skill_context,
)


def _availability():
    """Return the shared installation-availability model (one implementation, see _validator_utils)."""
    return load_workflow_availability()


def _installed_context(installed_skills_root: Optional[str]) -> tuple[Optional[frozenset], str, str]:
    """Return (installed Skill ids or None, human note, machine context kind).

    Only an explicitly supplied root grounds installation. The machine-readable kind
    carries no local path, because validate-plan rejects absolute paths in YAML.
    """
    return resolve_installed_skill_context(installed_skills_root)

# Fog type to historical/default workflow candidate (from workflow-planner
# SKILL.md). ADR 0027 requires a liveness check before any candidate can become
# a current selection. A compatibility-only former default is NOT silently
# replaced by another workflow.
FOG_TYPE_TO_WORKFLOW = {
    "product_fog": "product-implementation-workflow",
    "ui_fog": "ui-implementation-workflow",
    "docs_fog": "docs-implementation-workflow",
    "architecture_fog": "architecture-implementation-workflow",
}


def extract_brief_data(content: str) -> dict[str, Any] | None:
    """Extract machine-readable data from brief artifact YAML block."""
    import re

    # Look for YAML block in section 13 or last YAML block
    yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    if yaml_blocks:
        try:
            return yaml.safe_load(yaml_blocks[-1])
        except Exception:
            return None
    return None


def get_workflow_steps(workflow_id: str, registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract current executable workflow steps for a workflow ID."""
    if not registry:
        return []

    workflows = registry.get("workflows", [])
    for workflow in workflows:
        if workflow.get("id") == workflow_id and workflow.get("liveness", "active") == "active":
            return workflow.get("steps", [])
    return []


def plan_workflow(
    brief_path: str,
    repo_root: str = ".",
    installed_skills_root: Optional[str] = None,
) -> str:
    """Generate workflow orchestration plan from brief artifact.

    ``installed_skills_root`` is the Skill root an agent loads from, when the caller
    knows it. Omitting it leaves installation unknown. Planning still succeeds, but
    the plan records that the workflow is not executable now.

    Returns markdown artifact or error message.
    """
    # Read brief artifact
    if not os.path.exists(brief_path):
        return f"ERROR: Brief not found: {brief_path}"

    with open(brief_path, "r", encoding="utf-8") as f:
        brief_content = f.read()

    # Extract machine-readable data from brief
    brief_data = extract_brief_data(brief_content)
    if not brief_data:
        return "ERROR: Could not extract machine-readable data from brief YAML block"

    # Get fog type and validation
    primary_fog_type = brief_data.get("primary_fog_type")
    if not primary_fog_type:
        return "ERROR: primary_fog_type not found in brief"

    if primary_fog_type not in FOG_TYPE_TO_WORKFLOW:
        return f"ERROR: Unknown fog type: {primary_fog_type}"

    # Load the ADR-0027 operational registry view. Compatibility-only IDs are
    # preserved in the catalog view but excluded from this CURRENT active view.
    registry = load_workflow_registry(repo_root)
    if not registry:
        return "ERROR: Could not load workflow registry"

    workflows = registry.get("workflows", [])
    active_workflow_ids = {
        workflow.get("id")
        for workflow in workflows
        if isinstance(workflow, dict)
        and workflow.get("id")
        and workflow.get("liveness", "active") == "active"
    }

    # Determine routing decision method
    # PHASE 4.3 FIX: Honor escalation recommendations, now bounded by ADR 0027
    # liveness. A former default becoming compatibility-only does not authorize
    # the planner to invent a replacement route.
    default_workflow_id = FOG_TYPE_TO_WORKFLOW[primary_fog_type]
    recommended_workflow_id = brief_data.get("recommended_workflow_id", default_workflow_id)
    escalation_recommended = brief_data.get("escalation_recommended", False)

    if escalation_recommended and recommended_workflow_id in active_workflow_ids:
        chosen_workflow_id = recommended_workflow_id
        routing_decision_method = "escalation_recommended_accepted"
        routing_divergence = (chosen_workflow_id != recommended_workflow_id)
    elif default_workflow_id in active_workflow_ids:
        chosen_workflow_id = default_workflow_id
        if chosen_workflow_id == recommended_workflow_id:
            routing_decision_method = "diagnosis_primary_soft_context"
        else:
            routing_decision_method = "manual_override"
        routing_divergence = (chosen_workflow_id != recommended_workflow_id)
    else:
        recommendation_note = (
            f"; brief recommendation '{recommended_workflow_id}' is also not active"
            if recommended_workflow_id not in (None, "")
            and recommended_workflow_id not in active_workflow_ids
            else ""
        )
        return (
            f"ERROR: Default workflow '{default_workflow_id}' for {primary_fog_type} "
            f"is not currently active under ADR 0027{recommendation_note}. "
            "No replacement route is ratified. Select an active workflow explicitly "
            "or preserve/escalate the no-match decision instead of silently routing."
        )

    # Get workflow steps
    workflow_steps = get_workflow_steps(chosen_workflow_id, registry)
    if not workflow_steps:
        return f"ERROR: No active steps found for workflow: {chosen_workflow_id}"

    # Installation availability is evaluated against the same effective definition
    # that liveness selected above, so repository overrides apply. The chosen
    # workflow is active by construction (operational view), so live is True.
    chosen_definition = next(
        (
            workflow
            for workflow in workflows
            if isinstance(workflow, dict) and workflow.get("id") == chosen_workflow_id
        ),
        {},
    )
    availability = _availability()
    installed, context_note, context_kind = _installed_context(installed_skills_root)
    installation = availability.installation_status(chosen_definition, installed)
    execution = availability.execution_status(
        live=True,
        installation=installation,
        context_note=context_note,
    )
    installation_text = {
        "available": "available in the supplied installed Skill root",
        "missing_required_skills": "missing required Skills",
        "unknown": "unknown (no installed Skill root supplied)",
    }[installation["installation"]]
    required_text = ", ".join(installation["required_skills"]) or "none"
    if installation["installation"] == "unknown":
        missing_text = f"not evaluated (required: {required_text})"
        conditional_text = "not evaluated"
    else:
        missing_text = ", ".join(installation["missing_required_skills"]) or "none"
        conditional_text = ", ".join(installation["conditional_skills_absent"]) or "none"
    execution_text = execution["execution_status"]
    if execution["not_executable_reason"]:
        execution_text += f" ({execution['not_executable_reason']})"

    # Generate plan artifact
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Build plan artifact with proper variable substitution
    plan_artifact = f"""# Workflow Orchestration Plan

## 1. Brief Consumed

**Repository**: (from brief)
**Primary Fog Type**: {primary_fog_type}
**Source Brief**: {brief_path}

---

## 2. System Recommendation

Based on fog type classification:
- Fog Type: `{primary_fog_type}`
- Recommended Workflow: `{default_workflow_id}`
- Escalation Recommended: {str(escalation_recommended).lower()}
- Brief Recommended: `{recommended_workflow_id}`

---

## 3. Workflow Selection

**Selected Workflow**: `{chosen_workflow_id}`
**Routing Decision Method**: `{routing_decision_method}`
**Routing Divergence**: {str(routing_divergence).lower()}
**Installation Availability**: {installation_text}
**Missing Required Skills**: {missing_text}
**Conditional Skills Absent**: {conditional_text}
**Installation Context**: {context_note}
**Execution Status**: {execution_text}
**Execution Authorized**: false (planning never authorizes execution)

---

## 4. Why This Workflow

The `{chosen_workflow_id}` is designed to address {primary_fog_type} by:
- Identifying the root cause of the identified problem
- Producing diagnostic outputs and implementation artifacts
- Preparing the repository for the next phase of work

---

## 5. Workflow Steps

The selected workflow includes the following steps:

| Step | Skill | Input | Output | Gate | Description |
|------|-------|-------|--------|------|-------------|
"""

    for step in workflow_steps:
        step_id = step.get("id", "?")
        skill = step.get("skill", "?")
        input_artifact = step.get("input_artifact", "—")
        output_artifact = step.get("output_artifact", "?")
        gate = step.get("gate", "none")
        description = step.get("description", "")
        plan_artifact += f"| {step_id} | {skill} | {input_artifact} | {output_artifact} | {gate} | {description} |\n"

    plan_artifact += f"""
---

## 6. Execution Mode

**Recommended Mode**: `plan_only`
**Downstream execution**: Active-agent decision; this plan may recommend but never invokes a child workflow

---

## 7. Approval Gates

Steps in this workflow include approval gates. Each gate requires user or automated approval before proceeding.

---

## 8. Next Steps

After this plan is approved and executed:
1. Execute the selected workflow (`{chosen_workflow_id}`)
2. Produce diagnostic/implementation artifacts
3. Continue to Phase 3 implementation (if applicable)

---

## 9. Escalation Handling

If the selected workflow encounters issues:
- Attempted fixes will be recorded in validation logs
- Repeated failure returns evidence to the active agent; no automatic responsibility escalation is implied
- Escalation messages will include detailed error context and suggested next steps

---

## 10. Decision Rationale

The routing decision was made using `{routing_decision_method}`:
- System recommendation based on fog type: `{default_workflow_id}`
- Brief recommendation: `{recommended_workflow_id}`
- Selected workflow: `{chosen_workflow_id}`
- Divergence detected: {str(routing_divergence).lower()}

---

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
schema_version: 1
primary_fog_type: {primary_fog_type}
chosen_workflow_id: {chosen_workflow_id}
routing_decision_method: {routing_decision_method}
routing_divergence: {str(routing_divergence).lower()}
escalation_recommended: {str(brief_data.get('escalation_recommended', False)).lower()}
auto_escalation_allowed: false
installation_availability: {installation["installation"]}
required_skills: {json.dumps(installation["required_skills"])}
missing_required_skills: {json.dumps(installation["missing_required_skills"])}
conditional_skills_absent: {json.dumps(installation["conditional_skills_absent"])}
installation_context: {context_kind}
execution_status: {execution["execution_status"]}
not_executable_reason: {json.dumps(execution["not_executable_reason"])}
execution_authorized: false
created_at: "{timestamp}"
immutable: true
workflow_steps:
"""

    for step in workflow_steps:
        input_artifact = step.get('input_artifact') or 'null'
        plan_artifact += f"""  - step_id: {step.get('id')}
    skill: {step.get('skill')}
    input_artifact: {input_artifact}
    output_artifact: {step.get('output_artifact')}
    gate: {step.get('gate', 'none')}
    description: "{step.get('description', '')}"
"""

    plan_artifact += "```\n"

    return plan_artifact


def main(argv: list[str] | None = None) -> int:
    """Main entry point for workflow planner."""
    parser = argparse.ArgumentParser(description="Workflow Planner: Convert brief to orchestration plan")
    parser.add_argument("brief_path", nargs="?", help="Path to repository_sensemaking_brief.md")
    parser.add_argument("--repo-root", default=".", help="Root of the repository")
    parser.add_argument(
        "--installed-skills-root",
        default=None,
        help=(
            "Installed Skill root that the agent loads from (for example the harness "
            "Skills directory). Required to establish installation availability; "
            "without it the plan records installation as unknown."
        ),
    )
    parser.add_argument("--output", "-o", help="Output file path (default: artifacts/workflow_orchestration_plan.md)")
    args = parser.parse_args(argv)

    if not args.brief_path:
        parser.print_usage()
        return 1

    # Generate plan
    plan_artifact = plan_workflow(
        args.brief_path,
        args.repo_root,
        installed_skills_root=args.installed_skills_root,
    )

    # Check for errors
    if plan_artifact.startswith("ERROR:"):
        print(plan_artifact, file=sys.stderr)
        return 1

    # Write output
    output_path = args.output or "artifacts/workflow_orchestration_plan.md"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(plan_artifact)

    print(f"Workflow plan created: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
