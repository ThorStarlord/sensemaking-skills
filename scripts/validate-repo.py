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
        "skills/workflow-orchestrator/references/git-safety-policy.md",
        "skills/workflow-orchestrator/references/recovery-policy.md",
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
    registered_skills = {}
    if "skills/workflow-orchestrator/references/skill-registry.yaml" in registries:
        skill_registry = registries["skills/workflow-orchestrator/references/skill-registry.yaml"]
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
                    if a_type not in ["local", "local_command", "external", "prompt_only"]:
                        errors.append(f"Skill '{s_id}' has invalid availability type: {a_type}")
                    
                    # Invocation check for local_command
                    if a_type == "local_command":
                        invocation = skill.get("invocation")
                        if not invocation:
                            errors.append(f"Skill '{s_id}' is 'local_command' but missing 'invocation' contract")
                        else:
                            if not invocation.get("command"):
                                errors.append(f"Skill '{s_id}' invocation missing 'command'")

    # 4. Workflow & YOLO Validation
    if "skills/workflow-orchestrator/references/workflow-registry.yaml" in registries:
        workflow_registry = registries["skills/workflow-orchestrator/references/workflow-registry.yaml"]
        for workflow in workflow_registry.get("workflows", []):
            allowed_modes = workflow.get("allowed_execution_modes", [])
            if not allowed_modes:
                 errors.append(f"Workflow '{workflow['id']}' missing 'allowed_execution_modes'")
            
            # YOLO Safety Checks
            if "yolo_execution" in allowed_modes:
                if not workflow.get("branch_policy", {}).get("required"):
                    errors.append(f"Workflow '{workflow['id']}' allows YOLO but missing required branch_policy")
                
                steps = workflow.get("steps", [])
                for step in steps:
                    s_id = step.get("skill")
                    if s_id in registered_skills:
                        s_type = registered_skills[s_id]["availability"]["type"]
                        if s_type not in ["local", "local_command"]:
                            errors.append(f"Workflow '{workflow['id']}' allows YOLO but contains non-executable skill: {s_id}")

            # 4b. Recursive Orchestrator Check & Step Type Validation
            steps = workflow.get("steps", [])
            for step in steps:
                s_id = step.get("skill")
                
                if s_id == "workflow-orchestrator":
                    errors.append(f"Workflow '{workflow['id']}' contains a recursive call to 'workflow-orchestrator'.")
                
                s_type = step.get("step_type")
                if not s_type:
                    errors.append(f"Workflow '{workflow['id']}' step '{s_id}' missing 'step_type'")
                elif s_type not in ["local_execution", "prompt_handoff", "external_routing", "human_review"]:
                    errors.append(f"Workflow '{workflow['id']}' step '{s_id}' has invalid step_type: {s_type}")
                
                if s_id in registered_skills:
                    availability = registered_skills[s_id]["availability"]["type"]
                    if s_type == "local_execution" and availability not in ["local", "local_command"]:
                        errors.append(f"Workflow '{workflow['id']}' step '{s_id}' marked as local_execution but availability is {availability}")

    # 5. Artifact Handoff Validation
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
                
                if producer in producers:
                    artifact_id = producers[producer]["id"]
                    if artifact_id not in consumers.get(consumer, []):
                        errors.append(
                            f"Workflow '{workflow['id']}' has invalid handoff: "
                            f"{producer} produces '{artifact_id}', but {consumer} does not declare it as input"
                        )

    # 6. Frontmatter Check
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
                        errors.append(f"Skill description in {sf} should be lowercase")

    # 7. Template Section Count Check
    templates = {
        "skills/repo-sensemaker/references/repo-analysis-template.md": 13,
        "skills/workflow-orchestrator/references/workflow-orchestration-template.md": 11,
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

    # 8. Check examples
    examples_dirs = ["examples/repo-sensemaker", "examples/workflow-orchestrator", "examples/negative", "examples/pipeline", "examples/problem-framer", "examples/unknowns-mapper", "examples/prompt-handoff"]
    for ex_dir in examples_dirs:
        if os.path.exists(ex_dir):
            files = os.listdir(ex_dir)
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(ex_dir, f)
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if "file:///" in content:
                            errors.append(f"Example {f} in {ex_dir} contains absolute file:/// paths")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Validation passed! Repo is aligned with the hardened V1 artifact contracts, YOLO safety, recursive-free workflows, and local-command execution rules.")

if __name__ == "__main__":
    validate_repo()
