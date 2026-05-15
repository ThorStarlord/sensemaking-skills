import os
import re
import sys
import yaml
import argparse

def validate_improvement_plan(plan_path, repo_root):
    errors = []
    
    if not os.path.exists(plan_path):
        return [f"Plan file not found: {plan_path}"]
        
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Structural Header Check
    required_sections = [
        "Diagnosis",
        "Evidence",
        "Proposed Edits",
        "Impact Assessment",
        "Verification Plan"
    ]
    
    for section in required_sections:
        pattern = rf'## ([\d]+\. )?{re.escape(section)}'
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section: '{section}'")

    # 1.1 Failure Mode Class Verification (Flexible)
    fm_match = re.search(r'-\s*\*?\*?Failure Mode Class\*?\*?:\s*`?(.*?)`?\s*$', content, re.IGNORECASE | re.MULTILINE)
    if not fm_match:
        # Fallback to "Failure Mode" if Class is missing
        fm_match = re.search(r'-\s*\*?\*?Failure Mode\*?\*?:\s*`?(.*?)`?\s*$', content, re.IGNORECASE | re.MULTILINE)


        
    if not fm_match:
        errors.append("Missing mandatory field '- **Failure Mode Class**: Class X: Name'.")
    else:
        fm_class = fm_match.group(1)
        valid_classes = [
            "Class 1: Input Ambiguity",
            "Class 2: Wrong Routing",
            "Class 3: Artifact Weakness",
            "Class 4: Handoff Failure",
            "Class 5: Boundary Violation",
            "Class 6: Hallucinated Evidence",
            "Class 7: Path Hygiene Error",
            "Class 8: Over-Maintenance",
            "Class 9: Validator Mismatch",
            "Class 10: Status Overclaiming"
        ]
        is_valid = False
        fm_class_clean = fm_class.strip().lower()
        for vc in valid_classes:
            if fm_class_clean == vc.lower():
                is_valid = True
                break
        if not is_valid:
            errors.append(f"Invalid Failure Mode Class '{fm_class}'. Must be an EXACT match for one of the 10 formal classes defined in docs/philosophy/AGENTIC_FAILURE_MODES.md.")


    # 1.2 Defect Source Verification
    ds_match = re.search(r'-\s*\*?\*?Defect Source\*?\*?:\s*`?(\w+)`?', content, re.IGNORECASE)
    if not ds_match:
        errors.append("Missing mandatory field '- **Defect Source**: fixture_defect | validator_defect | registry_defect | consumer_skill_defect | producer_artifact_defect'.")
    else:
        ds = ds_match.group(1).lower()
        valid_sources = ["fixture_defect", "validator_defect", "registry_defect", "consumer_skill_defect", "producer_artifact_defect"]
        if ds not in valid_sources:
            errors.append(f"Invalid Defect Source '{ds}'. Must be one of: {', '.join(valid_sources)}")

    # 2. Source Report Verification
    match = re.search(r'-\s*\*?\*?Source Report\*?\*?:\s*\[(.*?)\]\((.*?)\)', content, re.IGNORECASE)
    if not match:
        # Also try to match non-linked Report ID for legacy support if needed
        match = re.search(r'-\s*\*?\*?(Source Report|Report ID)\*?\*?:\s*(.*)', content, re.IGNORECASE)
        if not match:
            errors.append("Missing mandatory Source Report link: '- **Source Report**: [name](path)'.")
    
    if match and match.lastindex >= 2:
        report_rel_path = match.group(2).strip()
        if report_rel_path.startswith("file://") or os.path.isabs(report_rel_path):
            errors.append(f"Source Report path must be relative, got: {report_rel_path}")
        else:
            plan_dir = os.path.dirname(plan_path)
            full_report_path = os.path.normpath(os.path.join(plan_dir, report_rel_path))
            if not os.path.exists(full_report_path):
                 errors.append(f"Source Report file not found at: {full_report_path}")

    # 3. Evidence Mapping Check
    if "Evidence Snippet" not in content and ">" not in content:
        errors.append("Missing Evidence Snippet (must include a blockquote with a quote from research).")

    # 4. Recommended Action Check
    action_match = re.search(r'-\s*\*?\*?Recommended Action\*?\*?:\s*`?(\w+)`?', content, re.IGNORECASE)
    if not action_match:
        # Fallback to recommended action without list bullet
        action_match = re.search(r'recommended\s*action\s*:\s*`?(\w+)`?', content, re.IGNORECASE)
        
    if not action_match:
        errors.append("Missing 'Recommended Action' (e.g., skill_edit, fixture_edit, no_skill_change).")
    else:
        action = action_match.group(1).lower()
        valid_actions = ["skill_edit", "fixture_edit", "validator_edit", "registry_edit", "no_skill_change"]
        if action not in valid_actions:
            errors.append(f"Invalid Recommended Action '{action}'. Must be one of: {', '.join(valid_actions)}")

    # 5. Proposed Edits Check
    if action_match and action == "skill_edit":
        if not re.search(r'edit\s*\*?\*?type\*?\*?\s*:', content, re.IGNORECASE):
            errors.append("Proposed edits must specify 'Edit Type' (instruction_edit, template_edit).")
        if not re.search(r'risk\s*\*?\*?level\*?\*?\s*:', content, re.IGNORECASE):
            errors.append("Proposed edits must specify 'Risk Level'.")
    
    # 5.1 Do Not Edit Check (Conditional if not skill_edit)
    if action_match and action != "skill_edit":
        if not re.search(r'Do Not Edit', content, re.IGNORECASE) and action != "no_skill_change":
            errors.append(f"Plans with Recommended Action '{action}' should specify a 'Do Not Edit' protection list.")

    # 6. Anti-Overfitting Check (Mandatory for all)
    if not re.search(r'anti[\s\-_]*overfitting', content, re.IGNORECASE):
        errors.append("Missing 'Anti-Overfitting Guard' rationale. Every change must justify why it isn't overfitting to the fixture.")


    # 6. Verification Plan Check
    if not re.search(r'(Rerun Scenario|Scenario)\*?\*?\s*:', content, re.IGNORECASE):
        errors.append("Verification Plan must specify a 'Rerun Scenario'.")
    if not re.search(r'(Success Criteria|Success)\*?\*?\s*:', content, re.IGNORECASE):
        errors.append("Verification Plan must specify 'Success Criteria'.")



    # 7. Path Hygiene
    abs_path_patterns = [r'[a-zA-Z]:\\', r'/[Uu]sers/', r'/[Hh]ome/']
    for pattern in abs_path_patterns:
        if re.search(pattern, content):
            errors.append(f"Absolute path detected in plan: {pattern}. All paths must be repository-relative.")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a skill improvement plan artifact.")
    parser.add_argument("plan_path", help="Path to the .md improvement plan file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    
    args = parser.parse_args()
    
    validation_errors = validate_improvement_plan(args.plan_path, args.repo_root)
    
    if validation_errors:
        print(f"Validation failed for {args.plan_path}:")
        for err in validation_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"Validation passed for {args.plan_path}!")
        sys.exit(0)

