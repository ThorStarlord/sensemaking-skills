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

    # 1.1 Failure Mode Class Verification
    fm_match = re.search(r'- \*\*Failure Mode Class\*\*: (Class \d+: [\w\s]+)', content, re.IGNORECASE)
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
        for vc in valid_classes:
            if vc.lower() in fm_class.lower():
                is_valid = True
                break
        if not is_valid:
            errors.append(f"Invalid Failure Mode Class '{fm_class}'. Must be one of the 10 formal classes.")

    # 2. Source Report Verification
    match = re.search(r'- \*\*Source Report\*\*: \[(.*?)\]\((.*?)\)', content)
    if not match:
        errors.append("Missing or malformed Source Report link in Diagnosis/Evidence.")
    else:
        report_rel_path = match.group(2)
        # Check if the path is relative and exists
        if report_rel_path.startswith("file://") or os.path.isabs(report_rel_path):
            errors.append(f"Source Report path must be relative, got: {report_rel_path}")
        else:
            # Plan is likely in examples/usage-research/scenarios/XYZ/
            plan_dir = os.path.dirname(plan_path)
            full_report_path = os.path.normpath(os.path.join(plan_dir, report_rel_path))
            if not os.path.exists(full_report_path):
                 errors.append(f"Source Report not found at: {full_report_path}")

    # 3. Evidence Mapping Check
    if "Evidence Snippet" not in content or ">" not in content:
        errors.append("Missing Evidence Snippet (must include a blockquote with a cite).")

    # 4. Recommended Action Check
    action_match = re.search(r'recommended\W*action\W*:\W*(\w+)', content, re.IGNORECASE)
    if not action_match:
        errors.append("Missing 'Recommended Action' (e.g., skill_edit, fixture_edit, no_skill_change).")
    else:
        action = action_match.group(1).lower()
        valid_actions = ["skill_edit", "fixture_edit", "validator_edit", "registry_edit", "no_skill_change"]
        if action not in valid_actions:
            errors.append(f"Invalid Recommended Action '{action}'. Must be one of: {', '.join(valid_actions)}")

    # 5. Proposed Edits Check (Conditional if action is skill_edit)
    if action_match and action_match.group(1).lower() == "skill_edit":
        if not re.search(r'edit\W*type\W*:', content, re.IGNORECASE):
            errors.append("Proposed edits must specify 'Edit Type' for skill_edit.")
        if not re.search(r'risk\W*level\W*:', content, re.IGNORECASE):
            errors.append("Proposed edits must specify 'Risk Level' for skill_edit.")
    else:
        # For non-skill edits, we still want to see edit_type (e.g., fixture_edit)
        if not re.search(r'edit\W*type\W*:', content, re.IGNORECASE):
            errors.append("Proposed edits must specify 'Edit Type' (e.g., fixture_edit, none).")

    # 6. Anti-Overfitting Check (Mandatory for all)
    if not re.search(r'anti\W*overfitting', content, re.IGNORECASE):
        errors.append("Missing 'Anti-Overfitting Guard' rationale for proposed edits.")

    # 6. Verification Plan Check
    if "Rerun Scenario" not in content:
        errors.append("Verification Plan must specify a 'Rerun Scenario'.")
    if "Success Criteria" not in content:
        errors.append("Verification Plan must specify 'Success Criteria'.")

    # 7. Path Hygiene
    abs_path_patterns = [r'[a-zA-Z]:\\', r'/[Uu]sers/', r'/[Hh]ome/']
    for pattern in abs_path_patterns:
        if re.search(pattern, content):
            errors.append(f"Absolute path detected in plan (pattern: {pattern}). All paths must be relative.")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a skill improvement plan artifact.")
    parser.add_argument("plan_path", help="Path to the .md improvement plan file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    
    args = parser.parse_args()
    
    validation_errors = validate_improvement_plan(args.plan_path, args.repo_root)
    
    if validation_errors:
        print(f"Improvement plan validation failed for {args.plan_path}:")
        for err in validation_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"Improvement plan validation passed for {args.plan_path}!")
        sys.exit(0)
