"""
Skill-Hygiene Validator v1

Performs three checks:
1. npm scripts exist (references in AGENTS.md exist in package.json)
2. skill IDs cross-ref (workflow-registry steps reference existing skills)
3. artifact contracts resolve (artifact refs in registry exist in contracts)

Exit codes:
  0: All checks passed
  1: One or more checks failed
"""

import os
import re
import json
import yaml
import sys
from pathlib import Path

from _validator_utils import flatten_skill_registry

# Canonical registry/contract paths (issue: these previously pointed at the
# repo-root-level legacy "references" tree, which no longer carries
# workflow-registry.yaml or skill-registry.yaml at all -- checks 2 and 3
# silently no-op'd, reporting PASSED for checks they never ran).
_REFS_DIR = os.path.join("skills", "workflow-planner", "references")
WORKFLOW_REGISTRY_PATH = os.path.join(_REFS_DIR, "workflow-registry.yaml")
SKILL_REGISTRY_PATH = os.path.join(_REFS_DIR, "skill-registry.yaml")
ARTIFACT_CONTRACTS_PATH = os.path.join(_REFS_DIR, "artifact-contracts.yaml")


def load_json(path):
    """Load JSON file safely"""
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def load_yaml(path):
    """Load YAML file safely"""
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        return None


def load_text(path):
    """Load text file safely"""
    if not os.path.exists(path):
        return ""
    try:
        with open(path) as f:
            return f.read()
    except Exception:
        return ""


def check_npm_scripts():
    """Check 1: npm scripts exist"""
    errors = []

    # Load package.json
    pkg = load_json("package.json")
    if not pkg or "scripts" not in pkg:
        errors.append("ERROR: package.json not found or has no scripts section")
        return errors

    available_scripts = set(pkg["scripts"].keys())

    # Find all `npm run X` references in documentation
    doc_paths = list(Path("docs").rglob("*.md")) if os.path.exists("docs") else []
    doc_paths.extend(list(Path(".").glob("AGENTS.md")) if os.path.exists("AGENTS.md") else [])

    for doc_path in doc_paths:
        content = load_text(str(doc_path))
        # Find `npm run X` patterns
        matches = re.findall(r"`npm run (\S+)`", content)
        for script in matches:
            if script not in available_scripts:
                errors.append(
                    f"MISSING_NPM_SCRIPT: {doc_path} references 'npm run {script}' "
                    f"which does not exist in package.json"
                )

    return errors


def check_skill_registry_xref():
    """Check 2: skill IDs cross-ref"""
    errors = []

    # Load both registries from their canonical paths.
    workflow_registry = load_yaml(WORKFLOW_REGISTRY_PATH)
    skill_registry_raw = load_yaml(SKILL_REGISTRY_PATH)

    if not workflow_registry or "workflows" not in workflow_registry:
        # A missing/malformed canonical registry is a hygiene failure, not a
        # reason to skip the check -- silently skipping is what let checks 2
        # and 3 report PASSED while never actually running (S1 finding).
        errors.append(f"ERROR: workflow-registry.yaml not found or malformed at {WORKFLOW_REGISTRY_PATH}")
        return errors

    if not skill_registry_raw or "ecosystems" not in skill_registry_raw:
        errors.append(f"ERROR: skill-registry.yaml not found or malformed at {SKILL_REGISTRY_PATH}")
        return errors

    available_skills = set(flatten_skill_registry(skill_registry_raw).keys())

    # Check each workflow step. Steps reference a skill via the `skill` key
    # (not `skill_id` -- the canonical workflow-registry.yaml schema).
    for workflow in workflow_registry["workflows"]:
        workflow_id = workflow.get("id", "unknown")
        for i, step in enumerate(workflow.get("steps", [])):
            skill_id = step.get("skill")
            if skill_id and skill_id not in available_skills:
                errors.append(
                    f"MISSING_SKILL_ID: workflow '{workflow_id}' step {i} "
                    f"references skill '{skill_id}' which does not exist in skill-registry.yaml"
                )

    return errors


def check_artifact_contracts():
    """Check 3: artifact contracts resolve"""
    errors = []

    # Load registry and contracts from their canonical paths.
    skill_registry_raw = load_yaml(SKILL_REGISTRY_PATH)
    artifact_contracts = load_yaml(ARTIFACT_CONTRACTS_PATH)

    if not skill_registry_raw or "ecosystems" not in skill_registry_raw:
        errors.append(f"ERROR: skill-registry.yaml not found or malformed at {SKILL_REGISTRY_PATH}")
        return errors

    if not artifact_contracts or "artifacts" not in artifact_contracts:
        errors.append(f"ERROR: artifact-contracts.yaml not found or malformed at {ARTIFACT_CONTRACTS_PATH}")
        return errors

    available_artifacts = {a["id"] for a in artifact_contracts["artifacts"]}

    # Each skill declares a single `artifact` field (not
    # `input_artifact_ids`/`output_artifact_ids`, which the canonical
    # skill-registry.yaml schema does not use).
    for skill_id, skill in flatten_skill_registry(skill_registry_raw).items():
        artifact_id = skill.get("artifact")
        if artifact_id and artifact_id not in available_artifacts:
            errors.append(
                f"MISSING_ARTIFACT_CONTRACT: skill '{skill_id}' "
                f"references artifact '{artifact_id}' which does not exist in artifact-contracts.yaml"
            )

    return errors


def main():
    """Run all checks"""
    all_errors = []

    print("Running skill-hygiene validator v1...")
    print()

    # Check 1: npm scripts
    print("Check 1: npm scripts exist...", end=" ")
    npm_errors = check_npm_scripts()
    if npm_errors:
        print(f"FAILED ({len(npm_errors)} errors)")
        all_errors.extend(npm_errors)
    else:
        print("PASSED")

    # Check 2: skill registry cross-ref
    print("Check 2: skill IDs cross-ref...", end=" ")
    skill_errors = check_skill_registry_xref()
    if skill_errors:
        print(f"FAILED ({len(skill_errors)} errors)")
        all_errors.extend(skill_errors)
    else:
        print("PASSED")

    # Check 3: artifact contracts
    print("Check 3: artifact contracts resolve...", end=" ")
    artifact_errors = check_artifact_contracts()
    if artifact_errors:
        print(f"FAILED ({len(artifact_errors)} errors)")
        all_errors.extend(artifact_errors)
    else:
        print("PASSED")

    print()

    # Print all errors
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) found:")
        print()
        for error in all_errors:
            print(f"  • {error}")
        print()
        return 1
    else:
        print("VALIDATION PASSED: All skill-hygiene checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
