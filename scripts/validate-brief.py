import os
import sys
import yaml
import re
import argparse

def validate_brief(artifact_path, repo_root="."):
    errors = []
    
    if not os.path.exists(artifact_path):
        errors.append(f"Brief file not found: {artifact_path}")
        return errors
        
    with open(artifact_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Extract evidence_excerpts YAML block
    evidence_match = re.search(r'```yaml\s+(evidence_excerpts:.*?)\s+```', content, re.DOTALL | re.IGNORECASE)
    if not evidence_match:
        # Fallback to searching for the list directly if header is different
        evidence_match = re.search(r'```yaml\s+(- file:.*?)\s+```', content, re.DOTALL)
        
    if not evidence_match:
        errors.append("Missing or malformed YAML block for evidence_excerpts. Required for YOLO safety.")
    else:
        try:
            data = yaml.safe_load(evidence_match.group(1))
            # Handle both { evidence_excerpts: [] } and a direct list []
            if isinstance(data, dict):
                excerpts = data.get('evidence_excerpts', [])
            elif isinstance(data, list):
                excerpts = data
            else:
                errors.append("evidence_excerpts block must be a list or a dict containing 'evidence_excerpts'")
                excerpts = []
                
            if not excerpts and "evidence_match" in locals(): # Only error if we found a block but it was empty
                 errors.append("Evidence excerpts list is empty. YOLO mode requires at least one piece of evidence.")
                
            for i, exc in enumerate(excerpts):
                # Check fields
                for field in ['file', 'lines', 'quote', 'supports_claim']:
                    if field not in exc:
                        errors.append(f"Excerpt[{i}] missing required field: {field}")
                
                # Check file existence (Relative to repo_root)
                file_path = exc.get('file')
                if file_path:
                    if file_path.startswith('file:///'):
                        errors.append(f"Excerpt[{i}] uses absolute file:/// path: {file_path}")
                    else:
                        full_path = os.path.join(repo_root, file_path)
                        if not os.path.exists(full_path):
                            errors.append(f"Excerpt[{i}] references non-existent file: {file_path} (Hallucination detected!)")
                
                # Check lines format
                lines = exc.get('lines')
                if lines and not re.match(r'^L\d+(?:-L\d+)?$', str(lines)):
                    errors.append(f"Excerpt[{i}] has invalid lines format: {lines} (Expected Lx or Lx-Ly)")

        except Exception as e:
            errors.append(f"Failed to parse evidence YAML: {e}")

    # 2. Validate recommended_workflow_id against registry
    handoff_match = re.search(r'## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```', content, re.DOTALL | re.IGNORECASE)
    if handoff_match:
        try:
            handoff_data = yaml.safe_load(handoff_match.group(1))
            workflow_id = handoff_data.get('recommended_workflow_id')
            
            if workflow_id:
                registry_path = os.path.join(repo_root, "skills/workflow-orchestrator/references/workflow-registry.yaml")
                if not os.path.exists(registry_path):
                    errors.append(f"Workflow registry not found at {registry_path}. Cannot validate workflow ID.")
                else:
                    with open(registry_path, 'r', encoding='utf-8') as rf:
                        registry = yaml.safe_load(rf)
                        valid_ids = {w['id'] for w in registry.get('workflows', [])}
                        if workflow_id not in valid_ids:
                            errors.append(f"Recommended workflow ID '{workflow_id}' not found in registry (Hallucination detected!)")
            else:
                errors.append("Machine-readable handoff missing 'recommended_workflow_id'")
        except Exception as e:
            errors.append(f"Failed to parse handoff YAML: {e}")
    else:
        errors.append("Missing '13. Machine-readable handoff' YAML block")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specialized validator for repository sensemaking brief.")
    parser.add_argument("artifact_path", help="Path to the brief .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    
    args = parser.parse_args()
    
    errs = validate_brief(args.artifact_path, args.repo_root)
    if errs:
        print(f"Brief verification failed:")
        for e in errs:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("Brief verification passed! Evidence and workflow ID are valid.")
        sys.exit(0)

