"""Generic external-executor interchange and AI Software Factory projection.

The interchange serializes an already-recorded execution handoff and validates a
worker-return envelope. Factory-specific rendering is a projection over the
generic envelope; it does not publish an issue, select an Archon workflow,
schedule a run, or grant authority.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Mapping

from .companion_io import mapping_sha256
from .execution import CampaignExecutionService


EXECUTION_INTERCHANGE_VERSION = "1"
HANDOFF_KIND = "sensemaking.execution-handoff"
RESULT_KIND = "sensemaking.execution-result"
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_WORKFLOW = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _find_handoff(
    service: CampaignExecutionService,
    handoff_id: str,
) -> Mapping[str, Any]:
    inspected = service.inspect()
    if not inspected.valid:
        raise ValueError("execution companion is invalid")
    for item in inspected.handoffs:
        if item.get("handoff_id") == handoff_id:
            return item
    raise ValueError(f"unknown handoff_id: {handoff_id}")


def _envelope_digest(value: Mapping[str, Any]) -> str:
    core = {key: item for key, item in value.items() if key != "envelope_digest"}
    return mapping_sha256(core)


def build_handoff_envelope(
    workspace: str | Path,
    *,
    handoff_id: str,
) -> dict[str, Any]:
    """Return one generic, integrity-bound delegation envelope."""
    service = CampaignExecutionService(workspace)
    handoff = dict(_find_handoff(service, handoff_id))
    core: dict[str, Any] = {
        "schema_version": EXECUTION_INTERCHANGE_VERSION,
        "kind": HANDOFF_KIND,
        "campaign_id": handoff["campaign_id"],
        "handoff_id": handoff["handoff_id"],
        "handoff_record_digest": handoff["record_digest"],
        "executor_kind": handoff["executor_kind"],
        "responsibility": handoff["responsibility"],
        "targets": handoff["targets"],
        "evidence_requirements": handoff["evidence_requirements"],
        "forbidden_actions": handoff["forbidden_actions"],
        "return_contract": {
            "schema_version": EXECUTION_INTERCHANGE_VERSION,
            "kind": RESULT_KIND,
            "required_fields": [
                "campaign_id",
                "handoff_id",
                "result_id",
                "worker",
                "source_before",
                "source_after",
                "changed_paths",
                "validations",
                "evidence_refs",
                "unresolved_uncertainties",
                "claims_supported",
                "claims_not_supported",
                "authority_exceeded",
            ],
            "digest": "sha256(canonical-json(envelope-without-envelope_digest))",
        },
        "selection_performed_by_tool": False,
        "authorization_granted_by_tool": False,
        "execution_performed_by_tool": False,
        "semantic_truth_established": False,
    }
    return {**core, "envelope_digest": _envelope_digest(core)}


def build_result_template(
    workspace: str | Path,
    *,
    handoff_id: str,
    result_id: str,
    worker: str,
) -> dict[str, Any]:
    """Return a fillable result envelope bound to an existing handoff."""
    handoff = build_handoff_envelope(workspace, handoff_id=handoff_id)
    core: dict[str, Any] = {
        "schema_version": EXECUTION_INTERCHANGE_VERSION,
        "kind": RESULT_KIND,
        "campaign_id": handoff["campaign_id"],
        "handoff_id": handoff_id,
        "handoff_record_digest": handoff["handoff_record_digest"],
        "result_id": result_id,
        "worker": worker,
        "source_before": "",
        "source_after": "",
        "changed_paths": [],
        "validations": [],
        "evidence_refs": [],
        "unresolved_uncertainties": [],
        "claims_supported": [],
        "claims_not_supported": [],
        "authority_exceeded": False,
        "worker_completion_establishes_global_closure": False,
        "campaign_evidence_admitted": False,
        "semantic_truth_established": False,
    }
    return {**core, "envelope_digest": _envelope_digest(core)}


def _list_of_strings(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{label} must contain only non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return tuple(value)


def import_result_envelope(
    workspace: str | Path,
    envelope: Mapping[str, Any],
) -> str:
    """Validate one generic worker return and append the normal result record."""
    service = CampaignExecutionService(workspace)
    if not isinstance(envelope, Mapping):
        raise ValueError("result envelope must be a JSON object")
    data = dict(envelope)
    if data.get("schema_version") != EXECUTION_INTERCHANGE_VERSION:
        raise ValueError("unsupported result envelope schema_version")
    if data.get("kind") != RESULT_KIND:
        raise ValueError(f"result envelope kind must be {RESULT_KIND}")
    digest = data.get("envelope_digest")
    if not isinstance(digest, str) or digest != _envelope_digest(data):
        raise ValueError("result envelope digest mismatch")

    handoff_id = data.get("handoff_id")
    handoff = dict(_find_handoff(service, str(handoff_id)))
    if data.get("campaign_id") != handoff.get("campaign_id"):
        raise ValueError("result envelope campaign_id does not match handoff")
    if data.get("handoff_record_digest") != handoff.get("record_digest"):
        raise ValueError("result envelope handoff_record_digest does not match handoff")
    if data.get("worker_completion_establishes_global_closure") is not False:
        raise ValueError(
            "worker_completion_establishes_global_closure must remain false"
        )
    if data.get("campaign_evidence_admitted") is not False:
        raise ValueError("campaign_evidence_admitted must remain false")
    if data.get("semantic_truth_established") is not False:
        raise ValueError("semantic_truth_established must remain false")
    if not isinstance(data.get("authority_exceeded"), bool):
        raise ValueError("authority_exceeded must be boolean")

    for field in ("result_id", "worker", "source_before", "source_after"):
        if not isinstance(data.get(field), str) or not str(data[field]).strip():
            raise ValueError(f"{field} must be non-empty text")

    return service.record_result(
        result_id=str(data["result_id"]),
        handoff_id=str(handoff_id),
        worker=str(data["worker"]),
        source_before=str(data["source_before"]),
        source_after=str(data["source_after"]),
        changed_paths=_list_of_strings(data.get("changed_paths"), "changed_paths"),
        validations=_list_of_strings(data.get("validations"), "validations"),
        evidence_refs=_list_of_strings(data.get("evidence_refs"), "evidence_refs"),
        unresolved_uncertainties=_list_of_strings(
            data.get("unresolved_uncertainties"),
            "unresolved_uncertainties",
        ),
        claims_supported=_list_of_strings(
            data.get("claims_supported"),
            "claims_supported",
        ),
        claims_not_supported=_list_of_strings(
            data.get("claims_not_supported"),
            "claims_not_supported",
        ),
        authority_exceeded=bool(data["authority_exceeded"]),
    )


def build_factory_issue_projection(
    workspace: str | Path,
    *,
    handoff_id: str,
    repository: str,
    workflow: str,
) -> dict[str, Any]:
    """Render an issue payload for a caller-selected AI Software Factory workflow."""
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        raise ValueError("repository must be OWNER/REPO")
    if not isinstance(workflow, str) or not _WORKFLOW.fullmatch(workflow):
        raise ValueError("workflow must be a non-empty workflow identifier")

    envelope = build_handoff_envelope(workspace, handoff_id=handoff_id)
    responsibility = envelope["responsibility"]
    title = (
        f"[Sensemaking {envelope['handoff_id']}] "
        f"{responsibility['statement']}"
    )
    if len(title) > 240:
        title = title[:237] + "..."

    pretty = json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False)
    targets = "\n".join(
        (
            f"- {item['alias']} — {item['repository_id']} "
            f"@ {item['head_sha']}; role: {item['role']}"
        )
        for item in envelope["targets"]
    )
    success = "\n".join(
        f"- {item}" for item in responsibility["success_conditions"]
    )
    evidence = "\n".join(
        f"- {item}" for item in envelope["evidence_requirements"]
    )
    forbidden = (
        "\n".join(f"- {item}" for item in envelope["forbidden_actions"])
        or "- none declared"
    )
    body = f"""<!-- sensemaking-execution-handoff:v1 -->
