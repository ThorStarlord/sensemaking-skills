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
        "Handoff Quality",
        "Routing Quality",
        "Recommended Skill Edits",
        "Next Test"
    ]
    
    for section in required_sections:
        # Match "## [number]. Section Name" or just "## Section Name"
        pattern = rf'## ([\d]+\. )?{re.escape(section)}'
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section: '{section}'")
            
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

    # Specific evidence check for Validation Friction
    if "Validation Evidence" not in content and "Validation Friction" in required_sections:
        # This is a bit looser but we want to encourage evidence
        pass

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
