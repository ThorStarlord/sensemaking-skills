"""Validate the repository-owned Version 1.0 release contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


class ReleaseContractError(ValueError):
    pass


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReleaseContractError(f"{label} must be a mapping")
    return value


def _strings(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ReleaseContractError(f"{label} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise ReleaseContractError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise ReleaseContractError(f"{label} contains duplicate values")
    return value


def validate(repo_root: Path) -> list[str]:
    contract_path = repo_root / "release-v1.0.yaml"
    try:
        raw = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReleaseContractError(f"cannot read {contract_path}: {exc}") from exc

    data = _mapping(raw, "release contract")
    if data.get("schema_version") != 1:
        raise ReleaseContractError("schema_version must be 1")

    release = _mapping(data.get("release"), "release")
    if release.get("version") != "1.0.0rc1":
        raise ReleaseContractError("release.version must be 1.0.0rc1")
    if release.get("scope_classification") not in {"reduced", "full"}:
        raise ReleaseContractError(
            "release.scope_classification must be 'reduced' or 'full'"
        )
    if not (repo_root / str(release.get("release_policy", ""))).is_file():
        raise ReleaseContractError("release policy path does not exist")

    support = _mapping(data.get("support"), "support")
    for field in ("python", "operating_systems", "harnesses"):
        _strings(support.get(field), f"support.{field}")
    native_harnesses = support.get("native_harnesses")
    if not isinstance(native_harnesses, list) or not all(
        isinstance(item, str) and item for item in native_harnesses
    ):
        raise ReleaseContractError("support.native_harnesses must be a list of strings")
    if not set(native_harnesses) <= set(support["harnesses"]):
        raise ReleaseContractError("support.native_harnesses must be a subset of support.harnesses")

    public = _mapping(data.get("public_surface"), "public_surface")
    _strings(public.get("cli"), "public_surface.cli")
    _strings(public.get("stable_python_modules"), "public_surface.stable_python_modules")
    if public.get("schema_version") != "2":
        raise ReleaseContractError("public_surface.schema_version must be 2")

    boundary = _mapping(data.get("package_boundary"), "package_boundary")
    source_only = _strings(boundary.get("source_only_modules"), "package_boundary.source_only_modules")
    pyproject = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    for module in source_only:
        package = module.removeprefix("sensemaking_skills.")
        if f'"sensemaking_skills.{package}*"' not in pyproject:
            raise ReleaseContractError(f"source-only module is not excluded from packaging: {module}")

    inventory = _mapping(data.get("skill_inventory"), "skill_inventory")
    supported = _strings(inventory.get("supported"), "skill_inventory.supported")
    internal = _strings(inventory.get("internal"), "skill_inventory.internal")
    experimental = _strings(inventory.get("experimental"), "skill_inventory.experimental", allow_empty=True)
    declared = supported + internal + experimental
    if len(declared) != len(set(declared)):
        raise ReleaseContractError("skill inventory categories overlap")
    canonical = {path.parent.name for path in (repo_root / "skills").glob("*/SKILL.md")}
    if set(declared) != canonical:
        missing = sorted(canonical - set(declared))
        extra = sorted(set(declared) - canonical)
        raise ReleaseContractError(f"Skill inventory mismatch; missing={missing}, extra={extra}")
    manifest_ids = {path.stem for path in (repo_root / "skill-manifests").rglob("*.yaml")}
    if not set(supported) <= manifest_ids:
        raise ReleaseContractError("every supported Skill must have a manifest")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ReleaseContractError("claims must be a non-empty list")
    claim_ids: list[str] = []
    for index, claim in enumerate(claims):
        item = _mapping(claim, f"claims[{index}]")
        claim_ids.append(str(item.get("id", "")))
        for field in ("id", "statement", "evidence", "status"):
            if not isinstance(item.get(field), str) or not item[field]:
                raise ReleaseContractError(f"claims[{index}].{field} must be non-empty")
        if not isinstance(item.get("support_required"), bool):
            raise ReleaseContractError(f"claims[{index}].support_required must be boolean")
    if len(claim_ids) != len(set(claim_ids)):
        raise ReleaseContractError("claims contain duplicate ids")

    return [
        f"release contract: {release['version']}",
        f"canonical Skills classified: {len(canonical)}",
        f"supported Skills with manifests: {len(supported)}",
        f"claims declared: {len(claims)}",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository checkout containing release-v1.0.yaml (required for this source-release check)",
    )
    args = parser.parse_args()
    try:
        for line in validate(args.repo_root.resolve()):
            print(line)
        print("PASS")
    except (OSError, ReleaseContractError) as exc:
        print(f"FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
