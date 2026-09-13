"""Validate cross-file authority links used by the Version 1.0 release."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


def find_stable_lab_imports(repo_root: Path, lab_modules: tuple[str, ...]) -> list[str]:
    """Return import references from stable product Python modules to lab code."""

    findings: list[str] = []
    stable_roots = (
        repo_root / "src" / "sensemaking_skills" / "campaign_semantics",
        repo_root / "src" / "sensemaking_skills" / "campaigns",
        repo_root / "src" / "sensemaking_skills" / "semantic_architecture",
        repo_root / "src" / "sensemaking_skills" / "setup_skills.py",
    )
    patterns = tuple(re.escape(module) for module in lab_modules)
    if not patterns:
        return findings
    matcher = re.compile(r"(?:from|import)\s+(" + "|".join(patterns) + r")")
    for root in stable_roots:
        files = [root] if root.is_file() else root.rglob("*.py") if root.is_dir() else []
        for path in files:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = matcher.search(line)
                if match:
                    findings.append(
                        f"{path.relative_to(repo_root)}:{line_number}: {match.group(1)}"
                    )
    return findings


def _load(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc


def _list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a list of non-empty strings")
    return value


def validate_contract_authority(repo_root: Path) -> list[str]:
    errors: list[str] = []
    release = _load(repo_root / "release-v1.0.yaml")
    if not isinstance(release, dict):
        return ["release-v1.0.yaml must be a mapping"]

    inventory = release.get("skill_inventory", {})
    supported = set(_list(inventory.get("supported", []), "skill_inventory.supported"))
    internal = set(_list(inventory.get("internal", []), "skill_inventory.internal"))
    experimental = set(_list(inventory.get("experimental", []), "skill_inventory.experimental"))
    declared = supported | internal | experimental
    if len(declared) != len(supported) + len(internal) + len(experimental):
        errors.append("Skill inventory categories overlap")

    skills_root = repo_root / "skills"
    canonical = {path.parent.name for path in skills_root.glob("*/SKILL.md")}
    if not skills_root.is_dir() or not canonical:
        errors.append("canonical Skill directory is missing: skills")
    missing = sorted(declared - canonical)
    extra = sorted(canonical - declared)
    errors.extend(f"Skill inventory missing canonical Skill: {item}" for item in missing)
    errors.extend(f"canonical Skill is not classified: {item}" for item in extra)

    manifest_root = repo_root / "skill-manifests"
    manifests: dict[str, dict[str, Any]] = {}
    for path in manifest_root.rglob("*.yaml") if manifest_root.is_dir() else ():
        value = _load(path)
        if isinstance(value, dict) and isinstance(value.get("skill_id"), str):
            skill_id = value["skill_id"]
            if skill_id in manifests:
                errors.append(f"duplicate Skill manifest: {skill_id}")
            manifests[skill_id] = value
    errors.extend(f"supported Skill has no manifest: {item}" for item in sorted(supported - set(manifests)))

    contract_path = repo_root / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
    artifact_data = _load(contract_path) if contract_path.is_file() else {}
    artifact_ids = {
        item.get("id")
        for item in artifact_data.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for skill_id in sorted(supported):
        manifest = manifests.get(skill_id, {})
        for artifact in manifest.get("produces", []):
            if artifact not in artifact_ids:
                errors.append(f"Skill {skill_id} produces undeclared artifact: {artifact}")

    pack_root = repo_root / "domain-packs"
    packed: set[str] = set()
    for path in pack_root.glob("*.yaml") if pack_root.is_dir() else ():
        value = _load(path)
        for reference in value.get("skill_manifests", []) if isinstance(value, dict) else []:
            packed.add(Path(str(reference)).stem)
    errors.extend(f"supported Skill is absent from Domain Packs: {item}" for item in sorted(supported - packed))

    pyproject = (repo_root / "pyproject.toml").read_text(encoding="utf-8") if (repo_root / "pyproject.toml").is_file() else ""
    for module in release.get("package_boundary", {}).get("source_only_modules", []):
        pattern = f'"{module}*"'
        if pattern not in pyproject:
            errors.append(f"source-only module is not excluded from packaging: {module}")
    lab_imports = find_stable_lab_imports(
        repo_root,
        tuple(release.get("package_boundary", {}).get("source_only_modules", [])),
    )
    errors.extend(f"stable product imports source-only lab module: {item}" for item in lab_imports)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate_contract_authority(args.repo_root.resolve())
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        print(f"FAIL: {len(errors)} contract-authority error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("contract authority graph: resolved")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
