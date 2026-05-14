import os
import sys
import yaml
import re
import argparse

def validate_brief(artifact_path):
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
        return errors

    try:
        data = yaml.safe_load(evidence_match.group(1))
        # Handle both { evidence_excerpts: [] } and a direct list []
        if isinstance(data, dict):
            excerpts = data.get('evidence_excerpts', [])
        elif isinstance(data, list):
            excerpts = data
        else:
            errors.append("evidence_excerpts block must be a list or a dict containing 'evidence_excerpts'")
            return errors
            
        if not excerpts:
            errors.append("Evidence excerpts list is empty. YOLO mode requires at least one piece of evidence.")
            
        for i, exc in enumerate(excerpts):
            # Check fields
            for field in ['file', 'lines', 'quote', 'supports_claim']:
                if field not in exc:
                    errors.append(f"Excerpt[{i}] missing required field: {field}")
            
            # Check file existence (Relative to current dir)
            file_path = exc.get('file')
            if file_path:
                if file_path.startswith('file:///'):
                    errors.append(f"Excerpt[{i}] uses absolute file:/// path: {file_path}")
                elif not os.path.exists(file_path):
                    errors.append(f"Excerpt[{i}] references non-existent file: {file_path} (Hallucination detected!)")
            
            # Check lines format
            lines = exc.get('lines')
            if lines and not re.match(r'^L\d+(?:-L\d+)?$', str(lines)):
                errors.append(f"Excerpt[{i}] has invalid lines format: {lines} (Expected Lx or Lx-Ly)")

    except Exception as e:
        errors.append(f"Failed to parse evidence YAML: {e}")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specialized validator for repository sensemaking brief.")
    parser.add_argument("artifact_path", help="Path to the brief .md file")
    
    args = parser.parse_args()
    
    errs = validate_brief(args.artifact_path)
    if errs:
        print(f"Brief verification failed:")
        for e in errs:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("Brief verification passed! Evidence excerpts are valid and exist on disk.")
        sys.exit(0)
