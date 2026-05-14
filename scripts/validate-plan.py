import os
import yaml
import sys
import re
import argparse

def validate_plan(plan_path, repo_root):
    errors = []
    
    # 1. Load Registries
    registry_base = os.path.join(repo_root, "skills", "workflow-orchestrator", "references")
    workflow_reg_path = os.path.join(registry_base, "workflow-registry.yaml")
    artifact_con_path = os.path.join(registry_base, "artifact-contracts.yaml")
    skill_reg_path = os.path.join(registry_base, "skill-registry.yaml")
    
    try:
        with open(workflow_reg_path, 'r', encoding='utf-8') as f:
            workflow_reg = yaml.safe_load(f)
        with open(artifact_con_path, 'r', encoding='utf-8') as f:
            artifact_con = yaml.safe_load(f)
        with open(skill_reg_path, 'r', encoding='utf-8') as f:
            skill_reg = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading registries: {e}")
        sys.exit(1)

    # 2. Extract Section 11 from Plan
    if not os.path.exists(plan_path):
        print(f"Plan file not found: {plan_path}")
        sys.exit(1)
        
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Match the YAML block in Section 11
    # Looking for "## 11. Machine-readable plan" followed by a yaml code block
    match = re.search(r'## 11\. Machine-readable plan\s+```yaml\s+(.*?)\s+```', content, re.DOTALL | re.IGNORECASE)
    if not match:
        errors.append("Section 11 YAML block not found or malformed.")
        return errors
        
    yaml_text = match.group(1)
    try:
        plan_data = yaml.safe_load(yaml_text)
    except Exception as e:
        errors.append(f"Failed to parse Section 11 YAML: {e}")
        return errors

    # 3. Basic Field Checks
    if plan_data.get("artifact_id") != "workflow_orchestration_plan":
        errors.append(f"artifact_id mismatch: expected 'workflow_orchestration_plan', got '{plan_data.get('artifact_id')}'")
        
    if "status" not in plan_data:
        errors.append("Missing 'status' in Section 11")
        
    chosen_id = plan_data.get("chosen_workflow_id")
    if not chosen_id:
        errors.append("Missing chosen_workflow_id in Section 11")
        return errors
        
    workflow = next((w for w in workflow_reg.get("workflows", []) if w["id"] == chosen_id), None)
    if not workflow:
        errors.append(f"chosen_workflow_id '{chosen_id}' not found in workflow-registry.yaml")
        return errors

    # 4. Path Hygiene Check (No absolute paths in YAML)
    yaml_dump = yaml.dump(plan_data)
    abs_path_patterns = [r'[a-zA-Z]:\\', r'/[Uu]sers/', r'/[Hh]ome/']
    for pattern in abs_path_patterns:
        if re.search(pattern, yaml_dump):
            errors.append(f"Absolute path detected in YAML block (pattern: {pattern}). All paths must be relative.")

    # 5. Execution Mode Check
    exec_mode = plan_data.get("execution_mode")
    if exec_mode not in workflow.get("allowed_execution_modes", []):
        errors.append(f"execution_mode '{exec_mode}' not allowed for workflow '{chosen_id}'")

    # 6. Initial Inputs Check
    plan_inputs = plan_data.get("initial_inputs", [])
    reg_inputs = workflow.get("initial_inputs", [])
    
    plan_input_ids = {i["id"] for i in plan_inputs}
    reg_input_ids = {i["id"] for i in reg_inputs}
    
    if plan_input_ids != reg_input_ids:
        errors.append(f"initial_inputs mismatch: plan has {plan_input_ids}, registry expects {reg_input_ids}")
    
    for i in plan_inputs:
        if "type" not in i or "required" not in i:
            errors.append(f"Initial input '{i.get('id')}' missing 'type' or 'required' fields")

    # 7. Step Validation
    plan_steps = plan_data.get("steps", [])
    reg_steps = workflow.get("steps", [])
    subset_run = plan_data.get("subset_run", False)
    
    if subset_run:
        if not plan_data.get("subset_reason"):
            errors.append("Missing 'subset_reason' for subset_run")
            
        included_ids = plan_data.get("included_steps", [])
        excluded_data = plan_data.get("excluded_steps", [])
        excluded_ids = [s.get("id") for s in excluded_data]
        
        all_reg_ids = [s["id"] for s in reg_steps]
        all_plan_ids = set(included_ids) | set(excluded_ids)
        
        if set(all_reg_ids) != all_plan_ids:
            errors.append(f"Subset mismatch: registry steps {all_reg_ids} not fully accounted for in plan ({all_plan_ids})")

        # Contiguity Check: included_steps must be a contiguous subsequence of registry steps
        if included_ids:
            try:
                first_idx = all_reg_ids.index(included_ids[0])
                last_idx = all_reg_ids.index(included_ids[-1])
                expected_subsequence = all_reg_ids[first_idx:last_idx+1]
                if included_ids != expected_subsequence:
                    errors.append(f"Non-contiguous subset: included_steps {included_ids} is not a contiguous sequence in workflow registry")
            except ValueError as e:
                errors.append(f"Step ID in included_steps not found in registry: {e}")
            
        steps_to_validate = []
        for s_id in included_ids:
            p_step = next((s for s in plan_steps if s["id"] == s_id), None)
            r_step = next((s for s in reg_steps if s["id"] == s_id), None)
            if not p_step:
                errors.append(f"Included step {s_id} missing from 'steps' list")
            elif not r_step:
                errors.append(f"Included step {s_id} not found in registry")
            else:
                steps_to_validate.append((p_step, r_step))
    else:
        if len(plan_steps) != len(reg_steps):
            errors.append(f"Step count mismatch: plan has {len(plan_steps)}, registry expects {len(reg_steps)}")
        steps_to_validate = zip(plan_steps, reg_steps)

    for p_step, r_step in steps_to_validate:
        s_id = p_step.get("id")
        if "status" not in p_step:
            errors.append(f"Step {s_id} missing 'status'")
            
        skill = p_step.get("skill")
        if skill != r_step.get("skill"):
            errors.append(f"Step {s_id} skill mismatch: plan='{skill}', reg='{r_step.get('skill')}'")
            
        s_type = p_step.get("step_type")
        if s_type != r_step.get("step_type"):
            errors.append(f"Step {s_id} step_type mismatch: plan='{s_type}', reg='{r_step.get('step_type')}'")
            
        gate = p_step.get("gate")
        if gate != r_step.get("gate"):
            errors.append(f"Step {s_id} gate mismatch: plan='{gate}', reg='{r_step.get('gate')}'")
            
        p_in_src = p_step.get("input_source")
        r_in_src = r_step.get("input_source")
        if p_in_src != r_in_src:
            errors.append(f"Step {s_id} input_source mismatch: plan='{p_in_src}', reg='{r_in_src}'")
            
        p_in_art = p_step.get("input_artifact")
        r_in_art = r_step.get("input_artifact")
        if p_in_art != r_in_art:
            errors.append(f"Step {s_id} input_artifact mismatch: plan='{p_in_art}', reg='{r_in_art}'")
            
        p_out_art = p_step.get("output_artifact")
        r_out_art = r_step.get("output_artifact")
        if p_out_art != r_out_art:
            errors.append(f"Step {s_id} output_artifact mismatch: plan='{p_out_art}', reg='{r_out_art}'")

        if p_out_art:
            contract = next((a for a in artifact_con.get("artifacts", []) if a["id"] == p_out_art), None)
            if not contract:
                errors.append(f"Step {s_id} output_artifact '{p_out_art}' not found in artifact-contracts.yaml")
            else:
                skill_meta = None
                for ecosystem in skill_reg.get("ecosystems", {}).values():
                    skill_meta = next((s for s in ecosystem.get("skills", []) if s["id"] == skill), None)
                    if skill_meta: break
                
                actual_producer = None
                if skill_meta and skill_meta.get("artifact") == p_out_art:
                    actual_producer = skill
                elif contract.get("produced_by") == skill:
                    actual_producer = skill
                    
                if not actual_producer:
                    errors.append(f"Step {s_id} skill '{skill}' is not contracted to produce '{p_out_art}'")

    # 8. Approval Gates & Behavior Check
    plan_gates = plan_data.get("approval_gates", [])
    step_gates = [s.get("gate") for s in plan_steps if s.get("gate")]
    if plan_gates != step_gates:
        errors.append(f"approval_gates mismatch: plan has {plan_gates}, steps have {step_gates}")
        
    gate_behavior = plan_data.get("gate_behavior", {})
    for g in plan_gates:
        if g not in gate_behavior:
            errors.append(f"Missing gate_behavior for gate '{g}'")
        elif gate_behavior[g] == "simulated_for_research":
            # Check if any step using this gate claims user approval
            for s in plan_steps:
                if s.get("gate") == g and s.get("approved_by_user") is True:
                    errors.append(f"Gate clash: step {s.get('id')} claims 'approved_by_user: true' but gate '{g}' is simulated")

    # 9. Stop Conditions Check
    stop_conds = plan_data.get("stop_conditions", [])
    if not stop_conds or not isinstance(stop_conds, list) or len(stop_conds) == 0:
        errors.append("stop_conditions missing or empty in Section 11")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a workflow orchestration plan artifact.")
    parser.add_argument("plan_path", help="Path to the .md plan file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    
    args = parser.parse_args()
    
    validation_errors = validate_plan(args.plan_path, args.repo_root)
    
    if validation_errors:
        print(f"Plan validation failed for {args.plan_path}:")
        for err in validation_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"Plan validation passed for {args.plan_path}!")
        sys.exit(0)
