"""Deterministic P6 capability inspection without semantic routing.

The active coding agent supplies the responsibility classification. This module
loads declared capability metadata, resolves current Skill/workflow identity and
workflow liveness facts, and enumerates compatible candidates. It never infers
a responsibility type, ranks candidates, selects a capability, or grants
execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

import yaml

from sensemaking_skills.campaign_semantics import Authority
from sensemaking_skills.campaign_semantics.models import Capability
from sensemaking_skills.campaign_semantics.registry import (
    AvailabilityStatus,
    CapabilityRegistry,
    RegisteredCapability,
)
from sensemaking_skills.setup_skills import (
    SkillsSetupError,
    find_skills_in_package,
    get_package_skills_dir,
)

from .errors import CampaignTransactionError
from .service import CampaignService


CATALOG_SCHEMA_VERSION = "1"
_ALLOWED_KINDS = {"skill", "workflow"}
_ALLOWED_FIELDS = {
    "id",
    "kind",
    "source",
    "accepted_responsibility_types",
    "input_artifact",
    "output_artifact",
    "completion_conditions",
    "mutates_repository",
    "authority",
    "availability",
    "availability_reason",
    "returns_control",
}
_ALLOWED_WORKFLOW_LIVENESS = {"active", "compatibility_only"}


class CapabilityCatalogError(ValueError):
    """Raised when declared capability metadata is structurally untrustworthy."""


@dataclass(frozen=True)
class CapabilityInspection:
    campaign_id: str
    responsibility_id: str
    responsibility_type: str
    responsibility_authority: Authority
    candidates: tuple[RegisteredCapability, ...]


def _nonempty_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CapabilityCatalogError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: Any, *, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise CapabilityCatalogError(f"{field} must be a string")
    return value.strip()


def _string_tuple(value: Any, *, field: str, required: bool = False) -> tuple[str, ...]:
    if value is None and not required:
        return ()
    if not isinstance(value, list):
        raise CapabilityCatalogError(f"{field} must be a list of strings")
    items = tuple(_nonempty_text(item, field=field) for item in value)
    if required and not items:
        raise CapabilityCatalogError(f"{field} must contain at least one value")
    if len(items) != len(set(items)):
        raise CapabilityCatalogError(f"{field} must not contain duplicate values")
    return items


def _load_yaml_mapping(path: Path, *, label: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise CapabilityCatalogError(f"failed to load {label} from {path}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise CapabilityCatalogError(f"{label} must be a YAML mapping")
    return value


def _package_default_path(filename: str) -> Path:
    return Path(str(files("sensemaking_skills.defaults").joinpath(filename)))


def _current_skill_ids() -> set[str]:
    """Return Skill implementations actually shipped by this install/source tree."""
    try:
        return set(find_skills_in_package(get_package_skills_dir()))
    except SkillsSetupError as exc:
        raise CapabilityCatalogError(
            f"cannot resolve current packaged Skill identities: {exc}"
        ) from exc


def _workflow_facts(
    *,
    registry_path: Path,
    liveness_path: Path,
) -> tuple[set[str], dict[str, str]]:
    registry_data = _load_yaml_mapping(registry_path, label="workflow registry")
    raw_workflows = registry_data.get("workflows", [])
    if not isinstance(raw_workflows, list):
        raise CapabilityCatalogError("workflow registry 'workflows' must be a list")

    workflow_ids: set[str] = set()
    for index, raw in enumerate(raw_workflows):
        if not isinstance(raw, Mapping):
            raise CapabilityCatalogError(
                f"workflow registry workflows[{index}] must be a mapping"
            )
        workflow_id = _nonempty_text(raw.get("id"), field=f"workflows[{index}].id")
        if workflow_id in workflow_ids:
            raise CapabilityCatalogError(
                f"workflow registry contains duplicate id {workflow_id!r}"
            )
        workflow_ids.add(workflow_id)

    liveness_data = _load_yaml_mapping(liveness_path, label="workflow liveness")
    default_liveness = _nonempty_text(
        liveness_data.get("default_liveness", "active"),
        field="workflow_liveness.default_liveness",
    )
    if default_liveness not in _ALLOWED_WORKFLOW_LIVENESS:
        raise CapabilityCatalogError(
            f"unknown default workflow liveness {default_liveness!r}"
        )
    raw_overrides = liveness_data.get("overrides", {}) or {}
    if not isinstance(raw_overrides, Mapping):
        raise CapabilityCatalogError("workflow liveness 'overrides' must be a mapping")

    effective = {workflow_id: default_liveness for workflow_id in workflow_ids}
    for raw_id, raw_liveness in raw_overrides.items():
        workflow_id = _nonempty_text(raw_id, field="workflow_liveness.override_id")
        liveness = _nonempty_text(
            raw_liveness,
            field=f"workflow_liveness.overrides.{workflow_id}",
        )
        if liveness not in _ALLOWED_WORKFLOW_LIVENESS:
            raise CapabilityCatalogError(
                f"unknown workflow liveness {liveness!r} for {workflow_id!r}"
            )
        if workflow_id in workflow_ids:
            effective[workflow_id] = liveness
    return workflow_ids, effective


def load_capability_registry(
    *,
    catalog_path: Path | None = None,
    workflow_registry_path: Path | None = None,
    workflow_liveness_path: Path | None = None,
) -> CapabilityRegistry:
    """Load strict declared capability metadata into the semantic registry.

    Alternate paths exist for qualification tests. Product callers normally use
    packaged defaults, which are included in the installed wheel.
    """

    catalog_path = catalog_path or _package_default_path("capability-registry.yaml")
    workflow_registry_path = workflow_registry_path or _package_default_path(
        "workflow-registry.yaml"
    )
    workflow_liveness_path = workflow_liveness_path or _package_default_path(
        "workflow-liveness.yaml"
    )

    data = _load_yaml_mapping(catalog_path, label="capability registry")
    schema_version = data.get("schema_version")
    if schema_version != CATALOG_SCHEMA_VERSION:
        raise CapabilityCatalogError(
            f"unsupported capability registry schema_version {schema_version!r}"
        )
    unknown_top = set(data) - {"schema_version", "capabilities"}
    if unknown_top:
        raise CapabilityCatalogError(
            "capability registry contains unknown top-level fields: "
            + ", ".join(sorted(unknown_top))
        )

    raw_capabilities = data.get("capabilities")
    if not isinstance(raw_capabilities, list):
        raise CapabilityCatalogError("capability registry 'capabilities' must be a list")

    skill_ids = _current_skill_ids()
    workflow_ids, workflow_liveness = _workflow_facts(
        registry_path=workflow_registry_path,
        liveness_path=workflow_liveness_path,
    )

    items: list[RegisteredCapability] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_capabilities):
        prefix = f"capabilities[{index}]"
        if not isinstance(raw, Mapping):
            raise CapabilityCatalogError(f"{prefix} must be a mapping")
        unknown = set(raw) - _ALLOWED_FIELDS
        if unknown:
            raise CapabilityCatalogError(
                f"{prefix} contains unknown fields: {', '.join(sorted(unknown))}"
            )

        capability_id = _nonempty_text(raw.get("id"), field=f"{prefix}.id")
        if capability_id in seen:
            raise CapabilityCatalogError(f"duplicate capability id {capability_id!r}")
        seen.add(capability_id)

        kind = _nonempty_text(raw.get("kind"), field=f"{prefix}.kind")
        if kind not in _ALLOWED_KINDS:
            raise CapabilityCatalogError(
                f"{prefix}.kind must be one of {sorted(_ALLOWED_KINDS)}"
            )
        _nonempty_text(raw.get("source"), field=f"{prefix}.source")
        accepted_types = _string_tuple(
            raw.get("accepted_responsibility_types"),
            field=f"{prefix}.accepted_responsibility_types",
            required=True,
        )
        output_artifact = _nonempty_text(
            raw.get("output_artifact"), field=f"{prefix}.output_artifact"
        )
        input_artifact = raw.get("input_artifact")
        if input_artifact is not None:
            input_artifact = _nonempty_text(
                input_artifact, field=f"{prefix}.input_artifact"
            )
        completion_conditions = _string_tuple(
            raw.get("completion_conditions", []),
            field=f"{prefix}.completion_conditions",
        )

        mutates_repository = raw.get("mutates_repository")
        if not isinstance(mutates_repository, bool):
            raise CapabilityCatalogError(f"{prefix}.mutates_repository must be boolean")
        returns_control = raw.get("returns_control", True)
        if not isinstance(returns_control, bool):
            raise CapabilityCatalogError(f"{prefix}.returns_control must be boolean")

        try:
            authority = Authority(
                _nonempty_text(raw.get("authority"), field=f"{prefix}.authority")
            )
        except ValueError as exc:
            raise CapabilityCatalogError(
                f"{prefix}.authority is not a known Authority value"
            ) from exc
        try:
            availability = AvailabilityStatus(
                _nonempty_text(raw.get("availability"), field=f"{prefix}.availability")
            )
        except ValueError as exc:
            raise CapabilityCatalogError(
                f"{prefix}.availability is not a known availability value"
            ) from exc
        availability_reason = _optional_text(
            raw.get("availability_reason"), field=f"{prefix}.availability_reason"
        )
        if availability is not AvailabilityStatus.AVAILABLE and not availability_reason:
            raise CapabilityCatalogError(
                f"{prefix}.availability_reason is required when availability is "
                f"{availability.value!r}"
            )

        if kind == "skill":
            # Historical/proposed/deprecated identities may stay in the catalog as
            # explicitly unavailable. Anything that claims a live/externally live
            # status must correspond to an actual shipped Skill implementation.
            if (
                availability is not AvailabilityStatus.UNAVAILABLE
                and capability_id not in skill_ids
            ):
                raise CapabilityCatalogError(
                    f"Skill capability {capability_id!r} has no current shipped "
                    "Skill implementation"
                )
        else:
            if capability_id not in workflow_ids:
                raise CapabilityCatalogError(
                    f"workflow capability {capability_id!r} is absent from the workflow catalog"
                )
            liveness = workflow_liveness[capability_id]
            if liveness == "compatibility_only":
                availability = AvailabilityStatus.UNAVAILABLE
                availability_reason = (
                    "workflow liveness is compatibility_only; current selection/execution "
                    "is prohibited"
                )

        capability = Capability(
            id=capability_id,
            accepted_responsibility_types=accepted_types,
            input_artifact=input_artifact,
            output_artifact=output_artifact,
            completion_conditions=completion_conditions,
        )
        items.append(
            RegisteredCapability(
                capability=capability,
                kind=kind,
                mutates_repository=mutates_repository,
                authority=authority,
                availability=availability,
                returns_control=returns_control,
                availability_reason=availability_reason,
            )
        )

    return CapabilityRegistry(items)


class CampaignCapabilityService:
    """Inspect declared candidates for an agent-supplied responsibility type."""

    def __init__(self, workspace: str | Path) -> None:
        self.lifecycle = CampaignService(workspace)

    def inspect(
        self,
        responsibility_type: str,
        *,
        registry: CapabilityRegistry | None = None,
    ) -> CapabilityInspection:
        if not isinstance(responsibility_type, str) or not responsibility_type.strip():
            raise CampaignTransactionError("responsibility_type must be non-empty")
        responsibility_type = responsibility_type.strip()

        snapshot = self.lifecycle.resume()
        responsibility = snapshot.state.active_responsibility
        if responsibility is None:
            raise CampaignTransactionError(
                "capability inspection requires one active responsibility"
            )
        if snapshot.state.authority is None:
            raise CampaignTransactionError(
                "active responsibility is missing its authority classification"
            )

        registry = registry or load_capability_registry()
        candidates = tuple(
            sorted(
                registry.candidates(responsibility_type),
                key=lambda item: item.capability.id,
            )
        )
        return CapabilityInspection(
            campaign_id=snapshot.state.campaign_id,
            responsibility_id=responsibility.id,
            responsibility_type=responsibility_type,
            responsibility_authority=snapshot.state.authority,
            candidates=candidates,
        )
