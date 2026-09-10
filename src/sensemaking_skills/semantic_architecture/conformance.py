"""Mechanical conformance checks for Skill and Domain Pack manifests.

Conformance validates declared interfaces and canonical vocabulary membership.
It does not determine whether a Skill is semantically good, whether a capability
is warranted, or whether a domain methodology is correct.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .models import SemanticDiagnostic

CANONICAL_SEMANTIC_CONCEPTS = {
    "Intent",
    "TargetSnapshot",
    "Observation",
    "Evidence",
    "Claim",
    "EpistemicStatus",
    "Uncertainty",
    "Responsibility",
    "SensemakingCapability",
    "SoftwareCapability",
    "ProductCapability",
    "Change",
    "Outcome",
    "Validation",
    "Decision",
    "Authority",
    "Artifact",
}


@dataclass(frozen=True)
class ConformanceResult:
    valid: bool
    diagnostics: tuple[SemanticDiagnostic, ...]
    skill_manifest_count: int
    domain_pack_count: int
    semantic_truth_established: bool = False


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _skill_manifest_diagnostics(
    path: Path,
    data: Any,
    *,
    repo_root: Path | None,
) -> list[SemanticDiagnostic]:
    diagnostics: list[SemanticDiagnostic] = []
    if not isinstance(data, dict):
        return [SemanticDiagnostic("SKILL_MANIFEST_MAPPING_REQUIRED", "manifest must be a mapping", str(path))]
    required = {
        "schema_version",
        "skill_id",
        "domain",
        "responsibilities",
        "consumes",
        "produces",
        "semantic_concepts",
        "repository_mutation",
    }
    for field in sorted(required - set(data)):
        diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_MISSING_FIELD", f"missing {field}", str(path)))
    if data.get("schema_version") not in {1, "1"}:
        diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_SCHEMA_VERSION", "schema_version must be 1", str(path)))
    for field in ("skill_id", "domain"):
        if not isinstance(data.get(field), str) or not data.get(field, "").strip():
            diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_TEXT_REQUIRED", f"{field} must be non-empty text", str(path)))
    for field in ("responsibilities", "consumes", "produces", "semantic_concepts"):
        if field in data and not _nonempty_strings(data.get(field)):
            diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_STRING_LIST_REQUIRED", f"{field} must be a list of non-empty strings", str(path)))
        values = data.get(field)
        if isinstance(values, list):
            for duplicate in sorted(_duplicates([item for item in values if isinstance(item, str)])):
                diagnostics.append(
                    SemanticDiagnostic(
                        "SKILL_MANIFEST_DUPLICATE_LIST_VALUE",
                        f"{field} contains duplicate value {duplicate!r}",
                        str(path),
                    )
                )
    if "repository_mutation" in data and not isinstance(data.get("repository_mutation"), bool):
        diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_BOOLEAN_REQUIRED", "repository_mutation must be boolean", str(path)))
    concepts = data.get("semantic_concepts", [])
    if isinstance(concepts, list):
        unknown = sorted({item for item in concepts if isinstance(item, str)} - CANONICAL_SEMANTIC_CONCEPTS)
        for concept in unknown:
            diagnostics.append(
                SemanticDiagnostic(
                    "SKILL_MANIFEST_UNKNOWN_SEMANTIC_CONCEPT",
                    f"semantic concept {concept!r} is not in the canonical manifest vocabulary",
                    str(path),
                )
            )
    prohibited = {"semantic_truth", "auto_route", "automatic_skill_selection", "automatic_uncertainty_ranking"}
    for field in sorted(prohibited & set(data)):
        diagnostics.append(
            SemanticDiagnostic(
                "SKILL_MANIFEST_PROHIBITED_AUTHORITY_FIELD",
                f"manifest field {field!r} would imply semantic control and is prohibited",
                str(path),
            )
        )
    if repo_root is not None:
        skill_id = data.get("skill_id")
        if isinstance(skill_id, str) and skill_id.strip():
            skill_file = repo_root / "skills" / skill_id / "SKILL.md"
            if not skill_file.is_file():
                diagnostics.append(
                    SemanticDiagnostic(
                        "SKILL_MANIFEST_SKILL_MISSING",
                        f"canonical Skill file does not exist: skills/{skill_id}/SKILL.md",
                        str(path),
                    )
                )
    return diagnostics


def _domain_pack_diagnostics(
    path: Path,
    data: Any,
    *,
    repo_root: Path | None,
) -> list[SemanticDiagnostic]:
    diagnostics: list[SemanticDiagnostic] = []
    if not isinstance(data, dict):
        return [SemanticDiagnostic("DOMAIN_PACK_MAPPING_REQUIRED", "domain pack must be a mapping", str(path))]
    required = {
        "schema_version",
        "domain_id",
        "capability_ledger",
        "skill_manifests",
        "responsibility_vocabulary",
        "artifact_contracts",
        "qualification_policy",
    }
    for field in sorted(required - set(data)):
        diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_MISSING_FIELD", f"missing {field}", str(path)))
    if data.get("schema_version") not in {1, "1"}:
        diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_SCHEMA_VERSION", "schema_version must be 1", str(path)))
    for field in ("domain_id", "capability_ledger", "qualification_policy"):
        if not isinstance(data.get(field), str) or not data.get(field, "").strip():
            diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_TEXT_REQUIRED", f"{field} must be non-empty text", str(path)))
    for field in ("skill_manifests", "responsibility_vocabulary", "artifact_contracts"):
        values = data.get(field)
        if field in data and not _nonempty_strings(values):
            diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_STRING_LIST_REQUIRED", f"{field} must be a list of non-empty strings", str(path)))
        if isinstance(values, list):
            for duplicate in sorted(_duplicates([item for item in values if isinstance(item, str)])):
                diagnostics.append(
                    SemanticDiagnostic(
                        "DOMAIN_PACK_DUPLICATE_LIST_VALUE",
                        f"{field} contains duplicate value {duplicate!r}",
                        str(path),
                    )
                )
    if repo_root is not None:
        for field in ("capability_ledger", "qualification_policy"):
            value = data.get(field)
            if isinstance(value, str) and value and not (repo_root / value).is_file():
                diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_REFERENCE_MISSING", f"{field} reference does not exist: {value}", str(path)))
        manifests = data.get("skill_manifests", [])
        if isinstance(manifests, list):
            pack_domain = data.get("domain_id")
            pack_responsibilities = set(data.get("responsibility_vocabulary", [])) if isinstance(data.get("responsibility_vocabulary"), list) else set()
            pack_artifacts = set(data.get("artifact_contracts", [])) if isinstance(data.get("artifact_contracts"), list) else set()
            for value in manifests:
                if not isinstance(value, str) or not value:
                    continue
                manifest_path = repo_root / value
                if not manifest_path.is_file():
                    diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_MANIFEST_MISSING", f"skill manifest does not exist: {value}", str(path)))
                    continue
                try:
                    manifest = _load_yaml(manifest_path)
                except (OSError, UnicodeError, yaml.YAMLError) as exc:
                    diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_MANIFEST_PARSE_FAILED", f"could not parse {value}: {exc}", str(path)))
                    continue
                if not isinstance(manifest, dict):
                    continue
                if manifest.get("domain") != pack_domain:
                    diagnostics.append(
                        SemanticDiagnostic(
                            "DOMAIN_PACK_MANIFEST_DOMAIN_MISMATCH",
                            f"manifest {value} declares domain {manifest.get('domain')!r}, expected {pack_domain!r}",
                            str(path),
                        )
                    )
                responsibilities = set(manifest.get("responsibilities", [])) if isinstance(manifest.get("responsibilities"), list) else set()
                missing_responsibilities = sorted(responsibilities - pack_responsibilities)
                for responsibility in missing_responsibilities:
                    diagnostics.append(
                        SemanticDiagnostic(
                            "DOMAIN_PACK_RESPONSIBILITY_UNDECLARED",
                            f"manifest {value} uses responsibility {responsibility!r} absent from pack vocabulary",
                            str(path),
                        )
                    )
                produces = set(manifest.get("produces", [])) if isinstance(manifest.get("produces"), list) else set()
                missing_artifacts = sorted(produces - pack_artifacts)
                for artifact in missing_artifacts:
                    diagnostics.append(
                        SemanticDiagnostic(
                            "DOMAIN_PACK_ARTIFACT_UNDECLARED",
                            f"manifest {value} produces {artifact!r} absent from pack artifact_contracts",
                            str(path),
                        )
                    )
    return diagnostics


def validate_conformance(
    manifests_dir: str | Path,
    *,
    domain_packs_dir: str | Path | None = None,
    repo_root: str | Path | None = None,
) -> ConformanceResult:
    manifests_root = Path(manifests_dir)
    packs_root = Path(domain_packs_dir) if domain_packs_dir is not None else None
    repository = Path(repo_root).resolve() if repo_root is not None else None
    diagnostics: list[SemanticDiagnostic] = []
    skill_ids: dict[str, Path] = {}
    domain_ids: dict[str, Path] = {}

    skill_paths = sorted(manifests_root.rglob("*.yaml")) if manifests_root.is_dir() else []
    for path in skill_paths:
        try:
            data = _load_yaml(path)
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            diagnostics.append(SemanticDiagnostic("SKILL_MANIFEST_PARSE_FAILED", str(exc), str(path)))
            continue
        diagnostics.extend(_skill_manifest_diagnostics(path, data, repo_root=repository))
        if isinstance(data, dict) and isinstance(data.get("skill_id"), str):
            skill_id = data["skill_id"]
            if skill_id in skill_ids:
                diagnostics.append(
                    SemanticDiagnostic(
                        "DUPLICATE_SKILL_MANIFEST_ID",
                        f"skill_id {skill_id!r} also declared by {skill_ids[skill_id]}",
                        str(path),
                    )
                )
            else:
                skill_ids[skill_id] = path

    pack_paths = sorted(packs_root.rglob("*.yaml")) if packs_root is not None and packs_root.is_dir() else []
    for path in pack_paths:
        try:
            data = _load_yaml(path)
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            diagnostics.append(SemanticDiagnostic("DOMAIN_PACK_PARSE_FAILED", str(exc), str(path)))
            continue
        diagnostics.extend(_domain_pack_diagnostics(path, data, repo_root=repository))
        if isinstance(data, dict) and isinstance(data.get("domain_id"), str):
            domain_id = data["domain_id"]
            if domain_id in domain_ids:
                diagnostics.append(
                    SemanticDiagnostic(
                        "DUPLICATE_DOMAIN_PACK_ID",
                        f"domain_id {domain_id!r} also declared by {domain_ids[domain_id]}",
                        str(path),
                    )
                )
            else:
                domain_ids[domain_id] = path

    return ConformanceResult(
        valid=not diagnostics,
        diagnostics=tuple(diagnostics),
        skill_manifest_count=len(skill_paths),
        domain_pack_count=len(pack_paths),
    )
