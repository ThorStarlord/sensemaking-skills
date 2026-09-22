"""Read-only Capability & Organization Tracer v0.

This module gives agents and operators a mechanically inspectable view of an
explicit organizational pattern and a small Skill-capability overlay. It never
selects a Skill, allocates a worker, grants authority, or executes work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml


ALLOWED_BINDING_KINDS = {"skill", "executor"}
ALLOWED_RELATIONSHIP_KINDS = {
    "delegates_to",
    "returns_evidence_to",
    "reviews",
    "informs",
}


@dataclass(frozen=True)
class OrganizationDiagnostic:
    code: str
    detail: str
    path: str = ""


@dataclass(frozen=True)
class SkillCapabilityProfile:
    skill_id: str
    package_role: str
    capability_families: tuple[str, ...]
    typical_roles: tuple[str, ...]
    authority_posture: str
    effect_boundary: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class OrganizationBinding:
    kind: str
    id: str
    provides: tuple[str, ...] = ()


@dataclass(frozen=True)
class OrganizationRole:
    id: str
    responsibility: str
    capability_requirements: tuple[str, ...]
    authority: str
    receives: tuple[str, ...]
    returns: tuple[str, ...]
    bindings: tuple[OrganizationBinding, ...]
    optional: bool = False


@dataclass(frozen=True)
class OrganizationRelationship:
    source: str
    target: str
    kind: str
    carries: tuple[str, ...] = ()


@dataclass(frozen=True)
class OrganizationPattern:
    organization_id: str
    objective_class: str
    roles: tuple[OrganizationRole, ...]
    relationships: tuple[OrganizationRelationship, ...]
    limits: tuple[str, ...]
    schema_version: int = 0


@dataclass(frozen=True)
class OrganizationInspection:
    organization_id: str
    objective_class: str
    roles: tuple[Mapping[str, Any], ...]
    relationships: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[OrganizationDiagnostic, ...]
    limits: tuple[str, ...]
    valid: bool
    selection_performed: bool = False
    authorization_granted: bool = False
    execution_performed: bool = False
    semantic_truth_established: bool = False


def _read_mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read YAML mapping {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML document must be a mapping: {path}")
    return value


def _required_text(data: Mapping[str, Any], key: str, *, where: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}.{key} must be a non-empty string")
    return value.strip()


def _string_tuple(
    data: Mapping[str, Any],
    key: str,
    *,
    where: str,
    required: bool = False,
) -> tuple[str, ...]:
    value = data.get(key, [])
    if value is None and not required:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"{where}.{key} must be a list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{where}.{key}[{index}] must be a non-empty string")
        result.append(item.strip())
    if required and not result:
        raise ValueError(f"{where}.{key} must not be empty")
    return tuple(result)


def load_skill_capability_profiles(path: str | Path) -> tuple[SkillCapabilityProfile, ...]:
    source = Path(path)
    data = _read_mapping(source)
    if data.get("schema_version") != 0:
        raise ValueError("Skill capability profile overlay requires schema_version: 0")
    raw_profiles = data.get("profiles")
    if not isinstance(raw_profiles, list) or not raw_profiles:
        raise ValueError("Skill capability profile overlay requires a non-empty profiles list")

    profiles: list[SkillCapabilityProfile] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_profiles):
        where = f"profiles[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be a mapping")
        skill_id = _required_text(item, "skill_id", where=where)
        if skill_id in seen:
            raise ValueError(f"duplicate skill_id in profile overlay: {skill_id}")
        seen.add(skill_id)
        profiles.append(
            SkillCapabilityProfile(
                skill_id=skill_id,
                package_role=_required_text(item, "package_role", where=where),
                capability_families=_string_tuple(
                    item,
                    "capability_families",
                    where=where,
                    required=True,
                ),
                typical_roles=_string_tuple(item, "typical_roles", where=where),
                authority_posture=_required_text(
                    item,
                    "authority_posture",
                    where=where,
                ),
                effect_boundary=_required_text(
                    item,
                    "effect_boundary",
                    where=where,
                ),
                notes=_string_tuple(item, "notes", where=where),
            )
        )
    return tuple(profiles)


def load_organization_pattern(path: str | Path) -> OrganizationPattern:
    source = Path(path)
    data = _read_mapping(source)
    if data.get("schema_version") != 0:
        raise ValueError("Organization Pattern v0 requires schema_version: 0")

    raw_roles = data.get("roles")
    raw_relationships = data.get("relationships")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise ValueError("Organization Pattern v0 requires a non-empty roles list")
    if not isinstance(raw_relationships, list):
        raise ValueError("Organization Pattern v0 requires a relationships list")

    roles: list[OrganizationRole] = []
    seen_roles: set[str] = set()
    for index, item in enumerate(raw_roles):
        where = f"roles[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be a mapping")
        role_id = _required_text(item, "id", where=where)
        if role_id in seen_roles:
            raise ValueError(f"duplicate role id: {role_id}")
        seen_roles.add(role_id)

        raw_bindings = item.get("bindings")
        if not isinstance(raw_bindings, list) or not raw_bindings:
            raise ValueError(f"{where}.bindings must be a non-empty list")
        bindings: list[OrganizationBinding] = []
        for binding_index, binding in enumerate(raw_bindings):
            binding_where = f"{where}.bindings[{binding_index}]"
            if not isinstance(binding, dict):
                raise ValueError(f"{binding_where} must be a mapping")
            kind = _required_text(binding, "kind", where=binding_where)
            if kind not in ALLOWED_BINDING_KINDS:
                raise ValueError(
                    f"{binding_where}.kind must be one of "
                    f"{sorted(ALLOWED_BINDING_KINDS)}"
                )
            bindings.append(
                OrganizationBinding(
                    kind=kind,
                    id=_required_text(binding, "id", where=binding_where),
                    provides=_string_tuple(
                        binding,
                        "provides",
                        where=binding_where,
                    ),
                )
            )

        optional = item.get("optional", False)
        if not isinstance(optional, bool):
            raise ValueError(f"{where}.optional must be a boolean")
        roles.append(
            OrganizationRole(
                id=role_id,
                responsibility=_required_text(
                    item,
                    "responsibility",
                    where=where,
                ),
                capability_requirements=_string_tuple(
                    item,
                    "capability_requirements",
                    where=where,
                    required=True,
                ),
                authority=_required_text(item, "authority", where=where),
                receives=_string_tuple(item, "receives", where=where),
                returns=_string_tuple(item, "returns", where=where),
                bindings=tuple(bindings),
                optional=optional,
            )
        )

    relationships: list[OrganizationRelationship] = []
    for index, item in enumerate(raw_relationships):
        where = f"relationships[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be a mapping")
        kind = _required_text(item, "kind", where=where)
        if kind not in ALLOWED_RELATIONSHIP_KINDS:
            raise ValueError(
                f"{where}.kind must be one of "
                f"{sorted(ALLOWED_RELATIONSHIP_KINDS)}"
            )
        relationships.append(
            OrganizationRelationship(
                source=_required_text(item, "from", where=where),
                target=_required_text(item, "to", where=where),
                kind=kind,
                carries=_string_tuple(item, "carries", where=where),
            )
        )

    return OrganizationPattern(
        organization_id=_required_text(
            data,
            "organization_id",
            where="organization",
        ),
        objective_class=_required_text(
            data,
            "objective_class",
            where="organization",
        ),
        roles=tuple(roles),
        relationships=tuple(relationships),
        limits=_string_tuple(data, "limits", where="organization"),
        schema_version=0,
    )


def _manifest_projection(repo_root: Path, skill_id: str) -> dict[str, Any] | None:
    manifests_root = repo_root / "skill-manifests"
    if not manifests_root.is_dir():
        return None
    for path in sorted(manifests_root.rglob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        if not isinstance(data, dict) or data.get("skill_id") != skill_id:
            continue
        return {
            "path": str(path.relative_to(repo_root)),
            "domain": data.get("domain"),
            "responsibilities": (
                list(data.get("responsibilities", []))
                if isinstance(data.get("responsibilities"), list)
                else []
            ),
            "repository_mutation": data.get("repository_mutation"),
        }
    return None


def project_skill_capability_profile(
    profiles_path: str | Path,
    *,
    skill_id: str,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    profiles = {
        profile.skill_id: profile
        for profile in load_skill_capability_profiles(profiles_path)
    }
    profile = profiles.get(skill_id)
    if profile is None:
        raise ValueError(f"skill profile not declared in overlay: {skill_id}")

    payload: dict[str, Any] = {
        "skill_id": profile.skill_id,
        "package_role": profile.package_role,
        "capability_families": list(profile.capability_families),
        "typical_roles": list(profile.typical_roles),
        "authority_posture": profile.authority_posture,
        "effect_boundary": profile.effect_boundary,
        "notes": list(profile.notes),
        "profile_overlay_authoritative": False,
        "selection_performed": False,
    }
    if repo_root is not None:
        repository = Path(repo_root).resolve()
        skill_path = repository / "skills" / skill_id / "SKILL.md"
        payload["canonical_skill_path"] = str(
            skill_path.relative_to(repository)
        )
        payload["canonical_skill_exists"] = skill_path.is_file()
        payload["manifest"] = _manifest_projection(repository, skill_id)
    return payload


def inspect_organization_pattern(
    pattern_path: str | Path,
    profiles_path: str | Path,
    *,
    repo_root: str | Path | None = None,
) -> OrganizationInspection:
    pattern = load_organization_pattern(pattern_path)
    profiles = {
        profile.skill_id: profile
        for profile in load_skill_capability_profiles(profiles_path)
    }
    repository = Path(repo_root).resolve() if repo_root is not None else None
    diagnostics: list[OrganizationDiagnostic] = []
    role_ids = {role.id for role in pattern.roles}
    role_views: list[dict[str, Any]] = []

    for role in pattern.roles:
        covered: set[str] = set()
        binding_views: list[dict[str, Any]] = []
        for binding in role.bindings:
            if binding.kind == "skill":
                profile = profiles.get(binding.id)
                if profile is None:
                    diagnostics.append(
                        OrganizationDiagnostic(
                            "ORG_SKILL_PROFILE_MISSING",
                            f"role {role.id} references unprofiled Skill {binding.id}",
                            role.id,
                        )
                    )
                    binding_views.append(
                        {
                            "kind": binding.kind,
                            "id": binding.id,
                            "capabilities": [],
                            "profile_found": False,
                        }
                    )
                    continue
                capabilities = set(profile.capability_families)
                covered.update(capabilities)
                skill_exists: bool | None = None
                if repository is not None:
                    skill_exists = (
                        repository / "skills" / binding.id / "SKILL.md"
                    ).is_file()
                    if not skill_exists:
                        diagnostics.append(
                            OrganizationDiagnostic(
                                "ORG_CANONICAL_SKILL_MISSING",
                                f"role {role.id} binds missing canonical Skill {binding.id}",
                                role.id,
                            )
                        )
                binding_views.append(
                    {
                        "kind": binding.kind,
                        "id": binding.id,
                        "capabilities": sorted(capabilities),
                        "profile_found": True,
                        "canonical_skill_exists": skill_exists,
                    }
                )
            else:
                capabilities = set(binding.provides)
                if not capabilities:
                    diagnostics.append(
                        OrganizationDiagnostic(
                            "ORG_EXECUTOR_CAPABILITIES_MISSING",
                            f"executor binding {binding.id} on role {role.id} "
                            "must declare provides",
                            role.id,
                        )
                    )
                covered.update(capabilities)
                binding_views.append(
                    {
                        "kind": binding.kind,
                        "id": binding.id,
                        "capabilities": sorted(capabilities),
                    }
                )

        missing = sorted(set(role.capability_requirements) - covered)
        if missing:
            diagnostics.append(
                OrganizationDiagnostic(
                    "ORG_CAPABILITY_UNSATISFIED",
                    f"role {role.id} lacks bindings for capabilities: "
                    + ", ".join(missing),
                    role.id,
                )
            )
        role_views.append(
            {
                "id": role.id,
                "responsibility": role.responsibility,
                "optional": role.optional,
                "capability_requirements": list(role.capability_requirements),
                "covered_capabilities": sorted(covered),
                "authority": role.authority,
                "receives": list(role.receives),
                "returns": list(role.returns),
                "bindings": binding_views,
            }
        )

    relationship_views: list[dict[str, Any]] = []
    for relation in pattern.relationships:
        if relation.source not in role_ids:
            diagnostics.append(
                OrganizationDiagnostic(
                    "ORG_RELATION_SOURCE_MISSING",
                    f"relationship source role does not exist: {relation.source}",
                    relation.source,
                )
            )
        if relation.target not in role_ids:
            diagnostics.append(
                OrganizationDiagnostic(
                    "ORG_RELATION_TARGET_MISSING",
                    f"relationship target role does not exist: {relation.target}",
                    relation.target,
                )
            )
        relationship_views.append(
            {
                "from": relation.source,
                "to": relation.target,
                "kind": relation.kind,
                "carries": list(relation.carries),
            }
        )

    return OrganizationInspection(
        organization_id=pattern.organization_id,
        objective_class=pattern.objective_class,
        roles=tuple(role_views),
        relationships=tuple(relationship_views),
        diagnostics=tuple(diagnostics),
        limits=pattern.limits,
        valid=not diagnostics,
    )


def inspect_organization_role(
    pattern_path: str | Path,
    profiles_path: str | Path,
    *,
    role_id: str,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    inspection = inspect_organization_pattern(
        pattern_path,
        profiles_path,
        repo_root=repo_root,
    )
    role = next(
        (item for item in inspection.roles if item.get("id") == role_id),
        None,
    )
    if role is None:
        raise ValueError(f"organization role not found: {role_id}")
    inbound = [
        item for item in inspection.relationships if item.get("to") == role_id
    ]
    outbound = [
        item for item in inspection.relationships if item.get("from") == role_id
    ]
    return {
        "organization_id": inspection.organization_id,
        "objective_class": inspection.objective_class,
        "role": role,
        "inbound_relationships": inbound,
        "outbound_relationships": outbound,
        "organization_valid": inspection.valid,
        "organization_diagnostics": [
            {
                "code": item.code,
                "detail": item.detail,
                "path": item.path,
            }
            for item in inspection.diagnostics
        ],
        "selection_performed": False,
        "authorization_granted": False,
        "execution_performed": False,
        "explicit_limit": (
            "Role inspection exposes declared bindings and evidence flow only; "
            "it does not assign an actor, select a Skill, or authorize execution."
        ),
    }
