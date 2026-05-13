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
        "docs/PRD-V1-Sensemaking.md",
        "skills/repo-sensemaker/SKILL.md",
        "skills/repo-sensemaker/agents/openai.yaml",
        "skills/repo-sensemaker/references/repo-analysis-template.md",
        "skills/workflow-orchestrator/SKILL.md",
        "skills/workflow-orchestrator/agents/openai.yaml",
        "skills/workflow-orchestrator/references/skill-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-registry.yaml",
        "skills/workflow-orchestrator/references/workflow-orchestration-template.md",
        "skills/workflow-orchestrator/references/execution-modes.md",
        "skills/workflow-orchestrator/references/artifact-contracts.yaml",
        "skills/problem-framer/SKILL.md",
        "skills/problem-framer/agents/openai.yaml",
        "skills/problem-framer/references/problem-frame-template.md",
        "skills/unknowns-mapper/SKILL.md",
        "skills/unknowns-mapper/agents/openai.yaml",
        "skills/unknowns-mapper/references/unknowns-map-template.md",
        "skills/prompt-handoff/SKILL.md",
        "skills/prompt-handoff/agents/openai.yaml",
        "skills/prompt-handoff/references/prompt-handoff-template.md",
        "skills/setup-sensemaking-skills/SKILL.md",
        "skills/setup-sensemaking-skills/agents/openai.yaml",
        "skills/setup-sensemaking-skills/references/agent-block-template.md",
        "skills/setup-sensemaking-skills/references/sensemaking-config-template.md",
        "skills/setup-sensemaking-skills/references/workflow-modes-template.md",
        "skills/sensemaking-docs-reconciler/SKILL.md",
        "skills/sensemaking-docs-reconciler/agents/openai.yaml"
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
        "skills/workflow-orchestrator/references/artifact-contracts.yaml",
        "skills/problem-framer/agents/openai.yaml",
        "skills/unknowns-mapper/agents/openai.yaml",
        "skills/prompt-handoff/agents/openai.yaml",
        "skills/setup-sensemaking-skills/agents/openai.yaml",
        "skills/sensemaking-docs-reconciler/agents/openai.yaml"
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

    # 3. Registry & Availability Check
    if "skills/workflow-orchestrator/references/skill-registry.yaml" in registries:
        skill_registry = registries["skills/workflow-orchestrator/references/skill-registry.yaml"]
        registered_skills = {}
        for ecosystem_id, ecosystem in skill_registry.get("ecosystems", {}).items():
            for skill in ecosystem.get("skills", []):
                s_id = skill["id"]
                registered_skills[s_id] = skill
                
                # Availability validation
                availability = skill.get("availability")
                if not availability:
                    errors.append(f"Skill '{s_id}' missing 'availability' block in registry")
                else:
                    a_type = availability.get("type")
                    if a_type not in ["local", "external", "prompt_only"]:
                        errors.append(f"Skill '{s_id}' has invalid availability type: {a_type}")

        # 4. Artifact Handoff Validation
        if "skills/workflow-orchestrator/references/artifact-contracts.yaml" in registries and \
           "skills/workflow-orchestrator/references/workflow-registry.yaml" in registries:
            
            contracts = registries["skills/workflow-orchestrator/references/artifact-contracts.yaml"]
            artifacts = contracts.get("artifacts", [])
            producers = {a["produced_by"]: a for a in artifacts}
            consumers = {}
            for artifact in artifacts:
                for consumer in artifact.get("consumed_by", []):
                    consumers.setdefault(consumer, []).append(artifact["id"])
            
            workflow_registry = registries["skills/workflow-orchestrator/references/workflow-registry.yaml"]
            for workflow in workflow_registry.get("workflows", []):
                steps = [s.get("skill") for s in workflow.get("steps", [])]
                for i in range(len(steps) - 1):
                    producer = steps[i]
                    consumer = steps[i + 1]
                    
                    # Validate registry existence
                    if producer not in registered_skills:
                        errors.append(f"Workflow '{workflow['id']}' references unregistered skill: {producer}")
                        continue
                    
                    # Local handoff validation
                    if producer in producers:
                        artifact_id = producers[producer]["id"]
                        if artifact_id not in consumers.get(consumer, []):
                            errors.append(
                                f"Workflow '{workflow['id']}' has invalid handoff: "
                                f"{producer} produces '{artifact_id}', but {consumer} does not declare it as input"
                            )

    # 5. Frontmatter Check (Lowercase descriptions)
    skill_files = [
        "skills/repo-sensemaker/SKILL.md",
        "skills/workflow-orchestrator/SKILL.md",
        "skills/problem-framer/SKILL.md",
        "skills/unknowns-mapper/SKILL.md",
        "skills/prompt-handoff/SKILL.md",
        "skills/setup-sensemaking-skills/SKILL.md",
        "skills/sensemaking-docs-reconciler/SKILL.md"
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

    # 6. Template Section Count Check
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

    # 7. Check examples
    examples_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator", "examples/negative", "examples/pipeline", "examples/problem-framer", "examples/unknowns-mapper", "examples/prompt-handoff"]
    
    # Mandatory Example Directories
    mandatory_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator", "examples/negative", "examples/pipeline"]
    for md in mandatory_dirs:
        if not os.path.exists(md):
            errors.append(f"Missing mandatory example directory: {md}")

    found_orchestration_plans = set()
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
                        
                        # Duplicate fixture check for orchestration plans
                        if ex_dir == "examples/workflow-orchestrator":
                            workflow_match = re.search(r'## \d+\. Chosen workflow\s*(.*)', content, re.IGNORECASE)
                            sequence_match = re.search(r'## \d+\. Skills in sequence\s*([\s\S]*?)(?=##|$)', content, re.IGNORECASE)
                            if workflow_match and sequence_match:
                                key = (workflow_match.group(1).strip().lower(), sequence_match.group(1).strip().lower())
                                if key in found_orchestration_plans:
                                    errors.append(f"Duplicate orchestration fixture found: {f} in {ex_dir} duplicates a previous plan")
                                found_orchestration_plans.add(key)

    # 8. Check for stale section counts in all governance docs
    v1_docs = ["README.md", "CONTEXT.md", "docs/PRD-V1-Sensemaking.md", "CONTRIBUTING.md"]
    for doc in v1_docs:
        if os.path.exists(doc):
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                # Stale section counts
                if "11-section" in content or "12-section" in content:
                     if "11-section" in content or "12-section Repository" in content or "12-section Sensemaking Brief" in content:
                        errors.append(f"Document {doc} contains stale section count references (11 or 12). Should be 13 for Repo Brief.")
                
                # Check for the five core skills mention in PRD/README
                if doc in ["README.md", "docs/PRD-V1-Sensemaking.md"]:
                    required_skills = ["problem-framer", "unknowns-mapper", "repo-sensemaker", "workflow-orchestrator", "prompt-handoff"]
                    for s in required_skills:
                        if s not in content:
                            errors.append(f"Document {doc} is missing mention of required V1 skill: {s}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Validation passed! Repo is aligned with the hardened V1 artifact contracts and availability rules.")

if __name__ == "__main__":
    validate_repo()
