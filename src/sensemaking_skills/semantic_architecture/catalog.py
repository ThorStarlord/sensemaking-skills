"""Read-only developer catalog for Skill Contract Manifests and Domain Packs.

The catalog improves discoverability over existing manifest bytes. It does not
create a second conformance authority, rank capabilities, or infer that a Skill
is appropriate for a task.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from .conformance import validate_conformance
from .models import SemanticDiagnostic


@dataclass(frozen=True)
class SemanticCatalogResult:
    skill_manifests: tuple[Mapping[str, Any], ...]
    domain_packs: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[SemanticDiagnostic, ...]
    conformance_valid: bool
    semantic_truth_established: bool = False
    selection_performed: bool = False


def _load_mapping(path: Path, *, code: str) -> tuple[dict[str, Any] | None, SemanticDiagnostic | None]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, SemanticDiagnostic(code, str(exc), str(path))
    if not isinstance(value, dict):
        return None, SemanticDiagnostic(code, "document must be a mapping", str(path))
    return value, None


def build_semantic_catalog(
    manifests_dir: str | Path,
    *,
    domain_packs_dir: str | Path | None = None,
    repo_root: str | Path | None = None,
    skill_id: str | None = None,
    domain_id: str | None = None,
) -> SemanticCatalogResult:
    """Project declared manifest/pack metadata with optional exact filters."""

    manifests_root = Path(manifests_dir)
    packs_root = Path(domain_packs_dir) if domain_packs_dir is not None else None
    repository = Path(repo_root).resolve() if repo_root is not None else None
    diagnostics: list[SemanticDiagnostic] = []
    manifests: list[dict[str, Any]] = []
    packs: list[dict[str, Any]] = []

    for path in sorted(manifests_root.rglob("*.yaml")):
        data, diagnostic = _load_mapping(path, code="SEMANTIC_CATALOG_MANIFEST_PARSE_FAILED")
        if diagnostic is not None:
            diagnostics.append(diagnostic)
            continue
        assert data is not None
        declared_skill = data.get("skill_id")
        declared_domain = data.get("domain")
        if skill_id is not None and declared_skill != skill_id:
            continue
        if domain_id is not None and declared_domain != domain_id:
            continue
        canonical_skill_path = None
        canonical_skill_exists = None
        if repository is not None and isinstance(declared_skill, str) and declared_skill:
            candidate = repository / "skills" / declared_skill / "SKILL.md"
            canonical_skill_path = str(candidate.relative_to(repository))
            canonical_skill_exists = candidate.is_file()
        manifests.append(
            {
                "path": str(path),
                "skill_id": declared_skill,
                "domain": declared_domain,
                "responsibilities": list(data.get("responsibilities", [])) if isinstance(data.get("responsibilities"), list) else [],
                "consumes": list(data.get("consumes", [])) if isinstance(data.get("consumes"), list) else [],
                "produces": list(data.get("produces", [])) if isinstance(data.get("produces"), list) else [],
                "semantic_concepts": list(data.get("semantic_concepts", [])) if isinstance(data.get("semantic_concepts"), list) else [],
                "repository_mutation": data.get("repository_mutation"),
                "canonical_skill_path": canonical_skill_path,
                "canonical_skill_exists": canonical_skill_exists,
            }
        )

    if packs_root is not None:
        for path in sorted(packs_root.rglob("*.yaml")):
            data, diagnostic = _load_mapping(path, code="SEMANTIC_CATALOG_DOMAIN_PACK_PARSE_FAILED")
            if diagnostic is not None:
                diagnostics.append(diagnostic)
                continue
            assert data is not None
            declared_domain = data.get("domain_id")
            if domain_id is not None and declared_domain != domain_id:
                continue
            pack_manifests = list(data.get("skill_manifests", [])) if isinstance(data.get("skill_manifests"), list) else []
            if skill_id is not None:
                matching_paths = {item["path"] for item in manifests if item.get("skill_id") == skill_id}
                normalized_matching = set()
                for value in matching_paths:
                    candidate = Path(value)
                    if repository is not None:
                        try:
                            normalized_matching.add(str(candidate.resolve().relative_to(repository)))
                        except ValueError:
                            normalized_matching.add(value)
                    else:
                        normalized_matching.add(value)
                if normalized_matching and not any(value in normalized_matching for value in pack_manifests):
                    continue
            packs.append(
                {
                    "path": str(path),
                    "domain_id": declared_domain,
                    "capability_ledger": data.get("capability_ledger"),
                    "skill_manifests": pack_manifests,
                    "responsibility_vocabulary": list(data.get("responsibility_vocabulary", [])) if isinstance(data.get("responsibility_vocabulary"), list) else [],
                    "artifact_contracts": list(data.get("artifact_contracts", [])) if isinstance(data.get("artifact_contracts"), list) else [],
                    "qualification_policy": data.get("qualification_policy"),
                }
            )

    conformance = validate_conformance(
        manifests_root,
        domain_packs_dir=packs_root,
        repo_root=repository,
    )
    return SemanticCatalogResult(
        skill_manifests=tuple(manifests),
        domain_packs=tuple(packs),
        diagnostics=tuple(diagnostics),
        conformance_valid=conformance.valid,
    )
