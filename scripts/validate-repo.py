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
        "skills/repo-sensemaker/SKILL.md",
        "skills/repo-sensemaker/agents/openai.yaml",
        "skills/repo-sensemaker/references/repo-analysis-template.md",
        "skills/workflow-orchestrator/SKILL.md",
        "skills/workflow-orchestrator/agents/openai.yaml",
        "skills/workflow-orchestrator/references/skill-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-orchestration-template.md"
    ]
    
    for f in core_files:
        if not os.path.exists(f):
            errors.append(f"Missing core file: {f}")

    # 2. Validate YAML files
    yaml_files = [
        "skills/repo-sensemaker/agents/openai.yaml",
        "skills/workflow-orchestrator/agents/openai.yaml",
        "skills/workflow-orchestrator/references/skill-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-registry.yaml"
    ]
    
    for yf in yaml_files:
        if os.path.exists(yf):
            try:
                with open(yf, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except Exception as e:
                errors.append(f"Invalid YAML in {yf}: {str(e)}")

    # 3. Check examples
    examples_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator"]
    for ex_dir in examples_dirs:
        if os.path.exists(ex_dir):
            for f in os.listdir(ex_dir):
                if f.endswith(".md"):
                    path = os.path.join(ex_dir, f)
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if "## Expected Behavior Checklist" not in content:
                            errors.append(f"Example {f} in {ex_dir} is missing expected behavior checklist")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Validation passed! Repo is aligned with two-skill architecture.")

if __name__ == "__main__":
    validate_repo()
