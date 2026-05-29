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

    # Load both registries
    workflow_registry = load_yaml("workflow-orchestrator/references/workflow-registry.yaml")
    skill_registry = load_yaml("workflow-orchestrator/references/skill-registry.yaml")

    if not workflow_registry or "workflows" not in workflow_registry:
        return errors  # Skip if workflow registry doesn't exist

    if not skill_registry or "skills" not in skill_registry:
        errors.append("ERROR: skill-registry.yaml not found or malformed")
        return errors

    available_skills = {s["id"] for s in skill_registry["skills"]}

    # Check each workflow step
    for workflow in workflow_registry["workflows"]:
        workflow_id = workflow.get("id", "unknown")
        for i, step in enumerate(workflow.get("steps", [])):
            skill_id = step.get("skill_id")
            if skill_id and skill_id not in available_skills:
                errors.append(
                    f"MISSING_SKILL_ID: workflow '{workflow_id}' step {i} "
                    f"references skill '{skill_id}' which does not exist in skill-registry.yaml"
                )

    return errors


def check_artifact_contracts():
    """Check 3: artifact contracts resolve"""
    errors = []

    # Load both registries and contracts
    skill_registry = load_yaml("workflow-orchestrator/references/skill-registry.yaml")
    artifact_contracts = load_yaml("workflow-orchestrator/references/artifact-contracts.yaml")

    if not skill_registry or "skills" not in skill_registry:
        return errors  # Skip if skill registry doesn't exist

    if not artifact_contracts or "artifacts" not in artifact_contracts:
        errors.append("ERROR: artifact-contracts.yaml not found or malformed")
        return errors

    available_artifacts = {a["id"] for a in artifact_contracts["artifacts"]}

    # Check each skill's input/output artifacts
    for skill in skill_registry["skills"]:
        skill_id = skill.get("id", "unknown")

        # Check input artifacts
        for artifact_id in skill.get("input_artifact_ids", []):
            if artifact_id not in available_artifacts:
                errors.append(
                    f"MISSING_ARTIFACT_CONTRACT: skill '{skill_id}' "
                    f"references input artifact '{artifact_id}' which does not exist in artifact-contracts.yaml"
                )

        # Check output artifacts
        for artifact_id in skill.get("output_artifact_ids", []):
            if artifact_id not in available_artifacts:
                errors.append(
                    f"MISSING_ARTIFACT_CONTRACT: skill '{skill_id}' "
                    f"references output artifact '{artifact_id}' which does not exist in artifact-contracts.yaml"
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