## Sensemaking execution handoff

This issue transports an already-selected responsibility. The issue does not
grant authority beyond the recorded handoff, and the factory must return
evidence to the parent decision context rather than treating worker completion
as global closure.

Campaign: {envelope['campaign_id']}
Handoff: {envelope['handoff_id']}
Responsibility: {responsibility['id']} — {responsibility['statement']}
Authority: {responsibility['authority']}
Decision blocked: {responsibility.get('decision_blocked') or 'none'}
Caller-selected factory workflow: {workflow}

### Targets

{targets}

### Success conditions

{success}

### Evidence the worker must return

{evidence}

### Forbidden actions

{forbidden}

### Machine-readable handoff

~~~json
{pretty}
~~~

### Return boundary

worker success != global closure
returned evidence != admitted evidence
factory workflow selected by caller != workflow selected by Sensemaking
"""
    command = (
        f"python factory/consumer.py run {workflow} "
        "--input target={ISSUE_URL} --detach --json"
    )
    return {
        "schema_version": EXECUTION_INTERCHANGE_VERSION,
        "kind": "ai-software-factory.github-issue-projection",
        "repository": repository,
        "workflow": workflow,
        "issue": {"title": title, "body": body},
        "factory_command_template": command,
        "handoff_envelope_digest": envelope["envelope_digest"],
        "workflow_selected_by_tool": False,
        "issue_published": False,
        "execution_submitted": False,
        "semantic_truth_established": False,
        "explicit_limit": (
            "This projection renders a GitHub Issue and command template for the "
            "caller-selected AI Software Factory workflow. It does not publish, "
            "schedule, execute, merge, deploy, or choose the workflow."
        ),
    }
