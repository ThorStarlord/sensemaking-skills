import os
import sys
import yaml
import re
import argparse

def validate_artifact(artifact_id, artifact_path, repo_root):
    errors = []

    if not os.path.exists(artifact_path):
        errors.append(f"Artifact file not found: {artifact_path}")
        return errors

    # Load contracts
    contracts_path = os.path.join(repo_root, "skills", "workflow-orchestrator", "references", "artifact-contracts.yaml")
    if not os.path.exists(contracts_path):
        errors.append(f"Contracts file not found at {contracts_path}")
        return errors
        
    try:
        with open(contracts_path, 'r', encoding='utf-8') as f:
            contracts_data = yaml.safe_load(f)
    except Exception as e:
        errors.append(f"Failed to parse artifact-contracts.yaml: {e}")
        return errors

    # Find specific contract
    contract = next((a for a in contracts_data.get("artifacts", []) if a["id"] == artifact_id), None)
    if not contract:
        errors.append(f"Contract for artifact_id '{artifact_id}' not found in artifact-contracts.yaml")
        return errors

    # Read artifact content
    with open(artifact_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ban file:/// links
    if "file:///" in content:
        errors.append("Absolute 'file:///' links are banned in generated artifacts. Use relative paths.")

    # 2. Check required sections
    required_sections = contract.get("required_sections", [])
    for section in required_sections:
        # re.escape escapes special chars, but typically not underscore in modern Python.
        # We replace underscore with a character class that matches space, underscore, or hyphen.
        section_regex_part = re.escape(section).replace('_', r'[\s_\-]').replace(r'\_', r'[\s_\-]')
        # Match "## Section Name" or "## section_name" or "## Section-name"
        pattern = rf"^##\s+(?:\d+\.\s+)?{section_regex_part}"
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required section: {section}")

    # 3. Check machine fields in YAML block
    required_fields = contract.get("required_machine_fields", [])
    if required_fields:
        yaml_blocks = re.findall(r'```yaml\s+(.*?)\s+```', content, re.DOTALL)
        if not yaml_blocks:
            errors.append("Missing machine-readable YAML block")
        else:
            found_valid_block = False
            for yaml_text in yaml_blocks:
                try:
                    data = yaml.safe_load(yaml_text)
                    if isinstance(data, dict):
                        # Check if this block has all required fields
                        missing = [f for f in required_fields if f not in data]
                        if not missing:
                            found_valid_block = True
                            break
                except Exception:
                    pass
            
            if not found_valid_block:
                errors.append(f"Could not find a single YAML block containing all required machine fields: {required_fields}")

    # 4. Specific validation for repository_sensemaking_brief
    if artifact_id == "repository_sensemaking_brief":
        # We expect an evidence_excerpts YAML block under that section
        # "## 8. Evidence excerpts\n```yaml\nevidence_excerpts:..."
        evidence_match = re.search(r'evidence_excerpts:.*?```yaml\s+(.*?)\s+```', content, re.DOTALL | re.IGNORECASE)
        # If it doesn't match the specific header layout, just try to find a yaml block containing evidence_excerpts
        if not evidence_match:
            evidence_match = re.search(r'```yaml\s+(evidence_excerpts:.*?)\s+```', content, re.DOTALL)
            
        if not evidence_match:
            errors.append("Missing or malformed YAML block for evidence_excerpts")
        else:
            try:
                evidence_data = yaml.safe_load(evidence_match.group(1))
                excerpts = evidence_data.get('evidence_excerpts', [])
                if not isinstance(excerpts, list):
                    errors.append("evidence_excerpts must be a list of excerpts")
                else:
                    for i, exc in enumerate(excerpts):
                        for f in ['file', 'lines', 'quote', 'supports_claim']:
                            if f not in exc:
                                errors.append(f"evidence_excerpt[{i}] missing field: {f}")
                        if 'file' in exc and exc['file'].startswith('file:///'):
                             errors.append(f"evidence_excerpt[{i}] file path must be relative, got: {exc['file']}")
            except Exception as e:
                errors.append(f"Failed to parse evidence_excerpts YAML: {e}")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate an artifact against its contract.")
    parser.add_argument("artifact_id", help="The ID of the artifact (e.g., repository_sensemaking_brief)")
    parser.add_argument("artifact_path", help="Path to the artifact markdown file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    
    args = parser.parse_args()
    
    validation_errors = validate_artifact(args.artifact_id, args.artifact_path, args.repo_root)
    
    if validation_errors:
        print(f"Artifact validation failed for {args.artifact_path}:")
        for err in validation_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"Artifact validation passed for {args.artifact_path}!")
        sys.exit(0)
