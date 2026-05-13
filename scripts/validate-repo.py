import os
import yaml
import sys
import re

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
        "skills/workflow-orchestrator/references/workflow-orchestration-template.md",
        "skills/workflow-orchestrator/references/execution-modes.md",
        "skills/problem-framer/SKILL.md",
        "skills/problem-framer/agents/openai.yaml",
        "skills/problem-framer/references/problem-frame-template.md",
        "skills/unknowns-mapper/SKILL.md",
        "skills/unknowns-mapper/agents/openai.yaml",
        "skills/unknowns-mapper/references/unknowns-map-template.md",
        "skills/prompt-handoff/SKILL.md",
        "skills/prompt-handoff/agents/openai.yaml",
        "skills/prompt-handoff/references/prompt-handoff-template.md"
    ]
    
    for f in core_files:
        if not os.path.exists(f):
            errors.append(f"Missing core file: {f}")

    # 2. Validate YAML files
    yaml_files = [
        "skills/repo-sensemaker/agents/openai.yaml",
        "skills/workflow-orchestrator/agents/openai.yaml",
        "skills/workflow-orchestrator/references/skill-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-registry.yaml",
        "skills/problem-framer/agents/openai.yaml",
        "skills/unknowns-mapper/agents/openai.yaml",
        "skills/prompt-handoff/agents/openai.yaml"
    ]
    
    registries = {}
    for yf in yaml_files:
        if os.path.exists(yf):
            try:
                with open(yf, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    registries[yf] = data
            except Exception as e:
                errors.append(f"Invalid YAML in {yf}: {str(e)}")

    # 3. Registry Parity Check
    if "skills/workflow-orchestrator/references/skill-registry.yaml" in registries and \
       "skills/workflow-orchestrator/references/workflow-registry.yaml" in registries:
        
        # Get all registered skill IDs
        skill_registry = registries["skills/workflow-orchestrator/references/skill-registry.yaml"]
        registered_skills = set()
        for ecosystem in skill_registry.get("ecosystems", {}).values():
            for skill in ecosystem.get("skills", []):
                registered_skills.add(skill["id"])
        
        # Check workflow steps
        workflow_registry = registries["skills/workflow-orchestrator/references/workflow-registry.yaml"]
        for workflow in workflow_registry.get("workflows", []):
            for step in workflow.get("steps", []):
                skill_id = step.get("skill")
                if skill_id and skill_id not in registered_skills:
                    errors.append(f"Workflow '{workflow['id']}' references unregistered skill: {skill_id}")

    # 4. Frontmatter Check (Lowercase descriptions)
    skill_files = [
        "skills/repo-sensemaker/SKILL.md",
        "skills/workflow-orchestrator/SKILL.md",
        "skills/problem-framer/SKILL.md",
        "skills/unknowns-mapper/SKILL.md",
        "skills/prompt-handoff/SKILL.md"
    ]
    for sf in skill_files:
        if os.path.exists(sf):
            with open(sf, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'^description:\s*(.*)$', content, re.MULTILINE)
                if match:
                    desc = match.group(1).strip()
                    if desc and desc[0].isupper():
                        errors.append(f"Skill description in {sf} should be lowercase: '{desc}'")

    # 5. Template Section Count Check
    templates = {
        "skills/repo-sensemaker/references/repo-analysis-template.md": 13,
        "skills/workflow-orchestrator/references/workflow-orchestration-template.md": 10,
        "skills/problem-framer/references/problem-frame-template.md": 7,
        "skills/unknowns-mapper/references/unknowns-map-template.md": 6,
        "skills/prompt-handoff/references/prompt-handoff-template.md": 8
    }
    for path, expected_count in templates.items():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                sections = re.findall(r'^## \d+\.', content, re.MULTILINE)
                if len(sections) != expected_count:
                    errors.append(f"Template {path} has {len(sections)} sections, expected {expected_count}")

    # 6. Check examples
    examples_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator", "examples/negative", "examples/problem-framer", "examples/unknowns-mapper", "examples/prompt-handoff"]
    
    # Mandatory Example Directories
    mandatory_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator", "examples/negative"]
    for md in mandatory_dirs:
        if not os.path.exists(md):
            errors.append(f"Missing mandatory example directory: {md}")

    for ex_dir in examples_dirs:
        if os.path.exists(ex_dir):
            files = os.listdir(ex_dir)
            if not any(f.endswith(".md") for f in files):
                 errors.append(f"Example directory {ex_dir} contains no Markdown fixtures")
            
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(ex_dir, f)
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if "## Expected Behavior Checklist" not in content:
                            errors.append(f"Example {f} in {ex_dir} is missing expected behavior checklist")
                        if "file:///" in content:
                            errors.append(f"Example {f} in {ex_dir} contains absolute file:/// paths (use relative links)")

    # 7. Check for stale section counts in README/CONTEXT
    v1_docs = ["README.md", "CONTEXT.md"]
    for doc in v1_docs:
        if os.path.exists(doc):
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                if "11-section" in content or "12-section" in content:
                     # Allow 12-section only if it's not describing the Repo Brief
                     if "11-section" in content or "12-section Repository" in content or "12-section Sensemaking Brief" in content:
                        errors.append(f"Document {doc} contains stale section count references (11 or 12). Should be 13 for Repo Brief.")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Validation passed! Repo is aligned with the hardened V1 artifact contracts.")

if __name__ == "__main__":
    validate_repo()
