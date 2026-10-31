"""Installation availability of catalogue workflows (fail closed).

Liveness (ADR 0027) decides whether a workflow is eligible in the catalogue.
This module answers a different question: whether the Skills a workflow needs
are present in the Skill root that an agent loads. It never changes liveness,
and an installation-available workflow is not thereby authorized to execute.

Steps marked conditional, or nested under ``if_true`` / ``if_false``, are
reported separately. They do not block availability, because the workflow text
states a fallback for them. Unknown installation state is reported as not
available.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

import yaml

ACTIVE = "active"
_BRANCH_KEYS = frozenset({"if_true", "if_false"})


def _load_defaults_mapping(filename: str) -> Mapping[str, Any]:
    text = files("sensemaking_skills.defaults").joinpath(filename).read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {}
    if not isinstance(data, Mapping):
        raise ValueError(f"packaged {filename} must be a mapping")
    return data


def catalogue_workflows() -> tuple[list[Mapping[str, Any]], dict[str, str]]:
    """Return packaged workflow definitions and their effective liveness."""
    registry = _load_defaults_mapping("workflow-registry.yaml")
    liveness = _load_defaults_mapping("workflow-liveness.yaml")
    raw_workflows = registry.get("workflows") or []
    if not isinstance(raw_workflows, list):
        raise ValueError("packaged workflow registry 'workflows' must be a list")
    workflows = [item for item in raw_workflows if isinstance(item, Mapping) and item.get("id")]
    default = liveness.get("default_liveness", ACTIVE)
    overrides = liveness.get("overrides") or {}
    effective = {str(item["id"]): str(overrides.get(item["id"], default)) for item in workflows}
    return workflows, effective


def required_skills(workflow: Mapping[str, Any]) -> tuple[frozenset[str], frozenset[str]]:
    """Return (required, conditional) Skill ids named by a workflow's steps."""
    required: set[str] = set()
    conditional: set[str] = set()
    _collect_skills(workflow.get("steps") or [], False, required, conditional)
    return frozenset(required), frozenset(conditional - required)


def _collect_skills(
    node: Any,
    in_conditional: bool,
    required: set[str],
    conditional: set[str],
) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_skills(item, in_conditional, required, conditional)
        return
    if not isinstance(node, Mapping):
        return
    here = in_conditional or node.get("conditional") is True
    skill = node.get("skill")
    if isinstance(skill, str) and skill:
        (conditional if here else required).add(skill)
    for key, value in node.items():
        if key == "skill":
            continue
        _collect_skills(value, here or key in _BRANCH_KEYS, required, conditional)


def installed_skill_ids(root: Path) -> frozenset[str]:
    """Return Skill ids whose tree (with SKILL.md) is present directly under root."""
    if not root.is_dir():
        return frozenset()
    return frozenset(
        child.name for child in root.iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    )


def workflow_availability(installed: Optional[Iterable[str]]) -> list[dict[str, Any]]:
    """Report installation availability for every active catalogue workflow.

    ``installed=None`` means the installed set is unknown. Every workflow is then
    reported as ``unknown`` and not available. The result says nothing about
    liveness beyond filtering to active workflows, and nothing about authority.
    """
    workflows, liveness = catalogue_workflows()
    installed_set = None if installed is None else frozenset(installed)
    rows: list[dict[str, Any]] = []
    for workflow in sorted(workflows, key=lambda item: str(item["id"])):
        workflow_id = str(workflow["id"])
        if liveness.get(workflow_id, ACTIVE) != ACTIVE:
            continue
        required, conditional = required_skills(workflow)
        if installed_set is None:
            status = "unknown"
            missing = sorted(required)
            conditional_absent = sorted(conditional)
        else:
            missing = sorted(required - installed_set)
            status = "available" if not missing else "missing_required_skills"
            conditional_absent = sorted(conditional - installed_set)
        rows.append(
            {
                "workflow_id": workflow_id,
                "installation": status,
                "installation_available": status == "available",
                "missing_required_skills": missing,
                "conditional_skills_absent": conditional_absent,
            }
        )
    return rows


def summarize_availability(rows: list[dict[str, Any]]) -> list[str]:
    """Render availability rows as ASCII lines for installer output."""
    available = [row["workflow_id"] for row in rows if row["installation_available"]]
    blocked = [row for row in rows if not row["installation_available"]]
    lines = [
        f"available here: {len(available)} of {len(rows)} active workflows "
        "(installation only; not liveness and not execution authority)"
    ]
    if blocked:
        lines.append("not available (required Skills missing; do not present as executable):")
        for row in blocked:
            if row["installation"] == "unknown":
                reason = "installed Skill set unknown"
            else:
                reason = "needs " + ", ".join(row["missing_required_skills"])
            lines.append(f"  {row['workflow_id']} ({reason})")
    return lines
