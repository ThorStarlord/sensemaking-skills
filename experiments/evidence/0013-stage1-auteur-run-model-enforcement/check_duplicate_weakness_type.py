import re
import sys

def check(brief_path: str) -> int:
    with open(brief_path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not m:
        print("FAIL: no ```yaml fence found in brief")
        return 2
    yaml_block = m.group(1)
    key_lines = [
        line for line in yaml_block.splitlines()
        if re.match(r"^weakness_type\s*:", line.strip())
    ]
    count = len(key_lines)
    if count == 0:
        print("FAIL: no weakness_type key found")
        return 2
    if count > 1:
        print(f"FAIL: duplicate weakness_type key found ({count} occurrences) -- HARD STOP")
        for i, line in enumerate(key_lines, 1):
            print(f"  occurrence {i}: {line.strip()}")
        return 1
    print(f"PASS: exactly one weakness_type key found: {key_lines[0].strip()}")
    return 0

if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
