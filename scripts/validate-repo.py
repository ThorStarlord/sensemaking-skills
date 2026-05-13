import os
import yaml
import sys

def validate_repo():
    errors = []
    
    # 1. Check core files
    core_files = [
        "README.md",
        "CONTEXT.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "skills/project-sensemaker/SKILL.md",
        "skills/project-sensemaker/agents/openai.yaml",
        "skills/project-sensemaker/references/skill-registry.yaml",
        "skills/project-sensemaker/references/output-template.md"
    ]
    
    for f in core_files:
        if not os.path.exists(f):
            errors.append(f"Missing core file: {f}")

    # 2. Validate YAML files
    yaml_files = [
        "skills/project-sensemaker/agents/openai.yaml",
        "skills/project-sensemaker/references/skill-registry.yaml"
    ]
    
    for yf in yaml_files:
        if os.path.exists(yf):
            try:
                with open(yf, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except Exception as e:
                errors.append(f"Invalid YAML in {yf}: {str(e)}")

    # 3. Check examples for checklists
    examples_dir = "examples"
    if os.path.exists(examples_dir):
        for f in os.listdir(examples_dir):
            if f.endswith(".md"):
                path = os.path.join(examples_dir, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if "## Expected Behavior Checklist" not in content:
                        errors.append(f"Example {f} is missing expected behavior checklist")
                    if "## 1. Fog Type" not in content or "## 12. Ready-to-Copy Prompt" not in content:
                        errors.append(f"Example {f} does not follow the 12-section template")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Validation passed! Repo is V1 ready.")

if __name__ == "__main__":
    validate_repo()
