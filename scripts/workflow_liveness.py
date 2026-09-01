"""Workflow catalog/liveness helpers (ADR 0027, issue #263).

Workflow registry identity is durable catalog data.  Liveness is a separate
contract that decides whether a registered workflow is eligible for CURRENT
recommendation, planning, or execution.

This module deliberately exposes both views:

* catalog view: every registered workflow, annotated with effective liveness;
* operational view: the same stable IDs remain recognizable, but
  compatibility-only definitions are fail-closed tombstones with no executable
  modes or steps.

Catalog validators should inspect the raw/annotated catalog.  Current
planning/runtime consumers should use the operational view.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

ACTIVE = "active"
COMPATIBILITY_ONLY = "compatibility_only"
ALLOWED_LIVENESS = {ACTIVE, COMPATIBILITY_ONLY}


def load_liveness_file(path: str | Path) -> dict[str, Any]:
    """Load a liveness overlay, defaulting compatibly when absent.

    External/custom registries that predate ADR 0027 remain active by default.
    Invalid values are preserved rather than silently normalized; repository
    validation is responsible for reporting malformed canonical overlays and
    operational consumers fail closed because only ``active`` is executable.
    """
    path = Path(path)
    if not path.exists():
        return {
            "schema_version": 1,
            "default_liveness": ACTIVE,
            "allowed_liveness": sorted(ALLOWED_LIVENESS),
            "overrides": {},
        }
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        return {
            "schema_version": None,
            "default_liveness": "invalid",
            "allowed_liveness": [],
            "overrides": {},
        }
    return data


def effective_liveness(workflow_id: str, overlay: dict[str, Any] | None) -> str:
    """Return the declared effective liveness for one workflow ID."""
    overlay = overlay or {}
    default = overlay.get("default_liveness", ACTIVE)
    overrides = overlay.get("overrides", {})
    if not isinstance(overrides, dict):
        return "invalid"
    return overrides.get(workflow_id, default)


def annotate_catalog(
    registry: dict[str, Any] | None,
    overlay: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Return a copy of the complete registry with ``liveness`` annotations."""
    if registry is None:
        return None
    result = deepcopy(registry)
    workflows = result.get("workflows", [])
    if not isinstance(workflows, list):
        return result
    for workflow in workflows:
        if not isinstance(workflow, dict):
            continue
        workflow_id = workflow.get("id")
        if workflow_id:
            workflow["liveness"] = effective_liveness(workflow_id, overlay)
    return result


def operationalize_catalog(
    registry: dict[str, Any] | None,
    overlay: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Return the current operational view while preserving stable IDs.

    Active definitions are unchanged apart from their explicit liveness field.
    Compatibility-only definitions remain present so consumers can recognize a
    historical ID, but their current execution surface is intentionally empty:
    no allowed execution modes and no executable steps.  This makes existing
    runtime/plan consumers fail closed without deleting catalog provenance.

    Unknown/invalid liveness values are treated the same way as non-active
    values: they are never silently promoted to current capability.
    """
    result = annotate_catalog(registry, overlay)
    if result is None:
        return None
    for workflow in result.get("workflows", []):
        if not isinstance(workflow, dict):
            continue
        if workflow.get("liveness") != ACTIVE:
            workflow["allowed_execution_modes"] = []
            workflow["steps"] = []
    return result


def active_workflow_ids(
    registry: dict[str, Any] | None,
    overlay: dict[str, Any] | None,
) -> list[str]:
    """Return sorted workflow IDs currently eligible for selection."""
    catalog = annotate_catalog(registry, overlay) or {}
    return sorted(
        workflow["id"]
        for workflow in catalog.get("workflows", [])
        if isinstance(workflow, dict)
        and workflow.get("id")
        and workflow.get("liveness") == ACTIVE
    )
