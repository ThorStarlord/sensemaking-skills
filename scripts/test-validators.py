import os
import subprocess
import sys

def run_test(plan_path):
    cmd = ["python", "scripts/validate-plan.py", plan_path, "--repo-root", "."]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip() + result.stderr.strip()

def main():
    fixtures_dir = "tests/fixtures/plans"
    valid_dir = os.path.join(fixtures_dir, "valid")
    invalid_dir = os.path.join(fixtures_dir, "invalid")
    
    results = []
    
    # Test valid fixtures
    if os.path.exists(valid_dir):
        for f in os.listdir(valid_dir):
            if f.endswith(".md"):
                path = os.path.join(valid_dir, f)
                passed, output = run_test(path)
                results.append({"fixture": f, "type": "valid", "passed": passed, "output": output})
                
    # Test invalid fixtures
    if os.path.exists(invalid_dir):
        for f in os.listdir(invalid_dir):
            if f.endswith(".md"):
                path = os.path.join(invalid_dir, f)
                passed, output = run_test(path)
                # For invalid fixtures, we expect failure (passed == False)
                results.append({"fixture": f, "type": "invalid", "passed": not passed, "output": output})
                
    # Print summary table
    print("| Fixture | Type | Result | Error/Output Snippet |")
    print("| :--- | :--- | :--- | :--- |")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        # Truncate output for table
        snippet = r["output"].replace("\n", " ").split("!")[0]
        if "Plan validation failed" in snippet:
            snippet = snippet.split("Plan validation failed for")[1].split(":")[1].strip()
        print(f"| {r['fixture']} | {r['type']} | {status} | {snippet} |")

if __name__ == "__main__":
    main()
