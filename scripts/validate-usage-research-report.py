import os
import re
import sys
import argparse

def validate_report(report_path):
    errors = []
    
    if not os.path.exists(report_path):
        return [f"Report file not found: {report_path}"]
        
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Required sections check
    required_sections = [
        "Scenario Tested",
        "Expected Behavior",
        "Actual Behavior",
        "What Worked",
        "Friction Points",
        "Routing Quality",
        "Handoff Quality",
        "Next Test"
    ]

    # Sections that have aliases or are only required in the new format
    optional_or_aliased = {
        "Evidence Excerpts": [],
        "Failure Classification": [],
        "Semantic Quality Score": [],
        "Recommended Maintainer Input": ["Recommended Skill Edits"]
    }
    
    for section in required_sections:
        pattern = rf'## ([\d]+\. )?{re.escape(section)}'
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section: '{section}'")

    for section, aliases in optional_or_aliased.items():
        patterns = [rf'## ([\d]+\. )?{re.escape(section)}']
        patterns.extend([rf'## ([\d]+\. )?{re.escape(alias)}' for alias in aliases])
        
        found = False
        for p in patterns:
            if re.search(p, content, re.IGNORECASE):
                found = True
                break
        
        # If it's a new required section but not found, we only error if it's not a legacy report
        if not found:
            # Check if this is a new standard report (indicated by Score or Classification)
            is_new_standard = "Semantic Quality Score" in content or "Failure Classification" in content
            if is_new_standard:
                errors.append(f"Missing required section in new standard report: '{section}'")
            
    # Check for placeholder text or generic AI tics if possible
    placeholders = ["TODO", "FIXME", "REPLACE_ME", "[INSERT"]
    for p in placeholders:
        if p in content:
            errors.append(f"Placeholder detected: '{p}'")
            
    # Check for absolute paths
    abs_path_patterns = [r'[a-zA-Z]:\\', r'/[Uu]sers/', r'/[Hh]ome/']
    for pattern in abs_path_patterns:
        if re.search(pattern, content):
            errors.append(f"Absolute path detected in report (pattern: {pattern}). All paths must be relative.")

    # Check for Semantic Quality Score format (only for new standard)
    score_match = re.search(r'- \*\*Score\*\*: \[?(\d+)\]?', content)
    if score_match:
        score = int(score_match.group(1))
        if not (0 <= score <= 21):
            errors.append(f"Invalid Semantic Quality Score: {score}. Must be between 0 and 21.")

    # Check for failure classification (only for new standard)
    if "Failure Classification" in content:
        if not re.search(r'- \*\*Classification\*\*: \[?(Structural|Semantic|Boundary|None)\]?', content, re.IGNORECASE):
            errors.append("Missing or invalid 'Failure Classification'. Must be one of: Structural, Semantic, Boundary, None.")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a usage research report artifact.")
    parser.add_argument("report_path", help="Path to the .md report file")
    
    args = parser.parse_args()
    
    validation_errors = validate_report(args.report_path)
    
    if validation_errors:
        print(f"Report validation failed for {args.report_path}:")
        for err in validation_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"Report validation passed for {args.report_path}!")
        sys.exit(0)
